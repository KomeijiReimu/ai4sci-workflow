#!/usr/bin/env python3
"""Run research evidence checks from the workflow checkout (Python 3.10+)."""
import argparse
import hashlib
import json
import importlib.util
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
VERSION = '0.1.0'


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--version', action='version', version=VERSION)
    sub = cli.add_subparsers(dest='cmd', required=True)
    sub.add_parser('freeze', help='Record the current plan digest before inspecting formal results').add_argument('project', nargs='?', default='.')
    sub.add_parser('audit', help='Check the manuscript against its evidence').add_argument('project', nargs='?', default='.')
    stats = sub.add_parser('stats', help='Run the upstream statistical risk scanner on named text/code files')
    stats.add_argument('files', nargs='+', type=Path)
    args = cli.parse_args()
    if args.cmd == 'freeze':
        research = Path(args.project) / 'research'
        raw = (research / 'plan.json').read_bytes()
        plan = json.loads(raw)
        if not isinstance(plan, dict) or not plan.get('question') or not plan.get('criteria'):
            raise ValueError('plan.json must specify a question and criteria')
        out = research / 'plan.sha256'
        digest = hashlib.sha256(raw).hexdigest() + '\n'
        if out.exists():
            if out.read_text() != digest:
                raise ValueError('plan changed after freeze: keep the original and document the new analysis separately')
        else:
            with out.open('x') as f:
                f.write(digest)
        print(f'{out}: {digest.strip()}')
        return 0
    if args.cmd == 'audit':
        return subprocess.call([sys.executable, str(ROOT / 'checks/audit.py'), args.project])
    scanner = ROOT / 'vendor/ai4s-desktop/runtime/skills/core/stats-integrity/stats_integrity_check.py'
    spec = importlib.util.spec_from_file_location('ai4sci_stats_scanner', scanner)
    if spec is None or spec.loader is None:
        raise ValueError(f'cannot load statistical checks: {scanner}')
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    files = mod.classify(args.files)
    by_path = {f.path: f.kind for f in files}
    for path in args.files:
        if str(path) not in by_path:
            raise ValueError(f'missing, empty, unreadable or unrecognized statistical input: {path}')
    kinds = set(by_path.values())
    result = mod.run([str(p) for p in args.files])
    result['coverage'] = {
        'causal_wording': 'scanned' if 'report' in kinds else 'not checked: no report',
        'seed': 'scanned' if 'code' in kinds else 'not checked: no code',
        'plan_adherence': 'scanned' if {'code', 'prereg'} <= kinds else 'not checked: supply code and an analysis_plan or prereg text',
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, ValueError) as exc:
        sys.exit(f'ai4sci: {exc}')
