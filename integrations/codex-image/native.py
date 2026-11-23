"""One Codex v2 stdio turn. Never approve a server request or replay a turn."""

import asyncio
import json
import os
from contextlib import suppress
from pathlib import Path


class SubmissionUnknown(RuntimeError):
    """A turn may have run, but its outcome was not received."""


class NativeFailure(RuntimeError):
    """Explicit protocol rejection or invalid completed output."""


def rejection_summary(detail):
    # Never publish raw RPC error messages, additionalDetails, or app-server stderr.
    normalized = json.dumps(detail).lower()
    if 'unauthorized (401)' in normalized or '"httpstatuscode": 401' in normalized:
        return 'authentication rejected (401)'
    return 'Codex reported a provider or transport error'


async def request_image(binary, prompt, cwd, model, timeout, scratch, run_log, record_attempt=None):
    scratch.mkdir(mode=0o700, parents=True, exist_ok=True)
    with open(os.devnull, 'wb') as stderr:
        proc = await asyncio.create_subprocess_exec(
            binary, '--disable', 'shell_tool', 'app-server', '--listen', 'stdio://',
            cwd=cwd, env={**os.environ, 'TMPDIR': str(scratch)},
            stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE,
            stderr=stderr, limit=64 * 1024 * 1024,
        )
        writer, reader = proc.stdin, proc.stdout
        assert writer is not None and reader is not None
        def send(msg):
            writer.write(json.dumps(msg).encode() + b'\n')

        thread = turn = image = None
        submitted = False
        retry_notice = None
        text = ''
        events = []
        try:
            async with asyncio.timeout(timeout):
                send({'id': 1, 'method': 'initialize', 'params': {
                    'clientInfo': {'name': 'codex-image2', 'version': '1.0'},
                    'capabilities': {'experimentalApi': True},
                }})
                while raw := await reader.readline():
                    msg = json.loads(raw)
                    method = msg.get('method')
                    if method and 'id' in msg:
                        raise RuntimeError(f'Unexpected app-server request: {method}; no approval granted')
                    if 'error' in msg:
                        raise NativeFailure(f'app-server rejected RPC {msg.get("id")}: {rejection_summary(msg["error"])}')
                    params = msg.get('params') or {}
                    if msg.get('id') == 1:
                        send({'method': 'initialized', 'params': {}})
                        options = {'cwd': str(cwd), 'sandbox': 'read-only', 'approvalPolicy': 'never', 'ephemeral': True}
                        if model:
                            options['model'] = model
                        send({'id': 2, 'method': 'thread/start', 'params': options})
                    elif msg.get('id') == 2:
                        thread = msg['result']['thread']['id']
                        if record_attempt:
                            record_attempt('submitting', thread, None)
                        submitted = True
                        send({'id': 3, 'method': 'turn/start', 'params': {
                            'threadId': thread, 'input': [{'type': 'text', 'text': prompt}],
                        }})
                    elif msg.get('id') == 3:
                        turn = msg['result']['turn']['id']
                        if record_attempt:
                            record_attempt('accepted', thread, turn)
                    elif thread and params.get('threadId') == thread:
                        if method == 'error' and turn is not None and params.get('turnId') == turn:
                            summary = rejection_summary(params.get('error'))
                            if params.get('willRetry') is False:
                                raise NativeFailure(f'{summary}; Codex reported willRetry=false')
                            retry_notice = summary  # Continue observing this same turn, never send a second one.
                        if method in ('item/started', 'item/completed') and params.get('turnId') == turn:
                            item = params['item']
                            kind = item['type']
                            events.append({'method': method, 'type': kind, 'id': item.get('id')})
                            if kind in ('commandExecution', 'fileChange', 'mcpToolCall', 'dynamicToolCall'):
                                raise RuntimeError(f'Unexpected {kind}; only native image generation is accepted')
                            if method == 'item/completed' and kind == 'agentMessage':
                                text = item['text']
                            if method == 'item/completed' and kind == 'imageGeneration':
                                if item.get('status') != 'completed':
                                    raise RuntimeError(f'imageGeneration status: {item.get("status")}')
                                if image is not None:
                                    raise RuntimeError('Multiple completed imageGeneration items; expected one')
                                image = item
                        if method == 'turn/completed' and params['turn']['id'] == turn:
                            if params['turn']['status'] != 'completed':
                                raise NativeFailure(f'Codex turn {params["turn"]["status"]}: {rejection_summary(params["turn"].get("error"))}')
                            if not image:
                                raise NativeFailure('No completed native imageGeneration event.')
                            return image, thread, turn, text
                raise RuntimeError('Codex app-server closed stdout before completion')
        except Exception as exc:
            if isinstance(exc, TimeoutError):
                message = f'Codex timed out after {timeout}s'
            elif isinstance(exc, RuntimeError):
                message = str(exc)
            else:
                message = 'Codex app-server protocol or I/O error'
            reason = SubmissionUnknown if submitted and not isinstance(exc, NativeFailure) else NativeFailure
            if retry_notice and reason is SubmissionUnknown:
                message += f'; last non-terminal notice: {retry_notice}'
            raise reason(f'{message}; thread={thread}, turn={turn}') from exc
        finally:
            if proc.returncode is None:
                with suppress(ProcessLookupError):  # Process can exit between EOF and waitpid.
                    proc.terminate()
            try:
                await asyncio.wait_for(proc.wait(), timeout=3)
            except TimeoutError:
                with suppress(ProcessLookupError):
                    proc.kill()
                await proc.wait()
            if run_log:
                Path(run_log).parent.mkdir(parents=True, exist_ok=True)
                Path(run_log).write_text(json.dumps({'threadId': thread, 'turnId': turn, 'events': events}, indent=2))
