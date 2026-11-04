import collections,datetime,hashlib,json,pathlib,sys
OUT=pathlib.Path(__file__).parent; PREFIX=OUT.resolve().relative_to(pathlib.Path.cwd()).as_posix()+'/'
p=json.loads((OUT/'notes101-a-visible-input.json').read_text());job=json.loads((OUT/'notes101-a-assignment.json').read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
source_meta={int(f.name.split('.')[0]):json.loads(f.read_text()) for f in (OUT/'sources').glob('*.meta.json')}
versions={1:'DailyMed BELBUCA revised12/2025; updated2026-01-02',2:'DailyMed XYWAV revised/updated7/2025',3:'DailyMed BRIXADI revised12/2025; updated2025-12-31',4:'DailyMed SUBLOCADE revised2/2025; updated2026-07-27',5:'DailyMed BUTRANS revised/updated5/2026',6:'DailyMed XYREM revised/updated7/2025',7:'DailyMed SPRAVATO highlights revised3/2026, Medication Guide09/2026, updated2026-09-22; 부분별 개정표기가 다름',9:'2026-11-04 current MA General Laws text; 개별 개정행위의 효력일은 페이지에서 확정하지 않음',10:'historical FDA label revised9/2024; current authority로 사용하지 않음',11:'eCFR title21 current through2026-11-02; 이 섹션 개별 개정효력일 전부는 확정하지 않음',12:'eCFR title45 current through2026-11-02; title last amended2026-10-29, 개별 조항 효력일과 동일하지 않음',13:'eCFR title45 current through2026-11-02; title last amended2026-10-29, 개별 조항 효력일과 동일하지 않음',14:'eCFR title45 current through2026-11-02; 개별 조항 효력일 전부는 확정하지 않음',15:'45CFR164.400 applies to breaches on/after2009-09-23; retrieved current through2026-11-02',16:'eCFR title45 current through2026-11-02; 개별 조항 효력일 전부는 확정하지 않음',17:'eCFR title45 current through2026-11-02; 개별 조항 효력일 전부는 확정하지 않음',18:'eCFR title45 current through2026-11-02; 개별 조항 효력일 전부는 확정하지 않음',19:'eCFR title45 current through2026-11-02; 개별 조항 효력일 전부는 확정하지 않음',20:'EPA current retrieved2026-11-04; 개별 guidance 발효일은 미확정',21:'FDA communication2025-08-27; REMS removal effective2025-06-13; page current2026-04-03',22:'FDA drug safety communication2022-01-12; 현재 접속한 FDA 공지의 제품/제형 설명만 사용',23:'FDA page current2026-03-04: elimination April2025, modifications fall2025; 각 품목별 정확 승인일은 페이지에서 전부 특정하지 않음',24:'FDA OA REMS modification approved2024-10-31; manufacturer mail-back availability deadline2025-03-31; page current2026-04-20',25:'FDA approval2026-02-09; delay notice2026-06-16; planned implementation2026-11-15; 2026-11-04 현재 미래 시행이며 실제 시행완료를 확인한 것은 아님',26:'FDA Q&A current2026-06-16; modified REMS의 미래 시행과 현재 testing enforcement discretion 구별',28:'FDA news release2025-09-25 REMS removal; page current2025-09-25',27:'FDA2024-09-16 notice; production discontinuation2024-09-30; page current2024-09-19. 공급 잔량/현 판매 여부를 실제 조사한 것은 아님',29:'MA Policy2023-02 adopted2023-05-04; revised2023-09-07/2025-09-04; 현행 URL PDF 회수',35:'2026-11-04 MA General Laws current text; 개별 amendment 효력일은 미확정',36:'eCFR title21 current through2026-11-02; Part1317 source79FR53565(2014-09-09), 개별 조항 효력일 전부는 확정하지 않음',37:'eCFR title21 current through2026-11-02; 개별 schedule 조항 효력일 전부는 확정하지 않음',41:'DailyMed LUMRYZ revised8/2026; updated2026-09-08. 검색API spl_version11/published2026-09-17과 표시업데이트일이 다르므로 단일 효력일로 합치지 않음',43:'eCFR title21 current through2026-11-02; 개별 schedule 조항 효력일 전부는 확정하지 않음',44:'DCP26-08-125 dated2026-08-25; rescinds/replaces DCP25-04-124; 개별 statewide algorithm 전체를 확인한 것은 아님',45:'247CMR9 official publication Massachusetts Register1536,2024-12-06; 현행 URL 회수, 개별 amendment 효력일 추가미확정',48:'DailyMed SUBOXONE revised/updated12/2025',49:'DailyMed ZUBSOLV revised1/2026; 현재 retrieved label, 실제 유통 lot labeling을 별도 확인하지 않음'}
def authority(n,section):
 meta=source_meta[n]; assert meta['status']==200
 stem=f'{n:02d}';raw=OUT/'sources'/f'{stem}.raw';txt=OUT/'sources'/f'{stem}.txt';mp=OUT/'sources'/f'{stem}.meta.json'
 return {'source_type':'PUBLIC_OFFICIAL','official_url':meta['url'],'exact_section':section,'law_checked_date':'2026-11-04','version_or_effective_date_status':versions.get(n,'현재 공식원문2026-11-04회수; 개별 효력일은 미확정'),'evidence_path':PREFIX+'sources/'+stem+'.raw','evidence_sha256':sha(raw),'text_evidence_path':PREFIX+'sources/'+stem+'.txt','text_evidence_sha256':sha(txt),'retrieval_metadata_path':PREFIX+'sources/'+stem+'.meta.json','retrieval_metadata_sha256':sha(mp)}
verdicts={}
def entries(uid,source,sections,findings):
 cs=next(x['claims'] for x in p['units'] if x['unit']['id']==uid)
 assert len(cs)==len(sections)==len(findings),(uid,len(cs),len(sections),len(findings))
 for c,sec,find in zip(cs,sections,findings):
  # Each section is (source number, exact clause), or list thereof.
  refs=[(source,sec)] if isinstance(source,int) else sec
  verdicts[c['claim_id']]={'claim_id':c['claim_id'],'claim_record_sha256':job['unit_bindings'][uid]['claim_record_sha256s'][c['claim_id']],'claim_read_completely':True,'legal_status':'KEEP','finding':find,'authorities':[authority(n,s) for n,s in refs]}
def refs(n,*sections):return [[(n,s)] for s in sections]
entries('ipledge-transition',None,[[(25,'FDA February9,2026 modification approval')],[(25,'FDA June16,2026 implementation-delay update')],[(25,'June16,2026: changed planned implementation toNovember15,2026')],[(25,'June16 delay paragraph; October13,2023 enforcement-discretion update')],[(26,'Q3/A3: registered health care professionals')],[(26,'Q3/A3: patients must be enrolled and agree to requirements')],[(26,'Q3/A3: pharmacies must be registered')],[(26,'Q3/A3: requirements determined by patient category')],[(25,'iPLEDGE REMS for Isotretinoin Products')],[(26,'Q6/A6 pretreatment tests in medical setting')],[(25,'February9,2026: Important changes for patients/prescribers')],[(25,'February9,2026: Important changes for pharmacies,30-day window')],[(25,'February9,2026: cannot-get-pregnant enrollment counseling/monthly documentation')],[(25,'February9,2026 pregnancy-test changes')],[(25,'February9,2026: annual pharmacy staff training/authorized representative records')],[(25,'February9,2026: removal of30-day prescription window')]],[
'FDA가2026-02-09 modification 승인 사실을 직접 명시한다. 승인과 시행을 구별한다.',
'현재 FDA 페이지의2026-06-16 절이 시행 연기를 직접 공지한다.',
'6월 공지는 기존8월8일에서 예정일을11월15일로 변경한다. 검토일11월4일에는 미래이다.',
'6월 절은 전체 modification 전까지10월2023 testing enforcement discretion을 계속한다고 한다. 두 상태를 같게 취급할 수 없다.',
'FDA Q3는 처방 health care professional의 iPLEDGE 등록을 요구한다.',
'FDA Q3는 수령 환자의 enrollment와 해당 요구 준수를 명시한다.',
'FDA Q3는 조제 pharmacy 등록을 명시한다.',
'Q3의 patient category에 따라 요건이 달라진다는 문구를 확인했다.',
'FDA는 모든 승인 isotretinoin의 shared-system이라고 하나 다른 retinoid 전체의 product-specific REMS를 여기서 대조하지 못했다.',
'Q6와2월 공지는 모든 pretreatment pregnancy tests의 medical-setting 조건을 남긴다.',
'치료 중·후에 prescriber가 허용하는 home testing과 pretreatment medical testing을 원문이 구별한다.',
'임신할 수 없는 환자의30일 prescription window 제거는 발표된 modification에 명시된다. 현행 전체 workflow로 조기 승계하지 않는다.',
'해당 환자는 enrollment counseling을 유지하되 monthly documentation을 더 이상 요구하지 않는다는 승인내용이다. 상담 자체 소멸이 아니다.',
'원문은 검사 장소,7-day window missed 반복검사 등 testing 변경을 열거한다. 본문은 미래 전부를 현행으로 확정하지 않는다.',
'FDA2월 공지에는 annual staff training과 authorized representative의 completion record 유지라는 clarification이 있다. 현재 상세 pharmacy training package는 별도 미확보다.',
'FDA 수정공지는 prescription-window 제거를 말한다. 이 자료만으로 현행30-day maximum supply의 별도 조항까지 입증하지는 못했다.'
])
entries('w5-b-9',None,refs(21,'What is FDA announcing:effectiveJune13,2025','What is FDA doing:participation no longer required','What should patients/HCPs do:ANC report/verification no longer REMS gate','What is FDA announcing/doing:continue ANC monitoring')+refs(23,'Eliminated REMS table:Ambrisentan Shared System','ERA prescribing information and EFT risk','Eliminated REMS table:Opsumit and generics','Eliminated REMS table:Opsynvi','Eliminated REMS table:Tryvio','ERA prescribing information and EFT risk','Modified REMS table:Bosentan Shared System','Modified REMS table:Filspari','Modified REMS paragraph:remove EFT requirements','Modified REMS paragraph:hepatotoxicity remains')+refs(28,'September25,2025 removal announcement','Same prescribing information/standard clinical care paragraph')+refs(25,'June16,2026 delayed implementation untilNovember15,2026','June16,2026 delay distinguished fromFebruary9 approval')+refs(21,'Risk remains;boxed warning and new Medication Guide','What FDA is doing:REMS removed/boxed warning retained')+refs(23,'Eliminated and Modified REMS tables'),[
'FDA는 clozapine REMS 제거 효력일을2025-06-13으로 명시한다.',
'Prescriber/pharmacy/patient의 기존 REMS 참여 의무가 더 이상 조제 전제가 아님을 FDA가 명시한다.',
'FDA는 ANC reporting과 pharmacy의 REMS eligibility/ANC verification 장벽 제거를 명시한다. 임상 검토 폐지는 아니다.',
'FDA는 prescribing information의 ANC monitoring frequency를 계속 따르도록 권고한다. federal REMS gate와 구별한 본문이 맞다.',
'Eliminated 표는 Letairis 및 ambrisentan generics를April2025 제거 대상으로 명시한다.',
'ERA label의 fetal-harm/pregnancy contraindication과 contraception 정보는 남는다.',
'Eliminated 표의 Opsumit 및 macitentan generics를 확인했다.',
'Eliminated 표의 macitentan+tadalafil Opsynvi를 확인했다.',
'Eliminated 표의 aprocitentan Tryvio를 확인했다.',
'FDA는 ERA의 EFT-risk mitigation labeling이 남는다고 한다. REMS 소멸과 위험관리 소멸을 같게 두지 않는다.',
'FDA는 bosentan Tracleer 및 generics의 REMS modification을fall2025 승인한 것으로 표시한다.',
'FDA는 sparsentan Filspari의 REMS modification을fall2025 승인한 것으로 표시한다.',
'두 수정은 EFT 관련 REMS요건 제거를 명시한다. 모든 REMS 제거가 아니다.',
'수정 후 두 제품의 hepatotoxicity 관련 REMS요건이 계속 유지된다고 직접 명시한다.',
'Caprelsa REMS 제거는2025-09-25 FDA news release가 명시한다.',
'동일 prescribing information과 standard clinical care가 남는다. 특별 certification/extra REMS monitoring 제거와 구별된다.',
'iPLEDGE11월15일은 예정 시행일이다.11월4일 현재 미래 workflow 완료를 단정할 수 없다.',
'FDA의 승인일과 연기 후 예정시행일을 대조하면10월20일에 수정 전부 시행이라고 외우는 해석은 성립하지 않는다.',
'Clozapine의 REMS제거 뒤에도 severe neutropenia 위험이 남는다는 FDA 사례가 일반 구별을 뒷받침한다.',
'같은 clozapine에서 boxed warning 유지와 REMS enrollment 제거가 동시에 명시되므로 두 사실은 동일하지 않다.',
'ERA의 eliminated/modified 차이와 iPLEDGE의 미래시행 사례는 제품별 현행상태를 구별하라는 학습 방법을 뒷받침한다.'
])
entries('w5-b-11',27,['September16,2024 update:production discontinuationSeptember30,2024','September16,2024:no new patient enrollments','September16,2024:no new prescriber/pharmacy enrollments','September16,2024:approved NDA/ANDA regardless marketing','September16,2024:existing patients while supply remains','TIRF medicine product list:Actiq','TIRF medicine product list:Fentora','TIRF medicine product list:Lazanda','TIRF medicine product list:Subsys','TIRF definition and dosage-form product list','December2020 modified REMS:outpatient prescriber certification','December2020 modified REMS:dispensing pharmacy certification','December2020 modified REMS:outpatient patient registry','December2020 modified REMS:document tolerance every outpatient prescription','December2020 modified REMS:outpatient pharmacy assess tolerance every dispensing','December2020 modified REMS:inpatient policies/procedures'],[
'FDA9월16일 공지는 제조사들이9월30일 생산을 중단한다고 발표했음을 직접 명시한다.',
'생산 중단에 따라 새로운 patient enrollment를 받지 않는다는 공지를 확인했다.',
'같은 문장은 prescriber와 pharmacy의 신규 enrollment도 중단한다고 한다.',
'NDA/ANDA 승인이 남는 동안 marketing status와 무관하게 REMS가 유지된다는 조건문이다. 현재 재고 판매가능성을 증명하지 않는다.',
'기존 환자는 남아있는 supply 범위에서 REMS하 치료를 계속할 수 있다고 한다. 무기한 공급 보장이 아니다.',
'Actiq oral transmucosal lozenge가 FDA TIRF list에 있다.',
'Fentora buccal tablet가 FDA TIRF list에 있다.',
'Lazanda nasal spray가 FDA TIRF list에 있다.',
'Subsys sublingual spray가 FDA TIRF list에 있다.',
'FDA 정의는 transmucosal immediate-release fentanyl이다. 경피 patch를 이 제형별 REMS로 자동 분류하지 않는다.',
'2020수정 후에도 outpatient 처방자의 program certification이 필요하다고 한다.',
'FDA는 TIRF dispensing pharmacy certification을 명시한다.',
'Outpatient TIRF 환자의 registry enrollment를 명시한다.',
'Prescriber는 outpatient 매처방마다 opioid tolerance를 document해야 한다.',
'Outpatient pharmacy는 매조제마다 tolerance 변화를 assess해야 한다.',
'Inpatient pharmacy는 tolerance verification policies/procedures를 마련한다. outpatient registry의 전부를 기계적 복사할 근거가 아니다.'
])
entries('w5-b-12',None,refs(4,'Highlights;2.1 subcutaneous extended-release injection')+refs(3,'Highlights;2.1 subcutaneous extended-release injection')+refs(4,'5.2 REMS:healthcare settings/pharmacies certification','5.2 REMS:directly toHCP forHCP administration')+refs(3,'5.2 REMS:certification','5.2 REMS:directly toHCP')+refs(4,'5.2 REMS:not dispensed to patient')+refs(3,'5.2 REMS:not dispensed to patient','2.1:weekly and monthly different formulations','2.1:doses weekly cannot be combined to monthly')+refs(5,'Highlights;2.1 transdermal system')+refs(1,'Highlights;2 buccal use')+refs(48,'Highlights;2 sublingual/buccal buprenorphine+naloxone film')+refs(49,'Highlights;2 sublingual buprenorphine+naloxone tablets')+[[(5,'1 Indications/severe persistent pain'),(4,'1 Indications/moderate-severe OUD')],[(4,'5.2 depot REMS'),(5,'5.5 Opioid Analgesic REMS'),(1,'5.5 Opioid Analgesic REMS')]]+refs(4,'1 Indications;2.3;14.3 single-dose transmucosal rapid induction')+[[(11,'21CFR1308.13(e)(2)(i) buprenorphine'),(4,'5.2 depot REMS'),(3,'5.2 depot REMS')]],[
'SUBLOCADE의 현행 label은 SC extended-release buprenorphine injection으로 식별한다.',
'BRIXADI의 현행 label은 SC extended-release buprenorphine injection으로 식별한다.',
'SUBLOCADE를 주문·조제하는 pharmacy/healthcare setting은 해당 REMS certification 대상이다.',
'SUBLOCADE5.2는 HCP에게 직접 공급하여 HCP가 투여하게 하는 경로를 명시한다.',
'BRIXADI5.2는 해당 pharmacy/healthcare setting certification을 명시한다.',
'BRIXADI5.2는 HCP 직접공급/HCP 투여를 명시한다.',
'SUBLOCADE5.2는 환자에게 dispense하지 않도록 verification procedures를 요구한다.',
'BRIXADI5.2는 환자에게 dispense하지 않도록 verification procedures를 요구한다.',
'BRIXADI2.1의 weekly와 monthly는 다른 formulations라는 직접 문구를 확인했다.',
'BRIXADI2.1은 weekly dose 합계로 monthly dose를 만들 수 없다고 명시한다. 임상적으로 허용된 label 전환표까지 부정하는 명제가 아니다.',
'BUTRANS는 buprenorphine transdermal system이다.',
'BELBUCA는 buprenorphine buccal film이며 buccal mucosa에 적용한다.',
'SUBOXONE 현행 label이 buprenorphine+naloxone sublingual/buccal film임을 확인했다. FDA dental 경고의 브랜드명 나열만으로 조합을 추정하지 않았다.',
'ZUBSOLV 현행 label이 buprenorphine+naloxone sublingual tablets임을 확인했다.',
'BUTRANS pain 적응증/route와 SUBLOCADE OUD 적응증/route가 다르다. generic명만으로 서로 대체하라는 label은 아니다.',
'BUTRANS/BELBUCA5.5의 opioid-analgesic education REMS는 SUBLOCADE5.2의 direct-HCP restricted distribution과 다르다.',
'현재 SUBLOCADE label은 single transmucosal dose 후 initiation을 포함한다. 모든 환자에게 과거7일 stabilization을 영구 요건으로 일반화할 수 없다. 안전한 환자별 induction 지시는 별도다.',
'Buprenorphine은1308.13(e)(2)(i)의CIII이며, schedule만으로 서로 다른 제품의 REMS가 통합되지 않는다.'
])
entries('w5-b-13',None,refs(7,'Highlights;2.1 esketamine nasal spray','Highlights CIII;9.1 controlled substance','5.5 SPRAVATO REMS certified settings','2.1 direct HCP supervision','2.1/5.5 supervised monitoring','5.5 only dispensed/administered certified settings')+[[(8,'FDA Online Label Repository disclaimer'),(7,'Highlights product identity/5.5 REMS')]]+refs(7,'5.5 product-specific SPRAVATO REMS')+refs(6,'Highlights/11 sodium oxybate')+refs(2,'Highlights/11 calcium oxybate','Highlights/11 magnesium oxybate','Highlights/11 potassium oxybate','Highlights/11 sodium oxybate')+refs(41,'Highlights/3 sodium oxybate extended-release suspension')+refs(11,'21CFR1308.13(c)(6) FDCA505-approved GHB products')+[[(11,'1308.13(c)(6) approved-product qualification'),(43,'1308.11(e)(1) GHB')]]+refs(6,'5.3 specially certified central pharmacy')+refs(2,'5.3 specially certified central pharmacy')+refs(41,'5.3 LUMRYZ REMS certified pharmacies')+[[(41,'2.1/2.4 once-nightly formulation/transition'),(6,'2.1 twice-nightly dosing')],[(41,'2.4 switching from immediate-release sodium oxybate'),(2,'2.5 switching from Xyrem')],[(41,'5.3 LUMRYZ REMS'),(2,'5.3 XYWAV andXYREM REMS')]],[
'SPRAVATO label은 esketamine nasal spray로 식별한다.',
'SPRAVATO label highlights와9.1은CIII라고 명시한다.',
'5.5는 certified healthcare setting과 product-specific REMS를 명시한다.',
'2.1의 direct HCP supervision 및5.5의 direct observation을 확인했다. 환자가 spray를 사용하더라도 supervision이 남는다.',
'각 session 후 적어도2시간 HCP monitoring과 안전한 퇴실평가가 필요하다. 본문은 monitoring 필요성만 말한다.',
'5.5는 certified setting에서만 dispense/administer하고 pharmacies는 certified settings에만 공급하게 한다. unrestricted take-home이 아니다.',
'Labels repository의 일반 disclaimer는 개별 compounded ketamine와 SPRAVATO 승인관계를 직접 판정하는 자료가 아니다. 현재 exact product-compounding authority는 미확보다.',
'SPRAVATO5.5는 특정 esketamine 제품의 REMS이다. compounded ketamine를 이 제품으로 취급해 자동 certification 적격성을 부여할 수 없다.',
'XYREM의 ingredient는 sodium oxybate이다.',
'XYWAV11은 calcium oxybate를 포함한다.',
'XYWAV11은 magnesium oxybate를 포함한다.',
'XYWAV11은 potassium oxybate를 포함한다.',
'XYWAV11은 sodium oxybate를 포함한다.',
'2024고정 PDF 대신2026-08 개정 current LUMRYZ label에서 sodium oxybate extended-release oral suspension임을 확인했다.',
'1308.13(c)(6)의CIII 예외는FDCA505 승인 GHB-containing drug product라는 한정이 있다.',
'승인 drug-product CIII 예외를 illicit GHB에 포괄 적용할 수 없다.1308.11(e)(1)의GHB 별도 분류도 직접 대조했다.',
'XYREM5.3은 specially certified central pharmacy 조제를 명시한다.',
'XYWAV5.3도 specially certified central pharmacy 조제를 명시한다.',
'LUMRYZ5.3은 별도 LUMRYZ REMS의 specially certified pharmacies를 명시한다.',
'LUMRYZ의extended-release once-nightly와XYREM의twice-nightly formulation은 같지 않다. 성분명만으로 자동대체한다는 명제가 아니다.',
'LUMRYZ2.4/XYWAV2.5에는 제품별 전환방법이 있다. 본문은 의학적으로 가능한 모든 전환을 금지하지 않고 regimen 자동대체를 금지하는 범위로 읽는다.',
'LUMRYZ REMS와XYWAV/XYREM REMS가 따로 명시되므로 기존 registry만으로 다른 제품의 REMS 절차를 충족했다고 추정할 수 없다.'
])
entries('w5-b-16',None,refs(24,'OA REMS update:October31,2024 approval/March31,2025 availability','OA REMS update:pharmacy option to order MBEs','OA REMS update:optional pharmacy order pathway','OA REMS update:existing disposal programs continue')+refs(36,'1317.01;1317.05(a);1317.30;1317.40;1317.70;1317.75','1317.05(a);1317.90;1317.95'),[
'FDA는 outpatient OA제조사가 pharmacy/dispensers 요청시 pre-paid MBE를 제공하도록 하는 modification과2025-03-31기한을 명시한다.',
'Pharmacy가 MBE를 order하는 것은 FDA가option이라고 표현한다.',
'FDA가 pharmacy option이라고 한 문구로부터 모든 opioid 처방마다 특정 envelope 의무가 생기지 않는다. 다른 법상 별도의무 여부 전체를 부정하는 결론은 아니다.',
'기존 disposal programs를 중단할 필요가 없다는 FDA 직접 문구를 확인했다.',
'DEA1317은 registrant inventory와 ultimate-user collection을 subpart A/B로 나눈다. mail-back/receptacle과 pharmacy inventory reverse-distribution을 혼동할 수 없다.',
'Author locator가USP797 FAQ로 잘못 연결되어 있었다. 이를 법적 근거로 채택하지 않고 직접회수한 DEA1317.05/1317.90/1317.95로 inventory disposal/destruction 의무를 독립 확인했다. OA교육이 대체한다는 예외는 없다.'
])
entries('w3-b-12',None,refs(12,'160.103 PHI/individually identifiable health information')+refs(16,'164.502(a) covered entity/business associate uses/disclosures')+refs(12,'160.103 PHI(1)(i),(ii) electronic','160.103 PHI(1)(iii) any other form/media','160.103 PHI(1)(iii) any other form/media','160.103 identifiable care/payment data','160.103 identifiable health condition information','160.103 identifiable health information/electronic media')+refs(14,'164.306(a),(c) electronic PHI','164.306(c) standards164.308/310/312')+refs(15,'164.400 subpartD breach applicability')+refs(12,'160.103 business associate(1)(i) billing','160.103 business associate(1),(3)(i) data service/routine access','160.103 business associate(1)(i) data analysis')+refs(16,'164.502(e)(1),(2) satisfactory assurances/written arrangement')+refs(12,'160.103 business associate(4)(i) treating provider exclusion')+refs(16,'164.502(a)(3) contract limitation'),[
'160.103은 PHI를 identifiable health information과 그 매체/예외로 정의한다. identifiable라는 조건을 지우지 않는다.',
'164.502(a)는 covered entity와BA의use/disclosure를 허용·요구된 경우로 제한한다.',
'전자 전송·보관 정보도 정의에 포함된다.',
'Any other form or medium이라는 정의가 paper를 포함한다.',
'Any other form or medium이므로 구두 PHI도 보호범위일 수 있다.',
'이름과 약물이 연결되어 care에 관한 identifiable정보이면 PHI 정의에 들 수 있다. 모든 봉투를 자동 확정하는 서술은 아니다.',
'식별가능 환자의 진단 상담발언은 건강상태에 관한 PHI일 수 있다.',
'식별가능 patient profile은 전자형태 PHI일 수 있다.',
'164.306(a),(c)는 ePHI security의 별도 기준이다.',
'164.306(c)가164.308/310/312 등 administrative/physical/technical standards를 참조한다.',
'SubpartD164.400은2009-09-23이후 PHI breach에 적용하는 별도 notification규칙의 applicability다.',
'Billing은160.103 BA 정의에 명시되며 pharmacy대신 처리하는 역할과 workforce예외를 본다.',
'정기적으로PHI에 접근하는 data transmission/IT 서비스는 실제 기능에 따라BA일 수 있다. 모든IT업체라는 일반화는 아니다.',
'On-behalf data analysis도BA 정의에 명시된다.',
'164.502(e)는 해당BA satisfactory assurances를164.504(e)에 맞는 written contract/arrangement로 문서화하게 한다.',
'환자 treatment disclosure를 받는 healthcare provider는 그 관계만으로BA가 아니라는 정의상 제외를 확인했다.',
'164.502(a)(3)는 계약이 있어도 covered entity가 했으면 위반인 이용을 일반 허용하지 않는다. 명시된 limited contract purposes는 별도다.'
])
entries('w3-b-13',None,refs(17,'164.506(a),(c)(1) treatment','164.506(a),(c)(1),(3) payment','164.506(a),(c)(1),(4) operations','164.506(c)(2) other provider treatment')+refs(19,'164.514(d)(2) workforce need/access categories')+refs(16,'164.502(b)(1) reasonable efforts/minimum necessary','164.502(b)(2)(i) provider treatment disclosures/requests','164.502(b)(2)(ii) to individual','164.502(b)(2)(iii) valid authorization','164.502(b)(2)(v) required by law')+refs(19,'164.514(d)(2)(i),(ii) internal uses')+refs(18,'164.508(a)(3) marketing and exceptions','164.508(a)(4);164.502(a)(5)(ii) sale')+[[(17,'164.506(a) excludes required authorizations'),(18,'164.508(a)(3),(4) marketing/sale')]],[
'164.506(a),(c)는 허용된treatment PHI경로를 마련한다. 다른authorization-required 범주와 safeguards는 남는다.',
'Payment도 own use/disclosure와 다른covered entity/provider의 payment 활동의 조건으로 허용된다.',
'Health-care operations도허용되나 타entity의operations는 관계·목적조건이 있다. 본문은허용범위내라고 한정한다.',
'164.506(c)(2)는 다른healthcare provider의treatment activities를 위한disclosure를 허용한다.',
'내부workforce에서업무상 필요한사람/범위/조건을식별·제한하는164.514(d)(2)가curiosity access를 정당화하지 않는다.',
'Minimum necessary는 intended purpose를 달성할 최소PHI로 제한하려는reasonable efforts다.',
'164.502(b)(2)(i)의disclosures to/requests by provider for treatment 예외를 확인했다. 내부모든use 예외가 아니다.',
'164.502(b)(2)(ii)는본인에게허용·요구되는use/disclosure 예외를 명시한다.',
'164.502(b)(2)(iii)는164.508 authorization에따른use/disclosure 예외를 명시한다.',
'164.502(b)(2)(v)는164.512(a)의required-by-law 경로예외를 명시한다.',
'외부treatment disclosure예외와내부workforce의role-based use 제한이별도로존재한다.',
'164.508(a)(3)는marketing authorization과face-to-face/nominal gift 예외를 명시한다. 본문일반론이맞다.',
'164.508(a)(4)는sale의authorization 및remuneration명시를요구한다. sale정의자체의예외도있으므로모든금전거래라고확장하지않는다.',
'164.506(a)의허용TPO는164.508의marketing/sale authorization을이름바꾸기로면제하지않는다.'
])
entries('w3-b-14',None,refs(13,'164.510(b)(1) directly relevant care/payment information','164.510(b)(2) available/capable patient agreement/no objection/inference','164.510(b)(3) absent/incapacitated professional judgment','164.510(b)(3) common-practice prescription pickup inference','164.510(b)(1) relevant scope;164.502(g) separate representative authority','164.510 introductory oral agreement;164.502(a)(1)(v)','164.502(g)(3) minors/state law','164.502(g)(3)(i),(ii) minor consent/state law')+refs(9,'MGLc112§12F paragraph2(i) married/widowed/divorced','MGLc112§12F paragraph2(ii) parent/child','MGLc112§12F paragraph2(iii) armed forces','MGLc112§12F paragraph2(iv) pregnant/believes pregnant','MGLc112§12F paragraph2(v) separate living/manages finances','MGLc112§12F paragraph2(vi) disease-limited consent','MGLc112§12F paragraphs1,2(vi) sexually active HIV prevention','MGLc112§12F paragraph2 categories and limited disease clause','MGLc112§12F final paragraph confidential records','MGLc112§12F final paragraph written consent/proper judicial order','MGLc112§12F final paragraph life/limb notification','MGLc112§12F final paragraph scope;HIPAA164.502(g)(3)')+[[(29,'Policy2023-02§II vaccine recipients age5+'),(9,'MGLc112§12F independent consent')],[(44,'DCP26-08-125 GeneralPrescribingRequirements(a),(d);HIVPrevention(a),(b)'),(9,'MGLc112§12F consent scope')],[(9,'MGLc112§12F final paragraph care confidentiality'),(13,'164.502(g)(3) personal representative/disclosure')]],[
'164.510(b)(1)는가족/지정인care/payment관여에직접관련된PHI를허용경로에따라공개할수있게한다.',
'환자가available하고capacity가있으면agreement,object할기회와반대없음,또는professional-judgment inference를본다.',
'환자가없거나incapacity/emergency로확인이불가능한경우best interests판단후관련PHI만공개하는경로다.',
'164.510(b)(3)는filled prescription pickup의common practice를professional judgment로고려할수있다고직접예시한다.',
'Care참여공개는관련범위만이다.가족의다른법적personal representative권한은별도여서가족관계만으로항상전체기록권한이생기지않는다.',
'164.510은oral agreement도허용한다.모든pickup설명에별도written authorization가필수는아니다.',
'164.502(g)(3)는state law의parent권한과minor독립consent/기밀약정등예외를함께본다.',
'부모가보험료를냈다는사실은164.502(g)(3)의consent/state-law조건을대체하지않는다.',
'12F paragraph2(i)에married/widowed/divorced minor를명시한다.이범주의동의권을특정질병에만한정하지않는다.',
'Paragraph2(ii)는minor가부모이면자신과그child care consent를명시한다.다른명시제한은별도로남는다.',
'Paragraph2(iii)는armed forces member를명시한다.',
'Paragraph2(iv)는pregnant 또는believes pregnant를명시한다.',
'Paragraph2(v)는separate living과자기financial affairs관리둘다필요하다.',
'Paragraph2(vi)는specified exposure/disease와그질환diagnosis/treatment범위를한정한다.모든category를질병한정으로읽지않는다.',
'12F는sexually active minor의HIV prevention consent를명시한다.약사제품별prescribing권한과동일하지않다.',
'12F는category별서술이다.특정질병한정예외를모든care에일반화하면안되지만marriage등다른범주의넓은care consent까지부정해서도안된다.기존미해결범위유지.',
'12F마지막문단은해당minor-consented medical/dental care기록의confidentiality를명시한다.',
'동일문단은minor written consent 또는proper judicial order외release금지문구를갖는다.바로뒤의notification규칙도함께읽었다.',
'Attending physician/dentist가life/limb endangered로합리적판단하면parent/guardian/foster parent에게통지하고minor에게통지사실을알린다.',
'12F는그section에따라동의한care정보범위다.모든minor의모든pharmacy기록에무조건공개/비공개일률규칙을만들지않는다.',
'Policy2023-02§II의5세이상administration scope와12Fconsent판정은별도다.본문은특정vaccine의환자적격성을전부확정하지않는다.',
'DCP26-08-125는허용FDA제품,approved labeling/statewide guidance,질환별training을요구한다.12Fconsent만으로제품/전문가scope를확대하지않는다.상세statewide algorithm은이번감사의범위아니다.',
'12F는care consent와마지막문단의기록공개를별도로규정하고HIPAA도personal representative를따로판단한다.두권한을합치지않는다.'
])
entries('w3-b-15',None,refs(13,'164.520(c)(2)(i) direct-treatment provider NPP','164.520(c)(2)(ii) good-faith acknowledgment','164.520(c)(2);164.508(b),(c) specific authorization','164.524(b)(2)(i);164.501 designated record set','164.524(b)(2) 30days after receipt','164.524(b)(2)(ii)(B) one extension up to30days','164.524(b)(2)(ii)(A) timely written reasons','164.524(b)(2)(ii)(A) completion date','164.524(b)(2);164.502(e) BA does not reset covered entity clock','164.530(j)(1);164.508(b)(6) required documentation','164.530(j)(2) six years from later creation/last effective date','164.530(j)(1),(2) documentation scope')+[[(13,'164.530(j)(1),(2)'),(45,'247CMR9.16(1) at least2years')],[(13,'164.530(j)(1),(2)'),(45,'247CMR9.16(1) separate pharmacy record minimum')]]+refs(13,'164.526(a),(b),(c) amendment right/denials','164.522(b) confidential communications','164.522(a) restrictions/mandatory self-pay condition','164.528(a) accounting and exceptions','164.526(c)(1) identify/append/link amendment'),[
'Direct-treatment covered provider에게첫서비스시점또는emergency후as-practicable NPP제공을요구한다.',
'164.520(c)(2)(ii)는emergency제외good-faith written acknowledgment노력과미수령이유문서화를명시한다.',
'NPPreceipt acknowledgment와164.508의목적/범위/유효조건을갖는authorization는별도다.',
'164.524(b)(2)는원칙적으로covered entity의request receipt후30일이내조치다.정의된record-set범위와예외는남는다.',
'조문은30days라고하며business-day제한이없다.일반calendar기간으로읽는다.',
'추가최대30일이며동일request에는한번만허용한다.',
'초기기한안에delay의서면이유를알려야한다.',
'그서면에는완료예정일도포함해야한다.',
'조문의receipt기준은covered entity다.BA로전달하거나offsite에있다는이유로시계를재시작하는문구가없다.',
'164.530(j)(1)은written policies/procedures와required writings/documented actions를보존대상으로삼고authorization문서도164.508(b)(6)의대상이다.',
'164.530(j)(2)는creation 또는last-effective중늦은날부터6년이다.무조건최초작성일부터만계산하지않는다.',
'문서범위가HIPAA-required documentation이므로모든medical/pharmacyrecord에6년또는정확폐기일을부여하는규칙이아니다.',
'실제247CMR9.16(1)의pharmacy기록최소2년과HIPAA적용문서6년을독립확인했다.2년경과가privacy문서일괄폐기허가가아니다.',
'247CMR9.16(1)과164.530(j)는다른scope의최소치다.같이해당하는자료는둘을충족해야한다.',
'164.526(a),(c)는amendment right,허용denial,수락시절차를규정한다.본문은모든요청을무조건수락한다고하지않는다.',
'164.522(b)는alternative means/location의reasonable confidential communication요청을accommodate하는조건부권리다.',
'164.522(a)는restriction요청권과일반동의의무없음,특정self-pay health-plan disclosure의mandatory restriction등을구별한다.',
'164.528(a)는accounting권리와TPO/authorization/가족care등예외를갖는다.모든공개목록권리로확대하지않는다.',
'수락amendment는affected record를식별하여append/link한다.원기록추적을숨겨사실을조작하는권한이아니다.'
])
# Preserve unresolved author source blockers; no automatic legal clearance.
blocked={
'NOTE-WAVE3-IPLEDGE-TRANSITION-009':'FDA iPLEDGE페이지의isotretinoin범위만으로다른retinoid별승인REMS/label전체를대조하지못했다.기존source-blocker를자동해제하지않는다.',
'NOTE-WAVE3-IPLEDGE-TRANSITION-015':'FDA공지는annual training clarification자체를입증하지만기존blocker인현재approved pharmacy training package상세를확보하지못했다.기존보류유지.',
'NOTE-WAVE3-IPLEDGE-TRANSITION-016':'30-day prescription window와별도의30-day supply maximum을규정하는현행pharmacy guide원문미확보.기존보류유지.',
'NOTE-WAVE9-W3-B-14-016':'Specific disease-limited consent와marriage등broad status-based consent의구별을현재문구가얼마나포괄하는지기존source-blocked범위가남는다.12F를대조했지만일반문구의모든확대적용을승인하지않는다.',
'NOTE15-w5-b-13-007':'Author의labels.fda.gov일반disclaimer는compounded ketamine의개별approval지위를확정하지않는다.추가FDA알림URL2건은404로직접원문확보실패;source_block으로남긴다.'}
for cid,reason in blocked.items():verdicts[cid].update(legal_status='SOURCE_BLOCKED',blocker=reason)
omissions={'ipledge-transition':['본문2단락의 “이번 dispensing authorization을 확인”은 participant enrollment/qualification과 별개의 처방별 조제 authorization 명제다. NOTE-WAVE3-...005–008은 등록/환자category만 열거하고 각 dispensing authorization 자체를 독립 열거하지 않았다. 현재 guide의 authorization 요건/기한을 확인할 추가 법규 항목으로 census에 보완해야 한다.'], 'w5-b-11':['본문2단락의 “같은 성분·CII”는 fentanyl/TIRF와fentanyl transdermal patch의 ScheduleII 분류를 전제한 독립 법적 명제다.001–016은 생산중단/REMS/제형을 열거하지만 CII 분류를 열거하지 않았다.독립회수21CFR1308.12(c)(9)의 fentanyl 조항으로 실제 법적 내용도 확인했다.']}
methods={
'ipledge-transition':'4단락을문장별로분해하여승인/연기일,집행재량,participant자격,처방별authorization,category,testing,window,supply,annualtraining을16claims와양방향대조.현재dispensing authorization명제를등록claims와별개로발견했다.',
'w5-b-9':'도입의REMS/위험/boxed-warning구별과7개제품행의상태·잔존위험·날짜를21claims와양방향대조.표의각약물·조합을FDA표와대조하고editorial운영매뉴얼한계를별도분류했다.',
'w5-b-11':'3단락의생산/신규enrollment/승인존속/남은재고,4brands,patch비교,outpatient·inpatient조건을16claims와대조했다.본문의CII분류전제가열거되지않음을확인했다.',
'w5-b-12':'3단락과제목의CIII를formulation/route/REMS공급처/환자직접교부/brand-composition/indication/과거7일generalization의18명제로대조.각부정문과weekly/monthly차이를별도로매칭했다.',
'w5-b-13':'3단락을Spravatoidentity/schedule/setting/supervision/monitoring,compound제품구별,4oxybatessalts,Lumryzformulation,approval한정schedule,각REMS/자동대체금지의22명제로대조했다.',
'w5-b-16':'2단락의manufacturer요구/pharmacy선택/universal-rule부정/기존disposal선택/ultimate-user대inventory/DEA대체불가를6claims와대조했다.잘못된USPsource locator는새DEA원문으로재검증했다.',
'w3-b-12':'3단락의PHI정의·3매체·3예시,Privacy/Security/Breach3층,BA서비스3유형·writtenassurance·treating-provider제외·BAA한계를17claims와양방향대조했다.',
'w3-b-13':'3단락의T/P/O각허용,provider treatment,workforce제한,minimumnecessary원칙·4예외,marketing/sale/외부홍보구별을14claims와대조했다.외부treatment예외를내부use에확대하지않았다.',
'w3-b-14':'4단락의가족범위/available·absent환자/픽업판단,minor대표권,12F각status·질병·HIV경로,기밀·writtenconsent·judicialorder·life/limb통지,4별도판단축을23claims와대조했다.',
'w3-b-15':'4단락의NPP/acknowledgment대authorization,requestclock·1회연장·서면내용·BA,6년scope와state기록보존,amendment/confidentialcommunication/restriction/accounting/append-link를19claims와대조했다.'}
records=[]
for u in p['units']:
 uid=u['unit']['id'];cs=[verdicts[c['claim_id']] for c in u['claims']];om=omissions.get(uid,[])
 records.append({'unit_id':uid,'binding':job['unit_bindings'][uid],'body_read_completely':True,'completeness':'OMISSIONS_FOUND' if om else 'COMPLETE','completeness_method':methods[uid],'omissions':om,'legal_status':'LEGAL_HOLD' if om or any(c['legal_status']=='LEGAL_HOLD' for c in cs) else 'SOURCE_BLOCKED' if any(c['legal_status']=='SOURCE_BLOCKED' for c in cs) else 'KEEP','claims':cs})
next(r for r in records if r['unit_id']=='w5-b-11')['omission_authorities']=[authority(37,'21CFR1308.12(c)(9) Fentanyl')]
context=json.loads((OUT/'notes101-a-related-context.json').read_text())
report={k:job[k] for k in ['stage','actor_provenance','auditor','auditor_instance']}
report.update(independent_of_authors=True,canonical_audit=False,canonical_release_credit=0,question_audit_credit=0,reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),records=records,scope_notes_ko='배정된current body10개/172claim전량의독립법규·완전성감사.저자및기존독립보고서결론은읽거나승계하지않았다.이보고서의처리수는release PASS가아니다.',input_observations={'assignment_raw_sha256':sha(OUT/'notes101-a-assignment.json'),'visible_input_raw_sha256':sha(OUT/'notes101-a-visible-input.json'),'related_context_raw_sha256':sha(OUT/'notes101-a-related-context.json'),'body_sha_and_census_raw_and_claim_record_bindings_verified':True,'root_strict_inventory_observation':'전달된packet의root strict inventory 관찰을입력provenance로보존한다.그것은독립법규판정을뜻하지않는다.','worker_load_notes_run':False,'worker_sparse_limitation':'immutable full-preimage sparse제외로loader재실행은하지않았고guard를우회/모킹하지않음;root가submit/integrate시에fulltree현재inventory를검증한다.'},related_surface_review={'questions_read_completely':True,'question_count':119,'question_ids':context['related_ids'],'all_stems_choices_keys_explanations_read':True,'reading_method':'raw119문항의모든stem/choice/전체explanation을lossless중복문구사전160개stem/choice+235개explanation과119개ID별완전mapping으로전량읽었다.현재rootprojection과해당4필드차이0개를대조했다.중복문장을새독립사례로세지않는다.','derived_count':11,'derived_visible_text_read_completely':True,'derived_findings_ko':['LAW-036의pain/OUD/제품별공급경로구별은이번buprenorphine본문과정합한다.다른methadone단원은배정외이므로새법규KEEP를부여하지않는다.','LAW-043/RF-036/RF-C-privacy/PHI-ePHI/TPOglossary는TPO대curiosity/family범위와Privacy/Security구별을유지한다.','clock-23은30calendar/조건부1회최대30일연장을유지한다.','LAW-044와RF-009/RF-062/RF-C-rems는승인대시행및REMS대monitoring구별을유지한다.다만currentdispensing조건을언급하는derived가있어도본문censusauthorization누락을해소하지못한다.','RF-C-privacy의배정외w6-a-12/w1-a-10 stored_source_hashes와source_hashes차이는관찰했으나배정단원binding은모두일치했다.배정외해시를수정하거나법규판정하지않는다.'],'question_boundary_ko':'MA-CASE/EXP/REV관련문항의전문/keys/모든해설을읽어본문과의설명정합성만평가했다.다른단원의mifepristone/HIV상세algorithm/전자security통제까지canonical독립질문PASS로승격하지않는다.문항감사credit0.'},summary={'units':10,'claims':172,'completeness_counts':dict(collections.Counter(r['completeness'] for r in records)),'unit_legal_counts':dict(collections.Counter(r['legal_status'] for r in records)),'claim_legal_counts':dict(collections.Counter(c['legal_status'] for r in records for c in r['claims']))},source_limitations_ko=['Firecrawl tool은잔여credit부족으로실제미실행.이를오류로기록하고공식HTTPS URL을직접회수했다.','eCFR/API XML4건406,USPFAQ403,추가FDAURL3건404실패도metadata에보존했다.실패응답을법규KEEP근거로쓰지않았다.','FDAlabels일반disclaimer를compoundedketamineapproval증거로사용하지않고해당claim을SOURCE_BLOCKED로두었다.','LUMRYZ2024PDF는historical비교원문으로만보존하고최신2026label을authority로사용했다.','검토일2026-11-04의접속공식원문과각사이트표시현재성만확인했다.개별시행일이특정되지않은법규는그한계를각authority에명시했다.'])
(OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
manifest=[]
for f in sorted((OUT/'sources').iterdir()):
 if f.is_file():manifest.append({'path':f.resolve().relative_to(pathlib.Path.cwd()).as_posix(),'raw_sha256':sha(f),'bytes':f.stat().st_size})
(OUT/'source-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report['summary'],ensure_ascii=False))
