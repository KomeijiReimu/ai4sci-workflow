"""Make the editable Word delivery from the canonical manuscript (Pandoc)."""

import os
from pathlib import Path
import re
import subprocess

paper = Path("research/paper.md").read_text(encoding="utf-8")
# The claim markers belong to the audit copy, not the published paragraphs.
clean = re.sub(r" \[C[1-9][0-9]*\]$", "", paper, flags=re.MULTILINE)
Path("paper").mkdir(exist_ok=True)
Path(".scratch").mkdir(exist_ok=True)
subprocess.run(["pandoc", "--from=markdown-smart", "--to=docx", "--output=paper/final.docx"],
               input=clean.encode(), check=True,
               env={**os.environ, "TMPDIR": str(Path(".scratch").resolve()), "SOURCE_DATE_EPOCH": "946684800"})
