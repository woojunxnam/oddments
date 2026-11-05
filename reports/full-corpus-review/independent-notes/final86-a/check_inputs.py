import json,hashlib,subprocess,re,sys
from pathlib import Path
from datetime import datetime,timezone
P=Path('reports/full-corpus-review/independent-notes/final86-a'); ROOT='/workspace/oddments'
sha=lambda b:hashlib.sha256(b).hexdigest();digest=lambda o:sha(json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
j=json.loads((P/'assignment.json').read_bytes());v=json.loads((P/'visible-input.json').read_bytes());c=json.loads((P/'related-context.json').read_bytes());assert v['job']==j
captured=v['source_head'];current=subprocess.check_output(['git','-C',ROOT,'rev-parse','HEAD']).decode().strip();cache={}
def raw(head,path):
 key=(head,path)
 if key not in cache:cache[key]=subprocess.check_output(['git','-C',ROOT,'show',head+':'+path])
 return cache[key]
def obj(head,path):
 s=raw(head,path).decode()
 return json.JSONDecoder().raw_decode(s[s.index('{'):])[0] if path.endswith('.js') else json.loads(s)
def questions(x):
 if isinstance(x,dict):
  if 'question_id' in x and 'stem' in x:yield x
  else:
   for val in x.values():yield from questions(val)
 elif isinstance(x,list):
  for val in x:yield from questions(val)
keys=('unit_id','chapter_id','actual_effective_body_sha256','atomic_claim_census_complete','atomic_claim_census_status','atomic_census_source','atomic_census_notes_revision','atomic_claim_ids','atomic_source_blocked_count')
proof={'checked_at_utc':datetime.now(timezone.utc).isoformat(),'captured_source_head':captured,'root_head_observed_for_current_equivalence':current,'strict_inventory_boundary_ko':'Root가 full load_notes/native inventory로 실제 current packet을 검증했다고 전달한 관찰은 아래 raw SHA로 묶었다. Worker는 sparse preimage 누락 때문에 loader를 호출·모킹·우회하지 않았다. 아래는 actual committed Git objects 및 전달원bytes의 독립 바이트/필드 대조이며 strict loader 재실행으로 위장하지 않는다.','input_original_bytes':{},'heads':{}}
for base,own in [('notes-final86-a-assignment.json','assignment.json'),('notes-final86-a-visible-input.json','visible-input.json'),('notes-final86-a-related-context.json','related-context.json')]:
 a=Path('/workspace/scratch')/base;b=P/own;assert a.read_bytes()==b.read_bytes();proof['input_original_bytes'][own]={'raw_sha256':sha(b.read_bytes()),'matches_original_scratch_bytes':True}
assert sha((P/'related-context.json').read_bytes())=='758d259eed21631c7cd36277432c1510fdeb87a365a31bcea7e24282096d53c3'
inv=Path('/workspace/scratch/notes-final86-verified-inventory.json');assert sha(inv.read_bytes())==v['validated_inventory_raw_sha256'];proof['root_strict_inventory_original_raw_sha256']=sha(inv.read_bytes())
for head in dict.fromkeys([captured,current]):
 guide=obj(head,'notes/guide.json');units={u['id']:u for ch in guide['chapters'] for u in ch['units']};ledger={r['unit_id']:r for r in map(json.loads,raw(head,'reports/full-corpus-review/notes-unit-ledger.jsonl').decode().splitlines())};rows=[]
 for u in v['units']:
  uid=u['unit']['id'];b=j['unit_bindings'][uid];assert b==u['binding'];assert sha(u['unit']['body'].encode())==b['body_sha256'];assert {k:units[uid][k] for k in ['id','title','body']}==u['unit']
  censusraw=raw(head,b['census_path']);assert sha(censusraw)==b['census_sha256'];census=json.loads(censusraw);cu=[x for x in census['units'] if x['unit_id']==uid];cl=[x for x in census['claims'] if x['unit_id']==uid];assert cu==[u['census_unit']] and cl==u['claims'];assert digest(cu[0])==b['census_unit_record_sha256'];assert {x['claim_id']:digest(x) for x in cl}==b['claim_record_sha256s'];assert digest({k:ledger[uid].get(k) for k in keys})==b['ledger_binding_sha256']
  rows.append({'unit_id':uid,'body_sha256':b['body_sha256'],'census_raw_sha256':b['census_sha256'],'census_unit_record_sha256':b['census_unit_record_sha256'],'claim_record_count':len(cl),'all_claim_digests_match':True,'ledger_binding_sha256':b['ledger_binding_sha256']})
 qp=[]
 for entry in c['questions']:
  full=[q for q in questions(obj(head,entry['source_path'])) if q['question_id']==entry['question']['question_id']];assert len(full)==1
  assert {k:full[0][k] for k in entry['question']}==entry['question'];qp.append({'question_id':entry['question']['question_id'],'visible_record_sha256':digest(entry['question']),'visible_fields_match_captured':True,'complete_record_hash_matches_captured':digest(full[0])==entry['complete_record_sha256']})
 dp=[]
 for entry in c['derived']:
  vis=entry['visible_item'];ident=vis.get('id',vis.get('term'));full=[x for x in obj(head,entry['source_path'])[entry['collection']] if x.get('id',x.get('term'))==ident];assert len(full)==1;assert {k:full[0][k] for k in vis}==vis
  for uid,h in vis.get('source_hashes',{}).items():
   if uid in j['unit_bindings']:assert h==j['unit_bindings'][uid]['body_sha256']
  dp.append({'id_or_term':ident,'visible_record_sha256':digest(vis),'visible_fields_match_captured':True,'complete_record_hash_matches_captured':digest(full[0])==entry['complete_record_sha256'],'assigned_source_hashes_match':True if vis.get('source_hashes') else 'NOT_PRESENT_GLOSSARY_NO_SOURCE_HASH_ASSERTION'})
 assert len(qp)==40 and len(dp)==12;assert c['missing_related_ids']==[]
 proof['heads'][head]={'units':rows,'questions':qp,'derived':dp,'related_source_file_raw_sha256s':{path:sha(raw(head,path)) for path in c['source_files']}}
# Anchor links only; no additional question IDs were embedded in the assigned bodies.
proof['body_links']=[{'unit_id':u['unit']['id'],'links':re.findall(r'\]\(([^)]+)\)',u['unit']['body'])} for u in v['units'] if '](' in u['unit']['body']]
proof['captured_and_observed_current_selected_content_equivalent']=True;proof['canonical_release_credit']=0;proof['question_audit_credit']=0
(Path(sys.argv[1]) if len(sys.argv)>1 else P/'input-verification.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n')
print('ACTUAL_GIT_OBJECT_BINDING_AND_VISIBLE_CONTEXT_PASS',captured,current,len(j['unit_ids']),sum(len(u['claims']) for u in v['units']),len(c['questions']),len(c['derived']))
