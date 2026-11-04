import sys,json,hashlib,subprocess
from pathlib import Path
root=Path('/tmp/remediation10-integration-preview-e');sys.path.insert(0,str(root/'scripts'))
import remediation_batch_registry as batch
import build_representative_rewrites as compiler
for path,data in compiler.build().items():path.write_bytes(batch.encoded(data))
config_path=root/'site/practice-expansion/publication.json';config=json.loads(config_path.read_bytes())
for addition in config['additional_banks']:
 if addition['path']==batch.BASE+'/questions.json':
  addition['sha256']=batch.sha((root/addition['path']).read_bytes());addition['question_count']=87
config['published_total']=2359;config['representative_selection']['sha256']=batch.sha((root/config['representative_selection']['path']).read_bytes());config_path.write_bytes(batch.encoded(config))
subprocess.run(['git','-C',str(root),'config','user.name','Temporary Engineering Preview'],check=True)
subprocess.run(['git','-C',str(root),'config','user.email','preview@example.test'],check=True)
subprocess.run(['git','-C',str(root),'add','.'],check=True)
if subprocess.check_output(['git','-C',str(root),'status','--porcelain']).strip():
 subprocess.run(['git','-C',str(root),'commit','--quiet','-m','TEMPORARY proposed generated preview; not root publication'],check=True)
import publish_practice
published=publish_practice.build_payload()
import build_representative_audit_ledger as audit
ledger=audit.build_ledger()
import build_full_corpus_review as core
outputs=core.build()
rows=[json.loads(s) for s in outputs[root/'reports/full-corpus-review/question-ledger.jsonl'].splitlines()]
new=set(batch.current_baseline(root)['candidate_question_hashes']);newrows=[r for r in rows if r['question_id'] in new]
assert len(newrows)==10 and all(r['checked_at'] is None and r['author_review_increment']==0 and r['current_id_author_review_required'] is True for r in newrows)
assert len(rows)==2359 and sum(r['checked_at'] is not None for r in rows)==2349
assert published['quality_selection']['recommended_ids']==batch.read(root,batch.BASE+'/selection.json')['recommended_ids']
assert len(published['quality_selection']['recommended_ids'])==202
for p,text in outputs.items():p.write_text(text)
subprocess.run(['git','-C',str(root),'add','.'],check=True)
if subprocess.check_output(['git','-C',str(root),'status','--porcelain']).strip():
 subprocess.run(['git','-C',str(root),'commit','--quiet','-m','TEMPORARY pending inventory preview; author54 remains unperformed'],check=True)
state=batch.read(root,'reports/full-corpus-review/work-queue.json')
import review_queue as queue
created=queue.plan(state,queue.read_ledger(root),root,batches=1,size=10,at='2026-11-04T15:00:00+00:00')
assert created==['review-84326c0189affeae'] and state['jobs'][-1]['sequence']==54
result=dict(stage='ISOLATED_TEMPORARY_ENGINEERING_PREVIEW_NOT_PUBLICATION',source_commit='efef468bfb635aa7d09e934cf65de6e1195e0ead',temporary_head=subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip(),source_bank_questions=len(batch.read(root,batch.BASE+'/questions.json')['questions']),source_bank_sources=len(batch.read(root,batch.BASE+'/questions.json')['sources']),prospective_combined_records=len(published['questions']),old_delivered_baseline_records=2349,default_count=len(published['quality_selection']['recommended_ids']),old355_implementation_counts=ledger['counts']['implementation_statuses'],native_author_pending_ids=sorted(new),native_author_pending_count=len(newrows),prospective_checked_count=sum(r['checked_at'] is not None for r in rows),native_author_plan_ids=created,native_author_sequence=54,author54_claim_submit_integrate_executed=False,root_shared_generated_changed=False,public_activation=False,canonical_release_credit=0,new_independent_review_credit=0,proposed_bank_sha256=batch.sha((root/batch.BASE/'questions.json').read_bytes()),proposed_selection_sha256=batch.sha((root/batch.BASE/'selection.json').read_bytes()))
Path('/tmp/remediation10-preview-result.json').write_bytes(batch.encoded(result));print(json.dumps(result,indent=2))
