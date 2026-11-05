import json,hashlib,subprocess,sys,runpy,collections,re
from pathlib import Path
sys.path.insert(0,'scripts');import note_review_queue as q
B=Path('reports/full-corpus-review/independent-notes/final86-b');job=json.load(open(B/'assignment.json'));packet=json.load(open(B/'visible-input.json'));context=json.load(open(B/'related-context.json'));sha=lambda b:hashlib.sha256(b).hexdigest();F=runpy.run_path(str(B/'claim-findings.py'))['F']
assert packet['job']==job
assert sha((B/'related-context.json').read_bytes())=='974f1a0eeac454ec84ae7e86567e588f723cc033387795790828e7c08d73a479'
def gitraw(head,path):return subprocess.check_output(['git','show',head+':'+path])
checks=[];guide=json.loads(gitraw('HEAD','notes/guide.json'));guideunits={u['id']:u for ch in guide['chapters'] for u in ch.get('units',[])}
for u in packet['units']:
 uid=u['unit']['id'];b=job['unit_bindings'][uid];assert u['binding']==b and sha(u['unit']['body'].encode())==b['body_sha256'];raw=gitraw('HEAD',b['census_path']);assert sha(raw)==b['census_sha256'];c=json.loads(raw);cu=next(z for z in c['units'] if z['unit_id']==uid);cc=[z for z in c['claims'] if z['unit_id']==uid];assert cu==u['census_unit'] and cc==u['claims'];assert q.digest(cu)==b['census_unit_record_sha256'];assert {z['claim_id']:q.digest(z) for z in cc}==b['claim_record_sha256s'];assert len(F[uid])==len(cc)
 body=guideunits[uid]['body'];bodymatch=body==u['unit']['body']
 assert bodymatch,uid+' base guide differs: needs exact revision evidence'
 checks.append({'unit_id':uid,'body_utf8_sha256':b['body_sha256'],'current_committed_guide_body_matches':bodymatch,'census_raw_sha256':sha(raw),'unit_record_sha256':q.digest(cu),'claim_count':len(cc),'all_claim_record_hashes_match':True})
cache={}
def source_json(head,path,js=False):
 k=(head,path)
 if k not in cache:
  raw=gitraw(head,path)
  if head==context['source_head']:assert sha(raw)==context['source_files'][path]
  cache[k]=json.JSONDecoder().raw_decode(raw.decode().split('=',1)[1].lstrip())[0] if js else json.loads(raw)
 return cache[k]
def visiblematch(v,o):return all(k in o and o[k]==val for k,val in v.items())
related=[]
for z in context['questions']:
 def get(head):
  d=source_json(head,z['source_path']);qs=d if isinstance(d,list) else d['questions'];return next(x for x in qs if x['question_id']==z['question']['question_id'])
 orig=get(context['source_head']);assert q.digest(orig)==z['complete_record_sha256'];assert visiblematch(z['question'],orig);assert visiblematch(z['question'],get('HEAD'))
 related.append({'id':z['question']['question_id'],'original_full_record_hash_matches':True,'original_and_current_visible_projection_equal':True})
for z in context['derived']:
 v=z['visible_item'];identifier=v.get('id',v.get('term'))
 def get(head):
  d=source_json(head,z['source_path'],True);return next(x for x in d[z['collection']] if x.get('id',x.get('term'))==identifier)
 orig=get(context['source_head']);assert q.digest(orig)==z['complete_record_sha256'];assert visiblematch(v,orig);assert visiblematch(v,get('HEAD'))
 for uid,h in v.get('source_hashes',{}).items():
  if uid in job['unit_bindings']:assert h==job['unit_bindings'][uid]['body_sha256']
 related.append({'id':identifier,'collection':z['collection'],'original_full_record_hash_matches':True,'original_and_current_visible_projection_equal':True})
assert len(checks)==20 and sum(x['claim_count'] for x in checks)==405 and len(context['questions'])==65 and len(context['derived'])==21 and not context['missing_related_ids']
(B/'input-validation.json').write_text(json.dumps({'checked_head':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'original_context_source_head':context['source_head'],'inputs_raw_sha256':{p.name:sha(p.read_bytes()) for p in [B/'assignment.json',B/'visible-input.json',B/'related-context.json']},'unit_checks':checks,'related_original_record_and_visible_checks':related,'root_strict_inventory_observation':'Root가 실제 strict load_notes inventory로 현재body/census/claim을 대조하여 전달한 projection. Worker는 sparse missing preimage guard를 우회·모킹하지 않았다. 이 provenance와 hash 일치는 법규 PASS를 뜻하지 않는다.','original_metadata_advance_handling':'원 source_head의 full source file·full record hash를 프로그램으로만 검증했다. 원·현재의 가시 projection은 별도로 대조하고 원입력 bytes를 덮어쓰지 않았다.','human_read':{'full_bodies':20,'all_propositions':405,'questions_full_stems_all_choices_keys_complete_korean_explanations':65,'derived_visible_text':21,'prior_model_conclusions_used':False}},ensure_ascii=False,indent=2)+'\n')
spec={}
def add(uid,a,b,keys,section):
 for n in range(a,b+1):
  assert (uid,n) not in spec;spec[(uid,n)]=(keys.split(','),section)
add('w4-c-16',1,8,'pharmacists,gpo360eee','21 USC 360eee(2),(12),(13),(24); FDA Pharmacists Confirm/Receive/Store/Provide/Investigate')
add('w4-c-16',9,9,'exemption2024','2024-07-12 small-dispenser letter pp1–3, expiration 2026-11-27')
add('w4-c-16',10,22,'exemption2026','2026-08-06 letter pp1–3 and footnotes14–15; effective period and corporate-entity employee definition')
add('w4-c-16',23,23,'exemption2024,exemption2026','2024 letter footnote7; 2026 letter footnote14: distinct assessment dates')
add('w4-c-16',24,28,'exemption2026','2026 letter pp2–3, specifically enumerated bullets and last two paragraphs')
add('w4-c-17',1,10,'exemption2026,gpo360eee-1,pharmacists','21 USC 360eee-1(d)(1),(3),(4); 2026 exemption letter pp2–3 limited paragraphs; FDA Pharmacists requirements')
add('w4-c-17',11,11,'exemption2026','2026 exemption letter final paragraph, continued implementation efforts strongly urged')
add('w4-c-17',12,15,'exemption2026,gpo360eee-1','21 USC 360eee-1(k)(1); 2026 letter footnote17; (d)(1),(4) retention requirements')
add('w4-c-18',1,8,'gpo360eee,pharmacists','21 USC 360eee(2)(A)–(D),(9)(C); FDA Pharmacists Confirm')
add('w4-c-18',9,13,'gpo360eee','21 USC 360eee(14),(20), product identifier and standardized numerical identifier definitions')
add('w4-c-18',14,15,'exemption2026','2026 exemption letter pp2–3 specific verification/enhanced-system exemptions')
add('w4-c-18',16,16,'gpo360eee-1','21 USC 360eee-1(g)(2)(A), third-party confidential written agreement and no relief of dispenser obligations')
add('w4-c-19',1,6,'gpo360eee','21 USC 360eee(21)(A)–(D), suspect product, including serious-harm qualifiers in (B),(D)')
add('w4-c-19',7,10,'gpo360eee-1,exemption2026','21 USC 360eee-1(d)(4)(A)(i),(ii); 2026 letter verification bullets')
add('w4-c-19',11,16,'gpo360eee','21 USC 360eee(8)(A)–(D), illegitimate product and credible-evidence threshold')
add('w4-c-19',17,20,'illegitimate,gpo360eee-1','FDA Notify FDA of Illegitimate Products, notification and submission instructions; 21 USC 360eee-1(d)(4)(B)(ii)')
add('w4-c-19',21,22,'illegitimate,gpo360eee-1','FDA Terminating Notifications; 21 USC 360eee-1(d)(4)(B)(iv)')
add('w4-c-19',23,23,'gpo360eee-1','21 USC 360eee-1(d)(4)(A)(iv),(B)(v), investigation/disposition retention')
add('w4-c-20',1,5,'recall,gpo360eee','21 CFR 7.3(g); 21 USC 360eee(8),(21), distinct recall/suspect/illegitimate definitions')
add('w4-c-20',6,8,'gpo360eee','21 USC 360eee(17), return definition')
add('w4-c-20',9,10,'gpo360eee-1,exemption2026','21 USC 360eee-1(g)(1)(F),(k)(2); 2026 letter enhanced saleable-return exemption; old (d)(1)(C)(i) sunset distinguished')
add('w4-c-20',11,14,'gpo353b,compounding,outsourcing','21 USC 353b(a) exemptions and conditions; FDA Compounding provisions chart, section582 exemption and CGMP distinction')
add('w4-c-20',15,15,'compounding','FDA compounding exemptions describe federal provisions only; MA247CMR21 current exact source unavailable')
add('w4-c-20',16,16,'gpo360eee-1,gpo353b','21 USC 360eee-1 dispenser duties and 353b conditional exemptions are distinct from product approval and state authority')
add('w4-c-15',1,3,'wholesale','247 CMR 7.02(1),(3), prebusiness licence and separate location requirements')
add('w4-c-15',4,13,'wholesale','247 CMR 7.03(3); 7.04(1)–(8), storage, quarantine, shipping inspection and returns')
add('w4-c-15',14,23,'wholesale','247 CMR 7.04(9),(10), records, two-year retention, offsite retrieval and written recall/crisis procedures')
add('w4-c-15',24,30,'1307.11','21 CFR 1307.11(a)–(c), distribution between registered practitioners, ScheduleI/II order forms and five-percent annual threshold')
add('w4-c-15',31,33,'gpo360eee,gpo360eee-1,wholesale','21 USC 360eee(19),(24)(B)(iii) specific-patient-need exception; 360eee-1(d)(1)(A)(ii);247CMR7.02/7.04 distinct wholesale obligations')
add('w6-a-2',1,3,'ind','FDA IND Application, Introduction: interstate transport and research permission distinguished from commercial marketing approval')
add('w6-a-2',4,7,'nda','FDA NDA, Introduction: proposed approval, safety/effectiveness, labeling and manufacturing controls')
add('w6-a-2',8,11,'anda','FDA ANDA Introduction: generic comparability, abbreviated application and bioequivalence')
add('w6-a-2',12,13,'bla','FDA BLA Process, Introduction and FAQs: product licence, interstate commerce and IND comparison')
add('w6-a-2',14,16,'biosimilar','FDA Biosimilar Basics, What is a biosimilar and interchangeable biosimilar; substitution subject to state pharmacy law')
add('w6-a-4',1,8,'otc,monograph','FDA Nonprescription Drug Application Process, NDA/ANDA and Rx-to-OTC/direct-to-OTC sections; OTC Monographs section505G conditions')
add('w6-a-4',9,15,'monograph,homeopathic','FDA OTC Drug Review Process: GRASE conditions and administrative orders; Homeopathic Products: no FDA-approved homeopathic products')
add('w6-a-5',1,7,'offlabel','FDA Understanding Unapproved Use of Approved Drugs, questions on approved drugs used for new indication/dose/route and provider judgment')
add('w6-a-5',8,15,'fdaterms,eua','FDA Understanding FDA Terms, EUA section; Emergency Use Authorization framework, emergency conditions and revocation/termination')
add('w6-a-5',16,21,'expanded,fdaterms','FDA Expanded Access, definition and criteria: serious disease, alternatives, benefit-risk, no interference with trials; separate from marketing approval')
add('w6-a-6',1,7,'supplement,ndi','FDA Dietary Supplements overview; NDI Background for Industry, notification not approval and conditions/75-day submission')
add('w6-a-6',8,13,'cosmetic','FDA Authority Over Cosmetics, intended-use distinction and no premarket approval except certain color additives; unrelated outdated recall/VCRP portions not relied upon')
add('w6-a-6',14,18,'homeopathic','FDA Homeopathic Products, no FDA-approved homeopathic products and risk-based enforcement guidance')
add('w6-a-6',19,23,'510k','FDA 510(k) Clearances, premarket notification and substantial-equivalence criteria distinguished from drug approval')
add('ndc-approval',1,1,'ndc','FDA NDC Product File Definitions, Important Considerations and NDC assignment/listing disclaimer')
add('ndc-approval',2,3,'dailymed','NLM About DailyMed, label/product scope and current-distribution/FDA-approved-label limitations')
add('ndc-approval',4,7,'ndcformat','FDA National Drug Code Format, current format, HIPAA distinction, final rule effective2033-03-07 and preparation period')
add('ndc-approval',8,8,'orange','FDA Orange Book Background, approved products and therapeutic equivalence evaluations')
add('ndc-approval',9,9,'purple','Purple Book About, licensed biologics and biosimilar/interchangeable reference-product relationships')
add('ndc-approval',10,10,'deaorange,orange','DEA Controlled Substances alphabetical list, CSA schedule columns; FDA Orange Book Background')
add('ndc-approval',11,12,'outsourcing','FDA Outsourcing Facilities, federal registration only; all DEA/state professional/facility provisions not fully acquired')
add('ndc-approval',13,13,'conduct','247 CMR 9.01(21), all elements of FDA-required REMS, including distribution/dispensing restrictions')
add('ndc-approval',14,14,'compounding','FDA Compounding Provisions chart, 503A/503B conditional exemptions from approval and CGMP distinction')
add('ndc-approval',15,15,'ndc','FDA NDC disclaimer on payer coverage limitations; all payer-specific legal obligations remain unverified')
add('recall-classification',1,6,'recall','21 CFR 7.3(m)(1)–(3), Class I/II/III risk definitions')
add('recall-classification',7,7,'enforcement','FDA Enforcement Reports, not-yet-classified recalls and initiation before FDA classification')
add('recall-classification',8,9,'recall','21 CFR 7.3(m) relative health hazard and 7.3(h) depth as recall strategy')
add('recall-classification',10,10,'enforcement','FDA Enforcement Reports, firm-initiated warning/recall before FDA hazard assessment/classification')
add('recall-classification',11,12,'recall','21 CFR 7.3(g), recall removal or correction of marketed violative product')
add('recall-classification',13,15,'recall','21 CFR 7.3(d), correction includes relabeling, repair, modification, adjustment, destruction, inspection without physical removal')
add('recall-classification',16,17,'recall','21 CFR 7.3(j), market withdrawal minor violation/no violation pathways')
add('recall-classification',18,19,'recall','21 CFR 7.3(k), stock recovery, direct control and no portion released for sale/use')
add('w5-a-20',1,3,'gpo351','21 USC 351(a)(1),(a)(2)(A), contamination/insanitary manufacturing or holding')
add('w5-a-20',4,5,'gpo351','21 USC 351(b),(c), compendial/noncompendial strength, quality, purity and plainly-stated-label exception in(b)')
add('w5-a-20',6,8,'gpo352','21 USC 352(a),(b),(c), false/misleading labeling, mandatory information and prominence/readability')
add('w5-a-20',9,13,'gpo351,gpo352','21 USC 351(a)–(c) and352(a)–(c), independently stated quality and labeling criteria, no actual-injury prerequisite')
add('w5-a-20',14,14,'ndc','FDA NDC Product File Definitions, NDC assignment/listing disclaimer')
add('w5-a-20',15,15,'dailymed','NLM About DailyMed, approved and unapproved products, submitted-label scope')
add('w5-a-20',16,17,'ndc,compounding','FDA NDC disclaimer; FDA 503A/503B conditional exemption table, separate approval and compounding requirements')
add('w5-a-20',18,18,'gpo360eee-1','21 USC 360eee-1(d)(1),(3),(4), tracing, authorized partners and verification, separately required')
add('w5-a-20',19,19,'1307.11','21 CFR 1307.11(a)–(c), separate DEA registration, orders and distribution conditions')
add('w5-a-20',20,20,'gpo351,gpo352','USCODE2024 edition metadata on sections351/352; no certification of all2026 amendments/product-specific exceptions')
add('w4-d-1',1,16,'definitions','Policy2025-02, definition of Quality-related Event, patient receives condition, items(1)–(7)(g)')
add('w4-d-1',17,18,'definitions,cqi','Policy2025-02 QRE definition;247CMR15.03(1),(2), QRE notification trigger')
add('w4-d-1',19,19,'defective','Policy2024-04, defective preparations identified prior to dispensing, CQI documentation recommended')
add('w4-d-1',20,20,'definitions,310.305','Policy2025-02 SADE definition;21CFR310.305(b), adverse drug experience definition')
add('w4-d-1',21,21,'defective','Policy2024-04, definition and examples of defective preparation')
add('w4-d-1',22,22,'310.305','21 CFR310.305(b), adverse drug experience, normal and other uses included')
add('w4-d-1',23,24,'39D,reporting,defective','MGLc112§39D(e);247CMR20.02(2);Policy2024-04, separate quality/clinical triggers')
add('w4-d-2',1,5,'cqi','247 CMR15.02(1), written program and detect/document/assess/prevent purposes')
add('w4-d-2',6,6,'cqi','247 CMR15.02(2), designated individual responsible for CQI compliance')
add('w4-d-2',7,9,'cqi','247 CMR15.02(3)(a)–(c), patient impact, causes and prevention response/workflow')
add('w4-d-2',10,10,'cqi','247 CMR15.02(4), ongoing personnel education at least annually')
add('w4-d-2',11,12,'cqi','247 CMR15.03(3)(b), individual/collective analysis, workflow/technology/training/staffing')
add('w4-d-2',13,13,'cqi','247 CMR15.03(4), personnel notification of SOP/system changes')
add('w4-d-2',14,15,'cqi','247 CMR15.03(3)(c),(d), remedial changes and indicators over predetermined period')
add('w4-d-3',1,2,'cqi','247 CMR15.03(1), personnel training and immediate discovery notification to pharmacist/MOR')
add('w4-d-3',3,7,'cqi','247 CMR15.03(2)(a),(b), immediate patient/representative notification, judgment-based prescriber/team notification and patient instructions')
add('w4-d-3',8,11,'cqi','247 CMR15.03(3)(a), pharmacist initial documentation within24hours of discovery/information; subsequent analysis separately stated')
add('w4-d-3',12,18,'cqi','247 CMR15.03(3)(a)1–5, required dates, names/titles, description and contacts')
add('w4-d-3',19,20,'cqi','247 CMR15.04(1), written program on premises and readily available to all personnel')
add('w4-d-3',21,25,'cqi','247 CMR15.04(2), QRE records two years from report date, orderly/date filing, offsite allowed')
add('w4-d-4',1,7,'definitions','Policy2025-02, Serious Injury definition(a)–(d), additional treatment/testing/monitoring at hospital or ED')
add('w4-d-4',8,9,'definitions','Policy2025-02, Serious Disability, major intervention and more-than-seven-days bodily-function limitation')
add('w4-d-4',10,17,'definitions','Policy2025-02, Serious Adverse Drug Event definition and outcomes(a)–(f)')
add('w4-d-4',18,18,'definitions,310.305,503Bguide-pdf','MA Policy2025-02 preventable SADE;21CFR310.305(b),(c);503B Guidance III(A),(B), serious and unexpected')
add('w4-d-4',19,19,'definitions','Policy2025-02, SADE outcome-based definition, reassess when qualifying outcome actually develops')
add('w4-d-5',1,2,'reporting','247 CMR20.02(1), resident MOR report within7business days of discovery of related serious injury/death')
add('w4-d-5',3,5,'39D','MGLc112§39D(b), as soon as possible and no later than7business days of improper-dispensing discovery')
add('w4-d-5',6,6,'39D,reporting','MGLc112§39D(b) versus247CMR20.02(1), distinct discovery language preserved')
add('w4-d-5',7,9,'reporting','247 CMR20.02(5) nonresident exclusion and20.07(3) separate MA-dispensing report within7business days')
add('w4-d-5',10,12,'reporting','247 CMR20.02(4), five years from Board filing and readily retrievable records')
add('w4-d-5',13,14,'reporting,cqi','247 CMR20.02(3) in-addition-to-CQI;15.03(2),(3), patient notification and CQI documentation')
add('w4-d-6',1,8,'reporting,39D','247 CMR20.02(2)(a)–(c), MOR, pharmacy manufactured/produced/compounded product,7business days from any employee knowledge;MGLc112§39D(c)')
add('w4-d-6',9,10,'reporting','247 CMR20.02(2), product-scope condition and no dispensing-error prerequisite')
add('w4-d-6',11,13,'defective,reporting','Policy2024-04, immediately submit Board SADE form for defective preparation caused or suspected of causing SADE;247CMR20.02(2) distinct general clock')
add('w4-d-6',14,14,'503Bguide-pdf,310.305','FDA503B Guidance III(A)–(C), serious-and-unexpected report ASAP/no later than15calendar days from initial receipt, follow-up clock;21CFR310.305(c)(1),(2)')
add('w4-d-7',1,6,'39D','MGLc112§39D(e), knows/reasonably should know, immediate recall, identify/segregate remaining stock and no dispensing/distribution')
add('w4-d-7',7,13,'defective','Policy2024-04, defective preparation definition: potency, quality, composition, dosage form, mislabeling, contamination, sterility, stability')
add('w4-d-7',14,14,'39D','MGLc112§39D(e), may-be-defective trigger, no proved patient-injury prerequisite')
add('w4-d-7',15,24,'39D','MGLc112§39D(e)(i)–(vii), seven recall-log fields with compound/actual potency and dosage form distinguished')
add('w4-d-7',25,26,'39D','MGLc112§39D(e), log available within7days of recall and retained at least10years')
add('w4-d-7',27,28,'reporting,defective','247 CMR20.06(2),(3), defective dispensed CSP/complex CNSP report within7days of identification;Policy2024-04')
add('w4-d-7',29,30,'39D,reporting','MGLc112§39D(e) recall/log versus247CMR20.06(2),(3) dispensed-product defect report, different scope and clocks')
add('w4-d-7',31,33,'defective,39D','Policy2024-04 pre-dispensing section, CQI documentation recommended;MGLc112§39D(e) known defective remaining stock')
add('w4-d-7',34,34,'oos','FDA Guidance Investigating OOS Test Results for Pharmaceutical Production, IV(B)(1), testing into compliance;nonbinding CGMP scope')
assert len(spec)==405
# Exact per-proposition section corrections after a second alignment with claim order.
def setsp(uid,a,b,keys,section):
 for n in range(a,b+1):spec[(uid,n)]=(keys.split(','),section)
setsp('w4-c-15',1,2,'wholesale','247 CMR7.02(1),(4), prebusiness and separate-location licences')
setsp('w4-c-15',3,4,'wholesale','247 CMR7.04(9)(c), separate Board/DPH and United States DEA controlled-substance registrations')
setsp('w4-c-15',5,5,'wholesale,gpo360eee','247 CMR7.02;21USC360eee(2)(B), wholesale licence and DSCSA licence-reporting requirements')
setsp('w4-c-15',6,14,'wholesale','247 CMR7.04(1)–(5), storage/security, incoming/outgoing inspection, quarantine and returned products')
setsp('w4-c-15',15,16,'wholesale','247 CMR7.04(7)(b),(c), recall/withdrawal and crisis procedures')
setsp('w4-c-15',17,18,'wholesale','247 CMR7.03(3), registered-pharmacist direct supervision and federal CGMP for repackaging/relabeling')
setsp('w4-c-15',19,23,'wholesale','247 CMR7.04(6)(a)1–3, source/destination, identity, quantity, receipt/disposition dates')
setsp('w4-c-15',24,25,'wholesale','247 CMR7.04(6)(b),(c), two years after disposition and two-working-day retrieval')
setsp('w4-c-15',26,26,'gpo360eee-1,pharmacists','21USC360eee-1(d)(1)(A)(iii);FDA Pharmacists Store tracing information six years')
setsp('w4-c-15',27,31,'gpo360eee','21USC360eee(19),(24)(A),(B)(i)–(iv), specific patient need, common control, emergency and dispensing exclusions')
setsp('w4-c-15',32,32,'1307.11','21CFR1307.11(a)–(c), separate DEA practitioner distribution requirements and five-percent threshold')
setsp('w4-c-15',33,33,'wholesale','247CMR7.02(1),7.04(9)(c), actual wholesale activity and separate registrations')
setsp('w4-c-20',6,7,'gpo360eee','21USC360eee(19), specific identified patient need, anticipated stock replenishment excluded')
setsp('w4-c-20',8,8,'gpo360eee,gpo360eee-1','21USC360eee(19);360eee-1(d)(1)(A)(ii), limited interdispenser information-transfer exception')
setsp('w4-c-20',10,10,'gpo360eee,conduct','21USC360eee(17),(18), authorized partner returns;247CMR9.01(5),(7), patient returns and quarantine')
setsp('w4-c-20',12,12,'gpo360eee','21USC360eee(13), product definition excludes compounded drugs compliant with353a/353b')
setsp('w4-c-20',16,16,'39D,gpo353b','MGLc112§39D(e), immediate pharmacy compounded-preparation recall/log;21USC353b conditional federal exemption')
setsp('w6-a-2',4,6,'nda','FDA NDA Introduction, safety/effectiveness and manufacturing quality decisions; submission is a proposal')
setsp('w6-a-2',7,10,'anda','FDA ANDA Introduction, generic review/potential approval, comparability and bioequivalence')
setsp('w6-a-2',11,11,'anda,conduct','FDA ANDA product-specific comparability;247CMR9.05(1)–(3), Massachusetts dispensing/substitution and licence-type conditions')
setsp('w6-a-2',16,16,'ind,nda,bla,conduct','FDA IND/NDA/BLA introductions;247CMR9.01(1),(4),9.05, distinct research/product/professional/dispensing questions')
setsp('w6-a-4',1,5,'otc,monograph','FDA Nonprescription Application Process, NDA/ANDA and direct-to-OTC/Rx-switch pathways;OTC monograph overview')
setsp('w6-a-4',6,12,'monograph','FDA OTC Drug Review Process,505G GRASE conditions and proposed/final/interim-final administrative orders')
setsp('w6-a-4',13,13,'otc','FDA Nonprescription Application Process, product-specific direct and Rx-to-OTC applications, labeling and consumer studies')
setsp('w6-a-4',14,15,'otc,conduct','FDA OTC application pathways concern product status;247CMR9.01(1),(4),9.15(2), separate recognized scope and prescription authority')
setsp('w6-a-5',1,2,'offlabel','FDA Understanding Off Label, approved drug unapproved uses and healthcare-provider medical judgment')
setsp('w6-a-5',3,4,'offlabel,conduct','FDA Off Label;247CMR9.01(1),(4),9.15(2), professional scope and controlled-substance/valid-prescription duties')
setsp('w6-a-5',5,5,'conduct','247CMR9.01(21), all FDA-required REMS elements including distribution and dispensing restrictions')
setsp('w6-a-5',6,6,'conduct','247CMR9.01(1),(4),9.15(2)(a)–(d), recognized scope, legitimate purpose, relationship, authenticity,94C19(a)')
setsp('w6-a-5',7,15,'fdaterms,eua','FDA Understanding FDA Terms, EUA conditions/evidence/revocation;Emergency Use Authorization framework and current product Fact Sheets')
setsp('w6-a-5',21,21,'fdaterms','FDA Understanding FDA Terms, Off-Label Use section, providers generally prescribe or administer using medical judgment')
setsp('w6-a-6',14,19,'homeopathic','FDA Homeopathic Products, no approved homeopathic products;approval/adulteration/misbranding and risk-based enforcement')
setsp('w6-a-6',20,23,'510k,nda','FDA510(k) Clearances substantial-equivalence premarket notification;NDA drug application, product versus professional licence')
versions={'exemption2024':'FDA letter issued2024-07-12, revised clarifying June12letter; exemption through2026-11-27, assessment2024-11-27.','exemption2026':'FDA letter issued/signed2026-08-06; period2026-11-27–2027-11-27, corporate employee assessment2026-11-27.','definitions':'Board Policy2025-02 adopted2025-08-07; official posted PDF.','defective':'Board Policy2024-04 adopted2024-09-05; official posted PDF.','reporting':'Mass.Register1536,2024-12-06 official PDF; individual clause initial effective dates not separately established.','conduct':'Mass.Register1536,2024-12-06 official PDF; individual clause initial effective dates not separately established.','cqi':'Mass.Register1536,2024-12-06 official PDF; individual clause initial effective dates not separately established.','wholesale':'Official247CMR7 posted PDF; individual amendment/effective dates not separately established.','503Bguide-pdf':'FDA guidance October2015; official guidance page current2020-04-21. Guidance recommendations and binding statutory requirement distinguished.','oos':'FDA nonbinding guidance revisedMay2022 (originalOctober2006); CGMP production/investigation scope, not direct blanket503A CGMP certification.','39D':'Current official Massachusetts General Laws c112§39D page reviewed2026-11-04; individual effective/amendment dates not separately established.'}
for k in ['recall','310.305','1307.11']:versions[k]='eCFR current displayed2026-11-02; retrieved/reviewed2026-11-04. Clause-specific first effective date not separately established.'
for k in ['gpo351','gpo352','gpo353b','gpo360eee','gpo360eee-1']:versions[k]='Official govinfo United States Code2024 edition.2026current-link also resolves to2024 edition; not a representation that all2026 amendments/product-specific exceptions have been exhaustively consolidated. Current FDA2026letter/pages separately cross-check relevant DSCSA duties.'
metas={p.name[:-10]:json.loads(p.read_bytes()) for p in (B/'sources').glob('*.meta.json')}
used={k for keys,section in spec.values() for k in keys}
content=[]
for k,m in metas.items():
 row={'source_key':k,'metadata_path':str(B/'sources'/(k+'.meta.json')),'metadata_sha256':sha((B/'sources'/(k+'.meta.json')).read_bytes()),'original_attempted_at':m.get('attempted_at'),'original_retrieved_at':m.get('retrieved_at'),'http_status':m.get('status'),'used_as_claim_authority':k in used}
 if 'raw_path' in m:
  assert sha(Path(m['raw_path']).read_bytes())==m['raw_sha256'] and sha(Path(m['text_path']).read_bytes())==m['text_sha256'];t=Path(m['text_path']).read_text();assert t.strip();lines=[x.strip() for x in t.splitlines() if x.strip()];dates=[lines[i+1] for i,x in enumerate(lines[:-1]) if 'Content current as of' in x]
  row.update(raw_path=m['raw_path'],raw_sha256=m['raw_sha256'],text_path=m['text_path'],text_sha256=m['text_sha256'],content_review='OFFICIAL_EXPECTED_CONTENT_CONFIRMED' if k in used else 'RETAINED_DISCOVERY_ALTERNATIVE_NOT_CLAIM_AUTHORITY',displayed_content_current_as_of=dates,scope='Only exact sections cited in report read and relied upon; acquisition200 is not substantive approval.')
  if dates:versions.setdefault(k,'FDA page Content current as of '+','.join(dates)+'; current official posted explanation reviewed2026-11-04. Individual statutory effective dates not established by page date.')
 else:row.update(content_review='FAILED_RETRIEVAL_NOT_AUTHORITY',failure=m.get('error',m.get('retrieval_status')))
 content.append(row)
(B/'source-content-validation.json').write_text(json.dumps({'reviewed_at':'2026-11-04','metadata_immutable':'Original GET metadata preserved without rewriting PENDING status. This separate content assessment records manual validation; no response200 alone used as proof.','cache':'This job source acquisitions are actual HTTPS GETs at original timestamps. Any other reviewer reusing these bytes must mark SAME_DAY_RETAINED_CACHE, not fresh GET.','official_failures':'House prelim endpoints and two MA247CMR21 paths and old503B report path failed; failures remain preserved. No soft200 error document used as authority.','sources':content},ensure_ascii=False,indent=2)+'\n')
def authority(k,section):
 m=metas[k];assert 'raw_path' in m
 return {'source_type':'PUBLIC_OFFICIAL','official_url':m['official_url'],'exact_section':section,'law_checked_date':'2026-11-04','version_or_effective_date_status':versions.get(k,'Current official published content reviewed2026-11-04; separate legal effective date not established.')+' Actual HTTPSGET timestamp '+m['retrieved_at']+'. Original metadata status plus separate source-content-validation.json content check.','evidence_path':m['raw_path'],'evidence_sha256':m['raw_sha256'],'text_path':m['text_path'],'text_sha256':m['text_sha256'],'retrieval_metadata_path':str(B/'sources'/(k+'.meta.json')),'retrieval_metadata_sha256':sha((B/'sources'/(k+'.meta.json')).read_bytes())}
blocked={('w4-c-20',15),('ndc-approval',11),('ndc-approval',12),('ndc-approval',15),('w5-a-20',20),('w4-d-7',34)}
blockers={('w4-c-20',15):'현행 MA outsourcing facility 면허247CMR21의 정확 원문 확보 실패. 연방DSCSA면제를 주면허면제로 읽지 않지만 해당 주법 명제 전면 판정은 보류.',('ndc-approval',11):'FDA establishment/DEA registration의 전체 현행 적용대상·면제 조문 직접 대조 미완료.',('ndc-approval',12):'MA facility별 licence와 individual professional licence의 전체 적용·예외 원문 미확보.',('ndc-approval',15):'모든 payer의 claim 승인과 처방·조제 적법성의 관계를 다룬 현재 1차 규정 전량 미검증.',('w5-a-20',20):'351/352 확보 판본2024 edition;2026 전체 개정·제품별 예외의 완전 검증을 뜻하지 않는다고 명시. 전체현행성 인증 불가.',('w4-d-7',34):'FDA OOS guidance는 nonbinding CGMP범위. 모든503A약국 predispensing defect에 동일 규칙을 직접 적용하는 일반 법적 범위 미확정.'}
omissions={'recall-classification':[
'본문 “Class III라고 무시하거나 ... 방치하지 않습니다”의 ClassIII라는 이유만으로 회수 대응을 생략하지 않는 별도 행동 명제가 census006의 risk definition에 열거되지 않았다. 위험이 낮다는 정의와 대응 생략 금지는 다른 명제이다.',
'본문은 FDA class 결정 전 업체 회수 통지를 방치하지 않는다고 한다. census007의 not-yet-classified 상태 정의와010의 두 날짜 차이는 분류 전 실제 회수 통지에 대응해야 한다는 행위 명제를 직접 열거하지 않는다. FDA Enforcement Reports의 firm initiation-before-classification을 확인했다.',
'본문은 class와 affected lot·진행 상태·실제 환자 harm이 서로 다른 정보라고 한다. census008은 risk degree,009는 recall depth만 열거하므로 affected lot·진행상태·실제 harm 유무와의 세 별도 구분이 빠져 있다.',
'본문 후반 workflow의 product·strength·form·lot·expiry 대조, stock 격리 및 전산 차단 행위가 정의 중심19claim에 없다. 이는 본문이 명시한 학습용 workflow이며 모든 recall의 독립적 동일 법정의무로 자동 확대하지 않고, 실제 recall instruction/적용법에 따른 범위를 따로 열거·판정해야 한다.',
'동 workflow에서 이미 교부된 환자·시설·배송분 추적, 회수지시에 따른 연락·반환 및 대체치료 지원, 수량 reconciliation·기록, 해당 Board/FDA/DSCSA 병행 trigger 검토가 전량 미열거이다. 각각의 행위·조건을 구분해야 한다. 마지막의 모든recall에 동일환자연락deadline을 신설하지 않는다는 범위 제한도 census에 없다.'
]}
methods={
'w4-c-16':'8개기본공급망 명제와2024/2026letter 날짜·기간·corporate entity·직종·25경계·IRS시간·assessment각주·bullet별역할·noapplication/noadditionalinfo를28명제와 양방향 대조했다.',
'w4-c-17':'면제후잔존의무, TI/TS6년과THsunset, 기존기록보존, 역할·단계·readiness권고를15명제와 대조했다.',
'w4-c-18':'authorized partner의4역할별등록/면허·reporting, NDCserial/lot/expiry, 광고/invoice부정예시, thirdparty책임을16명제와 대조했다.',
'w4-c-19':'suspect/illegitimate의 각정의경로·risk조건·격리/조사/identifier·판정후24h·reportplatform·termination·6년을23명제와 대조했다. 본문intentionaladulteration축약은claim004의seriousharm조건과 별도 아래법규보류로 처리했다.',
'w4-c-20':'recall/illegitimate/suspect구분, patientneed/stock·returns,503A/B제품제외·CGMP·주면허/recall독립성을16명제와 대조했다.',
'w4-c-15':'사업면허/등록층,온습도·보안·격리·in/out검사·returns,recall/crisis,repack/label감독CGMP,일반records2년·2workingdays와DSCSA6년,4transfer예외·DEA를33명제와대조했다.',
'w6-a-2':'IND/NDA/ANDA/BLA각정의·신청과승인·genericBE와제품별범위·MA대체·biosimilar/interchangeable구분을16명제와대조했다.',
'w6-a-4':'application/monograph두경로·direct/switch·GRASE조건·505Gorder세상태·제품별전환·OTC권한/보험층을15명제와대조했다.',
'w6-a-5':'offlabel정의와직종scope/CS/REMS잔존, EUA조건·evidence·FactSheet·기간/철회, expandedaccess환자/대안/시험밖/한계를21명제와대조했다.',
'w6-a-6':'supplement안전/label책임·enforcement·NDI, cosmeticintendeduse/color, homeopathic무승인/HPUS/진열/일반요건,510knotification/SE/다른권한을23명제와대조했다.',
'ndc-approval':'NDC와DailyMed의승인/판매한계,10/11/12digit및2026발표/2033효력,두OrangeBook/PurpleBook,등록/면허/REMS/compound/보험분리를15명제와대조했다.',
'recall-classification':'표4행의모든정의분기와class/depth/lot/status/harm구분,ClassIII/미분류부정행동,recall/correction/withdrawal/stockrecovery조건,후반workflow와법정deadline비확장한계를19명제와 대조했다. 정의와행동/조건제한이같은명제가아님을확인했다.',
'w5-a-20':'오염/insanitary/strength품질,misbranding3경로와동시성/피해불필요,번호/repository와승인/예외/tracing/CS분리,2024판본한계를20명제와대조했다.',
'w4-d-1':'QRE환자도달과wrongtype각항목·임상관리실패각항목,nearmiss통지/기록,adverseevent와productdefect·독립trigger를24명제와대조했다.',
'w4-d-2':'writtenCQI·4목적·책임·3절차·annualeducation·시스템원인·4요인·변경통지·indicator/효과를15명제와대조했다.',
'w4-d-3':'personnel→pharmacist와patient/team두즉시시계,judgment조건,24htrigger와initial/후속분리,5기록필드세분,program현장/접근·records2년/date/orderly/offsite를25명제와대조했다.',
'w4-d-4':'seriousinjury4경로·ED3additional행위,disabilitymajor/>7경계,MApreventableSADE각결과·DPH추가·federalunexpected차이·후속outcome을19명제와대조했다.',
'w4-d-5':'residentMOR/trigger·statute와regulation발견차이/asap·7business,nonresident별도20.07,5년filing·retrievable·patient/CQI병행을14명제와대조했다.',
'w4-d-6':'약국manufactured/produced/compounded, MOR와3수신처,anyemployee7business,commercial/정확조제경계,defectSADEcaused/suspected즉시,503B15calendar를14명제와대조했다.',
'w4-d-7':'known/reasonablyshouldknow즉시recall과잔량3조치,결함7예,log7필드와compound/actual구별·7일/10년,CSP/complexCNSPidentification7일,noncomplex/predispensing/권고/재시험범위를34명제와대조했다.'}
records=[]
for u in packet['units']:
 uid=u['unit']['id'];bind=job['unit_bindings'][uid];claims=[]
 for n,c in enumerate(u['claims'],1):
  keys,section=spec[(uid,n)];status='SOURCE_BLOCKED' if (uid,n) in blocked else 'KEEP';finding=F[uid][n-1]
  if (uid,n)==('w4-c-19',4):
   status='LEGAL_HOLD';finding+=' 현재census명제는위험조건을포함하지만 실제본문은intentionally adulterated를독립목록으로축약하고seriousharm한계를그경로에명시하지않는다. 본문은모든intentionaladulteration을같은suspect법정정의로확대해읽힐수있어법적범위명료화전보류한다.'
  e={'claim_id':c['claim_id'],'claim_record_sha256':bind['claim_record_sha256s'][c['claim_id']],'claim_read_completely':True,'statement_reviewed_ko':c['statement_ko'],'legal_status':status,'finding':finding,'authorities':[authority(k,section) for k in keys]}
  if status!='KEEP':e['blocker']='본문intentionaladulteration경로에21USC360eee(21)(B)의seriousadversehealthconsequences/death위험조건을명료하게적용하는adjudication필요. 올바른census조건으로본문축약문을자동면책하지않음.' if status=='LEGAL_HOLD' else blockers[(uid,n)]
  claims.append(e)
 om=omissions.get(uid,[]);status='LEGAL_HOLD' if om or any(c['legal_status']=='LEGAL_HOLD' for c in claims) else 'SOURCE_BLOCKED' if any(c['legal_status']=='SOURCE_BLOCKED' for c in claims) else 'KEEP'
 row={'unit_id':uid,'binding':bind,'body_read_completely':True,'completeness':'OMISSIONS_FOUND' if om else 'COMPLETE','completeness_method':methods[uid]+' 현재본문모든문단·표각행·수치/시점/행위주체/조건/예외/부정문을읽고모든census명제와양방향확인했다. 관련65Q의stem/모든보기/key/전체한국어해설과21derived가시전문을읽었으며그추가가정으로본문누락을메우지않았다.','omissions':om,'legal_status':status,'claims':claims,'related_question_ids_read':sorted({qid for c in u['claims'] for qid in c.get('related_question_ids',[])}),'independent_unit_finding':methods[uid]}
 if bind['author_nonlegal_classification'] is not None:row['nonlegal_classification_review']={'confirmed':True,'finding':'본문법적명제는전체census와별도감사했고비법적설명범위를독립확인했다.'}
 records.append(row)
prov={k:job[k] for k in ['stage','actor_provenance','auditor','auditor_instance']};prov.update(independent_of_authors=True,canonical_audit=False,canonical_release_credit=0,question_audit_credit=0)
counts={'units':dict(collections.Counter(r['legal_status'] for r in records)),'completeness':dict(collections.Counter(r['completeness'] for r in records)),'claims':dict(collections.Counter(c['legal_status'] for r in records for c in r['claims']))}
report={**prov,'checked_at':'2026-11-04','records':records,'input_provenance':{'source_head':packet['source_head'],'original_inputs_preserved':True,'body_and_census_hash_checks':'input-validation.json','root_strict_inventory_projection_is_not_legal_pass':True,'loader_guard_bypass':False},'related_surface_review':{'question_count':65,'all_stems_choices_keys_full_explanations_read':True,'derived_count':21,'all_derived_visible_text_read':True,'finding':'모든선택지와해설의추가가정·wronghandling·개념경계를읽었다. Workqueue모델의변형문항수를별도법규수나새감사자인원으로세지않는다. Related연결이모든claim의각수치/예외를직접출제한다는뜻은아니며Q/derived문구는본문/공식조항을대체하지않는다. Class미분류대응·CQI세시계·서로다른trigger구별의교육내용은실제공식조항과대조했지만questionauditcredit는0이다.','source_context_raw_sha256':sha((B/'related-context.json').read_bytes())},'source_content_validation':'source-content-validation.json','review_counts':counts,'limitations':['2024govinfo법전자료를2026완전통합판으로표시하지않았다. 관련현행FDA설명/2026면제letter를별도대조했지만351/352전체2026개정/제품별예외전량인증은SOURCE_BLOCKED다.','cosmetic공식페이지의오래된VCRP/mandatoryrecall부분은현재MoCRA전체인증에사용하지않았다. 본감사는intendeduse및premarket/coloradditive의한정명제만판정한다.','OOSguidance는비구속CGMP범위이며모든503Apre-dispensing조치의법정근거로자동확대하지않았다.','저자checked/sourceblocked상태는법적증거로복제하지않고원문을직접대조했다. 새공식회수로확인한명제와확인하지못한명제를개별분리했다. 기존독립HOLD해제권한이나새releasecredit가없다.','본문/census/sharedqueue/ledger/generated/loader/이전report는수정하지않았다. 모든신규경로는ownprefix안이다.']}
(B/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');(B/'review-counts.json').write_text(json.dumps(counts,ensure_ascii=False,indent=2)+'\n')
result={**prov,'worker_commit':'0'*40,'unit_hashes':{uid:b['body_sha256'] for uid,b in job['unit_bindings'].items()},'evidence':{'path':str(B/'report.json'),'raw_sha256':sha((B/'report.json').read_bytes())},'result_path':q.OUTPUT+job['job_id']+'-result.json','results':[{k:r[k] for k in ['unit_id','completeness','legal_status']} for r in records]};q.validate_result(job,result);q.validate_evidence(job,result,report);Path('/tmp/final86-b-precommit-envelope.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(counts,ensure_ascii=False));print('native validate_result/evidence PASS')
