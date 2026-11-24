"""Offline final-package checks; generate the ZIP and single-page PDF fixtures locally."""

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
STATEMENT = 'The estimate was 0.125.'
R = 'research/'
DOCX = R + 'final.docx'
PDF = R + 'final.pdf'
TEX = R + 'main.tex'
REVIEW = R + 'review.json'


def make_docx(path, body, declaration=''):
    with ZipFile(path, 'w') as z:
        z.writestr('[Content_Types].xml', '''<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>''')
        z.writestr('_rels/.rels', '''<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>''')
        z.writestr('word/document.xml', declaration + '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>'
                   + body + '</w:body></w:document>')


def pdf(lines):
    stream = b'BT /F1 12 Tf 20 200 Td 16 TL ' + b' T* '.join(b'(' + x.encode() + b') Tj' for x in lines) + b' ET'
    objects = [b'<< /Type /Catalog /Pages 2 0 R >>', b'<< /Type /Pages /Count 1 /Kids [3 0 R] >>',
               b'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 400 400] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>',
               b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>',
               b'<< /Length %d >>\nstream\n' % len(stream) + stream + b'\nendstream',
               b'<< /Title (' + STATEMENT.encode() + b') >>']
    data = b'%PDF-1.4\n'
    offsets = []
    for i, obj in enumerate(objects, 1):
        offsets.append(len(data))
        data += b'%d 0 obj\n' % i + obj + b'\nendobj\n'
    start = len(data)
    return data + b'xref\n0 7\n0000000000 65535 f \n' + b''.join(b'%010d 00000 n \n' % n for n in offsets) + (
        b'trailer\n<< /Size 7 /Root 1 0 R /Info 6 0 R >>\nstartxref\n%d\n%%%%EOF\n' % start)


class Submission(unittest.TestCase):
    def setUp(self):
        tmp = ROOT / '.local/tmp'
        tmp.mkdir(parents=True, exist_ok=True)
        study = tempfile.TemporaryDirectory(dir=tmp)
        self.addCleanup(study.cleanup)
        self.root = Path(study.name)
        (self.root / R).mkdir()
        (self.root / (R+'paper.md')).write_text(STATEMENT+' [C1]\n', encoding='utf-8')
        self.claim = dict(id='C1', statement=STATEMENT, status='supported', evidence=[])
        self.put(R+'claims.json', {'claims': [self.claim]})
        self.body = '<w:p><w:r><w:t xml:space="preserve">The estimate </w:t></w:r><w:r><w:t>was 0.125.</w:t></w:r></w:p>'
        make_docx(self.root / DOCX, self.body)
        self.artifacts = {'docx': DOCX}
        self.fmt = 'docx'
        self.package()

    def put(self, name, data):
        (self.root / name).write_text(json.dumps(data), encoding='utf-8')

    def digest(self, name):
        return hashlib.sha256((self.root / name).read_bytes()).hexdigest()

    def package(self, **overrides):
        self.review = dict(reviewer='Fixture reviewer', date='2020-01-31', status='approved',
                           visual_inspection='Fixture: read page one in a viewer.', open_revisions=[],
                           sha256={n: self.digest(n) for n in [R+'paper.md', R+'claims.json', *self.artifacts.values()]})
        self.put(REVIEW, {**self.review, **overrides})
        self.spec = dict(format=self.fmt, artifacts={k: {'path': n, 'sha256': self.digest(n)} for k, n in self.artifacts.items()},
                         review={'path': REVIEW, 'sha256': self.digest(REVIEW)})
        self.put(R+'submission.json', self.spec)

    def cli(self, code, **env):
        result = subprocess.run([sys.executable, ROOT/'checks/submission.py', self.root],
                                capture_output=True, text=True, env={**os.environ, **env})
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report['deliverability'], ('ready', 'incomplete', 'blocked')[code])
        return report

    def test_docx_ordinary_body_runs(self):
        self.assertEqual(self.cli(0)['content_check']['matched_claims'], ['C1'])

    def test_docx_sentence_boundaries(self):
        chinese = '估计值为0.125。'
        for statement, paragraph, code in [
                (STATEMENT, 'How large was the effect? '+STATEMENT+' It met the target.', 0),
                (STATEMENT, 'The first trial failed! '+STATEMENT+' [C1] The second succeeded.', 0),
                (chinese, '结果如何？'+chinese+'后续实验仍待完成。', 0),
                (chinese, '不能断言'+chinese+'后续实验仍待完成。', 2),
                (STATEMENT, 'It is not true that '+STATEMENT+' More data are needed.', 2),
                (STATEMENT, 'Unverified: '+STATEMENT, 2),
                (STATEMENT, STATEMENT+'7 was reported.', 2),
                (STATEMENT, STATEMENT+' [C2] Another result follows.', 2),
                ('0.125.', 'We measured 10.125. More data are needed.', 2),
                ('Estimate 0.125', 'Estimate 0.125 [C1]', 0),
                ('Estimate 0.125', 'Test completed. Estimate 0.125 times the baseline.', 2)]:
            with self.subTest(paragraph=paragraph):
                self.put(R+'claims.json', {'claims': [{**self.claim, 'statement':statement}]})
                (self.root / (R+'paper.md')).write_text(statement+' [C1]\n', encoding='utf-8')
                make_docx(self.root / DOCX, '<w:p><w:r><w:t>'+paragraph+'</w:t></w:r></w:p>')
                self.package()
                self.cli(code)

    def test_refreshed_docx_and_review_digests_do_not_establish_content(self):
        wrong = '<w:p><w:r><w:t>The estimate was 0.126.</w:t></w:r></w:p>'
        for extra in [f'<!--{STATEMENT}-->', f'<w:p><w:r><w:instrText>{STATEMENT}</w:instrText></w:r></w:p>',
                      f'<w:p><w:r><w:rPr><w:vanish/></w:rPr><w:t>{STATEMENT}</w:t></w:r></w:p>',
                      f'<w:p><w:r><w:t>Not true: {STATEMENT}</w:t></w:r></w:p>']:
            with self.subTest(extra=extra):
                make_docx(self.root / DOCX, wrong + extra)
                self.package()
                self.assertEqual(self.cli(2)['content_check']['missing_claims'], ['C1'])

    def test_malformed_empty_and_missing_docx(self):
        make_docx(self.root / DOCX, '')
        self.package()
        self.cli(2)
        make_docx(self.root / DOCX, self.body, '<?xml version="1.0" encoding="unknown-encoding"?>')
        self.package()
        self.assertIn('encoding', self.cli(2)['errors'][0])
        (self.root / DOCX).write_bytes(b'fake ZIP containing ' + STATEMENT.encode())
        self.package()
        self.cli(2)
        (self.root / DOCX).unlink()
        self.cli(2)

    def test_ledger_drift_and_missing_coverage(self):
        (self.root / (R+'claims.json')).write_bytes((self.root / (R+'claims.json')).read_bytes() + b'\n')
        self.assertIn('dated review', self.cli(2)['errors'][0])
        self.put(R+'claims.json', {'claims': [self.claim, {**self.claim, 'id':'C2', 'statement':'Second result.'}]})
        self.package()
        self.assertIn('C2', self.cli(2)['errors'][0])
        (self.root / (R+'paper.md')).write_text(STATEMENT+' [C1]\nSecond result. [C2]\n', encoding='utf-8')
        self.package()
        self.assertEqual(self.cli(2)['content_check']['missing_claims'], ['C2'])

    def test_external_review_and_package_must_bind_current_bytes(self):
        self.put(REVIEW, {**self.review, 'reviewer':'Other'})
        self.assertIn('digest', self.cli(2)['errors'][0])
        self.package()
        make_docx(self.root / DOCX, self.body+'<!--changed-->')
        self.assertIn('digest', self.cli(2)['errors'][0])
        self.spec['artifacts']['docx']['sha256'] = self.digest(DOCX)
        self.put(R+'submission.json', self.spec)
        self.assertIn('dated review', self.cli(2)['errors'][0])

    def test_incomplete_review_or_claim_and_invalid_review(self):
        self.package(status='needs-revision')
        self.cli(1)
        self.package(open_revisions=['Recheck page 2.'])
        self.cli(1)
        self.package(date='2020-02-31')
        self.cli(2)
        self.package(visual_inspection='')
        self.cli(2)
        self.put(R+'claims.json', {'claims': [{**self.claim, 'status':'partial'}]})
        self.package()
        self.cli(1)

    def test_word_tracked_edit(self):
        make_docx(self.root / DOCX, self.body+'<w:p><w:del w:id="1"><w:r><w:delText>Old</w:delText></w:r></w:del></w:p>')
        self.package()
        self.assertIn('tracked revisions', self.cli(1)['incomplete'][0])

    def test_alias_traversal_and_self_evidence(self):
        alias = R+'also-review.json'
        os.link(self.root / DOCX, self.root / alias)
        self.spec['review'] = {'path': alias, 'sha256': self.digest(alias)}
        self.put(R+'submission.json', self.spec)
        self.assertIn('aliases', self.cli(2)['errors'][0])
        self.spec['review']['path'] = 'research/../research/review.json'
        self.put(R+'submission.json', self.spec)
        self.assertIn('project-relative', self.cli(2)['errors'][0])
        self.put(R+'claims.json', {'claims': [{**self.claim, 'evidence':[{'kind':'quote', 'path':alias}]}]})
        self.package()
        self.assertIn('aliases', self.cli(2)['errors'][0])

    def test_pdf_extractor_absent_is_explicitly_blocked(self):
        self.fmt, self.artifacts = 'pdf', {'pdf': PDF}
        (self.root / PDF).write_bytes(pdf([STATEMENT]))
        self.package()
        self.assertIn('pdftotext not installed', self.cli(2, PATH='')['errors'][0])

    @unittest.skipUnless(shutil.which('pdftotext'), 'real PDF text extraction requires pdftotext')
    def test_pdf_and_latex_pdf_require_real_page_text(self):
        (self.root / TEX).write_text('\\documentclass{article}\n\\begin{document}'+STATEMENT+'\\end{document}', encoding='utf-8')
        for self.fmt, self.artifacts in [('pdf', {'pdf':PDF}), ('latex+pdf', {'tex':TEX, 'pdf':PDF})]:
            with self.subTest(fmt=self.fmt):
                (self.root / PDF).write_bytes(pdf(['What was measured? The estimate', 'was 0.125. More data are needed.']))
                self.package()
                self.assertEqual(self.cli(0)['content_check']['extractor'], 'pdftotext')
                (self.root / PDF).write_bytes(pdf(['It is not true that', STATEMENT]))
                self.package()
                self.assertEqual(self.cli(2)['content_check']['missing_claims'], ['C1'])
                (self.root / PDF).write_bytes(pdf(['The estimate was 0.215.']))
                self.package()
                self.assertEqual(self.cli(2)['content_check']['missing_claims'], ['C1'])
                (self.root / PDF).write_bytes(pdf([]))
                self.package()
                self.assertIn('no extractable', self.cli(2)['errors'][0])


if __name__ == '__main__':
    unittest.main()
