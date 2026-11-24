"""Read a versioned reviewer issue trail. A consistent trail is not a review verdict."""

from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys

if __package__:
    from .audit import file_id, local_file, manifest, records, text
    from .submission import submission
else:
    from audit import file_id, local_file, manifest, records, text
    from submission import submission


SPEC = 'research/rounds.json'
PAPER = 'research/paper.md'
REPLY = 'research/reply.md'
PACKAGE = 'research/submission.json'
REPLY_PREFIX = re.compile(r'^\[(I[1-9][0-9]*)\](?=[ \t]|$)((?:[ \t]+\[[A-Za-z][A-Za-z0-9_-]*\](?!\())*)')
CLAIM_SUFFIX = re.compile(r'(?:[ \t]+\[C[1-9][0-9]*\])+[ \t]*$')


def rounds(root: Path):
    errors, incomplete, history = [], [], []
    states, comments, passages = {}, {}, {}
    try:
        root = root.resolve(strict=True)
        used = {}

        def registered(name, role):
            path = local_file(root, name)
            identity = file_id(path)
            if identity in used and used[identity] != (role, name):
                raise ValueError(f'{name}: {role} aliases {used[identity][0]} ({used[identity][1]})')
            used[identity] = (role, name)
            return path

        def bound(ref, role, suffix=None):
            name = text(ref, 'path')
            if suffix and Path(name).suffix.lower() != suffix:
                raise ValueError(f'{name}: expected a {suffix} file for {role}')
            raw = registered(name, role).read_bytes()
            if not raw.strip() or hashlib.sha256(raw).hexdigest() != text(ref, 'sha256'):
                raise ValueError(f'{name}: empty file or stale {role} digest')
            return raw

        trail = manifest(registered(SPEC, 'issue trail').read_bytes(), SPEC)
        for name in ('plan.json', 'plan.sha256', 'run.json', 'claims.json', 'sources.json'):
            path = root / 'research' / name
            if path.exists():
                registered('research/' + name, 'study control')

        delivered = registered(PAPER, 'delivered manuscript')
        reply = registered(REPLY, 'delivered reply')
        previous = Counter(bound(trail.get('original'), 'original manuscript', '.md').decode().splitlines())
        sources = {}
        entries = records(trail, 'rounds')
        if not entries:
            raise ValueError('rounds: expected at least one review round')

        for n, entry in enumerate(entries, 1):
            if not isinstance(entry, dict):
                raise ValueError(f'round {n}: expected an object')
            version = text(entry.get('manuscript'), 'path')
            paper_bytes = bound(entry['manuscript'], f'round {n} manuscript', '.md')
            reply_bytes = bound(entry.get('reply'), f'round {n} reply', '.md')
            paper = Counter(paper_bytes.decode().splitlines())
            response = Counter(reply_bytes.decode().splitlines())
            if response[f'Manuscript version: `{version}`'] != 1:
                raise ValueError(f'round {n}: reply does not identify {version}')
            package = entry.get('package')
            if 'package' in entry:
                if Path(text(package, 'path')).suffix.lower() not in {'.docx', '.pdf'}:
                    raise ValueError(f'round {n}: expected a DOCX or PDF snapshot')
                bound(package, f'round {n} package')

            opened, reopened, answered = [], [], set()
            incoming, decisions = records(entry, 'comments'), records(entry, 'decisions')
            if not incoming and not decisions:
                raise ValueError(f'round {n}: no comments or decisions')
            for item in incoming:
                cid, issue = text(item, 'id'), text(item, 'issue')
                if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]*', cid) or re.fullmatch(r'I[0-9]+', cid) or cid in comments:
                    raise ValueError(f'round {n}: invalid or reused comment ID {cid}')
                if not re.fullmatch(r'I[1-9][0-9]*', issue):
                    raise ValueError(f'round {n}: invalid issue ID {issue}')
                text(item, 'reviewer')
                text(item, 'comment')
                if text(item, 'location') not in previous:
                    raise ValueError(f'{cid}: location not found in the manuscript under review')
                comments[cid] = issue
                if issue not in states:
                    opened.append(issue)
                    states[issue] = 'open'
                elif issue in passages:
                    reopened.append(issue)
                    states[issue] = 'reopened'
                    del passages[issue]

            for line in response:
                prefix = REPLY_PREFIX.match(line)
                if prefix:
                    issue, labels = prefix.groups()
                    if issue not in states:
                        raise ValueError(f'round {n}: reply names unregistered issue {issue}')
                    for cid in re.findall(r'\[([^\]]+)\]', labels):
                        if comments.get(cid) != issue:
                            raise ValueError(f'round {n}: reply comment {cid} is not registered for {issue}')

            previous_text = {CLAIM_SUFFIX.sub('', line).strip() for line in previous}
            for item in decisions:
                issue, status, line = (text(item, k) for k in ('issue', 'status', 'response'))
                if states.get(issue) not in ('open', 'reopened') or issue in answered:
                    raise ValueError(f'round {n}: duplicate decision or no active concern for {issue}')
                answered.add(issue)
                if status == 'open' and any(c['issue'] == issue for c in incoming):
                    refs = [issue, *(c['id'] for c in incoming if c['issue'] == issue)]
                else:
                    refs = [issue, *(cid for cid, owner in comments.items() if owner == issue)]
                if (response[line] != 1 or any(f'[{ref}]' not in line for ref in refs) or
                        not re.sub(r'\[[^\]]+\]', '', line).strip()):
                    raise ValueError(f'{issue}: actual reply needs the response line and its issue/comment references')
                if status == 'open':
                    continue
                if status not in ('revised', 'no-change'):
                    raise ValueError(f'{issue}: expected open, revised or no-change')
                passage = text(item, 'passage')
                unchanged = CLAIM_SUFFIX.sub('', passage).strip() in previous_text
                if paper[passage] != 1 or unchanged != (status == 'no-change'):
                    raise ValueError(f'{issue}: {status} passage inconsistent with this or the previous manuscript')
                evidence = records(item, 'evidence')
                if not evidence:
                    raise ValueError(f'{issue}: closing an issue requires evidence')
                for source in evidence:
                    name = text(source, 'path')
                    if name not in sources:
                        raw = bound(source, 'evidence')
                        sources[name] = text(source, 'sha256'), raw.decode()
                    digest, source_text = sources[name]
                    if text(source, 'sha256') != digest:
                        raise ValueError(f'{issue}: stale evidence digest for {name}')
                    quote = text(source, 'quote')
                    if quote not in source_text:
                        raise ValueError(f'{issue}: evidence quote missing in {name}')
                    if type(source.get('verbatim', False)) is not bool:
                        raise ValueError(f'{issue}: verbatim must be true or false')
                    if source.get('verbatim'):
                        # A quoted value of 1.6 must not match 11.6 or 1.60.
                        witness = r'(?<![\w.+−-])' + re.escape(quote) + r'(?!\w|\.\d)'
                        if not re.search(witness, source_text) or not re.search(witness, passage):
                            raise ValueError(f'{issue}: verbatim quote does not match {name} and the passage')
                states[issue], passages[issue] = status, passage

            for issue, passage in passages.items():
                if paper[passage] != 1:
                    raise ValueError(f'{issue}: previously closed passage no longer matches {version}')
            history.append(dict(round=n, manuscript=version, new=opened, reopened=reopened, issues=states.copy()))
            previous = paper
            if n == len(entries) and (delivered.read_bytes() != paper_bytes or reply.read_bytes() != reply_bytes):
                raise ValueError(f'{PAPER} and {REPLY} must match the last manuscript and reply byte for byte')

        # A declared package cannot silently fall back to the Markdown route.
        if any('package' in r for r in entries) or (root / PACKAGE).exists() or (root / PACKAGE).is_symlink():
            package = entries[-1].get('package')
            package_code, result = submission(root)
            if package_code == 2:
                raise ValueError('submission: ' + ', '.join(result['errors']))
            incomplete.extend('submission: ' + message for message in result['incomplete'])
            spec = manifest(registered(PACKAGE, 'submission manifest').read_bytes(), PACKAGE)
            rendered = spec['artifacts']['docx' if spec['format'] == 'docx' else 'pdf']
            if package is None or package['sha256'] != rendered['sha256']:
                raise ValueError('latest round does not bind the submitted DOCX/PDF bytes')
            registered(spec['review']['path'], 'submission review')
            for artifact in spec['artifacts'].values():
                if artifact['path'] != package['path']:
                    registered(artifact['path'], 'submission artifact')
            for issue, passage in passages.items():
                marker = re.search(r' \[(C[1-9][0-9]*)\]$', passage)
                if not marker or marker[1] not in result['content_check']['matched_claims']:
                    raise ValueError(f'{issue}: passage is not a marked claim matched in the submitted document')
        incomplete.extend(f'{issue}: {state}' for issue, state in states.items() if state in ('open', 'reopened'))
    except (OSError, ValueError, RuntimeError) as exc:
        errors.append(str(exc))
    code = 2 if errors else 1 if incomplete else 0
    return code, {'run': 'invalid' if errors else 'complete', 'deliverability': ('ready', 'incomplete', 'blocked')[code],
                  'history': history, 'issues': states, 'errors': errors, 'incomplete': incomplete,
                  'scope': 'File consistency and declared issue coverage only. No independent judgment is inferred.'}


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(2)
    code, detail = rounds(Path(sys.argv[1]))
    print(json.dumps(detail, sort_keys=True))
    sys.exit(code)
