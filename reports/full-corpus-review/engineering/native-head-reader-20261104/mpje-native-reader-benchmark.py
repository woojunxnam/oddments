import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

p=argparse.ArgumentParser()
p.add_argument('code_root');p.add_argument('operation',choices=['metadata','migration','build'])
p.add_argument('output_prefix');a=p.parse_args()
root=Path('/workspace/mpje-pr193-qa')
sys.path.insert(0,str(Path(a.code_root)/'scripts'))
counts=Counter();original=subprocess.check_output

def counted(command,*args,**kwargs):
    if command[0]=='git':counts[command[3]]+=1
    return original(command,*args,**kwargs)

subprocess.check_output=counted
started=time.perf_counter()
if a.operation=='metadata':
    from notes_independent_metadata import load_metadata
    bindings={};result={'metadata':load_metadata(root,source_bindings=bindings),'source_bindings':bindings}
elif a.operation=='migration':
    import notes_held_sixteenth as held
    binding=json.loads((root/held.MANIFEST).read_bytes())['closure']
    result=held.expected_migration(root,binding)
else:
    import build_full_corpus_review as builder
    builder.ROOT=root;builder.OUT=root/'reports/full-corpus-review'
    result={str(k.relative_to(root)):v for k,v in builder.build().items()}
elapsed=time.perf_counter()-started
raw=(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode()
Path(a.output_prefix+'.result.json').write_bytes(raw)
metrics={'code_root':a.code_root,'data_root':str(root),'data_head':original(['git','-C',str(root),'rev-parse','HEAD']).decode().strip(),'operation':a.operation,'seconds':elapsed,'git_calls':dict(counts),'result_sha256':hashlib.sha256(raw).hexdigest(),'result_bytes':len(raw)}
Path(a.output_prefix+'.metrics.json').write_text(json.dumps(metrics,indent=2)+'\n')
print(json.dumps(metrics),flush=True)
