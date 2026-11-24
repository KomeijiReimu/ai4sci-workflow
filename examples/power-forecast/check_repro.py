"""Recreate aggregates and figure in an ignored directory, compare bytes, run kit audit."""
import argparse
import gzip
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.request import Request, urlopen

from study import BASE, FILE, INPUT_SHA, digest


def main():
    here = Path(__file__).resolve().parent
    kit = here.parents[1]
    cache = kit/'.local/power-forecast'
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--archive', type=Path, default=cache/FILE, help='official uncompressed hourly single-index file')
    ap.add_argument('--download', action='store_true', help='fetch the official version if the archive is absent')
    args = ap.parse_args()
    archive = args.archive.expanduser().resolve()
    if not archive.exists():
        if not args.download:
            ap.error(f'Missing {archive}; add --download to fetch it.')
        archive.parent.mkdir(exist_ok=True, parents=True)
        partial = archive.with_suffix('.csv.partial')
        request = Request(BASE + FILE, headers={'Accept-Encoding': 'gzip'})
        with urlopen(request, timeout=90) as r, partial.open('wb') as f:
            if r.headers.get('Content-Encoding') == 'gzip':
                with gzip.GzipFile(fileobj=r) as stream:
                    shutil.copyfileobj(stream, f, 1 << 20)
            else:
                shutil.copyfileobj(r, f, 1 << 20)
        if digest(partial) != INPUT_SHA:
            raise ValueError(f'Download hash mismatch; partial file retained at {partial}')
        partial.replace(archive)
    if digest(archive) != INPUT_SHA:
        raise ValueError(f'Input hash mismatch; no results regenerated: {archive}')
    replay = cache/'replay'
    replay.mkdir(parents=True, exist_ok=True)
    for command in [
        ['study.py', archive, replay],
        ['followup.py', archive, replay],
        ['figure.py', replay/'primary.csv', replay/'mae.svg'],
    ]:
        subprocess.run([sys.executable, '-B', *command], cwd=here, check=True)
    for name in ['coverage.json', 'primary.csv', 'followup.csv', 'mae.svg']:
        if (replay/name).read_bytes() != (here/'research'/name).read_bytes():
            raise ValueError(f'Replay differs: {replay/name}')
    print('Input SHA-256 and four regenerated outputs match.', flush=True)
    subprocess.run([sys.executable, '-B', kit/'ai4sci.py', 'audit', here], check=True)


if __name__ == '__main__':
    main()
