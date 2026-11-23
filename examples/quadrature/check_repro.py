"""Check independent regeneration, read-only repeat and mismatch handling."""

import hashlib
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def main():
    root = Path(__file__).resolve().parent
    research = root / 'research'
    digest = hashlib.sha256((research / 'plan.json').read_bytes()).hexdigest()
    if (research / 'plan.sha256').read_bytes() != (digest + '\n').encode():
        raise SystemExit('Plan differs from frozen digest')
    stage = Path(tempfile.mkdtemp(prefix='.quadrature-check-', dir=root))
    print(f'Checking in {stage} (retained on failure)', flush=True)
    shutil.copyfile(root / 'run.py', stage / 'run.py')
    cmd = [sys.executable, 'run.py']
    subprocess.run(cmd, cwd=stage, check=True)
    files = [stage / 'research' / name for name in ('results.csv', 'errors.svg', 'run.json')]
    for path in files:
        if path.read_bytes() != (research / path.name).read_bytes():
            raise SystemExit(f'Clean reproduction differs: {path.name}')
    before = {p: (p.read_bytes(), p.stat().st_mtime_ns) for p in files}
    subprocess.run(cmd, cwd=stage, check=True)
    if any((p.read_bytes(), p.stat().st_mtime_ns) != before[p] for p in files):
        raise SystemExit('Repeat run modified an artifact')

    # Tamper only with this private, newly created copy.
    files[0].write_bytes(b'preserve this differing result\n')
    before = {p: (p.read_bytes(), p.stat().st_mtime_ns) for p in files}
    rejected = subprocess.run(cmd, cwd=stage, capture_output=True, text=True)
    if rejected.returncode == 0 or 'Refusing to replace differing artifact' not in rejected.stderr:
        raise SystemExit(f'Unexpected mismatch response: {rejected}')
    if any((p.read_bytes(), p.stat().st_mtime_ns) != before[p] for p in files):
        raise SystemExit('Rejected run modified an artifact')
    for path in files:
        path.unlink()
    (stage / 'research').rmdir()
    (stage / 'run.py').unlink()
    stage.rmdir()
    print('PASS: plan digest, clean reproduction, unchanged repeat, mismatch refusal')


if __name__ == '__main__':
    main()
