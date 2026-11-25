#!/usr/bin/env python3
"""Check every display cell in the reader-facing tables, independently of the editor."""
from pathlib import Path
from decimal import Decimal
import re,csv

root=Path(__file__).resolve().parent
paper=(root/'revised.md').read_text().splitlines()
for panel, labels, filename, first in [
    ('3a',['whole','early','late','late-minus-early'],'centered-sensitivity','estimate'),
    ('3b',['1900-1919','1920-1939','1940-1959','2000-2019'],'centered-sensitivity','estimate'),
    ('3c',['whole','early','late','late-minus-early'],'summary','draw_median')]:
    with (root/f'supplement/research/{filename}.csv').open() as f:
        rows={(r['model'],r['period']):r for r in csv.DictReader(f)}
    i=next(i for i,x in enumerate(paper) if x.startswith('**Table '+panel+'.'))
    table=[x for x in paper[i+1:i+9] if x.startswith('| Tr')]; assert len(table)==4
    for line,model in zip(table,['Tr','TrNc','TrNcZw','TrNcPd']):
        model_text,*cells = [x.strip() for x in line.strip('|').split('|')]; assert model_text==model and len(cells)==4
        for p,cell in zip(labels,cells):
            display=re.fullmatch(r'([-\d.]+) \[([-\d.]+), ([-\d.]+)\]',cell.replace('−','-')); assert display,cell
            for text,col in zip(display.groups(),[first,'lo95','hi95']):
                assert abs(Decimal(rows[model,p][col])-Decimal(text))<=Decimal('.005'),(panel,model,p,col)
print('OK: 144 numeric displays across Table 3a–c verified against the respective output columns.')
