#!/usr/bin/env python3
"""Rebuild the exact full manuscript from the supplied editable v1 extraction."""
import argparse
import hashlib
import json
from pathlib import Path

cli = argparse.ArgumentParser(description=__doc__)
cli.add_argument('original', type=Path)
cli.add_argument('destination', type=Path)
cli.add_argument('--check', action='store_true', help='compare to an existing destination instead of writing it')
args = cli.parse_args()
record = json.loads(Path(__file__).with_name('amendments.json').read_text())
raw = args.original.read_bytes(); sha = lambda b: hashlib.sha256(b).hexdigest()
if sha(raw) != record['source_sha256']:
    raise SystemExit('The editable source SHA-256 differs from this edition; no file written.')
lines=raw.splitlines(keepends=True); pos=0; chunks=[]
for edit in record['edits']:
    a,b=edit['first']-1,edit['last']
    if not pos <= a < b <= len(lines):
        raise SystemExit('Invalid or overlapping replacement coordinates.')
    chunks += [b''.join(lines[pos:a]),edit['replacement'].encode('utf-8')]; pos=b
final = b''.join(chunks + lines[pos:])
if sha(final)!=record['revised_sha256']:
    raise SystemExit('Rebuild mismatch; no file written.')
if args.check:
    if args.destination.read_bytes()!=final:
        raise SystemExit('Existing manuscript differs from rebuilt bytes.')
else:
    if args.destination.resolve()==args.original.resolve():
        raise SystemExit('Refusing to replace the original manuscript.')
    with args.destination.open('xb') as f:
        f.write(final)
print('Verified revision SHA-256:', sha(final))
