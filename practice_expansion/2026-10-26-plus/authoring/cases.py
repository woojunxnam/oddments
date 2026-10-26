"""Original single-scenario, reproducible boundary/record applications.

Nine deliberately related exercises per model; not nine independent legal rules.
No actual/remembered exam question is an input. All amounts are hypothetical.
"""
from datetime import date, timedelta
CASES=[]

def case(family,topic,area,units,scenario,lead,options,answer,reason, facts, authority):
    assert len(options)==4 and len(set(x[0] for x in options))==4
    CASES.append(dict(family=family,topic=topic,area=area,units=units,scenario=scenario,lead=lead,
        options=[dict(text=t,reason_ko=r,correct=i==answer) for i,(t,r) in enumerate(options)],
        reason=reason,facts=facts,authority=authority,style='single-case'))

def numeric(family,topic,area,units,scenario,lead,correct,alternatives,reason,facts,authority,unit='contact hours'):
    vals=[correct]+[v for v in alternatives if v!=correct]
    for delta in [1,2,3,5,10,20]:
        if len(set(vals))>=4:break
        if correct+delta not in vals:vals.append(correct+delta)
    vals=list(dict.fromkeys(vals))[:4]
    opts=[]
    for v in vals:
        display_unit = unit[:-1] if v==1 and unit.endswith('s') else unit
        txt=f'{v:g} {display_unit}' if isinstance(v,(int,float)) else str(v)
        opts.append((txt,reason if v==correct else f'이 선택지({v})는 조건에 따른 계산 결과({correct})와 다르다. '+reason))
    case(family,topic,area,units,scenario,lead,opts,0,reason,facts,authority)

CE='Policy 2021-04 §§I–VII, revised September 4, 2025; 247 CMR 4.03'
# SC01: daily ceiling combined with annual total.
for prior,day in [(9,10),(10,11),(11,12),(12,9),(13,10),(14,12),(8,9),(7,11),(6,10)]:
    allowed=min(day,8);need=max(0,20-prior-allowed)
    numeric('SC01','Annual CE credit after a one-day conference',1,['w1-a-6'],
      f'A Massachusetts pharmacist who does not practice CDTM has {prior} eligible CE contact hours. The pharmacist then completes {day} eligible hours at a conference on one calendar day. All live, law, and specialized-topic requirements are otherwise satisfied; the question concerns only the 20-hour total.',
      'How many additional eligible contact hours are needed for that calendar year?',need,[max(0,20-prior-day),20-prior,need+2],
      f'하루 인정 상한은 8시간이다. {prior}+{allowed}={prior+allowed}시간이므로 20시간까지 {need}시간을 더 채운다. 실제 수강 {day}시간을 모두 산입하지 않는다.',
      dict(prior=prior,one_day=day),CE)
# SC02: home study does not replace live minimum.
for total,live in [(20,0),(21,1),(22,2),(23,3),(24,4),(19,2),(18,3),(17,4),(16,1)]:
    need=max(5-live,20-total)
    numeric('SC02','Planning the remaining live CE',1,['w1-a-6'],
      f'A non-CDTM pharmacist has completed {total} eligible contact hours this year, of which {live} are live and the rest home study. The law and any specialized-topic requirements are satisfied. New live hours can be completed on separate days within the daily limit.',
      'What is the minimum number of additional live hours that satisfies both the annual total and live requirement?',need,[max(0,20-total),5,need+1],
      f'연간 total 20과 live 최소 5를 함께 충족한다. Total 부족은 {max(0,20-total)}, live 부족은 {5-live}이므로 적격 live {need}시간이 최소이다.',
      dict(total=total,live=live),CE)
# SC03: no carryover and current-year law deficit.
for current,law,previous in [(18,0,25),(19,0,28),(20,0,24),(18,1,22),(19,1,26),(20,1,21),(17,1,30),(16,0,24),(21,0,23)]:
    need=max(20-current,2-law)
    numeric('SC03','Prior-year excess and current-year law CE',1,['w1-a-6'],
      f'A non-CDTM pharmacist completed {previous} hours last year. This year the record contains {current} eligible hours, including {law} approved law hours; live and other specialized requirements are satisfied. Additional approved law courses will be spread across permissible days.',
      'How many additional current-year law hours are minimally sufficient to finish both the total and law requirements?',need,[max(0,20-current-(previous-20)),2-law,need+2],
      f'전년도 초과 시간은 carry over하지 않는다. 현재 total 부족 {max(0,20-current)}와 law 부족 {2-law} 중 큰 값인 {need}시간을 적격 law로 채우면 된다.',dict(current=current,law=law,previous=previous),CE)
# SC04: overlapping categories do not double actual hours.
for total,live,law in [(17,2,0),(18,3,0),(19,4,0),(16,1,1),(18,2,1),(20,3,1),(15,4,0),(19,1,0),(21,2,0)]:
    need=max(20-total,5-live,2-law)
    numeric('SC04','One course meeting live and law categories',1,['w1-a-6'],
      f'A pharmacist has {total} actual CE hours, including {live} live hours and {law} approved law hours. The pharmacist will take live law CE that qualifies for both categories; other requirements are satisfied.',
      'What is the minimum actual duration of additional live law CE needed, assuming daily limits are respected?',need,[max(0,20-total),max(0,2-law),need+3],
      f'추가 live-law 한 시간은 두 category를 동시에 채우지만 total에는 한 시간이다. max(20−{total},5−{live},2−{law})={need}시간이다.',dict(total=total,live=live,law=law),CE)
# SC05: CDTM 25 total, 5 related, regardless of number of agreements.
for total,related,agreements in [(20,0,1),(21,1,2),(22,2,3),(23,3,1),(24,4,2),(20,5,3),(22,5,2),(24,1,1),(25,2,3)]:
    need=max(25-total,5-related)
    numeric('SC05','CDTM CE across more than one agreement',1,['w1-a-8','w3-d-4'],
      f'A pharmacist participates in {agreements} CDTM agreement(s) this calendar year and has {total} eligible actual CE hours, including {related} hours generally related to the agreement areas. Live, law, and applicable pain-training requirements are satisfied. New practice-related CE will be eligible and within daily limits.',
      'What is the minimum additional practice-related CE needed under the stated annual requirements?',need,[max(0,20-total),max(0,25-total),need+5],
      f'CDTM의 최소치는 total 25와 관련 추가 5시간이다. 여러 agreement라는 이유만으로 5시간을 agreement 수만큼 자동 누적하지 않는다. 필요한 추가시간은 max(25−{total},5−{related})={need}.',dict(total=total,related=related,agreements=agreements),CE)
# SC06: precise grace trigger; year chosen is the study edition, not a prediction of future law.
for month,day in [(1,5),(5,30),(8,1),(9,29),(9,30),(10,1),(10,16),(11,20),(12,18)]:
    issued=date(2026,month,day); grace=month>=10
    opts=[('December 31, 2026','10월 1일 이전 면허는 이 특정 grace period의 대상이 아니므로 일반 연말 완료기한을 적용한다.'),
          ('April 30, 2027','10월 1일 또는 그 이후 exam/transfer 면허 취득자는 그 해 필요한 시간을 다음 해 4월 30일까지 완료하는 grace period가 있다.'),
          ('No CE is required for 2026','졸업연도 면제와 새 면허 취득일에 따른 grace period를 혼동한 결론이다.'),
          ('Two years after the license issue date','개인별 발급일로 연간 CE의 달력을 새로 만드는 규칙이 아니다.')]
    case('SC06','New Massachusetts license: deadline or exemption',1,['w1-a-7'],
      f'A pharmacist graduated from an ACPE school in 2021 and first obtains a Massachusetts license by transfer on {issued:%B %d, %Y}. No other CE exception applies.',
      'Under the currently posted CE policy, which deadline applies to the CE required for 2026?',opts,1 if grace else 0,
      opts[1 if grace else 0][1]+' 2021 졸업의 면제를 2026 면허취득연도로 이동시키지 않는다.',dict(issued=issued.isoformat(),graduated=2021),CE)
# SC07: materially distinct exemption/grace facts, not a series of graduation-year swaps.
ce_rows=[
 ('The pharmacist graduated from an ACPE school during 2026 and first became licensed in July 2026.',0,'ACPE graduation calendar year가 2026이므로 해당 general CE 졸업연도 면제를 적용한다.'),
 ('The pharmacist graduated in 2021 and first transferred into Massachusetts in May 2026.',1,'과거 졸업 면제를 새 transfer 연도에 다시 적용하지 않는다.'),
 ('The pharmacist graduated in 2021 and first transferred into Massachusetts on October 1, 2026.',2,'October1 또는 그 이후 최초 exam/transfer 면허는 해당연도 완료기한 grace를 검토한다.'),
 ('The pharmacist graduated in 2021 and first transferred into Massachusetts on September 30, 2026.',1,'September30은 October1 이후 grace trigger 전이다. 이 특정 grace가 적용되지 않는다.'),
 ('The pharmacist graduated from an ACPE school during 2026 and first became licensed in November 2026.',0,'Graduation-year 면제가 성립하는 사실을 단순 late-year grace로 바꾸어 CE 의무를 새로 만들지 않는다.'),
 ('The pharmacist first received a Massachusetts license in 2022, renewed it in November 2026, and graduated in 2021.',1,'오래전 최초 면허의 renewal를 그해 최초 exam/transfer license 취득으로 취급하지 않는다.'),
 ('The pharmacist graduated in 2021, transferred in August 2026, and completed 40 CE hours during 2025 but none during 2026.',1,'전년도 초과교육은 carryover되지 않으며 graduation exemption도 아니다.'),
 ('The pharmacist graduated in 2021 and first became licensed by examination in December 2026.',2,'Late-year grace는 transfer뿐 아니라 examination 경로에도 해당한다.'),
 ('The pharmacist graduated in 2021 and transferred in July 2026; the employer will reimburse courses only in the next calendar year.',1,'Employer reimbursement 일정은 법정 CE 면제나 grace 근거가 아니다.')]
opts=[('The 2026 ACPE graduation-year exemption applies.','실제 graduation calendar year에 해당하는지 확인한다.'),('Ordinary 2026 CE requirements remain due; no stated fact establishes this exemption or grace period.','General 연간요건을 유지하며 명시된 exemption/grace 조건을 별도로 판정한다.'),('The late-year licensing grace period permits completion of required 2026 hours by April 30, 2027.','그해10월1일 이후 최초 exam/transfer license 조건에 해당한다.'),('Any first renewal automatically waives the previous two years of CE.','이와 같은 포괄적 first-renewal 면제를 만들 수 없다.')]
for facts,ix,reason in ce_rows:
    case('SC07','Distinguishing an exemption from an extension',1,['w1-a-7','w1-a-6'],
      facts+' No military, hardship, or specialized-practice exception is being claimed.',
      'Which assessment of the general 2026 CE obligation is supported?',opts,ix,reason,dict(record=facts),CE)
# SC08: specialist CE requirements, actual duties vary rather than name swaps.
scenarios=[('personally compounds sterile preparations','sterile',5),('supervises personnel preparing sterile preparations','sterile',5),('performs final verification of finished CSPs for one week','sterile',5),('oversees the sterile-compounding operation','sterile',5),('personally compounds complex nonsterile preparations','complex nonsterile',3),('supervises complex nonsterile compounding','complex nonsterile',3),('performs final verification of finished complex nonsterile preparations','complex nonsterile',3),('physically administers routine vaccines','immunization',1),('directly supervises others administering vaccines','immunization',1)]
for activity,subject,hours in scenarios:
    numeric('SC08','Specialized CE follows the work performed',1,['w1-a-8'],
      f'During the calendar year, a Massachusetts pharmacist {activity}. The pharmacist does not engage in CDTM. The question concerns the specialized subject requirement, not the total 20-hour requirement.',
      f'How many eligible {subject} CE contact hours are required for this practice role under the current Board policy?',hours,[0,2,3 if hours!=3 else 5],
      f'이 업무에는 연간 {subject} {hours}시간 요건을 적용한다. 해당 specialized hours는 기본 20시간에 산입 가능하며, 임시 업무라고 자동 면제되지 않는다.',dict(activity=activity),CE)
# SC09: distinct renewal clocks, nine documented situations.
renewals=[('pharmacist personal registration','December 31 of the even-numbered renewal year'),('resident Drug Store pharmacy license','December 31 of the odd-numbered renewal year'),('nonresident Drug Store pharmacy license','December 31 of the odd-numbered renewal year'),('sterile-compounding pharmacy license','December 31 every year'),('complex nonsterile-compounding pharmacy license','December 31 every year'),('institutional sterile-compounding pharmacy license','December 31 every year'),('nonresident sterile-compounding pharmacy license','December 31 every year'),('pharmacy technician license','The licensee’s birthdate in its two-year renewal cycle'),('nonresident complex nonsterile-compounding pharmacy license','December 31 every year')]
renew_options=[('December 31 of the even-numbered renewal year','Pharmacist 개인 registration의 일반 짝수 해 달력이다.'),('December 31 of the odd-numbered renewal year','일반 resident/nonresident Drug Store license의 홀수 해 달력이다.'),('December 31 every year','해당 compounding license의 annual renewal 달력이다.'),('The licensee’s birthdate in its two-year renewal cycle','Technician의 2년 생일 기준 달력이다.')]
for kind,right in renewals:
    idx=[x[0] for x in renew_options].index(right)
    case('SC09','Matching the license to its renewal calendar',1,['w1-a-4','w1-b-5','w1-c-2'],
      f'The compliance calendar has a row for a Massachusetts {kind}. The manager must use that license’s ordinary expiration cycle, not the renewal date of another credential.',
      'Which calendar entry matches this credential?',renew_options,idx,f'{kind}에는 {right}를 적용한다. 개인·시설·특수면허의 갱신 주기를 합치지 않는다.',dict(credential=kind),'247 CMR 4.02,8.07,6.05–6.09')
# SC10: lapse/discipline branch with no ambiguous boundary at exactly two years.
for months,disciplinary in [(1,False),(3,False),(8,False),(18,False),(23,False),(25,False),(30,False),(25,True),(36,True)]:
    if months<=2:ix=0
    elif months<=24:ix=1
    elif disciplinary:ix=3
    else:ix=2
    opts=[('Stop practice; the ordinary 60-day additional-condition threshold has not yet been crossed.','만료 후 업무 유예는 없으며, 아직 60일 초과의 추가조건과 구분한다.'),('Stop practice and satisfy applicable Board reinstatement conditions; MPJE is not automatic from this duration alone.','일반 lapse 60일 초과는 Board 조건이 필요하지만 2년 초과 조항과 다르다.'),('Satisfy the MPJE requirement and other applicable Board conditions before ordinary renewal.','일반 nonrenewal 2년 초과에는 MPJE 및 기타 Board 조건이 선행한다.'),('Satisfy the disciplinary restoration conditions including MPJE; the Board may also require NAPLEX.','Suspended/revoked 2년 초과 경로에는 MPJE와 기타 조건, Board 재량 NAPLEX 가능성을 구별한다.')]
    scenario=f'A pharmacist has been {"suspended or revoked under a Board disciplinary order" if disciplinary else "expired solely for ordinary nonrenewal, with no suspension or revocation"} for {months} months. The pharmacist wants to resume work in Massachusetts. Assume this duration is measured after the applicable expiration or order date.'
    case('SC10','Restoring a lapsed or restricted registration',1,['w1-a-4'],scenario,'Which description best fits the applicable restoration pathway?',opts,ix,opts[ix][1]+' 복구 승인 전 independent practice는 하지 않는다.',dict(months=months,disciplinary=disciplinary),'247 CMR 4.02')
# SC11: count actual daily cap, not hours-worked employment advice.
for shifts in [(11,10),(12,9),(13,8),(14,11),(15,12),(10,14),(9,15),(13,13),(16,10)]:
    total=sum(min(v,12) for v in shifts)
    numeric('SC11','Creditable internship hours per day',1,['w1-b-2'],
      f'A Massachusetts intern logs {shifts[0]} hours on one day and {shifts[1]} hours on a separate day at an otherwise approved training site. Only the internship-credit ceiling is being evaluated; this question does not authorize any otherwise prohibited work schedule.',
      'What is the maximum combined internship credit for the two days?',total,[sum(shifts),min(sum(shifts),12),total-1],
      f'Internship credit는 하루 최대 12시간이다. min({shifts[0]},12)+min({shifts[1]},12)={total}. 실제 근무시간과 credit ceiling은 다르다.',dict(day1=shifts[0],day2=shifts[1]),'247 CMR 8.01(4)–(5)',unit='hours')
# SC12: standard ratios with max two interns, no vaccine exception.
for cert,intern,ordinary in [(2,0,2),(1,1,2),(0,2,2),(1,0,3),(0,1,3),(1,0,2),(0,1,2),(0,0,3),(2,0,3)]:
    n=cert+intern+ordinary;qual=cert+intern
    okay=(n<=3 and qual>=1) or (n==4 and qual>=2)
    ix=0 if okay else 1 if n==4 and qual<2 else 2 if n==3 and qual==0 else 3
    opts=[('The stated ordinary ratio and qualifying mix are satisfied.','3명에는 qualifying 1명, 4명에는 qualifying 2명 조합을 확인한다.'),('Four support staff need the required two-person qualifying mix.','4명 지원인력에 qualifying group 1명만 있으면 1:4 요건을 충족하지 못한다.'),('Three support staff need at least one intern or certified technician.','Ordinary technician 3명만으로 일반1:3을 충족하지 못한다.'),('The ordinary four-person ceiling is exceeded.','Vaccination 특례가 없는 일반 1-pharmacist 경로의 최대 support count는 4이다.')]
    case('SC12','Ordinary staffing: both headcount and credentials',1,['w1-b-8'],f'One pharmacist is not providing vaccination services. The filling team contains {cert} currently certified technicians, {intern} licensed interns, and {ordinary} ordinary technicians. Everyone is appropriately licensed and is actively assisting prescription preparation. No dedicated-training exclusion applies.',
      'Which assessment follows Policy 2026-02?',opts,ix,opts[ix][1],dict(certified=cert,intern=intern,ordinary=ordinary),'Policy 2026-02 §I(A)')
# SC13: dedicated training changes counted roles; never use certified trainee as qualified slot.
for ordinary,cert,trainer_work,computer_work in [(1,1,False,False),(1,1,True,False),(1,1,False,True),(0,2,False,False),(0,2,True,False),(2,1,False,False),(2,1,True,False),(1,2,False,True),(0,1,True,True)]:
    count=ordinary+cert+1+int(trainer_work)+int(computer_work)
    numeric('SC13','Counting dedicated training assignments',1,['w1-b-10'],
      f'The scheduled filling team includes {ordinary} ordinary technician(s) and {cert} certified technician(s). In addition, one certified employee is a dedicated trainee, one licensed dedicated trainer {"also independently fills prescriptions" if trainer_work else "only directly oversees that trainee"}, and one licensed employee scheduled for computer training {"also performs prescription-entry work" if computer_work else "does only training modules with no professional support work"}. All designations and written procedures are otherwise compliant.',
      'How many support personnel must be counted for this staffing calculation?',count,[ordinary+cert,ordinary+cert+1,count+1],
      f'일반 filling {ordinary+cert}명 + dedicated trainee 1명 + 독립업무 trainer {int(trainer_work)}명 + 업무 병행 computer trainee {int(computer_work)}명 = {count}명이다. 이 계산만으로 전체 ratio가 적법하다고 확정하는 것은 아니다.',
      dict(ordinary=ordinary,cert=cert,trainer_work=trainer_work,computer_work=computer_work),'Policy 2026-02 §§I(C),III',unit='people')
# SC14: current qualification determines assignment.
roles=[('current full technician license and current national certification','a new oral Schedule VI prescription',0),('current full technician license but expired national certification','a new oral Schedule VI prescription',1),('current full technician license without national certification','an unchanged verbal Schedule IV refill authorization',0),('only a current technician trainee license','an unchanged verbal Schedule IV refill authorization',1),('current full technician license and current national certification','final patient-specific prescription verification',2),('a current intern license under direct pharmacist supervision','patient counseling about a new inhaler',0),('a current intern license under direct pharmacist supervision','final patient-specific prescription verification',2),('an expired state technician license but current national certification','routine technician prescription-entry work',3),('current full technician license and current national certification','an emergency oral Schedule II authorization',2)]
opts=[('The assignment is within the stated personnel pathway.','해당 현재 자격과 승인/감독을 전제로 그 업무의 scope를 충족한다.'),('Reassign the task because the stated technician tier does not authorize it.','Ordinary technician와 PTT/CPhT의 전화처방 권한을 구별한다.'),('The identified pharmacist-only boundary still applies.','Final validation 또는 emergency oral CII의 pharmacist 역할을 해당 보조인력에 이전하지 않는다.'),('Restore the state license before assigning licensed technician work.','현재 national certification만으로 만료된 state license를 대체할 수 없다.')]
for role,task,ix in roles:
    case('SC14','A credential changes during employment',1,['w1-b-5','w1-b-6'],f'An employee has {role}. The on-duty pharmacist approves the assignment to handle {task}; all other routine training is complete.',
      'How should the pharmacist evaluate this assignment?',opts,ix,opts[ix][1],dict(role=role,task=task),'Policy 2020-15 §§II–III; 247 CMR 8.04,9.04')

# SC15: adult/non-IV/single-dose/valid order requirements; one controlling defect per row.
rows=[(28,'IM',True,True,'pharmacist'),(17,'IM',True,True,'pharmacist'),(32,'IV',True,True,'pharmacist'),(44,'SC',False,True,'pharmacist'),(39,'IM',True,False,'pharmacist'),(61,'SC',True,True,'intern'),(22,'IM',True,True,'certified technician'),(18,'SC',True,True,'pharmacist'),(16,'SC',True,True,'intern')]
for age,route,single,rx,role in rows:
    ix=0 if age>=18 and route!='IV' and single and rx and role!='certified technician' else 1 if age<18 else 2 if route=='IV' or not single else 3
    opts=[('Proceed under this pathway if all stated product and supervision conditions remain satisfied.','Adult·eligible product·route·single-dose·valid prescription·인력 조건이 모두 충족된 경로이다.'),('Do not use this circular as the authority for this patient’s age.','DCP26-03-124의 일반 대상은18세 이상이다.'),('Change or clarify the route/packaging plan before relying on this circular.','IV는 제외되고 single-dose packaging 조건이 있다.'),('Resolve the stated prescription or professional-role defect before administration.','Valid prescription과 pharmacist/intern 인력 조건을 확인한다. Technician vaccine scope를 비백신에 확대하지 않는다.')]
    case('SC15','Adult medication administration: the limiting condition',2,['w3-c-12','w3-c-13','w3-c-14'],f'A {age}-year-old patient presents for an otherwise eligible non-vaccine medication under DCP 26-03-124. The proposed route is {route}; the product is in {"single-dose" if single else "multidose"} packaging. A valid prescription {"is on file" if rx else "has not been issued"}. A trained {role} with current CPR would administer it, with appropriate supervision for an intern. All other product-specific requirements are satisfied.',
      'Which assessment best addresses the stated limiting condition?',opts,ix,opts[ix][1],dict(age=age,route=route,single=single,rx=rx,role=role),'DCP26-03-124, March11,2026')
# SC16: full technician + certification OR post-full-license hours, and training/CPR.
rows=[(True,True,10,True),(True,False,499,True),(True,False,500,True),(False,True,700,True),(True,False,600,False),(True,True,0,False),(True,False,0,True),(True,True,300,True),(True,False,720,True)]
opts=[('The described personnel qualifications are satisfied.','Full license, certification 또는 500 post-license hours, required training/current CPR를 모두 확인한다.'),('Complete the certification-or-post-licensure-experience pathway first.','National certification이 없다면 full PT license 후 최소500시간이 필요하다.'),('Obtain full technician licensure; trainee status is not sufficient.','PTT는 주 vaccination policy의 투약인력에 포함되지 않는다.'),('Complete or restore the stated training/CPR requirements first.','Full license와 경험/인증이 있어도 vaccine training·current CPR는 별도이다.')]
for full,cert,hours,training in rows:
    ix=2 if not full else 1 if not cert and hours<500 else 3 if not training else 0
    case('SC16','Technician vaccination qualification at the boundary',2,['w3-c-4'],f'A technician has {"a full Massachusetts PT license" if full else "only a Massachusetts trainee license"}, {"current" if cert else "no current"} national certification, and {hours} hours worked after full PT licensure{ "" if full else " claimed from trainee employment instead"}. Required vaccine training, documented on-the-job assessment, and current CPR {"are complete" if training else "are not all complete"}. A qualified pharmacist will select the vaccine, counsel, and directly supervise administration to an eligible adult.',
      'What must be addressed before this staff member vaccinates under the state policy?',opts,ix,opts[ix][1],dict(full=full,cert=cert,hours=hours,training=training),'Policy2023-02 §III(D)')
# SC17: retail CDTM permission conditions, no independent diagnostic assumption.
rows=[(35,'VI',True,True),(17,'VI',True,True),(42,'IV',True,True),(56,'II',True,True),(63,'VI',False,True),(47,'VI',True,False),(18,'VI',True,True),(74,'III',True,True),(29,'VI',False,True)]
opts=[('The stated retail CDTM prerequisites and schedule boundary are satisfied.','적격 pharmacist·adult·written referral/consent·CPA scope·VI 조건을 확인한다.'),('Use a different lawful authority; this retail CDTM age condition is not met.','Retail CDTM patient는18세 이상이다.'),('Do not prescribe this schedule under the retail CPA.','Retail/community CDTM는II–V prescribing를 허용하지 않는다.'),('Complete the missing patient-specific referral/consent or pharmacist qualifications.','서명 CPA만으로 patient referral·consent·개인 자격을 면제하지 않는다.')]
for age,sched,ref,qual in rows:
    ix=1 if age<18 else 2 if sched!='VI' else 3 if not ref or not qual else 0
    case('SC17','Retail CDTM: contract versus patient authority',2,['w3-d-2','w3-d-6','w3-d-7'],f'A retail pharmacist proposes to manage an expressly authorized hypertension therapy under a current signed CPA. The patient is {age}; the proposed prescription is Schedule {sched}. Patient-specific written physician referral and informed consent {"are documented" if ref else "are missing"}. The pharmacist {"meets" if qual else "has not completed"} the required individual qualifications and coverage. No separate statutory-prescribing pathway is being used.',
      'Which assessment is supported?',opts,ix,opts[ix][1],dict(age=age,schedule=sched,referral=ref,qualified=qual),'247 CMR16.02–16.04')

# SC18: two independent dates: actual issue and earliest dispensing.
for elapsed,earliest in [(29,0),(30,0),(31,0),(10,14),(14,14),(20,15),(45,0),(28,29),(12,8)]:
    issued=date(2026,9,1);today=issued+timedelta(days=elapsed);start=issued+timedelta(days=earliest)
    ix=2 if elapsed>30 else 1 if elapsed<earliest else 0
    opts=[('The stated timing permits consideration of dispensing today.','Issue-date validity와 earliest-fill instruction을 모두 충족한 시점이다. 다른 clinical/record duties는 남는다.'),('Wait until the valid earliest-fill date; today is too early.','처방이 만료되지 않았어도 prescriber의 earliest-fill date 전에는 조제하지 않는다.'),('Obtain a new legally valid prescription; the original is outside the MA validity period.','MA written/electronic CII는 issue 후30일을 지난 경우 invalid하다.'),('Treat the earliest-fill date as a replacement issue date and restart validity.','Earliest-fill 지시는 실제 발행일을 바꾸거나 validity clock를 재시작하지 않는다.')]
    case('SC18','CII: issue date and earliest-fill date',3,['w2-b-1','w2-b-3'],f'A Massachusetts practitioner issues a valid CII EPCS on {issued:%B %d, %Y}, with an earliest-fill date of {start:%B %d, %Y}. The pharmacy first considers dispensing on {today:%B %d, %Y}. This is not an out-of-state prescription or partial remainder. All non-timing conditions are met.',
      'Which timing decision is supported?',opts,ix,opts[ix][1],dict(elapsed_days=elapsed,earliest_day=earliest),'M.G.L. c.94C §23(a); 247 CMR9.04(10); 21 CFR1306.12')
# SC19: hour-based shortage clock, no imposed calendar-day conversion.
for hours,total,given in [(24,60,12),(48,90,30),(71,45,15),(72,60,20),(73,90,20),(80,50,10),(12,42,6),(60,30,8),(96,84,14)]:
    remain=total-given;ix=0 if hours<=72 else 1
    opts=[(f'Complete up to the remaining {remain} units under the original shortage-partial route.','72시간 이내이고 original authorized quantity를 넘지 않는 잔량의 경로이다.'),('Notify the prescriber; later supply requires a new prescription.','Shortage first partial 후72시간이 지나면 원 처방 잔량을 그대로 추가 공급할 수 없다.'),('Start a new 72-hour period when replacement stock arrives.','입고일은 shortage clock의 시작점이 아니다.'),(f'Dispense a new full quantity of {total} units because the prescription is still in date.','Already dispensed quantity를 차감하지 않는 중복 공급은 허용되지 않는다.')]
    case('SC19','Shortage partial: elapsed hours and remaining quantity',3,['w2-b-7'],f'A pharmacy could not supply the full quantity of {total} units on a CII prescription and dispensed {given}. Exactly {hours} hours have elapsed since that shortage partial. The remaining stock is now available; no patient-request or LTCF exception was used, and all other dates remain valid.',
      'Which action follows the stock-shortage partial-fill rule?',opts,ix,opts[ix][1]+f' 기록상 잔량은 {total}−{given}={remain}이다.',dict(hours=hours,total=total,dispensed=given),'21 CFR1306.13(a)')
# SC20: requested partial, competing quantity and issue-day limit.
for day,total,prior,request in [(10,60,10,20),(29,90,30,30),(30,50,20,15),(31,60,10,20),(18,45,40,10),(25,30,10,30),(8,90,70,10),(32,40,20,10),(15,20,20,10)]:
    allow=min(request,total-prior) if day<=30 else 0
    numeric('SC20','Patient-requested CII remainder: quantity and time',3,['w2-b-8'],
      f'An ordinary written/EPCS CII prescription issued by a Massachusetts practitioner authorizes {total} tablets. Properly documented patient-requested partial fills have already supplied {prior}. On issue-date day {day}, counting the next day as day 1, the patient requests {request} more at the same pharmacy. This is not an emergency oral order, stock-shortage partial, or LTCF exception; all other requirements are satisfied.',
      'What is the maximum number of tablets from this original authorization that can be supplied at this visit?',allow,[request,total-prior,total],
      f'30일 내라면 잔여 authorization {total-prior}와 이번 요청 {request} 중 작은 수량을 검토한다. Issue 후30일을 넘기면 이 경로에서 추가 공급은0이다. 이 사례의 최대는 {allow}.',dict(day=day,total=total,prior=prior,request=request),'21 CFR1306.13(b); M.G.L.c.94C §18(d¾)',unit='tablets')
# SC21: authorized refills versus legal maximum, six-month validity supplied unambiguously.
for authorized,used,in_time in [(0,0,True),(1,0,True),(2,1,True),(3,2,True),(5,4,True),(5,5,True),(5,1,False),(2,0,False),(4,1,True)]:
    count=max(0,min(authorized,5)-used) if in_time else 0
    numeric('SC21','Controlled refill history: remaining legal authorizations',3,['w2-c-1'],
      f'A Schedule IV prescription originally authorized {authorized} refill(s). The original dispensing is not included in the count; {used} refill(s) have since been completed. Today is clearly {"within" if in_time else "beyond"} six months from the issue date. No new authorization has been obtained.',
      'How many unused refill authorizations can still be exercised within this prescription’s lawful life, assuming clinical appropriateness?',count,[authorized,5-used,max(0,authorized-used)+1],
      f'Original fill을 제외한 authorized refills에서 이미 사용한 수를 뺀다. 법정5회 및 issue 후6개월 한도를 모두 적용하므로 이 경우 남은 유효 authorization은 {count}이다.',dict(authorized=authorized,used=used,in_time=in_time),'21 CFR1306.22',unit='refill(s)')
# SC22: Schedule VI validity vs transfer/reset, not unresolved continuation.
rows=[(True,2,False),(False,2,False),(True,0,False),(True,1,True),(True,5,False),(False,6,True),(True,3,True),(False,1,False),(True,0,True)]
opts=[('A timely transfer may preserve the remaining authorized refills.','VI prescription의 1년 및 남은 authorization을 보존하는 eligible transfer이다.'),('The original one-year validity has ended; transfer cannot restart it.','Transfer date로 original issue-date validity를 재설정하지 않는다.'),('There is no remaining refill authorization to transfer for this refill request.','Unexpired라는 사실만으로 새로운 refill authorization이 생기지 않는다.'),('The receiving pharmacy receives a new one-year prescription automatically.','이관은 새 prescriber order가 아니다.')]
for in_time,remaining,prior_transfer in rows:
    ix=1 if not in_time else 2 if remaining==0 else 0
    case('SC22','Schedule VI transfer without resetting authorization',3,['w2-c-7'],f'A Schedule VI prescription from a Massachusetts practitioner is {"within" if in_time else "past"} one year of its original issue date and shows {remaining} authorized refills remaining. It {"has already been transferred once" if prior_transfer else "has not previously been transferred"}. The patient now requests another refill transfer. No emergency-continuity exception is claimed.',
      'Which conclusion is correct?',opts,ix,opts[ix][1],dict(in_time=in_time,remaining=remaining,prior_transfer=prior_transfer),'247 CMR9.04(12),9.14(4)')
# SC23: materially different indication/product categories, not cosmetic drug swaps.
supply_rows=[('testosterone for a valid non-opioid indication',90),('methylphenidate for a valid indication',90),('amphetamine for a valid indication',90),('buprenorphine specifically for opioid use disorder',90),('buprenorphine solely for pain, not OUD',30),('oral hydromorphone for pain outside an implantable pump',30),('a CII drug supplied for an implantable infusion pump',90),('oxycodone for continuing pain therapy outside the first-opioid or minor limit',30),('ketamine for a valid non-opioid indication',90)]
for drug,cap in supply_rows:
    numeric('SC23','CII/CIII supply category after the 2024 change',3,['w2-b-2'],
      f'A Massachusetts pharmacist reviews {drug}. The prescriber has authorized at least 90 days, the prescription is otherwise in date, and no separate patient-specific or product limit is more restrictive. Evaluate the statutory single-fill ceiling, not whether the pharmacy should supply that entire amount.',
      'Under Policy 2024-05 and c.94C §23(d), what is the applicable maximum days-supply category?',cap,[7,30,60,90],
      f'이 사례는 {"OUD·non-opioid 또는 implantable-pump의 90일 범주" if cap==90 else "그 외 CII/CIII의30일 범주"}이다. Supply ceiling과 prescription validity는 다르며 authorized quantity를 임의 증가시키지 않는다.',dict(product_indication=drug),'M.G.L.c.94C §23(d); Policy2024-05',unit='days')
# SC24: recipient and hardship record, not an invented universal refusal rule.
id_rows=[('patient',True,False,False),('agent',True,False,False),('patient',False,True,True),('agent',False,True,True),('patient',False,True,False),('agent',False,True,False),('patient',False,False,False),('agent',False,False,False),('agent',True,True,True)]
opts=[('Inspect and record the applicable identifier for the actual recipient.','실제 수령 ultimate user/agent의 적격 identifier를 확인하는 일반 경로이다.'),('Use the documented hardship pathway with the required recipient record.','Serious hardship 판단·사유 문서화와 printed name/address/signature를 모두 갖춘 예외이다.'),('Complete the missing hardship documentation and recipient record before relying on that exception.','Serious hardship라는 말만으로 지정 수령자 기록이 면제되지 않는다.'),('The facts do not establish an identifier exception; obtain an acceptable identifier or establish another applicable lawful route.','유효 ID도 해당 serious-hardship 요건도 없으면 이 사실만으로 일반 요건을 생략할 수 없다.')]
for person,valid,hardship,record in id_rows:
    ix=0 if valid else 1 if hardship and record else 2 if hardship else 3
    case('SC24','Identification at pickup: the actual collecting person',3,['w2-c-11'],f'A {person} arrives to collect an ordinary PMP-reportable prescription subject to the customer-identifier rule. The actual recipient {"presents a valid acceptable government-issued identifier" if valid else "does not present an acceptable identifier"}. The pharmacist {"has documented a serious-hardship basis" if hardship else "has not established a serious-hardship basis"}. The required printed name, address, and signature {"are recorded" if record else "are not recorded"}. No delivery/refill-specific waiver applies.',
      'Which handling of the identifier requirement matches these facts?',opts,ix,opts[ix][1],dict(recipient=person,valid_id=valid,hardship=hardship,record=record),'247 CMR9.04(14)')
# SC25: each row has one independently decisive defect; no multiple-defect ambiguity.
transfer_rows=[
 ('It was originally an EPCS, has never been dispensed or transferred, and both pharmacies are appropriately DEA-registered.',None),
 ('It was originally a paper prescription, later scanned into the pharmacy computer; it has never been dispensed or transferred.', 'original paper format'),
 ('It was originally received by fax and entered into the computer; it has never been dispensed or transferred.', 'original fax format'),
 ('It was originally received orally and entered into the computer; it has never been dispensed or transferred.', 'original oral format'),
 ('It was originally an EPCS and some CII quantity has already been dispensed; it has not been transferred.', 'prior partial dispensing'),
 ('It was originally an EPCS and has never been dispensed, but it has already undergone one initial electronic transfer.', 'a prior initial electronic transfer'),
 ('It was originally a never-filled, never-transferred EPCS, but the receiving system would change the prescription contents during transmission.', 'alteration of prescription contents'),
 ('It was originally a never-filled, never-transferred EPCS, but the proposed move is not requested by the patient.', 'absence of the required patient request'),
 ('It was originally a never-filled, never-transferred EPCS, but the proposed receiving retail pharmacy lacks the required DEA registration.', 'an unregistered receiving pharmacy')]
for description,defect in transfer_rows:
    answer='Proceed with the initial electronic transfer, preserving all required content and records.' if defect is None else 'Do not use this pathway with '+defect+'; resolve the defect or use another lawful authorization route.'
    why='Original EPCS·never-filled·일회·환자요청·적격 retail pharmacies·전자형태·unaltered contents 등 조건을 모두 확인한다.' if defect is None else '이 사례의 결정적 장애는 '+defect+'이다. Original EPCS의 일회 initial-transfer 조건을 단순 전산 저장이나 다른 refill 규칙으로 우회하지 않는다.'
    options=[(answer,why),('Convert the prescription to a fax between the pharmacies to satisfy the electronic-transfer rule.','허용된 electronic pathway는 electronic form을 유지해야 한다.'),('Apply the real-time-database refill exception to remove every initial-transfer condition.','Refill transfer 예외는 initial unfilled EPCS의 요건을 모두 없애지 않는다.'),('Ask a certified technician to substitute for the required licensed-pharmacist communication.','해당 controlled-transfer 경로의 pharmacist communication을 VI technician transfer 권한으로 대체하지 않는다.')]
    case('SC25','The limiting condition in an initial EPCS transfer',3,['w2-c-6'],
      'A CII prescription is proposed for transfer between retail pharmacies in Massachusetts. '+description+' Except for any defect expressly stated, the other first-fill transfer conditions are met.',
      'Which response best fits these facts?',options,0,why,dict(description=description,defect=defect),'21 CFR1306.08(e)–(h); Policy2023-10')

# SC26: opened-container exact-count boundary; compare actual size, not cosmetic strength.
for schedule,count in [('II',25),('II',650),('II',1000),('III',800),('III',1000),('III',1001),('IV',1200),('V',900),('V',1500)]:
    exact=schedule=='II' or count>1000
    opts=[('An exact count is required for this opened container.','ScheduleI–II는 exact count이고 III–V도1,000 tablets/capsules 초과 container이면 exact count이다.'),('Federal inventory rules permit an estimate for this opened container.','이III–V opened-container 조건은1,000초과가 아니므로 federal rule상 estimate 허용이다. 다른 state/SOP 책임은 남는다.'),('No inventory entry is needed until the bottle is empty.','사용 중인 on-hand stock도 inventory 대상이다.'),('The prescription transaction total automatically replaces physical inventory.','Transaction total과 해당 실제 on-hand inventory는 다르다.')]
    case('SC26','Federal opened-container inventory method',4,['w2-d-6'],f'The pharmacist is taking the federal controlled-substance inventory. An opened container of Schedule {schedule} tablets holds {count} tablets. Evaluate the federal counting method for this container only; a stricter local procedure is not being assumed.',
      'Which counting assessment is supported?',opts,0 if exact else 1,opts[0 if exact else 1][1],dict(schedule=schedule,container_tablets=count),'21 CFR1304.11(e)')
# SC27: arithmetic tied to discrepancy analysis, not automatic theft classification.
for opening,receipt,dispensed,returned,physical in [(120,80,75,10,113),(150,100,90,20,140),(200,0,45,15,138),(85,60,40,5,100),(300,50,160,40,149),(75,120,70,10,110),(160,80,55,15,168),(90,40,40,0,87),(250,100,140,20,190)]:
    expected=opening+receipt-dispensed-returned;short=expected-physical
    numeric('SC27','Expected balance before investigating a discrepancy',4,['inventory-working-example','w2-d-7'],
      f'A CII perpetual record begins with {opening} tablets. Documented receipts are {receipt}, dispensing is {dispensed}, and lawful reverse distribution is {returned}. There are no other transactions or adjustments. The physical count is {physical}.',
      'What should the expected closing balance be before any discrepancy investigation or adjustment?',expected,[physical,opening+receipt-dispensed,opening-receipt+dispensed],
      f'Expected balance={opening}+{receipt}−{dispensed}−{returned}={expected}. 예상수량에서 실물을 뺀 차이는 {short}정이다. 이 차이는 조사 시작점이며 그 자체로 theft/significant loss를 자동 확정하지 않는다.',
      dict(opening=opening,received=receipt,dispensed=dispensed,reverse=returned,physical=physical),'247 CMR9.21(8); inventory arithmetic',unit='tablets')
# SC28: Form222 is an order-date clock, not the first shipment.
for day,first in [(10,3),(45,8),(59,20),(60,40),(61,5),(70,30),(30,15),(58,10),(65,59)]:
    left=max(0,60-day)
    texts=[f'The original 60-day order period remains open; {left} day(s) remain after today.',
           'The ordinary 60-day fulfillment period has ended; do not ship the remainder under this expired order.',
           f'A new 60-day period starts on first shipment day {first}.',
           'Use the patient-prescription 30-day rule instead of the stock-order rule.']
    # Korean explanatory text is deliberately explicit about legal clocks.
    opts=[(texts[0],f'Order date 기준 60일이다. 현재 day {day}이므로 기간 안이면 오늘 이후 {left}일이 남는다. First shipment에서 새로 시작하지 않는다.'),
          (texts[1],'Order date 후60일을 넘긴 잔량은 이 ordinary order의 허용기간을 벗어난다.'),
          (texts[2],'First shipment는 original60-day clock를 재시작하지 않는다.'),
          (texts[3],'Patient CII prescription과 registrant Form222 stock order의 기한은 다르다.')]
    case('SC28','Form 222 partial shipment near expiration',4,['w2-d-2'],f'A valid Form 222 is dated day 0. The supplier made its first partial shipment on day {first}. Today is day {day} after the order date, and the supplier wants to send the remainder. No special exception applies.',
      'Which description of the order’s ordinary fulfillment period is correct?',opts,0 if day<=60 else 1,opts[0 if day<=60 else 1][1],dict(day=day,first=first),'21 CFR1305.13')
# SC29: denominator must include distributed and dispensed dosage units.
for disp,distributed,new in [(9500,400,50),(19000,900,80),(4750,250,1),(20000,500,200),(9000,400,100),(30000,1200,200),(7600,350,100),(14000,600,50),(6000,250,200)]:
    d=distributed+new;total=disp+d; percent=100*d/total
    ix=0 if percent<=5 else 1
    opts=[('The proposed annual dosage-unit proportion does not exceed 5%; other conditions still must be satisfied.','지정분자와 분모로 계산한 비율이5%이하이다. 별도state/registration/record 요건까지 자동충족된다는 뜻은 아니다.'),('The proposed proportion exceeds 5%; do not rely on this limited distribution exception.','연간 distributed/(distributed+dispensed) 비율이5%를 초과한다.'),('Only the dollar value of the proposed transfer determines the 5% test.','이Federalexception의 기준은매출액이 아니라dosage units이다.'),('The denominator excludes all distributed dosage units.','분모에는같은해의distributed와dispensed dosage units가함께포함된다.')]
    case('SC29','The controlled-stock distribution percentage',4,['w2-d-4','five-percent-example'],f'For the relevant calendar year, a dispensing practitioner has dispensed {disp:,} controlled-substance dosage units and distributed {distributed:,} units counted under the limited distribution exception. A proposed stock transaction would distribute {new} additional units. All units use the same proper counting basis; assume no other transactions or exceptions.',
      'What does the dosage-unit percentage calculation show after the proposed transaction?',opts,ix,f'({distributed}+{new})/({disp}+{distributed}+{new})×100={percent:.3f}%. '+opts[ix][1],dict(dispensed=disp,distributed=distributed,proposed=new),'21 CFR1307.11')
# SC30: explicit applicable default + shorter chemical bound, not subscription USP completeness.
bud_rows=[('nonpreserved aqueous',14,8),('nonpreserved aqueous',14,21),('preserved aqueous',35,20),('preserved aqueous',35,50),('nonaqueous oral liquid',90,60),('nonaqueous oral liquid',90,120),('other nonaqueous dosage form',180,100),('other nonaqueous dosage form',180,200),('preserved aqueous',35,10)]
for form,default,chemical in bud_rows:
    val=min(default,chemical)
    numeric('SC30','BUD: the limiting supported interval',4,['w4-b-10','w4-b-11'],
      f'For a {form}, the pharmacist has confirmed an applicable default microbial maximum of {default} days under the stated storage conditions. Reliable data for this exact formulation and container support chemical stability for only {chemical} days. Ingredients expire later; there is no applicable preparation-specific longer-BUD route.',
      'What is the longest BUD supported by both stated limits?',val,[max(default,chemical),365,val+7],
      f'더 짧은 제한을 적용한다: min({default},{chemical})={val}일. Microbial maximum은 더 짧은 chemical stability를 넘기는 허가가 아니다. 실제 제품에서는 추가로 더 짧은 제한이 있는지도 확인한다.',dict(form=form,microbial=default,chemical=chemical),'USP<795> framework as explained in W4-B; stated hypothetical stability evidence',unit='days')



# SC31: fresh official-source expansion, not silently represented as a Week 1–6 rule.
for days,patient,registered in [(20,True,True),(44,True,True),(45,True,True),(46,True,True),(60,True,True),(10,False,True),(30,True,False),(40,False,True),(5,True,False)]:
    facts=f'The administering practitioner received a patient-specific Schedule III narcotic injection for OUD maintenance {days} days ago. It was supplied under 21 CFR 1306.07(f), not as general office stock. The planned recipient is {"the patient named on the prescription" if patient else "a different patient with an otherwise similar treatment plan"}. The delivery location {"is" if registered else "is not"} the location on the practitioner’s DEA registration. All requirements not expressly put at issue, including state authority and applicable REMS, are met.'
    ix=0 if days<=45 and patient and registered else 1 if days>45 else 2 if not patient else 3
    opts=[('The stated patient, location, and 45-day receipt conditions permit this administration.','제시된세조건이모두충족된다. 다른scope/REMS요건충족은문제에서명시한전제이지이규칙의면제가아니다.'),('The 45-day period after practitioner receipt has expired; do not administer under this delivery pathway.','§1306.07(f)(5)는practitioner receipt후45일이내 named patient투약을요구한다. 약국조제일이나예약일로시계를바꾸지않는다.'),('This delivered dose is restricted to the named patient; do not redirect it to the proposed recipient.','환자별직접배송경로이지general office stock또는다른환자의투약재고가아니다.'),('The stated delivery location fails the registered-location condition of this pathway.','§1306.07(f)(1)의practitioner DEA등록주소조건을별도로충족해야한다.')]
    case('SC31','Patient-specific OUD injection delivered to a practitioner',3,['w2-c-14'],facts,'Which conclusion addresses the controlling fact?',opts,ix,opts[ix][1],dict(days_after_receipt=days,named_patient=patient,registered_location=registered),'Fresh check: 21 CFR 1306.07(f)(1)–(6), eCFR edited through 2026-10-22')
# SC32–33: action-level classification only, not a blanket authorization to compound.
for family,kind,thresholds in [('SC32','surface',{5:3,7:5,8:50}),('SC33','viable air',{5:1,7:10,8:100})]:
    for iso,threshold in thresholds.items():
        for count in [threshold-1,threshold,threshold+1]:
            exceeds=count>threshold
            opts=[('This result exceeds the action level for the stated sample type and ISO class.','Policy2026-03의표는초과(>)를기준으로한다. 해당sampletype/ISOclass의threshold보다크면action-levelresult이다.'),('This result does not exceed that specific action level; other findings and trends still require assessment.','해당표의threshold이하이므로이단일결과가그actionlevel을초과하지않는다. 모든조제조건이나추세의적정성을자동보장하는것은아니다.'),('Apply the action level of the next less-clean ISO class instead.','실제로채취한공간의classification과sampletype을적용하며임의로더높은한도를선택하지않는다.'),('Average this count with another sampling site before applying the action level.','서로다른sampling site의값을평균해해당결과의초과를없애지않는다.')]
            unit='CFU per media device' if kind=='surface' else 'CFU per cubic meter of air per media device'
            case(family,f'Environmental monitoring: {kind} threshold',4,['w4-d-9'],f'A Massachusetts sterile pharmacy receives an ISO Class {iso} {kind} sample result of {count} {unit}. This is one validly collected sample, not a pooled result. Consider only whether this result exceeds the current Board policy’s action level for this sample type.',
              'Which interpretation of the result is supported?',opts,0 if exceeds else 1,f'ISO{iso} {kind} action level은 >{threshold}. 결과{count}는 '+('초과한다.' if exceeds else '초과하지않는다. 동일값을>로읽지않는다.'),dict(iso=iso,sample_type=kind,cfu=count,threshold=threshold),'Policy 2026-03 §I action-level tables')
# SC34: avoid confusing the state confirmed-loss pathway with DEA's initial notice.
loss_rows=[('A single Schedule VI tablet was confirmed stolen by an employee.',0),('A small quantity of non-PMP Schedule VI medication was confirmed diverted.',0),('An internal investigation confirmed a significant loss of Schedule II stock.',0),('An internal investigation confirmed a significant loss of Schedule IV stock.',0),('An internal investigation confirmed a significant loss of gabapentin stock, a PMP-reportable Schedule VI drug.',0),('An apparent stock discrepancy remains unconfirmed while records and physical counts are being reconciled.',1),('Investigation found a non-theft loss of Schedule IV stock to be insignificant, with no other reportable facts.',2),('Investigation traced missing tablets to a confirmed dispensing error, not theft or diversion.',3),('A negligible monetary loss of Schedule III stock was nonetheless confirmed to be employee theft.',0)]
loss_opts=[('Submit the Board’s confirmed-loss report within 7 calendar days, including DEA Form 106 if applicable.','現행Policy2026-01은confirmed theft/diversion의모든수량·schedule, significantII–V/PMP-VI손실을해당7calendar-day보고경로로정한다. 별도DEA초기통지의무는남는다.'),('Continue the investigation; do not submit an unconfirmed loss as a confirmed Board loss.','이Boardpolicy는unconfirmedloss를보고하지않도록한다. 사실확인·기록·다른적용의무를중단하는뜻은아니다.'),('Document the investigated insignificant loss on site and monitor adverse trends.','Theft/diversion이아닌insignificantloss는이Board보고대상에서제외되지만onsite기록·trend관리가남는다.'),('Handle the confirmed dispensing error through CQI; this policy does not require a loss report for that error.','Confirmeddispensingerror의lossreport예외와CQI요건을구별한다. seriousinjury등다른보고trigger는따로검토한다.')]
for description,ix in loss_rows:
    case('SC34','Confirmed loss, discrepancy, or dispensing error',4,['w4-d-13','w2-d-10'], 'A resident Board-licensed Massachusetts pharmacy evaluates the following event under Policy 2026-01. '+description+' This question concerns the Board loss-reporting pathway only, not whether a separate federal notice is required.',
      'Which response follows the stated Board policy?',loss_opts,ix,loss_opts[ix][1].replace('現행','현행'),dict(event=description,route=ix),'Policy 2026-01 §§II–III, adopted March 26, 2026')
# SC35: different legal events, different clock origins; no business-day ambiguity.
clock_rows=[('An ordinary vaccination is administered','2026-10-19T09:30',72,'w3-c-8','105 CMR222.100(A)'),('An ordinary vaccination is administered','2026-10-20T16:00',72,'w3-c-8','105 CMR222.100(A)'),('An unnamed newborn who already received a birth-dose immunization is named in the relevant health record','2026-10-20T08:15',24,'w3-c-8','105 CMR222.100(A)'),('An unnamed newborn who already received a birth-dose immunization is named in the relevant health record','2026-10-22T12:45',24,'w3-c-8','105 CMR222.100(A)'),('A provider receives the patient’s MIIS data-sharing-objection form','2026-10-21T11:00',24,'w3-c-8','105 CMR222.105(B)(2)'),('A pharmacist first learns of a QRE that has reached the patient','2026-10-19T14:20',24,'w4-d-3','247 CMR15.03(2)'),('A pharmacist first learns of a QRE that has reached the patient','2026-10-23T17:10',24,'w4-d-3','247 CMR15.03(2)'),('A retail CDTM pharmacist issues a nonurgent medication modification','2026-10-20T10:40',24,'w3-d-8','247 CMR16.03(5)(e)2'),('A retail CDTM pharmacist issues a nonurgent discontinuation prescription','2026-10-22T15:25',24,'w3-d-8','247 CMR16.03(5)(e)2')]
from datetime import datetime
for desc,start,hours,unit,auth in clock_rows:
    t=datetime.fromisoformat(start);due=t+timedelta(hours=hours)
    task='submit the immunization information to MIIS' if 'vaccination is' in desc or 'newborn' in desc else 'send the objection form to the Department' if 'objection' in desc else 'complete the initial QRE documentation' if 'QRE' in desc else 'provide the prescription change to the supervising physician'
    options=[]
    for h in [hours,12 if hours==24 else 24,48,96]:
        dt=t+timedelta(hours=h)
        options.append((dt.strftime('%B %d at %H:%M'),f'이사건의기한은trigger후{hours}시간이며 {due.strftime("%m/%d %H:%M")}까지이다. '+('즉시환자보호·통지는별도의무이다.' if 'QRE' in desc else '다른보고사건의시작점과섞지않는다.')))
    case('SC35','Event-specific reporting and documentation clock',4,[unit],desc+' at '+t.strftime('%H:%M on %B %d, %Y')+'. All times use the same local time zone, with no clock change during the interval.',f'What is the latest time to {task} under the stated hour-based requirement?',options,0,options[0][1],dict(event=desc,trigger=start,hours=hours,deadline=due.isoformat()),auth)
# SC36: separate administrative requirements removed in 2025 from clinical obligations.
cloz_rows=[('The software asks for a REMS dispense authorization before releasing an otherwise appropriate clozapine prescription.',0),('A new prescriber has not enrolled in the former Clozapine REMS registry.',0),('A patient has no enrollment record in the former Clozapine REMS system.',0),('A pharmacy employee says that no ANC follow-up is relevant because the REMS ended.',1),('A pharmacist proposes ignoring a patient-specific neutropenia concern because there is no REMS clearance step.',1),('The pharmacy wants to replace its safety review with the old registry’s approval number.',2),('An ANC result is being requested solely for mandatory upload to the removed REMS registry.',0),('The prescriber asks whether label-based ANC monitoring remains relevant after the REMS removal.',1),('The pharmacy treats the REMS removal as proof that every clozapine prescription is safe to dispense.',2)]
for desc,ix in cloz_rows:
    opts=[('Dispense only after restoring the former REMS enrollment and authorization process.','FDA가 제거한 REMS의 enrollment/authorization를 현행 필수 조건으로 다시 만들지 않는다.'),('Remove the former REMS access requirement, while retaining appropriate label-based monitoring and patient-specific review.','2025-06-13 REMS 제거는 과거 등록·authorization 장벽을 없앴지만 neutropenia 위험과 label-based ANC monitoring, 적법한 처방·DUR 의무는 남는다.'),('Treat removal of the REMS as removal of the need for ANC monitoring and clinical safety review.','행정 프로그램 제거와 약물 위험·label 기반 monitoring은 별개이다.'),('Apply the isotretinoin iPLEDGE dispensing window as the replacement clozapine rule.','서로 다른 약물 프로그램의 dispensing window를 clozapine의 대체 규칙으로 가져오지 않는다.')]
    case('SC36','Clozapine after removal of the REMS',2,['w3-b-9','w5-b-9'], 'A Massachusetts pharmacy reviews clozapine dispensing on October 26, 2026. '+desc,'Which overall conclusion correctly addresses the current regulatory and safety obligations?',opts,1,opts[1][1],dict(issue=desc),'FDA Clozapine REMS removal effective June 13, 2025; current labeling remains applicable')
# SC37: requested vs required communication; specify the controlling outcome.
admin_rows=[('An administration-related reaction requires additional testing in the emergency department.',0),('An administration-related event leads to inpatient hospitalization.',0),('An administration-related event is life-threatening.',0),('An administration-related reaction causes a persistent significant incapacity.',0),('A minor administration-related reaction occurs with none of the circular’s listed serious outcomes.',1),('An eligible prescription lacks the suggested words “for pharmacist administration,” and the intended setting is unclear.',2),('A prescriber has selected an appropriate reassessment interval other than exactly three months.',3),('An administration-related event prolongs an existing hospitalization.',0),('A minor injection-site reaction occurs without additional hospital or emergency-department care or other listed serious outcome.',1)]
admin_opts=[('Immediately report the event to the prescriber; assess any separate Board reporting duties.','DCP26-03-124의지정seriousoutcome이면prescriber에게immediatereport한다. 별도Board보고가있으면병행한다.'),('Appropriately communicate the reaction to the prescriber within 24 hours as the circular recommends.','일반adverseevent/reaction의24시간문구는should이다. 지정seriousoutcome의immediate의무와구별한다.'),('Use professional judgment and contact the prescriber as encouraged to clarify the intended administration setting.','권장notation누락자체가모든유효처방을자동무효화하는조항은아니다. 목적이불분명한경우권장되는연락을연결한다.'),('Follow the prescriber’s appropriate reassessment interval; quarterly is an example rather than a universal fixed deadline.','Circular는appropriateinterval을prescriber가정하며quarterly는예시이다. 모든약에90일고정의무를새로만들지않는다.')]
for desc,ix in admin_rows:
    case('SC37','Medication-administration communication under the 2026 circular',2,['w3-c-12','w3-c-15','w3-c-17'], 'The pharmacy is using the non-vaccine medication-administration pathway in DCP 26-03-124. Personnel, patient, product, and prescription requirements are otherwise met. '+desc,
      'Which response accurately reflects the circular’s wording?',admin_opts,ix,admin_opts[ix][1],dict(event=desc),'DCP 26-03-124: Prescriber Assessment, Reporting Adverse Events, Pharmacist-Prescriber Communication')
# SC38: product-specific special-packaging quantity, not a class-wide exemption.
pppa_rows=[('prednisone',5,21,105,'mg','tablet package'),('prednisone',5,22,105,'mg','tablet package'),('prednisone',1,100,105,'mg','tablet package'),('methylprednisolone',4,21,84,'mg','tablet package'),('methylprednisolone',4,22,84,'mg','tablet package'),('potassium',50,1,50,'mEq','individually wrapped unit dose'),('potassium',60,1,50,'mEq','individually wrapped unit dose'),('baloxavir marboxil',40,2,80,'mg','tablet package'),('baloxavir marboxil',40,4,80,'mg','tablet package')]
for drug,strength,quantity,limit,u,form in pppa_rows:
    total=strength*quantity;ok=total<=limit
    opts=[('The stated product-specific quantity exception applies to this package.','제시된제형·성분·포장량조건이모두해당제품예외범위안이다. 같은class의모든제품면제는아니다.'),('The package exceeds the product-specific quantity exception; that exception cannot justify non-CR packaging.','제품별포장총량/단위용량상한을초과했다. 다른명시적면제나환자요청을문제에서가정하지않는다.'),('A quantity exception for this product exempts every oral drug in the same therapeutic class.','PPPA예외는정확한제품·제형·포장량조건이며약리class전체로확대하지않는다.'),('The pharmacy may rely on the patient’s age instead of a request or product exception.','환자나이가자동non-CRwaiver를만들지않는다.')]
    case('SC38','PPPA package-total limits',3,['w3-a-13'],f'The proposed {form} contains {quantity} unit(s) of {drug}, each containing {strength} {u}, for a total of {total} {u}. It contains no other substance that independently requires special packaging. The described dosage form and packaging otherwise match the product-specific exception. No patient or prescriber non-CR request exists.',
      'Which assessment of the product-specific PPPA exception is correct?',opts,0 if ok else 1,f'해당한도는{limit}{u};제시된총량은{total}{u}이다. '+('상한이하이므로이조건을충족한다.' if ok else '상한을초과하므로이예외를적용할수없다.'),dict(drug=drug,strength=strength,count=quantity,total=total,limit=limit),'16 CFR1700.14(a)(10)(vi), (x), (xiv), (xxiv)')

assert len(CASES)==342, len(CASES)
