#!/usr/bin/env python3
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[1]
d=json.loads((R/'candidates/questions.json').read_text())
files={}
for p in sorted(R.rglob('*')):
 if not p.is_file() or p.name=='MANIFEST.json' or any(x in p.parts for x in ['__pycache__','.pytest_cache']):continue
 if p.name in ['test-progress.json','invalid-progress.json']:continue
 files[p.relative_to(R).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
m={'schema_version':'package-integrity/1.0','edition':d['edition'],'input_guide_sha256':d['input_guide_sha256'],
   'base_commit':d['base_commit'],'publication_eligible':False,'files':files}
(R/'MANIFEST.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
print('Manifest files:',len(files))
