#!/usr/bin/env python3
"""Install a project-local research kit or run its evidence checks (Python 3.10+)."""
import argparse
import hashlib
import json
import importlib.util
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
VERSION = '0.1.0'


def install(target):
    target = Path(target).expanduser().resolve()
    if target == ROOT or ROOT.name == '.ai4sci-kit':
        raise ValueError('Run init from the distribution checkout and select a separate project directory.')
    payload = {Path('.ai4sci-kit/ai4sci.py'): ROOT / 'ai4sci.py'}
    for name in ['skills', 'checks', 'templates', 'vendor', 'integrations', 'licenses']:
        for src in sorted((ROOT / name).rglob('*')):
            if not src.is_file() or '__pycache__' in src.parts or src.suffix == '.pyc':
                continue
            dest = (Path('.opencode/skills') / src.relative_to(ROOT / 'skills') if name == 'skills'
                    else Path('.ai4sci-kit') / src.relative_to(ROOT))
            payload[dest] = src
    for name in ['LICENSE', 'SOURCES.md']:
        payload[Path('.ai4sci-kit') / name] = ROOT / name
    blobs = {rel: src.read_bytes() for rel, src in payload.items()}
    hashes = {str(p): hashlib.sha256(b).hexdigest() for p, b in blobs.items()}
    blobs[Path('.ai4sci-kit/manifest.json')] = (json.dumps({'version': VERSION, 'sha256': hashes}, indent=2) + '\n').encode()
    # Check the whole install first: never half-apply a known collision in an existing project.
    missing = []
    for rel, data in blobs.items():
        dest = target / rel
        if any(p.is_symlink() for p in [dest, *dest.parents] if p != target and p.is_relative_to(target)):
            raise ValueError(f'symlink at install destination: {rel}')
        if any(p.exists() and not p.is_dir() for p in dest.parents if p.is_relative_to(target)):
            raise ValueError(f'parent is not a directory: {rel}')
        if dest.exists():
            if not dest.is_file() or dest.read_bytes() != data:
                raise ValueError(f'conflicting file (not overwritten): {rel}')
        else:
            missing.append((dest, data))
    for dest, data in missing:
        dest.parent.mkdir(parents=True, exist_ok=True)
        with dest.open('xb') as out:
            out.write(data)
    print(f'AI4Sci {VERSION}: {target} ({len(missing)} files installed). Open this project in OpenCode and request ai4sci.')


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--version', action='version', version=VERSION)
    sub = cli.add_subparsers(dest='cmd', required=True)
    sub.add_parser('init', help='Install skills and tools without replacing existing project files').add_argument('project')
    sub.add_parser('freeze', help='Record the current plan digest before inspecting formal results').add_argument('project', nargs='?', default='.')
    sub.add_parser('audit', help='Check the manuscript against its evidence').add_argument('project', nargs='?', default='.')
    stats = sub.add_parser('stats', help='Run the upstream statistical risk scanner on named text/code files')
    stats.add_argument('files', nargs='+', type=Path)
    args = cli.parse_args()
    if args.cmd == 'init':
        install(args.project)
        return 0
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
