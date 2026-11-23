"""Recheck the submitted numbers with SQLite and the pinned public DiscoveryBench files.

Python 3.10+, standard library only. All downloads and SQL tables stay in memory.
Prints evidence for the local assessment, not an official benchmark score.
"""
import csv
import hashlib
import io
import json
import math
from pathlib import Path
import sqlite3
from urllib.request import urlopen

BASE = Path(__file__).resolve().parent
COMMIT = 'c31fcf011e070f021a5f5b906896d0821f6880e8'
RAW = 'https://raw.githubusercontent.com/allenai/discoverybench/' + COMMIT + '/'
DIR = 'discoverybench/synth/test/astronomy_0_0/'
PREDICTORS = '''distance_to_nearest_star_forming_region star_formation_rate magnetic_field_presence galaxy_age dominant_stellar_age luminosity_variability has_binary_star_system velocity_dispersion_of_stars average_surface_temperature_of_stars ultraviolet_emission cosmic_radiation_level proportion_of_red_stars blue_signature_intensity'''.split()
FLAGS = {'magnetic_field_presence','has_binary_star_system','ultraviolet_emission'}

def checked(data, expected):
    if hashlib.sha256(data).hexdigest() != expected:
        raise ValueError('Input or submission digest differs from the recorded digest: '+expected)
    return data

def download(path, digest):
    with urlopen(RAW+path, timeout=30) as response:
        return checked(response.read(), digest)

def must(test, description):
    if not test:
        raise ValueError(description)

raw = download(DIR+'data.csv', '8e9f72b6820e7f4f234576112ffc53c956794abb6b5fef4aaedd79062ffabd9b')
meta = json.loads(download(DIR+'metadata_0.json', '699f47221dde8d79e9aac81ad4629cb0374f2fc4805d514b9529de2bd07e65b6').decode('latin-1'))
must(meta['id']==0 and [q['qid'] for q in meta['queries']]==[771], 'Mismatched metadata')
key = download('eval/answer_key_synth.csv', 'afd51d7053cefff6b335c209a42a1943217cb73a9fd36144a500cce49ecda675')
reader = csv.DictReader(io.StringIO(key.decode('cp1252')))
matches = [(r,reader.line_num) for r in reader if (r['dataset'],r['metadataid'],r['query_id'])==('astronomy_0_0','0','771')]
(gold,gold_line), = matches

checked((BASE/'submission/paper.md').read_bytes(), 'b9bf936f0b35acc8084c7bf53560b1a3e792b933c9c98520fe3602f9e290ccdf')
submitted = checked((BASE/'submission/contrasts.csv').read_bytes(), '9f220a24adeec83efc2cf4d718fccedf7a6b5db4c35154c1b0a5605b17c641d7')
expected = list(csv.DictReader(io.StringIO(submitted.decode())))
must(sorted(PREDICTORS)==sorted(r['predictor'] for r in expected), 'Unexpected predictors in submitted contrasts')
rows = list(csv.DictReader(io.StringIO(raw.decode())))
conn = sqlite3.connect(':memory:')
conn.execute('CREATE TABLE observation (class TEXT, y REAL,'+','.join('"'+c+'" REAL' for c in PREDICTORS)+')')
def number(s):
    return None if s=='' else float(s)
def record(r):
    return [r['dark_matter_density_classification'],number(r['galaxy_density_increase'])]+[{'True':1,'False':0,'':None}[r[c]] if c in FLAGS else number(r[c]) for c in PREDICTORS]
conn.executemany('INSERT INTO observation VALUES ('+','.join(['?']*(2+len(PREDICTORS)))+')',map(record,rows))
groups = [dict(zip(['class','rows','recorded','missing','min','max','distinct'],x)) for x in conn.execute('SELECT class,count(*),count(y),count(*)-count(y),min(y),max(y),count(distinct y) FROM observation GROUP BY class ORDER BY class')]
total,nonblank,levels,ymin,ymax = conn.execute('SELECT count(*),count(y),count(distinct y),min(y),max(y) FROM observation').fetchone()
mean, = conn.execute('SELECT avg(y) FROM observation').fetchone()
ssd, = conn.execute('SELECT sum((y-?)*(y-?)) FROM observation',(mean,mean)).fetchone()
sd = math.sqrt(ssd/(nonblank-1))
must((total,nonblank,levels,ymin,ymax,sd)==(500,494,1,1,1,0), 'Response claim failed')
for r in expected:
    c = r['predictor'] # matched against the explicit identifier allowlist above
    query = f'''WITH paired AS (SELECT {c} x, y FROM observation WHERE {c} IS NOT NULL AND y IS NOT NULL),
        ranked AS (SELECT x,row_number() OVER (ORDER BY x) i,count(*) OVER () n FROM paired),
        cut AS (SELECT avg(x) v FROM ranked WHERE i IN ((n+1)/2,(n+2)/2))
        SELECT x > {'0' if c in FLAGS else '(SELECT v FROM cut)'} upper_group,count(*),avg(y),min(y),max(y) FROM paired GROUP BY upper_group ORDER BY upper_group'''
    (g0,n0,m0,lo0,hi0),(g1,n1,m1,lo1,hi1) = conn.execute(query).fetchall()
    must((g0,g1,n0,n1,n0+n1)==(0,1,int(r['n_lower']),int(r['n_upper']),int(r['paired'])),c+': group count mismatch')
    for value,col in [(m0,'mean_lower'),(m1,'mean_upper'),(m1-m0,'difference')]:
        must(math.isclose(value,float(r[col]),rel_tol=1e-6,abs_tol=1e-8),c+': mismatch in '+col)
    must(lo0==hi0==lo1==hi1 and r['pearson']=='' and r['undefined_reason']=='constant outcome',c+': correlation not documented as undefined')
print(json.dumps({'source_commit':COMMIT,'task':['astronomy_0_0',0,771],'gold_physical_line_end':gold_line,'gold':gold['gold_hypo'],'rows':total,'recorded':nonblank,'missing':total-nonblank,'recorded_range':[ymin,ymax],'sample_sd':sd,'class_counts':groups,'independently_matched_contrasts':len(expected),'defined_correlations':0},indent=2))
