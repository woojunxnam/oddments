# Form G Batch 2 — G031–G060: author source review
**Date:** November 24, 2026. **State:** DRAFT_NOT_PUBLIC; not independent legal/pharmacist certification. Legacy Massachusetts-specific MPJE blueprint through February 28, 2027.

## Read-back validation
- Batch 2: 30 contiguous items; cumulative G: 60 contiguous unique IDs. All 60 five-option items have nonempty choices and keyed explanations, source and decision fields; all key/explanation and critical-error tag checks passed.
- Batch 2: 18 SBA, 12 SATA; 7 direct, 15 scenario, 8 integrated; 17 selected-option critical error tags. Cumulative G format: {"multi":23,"single":37}; difficulty: {"scenario":32,"direct":14,"integrated":14}.
- Areas (batch 2): 6 / 10 / 8 / 6. Cumulative: 13 / 20 / 15 / 12. All 22 legacy competency identifiers are represented; 19 in batch 2. This is editorial coverage, not evidence that every legal rule is tested.
- Read-only comparison: 480 A–D indexed stems/decisions + 120 E + 120 F + 30 G batch 1 = 750 unique comparison IDs. No exact normalized stem or ID collisions. Token-Jaccard screening of stems and topics/decisions plus author review of close candidates; not an independent semantic duplicate classifier. Repeated high-value laws are allowed when the deciding fact, role, or action changes.
- Twenty-three initial draft items underwent substantive rewrites; six received a second focused revision. Critical-error objects match batch 1's letter/mode/reason format.
- Batch 2 GitHub file content SHA: `f50e126dba433deb06e460736a26e2367510dd9e`.
- Remaining two G batches: 60 items, areas 13/20/14/13; difficulty target remaining 16 direct, 34 scenario, 10 integrated; target final SBA/SATA range per contract. No publication until the 120-item bounded release gate.

## Per-item legal/source map and comparison screen
Closest IDs below are computational screening candidates, not findings of equivalence. Exact decision comparisons and counterfactuals are in the draft JSON. Source review relied on Massachusetts statute/regulation/Board texts and current CFR/USC text; Cornell LII mirrors supplemented official sources. Official PDF text was reviewed where available; screenshot retrieval of the vaccine policy returned HTTP 403, so no visual-PDF verification is claimed. URL presence was tested, not every destination's HTTP status. Future effective changes and independent human review are not certified.

| ID | Legacy competency | Topic | Exact legal citation | Top comparison candidates (similarity) |
|---|---|---|---|---|
| G031 | 1.1 | Schedule II technician assistance requires pharmacist approval evidenced by written policies | 247 CMR 8.05(1)–(2) | E30-066 (0.22), E30-002 (0.18), E113 (0.18) |
| G032 | 1.1 | Checked refill that still requires pharmacist consultation during break | 247 CMR 9.19(17)(a)–(c) | E30-248 (0.18), D109 (0.11), E30-016 (0.11) |
| G033 | 1.1 | Institutional director's personnel documentation duties | 247 CMR 8.06(1)(a)–(c) | E30-002 (0.14), G001 (0.13), E30-244 (0.13) |
| G034 | 1.1 | On-duty pharmacist limits access to authorized personnel | 247 CMR 9.19(16)(b)(2), (4); 9.01(8) | E30-266 (0.13), E30-346 (0.13), F015 (0.12) |
| G035 | 1.2 | Personal registration renewal within 60 days after expiration | 247 CMR 4.02(1)–(5) | E30-156 (0.28), E061 (0.26), E117 (0.17) |
| G036 | 1.2 | Certification lapse changes role and staffing-ratio classification | 247 CMR 8.04(1)–(3); 8.06(3) | E30-121 (0.29), E30-247 (0.24), G006 (0.24) |
| G037 | 2.1 | Out-of-state Schedule II nonnarcotic prescription presented after five-day window | M.G.L. c.94C §18(d), §23(a); 247 CMR 9.04(10); 21 CFR 1308.12(d)(4) | E30-059 (0.22), E30-269 (0.22), G018 (0.21) |
| G038 | 2.1 | Out-of-state oral Schedule IV prescription and follow-up request | M.G.L. c.94C §18(c) | F080 (0.28), E30-008 (0.26), E053 (0.22) |
| G039 | 2.1 | Hospital-exempt practitioner paper prescription requires printed name as well as signature | 21 CFR 1306.05(a), (g); 1301.22(c) | E30-239 (0.20), E30-270 (0.18), E30-267 (0.17) |
| G040 | 2.1 | DEA exemption for employees of an individual registered practitioner | 21 CFR 1301.22(b)–(c) | E30-268 (0.21), E30-220 (0.17), E051 (0.17) |
| G041 | 2.1 | Phendimetrazine versus phentermine scheduling | 21 CFR 1308.13(b)(6); 1308.14(f)(9); 105 CMR 700.002(C)–(D) | E046 (0.30), E30-174 (0.27), E30-144 (0.25) |
| G042 | 2.2 | Emergency medication authority when planning vaccination service | DPH/Board Policy 2023-02, IV(A)–(B), IX | D034 (0.15), E30-191 (0.14), G013 (0.14) |
| G043 | 2.2 | Pediatric vaccine communication when free program is not used | DPH/Board Policy 2023-02, V(A), VI(B)–(C) | E30-232 (0.17), E30-191 (0.16), E30-062 (0.15) |
| G044 | 2.3 | Patient counseling tailored to relevant missed-dose and monitoring instructions | 247 CMR 9.18(3)–(5) | E30-137 (0.19), E30-003 (0.15), E30-157 (0.10) |
| G045 | 2.4 | Controlled medication disposal after death of ultimate user | 21 CFR 1317.30(a)–(b)(2); 247 CMR 9.01(5) | F018 (0.19), E30-349 (0.18), D073 (0.18) |
| G046 | 2.5 | HIPAA oral agreement limited to friend's involvement in care | 45 CFR 164.510(b)(1)–(2); 247 CMR 9.01(16) | F100 (0.30), D116 (0.15), E30-053 (0.15) |
| G047 | 3.1 | Schedule V refill limit in Massachusetts despite federal distinction | 247 CMR 9.04(13) | G012 (0.23), E30-228 (0.23), E009 (0.21) |
| G048 | 3.1 | Positive identification of the person collecting a controlled prescription | 247 CMR 9.04(14)(a)–(d); 105 CMR 700.012(A)(3) | E30-005 (0.27), E076 (0.19), E005 (0.17) |
| G049 | 3.2 | Initial EPCS transfer corrupted by intermediary conversion | 21 CFR 1306.08(d)–(h); Board Policy 2023-10 §I | G020 (0.24), E087 (0.18), F109 (0.18) |
| G050 | 3.3 | Documenting DUR intervention after direct patient consultation | 247 CMR 9.17(1)(g), (2) | E30-087 (0.19), E054 (0.18), E30-240 (0.17) |
| G051 | 3.3 | PMP reporting for lawful nonresident delivery into Massachusetts | 105 CMR 700.012(A)(1), (5) | E30-318 (0.18), E029 (0.16), E30-250 (0.16) |
| G052 | 3.4 | Authorized person requesting Schedule II partial fill | 21 CFR 1306.13(b)(1)(iii), (b)(4) | E30-179 (0.24), E30-316 (0.21), E30-064 (0.19) |
| G053 | 3.6 | Prescriber-specific conventional package request does not carry to another prescription | 15 USC 1473(b) | E30-029 (0.30), E30-219 (0.21), E30-103 (0.14) |
| G054 | 3.7 | Expired manufacturer stock cannot be dispensed to patient | 247 CMR 9.01(12) | E30-228 (0.16), E30-089 (0.14), E30-238 (0.13) |
| G055 | 4.1 | DEA Form 222 unexecuted forms kept at another location | 21 CFR 1305.12(e) | F118 (0.21), F115 (0.17), F090 (0.17) |
| G056 | 4.2 | Red C exception requires all specified electronic retrieval capabilities | 21 CFR 1304.04(h)(4) | G010 (0.16), E013 (0.13), E30-085 (0.12) |
| G057 | 4.3 | Distinguishing mandatory shipping policy from Board delivery best-practice advisory | 247 CMR 9.02(1)–(3); Board Advisory: Medication Delivery and Shipping (rev. 1/9/2025), p.1 | E059 (0.21), E052 (0.19), E056 (0.16) |
| G058 | 4.4 | Interoperable electronic prescribing technology and biologic substitution | M.G.L. c.112 §12EE(d)–(e) | E30-070 (0.19), F080 (0.18), E30-359 (0.18) |
| G059 | 4.5 | Compounding a product withdrawn for safety or effectiveness | 21 USC 353a(b)(1)(C); 21 CFR 216.24 | E30-187 (0.15), F085 (0.12), E30-025 (0.11) |
| G060 | 4.7 | Board suitability discretion regarding pharmacy interest holder | 247 CMR 6.03(4) | E119 (0.10), E080 (0.09), E098 (0.09) |

## Source register

- G031: [source 1](https://www.mass.gov/doc/247-cmr-8-pharmacy-interns-and-technicians/download), [source 2](https://www.law.cornell.edu/regulations/massachusetts/247-CMR-8-05)
- G032: [source 1](https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download), [source 2](https://www.law.cornell.edu/regulations/massachusetts/247-CMR-9-19)
- G033: [source 1](https://www.mass.gov/doc/247-cmr-8-pharmacy-interns-and-technicians/download), [source 2](https://www.law.cornell.edu/regulations/massachusetts/247-CMR-8-06)
- G034: [source 1](https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download), [source 2](https://www.law.cornell.edu/regulations/massachusetts/247-CMR-9-19), [source 3](https://www.law.cornell.edu/regulations/massachusetts/247-CMR-9-01)
- G035: [source 1](https://www.mass.gov/doc/247-cmr-4-personal-registration-renewal-continuing-education-requirement/download), [source 2](https://www.law.cornell.edu/regulations/massachusetts/247-CMR-4-02)
- G036: [source 1](https://www.mass.gov/doc/247-cmr-8-pharmacy-interns-and-technicians/download), [source 2](https://www.law.cornell.edu/regulations/massachusetts/247-CMR-8-04), [source 3](https://www.law.cornell.edu/regulations/massachusetts/247-CMR-8-06)
- G037: [source 1](https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94c/Section18), [source 2](https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94c/Section23), [source 3](https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download), [source 4](https://www.law.cornell.edu/cfr/text/21/1308.12)
- G038: [source 1](https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94c/Section18)
- G039: [source 1](https://www.ecfr.gov/current/title-21/section-1306.05), [source 2](https://www.law.cornell.edu/cfr/text/21/1306.05)
- G040: [source 1](https://www.ecfr.gov/current/title-21/section-1301.22), [source 2](https://www.law.cornell.edu/cfr/text/21/1301.22)
- G041: [source 1](https://www.ecfr.gov/current/title-21/section-1308.13), [source 2](https://www.law.cornell.edu/cfr/text/21/1308.13), [source 3](https://www.law.cornell.edu/cfr/text/21/1308.14), [source 4](https://www.mass.gov/doc/105-cmr-700-implementation-of-mgl-c94c-0/download)
- G042: [source 1](https://www.mass.gov/doc/2023-02-vaccine-administration-pdf/download)
- G043: [source 1](https://www.mass.gov/doc/2023-02-vaccine-administration-pdf/download)
- G044: [source 1](https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download), [source 2](https://www.law.cornell.edu/regulations/massachusetts/247-CMR-9-18)
- G045: [source 1](https://www.ecfr.gov/current/title-21/section-1317.30), [source 2](https://www.law.cornell.edu/cfr/text/21/1317.30), [source 3](https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download)
- G046: [source 1](https://www.ecfr.gov/current/title-45/section-164.510), [source 2](https://www.law.cornell.edu/cfr/text/45/164.510), [source 3](https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download)
- G047: [source 1](https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download), [source 2](https://www.law.cornell.edu/regulations/massachusetts/247-CMR-9-04)
- G048: [source 1](https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download), [source 2](https://www.law.cornell.edu/regulations/massachusetts/247-CMR-9-04), [source 3](https://www.mass.gov/doc/105-cmr-700-implementation-of-mgl-c94c-0/download)
- G049: [source 1](https://www.ecfr.gov/current/title-21/section-1306.08), [source 2](https://www.law.cornell.edu/cfr/text/21/1306.08), [source 3](https://www.mass.gov/doc/2023-10-unfilled-prescriptions-pdf/download)
- G050: [source 1](https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download), [source 2](https://www.law.cornell.edu/regulations/massachusetts/247-CMR-9-17)
- G051: [source 1](https://www.mass.gov/doc/105-cmr-700-implementation-of-mgl-c94c-0/download), [source 2](https://www.law.cornell.edu/regulations/massachusetts/105-CMR-700-012)
- G052: [source 1](https://www.ecfr.gov/current/title-21/section-1306.13), [source 2](https://www.law.cornell.edu/cfr/text/21/1306.13)
- G053: [source 1](https://www.law.cornell.edu/uscode/text/15/1473), [source 2](https://www.cpsc.gov/Poison-Prevention-Packaging-Act)
- G054: [source 1](https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download), [source 2](https://www.law.cornell.edu/regulations/massachusetts/247-CMR-9-01)
- G055: [source 1](https://www.ecfr.gov/current/title-21/section-1305.12), [source 2](https://www.law.cornell.edu/cfr/text/21/1305.12)
- G056: [source 1](https://www.ecfr.gov/current/title-21/section-1304.04), [source 2](https://www.law.cornell.edu/cfr/text/21/1304.04)
- G057: [source 1](https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download), [source 2](https://www.law.cornell.edu/regulations/massachusetts/247-CMR-9-02), [source 3](https://www.mass.gov/doc/medication-delivery-and-shipping-pdf/download)
- G058: [source 1](https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXVI/Chapter112/Section12EE)
- G059: [source 1](https://uscode.house.gov/us/usc/119-124/t21/s353a/), [source 2](https://www.ecfr.gov/current/title-21/section-216.24), [source 3](https://www.law.cornell.edu/cfr/text/21/216.24)
- G060: [source 1](https://www.mass.gov/doc/247-cmr-6-licensure-of-pharmacies/download), [source 2](https://www.law.cornell.edu/regulations/massachusetts/247-CMR-6-03)

## Scope of approval
Author-source review and structural/read-back checks only. No independent pharmacist review, psychometric calibration, real exam reproduction, or claim of pass probability. Keep A–F, existing mixes, and published Pages untouched. Do not expose keyed content before the blind attempt.
