# 주제별 기존 문항 학습과 공개 선택 보류

기존 canonical 본문·정답·grade·397개 공개 payload를 수정하지 않고, 현재 해시로 독립 선별한 9개 문항을 3개 주제 묶음으로 연결합니다. 한국어 통합노트 단락과 기존 viewer·저장 형식을 재사용합니다. 기존 해설은 영어이며 한국어 해설 완성으로 인증하지 않습니다. 새 문항이나 새 canonical RELEASED 승격으로 집계하지 않습니다.

공식 원문 22개와 현재 문항 28개를 별도 실제 세션에서 실독했습니다. 첫 선별 14개 권고 뒤 적용 조항이 누락된 MA-Q-0058과 환자 대리인 사실관계가 불충분한 MA-Q-0227을 보류했습니다. 남은 12개는 다른 실제 비작성자 세션이 모든 보기·해설과 공식 capture 26개를 추가 검토했습니다. MA-Q-0397의 may/must 해설 불일치, MA-Q-0020의 메타형 질문·반복 해설, MA-Q-0424의 난도·오답 구성 결함을 확인해 3개를 추가 보류했습니다. 최종 9개를 선택하며, 19개 보류 문항은 기본 모드·시험·오답·북마크·가이드 override·직접 링크·채점에서 제외합니다. 기본 active는 378개입니다. 기존 풀이와 기록·원래 문항 ID/정답/본문은 보존합니다. 이전 부정 판정을 다른 KEEP으로 덮어쓰지 않습니다.

`public-set-review.json`, `public-two-item-addendum.json`, `public12-second-opinion.json`은 실제 source/current-hash 검토이며 native data/audits 등록이나 canonical 등급 변경을 뜻하지 않습니다. 앞선 긍정 판정은 후속 current-hash 부정 판정의 승격 근거로 사용하지 않습니다. `public-official-source-evidence.tar.gz`와 `public12-official-source-evidence.tar.gz`에는 공개 1차 자료 원문과 조회·해시 증거만 있으며 공급자 스크린샷·비공개 초안·내부 이미지 매핑은 없습니다. eCFR의 본문 반영 시점 등 실제 확인 한계는 검토 파일에 명시합니다.

이전 후보의 실행 결과는 Node 계약 11 PASS, pytest wrapper 1 PASS, 실제 HTTP 브라우저 15 PASS/JS 오류0, validate_all 오류0/기존 경고9, generate_artifacts --write 성공, generate_artifacts --check drift0으로 원증거를 보존합니다. 9개 선택·19개 보류 후보는 확대된 부정 판정 보존 계약과 실제 HTTP 브라우저를 다시 실행하며, 전체 pytest·GitHub CI·Pages는 최종 후보의 실제 실행 결과로 확인합니다. 기존 main QA의 runner 디스크 부족은 통과 fixture만 정리하고 실패 fixture는 보존하는 pytest 기본 설정으로 완화했습니다. 보호 inventory1781과 결박 입력6466 파일의 원본 바이트는 동일하며, 이전 후보의 QA나 한정 배포 예외를 최종 후보의 PASS로 합산하지 않습니다.

336개 원자료 참조·334개 기존 감사 기록·중복2개는 비공개 Drive 메타데이터와 대조했고 원문을 내려받거나 재전사하지 않았습니다. 84개 비공개 초안의 실제 별도 세션 intake 검토에서 현실성84개가 미달해 그대로 공개하지 않았습니다. 보완본·현재 해시 감사·상세 매핑과 원자료 URL은 비공개로 보존합니다. 신규 canonical 입장에는 원1781/439 및 notes16 source binding을 보존하는 엄격한 successor 절차가 필요하며 이를 숫자 수정이나 검사 생략으로 우회하지 않습니다.
