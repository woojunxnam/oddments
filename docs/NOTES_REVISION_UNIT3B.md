# Unit 3B notes revision and remote build contract

Unit3A note source와 migration manifest는 그대로 둔다. 새 supervision/training revision을 순서대로 합성하며,기존 질문이 요청한 revision ID에는 정확한 이전 snapshot을 반환한다. 이전59개 객체의 complete-record hash가 달라지면 generation worker가 실패한다.

보호 검사는 notes/ 전체와 canonical data/audits를 계속 검사한다. 두 번째 migration은 site/notes/complete-notes.md 한 경로만 허용하며,이전 migration hash,이전 generated export copy/hash,새 source/hash 및 새 export/hash를 연결한다. 이미 검증된 old baseline을 재생성하거나 초기화하지 않는다. 전용 negative tests가 두 revision source·이전 export·기존 policies의 변경을 거부한다.

로컬 환경이 실패하여 feature branch 전용 일회성 materialization workflow를 사용한다. 해당 workflow는 정확한 branch와 명시적인 materialization commit message에서만 실행하고,동일 branch의 allowlisted generated files만 non-force push한다. source/canonical bytes는 변경하지 않으며,worker 기록을 확인한 뒤 workflow는 merge 전에 제거한다. 기존 QA/release gate는 유지한다. 이 workflow는 주기 실행·외부 통지·계정 변경을 만들지 않는다.

실제 시험 문항은 English, 선택지별 해설과 학습노트는 한국어다. author review,peer,자동QA,독립 canonical audit는 별도 상태다. 노트의 이전 읽음·북마크는 삭제하지 않고 새 판본 숙련으로 바꾸지 않는다.
