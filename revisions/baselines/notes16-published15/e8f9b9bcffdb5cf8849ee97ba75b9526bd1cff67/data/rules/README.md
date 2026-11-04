# Rule Registry

Rule JSON은 파일당 한 record입니다. 모든 record는 `schemas/rule.schema.json`을 통과하고 exact official section과 URL을 인용해야 합니다.

`content_hash`는 allowlisted semantic fields에서 계산됩니다. Semantic change 시 `content_version`을 올리고 hash를 갱신하십시오. Formatting-only change는 hash를 바꾸지 않습니다.
