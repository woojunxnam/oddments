# B 세션 공식 근거 열람 메모

실제 actor/session: `/root/independent_wave12_b`.
Auditor instance: `GPT:/root/independent_wave12_b:20261104`.
40개 assigned-visible-input 원문과 111개의 nearest-visible-input 후보의 stem 및 모든 보기를 실제 읽었다. 해당 후보의 기존 키·해설·판정은 비교 입력으로 출력하지 않았다. 배정 40개의 키·한국어 core·각 보기 해설·learning boundary는 모두 읽었다.

## 적용한 primary 범위

- 247 CMR 9 PDF: 9.01(4),(16),(21), 9.02, 9.04(1),(12),(13), 9.15, 9.16(1),(7),(8), 9.17 전부, 9.18 전부. 제품/수량 검증, prescription authenticity, DUR, profile 검색 및 합리적 정보확보, REMS와 상담의 별도 의무를 구분했다. 9.16의 institutional sterile compounding 예외와 9.18 inpatient 예외를 유지했다.
- MA c.94C §21A 전체 실질 조문: new prescription DUR, offer 방식·offsite toll-free access와 label 번호, 상담 수락·거절·기록 추정, inpatient 예외. 규정의 각 처방 counseling offer와 신규/중요 therapy 상담을 함께 읽었다.
- 42 CFR 456.705 전체: Medicaid state-plan DUR, counseling/offsite telephone, profiling. 이 federal Medicaid 틀이 MA 의무의 cash 예외를 만들지는 않는다.
- 21 CFR 208.20, 208.24 전체: FDA 승인 Guide의 형식·dispensing 의무. 208.24(e)의 208.26 면제 참조를 보존하고 refill 일괄 면제를 인정하지 않았다. 특정 환자 면제의 세부 adjudication은 이번 사실에 없어 수행하지 않았다.
- 21 CFR 310.501 및 310.515 전체: 각 oral contraceptive package, acute-care/LTCF 최초투여 전 및 매 30일, estrogen-progestogen oral contraceptive의 310.515(e) 예외. 정보 제공 시계는 refill validity가 아니다.
- 21 CFR 1306.04 전체, 특히 (a): corresponding responsibility는 federal controlled substances 문맥에서 사용했다.
- 45 CFR 160.103의 Business associate·전자매체/ePHI·health information·individually identifiable health information·PHI·use 정의. 164.302의 ePHI Security 적용 범위.
- 45 CFR 164.502 전체를 읽고 이번 판단에는 (a) 일반 허용, (b) minimum necessary 및 예외, (e) BA, (g) representative 범위를 인용했다. 새 reproductive-health 특수 규정의 실제 효력·vacatur를 인증하지 않았고 그 부분을 정답 근거로 사용하지 않았다.
- 164.504(e)의 BA 계약·허용사용 제한·명시적 예외, 164.506 전체의 TPO/consent, 164.508 전체의 marketing/sale·authorization·서식, 164.510(b)(1)-(3)의 가족 care 참여·환자 agreement/objection 및 pickup judgment, 164.514(d)의 직무별 접근·minimum necessary, 164.530(c),(h)의 safeguards와 권리 waiver 금지.
- 164.520 전체: NPP 내용·권리·direct-treatment good-faith acknowledgment·emergency와 electronic notice 및 문서화. 164.524(a)·164.526(a)의 access·amendment 권리도 직접 읽었다. 164.522를 별도로 가져왔지만 이번 legal authority로 세지 않았다.
- MA c.112 §12F 전체: 일반 status-based consent 범주와 service-limited 질환/HIV 예방 범주, 기록의 비밀유지·minor written consent·proper judicial order·life/limb danger 통지를 구분했다. 구체 서비스가 없는 배정 4문항은 일반 키는 옳아도 맥락 특정이 필요하다.

FDA Patient Labeling Resources의 CMI/Medication Guide 구분, FDA What's in a REMS?의 소수 Guide만 REMS에 포함된다는 설명과 제품별 ETASU·등록 범위, CDC About VISs의 정의·해당 접종 전 제공 범위도 직접 읽었다. FDA의 PMI proposed rule을 시행 규칙으로 쓰지 않았다.

## 실제 retrieval 한계

원문·추출문·메타데이터는 `official/`에 있다. 메타데이터에는 실제 UTC offset이 있는 시작·완료 시각, HTTP status, final URL, 응답 headers와 payload SHA가 있다. 보고서는 각 원문·추출문·메타데이터의 SHA를 결합한다. 현재 eCFR 페이지는 2026-11-02까지로 표시되므로 조회일 2026-11-04와 혼동하지 않았다. PDF publication date를 모든 조항의 별도 commencement로 추정하지 않고 effective date는 UNKNOWN으로 남겼다.

`medicaid-dur`의 US Code URL은 실제 404라 법률 확인으로 세지 않았으며 42 CFR 456.705와 MA 직접 조문으로 대체했다. registry `src-a5d51fbfaa5c`의 URL은 200 PDF여도 실제 문서 제목은 2026-04-01 Strengthening HIV Prevention, Reducing Stigma, and Expanding PrEP Access이다. general PrEP 접근·stigma·billing 문서이며 minor-consent-specific authority로 세지 않았다. 이 source identity 차이는 대체 primary와 별도로 남겼다.

Firecrawl scrape는 connected account credits 부족으로 실행되지 않았다. free gov search는 정확한 official locator 발견에만 사용했다. 공식 retrieval은 정상 inherited proxy/CA와 TLS verification을 유지한 urllib GET이다. 최초 연결 probe의 잘못 추정한 247-CMR-9-code-of-professional-conduct 경로는 404였다. 그 probe의 원 payload는 보존하지 않았고 법적 근거나 retained evidence로 주장하지 않는다.

## 현실성 판정의 제한

SATA all-four-true가 허용된다는 점을 유지했고 그 조합만으로 FAIL을 주지 않았다. 명시적으로 보관된 family 변형의 존재만으로도 FAIL을 주지 않았다. 실제 비교한 문구·사실·판단, default202 포함 여부와 각 distractor의 법적 혼동을 검토했다. COUN11의 세 문항은 setting·package·제품 예외를 구체적으로 판단하므로 archived drill 범위에서 10개 기준 PASS로 판정했다. 나머지는 극단적인 무제한 면제·포괄 허용·상식상 명백한 오류 등의 단서 또는 미특정 서비스/제품으로 독립적인 시험 품질이 부족하다. 새 canonical admission/release credit은 전부 0이다.
