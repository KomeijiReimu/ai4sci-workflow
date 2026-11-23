"""Verify the local text snapshots behind a study's quotations, without a network call."""

import hashlib
import re
from urllib.parse import urlsplit


def load_sources(root, plan, local_file, file_id, manifest, control_ids):
    name = 'research/sources.json'
    proposed = root / name
    if not proposed.exists() and not proposed.is_symlink():
        if plan.get('require_source_manifest'):
            raise ValueError(f'{name} required by frozen plan')
        return None
    path = local_file(root, name)
    identity = file_id(path)
    if identity in control_ids:
        raise ValueError(f'{name}: must be distinct from other study records')
    control_ids.add(identity)
    records = manifest(path.read_bytes(), name).get('sources')
    if not isinstance(records, list) or not records:
        raise ValueError(f'{name}: expected a nonempty sources array')
    by_file, ids = {}, set()
    for index, source in enumerate(records):
        label = f'{name}: sources[{index}]'
        for key in ('id', 'title', 'origin', 'locator', 'access', 'path', 'sha256'):
            if not isinstance(source, dict) or not isinstance(source.get(key), str) or not source[key].strip():
                raise ValueError(f'{label}: missing or blank {key}')
        sid = source['id']
        if sid in ids:
            raise ValueError(f'{label}: duplicate source ID {sid}')
        ids.add(sid)
        access = source['access']
        if access not in ('full-text', 'abstract', 'provided'):
            raise ValueError(f'{sid}: access must be full-text, abstract or provided')
        if access != 'provided':
            url = urlsplit(source['origin'])
            if url.scheme not in ('http', 'https') or not url.hostname:
                raise ValueError(f'{sid}: published source origin must be a stable HTTP(S) URL')
        snapshot = local_file(root, source['path'])
        key = file_id(snapshot)
        if key in control_ids or key in by_file:
            raise ValueError(f'{sid}: duplicate snapshot or study control file')
        digest = source['sha256']
        if not re.fullmatch('[0-9a-f]{64}', digest) or hashlib.sha256(snapshot.read_bytes()).hexdigest() != digest:
            raise ValueError(f'{sid}: source snapshot digest does not match {source["path"]}')
        by_file[key] = sid
    return by_file
