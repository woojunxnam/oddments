import sys,json,subprocess
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/'scripts'))
import note_review_queue as q
from notes_census_reassessment import replacement_row
OUT=Path(__file__).resolve().parent;ROOT=Path.cwd();PREFIX=OUT.relative_to(ROOT).as_posix()
def read(p):return json.loads(Path(p).read_text())
def sha(p):return q.raw_sha(Path(p).read_bytes())
def write(n,d):(OUT/n).write_bytes(q.encoded(d))
def gitraw(head,p):return subprocess.check_output(['git','show',head+':'+p])
j=read(OUT/'assignment.json');packet=read(OUT/'visible-input.json');u=packet['units'][0];uid='w3-c-1';b=j['unit_bindings'][uid];ctx=read(OUT/'related-context.json');head=ctx['source_head']
assert packet['job']==j and u['binding']==b and u['unit']['id']==uid
assert sha(OUT/'related-context.json')=='ff96a1f66c02fdb30fbd0b7425e5642f0cdeee63fc608d859b890cbfd27e2f7d'
assert q.raw_sha(u['unit']['body'].encode())==b['body_sha256']
census=read(b['census_path']);assert sha(b['census_path'])==b['census_sha256'] and census['claims']==u['claims'] and census['units'][0]==u['census_unit']
assert q.digest(u['census_unit'])==b['census_unit_record_sha256'] and {c['claim_id']:q.digest(c) for c in u['claims']}==b['claim_record_sha256s']
rrpath='reports/full-corpus-review/notes101-census-author/w3-c-1-reassessment.json';rr=read(rrpath);assert sha(rrpath)==j['reassessment_record_sha256'];assert q.digest(replacement_row(rr,census))==b['ledger_binding_sha256']
oldraw=gitraw(j['base_commit'],rr['previous_binding']['census_path']);assert q.raw_sha(oldraw)==rr['previous_binding']['census_sha256'];old=json.loads(oldraw);assert [c for c in old['claims'] if c['unit_id']==uid]==u['claims'][:23]
oldreportraw=gitraw(j['base_commit'],rr['previous_report']['path']);assert q.raw_sha(oldreportraw)==rr['previous_report']['raw_sha256'];oldrow=next(r for r in json.loads(oldreportraw)['records'] if r['unit_id']==uid);assert len(oldrow['omissions'])==1
assert q.raw_sha(oldrow['omissions'][0].encode())==j['reassessment_review']['omission_resolutions'][0]['omission_sha256'] and j['carried_legal_blockers'][uid]=={}
revision_path='revisions/notes/2026-10-30-cdtm13-vax04.json';revision_raw=gitraw(head,revision_path);revision=json.loads(revision_raw);actual=next(x for x in revision['units'] if x['id']==uid);assert actual['body']==u['unit']['body']
assert q.raw_sha(gitraw(head,b['census_path']))==b['census_sha256']
ledger_raw=gitraw(head,q.LEDGER);ledger=next(json.loads(l) for l in ledger_raw.splitlines() if json.loads(l)['unit_id']==uid);fields={k:ledger.get(k) for k in replacement_row(rr,census)};assert q.digest(fields)==b['ledger_binding_sha256']
for d in ctx['derived']:assert d['visible_item']['source_hashes'][uid]==b['body_sha256']
for f in ['site/notes/study-data.js','site/notes/refresh-data.js']:assert q.raw_sha(gitraw(head,f))==ctx['source_files'][f]
assert len(ctx['questions'])==5 and not ctx['missing_related_ids'] and len(ctx['derived'])==4
for x in ctx['questions']:
 raw=gitraw(head,x['source_path']);d=json.loads(raw);records=d['questions'] if isinstance(d,dict) else d;current=next(z for z in records if z['question_id']==x['question']['question_id'])
 for k in ['stem','choices','correct_choice_ids','explanation']:assert current[k]==x['question'][k]
extra=read(OUT/'body-linked-extra-questions-current.json');assert len(extra['questions'])==4 and extra['source_head']==head
for f,s in extra['source_file_raw_sha256s'].items():assert q.raw_sha(gitraw(head,f))==s
assert gitraw(head,'site/notes/cdtm13-16-vax01-04.html')==(OUT/'body-linked-vax01-original-amendment.html').read_bytes()
write('input-source-verification.json',{'assignment_packet_matches':True,'current_source_head':head,'actual_body_revision_source_path':revision_path,'actual_body_revision_source_raw_sha256':q.raw_sha(revision_raw),'current_committed_body_census_unit_all_24_claim_hashes_match':True,'current_committed_ledger_binding_matches':True,'native_replacement_row_binding_matches':True,'original_23_claim_objects_preserved_exactly':True,'original_report_raw_sha256':q.raw_sha(oldreportraw),'original_omission_sha256':q.raw_sha(oldrow['omissions'][0].encode()),'inherited_claim_legal_blockers':{},'related_questions_read_completely':5,'body_linked_extra_questions_read_completely':4,'derived_read_completely':4,'related_question_visible_fields_match_committed_current':True,'source_head_derived_file_hashes_match':True,'strict_inventory_observation':'Root observed ordinary strict current inventory; worker independently verifies committed current source HEAD body/census/claims/ledger, and source bytes; no notes loader/guard changes.','canonical_release_credit':0,'question_audit_credit':0})
def authority(name,section):
 m=read(OUT/'sources'/f'{name}.meta.json');ext='.raw' if name=='law24g' else '.pdf';return {'source_type':'PUBLIC_OFFICIAL','official_url':m['official_url'],'exact_section':section,'law_checked_date':'2026-11-04','version_or_effective_date_status':{'vaccine':'Policy2023-02 adopted2023-05-04; revised2023-09-07,2025-09-04. PDF prints no separate effective date. Live official HTTPS retrieval2026-11-04. State policy path only; no federal PREP pathway determination.','ratios':'Policy2026-02 adopted2026-09-03; supersedes Policy2024-03. No separate effective date printed. Live official HTTPS retrieval2026-11-04.','law24g':'Current official Massachusetts General Laws c112§24G posted text retrieved live2026-11-04; individual amendment effective date not separately established.'}[name],'evidence_path':PREFIX+'/sources/'+name+ext,'evidence_sha256':sha(OUT/'sources'/(name+ext)),'text_evidence_path':PREFIX+'/sources/'+name+'.txt','text_evidence_sha256':sha(OUT/'sources'/f'{name}.txt'),'retrieval_metadata_path':PREFIX+'/sources/'+name+'.meta.json','retrieval_metadata_sha256':sha(OUT/'sources'/f'{name}.meta.json')}
# Actual manual legal decisions after reading the complete policy, statute, final census and context.
findings=[
('Introduction, pharmacy personnel definition','정의는 licensed pharmacists, pharmacy interns, pharmacy technicians를 명시한다.'),
('Introduction, pharmacy personnel definition; III.D.1','정의와III.D.1은 PTT를 명시적으로 제외한다. 주 policy 경로에 한정한 본문이다.'),
('Introduction, pharmacy personnel definition; III.D.1–3','PTT 제외는 교육요건과 별개다. course나 employer approval만으로 제외된 직종의 권한이 생기지 않는다.'),
('Introduction; III.C.1','licensed pharmacist 지위와 pharmacist/intern의 사전 ACPE training을 함께 요구한다. 본문의 license/초기교육 최소 명제를 지지한다.'),
('III.A; Introduction, qualified direct supervisor requirement','모든 투여 personnel의 current CPR을 명시하며 감독자는 모든 immunizer 요건을 충족해야 한다.'),
('III.C.3','pharmacist는 매 calendar year ACPE-approved immunization-related CE 최소1시간을 이수해야 한다. 본문은 일반 유지교육 요건만 주장한다.'),
('III.C introductory paragraph and III.C.1','pharmacy intern도 투여 전 ACPE accredited course를 이수해야 한다.'),
('Introduction, intern/technician approval paragraph','intern 투여에는 on-duty licensed pharmacist approval이 필요하다.'),
('Introduction, intern/technician approval paragraph','intern의 direct supervisor는 면허 있는 약사이며 policy의 모든 immunizer 요건을 충족해야 한다.'),
('III.D.1(a)–(b)','주 PT 면허와 함께 national certification 또는 PT면허후500시간의 대체경로를 명시한다. trainee500시간과 다르다.'),
('III.D.2','technician은 assessment 포함 ACPE6-hour program을 완료해야 한다.'),
('III.D.3','6시간course 외에 experienced certified immunizer와 최소2시간 documented OJT 및 Skills Checklist를 요구한다.'),
('Introduction, intern/technician approval paragraph','적격 technician도 on-duty licensed pharmacist approval이 필요하다.'),
('Introduction, intern/technician approval paragraph','technician도 모든 immunizer 요건을 충족한 licensed pharmacist의 direct supervision이 필요하다.'),
('III.D.4','약사가 환자 상담과 백신 선택을 한 뒤 technician이 수행할 수 있는 행위는 physical preparation/administration이다.'),
('III.D.4','technician의 허용행위는 physical act로 제한하며 pharmacist selection/counseling을 선행조건으로 둔다. 독립 임상 권한으로 확대하지 않는다.'),
('Introduction; Policy2026-02 II, direct-supervision definition','전화승인은 premises에서의 contemporaneous observation/direction을 대체하지 않는다. intern의 일반 직접감독 정의와 vaccine policy의 qualified direct supervision을 함께 적용한다.'),
('Introduction; Policy2026-02 II, direct-supervision definition','MOR라는 직함이나 다른 장소에서의 전화승인만으로 현장의 qualified direct supervision이 충족되지 않는다.'),
('Introduction; III.A; MGLc112§24G second paragraph','intern 교육이 충분해도 supervisor가 모든 immunizer 요건을 충족해야 한다. CPR 만료 감독자를 허용하지 않는다.'),
('Policy2026-02 I and II; Policy2023-02 Introduction','ratios 규칙과 supervision 규칙은 각각 별도 절이다. vaccination staffing ratio 특례가 자격 있는 직접감독 조건을 삭제하지 않는다. 본문은 특정수치를 새로 주장하지 않는다.'),
('IV.A','투여 vaccine에는 prescription 또는 standing order가 필요하다.'),
('III.D.4','백신선택/상담과 technician에게 허용된 physical preparation/injection은 정책상 별개 행위다.'),
('IV.B; III.D.4','adverse-event emergency medication에도 prescription 또는 standing order가 필요하며 technician의 해당 제공은 standing order에 따른다.'),
('III.C.2(c),(g); III.D.4; IX Appendix, inclusion/exclusion criteria','새024는 원래 빠졌던 투여 전 screening을 독립 명제로 열거했다. Clinical evaluation of indications/contraindications, pre-administration education/screening 및 투여 전 standing-order inclusion/exclusion 평가를 문언으로 확인했다. 약사의 vaccine 선택·상담과 technician의 physical-only 범위를 함께 읽어 screening 임상판단의 주체를 판정했다. Training goal을 별도 처방권 또는 진단권으로 확대하지 않는다.')]
claims=[]
for n,(c,(section,finding)) in enumerate(zip(u['claims'],findings),1):
 auth=[authority('ratios',section)] if n==20 else [authority('vaccine',section)]
 if n in [17,18]:auth.append(authority('ratios','II, direct-supervision definition (on premises, contemporaneous observation/direction, readily available)'))
 if n in [9,19]:auth.append(authority('law24g','Section24G, second paragraph (intern immunization training and fully qualified supervising pharmacist)'))
 if n==20:auth.append(authority('vaccine','Introduction, qualified direct supervision requirements'))
 r={'claim_id':c['claim_id'],'claim_record_sha256':b['claim_record_sha256s'][c['claim_id']],'statement_ko':c['statement_ko'],'claim_read_completely':True,'legal_status':'KEEP','finding':finding,'authorities':auth};claims.append(r)
assert len(claims)==24
row={'unit_id':uid,'binding':b,'body_read_completely':True,'completeness':'COMPLETE','omissions':[],'completeness_method':'본문 전문을 문장·표의 직종/자격/행위/조건별로 최종24명제와 대조했다. 001–003은직종/PTT제외,004–007은license/교육/CPR/CE,008–009와013–014는승인·감독,010–012는PT대체경로·6+2교육,015–016·022는임상행위와물리행위분리,017–020은현장감독·MOR·부적격감독·ratio별도평가,021·023은vaccine/emergency medication order,024는투여전screening을 포괄한다. 원래 screening omission의 정확문자열을 읽고024의 실제명제 및 III.C.2(c),(g),IX와 대조해 해소를 확인했다. 원23개 claim object와 source metadata가 그대로 보존됨을 확인했다. 본문의 연습링크/작성일/학습권고는 비법규이며 수치를 새로 만들지 않는다.','legal_status':'KEEP','claims':claims,'reassessment_review':{**j['reassessment_review'],'final_census_read_completely':True,'all_original_omissions_reassessed':True,'all_original_propositions_preserved':True},'original_omission_reassessment':[{'original_omission':oldrow['omissions'][0],'omission_sha256':q.raw_sha(oldrow['omissions'][0].encode()),'resolution':'RESOLVED_IN_CENSUS','claim_ids':[u['claims'][-1]['claim_id']],'finding':'원래23명제 외에024가 pharmacist pre-administration screening 판단을 실제 추가했다. 보완 저자의 완료 선언에 의존하지 않고 fresh official PDF 전문의 지정조항을 직접 대조했다.'}],'related_context_review':{'all_questions_and_each_choice_and_explanation_read':True,'related_question_ids':ctx['related_ids'],'extra_body_linked_question_ids':[x['visible_question']['question_id'] for x in extra['questions']],'derived_read_completely':True,'derived_ids':[x['visible_item']['id'] for x in ctx['derived']],'finding':'5개배정문항과본문직접연결RW0041/VAX01원본추가3개,총9문항의stem/모든보기/정답/전체해설을 읽었다. 직종제외·교육·CPR·감독·PT경로·6+2교육 관련주장은 본단원과관련있으며 official policy와맞는다. inherited note body SHA가과거값인 metadata는 현재본문의근거로승계하지 않았다. derived4개의현재bodysource SHA를 확인했고 supervision/권한분리문구를 읽었다. CDTM·타약물route·flu population 등다른단원의독립PASS를 주장하지 않는다. question/canonicalcredit0.'}}
report={k:j[k] for k in ['stage','actor_provenance','auditor','auditor_instance']};report.update({'independent_of_authors':True,'canonical_audit':False,'canonical_release_credit':0,'question_audit_credit':0,'reviewed_at':'2026-11-04','records':[row],'limitations_ko':'배정된변경없는w3-c-1본문과최종24claim의독립판정이다. 주vaccine policy경로만검토했으며 PREP Act경로·타단원의권한·문항canonicalrelease를승인하지 않는다. 원래claim법규blocker는없고 순수screening census누락이해소됐다. 같은auditorinstance로인원credit를추가하지 않는다.'});write('report.json',report)
manifest=[{'path':f.relative_to(ROOT).as_posix(),'raw_sha256':sha(f)} for f in sorted(OUT.rglob('*')) if f.is_file() and f.name not in ['source-manifest.json']];write('source-manifest.json',manifest)
print('report',sha(OUT/'report.json'),'COMPLETE/KEEP24', 'current_source_head',head)
