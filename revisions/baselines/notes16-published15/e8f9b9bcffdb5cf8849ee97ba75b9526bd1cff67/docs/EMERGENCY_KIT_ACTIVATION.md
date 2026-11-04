# Emergency-kit R2 활성화와 보호 마이그레이션

`2026-11-03.emergency-kit.1`은 J 다음에 두 본문만 적용한다. K
packaging/pamphlet 후보는 `WHOLE_UNIT_HOLD` 상태로 적용하지 않는다.

- `w4-a-19`: LTCF emergency-kit 원본 PDF 표의 `≤50 beds` 및 정확히
  50병상 포함을 복원한다.
- `w4-a-20`: inpatient hospice ADD 표의 `≤10 / 11–20 / ≥21 beds`와
  시설별 medication-category units를 복원한다.
- 출처는 신규 7개 ID를 추가하며 기존 registry 항목을 덮어쓰지 않는다.
  chapter highlights, module m14, day23, LAW-053/054, RF-054/056은
  검토된 원문대로 유지하며 신규 패치는 0개다.

후보의 `AUDIT_PENDING_NOT_APPLIED`, `activation: false` 및 작성자 census
메타데이터는 역사 기록으로 보존한다. 별도
`revisions/notes/emergency-kit-activation.json`이 실제 활성화 근거다.
`scripts/notes_emergency_activation.py`는 실제 독립 감사 schema의 nested
candidate/census binding, 두 본문 record/body hash, 54개 claim record hash와
KEEP, 원본 PDF 및 시각 확인 render, 4개 카드 전문과 3개 summary의
no-patch 증거를 확인한다. official URL은 정확한 HTTPS hostname으로 검사한다.

고정된 원본 SHA-256:

| 파일 | SHA-256 |
| --- | --- |
| R2 candidate | `b891ef1f7b61e70e7967f5628a64109400e28b76d1b7816320d0611325a5e374` |
| R2 census | `c3093bbc0c7c6e29f89cce15d4ce97be02ef71a469295d21cbd43969ea742cb1` |
| fresh independent review | `714cac739db1ac83e8fecd364854178dccd691a8170828b48ab92cafe8e0ab94` |
| effective M semantic notes | `e1519c0290ff220eb8251307e26340d76d394a7ec1f3e651194d4495a03f1824` |

이 활성화로 기존 ratio/intern/reporting/CDTM의 4개 OPEN/HOLD는 해결되지
않는다. OCR 병상 경계 교정은 그 4개와 별도 사안이다. 문항 감사나 canonical
release credit도 추가하지 않는다. 관련 직접 문항을 찾지 못한 linkage gap을
보존한다.

`protected-migration-emergency-kit.json`은 12번째 마이그레이션이다.
실제 pr187 commit `0e1c03302b38401ed53085af4ee402abfd0b46ec`의 J export와
build를 `complete-notes-census-wave8-9.md`, `notes-build-census-wave8-9.json`에
보존한다. 새 M export, M build의 의미 해시, 독립 감사 및 활성화를 먼저
검증하고 J export와 당시 J build 문맥으로 되돌린다. 이후 기존 11번째
`protected-migration-census-wave8-9.json`의 annotation-only semantic guard를
그대로 실행한다. 이전 manifest bytes나 원본 1,781개 보호 기준은 바꾸지 않는다.

Root 통합 순서:

1. fresh independent audit commit과 활성화 구현 commit을 각각 반영한다.
2. NOTE10/11/12 등록과 두 본문의 명시적 current census supersedence를
   완료한 후 full-corpus ledger를 재생성한다.
3. notes/study/refresh 산출물을 재생성한다. Census annotation은 M 의미
   해시에 포함되지 않으므로 `semantic_notes_sha256`은 유지한다.
4. `protected-migration-emergency-kit.json`의 `new_sha256`만 최종
   `site/notes/complete-notes.md` raw SHA-256으로 갱신한다. J snapshot과
   이전 migration의 hash는 갱신하지 않는다.
5. 다음 검증 및 최종 repository 전체 검증을 수행한다.

```sh
python scripts/build_ultimate_notes.py --check
python scripts/build_exam_study.py --check
python scripts/build_refresh.py --check
python scripts/verify_representative_protected.py
python -m pytest -q tests/test_emergency_note_activation.py tests/test_note_final_activation.py tests/test_ultimate_notes.py tests/test_exam_study.py tests/test_refresh.py
```

전용 테스트는 hash 재결합, 중복 KEEP를 통한 실패 은폐, 추가 card/source,
미확인 table render, 과거 J snapshot 재결합, 기존 11단계 guard 변경과
새 build 의미 해시 변조를 거부하는지 확인한다.
