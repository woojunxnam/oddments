# 실제 publication의 두 SHA 결박을 위한 source guard

실제 actor는 `/root/notes16_engineering`, source commit은 `ceb646c3`이다.
Root HEAD118fe22e의 별도 worktree에서 구현했으며 실제 publication config,
activation source, migration 승인 파일은 변경하지 않았다.

실제 공개 PR192 config는 old selection SHA196f8cc5…와 bank SHA835e3d3d…를
갖는다.111+33 및 실제 fresh38의26개 negative source 연결로 archive warning과
결정적 selection/bank wrapper가 바뀌었으므로 이를 새 실제 바이트에 결박해야 한다.
기존 SHA를 alias로 면제하거나 config를 frozen 보호 목록에서 제거하지 않는다.

새 guard는 다음 두 값만 갱신할 수 있다.

- `representative_selection.sha256`
- `additional_banks` 중 path가 원 REPRESENTATIVE_BANK인 정확히 하나의 descriptor의 `sha256`

원 두 SHA는 실제 공개 closure의 원 selection/bank SHA와 같아야 한다. 새 두 SHA는
현재 HEAD에 실제 커밋된 해당 파일 바이트와 같아야 한다. 두 값만 원복한 encoded JSON은
원 config와 완전히 같아야 한다. Path, enabled/scope, bank 추가·순서·개수, 다른 필드 및
bool→int/숫자 type 변경도 허용하지 않는다. 원 config 원바이트는 실제 old preimage로 보존한다.

현재 selector의 `recommended_ids`는 원 공개202개 전체의 순서·ID와 같아야 한다.
기존 bank의 archive-input-digest 한 값 경계, 모든 원 question/key/source/metadata,
과거 warning 이력, actual native/current negative source와 결정적 builder 검증을
그대로 수행한다. 현재 primary와 strict supplementary known-negative/default 검사 및
context38 default exclusion도 다시 실행한다. 새로운 RELEASED나 default 승격은 없다.

실제 파일에 대한 read-only 확인에서 아래 두 raw SHA와 원202 순서 전체 불변을 확인했다.
이 확인은 root의 실제 config 갱신·커밋 이후 guard/전체 QA를 대신하지 않는다.

```
representative bank: eb94fa96864632d408d220a5ac2534c843016af60559551352f4096f2b70f405
selection:          1764c90fd801cf1cd70368e0d49456256d57dbeac57ae8e8c7b5b765bafd7695
```

`subset-qa.log`: 새 coupled-config 경계와 기존 wrapper 검사43 PASS,2.57초.
`combined-qa.log`: 새 config/기존 wrapper/published15 closure·full-preimage/supplementary
trace를 결합한100 PASS / 0 FAIL / 0 ERROR,222.12초. 합성 strict-bank 경계 stub은 테스트용이며
실제 native/source proof나 publication verification으로 보고하지 않는다.

Root는 실제 현재 두 SHA만 config에 반영·커밋한 뒤 실제 guard와 current publisher,
결정적 생성물, 전체 QA/CI 및 final16을 검증해야 한다. 원011 HOLD와 source-blocked
노트를 법규 PASS로 올리거나 기존 독립·현실성 release 정책을 바꾸지 않는다.
