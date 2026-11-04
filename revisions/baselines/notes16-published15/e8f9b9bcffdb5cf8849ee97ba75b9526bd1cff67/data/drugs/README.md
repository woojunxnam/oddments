# Drug Registry

Drug JSON은 파일당 한 record입니다. Indication은 FDA labeling 또는 DailyMed 같은 authoritative official source를 사용합니다.

각 `legal_consequences` 항목은 `summary`와 실제 canonical `rule_ids`를 가져야 합니다. 그 rule들의 current version/hash는 `verified_rule_dependencies`에 정확히 고정됩니다. Semantic change 시 `content_version`과 `content_hash`를 갱신하십시오.
