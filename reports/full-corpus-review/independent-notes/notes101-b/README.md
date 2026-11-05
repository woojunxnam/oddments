# 독립 노트 감사 — notes101-b

실제 새 감사 세션 `/root/independent_notes101_b`가 배정된 10단위와 169명제를 검토했다. 본문·census·질문·queue·생성 산출물은 수정하지 않았다. 이 결과의 canonical release credit와 question audit credit는 모두 0이다.

- 명제: KEEP 161, LEGAL_HOLD 1, SOURCE_BLOCKED 7.
- 단위: KEEP 6, LEGAL_HOLD 3, SOURCE_BLOCKED 1.
- 완전성: COMPLETE 8, OMISSIONS_FOUND 2.

`w3-b-16`의 개인 breach 통지 “최대 60 calendar days”는 §164.404(b)가 유보하는 §164.412의 법집행 지연을 생략했다. 관련 문항 MA-EXP-0509에는 “no authorized delay”라는 조건이 있지만 노트 본문에는 없다. 문항의 조건으로 노트를 보완하지 않았고 해당 명제를 LEGAL_HOLD로 판정했다.

`w1-a-10`의 본문은 complaint·criminal charge 단계도 licensure 보호의 trigger로 열거한다. Census의 관련 명제는 sanction만 서술하여 제재가 아직 없는 complaint와 charge의 보호를 독립적으로 식별하지 않았다. `w3-c-1`은 pharmacist 업무 표에 screening을 명시하지만 23개 census에는 이 업무가 별도로 열거되지 않았다. 두 절 모두 OMISSIONS_FOUND/LEGAL_HOLD다. 이는 본문에 없는 모든 법률 세부사항을 census에 추가하라는 결론이 아니다.

기존 SOURCE_BLOCKED 7명제는 유지했다. Minor guidance URL이 반환한 실제 문서는 2026-04-01 PrEP 서신이며 본문이 주장하는 2026-03-10 minor-consent guidance와 다르다. §12F와 별도의 현행 DCP 26-08-125 서신을 통해 minor consent, training, NPI, labeling/statewide guidance의 경계는 확인했지만 문서 귀속·EOB 세부 보호·shield reporting 적용관계를 자동으로 해제하지 않았다.

공식 HTTPS endpoint 30개에서 원문 바이트와 응답 metadata를 새로 보존했다. PDF는 pdftotext로, HTML은 텍스트를 추출하고 원문·추출문 SHA를 기록했다. eCFR의 표시 갱신일, retrieval일, 개별 시행일을 구분했다. eCFR 화면에 reproductive-health 조문 문자가 남아 있다는 사실만으로 집행 가능성을 확정하지 않고 HHS의 vacatur 공지를 함께 읽었다. Firecrawl 요청은 계정 credit 부족으로 실행되지 않아 공식 HTTPS 직접 다운로드로 진행했다.

배정 packet·assignment의 원바이트를 보존하고 실제 본문 UTF-8 SHA, census raw SHA, census unit record 및 169 claim record의 canonical SHA를 재계산했다. Sparse tree에서 누락된 immutable preimage를 우회하여 loader를 실행하지 않았다. Root의 strict inventory snapshot은 입력 provenance이며 독립 법규 PASS 근거가 아니다.

관련 원문 33문항의 stem, 모든 선택지, key, 전체 해설을 읽었다. 이 중 30개는 Root가 현재 커밋에서 추출한 projection과 visible fields가 모두 일치했고, 본문의 범위 링크에 따라 MA-EXP-0302–0304도 추가로 읽었다. Root가 제공한 관련 derived 7개, 10단위의 렌더링 텍스트, VAX01–04 연결 검토 문서도 읽었다. Derived의 actual effective source hashes는 배정 본문과 맞는다. RF-C-privacy의 2개 stored hash는 오래된 metadata이지만 effective source_hash 값은 현재 배정값이다. 이러한 학습 산출물은 독립 법규 근거로 사용하지 않았다.

상세 명제별 판단은 `review.json`, 원입력 대조는 `input-validation.json`, 공식 원문은 `sources/`에 있다. Envelope는 evidence commit 이후 별도 임시 파일로 만들며 worker branch에 커밋하지 않는다. 실제 postcommit native 검증은 별도 임시 proof 파일로 Root에 전달한다.
