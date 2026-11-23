#!/usr/bin/env python3
"""Exercise the checkout's evidence checks on a fresh study without accounts."""
import hashlib
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
        kit = ROOT / 'ai4sci.py'
        for name in ('trapezoid-note.md', 'left-note.md', 'plan.json'):
            shutil.copy2(research / name, dest / name)
        shutil.copy2(EXAMPLE / 'run.py', p)
        # Express the existing four-mesh prediction before this new run. Leave the
        # historical plan and digest in the archive untouched.
        plan_file = dest / 'plan.json'
        plan = json.loads(plan_file.read_bytes())
        criterion = next(item for item in plan['criteria'] if item['id'] == 'K2')
        criterion['required_observations'] = [
            {'path':'research/results.csv', 'key':{'n':str(n)}, 'column':'trap_order',
             'bounds':{'min':1.999999999, 'max':2.000000001}} for n in (8, 16, 32, 64)]
        plan_file.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        run(kit, 'freeze', p, cwd=ROOT)
        run('run.py', cwd=p)
        for name in ('results.csv', 'errors.svg', 'run.json'):
            if (dest / name).read_bytes() != (research / name).read_bytes():
                sys.exit(f'fresh experiment output differs: {name}')
        for name in ('paper.md', 'claims.json'):
            shutil.copy2(research / name, dest / name)
        report = json.loads(run(kit, 'audit', '.', cwd=p))
        outcomes = report['observation_outcomes']['K2']
        if report['deliverability'] != 'ready' or [o['outcome'] for o in outcomes] != ['met']*4:
            sys.exit(str(report))
        print('PASS | checkout CLI: fresh computation, CSV/SVG/run match, manuscript ready')
        table, receipt = dest/'results.csv', dest/'run.json'
        original_table, original_receipt = table.read_bytes(), receipt.read_bytes()
        table.write_bytes(b''.join(line for line in original_table.splitlines(keepends=True)
                                   if not line.startswith((b'16,', b'32,'))))
        record = json.loads(original_receipt)
        record['sha256']['research/results.csv'] = hashlib.sha256(table.read_bytes()).hexdigest()
        receipt.write_text(json.dumps(record), encoding='utf-8')
        missing = json.loads(run(kit, 'audit', p, cwd=ROOT, expect=2))
        if missing['criterion_coverage']['K2'] != {'required_observations':4, 'verified_observations':2}:
            sys.exit(str(missing))
        print('PASS | missing interior meshes rejected despite matching output checksum')
        table.write_bytes(original_table)
        receipt.write_bytes(original_receipt)
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
