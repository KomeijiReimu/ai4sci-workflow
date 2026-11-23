"""Project CLI for the same start/status functions used by stdio MCP."""

import argparse
import importlib.util
import json
import os
import subprocess
import sys

import server


def main():
    os.umask(0o077)
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('doctor', help='local checks only; does not submit a turn')
    generate = commands.add_parser('generate', help='submit once and return a job ID')
    generate.add_argument('prompt')
    generate.add_argument('--timeout', type=int, default=server.DEFAULT_TIMEOUT_SEC)
    generate.add_argument('--model')
    status = commands.add_parser('status')
    status.add_argument('job_id')
    status.add_argument('--wait', type=int, default=0)
    args = parser.parse_args()
    if args.command == 'doctor':
        binary = server.find_codex_bin()
        print(f'Codex: {binary}\nProject: {server.PROJECT_DIR}\nState/output: {server.STATE_DIR}')
        decoder = importlib.util.find_spec('PIL') is not None
        print(f'Pillow installed: {decoder}; Python: {sys.version.split()[0]}')
        ok = decoder and sys.version_info >= (3, 11)
        if not binary:
            return 1
        for check in (['--version'], ['app-server', '--help'], ['login', 'status']):
            result = subprocess.run([binary, *check], capture_output=True, text=True, timeout=10)
            supports_stdio = check[0] != 'app-server' or 'stdio://' in result.stdout
            info = ('stdio:// supported' if supports_stdio else 'stdio:// not advertised') if check[0] == 'app-server' and not result.returncode else (result.stdout + result.stderr).strip()
            print(f'{" ".join(check)}: exit {result.returncode}: {info}')
            ok &= result.returncode == 0 and supports_stdio
        print('No image requested. Account eligibility is only established by a completed native event and decoded PNG.')
        return 0 if ok else 1
    if args.command == 'generate':
        if not args.prompt.strip():
            parser.error('prompt may not be blank')
        payload, error = server.start_async_generate(args.prompt, model=args.model, timeout_seconds=args.timeout)
    else:
        payload, error = server.get_generate_status(args.job_id, wait_seconds=min(max(args.wait, 0), server.MAX_STATUS_WAIT_SEC))
    print(json.dumps({'error': error} if error else payload, ensure_ascii=False, indent=2))
    return int(payload is None or payload['status'] in ('failed', 'unknown'))


if __name__ == '__main__':
    sys.exit(main())
