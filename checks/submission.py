"""Check a final publication package after the independent offline evidence audit."""

from collections import Counter
from datetime import date
from decimal import InvalidOperation
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from zipfile import BadZipFile, ZipFile
import zlib

if __package__:
    from .audit import MARKER, STATUSES, file_id, local_file, manifest, records, text
else:
    from audit import MARKER, STATUSES, file_id, local_file, manifest, records, text


PAPER = 'research/paper.md'
LEDGER = 'research/claims.json'
SPEC = 'research/submission.json'
FORMATS = {'docx': {'docx'}, 'pdf': {'pdf'}, 'latex+pdf': {'tex', 'pdf'}}
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
CT = '{http://schemas.openxmlformats.org/package/2006/content-types}'
REL = '{http://schemas.openxmlformats.org/package/2006/relationships}'
MAIN_TYPE = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml'


def normalized(s):
    return ' '.join(s.split())


def docx_paragraphs(raw):
    """Ordinary text paragraphs only, not fields, annotations, or alternative representations."""
    with ZipFile(io.BytesIO(raw)) as package:
        if len(set(package.namelist())) != len(package.namelist()):
            raise ValueError('DOCX: duplicate package parts')
        types = ET.fromstring(package.read('[Content_Types].xml'))
        rels = ET.fromstring(package.read('_rels/.rels'))
        main = [r for r in rels.findall(REL + 'Relationship') if r.get('Type') ==
                'http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument']
        if (types.tag != CT + 'Types' or rels.tag != REL + 'Relationships' or len(main) != 1
                or main[0].get('TargetMode', 'Internal') != 'Internal'
                or main[0].get('Target') not in ('word/document.xml', '/word/document.xml')
                or [p.get('ContentType') for p in types.findall(CT + 'Override')
                    if p.get('PartName') == '/word/document.xml'] != [MAIN_TYPE]):
            raise ValueError('DOCX: missing or ambiguous main document relationship/content type')
        doc = ET.fromstring(package.read('word/document.xml'))
    bodies = doc.findall(W + 'body')
    if doc.tag != W + 'document' or len(bodies) != 1:
        raise ValueError('DOCX: missing or ambiguous Word document body')
    body = bodies[0]
    revisions = any(n.tag in {W+'ins', W+'del', W+'moveFrom', W+'moveTo'} or
                    (n.tag.startswith(W) and n.tag.endswith('PrChange')) for n in body.iter())

    paragraphs = set()
    def visit(node):
        for p in node:
            if p.tag in {W+'tbl', W+'tr', W+'tc'}:
                visit(p)
            elif p.tag == W+'p':
                chunks = []
                # Do not descend into arbitrary XML: e.g. drawings can carry text
                # boxes and alternative text unrelated to this body paragraph.
                for child in p:
                    if child.tag in {W+'pPr', W+'bookmarkStart', W+'bookmarkEnd', W+'proofErr'}:
                        continue
                    runs = list(child) if child.tag == W+'hyperlink' else [child]
                    for run in runs:
                        if run.tag != W+'r':
                            chunks.append('\0')
                            continue
                        if any(h.get(W+'val') not in ('0', 'false', 'off') for key in
                               ('vanish', 'webHidden', 'specVanish') for h in
                               run.findall(f'{W}rPr/{W}{key}')):
                            continue
                        for elem in run:
                            if elem.tag == W+'t':
                                chunks.append(elem.text or '')
                            elif elem.tag in {W+'tab', W+'br', W+'cr'}:
                                chunks.append(' ')
                            elif elem.tag != W+'rPr':
                                chunks.append('\0')
                line = normalized(''.join(chunks))
                if line and '\0' not in line:
                    paragraphs.add(line)
    visit(body)
    return paragraphs, revisions


def pdf_paragraphs(raw):
    if not raw.startswith(b'%PDF-'):
        raise ValueError('PDF: missing PDF header')
    try:
        result = subprocess.run(['pdftotext', '-enc', 'UTF-8', '-', '-'], input=raw,
                                capture_output=True, timeout=60)
    except FileNotFoundError as exc:
        raise ValueError('PDF extraction blocked: pdftotext not installed/on PATH') from exc
    if result.returncode or b'Syntax Error' in result.stderr:
        raise ValueError(f'pdftotext failed: {result.stderr.decode("utf-8", "replace")[:240]}')
    # Fold wraps inside text blocks; a lone physical line is not a paragraph
    # boundary (the preceding line may contain a negation or qualification).
    paragraphs = {normalized(block) for page in result.stdout.decode('utf-8').split('\f')
                  for block in re.split(r'\n[^\S\n]*\n', page) if block.strip()}
    if not paragraphs:
        raise ValueError('PDF: no extractable page text (no OCR performed)')
    return paragraphs


def has_statement(paragraphs, statement, cid):
    if statement in paragraphs or f'{statement} [{cid}]' in paragraphs:
        return True
    if statement[-1] not in '.!?。！？':
        return False  # A fragment needs an entire paragraph, not word boundaries.
    # ASCII stops require a separating space (a decimal point is not a stop).
    # Chinese sentence stops do not. A printed marker must be the claim's own.
    start = r'(?:^|(?:[.!?] |[。！？] ?)(?:\[C[1-9][0-9]*\] ?)?)'
    end = r'(?= |$)' if statement[-1] in '.!?' else ''
    marker = re.escape(f' [{cid}]')
    match = re.compile(start + re.escape(statement) + rf'(?:{marker}{end}|(?! ?\[C[0-9]+\]){end})')
    return any(match.search(p) for p in paragraphs)


def submission(root):
    errors, pending = [], []
    content = {'extractor': None, 'matched_claims': [], 'missing_claims': []}
    receipt = None
    fmt = None
    try:
        root = Path(root).resolve(strict=True)
        seen = {}

        def take(name):
            path = local_file(root, name)
            identity = file_id(path)
            if identity in seen:
                raise ValueError(f'{name} aliases {seen[identity]}: separate files required')
            seen[identity] = name
            return path.read_bytes()

        for name in ('research/plan.json', 'research/plan.sha256', 'research/run.json', 'research/sources.json'):
            if (root / name).exists():
                seen[file_id(local_file(root, name))] = name
        spec = manifest(take(SPEC), SPEC)
        paper, ledger = take(PAPER), take(LEDGER)
        actual = {PAPER: hashlib.sha256(paper).hexdigest(), LEDGER: hashlib.sha256(ledger).hexdigest()}
        claims = records(manifest(ledger, LEDGER), 'claims')
        canonical = paper.decode('utf-8')
        lines = Counter(line.strip() for line in canonical.splitlines())
        markers = Counter(MARKER.findall(canonical))
        statements, unique = {}, set()
        for claim in claims:
            cid, statement, status = (text(claim, k) for k in ('id', 'statement', 'status'))
            if (not re.fullmatch('C[1-9][0-9]*', cid) or cid in statements or MARKER.search(statement)
                    or normalized(statement) in unique or status not in STATUSES):
                raise ValueError(f'invalid or ambiguous ledger claim: {cid}')
            if lines[f'{statement} [{cid}]'] != 1 or markers[cid] != 1:
                raise ValueError(f'{cid}: missing or duplicate exact marked statement in {PAPER}')
            if claim['status'] != 'supported':
                pending.append(f'{cid}: ledger status {claim["status"]}')
            statements[cid] = normalized(statement)
            unique.add(normalized(statement))
            for evidence in records(claim, 'evidence'):
                if not isinstance(evidence, dict):
                    raise ValueError('invalid ledger evidence object')
                if 'path' in evidence:
                    name = evidence['path']
                    identity = file_id(local_file(root, name))
                    if seen.get(identity) in {SPEC, LEDGER, PAPER}:
                        raise ValueError(f'circular evidence in {cid}: {name}')
                    seen[identity] = name
        if not statements or set(markers) != set(statements):
            raise ValueError('empty ledger or unregistered canonical paper marker')
        fmt = text(spec, 'format')
        artifacts = spec.get('artifacts')
        if fmt not in FORMATS or not isinstance(artifacts, dict) or set(artifacts) != FORMATS[fmt]:
            raise ValueError('format/artifacts mismatch; expected docx, pdf, or latex+pdf')

        def bound_file(record):
            name = text(record, 'path')
            raw = take(name)
            digest = hashlib.sha256(raw).hexdigest()
            if digest != text(record, 'sha256'):
                raise ValueError(f'{name}: digest differs from submission manifest')
            return name, raw, digest

        for kind, record in artifacts.items():
            name, raw, digest = bound_file(record)
            if Path(name).suffix.lower() != '.' + kind or not raw:
                raise ValueError(f'{name}: expected a nonempty .{kind} file')
            actual[name] = digest
            if kind == 'tex':
                source = raw.decode('utf-8')
                if not any(line.strip() and not line.lstrip().startswith('%') for line in source.splitlines()):
                    raise ValueError(f'{name}: empty TeX source')
                continue
            if kind == 'docx':
                content['extractor'] = 'word/document.xml'
                paragraphs, revisions = docx_paragraphs(raw)
                if revisions:
                    pending.append('DOCX contains unresolved tracked revisions')
                if not paragraphs:
                    raise ValueError('DOCX: no ordinary extractable body paragraphs')
            else:
                content['extractor'] = 'pdftotext'
                paragraphs = pdf_paragraphs(raw)
            for cid, statement in statements.items():
                found = has_statement(paragraphs, statement, cid)
                content['matched_claims' if found else 'missing_claims'].append(cid)
            if content['missing_claims']:
                errors.append(f'{name}: missing complete final statement(s); see content_check.missing_claims')

        name, raw, _ = bound_file(spec.get('review'))
        review = manifest(raw, name)
        if review.get('sha256') != actual:
            raise ValueError(f'{name}: dated review does not bind the exact current paper, ledger and final files')
        reviewer, day, status = (text(review, k) for k in ('reviewer', 'date', 'status'))
        if not re.fullmatch(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', day) or date.fromisoformat(day) > date.today():
            raise ValueError('review.date must be an actual, nonfuture YYYY-MM-DD')
        note = text(review, 'visual_inspection')
        revisions = records(review, 'open_revisions')
        if any(not isinstance(s, str) or not s.strip() for s in revisions):
            raise ValueError('review.open_revisions must list nonblank descriptions')
        if status not in ('approved', 'needs-revision'):
            raise ValueError('review.status must be approved or needs-revision')
        if status != 'approved' or revisions:
            pending.append('review requests revision or still lists open revisions')
        receipt = {'path': name, 'reviewer': reviewer, 'date': day, 'status': status,
                   'visual_inspection': note, 'open_revisions': revisions}
    except (ValueError, OSError, RuntimeError, LookupError, InvalidOperation, BadZipFile, ET.ParseError,
            zlib.error, EOFError, subprocess.TimeoutExpired) as exc:
        errors.append(str(exc)[:300])
    code = 2 if errors else 1 if pending else 0
    return code, {'run': 'invalid' if errors else 'complete', 'format': fmt,
                  'deliverability': ('ready', 'incomplete', 'blocked')[code], 'errors': errors,
                  'incomplete': pending, 'content_check': content, 'review': receipt,
                  'scope': 'Package integrity and extracted claim text only; evidence and recorded visual review are separate checks.'}


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(json.dumps({'run': 'invalid', 'deliverability': 'blocked',
                          'errors': ['usage: python3 checks/submission.py STUDY']}))
        sys.exit(2)
    code, report = submission(Path(sys.argv[1]))
    print(json.dumps(report, sort_keys=True))
    sys.exit(code)
