# GPT Phase 2 v3 LEGAL re-audit — 2026-08-13

## 결론

- 독립 검토 범위: frozen target `a3dd4cd9e0372dd4ff7c872a2ae3c3c851157363`의 changed 52 questions만 검토했다.
- 입력 검증: LEGAL A `40`, LEGAL B `12`; 두 batch는 disjoint이고 frozen `question_hashes`와 canonical bytes가 모두 일치했다.
- 판정: `KEEP=47`, `MINOR_EDIT=5`, `MAJOR_REWRITE=0`, `DELETE=0`.
- 기존 정답: `YES=49`, `PARTIALLY=3`, `NO=0`.
- 명백한 wrong key: `0`.
- legal ambiguity: `3` — MA-Q-0014, MA-Q-0018, MA-Q-0084.
- material drug-fact error: `0`. 다만 `MA-Q-0016`의 OxyContin acute-pain product context는 REALISM failure로 별도 처리했다.

## 수정 또는 보강이 필요한 IDs

- `MA-Q-0014` — Stem에 prescriber location이 없다. Massachusetts 밖에서 발행된 Schedule II prescription이면 initial partial fill은 issue date 후 5일 이내여야 하므로 day 12 partial fill이 무효이고 D가 성립하지 않는다.
- `MA-Q-0018` — Stem에 prescriber location이 없어 out-of-state Schedule II prescription이면 day 28 initial partial fill이 적법하지 않다. 또한 rule_ids가 Massachusetts patient-request partial-fill 및 30-day remainder authority를 직접 포함하지 않는다.
- `MA-Q-0041` — 정답 C는 21 CFR 1306.22(a)의 Schedule III/IV refill count/time limits에 의존하지만 direct rule_ids에 FED-CIII-V-REFILL이 없다.
- `MA-Q-0047` — 정답 D의 controlled-substance record duty는 21 CFR Part 1304에 의존하지만 direct rule_ids에 FED-CS-RECORDS-2Y가 없다.
- `MA-Q-0084` — Choice E의 'collaborative-practice record'는 247 CMR 16.03(5)(e)2가 요구하는 supervising physician custody의 patient medical record보다 불명확하다. direct rule authority도 이 기록 의무를 직접 포괄하지 않는다.

## Authority findings

- Direct dependency 누락 `4`: `MA-Q-0018`의 Massachusetts patient-request partial-fill authorities, `MA-Q-0041`의 `21 CFR 1306.22(a)`, `MA-Q-0047`의 `21 CFR Part 1304`, `MA-Q-0084`의 `247 CMR 16.03/16.04`.
- Shared authority freshness `1`: `MA-PMP-REPORTING` metadata는 Guide `5.1` URL을 가리키지만 Massachusetts current reporting page는 Guide `5.2`를 게시한다. 이번 audit result는 `105 CMR 700.012`와 current Guide `5.2` page를 사용했다.
- EPCS transfer `MA-Q-0019`, `MA-Q-0036`: `21 CFR 1306.08(e)`의 state-law condition을 `247 CMR 9.14`와 대조했고 Massachusetts에서 transfer pathway가 성립함을 확인했다.
- 모든 SATA option은 개별 검토했으며 key에서 빠진 true option 또는 포함된 false option은 발견하지 못했다. `MA-Q-0084`의 E는 의무 자체가 아니라 record location 표현이 불명확해 `PARTIALLY`로 판정했다.

## Current official sources checked

- [Massachusetts General Laws c.94C § 18](https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section18)
- [Massachusetts General Laws c.94C § 23](https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section23)
- [105 CMR 700](https://www.mass.gov/regulations/105-CMR-70000-implementation-of-mgl-c94c)
- [105 CMR 721](https://www.mass.gov/regulations/105-CMR-72100-standards-for-prescription-format-and-security-in-massachusetts)
- [247 CMR 9](https://www.mass.gov/regulations/247-CMR-900-professional-practice-standards)
- [247 CMR 16](https://www.mass.gov/doc/247-cmr-16-collaborative-drug-therapy-management/download)
- [Massachusetts PMP reporting / Guide 5.2](https://www.mass.gov/info-details/pharmacy-reporting-and-data-submission)
- [DEA EPCS transfer rule summary](https://www.dea.gov/stories/2023/2023-09/2023-09-01/revised-regulation-allows-dea-registered-pharmacies-transfer)
- [DEA current controlled-substance list](https://www.deadiversion.usdoj.gov/schedules/orangebook/orangebook.pdf)
- [FDA SUBLOCADE label](https://www.accessdata.fda.gov/drugsatfda_docs/label/2025/209819Orig1s031lbl.pdf)
- [FDA XYWAV/XYREM REMS](https://www.accessdata.fda.gov/drugsatfda_docs/label/2025/021196Orig1s047%2C212690Orig1s017lbl.pdf)

## Scope and integrity

Canonical questions, rules, drugs, lifecycle fields와 release status는 수정하지 않았다. 이 보고서와 4개 `FULLY_ADJUDICATED` audit JSON만 산출 대상이다.
