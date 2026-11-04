import json,hashlib,re,subprocess,sys
from pathlib import Path
P=Path('reports/full-corpus-review/independent-notes/final86-a'); S=P/'sources'
job=json.loads((P/'assignment.json').read_text()); packet=json.loads((P/'visible-input.json').read_text()); context=json.loads((P/'related-context.json').read_text())
sha=lambda b:hashlib.sha256(b).hexdigest()
canon=lambda o:sha(json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
D={u['unit']['id']:u for u in packet['units']}; A={uid:{} for uid in D}
def keep(uid,n,src,section,anchor,reason):
 for i in ([n] if isinstance(n,int) else n):
  assert i not in A[uid],(uid,i)
  A[uid][i]=('KEEP',src,section,anchor,reason)
def k(uid,n,src,section,anchor,reason):keep(uid,n,src,section,anchor,reason)
def sb(uid,n,reason):
 for i in ([n] if isinstance(n,int) else n):
  assert i not in A[uid],(uid,i)
  A[uid][i]=('SOURCE_BLOCKED',None,None,None,reason)
def fq(uid,n,q,reason):k(uid,n,1,'USP <797> public FAQ Q'+str(q),str(q)+'. ',reason)
# Every line below is an independent claim-specific adjudication, not an author verdict projection.
u='w4-b-21'
fq(u,1,171,'Category 3의 Table 14 상한은 모든 applicable requirements를 충족할 때만 허용되고 Category 2에는 Table 13이 적용된다. 단순 표 숫자만으로 BUD를 부여할 수 없다.')
fq(u,2,175,'안정성 또는 무균성 유지기간이 category 상한보다 짧으면 더 짧은 BUD를 부여하라고 직접 설명한다.')
sb(u,3,'현재 full <797>의 ingredient-expiration 제한 조항을 직접 확보하지 못했다. FAQ175의 CSP 안정성 일반론만으로 모든 성분 expiration의 법적 처리와 예외를 확정하지 않는다.')
fq(u,4,171,'보수적인 BUD 설정에서 container-closure integrity를 고려하도록 직접 열거하므로 용기 무결성보다 긴 기간을 자동 허용할 수 없다.')
fq(u,5,177,'배치별 sterility release testing과 physicochemical stability를 입증하는 stability-indicating assay study를 구별한다. 무균시험만으로 화학적 안정성이 입증되지 않는다.')
sb(u,[6,7,8],'현재 USP <659>/<797> 정본의 보관 온도 정의를 확보하지 못했다. 2022 BUD fact sheet는 최신 정본 전체의 대체 근거가 아니므로 해당 온도 범위의 현행성을 확정하지 않는다.')
fq(u,9,170,'저장기간은 제품에 표시한 storage condition의 원래 BUD를 초과할 수 없다고 하므로 제품별 허용조건과 표의 보관분류를 연결해야 한다.')
sb(u,list(range(10,15))+list(range(17,34)),'현재 USP <797> Tables12–14와 모든 부속조건을 직접 확보하지 못했다. 공개 2022 fact sheet만으로 이 category·공정·시험·보관조건에 해당하는 정확한 최대기간 또는 freezer 경로 부재를 현행 정본으로 인증하지 않는다.')
fq(u,15,172,'질문 자체가 aseptic Category 2, sterile ingredients only, controlled room temperature의 4일 BUD를 특정하고 답변이 그 개정 근거를 설명한다. 2022공개USP BUD요약표의no-sterility/sterile-only행도같은4일을명시한다. 최신정본전체조건을인증한다는뜻은아니다.')
fq(u,16,181,'Category 2 전환 예시에서 4 days room temperature와 10 days refrigerated를 명시한다. 2022공개USP BUD요약표는그10일을aseptic/no-sterility/sterile-only행으로특정한다. 모든Category2공정에확대하지않고정본접근한계를유지한다.')
fq(u,34,170,'BUDs must not be additive라고 명시하고 냉동 후 해동하여 room-temperature 기간을 더해 연장하는 것을 부정하므로 45+10 자동 합산도 허용되지 않는다.')
fq(u,35,170,'원래 표시된 보관조건의 BUD를 넘기지 못한다는 원칙에 따라 하나의 저장·사용계획 안에서 기간을 판단해야 한다. 검증되지 않은 온도전환 연장은 근거가 없다.')
fq(u,36,177,'Category 3의 physicochemical stability는 stability-indicating assay study로 입증하고 실제 formula·procedure가 시험과 정확히 같아야 한다.')
fq(u,37,177,'시험과 CSP의 container closure systems가 exactly the same이어야 한다고 하므로 다른 용기·마개 자료를 자동 전용할 수 없다.')
for n,term in [(38,'personnel qualification'),(39,'sterile garb'),(40,'environmental monitoring'),(41,'sporicidal')]:fq(u,n,12,'Category 3 추가요건 설명에서 '+term+'에 관한 강화 조건을 실제로 열거한다. 세부 주기·모든 예외를 이 일반 명제의 KEEP에 포함하지 않는다.')
fq(u,42,12,'Category 3 추가 품질조치에 sterility testing을 명시한다.')
fq(u,43,12,'Category 3의 추가시험 설명은 endotoxin testing을 when applicable로 한정하므로 모든 CSP에 무조건 적용한다는 뜻이 아니다.')
fq(u,44,171,'BUD 설정 시 고려할 평가에 particulate matter를 명시한다. 시험의 전 세부방법까지 인증하지 않는다.')
fq(u,45,171,'BUD 설정 시 container closure integrity를 명시한다. 개별 용기 시험방법의 적합성까지 인증한 판정은 아니다.')
u='w4-b-22'
fq(u,1,195,'공개 FAQ에 인용된 조항은 single-dose container가 ISO Class5 또는 cleaner air에서 처음 entry/puncture된 경우를 직접 전제로 한다.')
fq(u,2,195,'해당 ISO5-or-cleaner first entry 조건에서 up to12h를 명시한다.')
fq(u,3,189,'bulk package 예에서 안정성 기준 기간이 더 길어도 더 짧은 labeled 사용시간을 함께 준수해야 한다고 명시한다. 짧은 applicable product restriction을 무시한 12시간 일률 적용은 근거가 없다.')
fq(u,4,195,'12시간 사용 동안 labeled storage requirements를 유지하는 조건을 직접 붙인다.')
fq(u,5,185,'septum 또는 metal septum ring을 제거한 용기는 ampule처럼 보며 어떤 기간도 보관하지 못한다고 설명한다.')
fq(u,6,188,'Multiple-Dose Container 정의를 parenteral administration용으로 특정하고 28일 규칙을 설명하므로 모든 topical 제품 규칙이 아니다.')
fq(u,7,188,'공개 FAQ는 conventionally manufactured multiple-dose containers에 initial entry/puncture 이후28일을 적용한다고 설명한다.')
fq(u,8,188,'28일 원칙에는 manufacturer가 다른 기간을 정한 경우라는 예외가 직접 있다.')
fq(u,9,188,'공개 FAQ는 이 labeling 규칙이 conventionally manufactured sterile topical products에는 적용되지 않는다고 명시한다.')
fq(u,10,188,'정의가 parenteral multidose container로 한정되므로 모든 개봉약에 동일28일을 붙이는 결론은 나오지 않는다.')
sb(u,11,'현재 full <797>의 compounded multiple-dose CSP category 제한 조항을 확보하지 못했다. FAQ178의 항균효력시험 설명만으로 Category2/3 조건 전체를 확정하지 않는다.')
fq(u,12,178,'aqueous multiple-dose CSP에는 <51> antimicrobial effectiveness testing 통과를 직접 요구한다. 해당하는 수성 multidose 경로의 명제로 판단했다.')
fq(u,13,180,'항균효력시험 자료를 원용할 때 formulation과 container closure system이 시험과 같아야 한다는 조건을 직접 명시한다.')
sb(u,14,'full <797>의 compounded-multidose labeling 조항을 직접 확보하지 못했다. 일반 약국표시·상용제품 개봉 규칙으로 이 별도 표시요건을 대체하지 않는다.')
fq(u,15,194,'공개 FAQ는 assigned BUD 또는 initial puncture 이후28일 중 짧은 기간까지만 사용한다고 직접 인용한다.')
sb(u,[16,17,18,19],'single-patient nonpreserved topical/ophthalmic CSP의 별도 labeling 및24h RT/72h refrigerated 경로와 적용제외를 현행 <797> 정본에서 직접 확인하지 못했다. FAQ188의 상용 topical 제외만으로 이 조제제품 경로의 요건을 입증하지 않는다.')
fq(u,20,194,'원료 multiple-dose container의 post-puncture 사용시간이 이를 써 만든 최종 CSP의 BUD를 제한하지 않는다는 별도 원칙을 직접 설명한다.')
fq(u,21,191,'commercial source container의 puncture-time limit와 최종 CSP BUD를 구별하므로 적법하게 원료를 사용했다는 사실만으로 완제품 최대기간이 자동 확정되지 않는다.')
u='w4-b-23'
sb(u,1,'full <797>의 release label/order 일치검사 조항을 확보하지 못했다. 공개 FAQ155의 외관검사만으로 label와 order 비교의 정확한 의무를 인증하지 않는다.')
fq(u,2,164,'compounding 완료 후 release/dispensing 전에 physical appearance가 예상대로인지 시각검사를 해야 한다는 정본 문구를 직접 인용한다.')
for n,term in [(3,'visible particulates'),(4,'cloudiness'),(5,'discoloration'),(6,'leakage, cracks')]:fq(u,n,155,'공개 FAQ는 release visual inspection 설명에서 '+term+'를 실제 검사 예로 열거한다. 해당 관찰항목을 검사한다는 명제에 맞는 직접 근거다.')
fq(u,7,163,'조제 당일 release/dispense하지 않은 CSP는 출고 직전 다시 시각검사하라는 인용 문구가 있다. 이미 dispense가 끝나 pickup만 기다리는 사례와는 FAQ164에서 구별한다.')
k(u,8,4,'Policy2024-04 remaining-stock paragraph','segregate','결함이 있는 remaining stock을 찾아 격리하고 dispense하지 못하게 하는 Board 정책을 확인했다.')
k(u,9,8,'MGL112§39D(e)','rectifies','Board와 함께 오류를 바로잡을 corrective action plan을 개발·시행하도록 하므로 결함 발견을 원인·시정 검토와 연결하는 일반 명제는 근거가 있다.')
k(u,10,4,'Policy2024-04 recall and recipient-contact paragraphs','recall','결함이 있거나 그럴 이유가 있는 조제약을 회수하고 이미 교부된 수령자에게 즉시 연락하는 경로를 명시한다.')
k(u,11,4,'Policy2024-04 reporting and SADE paragraphs','seven days','교부된 defective CSP/complex nonsterile의7일 보고와 SADE caused/suspected시 즉시 보고를 별도로 둔다. 모든 결함에 같은 보고기한을 붙이지 않는다.')
for n,reason in [(12,'Board는 sterility testing이 필요한 CSP를 negative result 전에 dispense하지 못한다는 현재 정책 입장을 명시한다. Draft17.17 인용을 promulgated regulation이라고 바꾸지 않았다.'),(13,'이 정책의 명시적 negative-before-dispense 입장 때문에 과거 inspection form의 결과 전 출고 후 회수조건을 현재 MA의 일반 선교부 허가로 읽을 수 없다.')]:k(u,n,5,'Policy2025-01 opening Board position','negative sterility test results',reason)
k(u,14,5,'Policy2025-01 opening / II.A','noninferior','USP71 또는 검증된 noninferior alternative를 명시하고 II.A에서 equivalent or superior validation을 요구한다.')
k(u,15,5,'Policy2025-01 II.C.1','each','각 CSP formulation별로 시험 간섭·억제를 배제하는 method-suitability challenge를 확인하도록 명시한다.')
k(u,16,5,'Policy2025-01 II.C.2','specific concentration','약국의 실제 sample, 구체농도, 같은 API CAS를 사용한 suitability인지 확인하도록 명시한다.')
k(u,17,5,'Policy2025-01 II.C','bacteria, yeast, and mold','낮은 수준의 bacteria 회수를 입증해야 한다는 challenge 조건을 직접 확인했다.')
k(u,18,5,'Policy2025-01 II.C','bacteria, yeast, and mold','같은 조항은 yeast와 mold도 별도로 열거하므로 세균만 검출하는 검사로 대체하지 않는다.')
k(u,19,5,'Policy2025-01 II.C.1','false','formulation의 inhibit/interfere 및 false positive/negative 위험을 suitability testing에서 배제해야 한다.')
k(u,20,5,'Policy2025-01 II.A/II.C','fully validated','검사법의 완전한 validation과 formulation별 suitability를 약국이 확인해야 하므로 vendor의 rapid 명칭만으로는 요건을 충족하지 못한다.')
k(u,21,5,'Policy2025-01 II.C.4','Method suitability must be repeated','CSP formulation 또는 관련 product composition이 바뀌면 suitability를 반복하도록 명시한다.')
k(u,22,5,'Policy2025-01 I.D','limitations','anaerobic microbes 미검출, 실패샘플 회수·동정, 배지·배양조건 등 선택 방법의 한계를 질문별로 검토하도록 한다.')
k(u,23,5,'Policy2025-01 III.C','sign','MOR 또는 designated PIC가 받은 method suitability 결과를 검토하고 서명·날짜를 남기는 조항을 확인했다.')
u='w4-b-24'
sb(u,list(range(1,9)),'현재 full <797> CSP labeling 조항의 해당 필드·해당조건을 직접 확보하지 못했다. 503B 법정 label 또는 MA compounded 표시 규칙을 모든 pharmacy CSP 표시목록의 대체 근거로 쓰지 않는다.')
k(u,9,6,'MGL94C§21 compounded preparation label','compounded','sterile/nonsterile compounded preparation이라는 표시를 container label에 넣도록 하는 주법 문구를 직접 확인했다.')
sb(u,10,'MGL94C§21은 특정 sterile/complex licensee 전화표시에 staffed56-hour와 같은 기관내 예외를 둔다. 원 명제의 모든 CSP label pharmacy contact라는 넓은 범위를 full <797> 정본에서 확인하지 못했다.')
k(u,11,7,'FDA Understanding Risks of Compounded Drugs','not FDA-approved','FDA는 compounded drugs가 FDA-approved가 아니라고 명시한다. sterile compounded 표시만으로 제품승인 주장이 되지 않는다.')
sb(u,12,'batch-linked 모든 complaint/AE/OOS 조사 범위와 세부기록을 현행 full <797>에서 직접 확인하지 못했다. MA defective 보고규칙만으로 모든 조사범주를 동일화하지 않는다.')
sb(u,13,'MGL112§39D(a)는 lot/expiry/BUD, 환자 처방 및 담당자 추적을 명시하지만 모든 components 추적 의무까지 직접 적시하지 않는다. full <797> compounding record 원문을 확보하지 못해 이 더 넓은 범위는 보류한다.')
k(u,14,8,'MGL112§39D(a)','individual, pharmacy technician','trace가 약국 또는 individual technician/automated device와 처방에 연결되도록 하는 accountability 조항을 확인했다.')
k(u,15,8,'MGL112§39D(a)','patient','lot·expiry·BUD 기록을 patient prescription 및 조제 주체와 연결하는 accountability 요구가 있다.')
sb(u,16,'complaint/AE/OOS investigation을 environment와 연결하는 정확한 현행 USP 조항을 직접 확보하지 못했다. 일반 CQI 의무만으로 environmental linkage의 전 범위를 확정하지 않는다.')
fq(u,17,162,'공개 FAQ의 OOS release-test 실패대응 절차는 다른 lots가 영향받았는지 investigate하고 필요하면 recall하라고 직접 명시한다. MA 선교부 금지 정책은 이 실패조사의 필요성을 없애지 않는다.')
sb(u,18,'실패 후 좋은 재검사 한 번으로 원래 failure를 삭제하지 못한다는 정확한 현행 <797>/OOS 조항을 직접 확보하지 못했다. 일반 조사·로그 의무로 이 특정 재시험 원칙을 대체하지 않는다.')
k(u,19,4,'Policy2024-04 log and destruction/return records paragraphs','10 years','defective preparation log와 파기/반품 문서를 최소10년 보존하도록 명시한다.')
k(u,20,4,'Policy2024-04 defective log paragraph','log','10년 규칙의 주어는 defective preparation log이므로 모든 정상 compounding record에 그대로 일반화할 근거가 아니다.')
k(u,21,8,'MGL112§39D(e)','10 years','defective log에 별도10년을 직접 정한 조항이므로 일반 처방 보존기간을 이유로 이를2년으로 줄일 수 없다.')
k(u,22,9,'MGL94C§23(e)','two years','일반 처방의 최소2년 조항을 직접 확인했고 defective10년 조항과 적용 기록을 구별했다.')
k(u,23,8,'MGL112§39D(a)','accountability','sterile/complex nonsterile accountability documentation을 별도로 요구하므로 일반 처방 원본과 동일 종류의 기록만 있다는 해석은 맞지 않는다.')
k(u,24,10,'247CMR15.04(2)','two years','CQI quality-related-event 기록은 최소2년이라는 별도 규칙이다. defective log10년과 기록·보존기간을 합치지 않았다.')
u='w5-a-12'
for n,reason in {1:'정책 첫 단락은 applicable temperature에서 full duration of infusion 동안 stability를 유지하도록 직접 요구한다.',2:'같은 정책은 entire infusion 동안 약물끼리 및 pump와의 compatibility를 직접 요구한다.',3:'due-diligence 항목에 stability/potency through entire infusion time를 별도로 명시한다.',4:'consider 항목에 all drugs in CSP 사이 physical compatibility를 명시한다.',5:'같은 항목은 chemical compatibility도 명시하여 물리적 외관만의 판단과 구별한다.',6:'특정 pump와 CSP의 compatibility가 별도 검토요소로 명시되어 다른 pump 자료를 자동 전용할 수 없다.',7:'temperature range 예시에 normal body temperature를 직접 든다.',8:'temperature range 예시에 fever를 직접 든다.',9:'extended infusion 사용 근거의 첫 경로는 drugs FDA-approved for such use이다. 단순히 성분이 승인됐다는 것과 다르다.',10:'두 번째 경로는 relevant and reliable sources에서 얻은 documentation이다.',11:'세 번째 경로는 해당 사용을 뒷받침하는 direct testing이다.',12:'실제 보관 온도와 infusion 전체기간에 관한 검토를 명시하므로 실온 용기 자료만으로 실제 체온 pump 내 사용을 자동 승인할 수 없다.',14:'정책은 administration이797 scope 밖이라고 인정하면서도39G/39I의 약국 출고 후 품질 유지 책임을 명시한다.',15:'마지막 단락은 각 CSP 처방을 evidence-based practice에 맞춰 평가하고 compounding/dispensing의 적정성을 보장하도록 요구한다.'}.items():k(u,n,11,'Policy2024-02 full policy','full duration',reason)
fq(u,13,166,'BUD와 administration/hang time을 다른 개념으로 정의하며 <797>이 infusion administration 시간을 다루지 않는다고 직접 설명한다.')
k(u,16,9,'MGL94C§23(d)','implantable infusion pump','주법의90-day supply 허용범주에 implantable infusion pump가 포함되지만 이는 조제약이 실제 체온 pump에서 안정한 기간이라는 품질검토와 다른 규칙이다.')
u='w5-a-11'
k(u,[1,2],13,'MA Board draft regulations list, 247CMR17/18','Draft','공식 페이지가 해당17/18을 draft로 분류한다. 목록·Board 검토 사실은 그 자체로 final promulgation이나 시행일을 입증하지 않는다.')
k(u,3,14,'Sterile inspection template introductory footnote','DRAFT','공식 검사 template 자체의 DRAFT247CMR17 인용을 확인했다. 이 문서가 현행 법령의 promulgation 증명은 아니다.')
k(u,4,15,'Media Fill Advisory I/II.B','2008','2022년 채택 문서는 purpose에서2008 USP, testing conditions에서2021 revised draft를 인용한다. 그 버전 출처를 현행 정본이라고 바꾸지 않는다.')
fq(u,5,8,'공개 FAQ는2022 revision의 official date를2023-11-01로 명시한다. 2008/2021draft를 인용한2022 advisory와 같은 버전의 Category 체계라고 볼 수 없다.')
fq(u,6,57,'initial garbing 세 번 성공은 succession이어야 하고 실패하면 처음부터 다시 세 번이라는 조건을 직접 설명한다.')
fq(u,7,50,'initial garbing의 세 가지 별도평가와 aseptic manipulation/media-fill의 initial1/subsequent1 평가를 구별하여 설명한다.')
fq(u,8,47,'직접 조제하지 않는 oversight personnel의 core/garbing/aseptic 평가를 at least12months로 다루므로 실제 compounder의 평가주기를 자동 적용하는 구조가 아니다.')
sb(u,9,'USP825 공식 FAQ 링크는403이고 현행 정본 전문을 확보하지 못했다. MA13의 일부 핵약국 규칙을 읽었다는 사실만으로 모든 preparation-specific825 예외까지 인증할 수 없다.')
sb(u,10,'세부6/3개월 competency와 전체 BUD matrix의 현행 정본/모든 예외를 확보하지 못했다. 일반적인 장간 교차참조 필요성은 인정하나 해당 세부요건 전체 법규인증은 보류한다.')
u='w4-c-1'
k(u,1,16,'NIOSH2025-103 introduction/HD definition','exposure','NIOSH의 분류는 취급 중 occupational exposure의 암·생식·장기독성 등의 위해특성을 다룬다. DEA abuse scheduling의 정의가 아니다.')
k(u,2,53,'DEA Drug Scheduling opening','abuse or dependency potential','DEA는 acceptable medical use와 abuse/dependency potential로 schedules를 설명한다. NIOSH의 노출독성 분류와 판단축이 다르다.')
k(u,3,54,'21CFR1308.14(c)(13)','Clonazepam','Clonazepam은 현행 ScheduleIV 항목이고 독립 회수한 NIOSH2024 Table2에도 등재되어 실제로 두 체계가 겹치는 예가 있다.')
k(u,4,16,'NIOSH2025-103 HD identification definition','hazardous','NIOSH의 HD 식별조건은 MSHI·발암·생식독성 등의 특성으로 정하며 연방 schedule 등재를 전제하지 않는다. 비규제약이라는 사실만으로 HD를 부정할 수 없다.')
k(u,5,47,'MGL112§39G sterile quality/current USP','quality','주법은 sterile quality 유지와 current USP all chapters 준수를 함께 요구한다. 여기서는 준비물 품질·오염방지라는795/797 일반 역할만 확인하며 모든 기술조항을 인증하지 않는다.')
sb(u,6,'800의 patients/healthcare personnel/environment 세 대상을 모두 명시하는 현재 full chapter를 확보하지 못했다. NIOSH worker guideline과 MA advisory의 일부 인용만으로 정본의 전체 scope 문구를 인증하지 않는다.')
fq(u,7,4,'sterile compounding 대상에 모든 작업장·personnel을 포함하고 sterile HD에는 추가800준수를 요구한다. HD라는 이유로797의 무균제품 보호가 사라지지 않는다.')
k(u,8,17,'USP800 MA Advisory containment paragraph','negative pressure','HD compounding에 적격 C-PEC 및 negative-pressure room을 드는 명시적 containment 지침을 확인했다. 무균제품 보호 외 작업자 노출통제가 함께 필요하다.')
u='w4-c-2'
k(u,1,18,'CDC NIOSH2024 publication metadata','2025-103','공식 CDC 발행페이지에 publication number2025-103과2024 list 제목을 함께 명시한다. 숫자의 연도표시를 목록 제목과 혼동하지 않았다.')
k(u,2,18,'CDC NIOSH2024 opening','2016','공식 발행페이지는2024 publication이2016 list를 supersede한다고 직접 설명한다.')
k(u,3,16,'NIOSH2025-103 Organization of the List','number of tables to two','현행2024 PDF가 two tables로 재편한 구조를 직접 설명한다.')
k(u,4,16,'NIOSH2025-103 Organization of the List','number of tables to two','현재 table구조 재편 때문에2016의 세 table 번호를 그대로 동일범주라고 대응시키는 것은 맞지 않는다. 실제2024 분류문구를 읽어야 한다.')
k(u,5,18,'CDC July17,2025 MSHI additions','July 17, 2025','공식 CDC 페이지는 발간 후 July17,2025의 Datroway/treosulfan/Emrelis MSHI 추가사항을 별도로 게시한다. PDF 발행시점만 보고 끝내지 않는다.')
k(u,6,17,'MA USP800 Advisory Identify HD','Identify all stocked','stocked HD를 파악하고 current NIOSH와 목록 외 HD를 포함한 시설목록을 만들도록 명시한다.')
k(u,7,17,'MA USP800 Advisory Identify HD / Assess Risk','new drugs','새 약을 평가할 procedure와 AOR의 dosage form/manipulation 요소를 함께 둔다. 새로운 약·제형은 기존 목록을 그대로 적용하기 전에 평가해야 한다.')
k(u,8,17,'MA USP800 Advisory Identify HD','every 12 months','시설 HD 목록을 적어도12개월마다 review하도록 직접 적시한다.')
k(u,9,17,'MA USP800 Advisory documented program / assessment','Documentation of the review','documented formal HD program과 review documentation을 요구한다. 목록의 정기 검토도 문서화된 프로그램으로 확인해야 한다.')
k(u,10,17,'MA USP800 Advisory Identify HD','may not be on','NIOSH list에 없을 수도 있는 다른 HD를 identify하라고 직접 명시한다.')
k(u,11,16,'NIOSH2025-103 scope and MSHI','special handling','MSHI 및 신약의 유해특성을 시설별로 평가하는 체계이며 목록 미등재가 안전성 보증은 아니다. 추가 공지18도 이런 한계를 실제로 보여 준다.')
for n,term in [(12,'Dosage form'),(13,'Packaging'),(14,'Manipulation'),(15,'Manipulation')]:k(u,n,17,'MA USP800 Advisory Assess Risk',term,{12:'AOR 필수요소에 dosage form을 직접 열거한다.',13:'AOR 필수요소에 packaging을 직접 열거한다.',14:'tablet counting 예와 crushing compounding full-containment 예를 구별하므로 같은 약이라도 작업별 노출평가가 달라진다.',15:'splitting·reconstituting 등 manipulation과 exposure risk를 평가요소로 명시한다. 먼지·에어로졸 발생 작업을 단순 intact dispensing과 같게 보지 않는다.'}[n])
for n,anchor,reason in [(16,'Spill control','formal program에 spill control/remediation SOP를 포함하도록 하므로 유출처리는 노출평가에서 빠질 수 없다.'),(17,'cleaning','formal program에 deactivation/decontamination/cleaning을 포함하여 표면청소도 HD 취급위험의 일부로 다룬다.'),(18,'Disposal / Waste','PPE·containment 검토의 대상 영역으로 Disposal/Waste Management를 직접 열거한다.'),(19,'receipt','독립 취급 전에 모든 직원이 job function별 training을 받도록 하며 receipt가 실제 예로 포함된다.'),(20,'job functions','all employees 및 역할별 교육 원칙과 cleaning/waste SOP를 함께 명시하므로 청소·폐기 담당자도 자기 역할의 보호절차 교육 대상이다.'),(21,'documented','운송을 HD 취급영역으로 열거하고 all employees 역할별 교육 및 initial/annual competency 문서화를 요구하므로 운송 담당자의 적용 교육·평가도 문서화 대상이다.')]:k(u,n,17,'MA USP800 Advisory program/training',anchor,reason)
u='w4-c-3'
for n,anchor,reason in [(1,'For other identified HD','antineoplastic manipulation/API compounding 외 HD에 AOR를 사용할 수 있다고 명시한다. 이를 모든HD 일반면제로 확대하지 않는다.'),(2,'Reproductive risk only','reproductive-risk-only를 HD risk category로 열거하고 other identified HD의 AOR 경로와 연결한다.'),(3,'Dosage form','AOR는 HD 종류와 dosage form·포장·조작을 평가하므로 finished dosage form별 적격성을 판단해야 한다.'),(4,'Documentation of the alternate','대체 containment/work practices의 documentation을 필수요소로 직접 명시한다.'),(5,'Type of HD','AOR 최소요소에 type of HD를 직접 명시한다.'),(6,'Dosage form','AOR 최소요소에 dosage form을 직접 명시한다.'),(7,'Risk of exposure','AOR 최소요소에 risk of exposure를 직접 명시한다.'),(8,'Packaging','AOR 최소요소에 packaging을 직접 명시한다.'),(9,'Manipulation','AOR 최소요소에 manipulation을 직접 명시한다.'),(10,'every 12 months','AOR는 적어도12개월마다 review하도록 명시한다.'),(11,'manipulating antineoplastic','antineoplastic manipulation은 모든 containment 전략을 적용하는 별도 시나리오다.'),(12,'hazardous drug active','NIOSH HD API compounding은 full-containment 시나리오이므로 AOR로 일반 면제할 수 없다.'),(13,'crushing tablets','crushed tablet로 조제하는 경우를 API compounding의 full-containment 범위에 직접 넣는다.'),(14,'opening capsules','opened capsule 사용도 full-containment 시나리오에 직접 포함한다.'),(15,'clonazepam','clonazepam crushing suspension의 C-PEC/negative pressure 예시 때문에 intact counting AOR를 그대로 분쇄조제에 전용할 수 없다.'),(16,'Manipulation','작업별 manipulation과 exposure risk가 필수 평가요소이므로 intact에서 분쇄로 바뀌면 같은 조건으로 취급할 수 없다.')]:k(u,n,17,'MA USP800 Advisory pp1–2 containment/AOR',anchor,reason)
k(u,17,48,'MGL112§39H complex nonsterile additional license','license','실제 complex nonsterile compounding에는 별도면허와 current USP 준수가 필요하고 sterile에는39G가 적용된다. 작업 변경을 AOR만으로 면허권한 확대라고 볼 수 없다.')
u='w4-c-4'
k(u,1,48,'MGL112§39H (with39G sterile counterpart)','license','complex nonsterile 조제의 추가 면허요건을 직접 확인했다. sterile 조제에는 별도로39G/39I가 있으므로 실제 작업형태의 권한을 판단해야 한다.')
k(u,2,17,'MA USP800 Advisory p1 containment example','negative pressure','HD suspension compounding 예에 C-PEC가 negative-pressure room에 위치해야 한다고 명시한다.')
k(u,3,17,'MA USP800 Advisory p1 containment example','primary engineering control','HD 조제의 full containment에 적절한 primary engineering control, 예를 들어 powder hood를 명시한다.')
k(u,4,52,'NIOSH2023-130 glossary, containment primary engineering control','Containment-primary','C-PEC의 목적은 worker/environment exposure를 줄이는 ventilated control이다. 제품보호 기능만 있는 일반 LAFW/CAI를 노출 containment로 자동 인정할 근거가 없다.')
k(u,5,17,'MA USP800 Advisory p1 full containment','containment','HD compounding에 별도 full containment를 적용하므로 제품의 무균성만 만족했다고 노출통제가 충족되는 것은 아니다.')
k(u,6,52,'NIOSH2023-130 glossary C-PEC','Containment-primary','glossary는 C-PEC를 HD handling의 worker/environment 노출을 최소화하는 ventilated device로 정의한다.')
k(u,7,52,'NIOSH2023-130 glossary C-SEC','Containment-secondary','C-SEC는 C-PEC가 있는 room이며 지정 containment 설계를 갖는다고 정의한다. primary 장비 자체와 같은 것이 아니다.')
sb(u,[8,9,10,11],'현행 full <800>의 sterile/nonsterile C-PEC·C-SEC, external venting, room classification 및 ventilation 조합별 세부조건을 직접 확보하지 못했다. NIOSH glossary와 MA 공개 checklist의 일부만으로 실제 설계의 현행 적합성을 인증하지 않는다.')
for n,anchor,reason in [(12,'qualified and trained','MA advisory는 designated person이 qualified and trained이어야 한다고 직접 명시한다.'),(13,'developing and implementing procedures','지정인이 procedures 개발·시행을 책임지도록 직접 정한다.'),(14,'overseeing compliance','지정인의 overseeing compliance 역할을 직접 명시한다.'),(17,'licensed','지정인이 반드시 licensed pharmacy individual일 필요는 없다고 직접 명시한다.'),(18,'premises','지정인이 반드시 premises에 있어야 하는 것은 아니라고 직접 명시한다.')]:k(u,n,17,'MA USP800 Advisory p1 designated person',anchor,reason)
sb(u,15,'MA advisory는 지정인의 procedure/compliance 책임만 직접 풀어 쓰고 other requirements는 full800에 맡긴다. 지정인에게 competency 관리 전 범위를 부여한 현행800 조항을 직접 확보하지 못했다.')
sb(u,16,'지정인의 environmental monitoring 및 결과조치 감독을 명시한 현재 full800 원문을 확보하지 못했다. generic compliance 문구로 이 구체적 역할을 입증하지 않는다.')
sb(u,19,'MA nonsterile795 designated-pharmacist의 구체 자격·상주조건에 관한 현재 primary 원문을 이번 회수에서 확보하지 못했다. HD advisory의 지정인 예외만으로 별도795 조건의 전 범위를 인증하지 않는다.')
k(u,20,20,'Policy2025-02 MOR definition','Manager of Record','MOR는 MA pharmacy의 법규·규정준수와 운영에 대한 책임을 지는 정의다. HD 지정인 역할을 두어도 MOR의 주법상 책임이 소멸하지 않는다.')
u='w4-c-5'
sb(u,[1,4,5,6,7,8],'현재 full800/797의 해당 chemotherapy glove 성능표준·sterile HD garbing의 정확한 의무와 예외를 확보하지 못했다. NIOSH의 권고·위험별 예시를 정본의 일률적 sterile 요건으로 바꾸지 않는다.')
k(u,2,52,'NIOSH2023-130 §6.4 Gloves suggested glove practices','Use powder-free gloves','powder가 HD를 흡착하고 작업구역을 오염시킬 수 있으므로 powder-free gloves 사용을 명시한다. NIOSH 지침의 성격으로 판정했고800 전 조항을 인증한 것은 아니다.')
k(u,3,52,'NIOSH2023-130 §6.4 Gloves suggested glove practices','Inspect gloves for defects','사용 전 gloves 결함검사와 손상/약물접촉 시 교체·폐기를 직접 권고한다.')
k(u,9,52,'NIOSH2023-130 §6.4 Gloves test information','permeation resistance','glove 소재·두께만으로 보호성능이 결정되지 않고 실제 HD에 대한 제조사 permeation resistance test정보로 선택해야 한다고 설명한다. nitrile 명칭만의 증명이 아니다.')
k(u,10,52,'NIOSH2023-130 §6.4 Gowns protective gowns','Gowns','해당 gown을 예상 exposure와 보호성능에 맞게 선택하는 위험기반 지침을 확인했다. 모든 작업에 동일 제품을 승인하는 판정이 아니다.')
k(u,11,52,'NIOSH2023-130 §6.4 Eye and Face Protection eye and face protection','Eye','splash 등 task exposure에 따른 eye/face 보호의 선택을 설명한다. 단순 가운으로 눈·얼굴 보호가 대체되지 않는다.')
k(u,12,52,'NIOSH2023-130 §6.4 Respiratory Protection respiratory protection','Selection of respirators','respirator 선택은 specific tasks and drugs에 근거해야 한다고 명시한다. N95는 gas/vapor를 보호하지 않는다는 한계도 직접 확인했다.')
k(u,13,55,'29CFR1910.134(k)(1)/(k)(3)','training','필수 respirator 사용자에게 사용 전 효과적 교육과 정기 재교육을 요구하는 OSHA 문구를 확인했다.')
k(u,14,55,'29CFR1910.134(f)','tight-fitting facepiece','tight-fitting facepiece의 초기·변경·정기 fit-test 조건을 확인했다. 명제의 해당 fit testing으로 읽으며 loose-fitting PAPR까지 같은 검사를 요구한다고 확대하지 않는다.')
k(u,15,52,'NIOSH2023-130 §6.4 Respiratory Protection','Loose-fitting surgical','loose-fitting surgical mask는 respirator가 아니며 respiratory protection이 필요한 HD 작업에서 사용하지 말라고 직접 설명한다.')
k(u,16,17,'MA USP800 Advisory Training','Before independently','all employees가 HD를 독립 취급하기 전에 job function에 맞는 교육을 받아야 한다고 직접 정한다.')
sb(u,[17,18,19],'새HD·새장비·중요SOP변경 각각의 도입 전 추가교육이라는 정확한 현행 full800 timing조항을 확보하지 못했다. MA advisory의 최초/연간 교육과 NIOSH 신규업무 지침만으로 이 세 가지 사전조건을 모두 동일하게 인증하지 않는다.')
k(u,20,17,'MA USP800 Advisory Training','every 12','competency는 initially 및 적어도12개월마다 reassess하라고 직접 명시한다.')
k(u,21,17,'MA USP800 Advisory Training','documented','같은 competency assessment 문구가 documented를 명시하여 평가의 실제 기록을 요구한다.')
sb(u,[22,23],'sterile aseptic competency의 정확한6개월/3개월 조건·category·평가종류를 현행 full797에서 직접 확보하지 못했다. HD annual 평가 규칙으로 이 숫자를 입증하지 않는다.')
fq(u,24,4,'sterile HD에는797 외800도 준수해야 한다고 하므로 역할별로 두 competence 체계가 동시에 적용될 수 있다. 이 판정은 별도22/23의6/3개월 숫자까지 확인했다는 뜻은 아니다.')
k(u,25,17,'MA USP800 Advisory Storage and Handling','Tablet or capsule forms','antineoplastic tablet를 automated counting/packaging machine에 넣어서는 안 된다고 직접 명시한다.')
k(u,26,17,'MA USP800 Advisory Storage and Handling','Tablet or capsule forms','같은 금지의 대상은 capsule도 포함한다.')
k(u,27,17,'MA USP800 Advisory Storage and Handling','not recommended','other HD의 장비 사용은 not recommended라고 하므로 antineoplastic must-not 금지와 법적 표현을 구별한다.')
k(u,28,52,'NIOSH2023-130 §6.3 administrative controls automated machines','automated','자동장비의 분쇄·마찰에 따른 powder 노출가능성을 시설별 평가하는 지침이 있다. 최종 환자포장이 intact라는 사실만으로 공용 장비의 잔류오염 노출이 사라지지 않는다.')
u='w4-c-6'
k(u,1,52,'NIOSH2023-130 glossary Deactivation','Deactivation','deactivation은 약물을 inactive/inert하게 바꾸는 처리로 정의되어 단순 표면청소와 구별된다.')
k(u,2,52,'NIOSH2023-130 glossary Decontamination','Decontamination','decontamination은 표면의 HD residue 제거로 정의되어 화학적 불활화와 다른 목적이다.')
fq(u,3,119,'cleaning을 organic/inorganic substances를 물·detergent 등으로 물리적으로 제거하는 과정으로 직접 정의한다.')
fq(u,4,119,'disinfecting을 표면·물체의 fungi/viruses/bacteria를 파괴하는 과정으로 설명하므로 미생물 통제 목적의 별도 처리다.')
fq(u,5,120,'sterile IPA는 one-step disinfectant cleaner가 아니고 sanitizing agent라고 직접 구별한다. 이것만 한 번 닦았다는 사실이 화학적HD 불활화·잔류제거·세정·소독 전 목적의 충족을 증명하지 않는다.')
sb(u,list(range(6,14))+list(range(15,20)),'현행 full800의 DDCD agent/농도/contact-time/순서/장비적합성/문서화 또는 damaged-package 후처리의 해당 구체조항을 직접 확보하지 못했다. NIOSH 일부 권고와 MA의 SOP 목록을 이 명제의 정확한 전체 수행요건으로 대체하지 않는다.')
k(u,14,52,'NIOSH2023-130 §8.2 receiving damaged containers','Open damaged','손상용기는 fume hood/Class1BSC/HEPA-filtered enclosure 안에서 열도록 하는 직접 지침을 확인했다. 일반 counter에서 무방비 개봉하는 경로와 구별한다.')
u='w4-c-7'
sb(u,list(range(1,10))+[11,12],'현재 full800의 spill SOP 구성·kit용량·접근표시·의복처리·즉시조치·기록·후속보고를 망라한 해당 조항을 직접 확보하지 못했다. NIOSH §7.2의 일부 권고를 각 세부요건 전체가 현행USP에서 확인됐다는 증명으로 쓰지 않는다.')
k(u,10,52,'NIOSH2023-130 §7.2 spill control','train workers','HD spill 대응인력의 사전 교육·대응절차 준비를 직접 설명한다. 무교육 직원에게 cleanup을 맡기는 지침이 아니다.')
k(u,13,52,'NIOSH2023-130 §7.2/§8.2 spills','spill','위험에 맞는 PPE와 trained cleanup 절차를 설명하므로 능력을 넘는 사건을 비적격 직원이 맨손 처리하는 것은 그 보호절차에 맞지 않는다.')
k(u,14,23,'247CMR13.05(1)/(9)','Nuclear Regulatory Commission','핵약국에 NRC 및 applicable state/federal 규칙을 추가 적용하고 unused radioactive return/disposal도 NRC 규칙에 따르게 한다. 일반HD waste와 동일체계가 아니다.')
k(u,15,52,'NIOSH2023-130 §7.1 Waste disposal','state','HD 폐기는 시설 폐기물 분류와 local/state/federal 규칙 및 적법한 폐기업체 경로를 따르도록 설명한다. 모든 RCRA 코드·허가를 검증했다는 뜻은 아니다.')
k(u,16,57,'21CFR1317.05/1317.15 disposal by registrants','reverse distributor','CS 폐기는 별도의DEA 등록업체·전달·보안·파기 조건이 있다. 일반HD 폐기계약만으로 이 의무가 충족되지 않는다.')
k(u,17,52,'NIOSH2023-130 §7.1 waste categories','hazardous waste','HD관련 hazardous/tracechemotherapy/nonhazardouspharmaceutical 등 폐기분류·경로를 구별한다. 이를 모든 biological waste와 같은 것으로 처리할 근거가 없다.')
k(u,18,57,'21CFR1317.15(a) (with NIOSH§7.1 waste authority)','registered','DEA reverse-distributor 등록은 controlled substance의 reverse distribution 권한이다. HD의 RCRA/기타 폐기수령 허가까지 이 등록 하나로 증명하지 않는다.')
k(u,19,23,'247CMR13.05(9)/(1)','disposal','radioactive return/disposal은 별도NRC/applicable radiation 규칙에 따르므로 DEA reverse-distributor라는 명칭만으로 수령권한을 확정할 수 없다.')
k(u,20,52,'NIOSH2023-130 §8.2 Transportation within facility','risk of breakage','운송용기는 breakage 위험을 최소화하도록 선택하고 doublebag/sealedcontainer를 사용하라는 직접 지침이다. 절대0위험 보증이 아니라 예방통제로 읽는다.')
k(u,21,52,'NIOSH2023-130 §8.2 Transportation within facility','risk of breakage','동일 지침은 leakage 위험의 최소화와 sealed containment를 직접 요구해 운송 중 HD 노출방지 목적을 뒷받침한다.')
sb(u,22,'모든 외부배송 HD에 storage/disposal instructions를 동봉해야 한다는 full800 정확조항을 직접 확보하지 못했다. 247CMR9.18의 필요한 환자상담 정보와 법정 shipment enclosure를 같은 의무로 보지 않는다.')
k(u,23,58,'247CMR9.18(4)/(5)(c)','preparation','새·변경처방 상담 및 약사의 판단상 필요한 preparation/use 정보 제공 조항을 확인했다. 필요한 HD safehandling 정보로 제한하여 판단한다.')
k(u,24,58,'247CMR9.18(5)(f)','storage','필요한 patient counseling 정보에 proper storage를 직접 열거한다. 모든 제품에 같은 보관정보가 적용되는 것은 아니다.')
k(u,25,58,'247CMR9.18(5)(f)','disposal','같은 조항은 proper disposal을 직접 열거한다. 환자별 필요정보 제공과 시설의 폐기허가는 구별한다.')
u='w4-c-8'
k(u,1,25,'21USC353a(a) introductory language','State','State-licensed pharmacy 또는 Federal facility의 licensed pharmacist 경로를 직접 명시한다. 모든 시설·무면허인을 허용하는 조항이 아니다.')
k(u,2,25,'21USC353a(a) introductory language','licensed physician','licensed physician 조제 경로가 pharmacists 경로와 별도로 직접 열거되어 있다.')
k(u,3,27,'21USC353b(a) opening','direct supervision','등록을 선택한 outsourcing facility에서 licensed pharmacist가 조제하거나 직접 감독한 약을 조건부 대상으로 명시한다.')
k(u,4,25,'21USC353a(a)(1)','identified individual patient','valid prescription order를 토대로 identified individual patient에게 조제하는 일반경로를 직접 명시한다.')
k(u,5,25,'21USC353a(a)(2)','limited quantities','anticipatory compounding은 limited quantities와 valid prescription history 및 established relationship 요건으로 제한한다. 무제한office stock 허용이 아니다.')
k(u,6,27,'21USC353b(d)(4)(C)','prescriptions','outsourcing facility는 identified individual patients의 prescriptions를 얻을 수도 있고 안 얻을 수도 있다고 직접 정한다. MA 별도등록은 별개다.')
k(u,7,27,'21USC353b(a)(8)','prescription executed','resale 제한 예외의 patient dispensing은353(b)(1)에 맞게 작성된 prescription을 직접 전제로 한다.')
k(u,8,25,'21USC353a(a) exemptions','351(a)(2)(B)','모든503A 조건을 충족한 drug에 한해351(a)(2)(B)의cGMP 면제가 적용된다. pharmacy라는 이름만의 자동면제가 아니다.')
k(u,9,28,'FDA FDCA503A/503B comparison cGMP','Current good manufacturing practice','FDA 공식 비교는503B에cGMP가 적용됨을 설명한다.503B(a)의 면제목록에도cGMP는 포함되지 않는다.')
k(u,10,27,'21USC353b(b)(1)/(d)(4)','electing','outsourcing facility가 되기 위한 별도 register 절차와 정의를 두므로503A pharmacy라고 자동등록되는 구조가 아니다.')
k(u,11,27,'21USC353b(b)(1)(A)','shall register','outsourcing facility가 되려면 등록하고 이후annual window에 계속 등록해야 한다고 명시한다.')
k(u,12,27,'21USC353b(a)(9)','fees owed','시설이 owed fees를 모두 납부해야 해당drug가503B 조건을 충족한다고 명시한다.')
k(u,13,27,'21USC353b(b)(2)/(b)(5)','Adverse event reporting','조제품 report(b2)와310.305에 따른 AEreport(b5)를 별도 등록시설 의무로 둔다.')
k(u,14,25,'21USC353a(a) conditional exemptions','355','조건 충족503A drug에는355의 premarket approval 조항 면제가 직접 있다. 이것은제품승인과 다르다.')
k(u,15,27,'21USC353b(a) conditional exemptions','355','각503B 조건 충족 시355 면제경로를 두므로 registration 자체의 approval이 아니라 조건부 예외다.')
k(u,16,7,'FDA Compounded drugs are not FDA-approved','not FDA-approved','FDA는 compounded drugs를 FDA-approved라고 하지 않는다. 시설등록을 개별약 승인으로 표현하면 안 된다.')
k(u,17,29,'21USC360eee(13)(B) product exclusions','353a','DSCSA product 정의에서353a 또는353b에 따라 적법하게 조제된 약의 제외를 직접 열거한다.503A라는 이름만으로 모든약이 자동제외되는 것은 아니다.')
k(u,18,27,'21USC353b(a) opening DSCSA582 exemption','360eee','각503B 조건 충족 시360eee-1(§582) 면제를 명시한다. 모든등록시설약의 자동면제와 다르다.')
k(u,19,35,'247CMR21.02/21.04','Massachusetts','MA는 FDA등록 증거 외 별도의 resident/nonresident 신청·등록절차를 요구한다. federal list만으로 MA 권한이 끝나지 않는다.')
k(u,20,47,'MGL112§39G state pharmacy/sterile licensure','license','MA retail sterile compounding에 별도license가 적용되고 complex nonsterile에는39H가 적용된다.503A 연방 조건부면제가 주면허를 없애지 않는다.')
k(u,21,27,'21USC353b(d)(4)(A)','one geographic location','outsourcing facility 정의는 one geographic location or address의 facility를 명시한다.')
k(u,22,27,'21USC353b(d)(4)(A)(i)','sterile drugs','같은 정의는 sterile drugs compounding에 종사하는 시설을 전제로 한다.')
k(u,23,27,'21USC353b(a) each condition','each of the following','연방 면제는 each following condition 충족이 전제이므로 시설등록 하나로 개별 조제약의 나머지조건까지 입증되지 않는다.')
k(u,24,27,'21USC353b(a)(11)/(d)(4)','only in accordance','compounding은 해당facility에서503B에 따라 수행되어야 한다. 다른 unit에서 만든 약에 등록시설 이름만 붙인 구조로 조건충족을 추정할 수 없다.')
u='w4-c-9'
for n,section,anchor,reason in [(1,'(a)(2)(A)(i)','clinical need','bulk clinical-need list 경로와 그 목록수립 절차를 법문이 직접 둔다.'),(2,'(a)(2)(A)(ii)','at the time of compounding','shortage 경로는 compounding 시점의 해당 drug shortage-list 등재를 요구한다.'),(3,'(a)(2)(A)(ii)','distribution, and dispensing','같은 법문은 distribution 시점도 직접 열거한다. 조제 시점에만 shortage였다는 사실로 충분하지 않다.'),(4,'(a)(2)(A)(ii)','distribution, and dispensing','dispensing 시점도 법문이 직접 요구한다. 목록에서 빠진 후에도 무기한 dispensing을 허용한다는 조항이 아니다.'),(5,'(a)(2)(B)','applicable monograph','bulk에 applicable monograph가 존재하면 각bulk가 이를 준수해야 한다고 명시한다.'),(6,'(a)(2)(C)','registered under section 360','bulk 제조자는 해당360 등록 establishment여야 하고 외국시설 등록경로도 직접 명시한다.'),(7,'(a)(2)(D)','certificate of analysis','각bulk가 valid certificate of analysis를 수반해야 한다고 직접 정한다.'),(8,'(a)(3)','other than bulk','nonbulk ingredient에도 존재하는 applicable compendial monograph 기준을 적용하도록 별도로 정한다.'),(9,'(a)(4)','unsafe or not effective','unsafe/ineffective 사유로 withdrawn/removed된 drug 목록에 없어야 한다고 직접 정한다.'),(10,'(a)(5)','essentially a copy','essentially-copy 제한을503B의 독립 조건으로 정한다. 등록시설이라는 사실로 없어지지 않는다.'),(11,'(a)(6)','demonstrable difficulties','difficult-to-compound 목록 비등재 또는 지정된 모든조건 준수의 두 경로를 직접 둔다.'),(12,'(a)(7)','prior to beginning','ETASU대상 source drug/bulk에 comparable controls를 조제 시작 전에 Secretary에게 입증하도록 직접 명시한다.'),(13,'(a) all conditions','each of the following','503B는 bulk/withdrawn/copy/difficulty/ETASU 등 각조건의 동시충족이 전제다. 승인제품 부재만의 무제한 허가가 아니다.'),(14,'(a)(8)','entity other than','조제한 outsourcing facility 외 entity가 판매·양도하지 못한다는 원칙을 직접 둔다.'),(15,'(a)(8)','prescription executed','353(b)(1)에 맞는 처방에 따른 dispensing은 이wholesaling 금지와 구별되는 명시적 예외다.'),(16,'(a)(8)','health care setting','healthcare setting에서 administration하는 것은 명시적 예외다. 일반wholesale resale와 같지 않다.')]:k(u,n,27,'21USC353b'+section,anchor,reason)
u='w4-c-10'
k(u,1,27,'21USC353b(b)(1)(A)','October 1','annual registration window의 시작을October1로 직접 명시한다.')
k(u,2,27,'21USC353b(b)(1)(A)','December 31','annual registration window의 끝을December31로 직접 명시한다.')
k(u,3,27,'21USC353b(b)(2)(A)','Upon initially registering','outsourcing productreport는 initially registering시에 제출하도록 직접 정한다.')
k(u,4,27,'21USC353b(b)(2)(A)','month of June','연간 June 중 한 번 productreport를 제출하도록 직접 정한다.')
k(u,5,27,'21USC353b(b)(2)(A)','month of December','연간 December 중 한 번 productreport를 제출하도록 직접 정한다.')
k(u,6,27,'21USC353b(b)(2)(A)(i)','previous 6-month','보고대상은 이전6개월간 facility가 조제한 drugs이며 그 기간을 직접 적시한다.')
k(u,7,27,'21USC353b(b)(1)/(b)(2)','Registration of outsourcing','annual facilityregistration과 initial/June/December productreport가 별도 paragraph·시점으로 정해져 있어 한 제출물로 합치지 않는다.')
labels=[(8,'(i)','This is a compounded drug','compounded drug임을 prominent하게 알리는 해당statement 또는 Secretary가 정한 comparable alternative를 직접 요구한다.'),(9,'(ii)','name, address, and phone','outsourcing facility name을label에 직접 요구한다.'),(10,'(ii)','name, address, and phone','outsourcing facility address를label에 직접 요구한다.'),(11,'(ii)','name, address, and phone','outsourcing facility phone number를label에 직접 요구한다.'),(12,'(iii)(I)','lot or batch','lot 또는batch number를label 항목으로 직접 열거한다.'),(13,'(iii)(II)','established name','drug established name을 직접 열거한다.'),(14,'(iii)(III)','dosage form and strength','dosage form과strength를 직접 열거한다.'),(15,'(iii)(IV)','quantity or volume','적절한 quantity 또는volume statement를 직접 열거한다.'),(16,'(iii)(V)','date that the drug','compounding date를 직접 열거한다.'),(17,'(iii)(VI)','expiration date','expiration date를 직접 열거한다. pharmacy797 BUD라는 다른 용어로 바꾸지 않는다.'),(18,'(iii)(VII)','storage and handling','storage와handling instructions를 직접 열거한다.'),(19,'(iii)(VIII)','if available','NDC는 available인 경우라는 조건이 직접 붙는다.'),(20,'(iii)(X)','active and inactive','active ingredients의 establishedname 및 각quantity/proportion 목록을 직접 요구한다.'),(21,'(iii)(X)','active and inactive','inactive ingredients도 같은 목록의 대상으로 직접 열거한다.'),(22,'(iii)(IX)','Not for resale','Not for resale statement를 직접 요구한다.'),(23,'(iii)(IX)','Office Use Only','identified patient의 처방에 따르지 않은 dispense/distribution에는 Office Use Only를 추가한다는 조건을 직접 명시한다.')]
for n,sec,anchor,reason in labels:k(u,n,27,'21USC353b(a)(10)(A)'+sec,anchor,reason)
k(u,24,27,'21USC353b(a)(10)(B)(ii)','1–800–FDA','개별unit를 꺼내는container에 MedWatch web 및FDA telephone 등 법정AEreporting 정보를 추가하도록 직접 정한다.')
k(u,25,27,'21USC353b(a)(10)(B)(iii)','directions for use','container의 directions for use에 필요한 dosage/administration을 포함하도록 직접 정한다.')
k(u,26,27,'21USC353b(a)(10)(B)(i)','not space on the label','ingredient목록 label공간이 없을 때 지정container에 그 정보를 표시하는 명시적 경로가 있다.')
k(u,27,27,'21USC353b(a)(10)(A)(iii)(VI)','expiration date','503B 법문은expiration date라고 적고 MA39D는compounding BUD를 별도로 정의한다. 출처를 읽지 않고두 용어·적용체계를 같다고 통일하지 않는다.')
k(u,28,27,'21USC353b(a)(10) applicability','Labeling of drugs','이label목록은503B 조건 중하나이다. 모든 pharmacy CSP의797 labeling목록으로 자동확대하지 않고 해당제도부터 확인해야 한다.')
u='w4-c-11'
k(u,1,27,'21USC353b(b)(5)','310.305','503B시설에310.305 adverse-event reporting을 직접 적용하고 현재32(a)/(c)에서 serious/unexpected 범위를 확인했다.')
k(u,2,32,'21CFR310.305(c)(1)(i)','as soon as possible','initial report는 가능한 한 신속히 제출해야 한다는 별도 표현이 있다.15일을 기다려도 된다는 뜻이 아니다.')
k(u,3,32,'21CFR310.305(c)(1)(i)','15 calendar days from initial','initial information receipt 이후15 calendar days를 넘기지 않는다는 기산점과단위를 직접 확인했다.')
k(u,4,32,'21CFR310.305(c)(2)','new information','serious/unexpected AE를 조사하고 newinformation 수령 시 followup을 제출하도록 직접 정한다.')
k(u,5,32,'21CFR310.305(c)(2)','within 15 calendar days','followup은 newinformation 수령 후15 calendar days 이내라는 기한을 직접 정한다.')
k(u,6,32,'21CFR310.305(c)(2)','as requested by FDA','followup은 FDA가 요구하는 경우에도 제출하도록 별도 대안을 직접 둔다.')
k(u,7,33,'FDA503B AE final guidance III.B','suspect drug','FDA는 의심약물과AE 두 요소만 있어도 가능한 한 신속히15일 내 보고하고 나머지를 후속으로 구하도록 설명한다. 모든 세부사항 수집을 initial 지연 이유로 삼지 않는다.')
for n,anchor,reason in [(8,'Death','serious 정의의 열거결과에 death가 직접 있다.'),(9,'life-threatening adverse','serious 정의는 실제사건에서 즉각 사망위험을 놓은life-threatening 경험을 포함한다.'),(10,'inpatient hospitalization','입원 또는 기존입원 연장을 직접 열거한다.'),(11,'persistent or significant','persistent/significant disability/incapacity를 직접 열거한다.'),(12,'congenital anomaly/birth defect','congenital anomaly/birth defect를 직접 열거한다.'),(13,'Important medical events','사망/입원 등이 당장 없어도 적절한 의학적판단상 중대한 결과 예방을 위해 의학·수술개입이 필요할 수 있는 important medicalevent를 포함한다.')]:k(u,n,32,'21CFR310.305(b) Serious adverse drug experience',anchor,reason)
for n,anchor,reason in [(14,'not listed in the current','unexpected는 현재label에 없는AE라고 직접 정의한다.'),(15,'greater severity','label상 기존AE보다greater severity인 경우도 unexpected에 포함한다.'),(16,'specificity','label상 기존AE보다greaterspecificity인 경우도 포함한다.'),(17,'rather than from the perspective','unexpected는 labeling상 미관찰기준이며 예상약리작용에서 보고자가 예상했는가를 기준으로 삼지 않는다고 직접 설명한다.')]:k(u,n,32,'21CFR310.305(b) Unexpected adverse drug experience',anchor,reason)
k(u,18,32,'21CFR310.305(g)(1)','period of 10 years','현재eCFR의 기록조항은(g)(1)이며 report대상AE의rawdata/correspondence등을10년 보존한다. 구FDAguidance의옛(f)번호를 현행번호로 쓰지 않았다.')
k(u,19,20,'Policy2025-02 SADE definition','preventable','MA SADE 정의는 preventable occurrence와 정해진 중대결과를 전제로 한다. 연방 unexpected 요건과 같지 않다.')
k(u,20,33,'FDA503B AE final guidance applicability','state','FDA guidance는 state의별도보고를 대체하지 않는다고 설명한다. 연방 serious/unexpected와 MA preventable SADE 정의를 합치면trigger가 달라진다.')
k(u,21,34,'247CMR20.02(1)/(2) resident serious injury/death and pharmacy-produced SADE','seven business','적용되는 MA trigger는 discovery/knowledge 기산7businessdays를 별도로 두므로 연방15calendar와 단위·기산점을 혼동하지 않는다.')
k(u,22,4,'Policy2024-04 SADE notification paragraph','immediately','defective preparation이SADE를 caused/suspected하면 Board에immediate notification하도록 별도 경로를 정한다.')
k(u,23,33,'FDA503B AE final guidance state requirements','state','연방보고는 주의별도보고를 대신하지 않는다는 FDA설명과 MA7businessday/immediate규칙을 함께 읽으면 federal15일만 지키고state기한을 생략할 수 없다.')
u='w4-c-12'
for n,sec,anchor,reason in [(1,'21.02(1)/(2)','located in','resident 시설은MA21.02 신청·등록경로를 따르고 nonresident는21.04로 구별한다.'),(2,'21.02(3)(b)','controlled','resident신청서에MCSR신청서를 포함하도록 직접 정한다.'),(3,'21.02(3)(d)','valid, current','유효한 current FDA503B registration 증거를 제출하도록 직접 정한다.'),(4,'21.02(3)(e)','two years immediately','resident신청 직전2년 이내FDA inspection 증거를 직접 요구한다.'),(5,'21.04(1)(c)','valid, current','nonresident신청에도 유효 current FDA503B registration증거를 직접 요구한다.'),(6,'21.04(1)(d)','two years immediately','nonresident신청 직전2년 이내FDA inspection증거를 직접 요구한다.'),(7,'21.04(1)(f)','within three months','home state에서license/registration받는 경우그기관의3개월 이내발급goodstanding증거를 제출하도록 조건부로 직접 정한다.'),(8,'21.04(1)','Non-resident','nonresident에게도MA신청서·FDA자료·조건부home-state자료 등 별도등록경로를 둔다.'),(9,'21.02/21.04','application','FDA등록은MA신청의 증빙 중하나이다. FDA공개목록만으로MA등록조건 전체가 충족되지 않는다.'),(10,'21.03(2)','not inspected','직전2년FDAinspection이없되나머지완전한신청을낸 경우의provisional경로를 직접 정한다.'),(11,'21.03(1)','not eligible','nonresident는provisionalregistration에eligible하지않다고 직접 정한다.'),(12,'21.03(3)','may compound','provisional시설은sterilepreparation을compound할수있다고 직접허용한다.'),(13,'21.03(3)','may not distribute','FDAinspection과MAfullregistration전distribute금지를 직접정한다.'),(14,'21.03(3)','or dispense','같은조건이충족되기전dispense금지도 직접정한다.'),(15,'21.03(3)/(5)','received a Massachusetts','FDAinspection뿐아니라MAregistration을받아야output을허용하므로pendingapplication은fullregistration이아니다.'),(16,'21.05(1)','each odd numbered year','fullresident/nonresidentregistration은발급후해당odd-numberedyear12월31일만료를 직접정한다.'),(17,'21.05 (with21USC353b(b)(1)(A))','December 31st','MA의oddyearexpiry와연방annualOct–Decregistration은각각다른법령·주기다.'),(18,'21.02(6)/21.04(3)','non-transferrable','resident/nonresidentregistration은non-transferrable이라고직접정한다.'),(19,'21.08(2)/(3)/(5)','60 days','ownershiptransfer에는원registrant최소60일사전통지·새registrant60일내신청·승인전output금지라는별도절차를직접둔다.'),(21,'21.12(1)','prior','relocation은Board의priorapproval을요구하는조항을직접확인했다.'),(22,'21.12(1)','90 days','신청은원칙적으로희망이전최소90일전이라고직접정한다.'),(23,'21.12(1)','otherwise','Board가달리승인한경우라는90일예외를직접둔다.'),(24,'21.12','inspected','새장소에서FDAinspection전distribute/dispense할수없다는별도조건을직접정한다.'),(25,'21.09(4)','inspection by the FDA','FDAinspection은within14daysinwriting통지대상으로직접열거한다.'),(26,'21.09(5)','Form 483','FDAForm483수령은동일14일서면통지대상이다.'),(27,'21.09(5)','Warning Letter','FDAwarningletter수령도동일14일서면통지대상이다.')]:k(u,n,35,'247CMR'+sec,anchor,reason)
sb(u,20,'본문/명제는 ownership/control 변경에 해당 사전 절차를 적용한다고 넓게 쓴다. 21.08은ownershiptransfer사전60일통지이나21.09(2)/(3)은officers/directors 및5%초과ownership변경을14일내사후서면통지로 둔다. control의범위·어느변경이사전대상인지명확하지않아일괄사전요건으로인증하지않는다.')
u='w4-c-13'
for n,sec,anchor,reason in [(1,'13.02 Qualified nuclear pharmacist','registered as a pharmacist','qualifiednuclearpharmacist정의가MA Board등록pharmacist를전제로직접명시한다.'),(2,'13.02 Qualified nuclear pharmacist','education, training and experience','일반pharmacist등록외education/training/experience에관해Board에satisfactoryevidence를제출하는별도자격이다.'),(3,'13.02 Qualified nuclear pharmacist','official letter','Board의qualification공식letter를받아야한다는정의를직접확인했다.'),(4,'13.03(1)/(7)','nuclear pharmacy permit','nuclearpharmacy설립의별도permit신청·발급절차를직접둔다.'),(5,'13.05(1)','other appropriate federal and state','NRC/FDA및otherapplicablefederal/stateagency규칙준수를별도로정한다.'),(6,'13.05(3)','Only designated qualified','radiopharmaceutical활동은designatedqualifiednuclearpharmacist가수행하도록정하므로일반compounding교육만으로권한을추정할수없다.'),(7,'13.06','200','formal교육경로의200contacthours를직접정한다.'),(8,'13.06','60','200hours중lab최대60hours라는상한을직접정한다.'),(9,'13.06','500','추가실무경로는3monthsfulltime또는500hoursactualpracticalexperience로정한다.'),(10,'13.06','supervision','qualifiednuclearpharmacist감독또는Boardapprovedprogram등실무경로의조건을직접정한다.'),(11,'13.06','affidavit','교육·훈련·경험에관한상세affidavit를Board에내도록직접정한다.'),(12,'13.05(3)/(16)','personal attendance','적어도한명의qualifiednuclearpharmacist가항상personalattendance해야한다는현장조건을직접정한다.'),(14,'13.03(4)(j)','adequate shielding','dosagedispensing을위한adequateshielding및필요equipment를직접열거한다.'),(15,'13.03(4)(f)–(i)','radiation','survey meter/area monitor/personneldosimeter등radiationmonitoringequipment를직접열거한다.'),(18,'13.05(12)(e)','amount of radioactive material','outerlabel에radioactiveactivityamount를넣도록정하므로quantity는일반tablet개수와같이해석할수없다.'),(19,'13.05(12)(e)','time of calibration','activity를attimeofcalibration으로특정하므로수치해석에기준시간이필요하다.별도의calibrationstamp표시의무까지이조항이명시한것은아니다.')]:k(u,n,23,'247CMR'+sec,anchor,reason)
sb(u,13,'247CMR13.05(22)의adequate security 원칙은 확인했지만 명제의 구체적 접근제한을 직접 정하는 현행825/방사선 원문은 확보하지 못했다. 일반 보안문구를 access restriction 전체의 증거로 확대하지 않는다.')
sb(u,16,'현재 MA radioactive-material licensing의105CMR120 회수는HTTP200이나본문0바이트였다. federal10CFR30.3의NRClicense원칙만으로MA Agreement State의실제facilitylicense조건을대체하지않아보류한다.')
sb(u,17,'현재state radiation-specificSOP조항/USP825전문을확보하지못했다.247CMR13의방사선규칙일반준수문구만으로필수SOP의전범위를인증하지않는다.')
u='w4-c-14'
for n,sec,anchor,reason in [(1,'13.05(12)(a)','radiation symbol','outercontainer의radiationsymbol표시를직접열거한다.'),(2,'13.05(12)(b)','Caution','Caution–RadioactiveMaterial경고를outercontainer표시에직접열거한다.'),(3,'13.05(12)(c)','radionuclide','radionuclide name을outercontainer표시에직접열거한다.'),(4,'13.05(12)(d)','chemical form','chemicalform또는commonname을직접열거한다.'),(5,'13.05(12)(e)','amount of radioactive material','calibration시점activityamount를직접열거한다.별도calibrationdate/time stamp와는구별한다.'),(6,'13.05(12)(h)','expiration','expirationdate또는time을직접열거한다.'),(9,'13.05(6)(e)/13.02 service','specific instructions','유효nuclearRx에는필요한specificinstructions를포함하고radiopharmaceuticalservice에는safeuseadvice가포함된다.환자사용에필요한지침이라는범위로판단했다.'),(10,'13.05(6)(d)','unknown at the time','정확한원문조건은처방수령시환자이름이unknown인경우이다.이를명제의한정된nuclear경로로읽으며모든일반처방의dispensing시점신원확인면제로확장하지않는다.'),(11,'13.05(6)(d)','72 hours after dispensing','환자이름·주소를dispensing후72시간안에얻어야한다고기산점·기한을직접정한다.'),(13,'13.05(5)','three years','radiopharmaceuticalacquisition/disposition상세기록최소3년보존을직접정한다.'),(14,'13.05(9)','not administered','unusedradiopharmaceutical을disposal목적으로반환받을수있고quantity기록을유지하는경로를정한다.'),(15,'13.05(9)','disposal','이반환허용의목적은disposal이다.일반stock재편입·다른환자재판매허가를이조항에서추론할수없다.'),(16,'13.05(9)/(1)','NRC','unusedreturn/disposal은NRC규칙및applicableagency조건에따르는별도경로다.')]:k(u,n,23,'247CMR'+sec,anchor,reason)
sb(u,7,'247CMR13.05(12)(e)는amount of radioactive activity at the time of calibration을요구하지만calibrationdate/time자체의별도인쇄의무는직접명시하지않는다.현행825/NRC·state별도원문을확보하지못해그추가표시는보류한다.')
sb(u,8,'현행USP825의innercontainer와outershield구체표시조항을직접확보하지못했다.247CMR13.05(12)는outercontainer목록만있어innerlabel전요건의대체증거가아니다.')
k(u,12,6,'MGL94C§21 normal prescription patient label (with247CMR13.05(6)(d))','patient','일반Rx환자표시요건과핵약국의unknown-at-receipt72h한정경로는서로다른조문이다.핵약국예외를일반약국환자확인유예로확대할수없다.')
k(u,17,9,'MGL94C§23(e) (with247CMR13.05(5))','two years','일반처방보존은최소2년이고핵약국acquisition/disposition은별도3년이다.기록종류를구별하여더긴의무를줄이지않았다.')
sb(u,18,'USP825공식FAQ는403이며현재정본전문과MA방사선규정본문을회수하지못했다.13장일반요건을확인했어도preparation-specific모든825/방사선세부조건을인증하지않는다.')
# Independent body-to-census omissions; do not edit author census or bodies.
OMISSIONS={'w5-a-12':['본문 첫 문단의 “Medication뿐 아니라 첨가제”는 비약물 첨가제(excipient)의 안정성·호환성을 실제 체온 및 전체 pump infusion 기간에 대해 평가한다는 추가 원자 명제다. 최종16개 census는 all drugs(4·5), CSP/pump(6), 온도(7·8)만 열거하며 비약물 첨가제를 독립 항목으로 포착하지 않는다. Policy2024-02는 drugs/CSP/pump를 명시하지만 excipient를 직접 별도 열거하지 않아 이 누락 명제의 정확한 법적 범위도 SOURCE_BLOCKED이다. 새 저자 원자 추가와 독립 재평가가 필요하며 이 보고서가 census를 수정하지 않는다.']}
# Check every expected ordinal exactly once and every retained anchor literally (case-insensitive).
for uid,u in D.items():assert set(A[uid])==set(range(1,len(u['claims'])+1)),(uid,sorted(set(range(1,len(u['claims'])+1))-set(A[uid])))
missing=[]
for uid,items in A.items():
 for n,(status,src,section,anchor,reason) in items.items():
  if src and re.sub(r'\s+',' ',anchor.lower()) not in re.sub(r'\s+',' ',(S/f'{src:02}.txt').read_text().lower()):missing.append((uid,n,src,anchor,section))
if missing:
 print('MISSING_LITERAL_ANCHORS',json.dumps(missing,ensure_ascii=False));sys.exit(2)
print('Mapped',sum(map(len,A.values())),'claims', {s:sum(x[0]==s for v in A.values() for x in v.values()) for s in ['KEEP','SOURCE_BLOCKED','LEGAL_HOLD']})
# Retained document validity, document vintage, and precise text ranges. Response headers
# are retrieval metadata; publication/effective dates below come from the document itself.
valid={1,2,4,5,6,7,8,9,10,11,13,14,15,16,17,18,20,23,24,25,26,27,28,29,30,31,32,33,34,35,46,47,48,49,51,52,53,54,55,57,58}
versions={1:'Publisher FAQ dated2023-12-11, Q8:2022revision official2023-11-01; May2024 version title-only789update. Retrieved2026-11-04; current subscription USP-NF full797/659 not obtained. KEEP limited to the explicitly retained public publisher explanations.',2:'USP2022 BUD summary hosted by Mississippi Board; historical corroboration only; no current full797 matrix certification.',4:'Policy2024-04 adopted2024-09-05; current MA official posted PDF retrieved2026-11-04; no later supersession established by this document alone.',5:'Policy2025-01 adopted2025-05-01; current MA official posted PDF retrieved2026-11-04. Board policy position quotes Draft17.17(2), not promulgation evidence for draft.',10:'247CMR15 official MA PDF, MAReg1536 dated2024-12-06, retrieved2026-11-04.',11:'Policy2024-02 adopted2024-10-17; current MA official posted PDF retrieved2026-11-04.',13:'Current MA draft-regulations listing retrieved2026-11-04; draft listing is not promulgation/effective-date proof.',14:'Official inspection template referencing DRAFT247CMR17; footnote URL last accessed2023-12-20. Used only for template/draft-source classification, not all current technical requirements.',15:'Media Fill Advisory adopted2022-04-07, explicitly cites2008USP and2021revised draft. Historical supplementary guidance, not current full797 substitution.',16:'NIOSH publication2025-103, title2024list, publicationDec2024; supersedes2016. Occupational health guidance/list, not independently binding law; FDA-CDER human HD scope and postpublication notices remain relevant.',17:'MA USP800 Community Pharmacies Advisory adopted2019-12-05/revised2022-02-03; current official posted PDF retrieved2026-11-04; practical nonexhaustive Board guidance explicitly directs readers to full800.',18:'CDC official publication page for2025-103, page date2025-07-25; includes July17,2025 postpublication MSHI additions. Retrieved2026-11-04.',20:'Policy2025-02 adopted2025-08-07; current MA posted definitions PDF retrieved2026-11-04.',23:'Current official MA247CMR13 posted PDF retrieved2026-11-04; no discrete effective date printed/independently established. Duplicate legacy paragraph numbering exists later in13.05; cited first explicit clauses are identified by quoted text and retained line range. Current825 and radiation-license details are not certified.',25:'Official GovInfo United States Code2024Edition §353a, retrieved2026-11-04, historical amendment note last2013; current FDA posted comparison independently corroborates the described503A framework. Not mislabeled as2025/2026 consolidated edition; exhaustive later-amendment certification unavailable.',26:'Current FDA official outsourcing page retrieved2026-11-04; displayed content-current date2022-03-29. Registration/reporting framework corroboration only.',27:'Official GovInfo United States Code2024Edition §353b, retrieved2026-11-04; added2013 note; current FDA posted comparison/outsourcing pages corroborate the framework. No2025/2026 consolidated edition obtained; exhaustive later-amendment certification not represented.',28:'Current FDA official FDCA503A/B comparison retrieved2026-11-04; displayed content-current date2021-08-13; nonexhaustive agency explanation corroborating statutory framework.',29:'Official GovInfo United States Code2024Edition §360eee, retrieved2026-11-04; product-definition exclusion only; no blanket DSCSA certification for all pharmacy activity.',31:'Official GovInfo United States Code2024Edition PDF duplicate of retained §353bHTML; not separate independent current-law confirmation.',32:'Current eCFR21CFR310.305 retrieved2026-11-04, displayedTitle21 current through2026-11-02; recordkeeping current(g)(1). eCFR is continuously updated editorial text, not the official annual legal print edition.',33:'FDA final Guidance for Industry, Adverse Event Reporting for Outsourcing Facilities Under503B, October2015. Nonbinding guidance applying310.305; old subsection(f) recordkeeping reference is not current(g).',34:'247CMR20 official MA posted reporting PDF retrieved2026-11-04; MAReg1536 dated2024-12-06.',35:'247CMR21 official MA PDF, MAReg1305 dated2016-01-29, retrieved2026-11-04. No later-effective amendment independently established; current posted text used for exact clauses.',46:'Current eCFR10CFR30.3 retrieved2026-11-04; NRC federal licensing principle only, does not itself establish MA Agreement State license/SOP details.',51:'CDC publication2023-130 official landing page,2023-04-21, retrieved2026-11-04. Occupational guidance not standalone binding USP800 text.',52:'NIOSH2023-130 Managing Hazardous Drug Exposures: Information for Healthcare Settings,2023. Public occupational-health recommendations, not full current USP800 and not blanket technical/legal facility certification.',53:'Current official DEA Drug Scheduling information page retrieved2026-11-04; general scheduling explanation; no discrete revision/effective date established.',58:'247CMR9 official MA PDF, MAReg1536 dated2024-12-06, retrieved2026-11-04; patient counseling9.18 applied only as appropriate to patient need.'}
for n in [6,8,9,47,48,49]:versions[n]='Massachusetts Legislature current official posted General Laws section retrieved2026-11-04. Section text has no discrete effective date or complete amendment chronology established here; no inferred2026 enactment date.'
for n in [24,54,55,57]:versions[n]='Current eCFR official government editorial resource retrieved2026-11-04; exact section/range retained. No discrete original effective date independently established; not a claim of official annual print-edition status.'
# Exact source segments use section-specific retained ranges; do not attach an unrelated
# group snippet to a claim just because the same source is broadly relevant.
def lines(src,a,b):
 t=(S/f'{src:02}.txt').read_text();ls=[x+'\n' for x in t.split('\n')];return sum(map(len,ls[:a-1])),sum(map(len,ls[:b]))
def span(src,section,anchor):
 t=(S/f'{src:02}.txt').read_text();lo,hi=0,len(t)
 if src==1:
  q=int(re.search(r'Q(\d+)',section).group(1));m=re.search(r'(?m)^[\f]*'+str(q)+r'\. ',t);assert m
  lo=m.start();m2=re.search(r'(?m)^[\f]*'+str(q+1)+r'\. ',t[m.end():]);hi=m.end()+m2.start() if m2 else len(t)
 elif src in {4,5,10,11,17,20}:lo,hi=0,len(t)
 elif src==14:lo,hi=0,min(7000,len(t))
 elif src==15:lo,hi=0,min(5000,len(t))
 elif src==16:
  lo,hi=lines(src,410,435) if 'Organization' in section else lines(src,175,310)
  # Publication foreword describes reduction from3tables to2 most explicitly.
  if 'number of tables to two' in anchor:lo,hi=lines(src,45,70)
 elif src==52:
  if 'glossary' in section:lo,hi=lines(src,370,440)
  elif '6.4 Gloves' in section:lo,hi=lines(src,1140,1206)
  elif '6.4 Gowns' in section:lo,hi=lines(src,1207,1230)
  elif '6.4 Respiratory' in section:lo,hi=lines(src,1231,1277)
  elif '6.4 Eye' in section:lo,hi=lines(src,1290,1320)
  elif '6.3' in section:lo,hi=lines(src,1050,1120)
  elif 'Transportation' in section:lo,hi=lines(src,1924,1934)
  elif 'receiving damaged' in section:lo,hi=lines(src,1915,1923)
  elif '7.1' in section:lo,hi=lines(src,1467,1497)
  elif '7.2' in section:lo,hi=lines(src,1498,1535)
 elif src==23:
  if '13.06' in section:lo,hi=lines(src,363,380)
  elif '13.03' in section:lo,hi=lines(src,89,164)
  elif '13.02' in section and '13.05' not in section:lo,hi=lines(src,18,88)
  else:
   lo,hi=lines(src,162,304)
   m=re.search(r'13\.05\((\d+)\)',section)
   if m:
    n=int(m.group(1));r=re.search(r'(?m)^\s*\('+str(n)+r'\)',t[lo:hi]);assert r,(src,section)
    start=lo+r.start();r2=re.search(r'(?m)^\s*\('+str(n+1)+r'\)',t[start+len(r.group(0)):hi]);end=start+len(r.group(0))+r2.start() if r2 else hi
    lo,hi=start,end
 elif src==35:
  m=re.search(r'21\.(\d+)',section)
  if m:
   n=int(m.group(1));pat=r'(?m)^21\.'+str(n).zfill(2)+r': (?!continued)';matches=list(re.finditer(pat,t));assert matches
   lo=matches[-1].start();nextm=re.search(r'(?m)^21\.'+str(n+1).zfill(2)+r': ',t[lo+1:]);hi=lo+1+nextm.start() if nextm else len(t)
 elif src==55:
  marker=r'(?m)^\(k\) Training and information\.' if '(k)' in section else r'(?m)^\(f\) Fit testing\.'
  m=re.search(marker,t);assert m;lo=m.start();hi=min(len(t),lo+8500)
 elif src==57:
  marker='§ 1317.15 Reverse distributor' if '1317.15' in section and '1317.05/' not in section else '§ 1317.05'
  m=t.find(marker, t.find('Subpart A—Disposal'));lo=m if m>=0 else 0;hi=min(len(t),lo+6000)
 elif src==58:lo,hi=lines(src,665,730)
 elif src==33:
  if 'III.B' in section:lo,hi=lines(src,311,341)
  elif 'state' in section or 'applicability' in section:lo,hi=lines(src,155,180)
 if src not in {1,11,14,15,16,23,35,52,55,57,58,33}:
  # Prefer legal/content body over site-navigation occurrences for short anchors.
  if src in {25,27,29}:
   m=re.search(r'(?m)^§(?:353a|353b|360eee)\.',t);lo=m.start() if m else 0
  elif src in {6,8,9,47,48,49}:
   m=re.search(r'Section\s+(?:21|23|39D|39G|39H|39I)\.',t);lo=m.start() if m else 0
  elif src in {32,54}:
   m=re.search(r'(?m)^§ (?:310\.305|1308\.14) ',t);lo=m.start() if m else 0
  elif src==53:
   m=t.find('Drugs, substances, and certain chemicals');lo=m if m>=0 else 0
 # Use whitespace-tolerant matching but preserve exact raw extracted bytes in excerpt.
 pat=r'\s+'.join(re.escape(w) for w in anchor.split());m=re.search(pat,t[lo:hi],re.I)
 if not m:
  raise AssertionError(('ANCHOR_OUTSIDE_EXACT_SECTION',src,section,anchor,lo,hi,t[lo:lo+120]))
 a,b=lo+m.start(),lo+m.end()
 if src in {1,4,5,10,11,17,20,16,23,35,52,55,57,58,33}:a,b=lo,hi
 else:
  a=max(lo,t.rfind('\n\n',lo,a));a=a if a==lo else a+2
  end=t.find('\n\n',b,hi);b=min(hi,end if end>=0 else b+1400)
  if b-a<min(250,hi-lo):b=min(hi,a+1600)
 return a,b,t[a:b]
def authority(src,section,anchor):
 m=json.loads((S/f'{src:02}.meta.json').read_text());assert src in valid
 a,b,quote=span(src,section,anchor);t=(S/f'{src:02}.txt').read_text()
 return {'source_type':'PUBLIC_OFFICIAL','official_url':m['official_url'],'exact_section':section,'law_checked_date':'2026-11-04','version_or_effective_date_status':versions.get(src,'Current official posted public source retrieved2026-11-04; discrete effective date not independently established.'),'evidence_path':str(S/f'{src:02}{m["raw_extension"]}'),'evidence_sha256':m['raw_sha256'],'text_evidence_path':str(S/f'{src:02}.txt'),'text_evidence_sha256':m['text_sha256'],'retrieval_metadata_path':str(S/f'{src:02}.meta.json'),'retrieval_metadata_sha256':sha((S/f'{src:02}.meta.json').read_bytes()),'retrieved_at_utc':m['retrieved_at'],'retrieval_kind':m['retrieval_kind'],'http_status':m['http_status'],'evidence_excerpt':quote,'text_character_range':[a,b],'text_line_range':[t[:a].count('\n')+1,t[:b].count('\n')+1]}
# Secondary directly read authority where a finding expressly compares two legal systems.
EXTRA={('w4-b-21',15):[(2,'USP2022 BUD fact sheet p3 Category2 aseptic/no-sterility/sterile-only row','Aseptically processed, no sterility testing')],('w4-b-21',16):[(2,'USP2022 BUD fact sheet p3 Category2 aseptic/no-sterility/sterile-only row','Aseptically processed, no sterility testing')],('w4-c-8',13):[(27,'21USC353b(b)(2)(A)','Upon initially registering')],('w4-c-7',14):[(23,'247CMR13.05(9)','disposal')],('w4-c-7',18):[(52,'NIOSH2023-130 §7.1 Hazardous Drug Waste','state')],('w4-c-1',3):[(16,'NIOSH2024 Table2 clonazepam','clonazepam')],('w4-c-1',5):[(48,'MGL112§39H current USP complex nonsterile','USP')],('w4-c-3',17):[(47,'MGL112§39G sterile compounding license','license')],('w4-c-4',1):[(47,'MGL112§39G sterile compounding license','license')],('w4-c-10',27):[(8,'MGL112§39D(a) Beyond-use date definition','Beyond-use date')],('w4-c-11',1):[(32,'21CFR310.305(a)/(c)(1)(i)','serious and unexpected')],('w4-c-11',20):[(20,'Policy2025-02 SADE definition','preventable')],('w4-c-11',23):[(34,'247CMR20.02(1)/(2)','seven business'),(4,'Policy2024-04 SADE notification','immediately')],('w4-c-12',17):[(27,'21USC353b(b)(1)(A)','October 1')],('w4-c-14',12):[(23,'247CMR13.05(6)(d)','unknown at the time')],('w4-c-14',17):[(23,'247CMR13.05(5)','three years')]}
# For Table2 direct entry the source needs the actual Table2 line, not introductory scope.
oldspan=span
def span(src,section,anchor):
 if src==16 and 'Table2 clonazepam' in section:
  t=(S/'16.txt').read_text();a,b=lines(src,1038,1052);assert 'clonazepam' in t[a:b].lower();return a,b,t[a:b]
 return oldspan(src,section,anchor)
# Update content-validity annotations before authority metadata digests are calculated.
for mp in sorted(S.glob('*.meta.json')):
 n=int(mp.name.split('.')[0]);m=json.loads(mp.read_text());raw=(S/f'{n:02}{m["raw_extension"]}').read_bytes();txt=(S/f'{n:02}.txt').read_bytes();assert sha(raw)==m['raw_sha256'] and sha(txt)==m['text_sha256']
 if n in valid:m['content_validity']='VALID_OFFICIAL_DOCUMENT; limited sections read/used as identified in report; not blanket full-document legal certification'
 elif n in {39,40,41}:m['content_validity']='REJECTED_HTTP200_SOFT404_PAGE_NOT_FOUND_NOT_STATUTORY_TEXT'
 elif n==44:m['content_validity']='REJECTED_HTTP200_ZERO_BYTE_RESPONSE_NO_LEGAL_TEXT'
 elif n==50:m['content_validity']='REJECTED_META_REFRESH_ONLY_NO_SUBSTANTIVE_DOCUMENT; actual destination retained separately as51/52'
 else:m['content_validity']='REJECTED_HTTP_ACCESS_OR_NOT_FOUND_RESPONSE_NOT_LEGAL_AUTHORITY'
 m['manual_content_review_date']='2026-11-04';mp.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
provenance={'stage':job['stage'],'actor_provenance':job['actor_provenance'],'auditor':job['auditor'],'auditor_instance':job['auditor_instance'],'independent_of_authors':True,'canonical_audit':False,'canonical_release_credit':0,'question_audit_credit':0}
report={**provenance,'captured_source_head':packet['source_head'],'review_date_utc':'2026-11-04','scope_read':{'units':20,'claims':432,'questions':40,'derived':12,'question_and_canonical_credit':0},'source_use_limit_ko':'공식 공개원문만 보존했다. 문서의 실제 발행일/효력 한계를 retrieval UTC와 구별했다. USP 공개 FAQ와 MA advisory의 좁은 설명은 그 범위만 확인하고 구독 정본·모든800/825·HVAC·waste code를 인증하지 않았다. 저자 SOURCE_CHECKED/기존 감사 결론을 법적 증거로 사용하지 않았다.','records':[]}
errors=[]
for uid,u in D.items():
 cs=[]
 for n,c in enumerate(u['claims'],1):
  status,src,section,anchor,reason=A[uid][n];aa=[]
  try:
   if src:aa=[authority(src,section,anchor),*[authority(*x) for x in EXTRA.get((uid,n),[])]]
  except Exception as e:errors.append((uid,n,str(e)));continue
  finding='검토 명제: '+c['statement_ko']+'\n독립 대조: '+reason
  cc={'claim_id':c['claim_id'],'claim_record_sha256':canon(c),'claim_read_completely':True,'statement_ko':c['statement_ko'],'legal_status':status,'finding':finding,'authorities':aa}
  if status!='KEEP':cc['blocker']='직접 확인하지 못한 명제별 요건: '+c['statement_ko']+' '+reason
  cs.append(cc)
 omissions=OMISSIONS.get(uid,[]);st='LEGAL_HOLD' if omissions else 'SOURCE_BLOCKED' if any(c['legal_status']=='SOURCE_BLOCKED' for c in cs) else 'KEEP'
 report['records'].append({'unit_id':uid,'title':u['unit']['title'],'binding':u['binding'],'body_read_completely':True,'completeness':'OMISSIONS_FOUND' if omissions else 'COMPLETE','completeness_method':'실제 배정 body 전문을 문장·표의 각 셀·수치·기산점·조건·예외·권한·기록 단위로 분해하여 전체 '+str(len(u['claims']))+'개 census 명제와 양방향 대조했다. 관련40문항 각 보기·정답·전체해설 및12derived의 보충/상충 범위도 읽었다. 완전성은 법규KEEP와 별도이며 출처확인 실패를 census 삭제로 처리하지 않았다.','omissions':omissions,'legal_status':st,'claims':cs})
if errors:print('SECTION_MAPPING_ERRORS',json.dumps(errors,ensure_ascii=False));sys.exit(3)
(P/'review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('REPORT',len(report['records']),sum(len(r['claims']) for r in report['records']))
