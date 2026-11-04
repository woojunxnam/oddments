"""Assemble this session's manually judged option findings; no question writes."""
from pathlib import Path
import json,hashlib,datetime,copy
ROOT=Path(__file__).resolve().parents[3];BASE=Path('reports/full-corpus-review/recovered-phase11-d-evidence')
def read(p):return json.loads((ROOT/p).read_bytes())
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def stamp():return datetime.datetime.now(datetime.timezone.utc).isoformat()
packet=read(BASE/'assigned-visible-input.json');job=read(BASE/'assignment.json');findings=read(BASE/'option-findings.json');dupes=read(BASE/'duplicate-measurement.json');loc=read(Path('reports/full-corpus-review/phase11-d-evidence/source-locators.json'))
byloc={r['question_id']:r for r in loc['records']};dupby={r['question_id']:r for r in dupes['records']};today='2026-11-04'
# Explicit source scopes actually read in this session, with publication/effectivity limitations.
specs={
'vaccine-policy':('Board/DCP/Immunization Program Policy 2023-02: Vaccine Administration','III.C.2(c),(g); IV.D–G; V.A; VI.A–C; VII.A–B; VIII.A–B; IX Appendix','Adopted 2023-05-04; revised 2023-09-07 and 2025-09-04, as printed. Separate commencement date not stated; current stable official URL retrieved 2026-11-04. No later supersession independently established outside the returned official document.'),
'miis-regulation':('105 CMR 222 Massachusetts Immunization Information System','222.003; 222.100(A),(C); 222.105(A),(B)(1)–(4); 222.200(C); 222.205(A)(1),(B)','Official PDF footer Mass. Register #1528, 2024-08-16. This is the posted regulatory version; separate commencement not stated in retrieved text.'),
'board-reporting':('247 CMR 20 Reporting','20.02(1)–(5)','Official PDF footer Mass. Register #1536, 2024-12-06. Conditional Board trigger only; no blanket vaccine adverse-event Board-reporting obligation inferred.'),
'medication-circular':('DCP Circular Letter 26-03-124 Pharmacist Administration of Medications','Purpose; Dispensing by Administration(a)–(f); Prescriber Assessment; Training; CPR Certification; Continued Competency; Pre-administration Patient Counseling; Administration and Dosing; Record Keeping; Pharmacist-Prescriber Communication','Dated 2026-03-11; expressly replaces DCP23-04-118 of 2023-04-21. Separate commencement not stated in retrieved circular.'),
'cdc-vis-current':('CDC Facts About VISs','VISs are required by law; Ways to give a VIS; Other provider responsibilities','CDC page dated 2024-08-02; retrieved current URL 2026-11-04. Official CDC explanation of NCVIA 42 USC300aa-26; direct US Code request failed404 and is not claimed as statutory-text retrieval.'),
'vaers-faq':('CDC/FDA Vaccine Adverse Event Reporting System FAQ','Who can report to VAERS?; What are healthcare providers required to report?; What are the strengths and limitations of VAERS?','Official FAQ retrieved 2026-11-04. No page-wide effective date asserted. Uses table/contraindication reporting in vaccine policy rather than extrapolating a universal COVID-era EUA rule.'),
'cdc-storage':('CDC Vaccine Storage and Handling Toolkit','Section One Vaccine Cold Chain (appearance); Section Three Temperature Excursions (printed p15)','PDF March2024, updated2024-03-29 as printed; retrieved current stable official URL2026-11-04. General appearance/excursion guidance only, no product-specific viability conclusion.'),
'ma-drugstore':('247 CMR 6 Licensure of Pharmacies','6.02(1),(2)','Official posted PDF retrieved2026-11-04. Separate effective date not established in this review; facility-license condition read from current official text.'),
'nabp-format':('NABP Take the MPJE Exam public format page','About the MPJE / 2.5-hour, 120-question selected-response format','Public format only, not legal authority. Current URL retrieved2026-11-04; no protected Pre-MPJE or recalled questions viewed.')}
sources={}
for name,(authority,section,version) in specs.items():
 meta=read(BASE/'official'/f'{name}.meta.json');tp=BASE/'official'/f'{name}.txt';rp=BASE/'official'/f'{name}.raw';mp=BASE/'official'/f'{name}.meta.json'
 assert meta['http_status']==200
 sources[name]=dict(authority=authority,source_type='OFFICIAL_REGULATION' if name in {'miis-regulation','board-reporting','ma-drugstore'} else 'OFFICIAL_AGENCY_GUIDANCE',official_url=meta['official_url'],exact_section=section,law_checked_date=today,effective_date_or_version=version,effective_date=None,effectivity_limitations=version,http_status=200,legal_authority_used=name!='nabp-format',retrieval_mode='LIVE_OFFICIAL_HTTPS',retrieved_at=meta['retrieved_at'],read_at=stamp(),tls_verified=True,evidence_path=str(tp),evidence_sha256=sha(tp),raw_path=str(rp),raw_sha256=sha(rp),retrieval_metadata_path=str(mp),retrieval_metadata_sha256=sha(mp))
for name in ['cdc-vis','usc-vis','usc-adverse']:
 mp=BASE/'official'/f'{name}.meta.json';meta=read(mp);tp=BASE/'official'/f'{name}.txt';rp=BASE/'official'/f'{name}.raw'
 sources[name]=dict(authority='FAILED_OFFICIAL_RETRIEVAL_NOT_LEGAL_EVIDENCE',official_url=meta['official_url'],exact_section='Requested URL returned404; no law finding based on body',law_checked_date=today,http_status=meta['http_status'],legal_authority_used=False,effective_date=None,effectivity_limitations='No effective legal content retrieved.',retrieval_mode='LIVE_OFFICIAL_HTTPS',retrieved_at=meta['retrieved_at'],read_at=stamp(),tls_verified=True,evidence_path=str(tp),evidence_sha256=sha(tp),raw_path=str(rp),raw_sha256=sha(rp),retrieval_metadata_path=str(mp),retrieval_metadata_sha256=sha(mp))
groups={
'vis':['vaccine-policy','miis-regulation','cdc-vis-current'],
'vaccine-screen':['vaccine-policy'],
'miis-query':['vaccine-policy','miis-regulation'],
'miis-clock':['miis-regulation'],
'miis-privacy':['miis-regulation'],
'pediatric':['vaccine-policy','miis-regulation'],
'vaers':['vaccine-policy','miis-regulation','vaers-faq','board-reporting'],
'storage':['vaccine-policy','cdc-storage','ma-drugstore'],
'med-scope':['medication-circular','ma-drugstore','vaccine-policy'],
'med-training':['medication-circular'],
'med-rx':['medication-circular']}
# Item-specific editorial defects identified after reading all visible variants and nearest candidates.
flaws={
321:('authentic_distractors','wording_not_guessable','natural_rule_combination','CaseA는VIS시점이라는한판단인데CaseB와모든환자동일문진표라는정책외주장을끼워넣는다. B necessarily/every와D one identical의과장은실제 VIS대체오류보다쉽게배제된다.'),
322:('authentic_distractors','wording_not_guessable','natural_rule_combination','age만확인한CaseB의screening누락은실무적이지만A동일문진표·D모든공식자료대체라는과장오답과독립VIS사례가불필요하게함께있다.'),
323:('authentic_distractors','wording_not_guessable','CaseB환자screening과VIS사전제공을함께판단하나B사후=사전,C연령만으로면제,Dgeneric필연대체는모두명백한확대형오답으로임상/법적근접오답의긴장이약하다.'),
324:('wording_not_guessable','natural_rule_combination','INCORRECT C의모든백신·환자에동일문진표라는보편문구가오류를드러낸다. A/B/D의사전자료·screening의무는CaseA/B에걸쳐반복되나단일판단으로연결되지않는다.'),
325:('authentic_distractors','wording_not_guessable','A기록열기만으로오늘투여자동기록은질문행위와데이터전송을혼동한과장이다. C는별도COVID권고를끌어와CaseA의단골예외부정을피상적으로고르게한다.'),
326:('authentic_distractors','wording_not_guessable','조회예외와보고의구별은중요하나C자동기록/D과거한번접종유무만이라는과장과B단골면제가근접한법적대안보다는쉽게탈락한다. 현재default MA-REV0060과같은influenza판단을두사례틀로늘렸다.'),
327:('authentic_distractors','wording_not_guessable','SATA에서B onlyever와C familiarpatient예외는공식조회요건과의정교한근접오류보다막연한부정이다. A/D는둘다조회와보고구별을반복한다.'),
328:('wording_not_guessable','natural_rule_combination','INCORRECT B는opening만으로automatically문서화한다는기술적과장이다. COVIDformulation권고와routine조회예외는같은case의경합조건으로엮이지않는다.'),
332:('authentic_distractors','wording_not_guessable','INCORRECT A의newborn특례를everyreport/nextvisit으로확대하는과장이오류를드러낸다. B/C/D는각각보고필드·72시간·24시간의정확한설명이다.'),
333:('authentic_distractors','wording_not_guessable','보고와공유구별은법적주제이나C necessarilyerases와D withoutcarepurpose는직접적인과장·무권한열람이다. B만정상행동으로보여실질적조건경합이약하다.'),
334:('authentic_distractors','wording_not_guessable','Curiosityaccess라는명시된부당목적은C의정답을상식적으로드러내며A기록삭제·D종이만보관은근접법적대안보다극단적이다.'),
335:('authentic_distractors','distinct_from_bank','A/B/C/D모두옳은총괄설명으로경합하는scope·trigger보기없이긍정문네개를재확인한다. 인접333/334/336과동일casepair와같은문장이재노출되므로이세트의독립새사례가치는낮다. allcorrect형식자체를법규오류라고하지않는다.'),
336:('wording_not_guessable','authentic_distractors','INCORRECT D의restrictedsharing necessarily erasesDepartment는규정의접근제한을기록삭제로바꾸는과장이다. 나머지는보고·GUI·carepurpose의의무문장으로동일family내용을재노출한다.'),
337:('authentic_distractors','wording_not_guessable','비용고지와freevaccine대안은현실적이나D everypossiblefeezero·C백신이ongoingcare대체라는극단적오답때문에정답A가언어상도드라진다.'),
338:('authentic_distractors','wording_not_guessable','CaseB상담여부는법적조건검토가필요하나D everypossiblefeezero와C allcostinformation사후연기는거친오답이다. prior-exposure로whole-key신규판정은하지않는다.'),
339:('authentic_distractors','wording_not_guessable','SATA는A allcost사후연기,C everypossiblefeezero,DPCPnotification대체라는과장오답을통해B상담문장만남긴다. prior-exposure로whole-key신규판정은하지않는다.'),
341:('authentic_distractors','wording_not_guessable','Reportableevent/time과인과입증구별은의미있으나C VAERS가immediatecare까지제거한다는환자안전상극단적오답이현실적법적혼동을희석한다. defaultREV0062가동일MIIS/VAERS주제를다룬다.'),
342:('authentic_distractors','wording_not_guessable','MIIS와VAERS는실무에서구분해야하나D immediatecare면제와C제조사contraindication전면제외는근접해석보다과장오답이다. 동일casepair의341정답내용이보기B에반전되어재노출된다.'),
343:('authentic_distractors','wording_not_guessable','SATA B의VAERS가immediatecare와Boardreport모두제거한다는문구가매우쉽다. A/C는reportableevents조건을잘반영하지만현실성10기준전부PASS는아니다.'),
344:('authentic_distractors','wording_not_guessable','INCORRECT B의즉시환자보호까지소멸주장은정교한trigger혼동과다르다. A/C/D는동일family에서이미옳다고제시된문장들이다.'),
345:('authentic_distractors','wording_not_guessable','2시간predraw와1시간MA기준은관련있지만D교육증이시설권한을대체,A외관만으로excursion면제는과장오답이다. 정확한MA/USP기준차이를보기에서경합시키지않았다.'),
346:('authentic_distractors','natural_rule_combination','CaseB의외관만으로품질판정은현실적오류이나보기A/B/C는모두CaseA준비·면허주제라CaseB의온도/시간/제조사지침에관한근접대안을제시하지않는다.'),
348:('wording_not_guessable','authentic_distractors','INCORRECT A trainingcertificate replacesanyauthorization의무제한대체가쉽게오류로보인다. 다른보기의1시간기준·외관한계는이미반복된내용이다.'),
349:('authentic_distractors','wording_not_guessable','tech백신자격과LAI권한구별은중요하나A17세IV,D모든시설등록소멸,Csingle-dose조건제거는한꺼번에범위를너무넓힌오답이라중간경계판단이약하다.'),
350:('authentic_distractors','wording_not_guessable','17세와IV두부적격조건을동시에주어선택C가쉽고나머지는technician자동권한·포장조건제거·시설등록소멸이다. 하나의근접적격사례에서age/route를선별할긴장이없다.'),
351:('authentic_distractors','distinct_from_bank','A/B/C/D모두옳고동일CaseA/B를349/350/352에서반복한다. 권한·MCSR·age/route·포장조건을모두긍정문으로나열하여실제경계오답을판별하지않는다. 법규상키가allcorrect라는사실과현실성결함을분리한다.'),
352:('authentic_distractors','wording_not_guessable','INCORRECT D의개인예외가시설등록모두를없앤다는확대가오류를드러낸다. 나머지A/B/C는같은두사례의명시된기본조건들이다.'),
353:('authentic_distractors','wording_not_guessable','약물·환자군별교육은필요하나B교육이REMSoverride,C역량이CPR삭제,D내부숫자가법이라는과장이정답A를쉽게한다.'),
354:('reasoning_not_trivia','wording_not_guessable','CaseB는회람에없다고stem이직접준숫자를법이라고하면안된다는일반논리다. 특정근거간주CE숫자·기산점경합없이B를고를수있다.'),
355:('authentic_distractors','wording_not_guessable','SATA A아무annual숫자법표시,BREMSoverride,Dvaccinecourse모든LAI역량확정은극단적이고C currentCPR만정상적인의무문장이다.'),
356:('authentic_distractors','wording_not_guessable','INCORRECT C교육이manufacturer/REMS조건을override한다는표현이직접오류를노출한다. 다른보기는교육/CPR/임의CE숫자경계를상식적으로재확인한다.'),
357:('authentic_distractors','wording_not_guessable','권고notation과validRx요건은의미있으나Auncertainty무시,Cconsent가상담대체,Bquarterly가전제품90일새Rx라는극단적오답이정답D를쉽게한다.'),
360:('authentic_distractors','wording_not_guessable','INCORRECT Bconsentsignature replacescounseling은별개의행위를합친단순오류이고나머지A/C/D는동일family의권고·필수구분을긍정문으로반복한다.')}
passes={329,330,331,340,347,358,359}
group_practice={321:'VIS사전제공·patient-specificscreening',325:'noninfluenza/COVID MIIS조회와별도투여보고',329:'투여후72시간과objectionreceipt후24시간의두시계',333:'Department보고·inter-site공유·허용목적접근',337:'freepediatricstock미이용비용고지와childhoodprimarycare상담',341:'MIISdose기록·VAERSreportableevent·조건부Board보고',345:'2시간predraw의MA1시간기준·시설자격·temperatureexcursion',349:'백신technician과pharmacist/intern일반투여주체·18세·SC/IM',353:'약물·환자군교육·CPR·continuedcompetency·REMS',357:'권고notation·prescriberreassessment예시·validrefills·사전상담'}
criteria=['jurisprudence_reasoning','practice_plausibility','authentic_distractors','wording_not_guessable','reasoning_not_trivia','natural_rule_combination','appropriate_drug_context','distinct_from_bank','not_schedule_flashcard','public_style_without_copying']
records=[]
for row in packet['records']:
 q=row['original_visible_content'];qid=q['question_id'];n=int(qid[-4:]);start=321+4*((n-321)//4);topic=group_practice[start];opts=[];used=[];calculated=[]
 for c in q['choices']:
  supported,finding,group=findings[c['text']]; auths=[copy.deepcopy(sources[k]) for k in groups[group]]; used+=groups[group]
  selected=(not supported if 'INCORRECT' in q['stem'] else supported)
  if selected:calculated.append(c['id'])
  opts.append(dict(choice_id=c['id'],option_text=c['text'],option_text_sha256=hashlib.sha256(c['text'].encode()).hexdigest(),statement_supported=supported,selected_under_polarity=selected,finding_ko=finding,authorities=auths))
 assert calculated==q['correct_choice_ids'],(qid,calculated,q['correct_choice_ids'])
 exposed=n in {338,339};cr={k:True for k in criteria};reason=flaws.get(n,(f'{topic}을구체적행위·기산점·권고와필수범위에적용한다.'))[-1]
 if n in flaws:
  for k in flaws[n][:-1]:cr[k]=False
 assert (n in passes)==all(cr.values()),qid
 nearest=dupby[qid]['nearest'];same=[x['question_id'] for x in packet['records'] if x['question_id']!=qid and x['original_visible_content']['stem'].split('\n\nWhich')[0]==q['stem'].split('\n\nWhich')[0]]
 # The concrete duplicate examples actually read were the two nearest canonical/default examples for each four-item group, plus every sibling visible original.
 comparison=dupby[f'MA-EXP-{start:04d}']['nearest'];read_near=[x['question']['question_id'] for x in comparison if x['pool'] in {'canonical','default'}]
 cf={
 'jurisprudence_reasoning':f'{qid}는{topic}에서선택지행위가허용/필수인지구분한다. INCORRECT반전과SATA전체조합은선택지별지원판정으로다시계산했다.',
 'practice_plausibility':f'{qid}의약국업무상황({topic})은실제프로세스에서발생가능하다. CaseA/B사실을임의로추가하지않았다.',
 'authentic_distractors':f'{qid}의보기전체를공식근거와대조했다. '+(reason if not cr['authentic_distractors'] else f'{topic}의실제혼동(의무범위/기산점/권고와필수)을경쟁대안으로시험한다.'),
 'wording_not_guessable':f'{qid}: '+(reason if not cr['wording_not_guessable'] else '정답은단순긍정어/부정어만으로확정되지않으며해당규칙·사실의범위를구분해야한다.'),
 'reasoning_not_trivia':f'{qid}: '+(reason if not cr['reasoning_not_trivia'] else f'{topic}의scope또는trigger를사례의행위에적용한다. 단독숫자암기/Schedule분류만으로끝나지않는다.'),
 'natural_rule_combination':f'{qid}: '+(reason if not cr['natural_rule_combination'] else f'{topic}이라는공통업무맥락에서조건들이연결된다. 여러규칙이필요하지않은단일판단에는인위적연결을강제하지않았다.'),
 'appropriate_drug_context':f'{qid}는특정성분에따라결론이달라지지않는workflow/scope문항이다. 제품명이없는일반백신/eligibleLAI표현을임의의제품조건으로확대하지않았다.',
 'distinct_from_bank':f'{qid}: canonical439·공개2349·default202에서lexical후보를측정했고,{read_near}및동일casepair형제{same}의실제보이는문장을읽었다. '+(reason if not cr['distinct_from_bank'] else '공통주제만으로semanticduplicate판정을하지않았다. 원형제casepair재사용은알려진연습변형맥락으로따로기록한다.'),
 'not_schedule_flashcard':f'{qid}는{topic}에관한행위판단이며단순Schedule암기문항이아니다.',
 'public_style_without_copying':f'{qid}는공개NABPformat및currentstyleprofile에따른selected-response형식이다. 해당원문과공식법규를검토했으며protectedPre-MPJE/recall/상업bank원문을읽거나변환하지않았다.'}
 record=dict(question_id=qid,record_sha256=row['record_sha256'],family_id=byloc[qid]['family_id'],read_scope=dict(stem_read_completely=True,all_choices_read_completely=True,stored_key_read=True,core_explanation_read_completely=True,all_choice_explanations_read_completely=True,learning_boundary_read=True,choice_count=len(q['choices']),actual_visible_content_sha256=row['visible_content_sha256']),legal_review=dict(existing_answer_correct='NOT_ASSESSED' if exposed else 'YES',stored_key=q['correct_choice_ids'],independently_expected_key=[] if exposed else calculated,provisional_source_based_key_not_fresh=None if not exposed else calculated,per_choice_findings=opts,authorities=[copy.deepcopy(sources[k]) for k in dict.fromkeys(used)],verdict='HOLD' if exposed else 'KEEP',finding_ko=('이전D결론의집계및해당ID가AMBIGUOUS였다는checkpoint가full-historyfork에노출됐다. 현재공식자료와원문을다시읽었으나이세션을새whole-key독립판정으로세지않는다. 별도실제fresh세션필요.' if exposed else f'{qid}의모든보기지원여부를공식해당조항으로따로확인했고, '+('INCORRECT극성에따라거짓문장을선택하여' if 'INCORRECT' in q['stem'] else '참문장을선택하여')+f' 계산한키{calculated}가저장키와일치한다. 해설은이원문조건에한정하며법적release증명으로확대하지않는다.'),blocker='PRIOR_CONCLUSION_EXPOSURE_REQUIRES_GENUINELY_FRESH_SESSION' if exposed else None,law_checked_date=today,reviewed_at=stamp(),original_explanation_review=dict(core_read_in_full=True,all_choice_rationales_read_in_full=True,core_finding_ko=f'{topic}에관한원한국어core전문을공식조항과대조했다. 권고를must로확대하거나특수경로예외를보편화하지않는범위로읽는다. '+('childhoodvisit의during/purpose조건은별도fresh판정이필요하므로여기서PASS로닫지않는다.' if exposed else ''),choice_analysis={c['id']:dict(original_rationale_read=True,finding_ko=findings[c['text']][1],original_rationale_sha256=hashlib.sha256(q['explanation']['choice_analysis'][c['id']].encode()).hexdigest()) for c in q['choices']})),realism_review=dict(verdict='PASS' if all(cr.values()) else 'FAIL',decision='KEEP' if all(cr.values()) else 'NEEDS_REMEDIATION',criteria=cr,criterion_findings_ko=cf,finding_ko=reason,duplicate_review=dict(measurement_path=str(BASE/'duplicate-measurement.json'),measurement_sha256=sha(BASE/'duplicate-measurement.json'),nearest_candidates_measured=nearest,actual_comparison_read_ids=read_near+same,comparison_scope='Top two canonical/default candidates for each four-item same-case group and all four exact sibling originals; nearest rankings for every row retained. Rankings alone are not semantic verdicts.',automatic_similarity_is_verdict=False),score_used_as_verdict=False),exposure_limitations=dict(prior_item_conclusion_seen=exposed,fresh_whole_key_credit=0 if exposed else 1,description='Inherited checkpoint listed prior D38KEEP/2HOLD batch aggregate. Only0338/0339 were identified individually as priorAMBIGUOUS. No original Dreport was available or read. No author/independent report used to inherit option truth.'),safe_hold_recommended=exposed or not all(cr.values()),release_eligible=False,canonical_release_credit=0,required_next_action_ko=('별도실제fresh세션의전보기·키·법규·현실성검토를받고원차단이력을보존한다.' if exposed else ('현재독립stage판정은canonicalrelease가아니다. 기존negative/HOLD이력과archive-only상태를보존하고정식release절차를따른다.' if all(cr.values()) else '구체적현실성결함을해결한별도currentcontent에freshlegal/realism감사를수행한다. 기존원문·키·이력·사용자기록은보존하고기본연습에서보류한다.')))
 records.append(record)
context=[]
for path in ['docs/INDEPENDENT_LEGACY_REVIEW_RUNBOOK.md','docs/REVIEW_QUEUE.md','docs/RELEASE_POLICY.md','docs/AUDIT_WORKFLOW.md','docs/SOURCE_USE_POLICY.md','docs/QUESTION_AUTHORING_STANDARD.md']:
 target=BASE/'context'/Path(path).name;(ROOT/target).parent.mkdir(parents=True,exist_ok=True);(ROOT/target).write_bytes((ROOT/path).read_bytes());context.append(dict(path=str(target),sha256=sha(target)))
for path in ['data/exam_style/mpje_style_profile.json','data/blueprint.json','schemas/exam_style_profile.schema.json','schemas/blueprint.schema.json']:
 target=BASE/'context'/Path(path).name;(ROOT/target).write_bytes((ROOT/path).read_bytes())
profile=read(Path('data/exam_style/mpje_style_profile.json'));bp=read(Path('data/blueprint.json'))
report=dict(schema_version=1,stage='independent-legacy',job_id=job['job_id'],independent_of_authors=True,auditor='GPT',auditor_instance='GPT:/root/recover_d_review:20261104',actor_provenance=dict(actor_id='/root/recover_d_review',session_id='/root/recover_d_review'),canonical_audit=False,canonical_release_credit=0,author_review_credit=0,reviewed_at=today,reviewed_at_aware=stamp(),question_hashes=job['question_hashes'],context=dict(read_docs=context,assignment_path=str(BASE/'assignment.json'),assignment_sha256=sha(BASE/'assignment.json'),visible_input_path=str(BASE/'assigned-visible-input.json'),visible_input_sha256=sha(BASE/'assigned-visible-input.json'),previous_local_worker_evidence='UNAVAILABLE_IN_NEW_ENVIRONMENT_NOT_RECOVERED',original_missing_commit='ff66af3b only; fullSHA unresolved and GitHub422. No original bytes reconstructed.'),style_profile=dict(profile_id=profile['profile_id'],content_version=profile['content_version'],content_hash=profile['content_hash'],file_sha256=sha(Path('data/exam_style/mpje_style_profile.json')),schema_sha256=sha(Path('schemas/exam_style_profile.schema.json'))),blueprint=dict(content_version=bp['content_version'],content_hash=bp['content_hash'],file_sha256=sha(Path('data/blueprint.json')),schema_sha256=sha(Path('schemas/blueprint.schema.json'))),sources=list(sources.values()),records=records,summary=dict(assigned=40,visible_originals_read=40,all_choices_read=160,whole_key_assessed=38,whole_key_not_assessed_prior_exposure=2,legal_keep=38,legal_hold=2,realism_pass=sum(all(r['realism_review']['criteria'].values()) for r in records),realism_fail=sum(not all(r['realism_review']['criteria'].values()) for r in records),canonical_release_credit=0),limitations_ko=['원D로컬보고서/commit은현환경에없다. 이보고서는새실제세션의재검토이며원D판정을복구했다고주장하지않는다.','full-historyfork에원D집계및0338/0339의priorAMBIGUOUS가노출됐다. 두IDwhole-keyfreshcredit0/HOLD/NOT_ASSESSED를보존한다.','공식자료retrieval성공과정확section의실독을기록했으나전세계모든미게시개정·제품별상황까지법적효력을보증하지않는다.','canonical439/public2349/default202전체visible문장으로nearest후보를측정했으나semantic판정은명시적으로읽은근접원문에한정한다.','별도canonicaldata/audits admission/adjudication/RELEASED전환을수행하지않는다. 원0351을비롯한기존negative/HOLD는이법규키재확인으로해제하지않는다.'])
out=ROOT/'reports/full-corpus-review/recovered-phase11-d-review.json';out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report['summary'],ensure_ascii=False))
