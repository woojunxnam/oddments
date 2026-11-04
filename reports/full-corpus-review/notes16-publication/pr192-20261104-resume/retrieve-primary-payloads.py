from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,subprocess,urllib.request

root=Path('/workspace/mpje-notes16-qa')
base=Path('reports/full-corpus-review/notes16-publication/pr192-20261104-resume')
(root/base).mkdir(parents=True,exist_ok=True)
api='https://api.github.com/repos/woojunxnam/oddments/'
merge='e8f9b9bcffdb5cf8849ee97ba75b9526bd1cff67'
tested='4c6380f14b516e6486c8ce8e8fdfcf75eb9ce7aa'
def retrieve(name,url):
    destination=base/name
    request=urllib.request.Request(url,headers={'User-Agent':'MPJE-publication-evidence/1'})
    with urllib.request.urlopen(request,timeout=60) as response:
        raw=response.read();status=response.status;final=response.url
    assert status==200 and final==url
    (root/destination).write_bytes(raw)
    return dict(path=str(destination),raw_sha256=hashlib.sha256(raw).hexdigest(),official_url=url,http_status=status,tls_verified=True,retrieved_at_utc=datetime.now(timezone.utc).isoformat())
receipt=dict(schema_version=1,status='PENDING_ROOT_CONTROLLER_ATTESTATION',controller_actor='/root/notes16_engineering',repository='woojunxnam/oddments',published_commit=merge,tested_commit=tested,pull_number=192,canonical_release_credit=0,question_audit_credit=0)
receipt['pull']=retrieve('pull-192.raw.json',api+'pulls/192')
receipt['published_commit_payload']=retrieve('published-commit.raw.json',api+'commits/'+merge)
receipt['tested_commit_payload']=retrieve('tested-commit.raw.json',api+'commits/'+tested)
published=json.loads((root/receipt['published_commit_payload']['path']).read_bytes())
receipt['published_tree']=published['commit']['tree']['sha']
receipt['ci_runs']=[retrieve(f'qa-{run}.raw.json',api+'actions/runs/'+str(run)) for run in [41801395120,41806901962]]
receipt['pages_run']=retrieve('pages-41806902060.raw.json',api+'actions/runs/41806902060')
receipt['public_assets']=[]
for source in ['site/notes/complete-notes.md','site/notes/build.json']:
    binding=retrieve('public-'+source.rsplit('/',1)[-1],'https://woojunxnam.github.io/oddments/'+source.removeprefix('site/'))
    actual=(root/binding['path']).read_bytes()
    expected=subprocess.check_output(['git','-C',str(root),'show',merge+':'+source])
    assert actual==expected,(source,'Public payload differs from published commit')
    receipt['public_assets'].append(dict(source_path=source,payload=binding))
(root/base/'receipt-proposal.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(status='ACTUAL_BYTES_RETAINED_AWAITING_ROOT_ATTESTATION',tree=receipt['published_tree'],payloads=8,actor=receipt['controller_actor']),ensure_ascii=False))
