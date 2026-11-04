from pathlib import Path
from collections import Counter
import json,hashlib
root=Path(__file__).resolve().parents[3]
def read(p):return json.loads((root/p).read_text())
def sha(raw):return hashlib.sha256(raw).hexdigest()
def write(p,obj):(root/p).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
before_path='reports/phase10-default-qa-e/before-phase10-selection.json'; before=read(before_path);defaults=set(before['recommended_ids']);assert len(defaults)==229
state=read('reports/full-corpus-review/independent-legacy-work-queue.json');jobs=state['jobs'][33:37];assert len(jobs)==4 and all(j['status']=='INTEGRATED' for j in jobs)
hp='reports/representative-rewrite/nonlegacy-default-holds.json';hold_snapshot='reports/full-corpus-review/phase10-before-nonlegacy-default-holds.json'
if not (root/hold_snapshot).exists():(root/hold_snapshot).write_bytes((root/hp).read_bytes())
holds=read(hold_snapshot);original_holds=json.loads(json.dumps(holds['holds']));existing={x['question_id'] for x in original_holds}
np='reports/representative-rewrite/archive-review-notices.json';notice_snapshot='reports/full-corpus-review/phase10-before-archive-review-notices.json'
if not (root/notice_snapshot).exists():(root/notice_snapshot).write_bytes((root/np).read_bytes())
notices=read(notice_snapshot);original_notices=json.loads(json.dumps(notices['notices']));notice_ids={qid for n in original_notices for qid in n['question_ids']};original_notice_by_id={qid:n for n in original_notices for qid in n['question_ids']};new_notices=[]
rows=[];sources=[];summary=Counter();default_negative=[]
for letter,job in zip('abcd',jobs):
 path='reports/full-corpus-review/independent-phase10-'+letter+'-review.json';raw=(root/path).read_bytes();report=json.loads(raw);digest=sha(raw)
 sources.append({'job_id':job['job_id'],'worker_commit':job['result']['worker_commit'],'report_path':path,'raw_sha256':digest})
 assert set(job['question_hashes'])=={r['question_id'] for r in report['records']}
 for r in report['records']:
  qid=r['question_id'];legal=r['legal_review'];real=r['realism_review'];summary['legal_'+legal['verdict']]+=1;summary['key_'+legal['existing_answer_correct']]+=1;summary['realism_'+real['verdict']]+=1
  negative=legal['verdict']!='KEEP' or legal['existing_answer_correct']!='YES' or real['verdict']!='PASS'
  if not negative:continue
  action=r['required_next_action_ko'];assert isinstance(action,str) and action.strip()
  detail=' '.join(str(part).strip() for part in [legal.get('finding_ko',''),real.get('finding_ko',''),action] if part)
  reason=f"독립 검토: 법규 {legal['verdict']}, 저장 정답 {legal['existing_answer_correct']}, 현실성 {real['verdict']}. {detail} 원문·정답·과거 사용자기록을 보존하며 확인한 결함 또는 절차 보류가 해결되기 전 기본 연습에서 제외합니다."
  binding={'question_id':qid,'record_sha256':r['record_sha256'],'review_source':path,'review_source_sha256':digest,'legal_verdict':legal['verdict'],'existing_answer_correct':legal['existing_answer_correct'],'realism_verdict':real['verdict'],'new_review_credit':0}
  assert r['record_sha256']==job['question_hashes'][qid]
  if qid in defaults:
   assert qid not in existing
   holds['holds'].append({'question_id':qid,'question_record_sha256':r['record_sha256'],'review_source':path,'review_source_sha256':digest,'reason':reason,'next_action':action});default_negative.append(qid);binding['action']='HOLD_FROM_DEFAULT_PRESERVE_ARCHIVE_AND_HISTORY'
  else:binding['action']='PRESERVE_ARCHIVE_ADD_SOURCE_BOUND_REVIEW_NOTICE'
  if not qid.startswith('MA-RW-'):
   new_notices.append({'question_ids':[qid],'issue_type':'INDEPENDENT_REVIEW_FINDING','reason':reason,'checked_at':report['review_date'],'question_record_hashes':{qid:r['record_sha256']},'review_source':path,'review_source_sha256':digest});
   if qid in original_notice_by_id:new_notices[-1]['previous_notices']=[original_notice_by_id[qid]]
   binding['archive_notice']=True;binding['newly_notified_archive_id']=qid not in notice_ids
  else:binding['archive_notice']=False;binding['notice_delivery']='EXISTING_NONLEGACY_SAFETY_HOLD_RENDERER'
  rows.append(binding)
assert len(rows)==59 and len(default_negative)==27
new_notice_ids={qid for n in new_notices for qid in n['question_ids']};retained=[]
for old in original_notices:
 remaining=[qid for qid in old['question_ids'] if qid not in new_notice_ids]
 if not remaining:continue
 current=json.loads(json.dumps(old))
 if remaining!=old['question_ids']:current.update(question_ids=remaining,question_record_hashes={qid:old['question_record_hashes'][qid] for qid in remaining})
 retained.append(current)
notices['notices']=retained+new_notices
assert holds['holds'][:len(original_holds)]==original_holds
assert all(old in notices['notices'] or any(old in n.get('previous_notices',[]) for n in new_notices) for old in original_notices)
write(hp,holds);write(np,notices)
write('reports/full-corpus-review/phase10-default-safety-dispositions.json',{'purpose':'ROOT_CONTAINMENT_OF_ACTUAL_INTEGRATED_FINDINGS_NOT_NEW_AUDIT','sources':sources,'before_selection':{'path':before_path,'raw_sha256':sha((root/before_path).read_bytes())},'reviewed_ids':160,'reviewed_default_ids':128,'reviewed_archive_ids':32,'summary':dict(summary),'negative_records':len(rows),'new_default_holds':len(default_negative),'default_before':229,'default_after_expected':len(defaults-set(default_negative)),'default_removed_ids':sorted(default_negative),'archive_notice_records_written':sum(r['archive_notice'] for r in rows),'newly_notified_archive_ids':sum(r.get('newly_notified_archive_id',False) for r in rows),'previous_notice_snapshot':{'path':notice_snapshot,'raw_sha256':sha((root/notice_snapshot).read_bytes())},'previous_hold_snapshot':{'path':hold_snapshot,'raw_sha256':sha((root/hold_snapshot).read_bytes())},'new_review_credit':0,'canonical_release_credit':0,'records':rows})
print(json.dumps({'negative_records':len(rows),'new_default_holds':len(default_negative),'archive_notice_records_written':sum(r['archive_notice'] for r in rows),'newly_notified_archive_ids':sum(r.get('newly_notified_archive_id',False) for r in rows),'previous_notice_snapshot':{'path':notice_snapshot,'raw_sha256':sha((root/notice_snapshot).read_bytes())},'previous_hold_snapshot':{'path':hold_snapshot,'raw_sha256':sha((root/hold_snapshot).read_bytes())},'default_expected':229-len(default_negative),'summary':dict(summary)}))
