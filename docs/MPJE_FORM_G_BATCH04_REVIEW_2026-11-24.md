# Form G Batch 4 — Author Legal Review and Read-back QA
Date: 2026-11-24 | Status: DRAFT — NOT RELEASED
Scope: G091–G120; legacy NABP blueprint through February 28, 2027.

## Final-batch decisions
- Two close-overlap candidates replaced: G100 and G117. G091 simplified to a single break to avoid ambiguous aggregation; G108 expanded to cover both documentation accuracy and federal retention; G115 classified as direct knowledge. Initial G91–G99 draft identifiers were padded to the canonical G091–G099 format before read-back.
- The specialty-pickup advisory item explicitly distinguishes Board recommendations from binding law.
- Comparison set: 480 indexed A–D + 240 E/F + 90 earlier G = 810. Normalized exact stem/ID comparison found zero collisions for batch 4. Nearest IDs were screened by token Jaccard over stems and topic/decision text; this is not proof of semantic uniqueness. Recurring core laws are intentional when the legal decision differs.

## Full-form structural read-back
- 120 sequential unique IDs; 120 distinct normalized stems; 600 options and option-specific rationales; answer-key/Correct-Incorrect prefix alignment; five unique choices per question; required citation/source and legal metadata; critical-error object letter/mode/reason validation. Zero reported errors.
- Exact normalized-stem/ID collision against all 720 A–F items: zero.
- Areas 26/40/29/25; all 22 competency quotas match the frozen contract.
- Difficulty: 30 direct / 66 scenario / 24 integrated. Type: 76 single / 44 multi. Critical error flags: 63 total; 9 in batch 4.
- Batch 4: areas 6/10/7/7; 19 competencies; difficulty 8/17/5; single 21, multi 9.
- JSON blob: `ac4fd6c10c8b325c4092cc7d3ea94f4817ca3e85`

## Item source and overlap ledger
| ID | Competency | Topic | Citation | Closest comparison IDs | Revision |
|---|---|---|---|---|---|
| G091 | 1.1 | Maximum temporary absence of a sole pharmacist | 247 CMR 9.19(17)(a) | E30-016, F079, E30-252 | 2 |
| G092 | 1.1 | Manager responsibility for adequate staffing despite legal ratio | 247 CMR 9.23(2)(c)-(d) | G061, E30-249, E30-128 | 1 |
| G093 | 1.1 | DEA registration and employed dispensing pharmacist | 21 CFR 1306.06 | E30-267, G040, E30-117 | 1 |
| G094 | 1.2 | Pharmacist licensure application fees after Board review | 247 CMR 3.01(9) | E30-257, F067, E064 | 1 |
| G095 | 1.2 | Board-approved home-study CE program design | 247 CMR 4.05(3)(c)-(e) | E30-226, F063, F076 | 1 |
| G096 | 1.2 | Technician licensure education while enrolled in high school | 247 CMR 8.02(3)(a)-(e) | G006, E30-031, E30-002 | 1 |
| G097 | 2.1 | Schedule classification of a barbiturate by dosage form | 21 CFR 1308.12(e)(3); 1308.13(c)(2); 105 CMR 700.002(B)-(C) | E30-010, G041, E046 | 1 |
| G098 | 2.1 | Pain-management training prerequisite excludes veterinarians | M.G.L. c.94C §18(e) | E116, E30-152, E30-112 | 1 |
| G099 | 2.1 | Quantity exception for an implantable infusion pump | M.G.L. c.94C §23(d) | G009, E30-214, E30-069 | 1 |
| G100 | 2.1 | Same-state prescribing-only office and separate DEA registration | 21 CFR 1301.12(a),(b)(3) | E088, G040, E30-238 | 2 |
| G101 | 2.1 | Prescription issuance date versus future earliest-fill instruction | 21 CFR 1306.05(a); 1306.12(b)(1)(ii) | F107, G018, G019 | 1 |
| G102 | 2.2 | Initial vaccine training for pharmacist or pharmacy intern | Board/DCP Policy 2023-02 §III(C)(1), revised 9/4/2025 | G013, E30-221, E30-245 | 1 |
| G103 | 2.2 | COVID vaccine prior-dose verification recommendation versus reporting | Board/DCP Policy 2023-02 §IV(E)-(G), revised 9/4/2025 | E30-062, E30-014, E30-245 | 1 |
| G104 | 2.3 | Measuring device recommendation versus dispensing a device | 247 CMR 9.18(9) | D047, G044, E30-155 | 1 |
| G105 | 2.4 | MassHealth unit-dose return excluded by third-party payment | 130 CMR 456.621(A), (B)(1) | D049, D050, G016 | 1 |
| G106 | 2.5 | HIPAA oral request to suspend accounting of disclosures | 45 CFR 164.528(a)(2) | D007, F101, F035 | 1 |
| G107 | 3.1 | Documented good-faith refusal of unverified interstate controlled prescription | M.G.L. c.94C §18(c) | G038, E30-128, E075 | 1 |
| G108 | 3.2 | Automated initial EPCS transfer accuracy and record retention | 21 CFR 1306.08(f)(2),(4)-(6),(h); compare 21 CFR 1306.25(c) | G049, G020, E005 | 2 |
| G109 | 3.3 | MassPAT access when practitioner license suspended | 105 CMR 700.012(F)(1)-(3) | G065, D100, E30-156 | 1 |
| G110 | 3.4 | Practitioner requests Schedule II partial fill after issuance | 21 CFR 1306.13(b)(3), (5)(i) | G082, G029, G025 | 1 |
| G111 | 3.5 | Institutional Schedule III-V label exception quantity threshold | 21 CFR 1306.24(c)(1)-(4) | E092, F038, E013 | 1 |
| G112 | 3.6 | Child-resistant packaging exemption for potassium unit doses | 16 CFR 1700.14(a)(10)(vi) | E087, G009, E30-219 | 1 |
| G113 | 3.8 | Single small pseudoephedrine package logbook exception | 21 CFR 1314.30(a) | G024, E30-094, G082 | 1 |
| G114 | 4.1 | CSOS electronic order cannot be endorsed to another supplier | 21 CFR 1305.23; 1305.22(a) | D064, D063, G089 | 1 |
| G115 | 4.2 | Actual receipt date for controlled stock records | 21 CFR 1304.21(d) | E099, G029, E018 | 2 |
| G116 | 4.2 | Controlled-substance access following DEA registration denial | 21 CFR 1301.76(a) | E088, E30-177, E30-057 | 1 |
| G117 | 4.3 | Specialty pharmacy delivery to retail pickup location | Massachusetts Board of Registration in Pharmacy, Advisory: Medication Delivery and Shipping, revised January 9, 2025, Delivery to Alternative Locations | D120, G057, F068 | 2 |
| G118 | 4.5 | USP 797 competency of pharmacists who directly supervise without compounding | USP <797> §§2.1-2.3; official USP <797> FAQ Q47 (Dec. 11, 2023); 247 CMR 9.01(3) | E30-120, E30-342, E30-186 | 1 |
| G119 | 4.5 | Section 503A requirements for ingredients other than bulk drug substances | 21 USC 353a(b)(1)(A)-(B) | G028, E30-187, E30-025 | 1 |
| G120 | 4.7 | Board waiver petition must demonstrate substantive safeguards | 247 CMR 14.01(1)-(3) | G048, E30-017, E30-260 | 1 |

## Source review limitations
- Author checked relevant official Massachusetts laws/regulations and Board documents, federal regulatory text and official USP FAQ. Cornell LII text reproductions supplement agency sources. Source URLs are stored per question. No independent licensed-pharmacist or attorney certification; no empirically calibrated difficulty or real-exam predictive validation.
- Vaccine Policy 2023-02: indexed text identifies the September 4, 2025 revision; PDF image retrieval showed an older copy on one page and returned HTTP 403 on others. G102–G103 are explicitly tied to the cited revision; reconfirm the controlling policy copy in the bounded final release review. Delivery advisory text identifies the January 9, 2025 revision; PDF image request for alternative-location section returned 403. USP official FAQ Q47 was visually checked.
- October 2026 proposed amendments to 105 CMR 700 are not treated as effective solely on the basis of a hearing notice. Verify the published effective regulation at the release gate.
- Source URL presence/scheme was checked, not an exhaustive HTTP link audit. Structural read-back of 120 questions is not a fresh independent substantive legal review of the earlier 90 questions.

## Release decision
Authorship complete; draft remains isolated. Next gate: bounded legal review of the complete Form G (including source-version limitations), final key/choice and manifest validation, application/UI/storage-history regression, merge and public Pages verification. Do not publish before those checks. Existing A–F and public Pages remain untouched.
