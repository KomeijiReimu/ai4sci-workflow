#!/usr/bin/env python3
"""OpenCode adaptation of the ARIS codex-image2 bridge (see LICENSE and guide.md)."""

from __future__ import annotations

import asyncio
import base64
import io
import json
import os
import re
import shutil
import subprocess
import sys
import time
import traceback
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from native import SubmissionUnknown, request_image


SERVER_NAME = os.environ.get("CODEX_IMAGE2_SERVER_NAME", "codex-image2")
CODEX_BIN = os.environ.get("CODEX_IMAGE2_CODEX_BIN", "codex")
DEFAULT_TIMEOUT_SEC = int(os.environ.get("CODEX_IMAGE2_TIMEOUT_SEC", "600"))
DEFAULT_JOB_EXPIRY_GRACE_SEC = int(
    os.environ.get("CODEX_IMAGE2_JOB_EXPIRY_GRACE_SEC", "60")
)
MAX_STATUS_WAIT_SEC = int(os.environ.get("CODEX_IMAGE2_MAX_STATUS_WAIT_SEC", "30"))
DEFAULT_MODEL = os.environ.get("CODEX_IMAGE2_MODEL", "")
DEBUG_LOG_RAW = os.environ.get("CODEX_IMAGE2_DEBUG_LOG", "").strip()
DEBUG_LOG = Path(DEBUG_LOG_RAW).expanduser() if DEBUG_LOG_RAW else None
SAVE_RUN_LOGS = os.environ.get("CODEX_IMAGE2_SAVE_RUN_LOGS", "").strip().lower() in {
    "1",
    "true",
    "yes",
    "on",
}
PROJECT_DIR = Path(os.environ.get("CODEX_IMAGE2_PROJECT_DIR", os.getcwd())).resolve()
STATE_DIR = PROJECT_DIR / ".local" / "codex-image"
JOBS_DIR = STATE_DIR / "jobs"
RUNS_DIR = STATE_DIR / "runs"

TERMINAL_JOB_STATES = {"completed", "failed", "unknown"}
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
_use_ndjson = False


def debug_log(message: str) -> None:
    if DEBUG_LOG is None:
        return
    try:
        DEBUG_LOG.parent.mkdir(parents=True, exist_ok=True)
        with DEBUG_LOG.open("a", encoding="utf-8") as fh:
            fh.write(f"{message}\n")
    except OSError:
        pass


def send_response(response: dict[str, Any]) -> None:
    global _use_ndjson

    payload = json.dumps(response, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    debug_log(f"SEND {payload.decode('utf-8', errors='replace')}")
    if _use_ndjson:
        sys.stdout.buffer.write(payload + b"\n")
    else:
        header = f"Content-Length: {len(payload)}\r\n\r\n".encode("utf-8")
        sys.stdout.buffer.write(header + payload)
    sys.stdout.buffer.flush()


def read_message() -> dict[str, Any] | None:
    global _use_ndjson

    line = sys.stdin.buffer.readline()
    if not line:
        return None

    line_text = line.decode("utf-8").rstrip("\r\n")
    if line_text.lower().startswith("content-length:"):
        try:
            content_length = int(line_text.split(":", 1)[1].strip())
        except ValueError:
            return None

        while True:
            header_line = sys.stdin.buffer.readline()
            if not header_line:
                return None
            if header_line in {b"\r\n", b"\n"}:
                break

        body = sys.stdin.buffer.read(content_length)
        try:
            return json.loads(body.decode("utf-8"))
        except json.JSONDecodeError:
            return None

    if line_text.startswith("{") or line_text.startswith("["):
        _use_ndjson = True
        try:
            return json.loads(line_text)
        except json.JSONDecodeError:
            return None

    return None


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_utc_timestamp(raw_value: Any) -> datetime | None:
    if not isinstance(raw_value, str) or not raw_value:
        return None
    try:
        return datetime.fromisoformat(raw_value.replace("Z", "+00:00"))
    except ValueError:
        return None


def utc_after_seconds(seconds: int) -> str:
    return (datetime.now(timezone.utc) + timedelta(seconds=seconds)).replace(
        microsecond=0
    ).isoformat().replace("+00:00", "Z")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_suffix(path.suffix + ".tmp")
    temp_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    temp_path.replace(path)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def job_state_path(job_id: str) -> Path:
    return JOBS_DIR / f"{job_id}.json"


def classify_worker_state(pid: int | None) -> str:
    if not pid or pid <= 0:
        return "missing"
    try:
        waited_pid, _ = os.waitpid(pid, os.WNOHANG)
    except ChildProcessError:
        try:
            os.kill(pid, 0)
        except OSError:
            return "exited"
        return "running"
    except OSError:
        return "exited"
    if waited_pid == 0:
        return "running"
    return "exited"


def find_codex_bin() -> str | None:
    if Path(CODEX_BIN).is_file():
        return CODEX_BIN
    return shutil.which(CODEX_BIN)


def normalize_string_list(raw_value: Any) -> tuple[list[str], str | None]:
    if raw_value is None:
        return [], None
    if isinstance(raw_value, str):
        candidate = raw_value.strip()
        return ([candidate] if candidate else []), None
    if not isinstance(raw_value, list):
        return [], "referenceImagePaths must be a string or an array of strings"

    values: list[str] = []
    for item in raw_value:
        if not isinstance(item, str):
            return [], "referenceImagePaths entries must be strings"
        candidate = item.strip()
        if candidate:
            values.append(candidate)
    return values, None


def resolve_cwd(raw_cwd: str | None) -> tuple[Path, str | None]:
    if raw_cwd:
        cwd = Path(raw_cwd).expanduser()
    else:
        cwd = PROJECT_DIR
    try:
        cwd = cwd.resolve()
    except OSError as exc:
        return cwd, f"failed to resolve cwd {raw_cwd!r}: {exc}"
    if not cwd.exists():
        return cwd, f"working directory does not exist: {cwd}"
    if not cwd.is_dir():
        return cwd, f"working directory is not a directory: {cwd}"
    if not cwd.is_relative_to(PROJECT_DIR):
        return cwd, f"working directory must be within {PROJECT_DIR}"
    return cwd, None


def resolve_output_path(raw_output_path: str | None, *, cwd: Path, job_id: str) -> Path:
    if raw_output_path:
        path = Path(raw_output_path).expanduser()
        if not path.is_absolute():
            path = cwd / path
    else:
        path = allowed_output_root(cwd=cwd) / f"codex-image2-{job_id}.png"
    return path.resolve()


def allowed_output_root(*, cwd: Path) -> Path:
    return STATE_DIR / "images"


def validate_output_path(output_path: Path, *, cwd: Path) -> str | None:
    root = allowed_output_root(cwd=cwd)
    try:
        output_path.relative_to(root)
    except ValueError:
        return f"outputPath must stay under {root}"
    if output_path == root:
        return f"outputPath must be a file under {root}, not the directory itself"
    if output_path.exists():
        return f"outputPath already exists; refusing to overwrite: {output_path}"
    return None


def parse_timeout_seconds(raw_value: Any) -> tuple[int | None, str | None]:
    if raw_value is None:
        return DEFAULT_TIMEOUT_SEC, None
    try:
        timeout_sec = int(raw_value)
    except (TypeError, ValueError):
        return None, "timeoutSeconds must be an integer"
    if timeout_sec <= 0:
        return None, "timeoutSeconds must be positive"
    return timeout_sec, None


def is_png_bytes(raw_bytes: bytes) -> bool:
    from PIL import Image
    if not raw_bytes.startswith(PNG_SIGNATURE):
        return False
    try:
        with Image.open(io.BytesIO(raw_bytes)) as image:
            image.verify()
        with Image.open(io.BytesIO(raw_bytes)) as image:
            image.load()
        return True
    except (ValueError, SyntaxError, OSError):
        return False


def maybe_run_log_path(run_id: str) -> Path | None:
    if not SAVE_RUN_LOGS:
        return None
    return RUNS_DIR / f"{run_id}.log"


def scrub_job_request(job: dict[str, Any]) -> None:
    request = job.get("request")
    if not isinstance(request, dict):
        return
    job["request"] = {
        "cwd": request.get("cwd"),
        "outputPath": request.get("outputPath"),
        "timeoutSec": request.get("timeoutSec"),
    }


def fail_job(job_path: Path, job: dict[str, Any], message: str, *, uncertain: bool = False) -> dict[str, Any]:
    finished_at = utc_now()
    job["status"] = "unknown" if uncertain else "failed"
    job["error"] = message
    job["completedAt"] = finished_at
    job["updatedAt"] = finished_at
    job["result"] = None
    if not uncertain:
        scrub_job_request(job)
    write_json(job_path, job)
    return job


def build_bridge_prompt(
    prompt: str,
    *,
    system: str | None,
    reference_image_paths: list[str],
) -> str:
    sections: list[str] = [
        "You are operating behind a Codex native image-generation MCP bridge.",
        "Use native image generation through the Codex app-server.",
        "Do not use shell commands, Python, SVG, HTML, Canvas, or manual bitmap encoding.",
        "Do not fabricate success. If native image generation is unavailable, reply exactly NATIVE_IMAGE_UNAVAILABLE.",
        "Generate exactly one publication-quality raster image unless the user explicitly requests multiple variants.",
        "",
    ]
    selected_system = (system or "").strip()
    if selected_system:
        sections.extend(["## System Instructions", selected_system, ""])
    if reference_image_paths:
        sections.append("## Reference Images")
        sections.append(
            "These local image files are available. If image viewing tools are available in this Codex session, inspect them before generating."
        )
        for path in reference_image_paths:
            sections.append(f"- {path}")
        sections.append("")
    sections.extend(["## User Request", prompt.strip()])
    return "\n".join(sections).strip()


def materialize_generated_image(
    image_item: dict[str, Any],
    output_path: Path,
) -> tuple[Path | None, str | None, str | None, str | None]:
    saved_path_value = image_item.get("savedPath")
    revised_prompt = image_item.get("revisedPrompt")
    revised_prompt_text = revised_prompt if isinstance(revised_prompt, str) else None

    if isinstance(saved_path_value, str) and saved_path_value:
        source_path = Path(saved_path_value).expanduser()
        if source_path.is_file():
            source_bytes = source_path.read_bytes()
            if not is_png_bytes(source_bytes):
                return None, None, None, "imageGeneration savedPath did not contain a PNG image"
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with output_path.open('xb') as out:
                out.write(source_bytes)
            return output_path, str(source_path), revised_prompt_text, None

    raw_result = image_item.get("result")
    if isinstance(raw_result, str) and raw_result.strip():
        try:
            decoded = base64.b64decode(raw_result)
        except ValueError as exc:
            return None, None, None, f"imageGeneration result was not valid base64: {exc}"
        if not is_png_bytes(decoded):
            return None, None, None, "imageGeneration result did not decode to a PNG image"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open('xb') as out:
            out.write(decoded)
        return output_path, None, revised_prompt_text, None

    return None, None, None, "imageGeneration item did not contain a savedPath or decodable result"


def run_codex_image(
    prompt: str,
    *,
    cwd: Path,
    output_path: Path,
    system: str | None = None,
    model: str | None = None,
    reference_image_paths: list[str] | None = None,
    timeout_sec: int | None = None,
    run_log_path: Path | None = None,
    record_attempt=None,
) -> tuple[dict[str, Any] | None, str | None]:
    bin_path = find_codex_bin()
    if not bin_path:
        return None, f"Codex CLI not found: {CODEX_BIN}"

    output_path = output_path.resolve()
    output_path_error = validate_output_path(output_path, cwd=cwd)
    if output_path_error:
        return None, output_path_error

    normalized_refs = reference_image_paths or []
    prompt_text = build_bridge_prompt(
        prompt,
        system=system,
        reference_image_paths=normalized_refs,
    )
    selected_model = model or DEFAULT_MODEL
    effective_timeout = timeout_sec or DEFAULT_TIMEOUT_SEC
    started = time.monotonic()
    if sys.version_info < (3, 11):
        return None, "Python 3.11+ is required. No turn submitted."
    try:
        from PIL import Image  # Require the decoder before submitting a turn.
    except ImportError:
        return None, "Pillow is required for PNG validation. See guide.md. No turn submitted."
    try:
        image_item, thread, turn, response_text = asyncio.run(request_image(
            bin_path, prompt_text, cwd, selected_model, effective_timeout, STATE_DIR / "tmp", run_log_path, record_attempt,
        ))
    except SubmissionUnknown:
        raise
    except (RuntimeError, OSError) as exc:
        return None, str(exc)
    generated_output, source_saved_path, revised_prompt, materialize_error = materialize_generated_image(
        image_item,
        output_path,
    )
    if materialize_error:
        return None, materialize_error
    if generated_output is None:
        return None, "Codex image bridge failed to materialize the generated image"

    return {
        "threadId": thread,
        "turnId": turn,
        "eventId": image_item.get("id"),
        "response": response_text,
        "model": selected_model or None,
        "duration_ms": int((time.monotonic() - started) * 1000),
        "nativeToolConfirmed": True,
        "imageCount": 1,
        "outputPath": str(generated_output),
        "sourceSavedPath": source_saved_path,
        "revisedPrompt": revised_prompt,
        "runLogPath": str(run_log_path) if run_log_path is not None else None,
    }, None


def serialize_job(job: dict[str, Any]) -> dict[str, Any]:
    result = job.get("result") or {}
    attempt = job.get("attempt") or {}
    status, error = job.get('status'), job.get('error')
    # Older job files included raw stderr and prematurely classified reconnect notifications.
    # Present them safely without rewriting the historical evidence.
    if isinstance(error, str) and '; stderr:' in error:
        prefix = error.split('; stderr:', 1)[0]
        ids = re.search(r'; thread=([\w-]+), turn=([\w-]+)', prefix)
        if ids:
            attempt = {'threadId': ids[1], 'turnId': ids[2]}
        if 'Reconnecting' in prefix:
            status = 'unknown'
        error = ('Historical authentication rejection (401); no terminal turn observed.' if 'unauthorized (401)' in prefix
                 else 'Historical app-server error; raw diagnostics withheld.')
    return {
        "jobId": job.get("jobId"),
        "status": status,
        "done": status in TERMINAL_JOB_STATES,
        "threadId": result.get("threadId") or attempt.get("threadId"),
        "turnId": result.get("turnId") or attempt.get("turnId"),
        "eventId": result.get("eventId"),
        "response": result.get("response"),
        "model": result.get("model"),
        "duration_ms": result.get("duration_ms"),
        "nativeToolConfirmed": result.get("nativeToolConfirmed"),
        "imageCount": result.get("imageCount"),
        "outputPath": result.get("outputPath"),
        "sourceSavedPath": result.get("sourceSavedPath"),
        "revisedPrompt": result.get("revisedPrompt"),
        "runLogPath": result.get("runLogPath"),
        "error": error,
        "createdAt": job.get("createdAt"),
        "startedAt": job.get("startedAt"),
        "completedAt": job.get("completedAt"),
        "updatedAt": job.get("updatedAt"),
        "expiresAt": job.get("expiresAt"),
        "resumeHint": (f"Do not resubmit. Inspect {job_state_path(job['jobId'])} and reconcile the original turn."
                       if status == "unknown" else "Call generate_status with this jobId until done=true."),
    }


def start_async_generate(
    prompt: str,
    *,
    cwd: str | None = None,
    output_path: str | None = None,
    system: str | None = None,
    model: str | None = None,
    reference_image_paths: Any = None,
    timeout_seconds: Any = None,
) -> tuple[dict[str, Any] | None, str | None]:
    resolved_cwd, cwd_error = resolve_cwd(cwd)
    if cwd_error:
        return None, cwd_error

    refs, refs_error = normalize_string_list(reference_image_paths)
    if refs_error:
        return None, refs_error

    timeout_sec, timeout_error = parse_timeout_seconds(timeout_seconds)
    if timeout_error:
        return None, timeout_error
    assert timeout_sec is not None

    job_id = uuid.uuid4().hex
    resolved_output_path = resolve_output_path(output_path, cwd=resolved_cwd, job_id=job_id)
    output_path_error = validate_output_path(resolved_output_path, cwd=resolved_cwd)
    if output_path_error:
        return None, output_path_error
    created_at = utc_now()
    job = {
        "jobId": job_id,
        "status": "queued",
        "createdAt": created_at,
        "startedAt": None,
        "completedAt": None,
        "updatedAt": created_at,
        "expiresAt": utc_after_seconds(timeout_sec + DEFAULT_JOB_EXPIRY_GRACE_SEC),
        "error": None,
        "result": None,
        "workerPid": None,
        "request": {
            "prompt": prompt,
            "cwd": str(resolved_cwd),
            "outputPath": str(resolved_output_path),
            "system": system,
            "model": model,
            "referenceImagePaths": refs,
            "timeoutSec": timeout_sec,
        },
    }

    job_path = job_state_path(job_id)
    write_json(job_path, job)

    try:
        worker = subprocess.Popen(
            [sys.executable, str(Path(__file__).resolve()), "--run-job", job_id],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            close_fds=True,
            start_new_session=True,
        )
    except OSError as exc:
        job["status"] = "failed"
        job["completedAt"] = utc_now()
        job["updatedAt"] = job["completedAt"]
        job["error"] = f"Failed to launch background image worker: {exc}"
        write_json(job_path, job)
        return None, job["error"]

    debug_log(f"JOB_START job_id={job_id} worker_pid={worker.pid}")
    return serialize_job(job), None


def get_generate_status(job_id: str, *, wait_seconds: int = 0) -> tuple[dict[str, Any] | None, str | None]:
    if Path(job_id).name != job_id:
        return None, "Invalid jobId"
    job_path = job_state_path(job_id)
    if not job_path.exists():
        return None, f"Unknown jobId: {job_id}"

    deadline = time.monotonic() + max(wait_seconds, 0)
    while True:
        job = read_json(job_path)
        if job.get("status") in {"queued", "running"}:
            expires_at = parse_utc_timestamp(job.get("expiresAt"))
            uncertain = bool(job.get("attempt"))
            if expires_at is not None and datetime.now(timezone.utc) > expires_at:
                job = fail_job(job_path, job, "Background image worker exceeded its deadline before writing a final result", uncertain=uncertain)
            elif job.get("status") == "running":
                worker_state = classify_worker_state(job.get("workerPid"))
                if worker_state in {"missing", "exited"}:
                    job = fail_job(job_path, job, "Background image worker exited before writing a final result", uncertain=uncertain)
        if job.get("status") in TERMINAL_JOB_STATES:
            return serialize_job(job), None
        if time.monotonic() >= deadline:
            return serialize_job(job), None
        time.sleep(min(0.5, max(deadline - time.monotonic(), 0.0)))


def run_async_job(job_id: str) -> int:
    job_path = job_state_path(job_id)
    if not job_path.exists():
        debug_log(f"JOB_MISSING job_id={job_id}")
        return 1

    job = read_json(job_path)
    if job['status'] != 'queued':
        return 1  # Never replay an existing attempt.
    job["status"] = "running"
    job["startedAt"] = utc_now()
    job["updatedAt"] = job["startedAt"]
    job["workerPid"] = os.getpid()
    write_json(job_path, job)
    debug_log(f"JOB_RUNNING job_id={job_id} worker_pid={os.getpid()}")

    request = job.get("request") or {}
    run_log_path = maybe_run_log_path(job_id)
    def record_attempt(phase, thread, turn):
        if read_json(job_path)['status'] != 'running':
            raise SubmissionUnknown('Job is no longer running; inspect the existing record')
        job['attempt'] = {'phase': phase, 'threadId': thread, 'turnId': turn}
        job['updatedAt'] = utc_now()
        write_json(job_path, job)

    uncertain = False
    try:
        payload, error = run_codex_image(
            str(request.get("prompt", "")),
            cwd=Path(str(request.get("cwd"))),
            output_path=Path(str(request.get("outputPath"))),
            system=request.get("system"),
            model=request.get("model"),
            reference_image_paths=request.get("referenceImagePaths") or [],
            timeout_sec=request.get("timeoutSec"),
            run_log_path=run_log_path,
            record_attempt=record_attempt,
        )
    except Exception as exc:
        payload = None
        uncertain = isinstance(exc, SubmissionUnknown) or bool(job.get('attempt'))
        error = str(exc)
        debug_log(traceback.format_exc())

    finished_at = utc_now()
    job = read_json(job_path)
    if job['status'] in TERMINAL_JOB_STATES:
        return 1
    job["updatedAt"] = finished_at
    job["completedAt"] = finished_at
    if error:
        fail_job(job_path, job, error, uncertain=uncertain)
        debug_log(f"JOB_FAILED job_id={job_id} error={error}")
        return 1

    job["status"] = "completed"
    job["error"] = None
    job["result"] = payload
    scrub_job_request(job)
    write_json(job_path, job)
    debug_log(f"JOB_COMPLETED job_id={job_id} output={(payload or {}).get('outputPath')}")
    return 0


def tool_success(request_id: Any, payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "result": {
            "content": [{"type": "text", "text": json.dumps(payload, ensure_ascii=False)}],
        },
    }


def tool_error(request_id: Any, message: str) -> dict[str, Any]:
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "result": {
            "content": [{"type": "text", "text": json.dumps({"error": message}, ensure_ascii=False)}],
            "isError": True,
        },
    }


def handle_request(request: dict[str, Any]) -> dict[str, Any] | None:
    request_id = request.get("id")
    method = request.get("method", "")
    params = request.get("params", {})
    if DEBUG_LOG is not None:
        param_keys = sorted(params.keys()) if isinstance(params, dict) else []
        debug_log(f"REQUEST id={request_id!r} method={method} param_keys={param_keys}")

    if request_id is None:
        if method in {"notifications/initialized", "initialized"}:
            return None
        return None

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": SERVER_NAME, "version": "0.1.0"},
            },
        }

    if method == "ping":
        return {"jsonrpc": "2.0", "id": request_id, "result": {}}

    if method == "resources/list":
        return {"jsonrpc": "2.0", "id": request_id, "result": {"resources": []}}

    if method == "resources/templates/list":
        return {"jsonrpc": "2.0", "id": request_id, "result": {"resourceTemplates": []}}

    if method in {"notifications/initialized", "initialized"}:
        return {"jsonrpc": "2.0", "id": request_id, "result": {}}

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "tools": [
                    {
                        "name": "generate_start",
                        "description": "Start a background native image generation job through the Codex app-server.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "prompt": {"type": "string", "description": "Image generation prompt"},
                                "cwd": {"type": "string", "description": "Optional working directory"},
                                "outputPath": {"type": "string", "description": "Optional PNG file path inside .local/codex-image/images"},
                                "system": {"type": "string", "description": "Optional extra bridge instructions"},
                                "model": {"type": "string", "description": "Optional Codex text model override"},
                                "referenceImagePaths": {
                                    "oneOf": [
                                        {"type": "string"},
                                        {"type": "array", "items": {"type": "string"}},
                                    ],
                                    "description": "Optional local reference image paths that Codex may inspect before generating",
                                },
                                "timeoutSeconds": {
                                    "type": "integer",
                                    "description": "Optional positive timeout for the underlying Codex image call",
                                },
                            },
                            "required": ["prompt"],
                        },
                    },
                    {
                        "name": "generate_status",
                        "description": "Check whether a background image generation job has finished and fetch the output path when available.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "jobId": {"type": "string", "description": "Background image job id"},
                                "job_id": {"type": "string", "description": "Alias of jobId"},
                                "waitSeconds": {
                                    "type": "integer",
                                    "description": "Optional bounded wait before returning status; capped to keep the MCP server responsive",
                                },
                            },
                            "required": ["jobId"],
                        },
                    },
                ]
            },
        }

    if method == "tools/call":
        name = params.get("name", "")
        args = params.get("arguments", {})
        if not isinstance(args, dict):
            return tool_error(request_id, "tool arguments must be an object")

        if name == "generate_start":
            prompt = str(args.get("prompt", "")).strip()
            if not prompt:
                return tool_error(request_id, "prompt is required")
            payload, error = start_async_generate(
                prompt,
                cwd=args.get("cwd"),
                output_path=args.get("outputPath"),
                system=args.get("system"),
                model=args.get("model"),
                reference_image_paths=args.get("referenceImagePaths"),
                timeout_seconds=args.get("timeoutSeconds"),
            )
            if error:
                return tool_error(request_id, error)
            return tool_success(request_id, payload or {})

        if name == "generate_status":
            job_id = args.get("jobId") or args.get("job_id")
            if not job_id:
                return tool_error(request_id, "jobId or job_id is required")
            wait_seconds = args.get("waitSeconds", 0)
            try:
                wait_seconds = int(wait_seconds)
            except (TypeError, ValueError):
                wait_seconds = 0
            wait_seconds = min(max(wait_seconds, 0), MAX_STATUS_WAIT_SEC)
            payload, error = get_generate_status(str(job_id), wait_seconds=wait_seconds)
            if error:
                return tool_error(request_id, error)
            return tool_success(request_id, payload or {})

        return tool_error(request_id, f"unknown tool: {name}")

    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {"code": -32601, "message": f"Unknown method: {method}"},
    }


def main() -> int:
    os.umask(0o077)
    if len(sys.argv) == 3 and sys.argv[1] == "--run-job":
        return run_async_job(sys.argv[2])

    while True:
        request = read_message()
        if request is None:
            return 0
        response = handle_request(request)
        if response is not None:
            send_response(response)


if __name__ == "__main__":
    raise SystemExit(main())
