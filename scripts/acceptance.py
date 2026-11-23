#!/usr/bin/env python3
"""Install into a new study and exercise the public user path without accounts."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / 'examples/quadrature'


def run(*args, cwd, expect=0):
    result = subprocess.run([sys.executable, *args], cwd=cwd, text=True, capture_output=True)
    if result.returncode != expect:
        sys.exit(f'{args}: expected {expect}, got {result.returncode}\n{result.stdout}\n{result.stderr}')
    return result.stdout


def main():
    scratch = ROOT / '.local' / 'tmp'
    scratch.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=scratch) as temp:
        p = Path(temp)
        dest = p / 'research'
        dest.mkdir()
        research = EXAMPLE / 'research'
        run(ROOT / 'ai4sci.py', 'init', p, cwd=p)
        kit = p / '.ai4sci-kit' / 'ai4sci.py'
        for name in ('trapezoid-note.md', 'left-note.md', 'plan.json'):
            shutil.copy2(research / name, dest / name)
        shutil.copy2(EXAMPLE / 'run.py', p)
        run(kit, 'freeze', '.', cwd=p)
        run('run.py', cwd=p)
        for name in ('results.csv', 'errors.svg', 'run.json'):
            if (dest / name).read_bytes() != (research / name).read_bytes():
                sys.exit(f'fresh experiment output differs: {name}')
        for name in ('paper.md', 'claims.json'):
            shutil.copy2(research / name, dest / name)
        report = json.loads(run(kit, 'audit', '.', cwd=p))
        if report['deliverability'] != 'ready':
            sys.exit(str(report))
        print('PASS | installed kit: fresh computation, CSV/SVG/run match, manuscript ready')
        paper = dest / 'paper.md'
        original = paper.read_text()
        paper.write_text(original.replace('0.3359375', '0.7359375'))
        claims = dest / 'claims.json'
        # Make paper + ledger agree on the WRONG result. Only raw evidence can catch this.
        claims.write_text(claims.read_text().replace('0.3359375', '0.7359375'))
        wrong = json.loads(run(kit, 'audit', '.', cwd=p, expect=2))
        if wrong['claims'].get('C1') != 'invalid':
            sys.exit(str(wrong))
        print('PASS | aligned but wrong manuscript and ledger rejected against raw data (C1)')
        (dest / 'plan.json').write_bytes((dest / 'plan.json').read_bytes() + b'\n')
        run(kit, 'audit', '.', cwd=p, expect=2)
        run(kit, 'freeze', '.', cwd=p, expect=1)
        print('PASS | changed plan refused; original digest preserved')
        lit = json.loads(run(kit, 'audit', ROOT / 'examples/source-audit', cwd=p))
        if lit.get('scientific_run') != 'not-applicable' or lit['deliverability'] != 'ready':
            sys.exit(str(lit))
        print('PASS | Chinese literature-only synthesis checked without inventing an experiment')


if __name__ == '__main__':
    main()
