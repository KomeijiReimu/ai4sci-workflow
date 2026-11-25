#!/usr/bin/env python3
"""Stage the nine scientific CSVs by checksum from an offline v1 release checkout."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
from urllib.parse import urlsplit

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('release',type=Path,help='root of KNMI release 8c4b55df2b88feb4ebaa191f6d3e8bb9a4b8c86b')
p.add_argument('destination',type=Path,help='new directory, outside the publication bundle')
a=p.parse_args(); manifest=json.loads(Path(__file__).with_name('inputs.json').read_text()); copy={}
for label,r in manifest.items():
    if label.endswith('.csv') or label=='REUSE.txt':
        source=a.release/urlsplit(r['origin']).path.split('8c4b55df2b88feb4ebaa191f6d3e8bb9a4b8c86b/')[1]
        if hashlib.sha256(source.read_bytes()).hexdigest()!=r['sha256']:
            raise SystemExit('Source mismatch: '+source.name)
        copy[label]=source
a.destination.mkdir(parents=True,exist_ok=False)
for label,source in copy.items():
    shutil.copyfile(source,a.destination/label)
print('Staged nine verified scientific CSVs and BSD notice; no network access.')
