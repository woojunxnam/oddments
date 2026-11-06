# Git source reader 후속 강화

시작 기준은 successor worktree의 `2880a4537137d90a6bb6a300bdecb955fab415fd`이며 첫 인프라 commit은 `9f2f4551392fc45305b563bfdc38eff5f83f67bd`입니다. 기존 독립 검토의 58 PASS와 P2/R1 finding은 원문 그대로 보존했습니다. Git symlink의 target 문자열을 regular source로 읽던 공백을 exact tree mode·OID 검사로 수정했습니다.

현재 4파일 해시에 대해 작성자 63 PASS와 별도 reviewer의 63 PASS를 각각 실제 확보했습니다. 독립 검토는 Git 정상 경로 7개, unsafe 경로 4개 및 다른 유효 blob을 바꿔치기한 mock OID 불일치를 확인했고 새 finding은 0개입니다. mock은 실제 legacy replay가 아닙니다. 원1781 보호 검증의 단일 실제 PASS는 이전 단계의 별도 증거이며 이번 reader 수정 뒤 반복 실행하지 않았습니다.

새 canonical·rule·drug·audit 추가와 활성화·admission·RELEASED·배포 credit은 모두 0입니다. 기존439/397·격리2개·delivery hold16개·노트306단위/7086명제를 유지했습니다. 이 결과를 UI 후보 f877의 CI 결과로 사용하지 않았으며 새 pytest 설정을 가져오거나 rebase하지 않았습니다. 실제 admission에 필요한 승인·native audit·source context·legacy replay·producer·coverage 연결은 계속 미구현/차단 상태입니다.
