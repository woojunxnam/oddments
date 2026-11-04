import json,re,hashlib,datetime,sys,collections
from pathlib import Path
exec(open('/tmp/final86-d-manual.py').read())
root=Path('/workspace/notes-final86-d');base=root/'reports/full-corpus-review/independent-notes/final86-d';packet=json.loads((base/'visible-input.json').read_bytes());job=json.loads((base/'assignment.json').read_bytes());prefix=str(base.relative_to(root));metas={p.name[:16]:json.loads(p.read_bytes()) for p in (base/'sources').glob('*.meta.json')};labels=json.loads((base/'product-label-review-data.json').read_bytes());nlms=json.loads((base/'nlm-label-review-data.json').read_bytes())
def sha(x):return hashlib.sha256(x).hexdigest()
def digest(x):return sha(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def compact(s):return re.sub(r'\s+',' ',s).strip()
def txt(k):return compact((root/metas[k]['text_path']).read_text())
def keyurl(u):return sha(u.encode())[:16]
def auth(k,section):
 m=metas[k];assert m.get('status_code')==200
 ver='공식 문서 원문을 검토일에 대조했다. 별도 시행일을 확정하지 못한 경우 조회일을 시행일로 사용하지 않는다.'
 if k in labelbykey:ver='SPL effective_time='+str(labelbykey[k]['effective_time'])+'; version='+str(labelbykey[k]['version'])+'; label set_id='+str(labelbykey[k]['setid'])+'. 검색 URL의 cutoff가 있으면 그 이후 변경 및 현재 판매는 인증하지 않는다.'
 if 'retention_note_ko' in m:ver+=' 같은 날 원 GET retained; 원수집시각 '+m['requested_at_utc']+'. 이번 배치 새 GET으로 세지 않았다.'
 else:ver+=' 실제 GET '+m['requested_at_utc']+'.'
 return {'source_type':'PUBLIC_OFFICIAL','official_url':m['official_url'],'exact_section':section,'law_checked_date':'2026-11-04','version_or_effective_date_status':ver,'evidence_path':m['raw_path'],'evidence_sha256':m['raw_sha256'],'text_evidence_path':m['text_path'],'text_evidence_sha256':m['text_sha256'],'metadata_path':prefix+'/sources/'+k+'.meta.json','metadata_sha256':sha((base/'sources'/(k+'.meta.json')).read_bytes())}
labelbykey={l['key']:l for l in labels}
# 직접 읽은 DailyMed 본문 라벨의 section 11/1/2/3/5/12 구획을 보존한다.
for name,k in {'Vyvanse':'19f6e6144c7500ad','Focalin':'0fd0012bde32f684','Butrans':'fbe5bf39e31059b8','Belbuca':'795d2435b615601a','Sublocade':'cfe1b43dedfd2c76','Brixadi':'21b44f50aa9af456','Spravato':'183e44eb17e3d446','Fycompa':'14a1f9172369f309','Xyrem':'3fa760b2f2a5e168','Xywav':'3c3ba895120469aa','Lumryz':'add4a78b5846712a'}.items():
 t=txt(k);ss={}
 for nn,title,field in [(11,'DESCRIPTION','description'),(1,'INDICATIONS AND USAGE','indications_and_usage'),(2,'DOSAGE AND ADMINISTRATION','dosage_and_administration'),(3,'DOSAGE FORMS AND STRENGTHS','dosage_forms_and_strengths'),(5,'WARNINGS AND PRECAUTIONS','warnings_and_cautions'),(9,'DRUG ABUSE AND DEPENDENCE','drug_abuse_and_dependence'),(12,'CLINICAL PHARMACOLOGY','clinical_pharmacology')]:
  hits=list(re.finditer(str(nn)+r'\s+'+title,t));pos=hits[-1].start() if hits else -1
  if pos>=0:
   end=re.search(r'\b'+str(nn+1)+r'\s+[A-Z][A-Z ]{4,}',t[pos+10:]);ss[field]=t[pos:pos+10+end.start()] if end else t[pos:pos+13000]
 labelbykey[k]={'key':k,'url':metas[k]['official_url'],'setid':metas[k]['official_url'].split('setid=')[-1],'effective_time':'현재 게시 SPL 원문의 문서 버전 참조; 별도 시행일 미확정','version':'raw 원문 보존','openfda':{'brand_name':[name]},'sections':ss}
for d in nlms:
 # 오래된 Sonata2010 / Ultracet2012는 현재 라벨 검증으로 사용하지 않는다.
 if d['key'] in ['c094923cfbb61510','c830faaa71a6b933']:continue
 name={'44b79e9f73c74a9b':'ella','8fc6c04680786374':'Mifeprex','a0a23e98a4a04850':'Ztalmy','ed731f068a577a42':'Rextovy'}[d['key']];ss={}
 for s in d['sections']:
  for term,field in [('DESCRIPTION','description'),('INDICATIONS AND USAGE','indications_and_usage'),('DOSAGE FORMS','dosage_forms_and_strengths'),('Controlled Substance','controlled_substance'),('DOSAGE AND ADMINISTRATION','dosage_and_administration'),('Mechanism of Action','clinical_pharmacology'),('REMS','warnings_and_cautions')]:
   if term.lower() in s['title'].lower():ss[field]=ss.get(field,'')+' '+s['text']
 labelbykey[d['key']]={'key':d['key'],'url':metas[d['key']]['official_url'],'setid':d['setid'],'effective_time':d['effective_time'],'version':d['version'],'openfda':{'brand_name':[name]},'sections':ss}
brandmap={}
for l in labelbykey.values():
 for n in l['openfda'].get('brand_name',[]):brandmap[n.lower()]=l['key']
# 각 표 행과 현재 실제 확보한 구체 제품 라벨의 수동 연결. FDA 조회 실패 브랜드는 여기서 생성하지 않는다.
rows={};rowlabels={}
for u in packet['units'][6:]:
 for ln in u['unit']['body'].splitlines():
  m=re.match(r'\| ([AB]\d{3}) (.+?) — (.+?) \|',ln)
  if m:
   rid,g,brands=m.groups();rows[rid]={'generic':g,'line':ln,'brands':brands}
   found=[]
   for brand in re.split(r' / | — ',brands):
    if brand.lower() in brandmap:found.append(brandmap[brand.lower()])
   rowlabels[rid]=list(dict.fromkeys(found))
extra={'A027':['Ketalar'],'A031':[],'A056':['tramadol hydrochloride','ConZip'],'A057':[],'A058':['Butorphanol Tartrate'],'A060':['Lomaira'],'A065':['Phenobarbital'],'A071':['Ztalmy'],'A075':[],'B007':['Vivitrol','Naltrexone Hydrochloride'],'B010':['ella'],'B014':['Mifeprex'],'B023':['Doxycycline Hyclate'],'B024':['Ceftriaxone Sodium']}
for r,ns in extra.items():rowlabels[r]=list(dict.fromkeys(rowlabels.get(r,[])+[brandmap[n.lower()] for n in ns if n.lower() in brandmap]))
# 새 실제 GET으로 확보하고 본문을 직접 읽은 다른 제형 라벨을 해당 행에 한정 연결한다.
for rr,kk in {'A011':['2d3da8cc568355b8'],'A041':['2443f0d5b89dd4fa'],'A043':['22b80269d5eab26d','16410de9e10f387d'],'A058':['500ed38aa879b56e'],'A065':['99cc442f86bf61f4'],'B025':['9a718331007a6e5b']}.items():rowlabels[rr]=list(dict.fromkeys(rowlabels[rr]+kk))
# 직접 읽은 연방 조항별 실제 성분 연결. 명칭 색인 조회만으로 schedule을 부여하지 않는다.
fed={}
def fs(rids,k,clause,fact):
 for rid in rids.split():fed[rid]=(k,clause,fact)
fs('A001 A002','b95308609ca5bd38','21 CFR1308.12(d)(1)','amphetamine 및 그 salts/optical isomers를 ScheduleII stimulant로 열거한다.')
fs('A003','b95308609ca5bd38','21 CFR1308.12(d)(5)','lisdexamfetamine을 ScheduleII에 명시한다.')
fs('A004 A005','b95308609ca5bd38','21 CFR1308.12(d)(4)','methylphenidate와 해당 isomer 범위를 ScheduleII로 정한다. Focalin의 d-threo 성분 설명과 함께 대조했다.')
for rid,chemical in [('A006','hydrocodone'),('A007','hydrocodone'),('A008','oxycodone'),('A009','oxycodone'),('A010','morphine'),('A011','hydromorphone'),('A017','codeine')]:fs(rid,'b95308609ca5bd38','21 CFR1308.12(b)(1)',chemical+' 및 해당 preparations를 ScheduleII에 포함한다. 별도의 적격 조합 예외와 구분한다.')
for rid,clause,chemical in [('A012','(c)(15)','methadone'),('A013','(c)(9)','fentanyl'),('A014','(c)(9)','fentanyl'),('A015','(c)(19)','pethidine(meperidine)'),('A016','(c)(29)','tapentadol'),('A018','(f)(2)','FDA-approved oral-solution dronabinol'),('A019','(f)(1)','nabilone')]:fs(rid,'b95308609ca5bd38','21 CFR1308.12'+clause,chemical+'을 ScheduleII에 직접 열거한다.')
fs('A020','518d30bed444e571','21 CFR1308.13(g)(1)','synthetic dronabinol in sesame oil, soft gelatin capsule, FDA-approved 조건의 ScheduleIII 예외를 정한다.')
fs('A021 A022 A023 A024 A025 A026','518d30bed444e571','21 CFR1308.13(e)(2)(i)','buprenorphine 및 해당 preparation 범위를 ScheduleIII로 정한다. naloxone 병용·투여제형 자체가 이 성분의 III 분류를 지우지 않는다.')
fs('A027 A028','518d30bed444e571','21 CFR1308.13(c)(7)','ketamine 및 isomer를 ScheduleIII로 정한다. esketamine의 S-enantiomer 라벨을 함께 대조했다.')
fs('A029','518d30bed444e571','21 CFR1308.13(f)(1)(84)','testosterone과 salts/esters 등 해당 anabolic steroid 범위를 ScheduleIII로 열거한다.')
fs('A030','518d30bed444e571','21 CFR1308.13(e)(1)(ii)','적격 codeine 조합의90mg/dosage unit 및 active nonnarcotic recognized therapeutic amount 조건을 정한다. 특정 브랜드 함량은 별도이다.')
fs('A033','518d30bed444e571','21 CFR1308.13(c)(11)','perampanel을 ScheduleIII에 명시한다.')
fs('A034','518d30bed444e571','21 CFR1308.13(b)(2)','benzphetamine을 ScheduleIII stimulant에 명시한다.')
fs('A035','518d30bed444e571','21 CFR1308.13(b)(6)','phendimetrazine을 ScheduleIII stimulant에 명시한다.')
fs('A036 A037 A038','518d30bed444e571','21 CFR1308.13(c)(6)','FDA-approved drug product의 gamma-hydroxybutyric acid/salts preparations를 ScheduleIII로 정한다. 불법 GHB의I와 구분한다.')
for rid,num,chemical in [('A039',2,'alprazolam'),('A040',13,'clonazepam'),('A041',19,'diazepam'),('A042',34,'lorazepam'),('A043',41,'midazolam'),('A044',55,'temazepam'),('A045',57,'triazolam'),('A046',10,'chlordiazepoxide'),('A047',14,'clorazepate'),('A048',12,'clobazam'),('A049',59,'zolpidem'),('A050',60,'zopiclone/isomers (eszopiclone)'),('A051',58,'zaleplon'),('A052',54,'suvorexant'),('A053',32,'lemborexant'),('A054',17,'daridorexant'),('A055',7,'carisoprodol'),('A062',61,'zuranolone'),('A065',49,'phenobarbital')]:fs(rid,'80f2617da63c92a7','21 CFR1308.14(c)('+str(num)+')',chemical+'을 ScheduleIV에 열거한다.')
fs('A056 A057','80f2617da63c92a7','21 CFR1308.14(b)(3)','tramadol 및 salts/isomers를 ScheduleIV로 정한다.')
fs('A058','80f2617da63c92a7','21 CFR1308.14(g)(2)','butorphanol을 ScheduleIV로 정한다.')
fs('A059','80f2617da63c92a7','21 CFR1308.14(g)(3)','eluxadoline을 ScheduleIV로 정한다.')
fs('A060 A061','80f2617da63c92a7','21 CFR1308.14(f)(9)','phentermine을 ScheduleIV로 정한다. topiramate와 복합제인 사실만으로 phentermine 분류가 없어지지 않는다.')
for rid,num,chemical in [('A067',7,'pregabalin'),('A068',5,'lacosamide'),('A069',1,'brivaracetam'),('A070',2,'cenobamate'),('A071',4,'ganaxolone'),('A072',6,'lasmiditan')]:fs(rid,'10ed3ddb11cfe00d','21 CFR1308.15(e)('+str(num)+')',chemical+'을 ScheduleV로 직접 열거한다.')
fs('A073','10ed3ddb11cfe00d','21 CFR1308.15(c)(4)','diphenoxylate<=2.5mg, atropine sulfate>=25mcg/dosage unit 조합을 ScheduleV에 포함한다.')
fs('A074 A075','10ed3ddb11cfe00d','21 CFR1308.15(c)(1)','codeine<=200mg/100mL 또는100g, 하나 이상 active nonnarcotic ingredient의 valuable medicinal qualities 조건을 모두 요구한다. 농도만으로V를 부여하지 않는다.')
# A061~A066의 실제 행 확인은 생성 후 교차 검증한다.
rowlabels['A060']=[brandmap['nuvigil']]
rowlabels['A074']=[brandmap['guaifenesin and codeine phosphate']]
for rid in ['A059','A060','A061','A062','A063','A064','A066']:fed.pop(rid,None)
fs('A059 A060','80f2617da63c92a7','21 CFR1308.14(f)(7)','modafinil 및 isomers를 ScheduleIV로 정한다. armodafinil의 R-enantiomer 설명과 함께 대조했다.')
fs('A061 A062','80f2617da63c92a7','21 CFR1308.14(f)(9)','phentermine을 ScheduleIV로 정한다. topiramate와의 조합도 해당 성분을 포함한다.')
fs('A063','80f2617da63c92a7','21 CFR1308.14(g)(3)','eluxadoline을 ScheduleIV로 정한다.')
fs('A064','80f2617da63c92a7','21 CFR1308.14(b)(1)','difenoxin<=1mg 및 atropine sulfate>=25mcg/dosage unit 조합을 ScheduleIV로 정한다. 더 낮은difenoxin의V예외와 구분한다.')
fs('A066','80f2617da63c92a7','21 CFR1308.14(c)(61)','zuranolone을 ScheduleIV로 직접 열거한다.')
# 독립 판정은 이 map으로만 결정하며 author review_status를 복제하지 않는다.
overrides={}
def ov(uid,n,status,finding,refs):
 us=[u for u in packet['units'] if u['unit']['id']==uid][0];c=us['claims'][n-1];overrides[c['claim_id']]=(status,finding,refs)
def byid(cid,status,finding,refs):overrides[cid]=(status,finding,refs)
# 본문/문항과 직접 대조한 법규의미, 충돌 및 미확인 범위.
ov('w4-d-13',37,'SOURCE_BLOCKED',manual['w4-d-13'][36],[('da8a8280d110a471','247 CMR9.19(15)'),('6e9b85106a298fa8','Policy2026-03 III.F')])
ov('w2-b-14',10,'SOURCE_BLOCKED',manual['w2-b-14'][9],[('216ae6407ed243a6','MGL94C§18(d); 현재 접수기제는 미확인')])
for n in [7,12]:ov('w1-c-18',n,'LEGAL_HOLD',manual['w1-c-18'][n-1],[('da8a8280d110a471','247CMR9.23(2)(f),(5)'),('aea01b105528c3d2','247CMR20.05(3)'),('7c2a878e9781522e','Policy2022-02 I-II; revised2025-05-01')])
ov('appendix-a-4',50,'LEGAL_HOLD','Butrans와 Belbuca의 현재§1은 모두 severe/persistent pain의 opioid analgesic 적응증이다. Route 차이는 분명하나 원문의 buccal/SL/depot와 indication이 다르다는 묶음 표현이 buccal에도 적응증 차이를 주장하면 부정확하다. buccal route 차이와 OUD제품 적응증 차이를 분리해야 한다.',[('fbe5bf39e31059b8','BUTRANS SPL§1,§11'),('795d2435b615601a','BELBUCA SPL§1,§11')])
# 각 특정 법규비교에 대한 별도 독립 수동 판정.
custom={
'appendix-a-1':{
19:('KEEP','amphetamine류가 비마약성CII라는 분기는 MA§1의 narcotic 정의, DEA 표N,700.002(B)의II편입으로 확인했다. opioid와 동일분기로 합치지 않는다.',['ec3b48bfddfcb0ac','a397fe32483f69ac','c843cbe335da96c8']),
20:('KEEP','MA§18(d)는 nonnarcotic II를 다른 주 적격 practitioner 경로에 포함하고(d1/2)는 narcotic II에 contiguous/Maine 및 verification 조건을 둔다. 두 예외를 동일시할 수 없다.',['216ae6407ed243a6']),
21:('KEEP','MA§23(d)는 non-opioid II/III의90일 supply분기와 그 외30일분기를 구별한다. opioid와 nonnarcotic CII를 같은 quantity예외로 일반화하지 않는다.',['879439ccbb94f889']),
24:('SOURCE_BLOCKED','Adderall 현재§11에는 네 가지 amphetamine salts가 있으나 Dexedrine의 현재 정확 라벨 조회가404였다. 단일dextroamphetamine과 mixed salts의 명칭 차이는 보이나 해당 브랜드 구성 비교의 현재 직접라벨을 완결하지 못했다.',['83516f821f6a27d3']),
29:('KEEP','1308.12(d)(5)에 lisdexamfetamine이 명시되어 있으므로 prodrug라는 기전은II지정을 제거하지 않는다. Vyvanse§12.1의 dextroamphetamine prodrug 설명과 일치한다.',['b95308609ca5bd38','19f6e6144c7500ad']),
34:('KEEP','MA112§12D의 substitution은 동일 active ingredient/strength/dosage form의 법적 product선택 조건을 요구한다. 경구 methylphenidate와 Daytrana transdermal system의 delivery차이를 성분명 하나로 무시할 수 없다.',['eb2292f04d83820a','a024032395e490ca']),
35:('KEEP','MA112§12D의 동일 dosage form 조건과 Daytrana§11의 transdermal system을 대조했다. 성분명 동일만으로 다른 제형의 자동교체 권한을 만들지 않는다.',['eb2292f04d83820a','a024032395e490ca']),
39:('KEEP','Focalin§2.2는 racemic methylphenidate에서 시작할 때 총일일량의1/2을 명시한다. 따라서 같은mg으로 자동 치환하는 설명은 성립하지 않는다.',['0fd0012bde32f684']),
40:('KEEP','Focalin은 tablet, FocalinXR는 extended-release capsule로 각§3/11이 다르다. IR/XR분기를 구별한 명제만 확인하며 특정환자 전환용량은 인증하지 않는다.',['0fd0012bde32f684','e7eff367261570ca'])},
'appendix-a-2':{
35:('KEEP','1308.12(b)(1)은 hydrocodone을II로 직접 열거한다. 단일성분도 조합예외 없이II이다.',['b95308609ca5bd38']),36:('KEEP','1308.12(b)(1)의 preparations 범위와 Norco§11의 hydrocodone/APAP 조합을 함께 읽었다. APAP가 포함되어도hydrocodone II가 유지된다.',['b95308609ca5bd38','71b52788ca096df6']),39:('KEEP','Norco의hydrocodone/APAP는1308.12(b)(1)의hydrocodone preparation이다. codeine조합III의 규칙을 적용할 성분이 아니다.',['b95308609ca5bd38','71b52788ca096df6']),42:('KEEP','OxyContin§11은extended-release, Roxicodone§11은immediate-release이다. MA112§12D의dosage form조건과 대조하면 처방제품 구분을 생략한 동일취급이 불가하다.',['d5a0a6f87e071184','8731d9f86c9336d7','eb2292f04d83820a']),45:('KEEP','Percocet§11은oxycodone/APAP이며1308.12(b)(1)의oxycodone preparations II에 해당한다.',['5a5c60e180a56c2e','b95308609ca5bd38']),46:('KEEP','1308.13(e)(1)의조건부III조합은codeine에 관한 조항이다. Percocet의oxycodone을codeine으로 바꾸어 읽을 수 없다.',['518d30bed444e571','5a5c60e180a56c2e']),54:('KEEP','1308.12(b)(1)은hydrocodone과hydromorphone을 별도로 열거하며 Norco와Dilaudid§11의active성분도 다르다.',['b95308609ca5bd38','71b52788ca096df6','aeea2fd982f07afd']),55:('KEEP','서로 다른hydrocodone/hydromorphone은 MA112§12D의동일active ingredient 조건을 충족하지 않는다. 이름 유사성이 substitution근거가 아니다.',['eb2292f04d83820a','b95308609ca5bd38']),58:('KEEP','21CFR1306.04(c)는III–V OUD Rx경로를 별도로 두며1306.07의OTP narcotic administration/dispensing을 구분한다. MethadoneII를 일반pain Rx와 OUD OTP로 구별한 범위의 명제이다.',['386cb3e809e75e4b']),67:('SOURCE_BLOCKED','TIRF 개별 제품별 현재REMS와 공급상태를 이번 정확브랜드404자료로 완결할 수 없다.1308.12의fentanyl II만으로TIRF법적 접근경로를 인증하지 않는다.',['b95308609ca5bd38']),68:('SOURCE_BLOCKED','Actiq/Fentora/Lazanda/Subsys의현재exact FDA조회가실패했다. 표가재고보증이아니라는 한계는유지하되 현재생산·공급상태가검증되었다고판정하지 않는다.',[]),75:('KEEP','1308.14(b)(3)의tramadol IV와1308.12(c)(29)의tapentadol II를직접대조했다.',['80f2617da63c92a7','b95308609ca5bd38']),78:('KEEP','1308.12(b)(1)의codeine II에비해1308.13(e)(1),1308.15(c)는비마약성동반성분·함량조건을갖춘조합예외이다. 단일codeine에조합예외를적용하지 않는다.',['b95308609ca5bd38','518d30bed444e571','10ed3ddb11cfe00d'])},
'appendix-a-3':{
7:('KEEP','1308.12(f)(2)의FDA-approved oral-solution dronabinol은II이다. 모든dronabinol을III로묶지않는다.',['b95308609ca5bd38']),8:('KEEP','1308.12(f)(2)의제형조건은oral solution이다. 현재Syndros브랜드라벨까지확인했다는뜻은아니다.',['b95308609ca5bd38']),9:('KEEP','1308.12(f)(2)의oral solution II와1308.13(g)(1)의FDA-approved synthetic sesame-oil softgel III는서로다른조건분기이다.',['b95308609ca5bd38','518d30bed444e571']),12:('KEEP','1308.12(f)는nabilone과dronabinol oral solution을별도항목으로열거한다. 서로다른성분식별범위이다.',['b95308609ca5bd38']),13:('SOURCE_BLOCKED','nabilone의II지정은확인했으나 cannabidiol의현재정확라벨·성분정의까지이배치에서대조하지못했다. 명칭차이만으로비교전체를완료하지않는다.',['b95308609ca5bd38']),14:('KEEP','1308.13(g)(1)는synthetic dronabinol in sesame oil이라는조건을명시한다.',['518d30bed444e571']),15:('KEEP','1308.13(g)(1)는soft gelatin capsule제형을요구한다.',['518d30bed444e571']),16:('KEEP','1308.13(g)(1)는FDA-approved drug product조건을명시한다. 임의조제품에는그대로적용할수없다.',['518d30bed444e571']),17:('KEEP','1308.12(f)(2)의II oral solution이존재하므로dronabinol전제형이III라는일반화는성립하지않는다.',['b95308609ca5bd38','518d30bed444e571'])},
'appendix-a-5':{31:('KEEP','1308.13(f)(1)(84)는testosterone을anabolic steroid목록에명시한다.',['518d30bed444e571']),32:('KEEP','2025MAActsChapter16§7–8은라벨대체표시허용에Except as required by federal law/to extent allowable조건을둔다. 성별확정의료목적이연방라벨요구를삭제하지않는다.',['b081dd7831ee39ab','386cb3e809e75e4b']),33:('KEEP','1308.13(f)의testosterone III지정과1306.03/.04/.21의적법prescriber·purpose·처방조건이계속적용된다. GAC목적의MA라벨조정과연방처방제한소멸은다르다.',['518d30bed444e571','386cb3e809e75e4b','b081dd7831ee39ab']),36:('KEEP','1308.13(e)(1)(ii)는적격codeine조합의dose당90mg이하조건을명시한다. 이것만으로특정브랜드함량을확인한것은아니다.',['518d30bed444e571']),37:('KEEP','1308.13(e)(1)(ii)는하나이상의active nonnarcotic ingredient를함께요구한다.',['518d30bed444e571']),38:('KEEP','같은조항은그성분이recognized therapeutic amounts로존재해야한다고명시한다.',['518d30bed444e571']),47:('KEEP','1308.15(e)(5)의lacosamide V와1308.13(c)(11)의perampanel III는분류가다르다.',['10ed3ddb11cfe00d','518d30bed444e571']),49:('KEEP','1308.13(b)(2)는benzphetamine을stimulants하위에열거한다.',['518d30bed444e571']),50:('KEEP','1308.14(f)(9)의phentermine IV와1308.13(b)(2)의benzphetamine III를직접대조했다.',['80f2617da63c92a7','518d30bed444e571']),52:('KEEP','1308.13(b)(6)는phendimetrazine을stimulants하위에열거한다.',['518d30bed444e571']),53:('KEEP','1308.14(f)(9)의phentermine IV와1308.13(b)(6)의phendimetrazine III를직접대조했다.',['80f2617da63c92a7','518d30bed444e571']),56:('KEEP','1308.15(e)(7)의pregabalin V와1308.13(c)(11)의perampanel III를직접대조했다.',['10ed3ddb11cfe00d','518d30bed444e571'])}}
for uid,ds in custom.items():
 for num,(st,why,ks) in ds.items():ov(uid,num,st,why,[(k,'위 finding에 명시한 정확 조항/라벨 section') for k in ks])
# 수동으로 검토한 좁은 법규 비교를 product_row_id/claim suffix에 직접 묶는다.
def ridov(rid,suffix,status,why,refs):
 cs=[c for u in packet['units'] for c in u['claims'] if c.get('product_row_id')==rid and c['claim_id'].endswith('-'+suffix)]
 assert len(cs)==1,(rid,suffix,len(cs));byid(cs[0]['claim_id'],status,why,refs)
def rc(rid,suffix,why,ks,section):ridov(rid,suffix,'KEEP',why,[(k,section) for k in ks])
rc('B001','007','MA DPH reporting 안내는 gabapentin을ScheduleVI drug of concern으로지정하고II–V와함께PMP전송대상으로명시한다. Neurontin§9.1의연방비통제설명과별개이다.',['deef2ce4e7c3c4f4','a397fe32483f69ac'],'105CMR700.001 Additional Drug;700.012(A);MA DPH Who must report')
rc('B001','008','Neurontin§9.1은not a controlled substance라하고MA DPH는gabapentin VI/PMP보고를별도로정한다. 주보고와연방schedule을혼동하지않는비교이다.',['d14c2d777059b353','deef2ce4e7c3c4f4'],'NEURONTIN SPL§9.1;MA DPH gabapentin reporting')
rc('B001','009','1308.15(e)(7)는pregabalin을V에명시하며gabapentin의연방비통제설명과대조된다.',['10ed3ddb11cfe00d','d14c2d777059b353'],'21CFR1308.15(e)(7);NEURONTIN§9.1')
rc('B002','007','Horizant§11의gabapentin enacarbil prodrug와Neurontin§11의gabapentin은명칭·화학구조가다르다. 같은성분으로자동치환한다는주장이아니다.',['af49cfae42bfeaea','d14c2d777059b353'],'HORIZANT/NEURONTIN SPL§11')
for suff,why in [('007','Narcan 4mg nasal의dose는FDA승인공지의명시값4mg이다.'),('008','FDA2023-03-29공지는Narcan4mg nasal의OTC승인을명시한다. 모든naloxone제품으로확대하지않는다.'),('011','FDA공지는다른formulation/dosage의naloxone Rx status는유지된다고명시한다.')]:rc('B003',suff,why,['ee5ed9141f089516'],'FDA2023-03-29 Narcan4mg OTC approval;other formulations paragraph')
for suff,why in [('009','FDA2026-06-16공지는Rextovy4mg intranasal제품을명시한다.'),('010','FDA2026-06-16공지는Rextovy4mg nasal을처방없이직접구매할수있는OTC로승인했다.')]:rc('B003',suff,why,['a911d1e709aa4d8d'],'FDA2026-06-16 Rextovy OTC approval paragraphs1-2')
rc('B003','012','MA Policy2024-01은OTC발매후에도standing order를보험처리에사용할수있다고명시한다. 직접OTC구매와환자별order/profile/reporting경로를구별한다.',['7323a3006b2ccaf8'],'Policy2024-01 Naloxone Dispensing I-IV;revised2025-02-06')
rc('B004','006','FDA2023-07-28공지는RiVive3mg nasal을명시한다.',['e2d3387e5bf51c71'],'FDA2023-07-28 RiVive approval')
rc('B004','007','FDA2023-07-28공지는RiVive3mg nasal을OTC로승인했다.',['e2d3387e5bf51c71'],'FDA2023-07-28 RiVive OTC approval')
rc('B004','008','각FDA승인공지는RiVive3mg와Narcan/Rextovy4mg를명시한다. strength차이를동일mg제품으로취급하지않는다.',['e2d3387e5bf51c71','ee5ed9141f089516','a911d1e709aa4d8d'],'각FDA RiVive/Narcan/Rextovy approval의dose')
rc('B005','007','Kloxxado§3은한기기당8mg naloxone hydrochloride를명시한다.',['8e3e83250da8b18d'],'KLOXXADO SPL§3,§11')
rc('B005','008','FDAOTC승인공지의다른formulation/dose는Rx유지문구와Kloxxado현재Rx라벨을대조했다. 다른낮은용량OTC승인을8mg에복사하지않는다.',['ee5ed9141f089516','8e3e83250da8b18d'],'FDA NarcanOTC approval other formulations;KLOXXADO label')
for suff,name,k in [('007','naloxone','03f32bd3411dc78f'),('008','naltrexone','06c6d1d73778f3ce')]:rc('B006',suff,'Opvee§11의nalmefene과'+name+'제품§11은별개의active ingredient이다. 이름유사성으로같은약으로취급하지않는다.',['7b3adc3e1eecfa35',k],'각SPL§11 Description')
rc('B007','011','Vivitrol§1의alcohol dependence/relapse prevention치료와Narcan§1의급성opioid overdose emergency치료는목적이다르다.',['23fc04f8ccf96d04','03f32bd3411dc78f'],'VIVITROL/NARCAN SPL§1')
rc('B008','006','OpillDrugFacts와MA MassHealth order는dailycontinuous사용과응급피임용사용금지를명시한다.',['533e465d78e3037a','75f74b46ced25030'],'OPILL DrugFacts Uses/Directions;MassHealth order Protocol5(a)')
rc('B008','007','MassHealth2025-01-27order는회원/HSN적격자에게norgestrel0.075mg를보험order로조제하는절차이다. OTC구매자체와구분된다.',['75f74b46ced25030'],'MassHealth OTC oral contraceptive standing order Protocol1-7')
for suff,why in [('005','PlanBOne-StepDrugFacts active ingredient는levonorgestrel1.5mg이고Directions는1tablet경구용량이다.'),('006','현재PlanBOne-StepDrugFacts와HUMAN OTC제품라벨은해당제품의OTC상태를뒷받침한다.')]:rc('B009',suff,why,['d8a9d653ef9b636a'],'Plan B One-Step DrugFacts Active ingredient/Uses/Directions')
for suff,why in [('007','MA EC약국안내는levonorgestrelOTC의연령제한없음을명시한다.'),('008','MA안내는OTC직접구매와보험coverage를위한standing order처방조제를구별한다.'),('009','MA안내는levonorgestrel및ulipristal의statewide EC standing order경로를명시한다.')]:rc('B009',suff,why,['c8663b4a2c7e1972'],'MA Emergency contraception information for pharmacies;Standing Order/Access')
rc('B010','007','MA EC약국안내는ulipristal acetate/ella를statewide EC standing order대상으로명시한다.환자개별유효처방및counseling조건을따른다.',['c8663b4a2c7e1972'],'MA EC pharmacy guidance;ulipristal acetate standing order')
for rid,suffs in [('B011',['009','010','011','012']),('B012',['009'])]:
 for suff in suffs:rc(rid,suff,'DCP26-08-125의Contraceptives절은oral hormonal제품과patch만명명하고any-age/risk-assessment/12month/training조건을둔다. '+{'009':'해당patch경로를구별한다.' if rid=='B011' else 'vaginal ring은이열거경로에포함되지않는다.','010':'이열거를vaginal ring의포괄독립처방권한으로넓히지않는다.','011':'이열거를implant의포괄독립처방권한으로넓히지않는다.','012':'이열거를IUD의포괄독립처방권한으로넓히지않는다.'}[suff],['682aabe3c4ae1a78'],'DCP26-08-125 Hormonal Contraceptive Patches and Oral Hormonal Contraceptives(a)-(e)')
rc('B013','010','Depo-Provera§11은IMinjectable suspension,Provera§11은oraltablets이다. 같은generic이지만제형은다르다.',['75acf1c8bdda2694','b42286c75ef30597'],'DEPO-PROVERA/PROVERA SPL§11')
for suff,why in [('011','16CFR1700.14(a)(10)(xix)의예외는medroxyprogesterone acetate tablets라는정확한제형을명시한다.'),('012','해당예외는tablets로한정되어있으므로injection포장의예외근거로확장할수없다. 다른포장예외는이명제로판정하지않는다.')]:rc('B013',suff,why,['3c0c5d9726e8711b'],'16CFR1700.14(a)(10)(xix)')
for suff,why in [('007','Mifeprex현재§5.3은Mifepristone REMS제한프로그램을명시한다.'),('008','Mifeprex§5.3은Prescriber Agreement Form을통한prescriber certification을명시한다.'),('009','Mifeprex§5.3은certified pharmacies가certified prescriber의처방으로조제할수있다고명시한다.'),('010','Mifeprex§5.3은patient가Patient Agreement Form에서명하도록한다. 단순정보제공보다구체적인조건이다.'),('011','Mifeprex§1의misoprostol병용70일이내임신종결과ella§1의응급피임은서로다른적응증이다.')]:rc('B014',suff,why,['8fc6c04680786374']+(['44b79e9f73c74a9b'] if suff=='011' else []),'MIFEPREX SPL§1,§5.3;필요시ella§1')
for suff,why in [('007','Korlym§1은endogenous Cushing syndrome의hyperglycemia치료,Mifeprex§1은misoprostol병용임신종결로허가목적이다르다.'),('008','FDAmifepristoneQ&A는abortion제품REMS와Korlym다른indication을구별한다. generic명하나로REMS를복사하지않는다.'),('009','Korlym§3의300mgtablet과Mifeprex§3의200mgtablet은strength가다르며각regimen도다르다.')]:rc('B015',suff,why,['7cd85548c94d3c80','8fc6c04680786374']+(['8c6e5574f68a3ec4'] if suff=='008' else []),'KORLYM/MIFEPREX SPL§1,§3;FDA mifepristone Q&A Korlym')
rc('B016','007','Cytotec§11은misoprostol,Mifeprex§11은mifepristone을active성분으로한다. 두약은같은성분이아니다.',['b9124053835afd4e','8fc6c04680786374'],'CYTOTEC/MIFEPREX SPL§11')
for rid,suff in [('B017','008'),('B018','008')]:rc(rid,suff,'Truvada§11은tenofovir disoproxil fumarate,Descovy§11은tenofovir alafenamide를emtricitabine과결합한다. TDF와TAF를동일formulation으로취급하지않는다.',['cd9e5b6a5311e028','8c31ea817cf57398'],'TRUVADA/DESCOVY SPL§11')
rc('B019','008','DCP26-03-124는HIVprevention용cabotegravir투여를조건부허용하고DCP26-08-125는별도training/statewideguidance를따르는처방권한을정한다. 투여허용이독립처방전체허용이라는뜻은아니다.',['368bb8382bd0ca7e','682aabe3c4ae1a78'],'DCP26-03-124 eligible medication/general conditions;DCP26-08-125 HIV prevention')
rc('B020','010','Cabenuva§11은cabotegravir suspension과rilpivirine suspension의co-packaged제품을명시한다. cabotegravir단일Apretude와다르다.',['34ec33f97ddd6ca3'],'CABENUVA SPL§11')
rc('B020','011','Cabenuva§1은기존억제상태HIV-1치료대체요법,Apretude§1은HIV-1PrEP를적응증으로한다.',['34ec33f97ddd6ca3','a007be0d0da86679'],'CABENUVA/APRETUDE SPL§1')
rc('B021','009','Yeztugo§1은HIV-1PrEP,Sunlenca§1은다제내성HIV치료를정한다. 최신Sunlenca라벨의추가oral-loading내용도예방제품과동일하다는뜻이아니다.',['ca59111271b063b2','323eca9caf0cc23e'],'YEZTUGO/SUNLENCA SPL§1')
for suff,why in [('007','DCP26-03-124의eligibleSTI medications는ceftriaxone(IM injection)을명명한다. validRx/18세이상/훈련/CPR등일반조건을함께따른다.'),('008','DCP26-03-124의dispensing-by-administration조건(c)는not intravenous이고투여절은SC/IM만허용한다. ceftriaxoneIV라벨의존재가약사IV권한을만들지않는다.')]:rc('B024',suff,why,['368bb8382bd0ca7e'],'DCP26-03-124 Dispensing by Administration(c);STI medications;Administration and Dosing')
for suff,why in [('010','FDA는clozapineREMS를2025-06-13효력으로제거했다고공표했다.'),('011','FDA는REMS제거후에도ANCmonitoring을label에따라계속할것을권고한다.'),('012','FDA공지는neutropenia등안전위험·임상monitoring을유지하며REMS제거를모든안전관리의제거로설명하지않는다.')]:rc('B026',suff,why,['fbc9487ba46f65a6'],'FDA Clozapine REMS removal;effective2025-06-13;ANC recommendations')
for suff,why in [('009','FDAiPLEDGE안내는모든FDA승인isotretinoin제품이공유REMS하에있다고명시한다.'),('010','FDA공유프로그램의대상은isotretinoin제품이다. retinoid계열명만으로다른성분에적용한다는내용은없다.'),('011','FDA2026-06-16update는승인된변경의implementation을2026-11-15로연기했다고명시한다.'),('012','2026-11-04검토일에도11월15일은미래이다. 따라서11월3일에그예정변경을이미시행된규칙으로사용하지않는다.')]:rc('B027',suff,why,['97220482a752bfa2'],'FDA iPLEDGE June16,2026 update;sharedsystem;implementation2026-11-15')
for rid,suff,why in [('B028','007','FDA는ambrisentan/LetairisREMS를2025년4월제거했다.'),('B029','007','FDA는macitentan/Opsumit공유REMS를2025년4월제거했다.'),('B030','008','FDA는macitentan+tadalafil/Opsynvi공유REMS를2025년4월제거했다.'),('B031','007','FDA는aprocitentan/TryvioREMS를2025년4월제거했다.'),('B028','008','FDA는REMS제거후에도embryofetalrisk와pregnancycontraindication을label로유지한다고명시한다.'),('B029','008','FDA는macitentanREMS는제거했지만bosentan은fall2025수정후hepatotoxicityREMS를유지한다고구별한다.'),('B031','008','FDA는TryvioREMS제거후에도label로risk/mitigation을계속전달한다고설명한다.'),('B032','007','FDA는BosentanSharedSystemREMS를fall2025에수정승인했다고명시한다.'),('B032','008','수정은bosentan의embryofetaltoxicity관련REMS요구를제거한것이다. label의임신위험까지제거하지않는다.'),('B032','009','FDA는bosentan의hepatotoxicity관련REMS가유지된다고명시한다.'),('B033','006','FDA는FilspariREMS를fall2025에수정승인했다고명시한다.'),('B033','007','Filspari수정은embryofetaltoxicity관련REMS요구의제거이며label의위험정보는유지된다.'),('B033','008','FDA는Filspari의hepatotoxicity관련REMS가유지된다고명시한다.')]:rc(rid,suff,why,['3e29a0f4d0f32a01'],'FDA ERA REMS information;contentcurrent2026-03-04;April2025eliminations/fall2025modifications')
rc('B030','009','Opsynvi§11은macitentan+tadalafil복합제,Opsumit§11은macitentan단일제이다. 같은macitentan을포함해도동일제품이아니다.',['a345ee8056380447','2e86b17790584af0'],'OPSYNVI/OPSUMIT SPL§11')
rc('B034','007','FDA2025-09-25공지는CaprelsaREMS를당일제거했다고명시한다.',['34acd0a0bab6ea69'],'FDA2025-09-25 Caprelsa REMS removal')
rc('B034','008','FDA제거공지는Caprelsa의prescribing information이유지되고표준심장리듬안전관리이상별도certification은필요없다고설명한다. QT안전관리까지제거한것으로읽지않는다.',['34acd0a0bab6ea69'],'FDA2025-09-25 Caprelsa label/standardclinicalcare paragraphs')
section_default={'ec3b48bfddfcb0ac':'MGL94C§1 Narcotic drug definition','a397fe32483f69ac':'105CMR700.002(A)-(F);700.001 Additional Drug','c843cbe335da96c8':'DEA Controlled Substances Alphabetical List: finding에 특정한 성분 행 Other Names/Narcotic column','216ae6407ed243a6':'MGL94C§18(d),(d1/2),(d3/4)','879439ccbb94f889':'MGL94C§23(a),(d)','eb2292f04d83820a':'MGL112§12D generic substitution: active ingredients/strength/dosage form','b95308609ca5bd38':'21CFR1308.12(b)(1),(c),(d),(f): finding에 특정한 성분 entry','518d30bed444e571':'21CFR1308.13(b),(c),(e),(f),(g): finding에 특정한 성분 entry','80f2617da63c92a7':'21CFR1308.14(b),(c),(f),(g): finding에 특정한 성분 entry','10ed3ddb11cfe00d':'21CFR1308.15(c),(e): finding에 특정한 성분 entry','386cb3e809e75e4b':'21CFR1306.03,.04,.07,.13,.21,.22: finding에 특정한 조항','b081dd7831ee39ab':'MA Acts2025Chapter16§7-8'}
def ref(k,s,why=''):
 if s=='위 finding에 명시한 정확 조항/라벨 section':
  s=section_default.get(k,'SPL§1,§2,§3,§11,§12: 개별 판단에 명시한 비교 구획')
  rulekeys={'b95308609ca5bd38':'1308.12','518d30bed444e571':'1308.13','80f2617da63c92a7':'1308.14','10ed3ddb11cfe00d':'1308.15','386cb3e809e75e4b':'1306.'}
  if k in rulekeys:
   exact=list(dict.fromkeys(z for z in re.findall(r'130[468]\.\d+(?:\([A-Za-z0-9]+\))*',why) if z.startswith(rulekeys[k])))
   if exact:s='21 CFR '+', '.join(exact)+'; 개별 판단의 제품·조건 대조'
 return auth(k,s)
def extract(l,field,pattern=None):
 t=compact(l['sections'].get(field,''))
 if pattern:
  m=re.search(pattern,t,re.I)
  if m:return t[max(0,m.start()-60):min(len(t),m.end()+450)]
 return t[:650]
def facts(c):
 rid=c['product_row_id'];st=c['statement_ko'];kind=c['claim_kind'];ls=rowlabels.get(rid,[]);g=rows[rid]['generic'];basewhy=rid+' '+g+' 행의 '
 if kind in ['BRAND_ACTIVE_RELATION','BRAND_INGREDIENT_MEMBERSHIP']:
  if st.startswith('DEA의'):
   brand=st.split('명칭표는 ',1)[1].split('를 ',1)[0];chemical=st.split('를 ',1)[1].split('에 연결')[0];lines=(root/metas['c843cbe335da96c8']['text_path']).read_text().splitlines();hits=[ln for ln in lines if re.search(r'\b'+re.escape(brand)+r'\b',ln,re.I) and chemical.lower().split(' ')[0] in ln.lower()]
   if hits:return 'KEEP','DEA의 '+chemical+' 행 Other Names에 '+brand+'가 실제로 있다: '+compact(hits[0])+'. 이 명칭 연결만 확인하며 현재 판매·현행 제품 라벨을 보증하지 않는다.',[auth('c843cbe335da96c8','DEA alphabetical list: '+chemical+' row / Other Names')]
   return 'SOURCE_BLOCKED','DEA current alphabetical list에서 '+brand+'와 '+chemical+'의 정확한 같은 행 연결을 확인하지 못했다. 상위계열·유사브랜드의 행을 해당 명제의 증거로 대체하지 않는다.',[auth('c843cbe335da96c8','DEA alphabetical list: '+chemical+' exact-row limitation')]
  brand=st.split('의 ',1)[0];k=brandmap.get(brand.lower())
  if k:
   l=labelbykey[k];quote=extract(l,'description') or extract(l,'active_ingredient');expected=st.split('식별은 ',1)[-1].split('이다.')[0] if '식별은' in st else st.split('연결에는 ',1)[-1].split('가 포함')[0];return 'KEEP',brand+'의 현재 확보 SPL§11/active ingredient를 읽어 '+expected+' 연결을 대조했다. 직접 라벨 문구: '+quote+'. 제품명 검색결과만으로 법적 scope·현재 유통을 승인하지 않는다.',[auth(k,'SPL§11 DESCRIPTION;해당 active ingredient/active moiety')]
  return 'SOURCE_BLOCKED',brand+'의 정확한 현재 제품 라벨을 확보하지 못했다. '+rid+'의 같은 성분 다른 제품 라벨'+('('+','.join(ls)+')' if ls else '')+'만으로 이 브랜드의 전체 성분 구성을 확정하지 않는다. 실패 GET와 오래된 retained version의 한계는 source metadata에 남겼다.',[]
 if kind in ['FEDERAL_SCHEDULE','MASSACHUSETTS_CLASSIFICATION','MASSACHUSETTS_SCHEDULE']:
  if rid in fed:
   k,cl,why=fed[rid];refs=[auth(k,cl)];why=basewhy+why
   if kind!='FEDERAL_SCHEDULE':refs.append(auth('a397fe32483f69ac','105CMR700.002(A)-(E): corresponding21CFR1308 schedule incorporation'));why+=' MA700.002는 해당 연방목록을 같은I–V에 편입한다.'
   if 'nonnarcotic' in st:refs.extend([auth('ec3b48bfddfcb0ac','MGL94C§1 Narcotic drug'),auth('c843cbe335da96c8','DEA alphabetical list '+g+' row:Narcotic N')]);why+=' MA narcotic 정의와 DEA N표시도 대조하여 nonnarcotic 범위를 구별했다.'
   return 'KEEP',why,refs
  return 'SOURCE_BLOCKED',basewhy+st+'를 특정 제품 조건과 연결하는 controlling rule을 완결하지 못했다. constituent의 일반 분류와 product-specific exemption/함량 예외를 구분해야 한다.',[]
 if kind=='RX_AUTHORITY' or kind=='RX_PATHWAY':
  if rid in fed and not fed[rid][1].startswith('21 CFR1308.15'):
   return 'KEEP',basewhy+'해당 성분의'+fed[rid][1]+'와21CFR1306.03/.04/.21을 함께 대조했다. II/III/IV 스케줄이라는 사실과 적격 practitioner의 유효 처방 요건을 구별하여 Rx경로를 확인한다.',[auth(fed[rid][0],fed[rid][1]),auth('386cb3e809e75e4b','21CFR1306.03,.04;II .11/III-IV .21')]
  return 'SOURCE_BLOCKED',basewhy+st+'는 CV의 비처방 federal 예외와 MA dispensing 조건까지 구별해야 한다. 스케줄V 표기만으로 해당 Rx경로의 세부요건을 인증하지 않는다.',[auth('386cb3e809e75e4b','21CFR1306.21,.26;CV dispensing distinction')]
 if kind=='FEDERAL_UNSCHEDULED':
  if rid in ['B001','B002']:
   k=ls[0];return 'KEEP',g+'의현재SPL§9.1은명시적으로not a controlled substance라고설명한다: '+extract(labelbykey[k],'controlled_substance')+'. MA의VI/PMP지정과별도로연방명제를확인했다.',[auth(k,'SPL§9.1 Controlled Substance')]
  if rid in ['B003','B004','B005','B006','B007']:return 'KEEP',g+'은21CFR1308.12(b)(1)의opium/opiate범위에서명시적으로제외되는'+{'B003':'naloxone','B004':'naloxone','B005':'naloxone','B006':'nalmefene','B007':'naltrexone'}[rid]+'이다. 현재1308.11–.15의다른목록과해당성분을대조했다. opioid agonist의schedule을antagonist에복사하지않는다.',[auth('b95308609ca5bd38','21CFR1308.12(b)(1):namedexceptions'),auth('518d30bed444e571','21CFR1308.13 entries'),auth('80f2617da63c92a7','21CFR1308.14 entries'),auth('10ed3ddb11cfe00d','21CFR1308.15 entries')]
  return 'SOURCE_BLOCKED',g+'의FDA허가·Rx/OTC표기는확보했으나이는연방schedule부존재의직접법규증거가아니다. 현재모든목록의명명·포괄정의예외까지이성분에대해완결한근거를제시하지못하므로비통제명제를보류한다.',[auth(ls[0],'SPL§11:ingredientidentificationonly') ] if ls else []
 if kind in ['MA_SCHEDULE_VI']:
  if rid=='B001':return 'KEEP','MA DPH는gabapentin을명시적으로ScheduleVI drug of concern이라부른다.700.002(F)의prescription/residual분류와함께확인했다.',[auth('deef2ce4e7c3c4f4','MA DPH Pharmacy reporting:Gabapentin prescriptions/VI'),auth('a397fe32483f69ac','105CMR700.002(F)')]
  if rid=='B007':return 'KEEP','naltrexone은1308.12(b)(1)의명시적제외성분이며현재Vivitrol/Naltrexone라벨은Rx제품이다.700.002(F)는다른schedule에없는prescriptiondrug를VI로분류한다.',[auth('b95308609ca5bd38','21CFR1308.12(b)(1) naltrexoneexception'),auth('a397fe32483f69ac','105CMR700.002(F)'),auth(ls[0],'SPLprescriptionproduct;§11')]
  return 'SOURCE_BLOCKED',g+'의MA VI주장은700.002(F)의residual prescription범주와연결되지만,이제품의연방I–V비해당조건을이감사에서완결하지못했다. Rx라벨확인만으로그조건을자동충족시켜VI를PASS하지않는다.',[auth('a397fe32483f69ac','105CMR700.002(F) residualprescriptiondrug')]+([auth(ls[0],'SPL§11;Rxproductidentificationonly')] if ls else [])
 if kind=='PRODUCT_RX_STATUS':
  if ls:
   k=ls[0];l=labelbykey[k];raw=txt(k)
   if re.search(r'\brx\s+only\b|prescription (medicine|drug)|prescription status',raw,re.I):
    m=re.search(r'\brx\s+only\b|prescription (medicine|drug)',raw,re.I);quote=raw[max(0,m.start()-90):m.end()+160] if m else 'labelのprescription표시'
    return 'KEEP',g+'의표에명시된Rx제품에대해현재라벨의prescription표시를직접확인했다: '+quote+'. 성분전체의모든제형이Rx라는뜻은아니다.',[auth(k,'SPLprescription/Rx-only labeling;§11 productidentity')]
  return 'SOURCE_BLOCKED',g+'의해당Rx제품표시를현재정확라벨본문의Rx-only표시와직접연결하지못했다. FDA검색index의product_type값만으로법적Rx판정을완결하지않는다.',[auth(ls[0],'SPL:product_typeindexaloneinsufficient')] if ls else []
 # 아래는 단순 제품 사실만 수락. 범위·자동대체·권한·일반화는 별도 수동 판정/보류.
 if any(z in st for z in ['자동','동일','다르','구별','확인','별도','분기','권한','규칙','제거','REMS','인증','certified','직접 제공','직접 dispense','환자에게','monitoring','감독','관찰','workflow','경로','해석','전부','아니다','아닌','판매','제한','조건','적격','exempt','exemption']):
  quotes=[];aa=[]
  for k in ls[:2]:quotes.append('/'.join(labelbykey[k]['openfda'].get('brand_name',[]))+': '+extract(labelbykey[k],'description')[:260]);aa.append(auth(k,'SPL§11 productfactonly;scopeclaimnotestablished'))
  return 'SOURCE_BLOCKED',basewhy+'「'+st+'」에서제품사실과법적효과를분리했다. '+('직접읽은제품정보는 '+' / '.join(quotes)+'. ' if quotes else '정확한현재제품라벨이확보되지않았다. ')+'이사실만으로명제의범위·대체·권한·절차까지결론낼수있는직접조항연결을완결하지못하여보류한다.',aa
 termgroups=[]
 for ko,eng in [('경구',r'oral|orally'),('sublingual',r'sublingual'),('구강점막',r'buccal|sublingual|transmucosal'),('transdermal',r'transdermal'),('buccal',r'buccal'),('subcutaneous',r'subcutaneous'),('Subcutaneous',r'subcutaneous'),('Intramuscular',r'intramuscular'),('intramuscular',r'intramuscular'),('nasal',r'nasal|intranasal'),('Nasal',r'nasal|intranasal'),('rectal',r'rectal'),('주사',r'inject'),('injection',r'inject'),('Injection',r'inject'),('film',r'film'),('Film',r'film'),('tablet',r'tablet'),('Tablet',r'tablet'),('capsule',r'capsule'),('gel',r'\bgel\b'),('Spray',r'spray'),('spray',r'spray'),('Patch',r'patch|transdermal'),('Ring',r'ring'),('extended-release',r'extended.release'),('Extended-release',r'extended.release'),('ER',r'extended.release'),('IR',r'immediate.release'),('stimulant',r'stimulant'),('prodrug',r'prodrug'),('benzodiazepine',r'benzodiazepine'),('hypnotic',r'hypnotic'),('opioid',r'opioid|opiate'),('analgesic',r'analgesic'),('anesthetic',r'anesthe'),('seizure',r'seizure'),('Overdose',r'overdose'),('Emergency contraception',r'emergency contracept|prevent pregnancy'),('Contraceptive',r'contracept|prevent pregnancy'),('Daily',r'every day|daily|one tablet'),('OUD',r'opioid.*(?:dependence|disorder)|dependence.*opioid'),('AUD',r'alcohol.*dependence'),('Antipsychotic',r'antipsychotic'),('Retinoid',r'retinoid'),('Endothelin receptor antagonist',r'endothelin.*receptor antagonist'),('Oncology',r'cancer'),('Antibacterial',r'antibacterial|antibiotic'),('Long-acting',r'extended.release|long.acting')]:
  if (ko in st if ko in ['ER','IR','OUD','AUD'] else ko.lower() in st.lower()):termgroups.append(eng)
 if 'HIV prevention' in st:termgroups.append(r'pre.exposure prophylaxis|PrEP')
 if 'HIV treatment' in st:termgroups.append(r'treatment of HIV|HIV.1.*treatment|HIV.1.*infect')
 if 'solution' in st:termgroups.append(r'solution')
 if 'suspension' in st:termgroups.append(r'suspension')
 if not termgroups:return 'SOURCE_BLOCKED',basewhy+'「'+st+'」를읽었으나현재공식자료의정확한성분·기전·제형구획과직접대응하는근거를완결하지못했다. author분류는독립법규판정을대신하지않는다.',[]
 for k in ls:
  l=labelbykey[k];allfields=' '.join(v for f,v in l['sections'].items() if f not in ['warnings_and_cautions','boxed_warning'])
  if all(re.search(pat,allfields,re.I) for pat in termgroups):
   # 첫 번째 필드에 키워드가 없는 경우 다음 실제 일치 필드로 이동한다.
   evidence=[]
   for pat in termgroups:
    for field in ['description','indications_and_usage','dosage_forms_and_strengths','dosage_and_administration','clinical_pharmacology','controlled_substance','drug_abuse_and_dependence','active_ingredient','purpose']:
     if re.search(pat,l['sections'].get(field,''),re.I):evidence.append((field,extract(l,field,pat)));break
   evidence=list(dict.fromkeys(evidence));return 'KEEP',basewhy+'「'+st+'」를현재'+('/'.join(l['openfda'].get('brand_name',[])))+'라벨의해당구획과대조했다. '+ ' / '.join(f+' 원문: '+q for f,q in evidence)+'. 이판정은기재된제형·역할명제에한정하며별도조제·투여권한을부여하지않는다.',[auth(k,'SPL '+','.join(f for f,q in evidence)+' (fulltextpreserved)')]
 return 'SOURCE_BLOCKED',basewhy+'「'+st+'」에필요한'+','.join(termgroups)+'의동시제품근거를확보하지못했다. '+('확보라벨은'+','.join('/'.join(labelbykey[k]['openfda'].get('brand_name',[])) for k in ls)+'이며다른route/release/적응증또는옛브랜드를대신사용하지않는다.' if ls else '정확한현재브랜드라벨조회가실패했거나오래된버전뿐이다.'),[auth(k,'SPL§1/§11:claimedform/roleunresolved') for k in ls[:2]]
exec(open('/tmp/final86-d-final-overrides.py').read())
omissions=collections.defaultdict(list)
missing=[]
def om(uid,rid,text,why,near):
 item={'unit_id':uid,'product_row_id':rid,'omitted_proposition_ko':text,'body_excerpt':rows[rid]['line'],'why_not_covered_ko':why,'nearest_existing_claims':near,'legal_status':'LEGAL_HOLD','required_action_ko':'원문 법규명제를 보존한 채 해당 원자를 census에 별도 추가하고 현재 controlling rule과 제품조건으로 독립 재검토한다. 이 감사는 원문/census를 수정하지 않는다.'};missing.append(item);omissions[uid].append(rid+': '+text+' — '+why+' (구체 매핑: completeness-omission-map.json)')
for rid in ['A006','A007','A008','A009','A010','A011','A013','A015','A016']:
 u=[x for x in packet['units'] if x['unit']['id']=='appendix-a-2'][0];near=[c['claim_id'] for c in u['claims'] if c.get('product_row_id')==rid];om('appendix-a-2',rid,rid+'의 해당 opioid 제품은 MA에서도 CII 규칙의 대상이다.','Federal/MA 열의 두 번째 “Opioid·CII 규칙”은 MA 법규효과이다. 기존 FEDERAL_SCHEDULE 및 opioid 임상역할 명제는 MA700.002 편입의 독립 원자를 대체하지 않는다.',near)
u=[x for x in packet['units'] if x['unit']['id']=='appendix-a-2'][0];om('appendix-a-2','A017','단일성분 codeine의 연방 schedule은II이다.','원문의Federal열은II를명시하지만A017에는FEDERAL_SCHEDULE 원자가없다. oral/opioid 및 CIII/CV조합예외 배제는 긍정적인II지정을 원자화한 명제와 다르다.',[c['claim_id'] for c in u['claims'] if c.get('product_row_id')=='A017'])
for uid,rids,schedule in [('appendix-a-3',['A019'],'II'),('appendix-a-5',['A033','A034','A035'],'III'),('appendix-a-7',['A039','A040','A042','A044','A045','A047','A048'],'IV')]:
 u=[x for x in packet['units'] if x['unit']['id']==uid][0]
 for rid in rids:om(uid,rid,rid+'의 해당 제품은 MA Schedule'+schedule+' 분기이다.','Federal/MA 두 번째 열의 C'+schedule+' 식별/Rx 규칙은 MA분류를 표현한다. 기존 연방 schedule 원자와 일반 Rx authority만으로 MA700.002 편입 명제까지 전수목록에 있다고 볼 수 없다.',[c['claim_id'] for c in u['claims'] if c.get('product_row_id')==rid])
# 이미 직접 읽은 숫자/trigger/예외의 수동 기록을 실제 assigned hashes에 binding한다.
records=[];flat=[]
for u in packet['units']:
 uid=u['unit']['id'];cs=[]
 if uid in manual:assert len(manual[uid])==len(u['claims']),(uid,len(manual[uid]),len(u['claims']))
 for i,c in enumerate(u['claims'],1):
  cid=c['claim_id'];statement=c['statement_ko']
  if cid in overrides:
   status,why,refs=overrides[cid];aa=[ref(k,s,why) for k,s in refs]
  elif uid in manual:
   status='KEEP';why=manual[uid][i-1];aa=[]
   for a in [c]+c.get('additional_authorities',[]):
    if a.get('official_url'):
     k=keyurl(a['official_url']);section='; '.join(a.get('authority_clauses',[])) or a.get('exact_section_context','')
     if k in metas and metas[k].get('status_code')==200:aa.append(auth(k,section or why.split('는')[0]))
   if uid=='w2-b-14' and i==6:aa=[auth('386cb3e809e75e4b','21CFR1306.13(c)'),auth('879439ccbb94f889','MGL94C§23(a)')]
   if uid=='w2-b-14' and i==3:aa.append(auth('216ae6407ed243a6','MGL94C§18(d3/4)'))
   if uid=='w4-d-13' and i in [31,32,33] or uid=='w4-d-15' and i==11:aa.extend([auth('5f0921038b308175','21USC353b(b)(5)'),auth('f5e992ffdcba530d','FDA503B adverse event reporting guidance III.A-C,H;310.305(c),(g)')])
   if uid=='w4-d-15' and i==11:
    for a in aa:
     if '310.305(f)' in a['exact_section']:a['exact_section']=a['exact_section'].replace('310.305(f)','310.305(g)')
   if uid=='w4-d-15' and i==30:
    for a in aa:a['exact_section']='21CFR1304.04(b)(2),(h);readableequipment/electronicprescriptionrecords'
   if uid=='w6-a-15' and i in [8,10,14]:aa.append(auth('d00d60a208a6ff0a','HHS-OIG Fraud & Abuse Laws:AKS/safeharbors/Stark'))
  else:status,why,aa=facts(c)
  assert status!='KEEP' or aa,(uid,cid)
  why=re.sub(r'(?<=[A-Za-z0-9])(?=[가-힣])|(?<=[가-힣])(?=[A-Za-z0-9])',' ',why).replace('labelの','라벨의 ')
  item={'claim_id':cid,'claim_record_sha256':job['unit_bindings'][uid]['claim_record_sha256s'][cid],'statement_ko':statement,'claim_read_completely':True,'legal_status':status,'finding':why,'authorities':aa}
  if status!='KEEP':item['blocker']=why
  cs.append(item);flat.append(item)
 comp='OMISSIONS_FOUND' if omissions[uid] else 'COMPLETE';legal='LEGAL_HOLD' if omissions[uid] or any(c['legal_status']=='LEGAL_HOLD' for c in cs) else 'SOURCE_BLOCKED' if any(c['legal_status']=='SOURCE_BLOCKED' for c in cs) else 'KEEP'
 records.append({'unit_id':uid,'binding':job['unit_bindings'][uid],'body_read_completely':True,'all_claim_records_read_completely':True,'completeness':comp,'completeness_method':'현재 exact body 전문을 제목·문장·표의 행/열별로 분해하여 all assigned claim statements와 역방향 대조했다. 숫자·기한·trigger·의무주체·예외·성분별/브랜드별·제형·연방/MA분류·권한·비교조건을 별도로 확인했고, 단순 명제 수나 author complete표시를 완전성 근거로 쓰지 않았다. 누락 항목과 근접 claim IDs는 completeness-omission-map.json에 구체적으로 연결했다.','omissions':omissions[uid],'legal_status':legal,'claims':cs})
report={k:job[k] for k in ['stage','actor_provenance','auditor','auditor_instance']};report.update(independent_of_authors=True,canonical_audit=False,canonical_release_credit=0,question_audit_credit=0,review_date='2026-11-04',methodology_ko='동일 actual GPT instance가 배정된20개 current body와1084개 exact census 명제를 전부 읽고 관련8문항의 모든보기/정답/전체해설 및118개 파생자료 전문을 대조했다. Author source-checked/census-complete는 법규권위가 아니며 판단은 현재 공식원문·직접 제품라벨·controlling rule에 제한한다. 미확인 제품·법적효과는 SOURCE_BLOCKED, 모호한 법적효과/누락은LEGAL_HOLD이다. 동명 성분의 다른제형/역사적 브랜드/색인 조회를 현행 제품규칙에 대신 사용하지 않는다.',records=records)
(base/'audit-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');(base/'completeness-omission-map.json').write_text(json.dumps(missing,ensure_ascii=False,indent=2)+'\n');(base/'claim-review-table.json').write_text(json.dumps([{'claim_id':c['claim_id'],'statement_ko':c['statement_ko'],'legal_status':c['legal_status'],'finding':c['finding'],'source_sections':[(a['official_url'],a['exact_section']) for a in c['authorities']]} for c in flat],ensure_ascii=False,indent=2)+'\n')
print('claims',len(flat),collections.Counter(c['legal_status'] for c in flat),'omissions',len(missing));print([(r['unit_id'],r['completeness'],r['legal_status'],collections.Counter(c['legal_status'] for c in r['claims'])) for r in records])
