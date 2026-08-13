# Phase 2 Batch A LEGAL_VERIFICATION

## 결론

| Verdict | Count |
|---|---:|
| `KEEP` | 37 |
| `MINOR_EDIT` | 2 |
| `MAJOR_REWRITE` | 1 |
| `DELETE` | 0 |

- `audit_status`: `FULLY_ADJUDICATED`
- frozen SHA: `67464e7a7ff2cfe88285c7c0f0f4164e92df46cd`
- non-`KEEP`: `MA-Q-0023`, `MA-Q-0024`, `MA-Q-0043`
- 모든 SATA option은 proposition별로 별도 판정했고, drug-linked item은 current DailyMed labeling과 21 CFR Part 1308 schedule을 교차 확인했다.

## Item-by-item adjudication

| Question_ID | Verdict | Existing_Answer_Correct | Proposed_Answer | Finding |
|---|---|---|---|---|
| `MA-Q-0011` | `KEEP` | `YES` | A: Decline the refill and require a new lawful Schedule II prescription. | key 일치; `FED-CII-NO-REFILL`, `FED-CS-SCHEDULES`의 current trigger·deadline·scope 확인 |
| `MA-Q-0012` | `KEEP` | `YES` | B: Treat the Schedule II prescription as expired under the 30-day Massachusetts validity rule. | key 일치; `MA-CII-VALIDITY-30D`, `FED-CS-SCHEDULES`의 current trigger·deadline·scope 확인 |
| `MA-Q-0013` | `KEEP` | `YES` | C: The nonnarcotic Schedule II out-of-state pathway may permit dispensing after verification. | key 일치; `MA-CII-OUTSTATE`, `FED-CS-SCHEDULES`의 current trigger·deadline·scope 확인 |
| `MA-Q-0014` | `KEEP` | `YES` | D: The same pharmacy may dispense the documented remainder before the 30-day issue-date deadline. | key 일치; `MA-CII-REMAINDER-30D`, `FED-CS-SCHEDULES`의 current trigger·deadline·scope 확인 |
| `MA-Q-0015` | `KEEP` | `YES` | E: The prescriber must address the Massachusetts initial-opiate seven-day limit or document an applicable exception. | key 일치; `MA-OPIOID-SEVEN-DAY`, `FED-CS-SCHEDULES`의 current trigger·deadline·scope 확인 |
| `MA-Q-0016` | `KEEP` | `YES` | A: The initial outpatient opiate supply generally may not exceed seven days without a documented statutory exception. | key 일치; `MA-OPIOID-SEVEN-DAY`, `FED-CS-SCHEDULES`의 current trigger·deadline·scope 확인 |
| `MA-Q-0017` | `KEEP` | `YES` | B: A minor's opiate prescription is generally limited to seven days unless the prescriber documents a statutory exception. | key 일치; `MA-OPIOID-SEVEN-DAY`, `FED-CS-SCHEDULES`의 current trigger·deadline·scope 확인 |
| `MA-Q-0018` | `KEEP` | `YES` | C: Do not refill the Schedule II prescription; a new lawful prescription is required. | key 일치; `FED-CII-NO-REFILL`, `FED-CS-SCHEDULES`의 current trigger·deadline·scope 확인 |
| `MA-Q-0019` | `KEEP` | `YES` | D: Use the one-time pharmacist-to-pharmacist electronic transfer pathway if Massachusetts law and all federal conditions are satisfied. | key 일치; `FED-EPCS-TRANSFER`, `FED-CS-SCHEDULES`의 current trigger·deadline·scope 확인 |
| `MA-Q-0020` | `KEEP` | `YES` | E: Apply the contiguous-state Schedule II narcotic pathway and its five-day and verification conditions. | key 일치; `MA-OUTSTATE-CII-NARCOTIC`, `FED-CS-SCHEDULES`의 current trigger·deadline·scope 확인 |
| `MA-Q-0021` | `KEEP` | `YES` | A: Treat it as a patient-requested Schedule II partial fill and dispense any lawful remainder within the applicable 30-day window. | key 일치; `FED-CII-PARTIAL-PATIENT`, `FED-CS-SCHEDULES`의 current trigger·deadline·scope 확인 |
| `MA-Q-0022` | `KEEP` | `YES` | B: The Schedule II prescription is invalid because more than 30 days have elapsed since issue. | key 일치; `MA-CII-VALIDITY-30D`, `FED-CS-SCHEDULES`의 current trigger·deadline·scope 확인 |
| `MA-Q-0023` | `MINOR_EDIT` | `YES` | C: Dispense no more than the amount necessary for the emergency period and follow the emergency Schedule II documentation pathway. | key C의 quantity 결론은 맞지만 explanation이 emergency oral Schedule II의 material safeguard인 7-day follow-up prescription deadline을 명시하지 않는다. 'documentation pathway'라는 포괄 문구만으로는 current 21 CFR 1306.11(d)를 안전하게 암기하기 어렵다. |
| `MA-Q-0024` | `MINOR_EDIT` | `YES` | D: The Schedule III opioid-use-disorder treatment pathway may allow up to a 90-day single fill if no other restriction controls. | key D와 Schedule III/OUD quantity rule은 맞다. 다만 related_facts가 discontinued brand인 Subutex를 current generic buprenorphine의 현행 brand처럼 괄호에 제시한다. 현재 DailyMed에는 generic buprenorphine sublingual tablets가 유통되고 Subutex NDA product는 discontinued listing이다. |
| `MA-Q-0025` | `KEEP` | `YES` | E: Treat covered Schedule III dispensing as MassPAT-reportable under the current dispenser standard. | key 일치; `MA-PMP-REPORTING`, `FED-CS-SCHEDULES`의 current trigger·deadline·scope 확인 |
| `MA-Q-0026` | `KEEP` | `YES` | A: Require renewed prescriber authorization because the federal five-refill limit has been reached. | key 일치; `FED-CIII-V-REFILL`, `FED-CS-SCHEDULES`의 current trigger·deadline·scope 확인 |
| `MA-Q-0027` | `KEEP` | `YES` | B: The out-of-state Schedule IV prescription may be filled within 30 days after required verification. | key 일치; `MA-RX-OUTSTATE-III-VI`, `FED-CS-SCHEDULES`의 current trigger·deadline·scope 확인 |
| `MA-Q-0028` | `KEEP` | `YES` | C: Federal law limits Schedule IV prescriptions to five refills within six months, despite the prescriber's notation. | key 일치; `FED-CIII-V-REFILL`, `FED-CS-SCHEDULES`의 current trigger·deadline·scope 확인 |
| `MA-Q-0029` | `KEEP` | `YES` | D: The prescription may not be refilled more than six months after issue. | key 일치; `FED-CIII-V-REFILL`, `FED-CS-SCHEDULES`의 current trigger·deadline·scope 확인 |
| `MA-Q-0030` | `KEEP` | `YES` | E: Do not transfer it a second time under the federal one-time electronic controlled-prescription rule. | key 일치; `FED-EPCS-TRANSFER`, `FED-CS-SCHEDULES`의 current trigger·deadline·scope 확인 |
| `MA-Q-0031` | `KEEP` | `YES` | A: Report the Schedule IV dispensing to MassPAT under the current submission standard. | key 일치; `MA-PMP-REPORTING`, `FED-CS-SCHEDULES`의 current trigger·deadline·scope 확인 |
| `MA-Q-0032` | `KEEP` | `YES` | B: The five-refill maximum is exhausted even though the six-month period has not ended. | key 일치; `FED-CIII-V-REFILL`, `FED-CS-SCHEDULES`의 current trigger·deadline·scope 확인 |
| `MA-Q-0033` | `KEEP` | `YES` | C: Decline the refill because the prescription is now more than six months past its issue date. | key 일치; `FED-CIII-V-REFILL`, `FED-CS-SCHEDULES`의 current trigger·deadline·scope 확인 |
| `MA-Q-0034` | `KEEP` | `YES` | D: Do not use the out-of-state Schedule IV pathway because its 30-day issue window has elapsed. | key 일치; `MA-RX-OUTSTATE-III-VI`, `FED-CS-SCHEDULES`의 current trigger·deadline·scope 확인 |
| `MA-Q-0035` | `KEEP` | `YES` | E: One additional refill may be lawful because neither the five-refill cap nor six-month clock is exhausted. | key 일치; `FED-CIII-V-REFILL`, `FED-CS-SCHEDULES`의 current trigger·deadline·scope 확인 |
| `MA-Q-0036` | `KEEP` | `YES` | A: Confirm it has not been transferred before, remains electronic and unaltered, and state law permits the transfer. | key 일치; `FED-EPCS-TRANSFER`, `FED-CS-SCHEDULES`의 current trigger·deadline·scope 확인 |
| `MA-Q-0037` | `KEEP` | `YES` | B: Report it because Schedule IV status, not benzodiazepine class alone, brings covered dispensing into MassPAT. | key 일치; `MA-PMP-REPORTING`, `FED-CS-SCHEDULES`의 current trigger·deadline·scope 확인 |
| `MA-Q-0038` | `KEEP` | `YES` | C: Check both the five-refill maximum and six-month issue-date window; neither is yet exhausted on these facts. | key 일치; `FED-CIII-V-REFILL`, `FED-CS-SCHEDULES`의 current trigger·deadline·scope 확인 |
| `MA-Q-0039` | `KEEP` | `YES` | D: The six-month issue-date limit prevents another Schedule IV refill. | key 일치; `FED-CIII-V-REFILL`, `FED-CS-SCHEDULES`의 current trigger·deadline·scope 확인 |
| `MA-Q-0040` | `KEEP` | `YES` | E: Resolve the Massachusetts initial-opiate seven-day limit before dispensing the requested quantity. | key 일치; `MA-OPIOID-SEVEN-DAY`, `FED-CS-SCHEDULES`의 current trigger·deadline·scope 확인 |
| `MA-Q-0041` | `KEEP` | `YES` | A: On this record, a qualifying non-opioid Schedule III prescription may use the statutory 90-day single-fill pathway for testosterone cypionate.; B: For this scenario, covered dispensing is reportable to MassPAT for testosterone cypionate.; C: Under these facts, federal Schedule III refill limits remain a separate check when refills are authorized for testosterone cypionate. | key 일치; `MA-CS-QUANTITY-II-III`, `MA-PMP-REPORTING`의 current trigger·deadline·scope 확인 |
| `MA-Q-0042` | `KEEP` | `YES` | A: A fifth refill may remain inside the federal numerical limit for phentermine.; B: Under these facts, covered Schedule IV dispensing is MassPAT-reportable for phentermine. | key 일치; `FED-CIII-V-REFILL`, `MA-PMP-REPORTING`의 current trigger·deadline·scope 확인 |
| `MA-Q-0043` | `MAJOR_REWRITE` | `PARTIALLY` | C, D | key가 B를 포함하지만, M.G.L. c. 94C, § 23은 non-opioid Schedule III prescription을 최대 90-day supply로 fill할 수 있다고 허용할 뿐, 모든 phendimetrazine prescription에서 그 pathway를 'required to be considered'한다고 규정하지 않는다. option B는 permission을 별도 affirmative duty로 바꾸므로 official text로 지지되지 않고 SATA set가 ambiguous하다. |
| `MA-Q-0044` | `KEEP` | `YES` | C: In this setting, schedule IV refill timing and count limits apply for modafinil.; D: At this stage, covered dispensing must be reported to MassPAT for modafinil. | key 일치; `FED-CIII-V-REFILL`, `MA-PMP-REPORTING`의 current trigger·deadline·scope 확인 |
| `MA-Q-0045` | `KEEP` | `YES` | C: At this stage, schedule III refill limits apply if refills are authorized for ketamine.; D: Given the described event, covered outpatient dispensing is MassPAT-reportable for ketamine.; E: On this record, ketamine's anesthetic indication does not remove its federal or Massachusetts Schedule III status. | key 일치; `FED-CIII-V-REFILL`, `MA-PMP-REPORTING`의 current trigger·deadline·scope 확인 |
| `MA-Q-0046` | `KEEP` | `YES` | A: Given the described event, the federal six-month issue-date clock remains relevant for perampanel.; E: On this record, covered Schedule III dispensing is reported to MassPAT for perampanel. | key 일치; `FED-CIII-V-REFILL`, `MA-PMP-REPORTING`의 current trigger·deadline·scope 확인 |
| `MA-Q-0047` | `KEEP` | `YES` | A: On this record, current product-specific REMS requirements must be satisfied for sodium oxybate.; B: For this scenario, federal Schedule III refill limits remain independently applicable for sodium oxybate.; C: Under these facts, xyrem is Schedule III when it is an FDA-approved sodium oxybate product under the federal scheduling exception.; D: In this setting, rEMS compliance does not displace ordinary controlled-substance record duties for sodium oxybate. | key 일치; `FED-REMS`, `FED-CIII-V-REFILL`의 current trigger·deadline·scope 확인 |
| `MA-Q-0048` | `KEEP` | `YES` | A: For this scenario, schedule III refill limits apply to the prescription for dronabinol.; D: Under these facts, covered dispensing is MassPAT-reportable for dronabinol.; E: In this setting, the federal six-month issue-date limit applies independently of the number of refills written for dronabinol. | key 일치; `FED-CIII-V-REFILL`, `MA-PMP-REPORTING`의 current trigger·deadline·scope 확인 |
| `MA-Q-0049` | `KEEP` | `YES` | A: Under these facts, a Schedule II prescription for Syndros may not be refilled for dronabinol oral solution.; B: In this setting, the Massachusetts 30-day Schedule II validity period applies for dronabinol oral solution.; E: At this stage, syndros is Schedule II even though dronabinol capsules marketed as Marinol are Schedule III for dronabinol oral solution. | key 일치; `FED-CII-NO-REFILL`, `MA-CII-VALIDITY-30D`의 current trigger·deadline·scope 확인 |
| `MA-Q-0050` | `KEEP` | `YES` | B: In this setting, the Massachusetts Schedule V five-refill and six-month limits apply for diphenoxylate and atropine.; C: At this stage, covered Schedule V dispensing is MassPAT-reportable for diphenoxylate and atropine. | key 일치; `MA-RX-CV-REFILL`, `MA-PMP-REPORTING`의 current trigger·deadline·scope 확인 |

## Authority record

아래 official sources를 2026-08-13에 확인했다. 각 item의 exact source set은 machine-readable audit의 `authorities`에 보존했다.

- [Current FDA labeling for alprazolam](https://dailymed.nlm.nih.gov/dailymed/search.cfm?query=alprazolam) — `Current DailyMed labeling: indication and DEA schedule for alprazolam`
- [Current FDA labeling for amphetamine-dextroamphetamine](https://dailymed.nlm.nih.gov/dailymed/search.cfm?query=amphetamine+dextroamphetamine) — `Current DailyMed labeling: indication and DEA schedule for amphetamine-dextroamphetamine`
- [Current FDA labeling for buprenorphine](https://dailymed.nlm.nih.gov/dailymed/search.cfm?query=buprenorphine) — `Current DailyMed labeling: indication and DEA schedule for buprenorphine`
- [Current FDA labeling for buprenorphine-er](https://dailymed.nlm.nih.gov/dailymed/search.cfm?query=buprenorphine+er) — `Current DailyMed labeling: indication and DEA schedule for buprenorphine-er`
- [Current FDA labeling for chlordiazepoxide](https://dailymed.nlm.nih.gov/dailymed/search.cfm?query=chlordiazepoxide) — `Current DailyMed labeling: indication and DEA schedule for chlordiazepoxide`
- [Current FDA labeling for clonazepam](https://dailymed.nlm.nih.gov/dailymed/search.cfm?query=clonazepam) — `Current DailyMed labeling: indication and DEA schedule for clonazepam`
- [Current FDA labeling for daridorexant](https://dailymed.nlm.nih.gov/dailymed/search.cfm?query=daridorexant) — `Current DailyMed labeling: indication and DEA schedule for daridorexant`
- [Current FDA labeling for dexmethylphenidate](https://dailymed.nlm.nih.gov/dailymed/search.cfm?query=dexmethylphenidate) — `Current DailyMed labeling: indication and DEA schedule for dexmethylphenidate`
- [Current FDA labeling for dextroamphetamine](https://dailymed.nlm.nih.gov/dailymed/search.cfm?query=dextroamphetamine) — `Current DailyMed labeling: indication and DEA schedule for dextroamphetamine`
- [Current FDA labeling for diazepam](https://dailymed.nlm.nih.gov/dailymed/search.cfm?query=diazepam) — `Current DailyMed labeling: indication and DEA schedule for diazepam`
- [Current FDA labeling for diphenoxylate-atropine](https://dailymed.nlm.nih.gov/dailymed/search.cfm?query=diphenoxylate+atropine) — `Current DailyMed labeling: indication and DEA schedule for diphenoxylate-atropine`
- [Current FDA labeling for dronabinol](https://dailymed.nlm.nih.gov/dailymed/search.cfm?query=dronabinol) — `Current DailyMed labeling: indication and DEA schedule for dronabinol`
- [Current FDA labeling for dronabinol-solution](https://dailymed.nlm.nih.gov/dailymed/search.cfm?query=dronabinol+solution) — `Current DailyMed labeling: indication and DEA schedule for dronabinol-solution`
- [Current FDA labeling for eszopiclone](https://dailymed.nlm.nih.gov/dailymed/search.cfm?query=eszopiclone) — `Current DailyMed labeling: indication and DEA schedule for eszopiclone`
- [Current FDA labeling for fentanyl](https://dailymed.nlm.nih.gov/dailymed/search.cfm?query=fentanyl) — `Current DailyMed labeling: indication and DEA schedule for fentanyl`
- [Current FDA labeling for hydrocodone-acetaminophen](https://dailymed.nlm.nih.gov/dailymed/search.cfm?query=hydrocodone+acetaminophen) — `Current DailyMed labeling: indication and DEA schedule for hydrocodone-acetaminophen`
- [Current FDA labeling for hydromorphone](https://dailymed.nlm.nih.gov/dailymed/search.cfm?query=hydromorphone) — `Current DailyMed labeling: indication and DEA schedule for hydromorphone`
- [Current FDA labeling for ketamine](https://dailymed.nlm.nih.gov/dailymed/search.cfm?query=ketamine) — `Current DailyMed labeling: indication and DEA schedule for ketamine`
- [Current FDA labeling for lemborexant](https://dailymed.nlm.nih.gov/dailymed/search.cfm?query=lemborexant) — `Current DailyMed labeling: indication and DEA schedule for lemborexant`
- [Current FDA labeling for lisdexamfetamine](https://dailymed.nlm.nih.gov/dailymed/search.cfm?query=lisdexamfetamine) — `Current DailyMed labeling: indication and DEA schedule for lisdexamfetamine`
- [Current FDA labeling for lorazepam](https://dailymed.nlm.nih.gov/dailymed/search.cfm?query=lorazepam) — `Current DailyMed labeling: indication and DEA schedule for lorazepam`
- [Current FDA labeling for meperidine](https://dailymed.nlm.nih.gov/dailymed/search.cfm?query=meperidine) — `Current DailyMed labeling: indication and DEA schedule for meperidine`
- [Current FDA labeling for methadone](https://dailymed.nlm.nih.gov/dailymed/search.cfm?query=methadone) — `Current DailyMed labeling: indication and DEA schedule for methadone`
- [Current FDA labeling for midazolam](https://dailymed.nlm.nih.gov/dailymed/search.cfm?query=midazolam) — `Current DailyMed labeling: indication and DEA schedule for midazolam`
- [Current FDA labeling for modafinil](https://dailymed.nlm.nih.gov/dailymed/search.cfm?query=modafinil) — `Current DailyMed labeling: indication and DEA schedule for modafinil`
- [Current FDA labeling for morphine](https://dailymed.nlm.nih.gov/dailymed/search.cfm?query=morphine) — `Current DailyMed labeling: indication and DEA schedule for morphine`
- [Current FDA labeling for oxycodone](https://dailymed.nlm.nih.gov/dailymed/search.cfm?query=oxycodone) — `Current DailyMed labeling: indication and DEA schedule for oxycodone`
- [Current FDA labeling for oxymorphone](https://dailymed.nlm.nih.gov/dailymed/search.cfm?query=oxymorphone) — `Current DailyMed labeling: indication and DEA schedule for oxymorphone`
- [Current FDA labeling for perampanel](https://dailymed.nlm.nih.gov/dailymed/search.cfm?query=perampanel) — `Current DailyMed labeling: indication and DEA schedule for perampanel`
- [Current FDA labeling for phendimetrazine](https://dailymed.nlm.nih.gov/dailymed/search.cfm?query=phendimetrazine) — `Current DailyMed labeling: indication and DEA schedule for phendimetrazine`
- [Current FDA labeling for phentermine](https://dailymed.nlm.nih.gov/dailymed/search.cfm?query=phentermine) — `Current DailyMed labeling: indication and DEA schedule for phentermine`
- [Current FDA labeling for sodium-oxybate](https://dailymed.nlm.nih.gov/dailymed/search.cfm?query=sodium+oxybate) — `Current DailyMed labeling: indication and DEA schedule for sodium-oxybate`
- [Current FDA labeling for suvorexant](https://dailymed.nlm.nih.gov/dailymed/search.cfm?query=suvorexant) — `Current DailyMed labeling: indication and DEA schedule for suvorexant`
- [Current FDA labeling for tapentadol](https://dailymed.nlm.nih.gov/dailymed/search.cfm?query=tapentadol) — `Current DailyMed labeling: indication and DEA schedule for tapentadol`
- [Current FDA labeling for temazepam](https://dailymed.nlm.nih.gov/dailymed/search.cfm?query=temazepam) — `Current DailyMed labeling: indication and DEA schedule for temazepam`
- [Current FDA labeling for testosterone-cypionate](https://dailymed.nlm.nih.gov/dailymed/search.cfm?query=testosterone+cypionate) — `Current DailyMed labeling: indication and DEA schedule for testosterone-cypionate`
- [Current FDA labeling for tramadol](https://dailymed.nlm.nih.gov/dailymed/search.cfm?query=tramadol) — `Current DailyMed labeling: indication and DEA schedule for tramadol`
- [Current FDA labeling for triazolam](https://dailymed.nlm.nih.gov/dailymed/search.cfm?query=triazolam) — `Current DailyMed labeling: indication and DEA schedule for triazolam`
- [Current FDA labeling for zaleplon](https://dailymed.nlm.nih.gov/dailymed/search.cfm?query=zaleplon) — `Current DailyMed labeling: indication and DEA schedule for zaleplon`
- [Current FDA labeling for zolpidem](https://dailymed.nlm.nih.gov/dailymed/search.cfm?query=zolpidem) — `Current DailyMed labeling: indication and DEA schedule for zolpidem`
- [Emergency oral Schedule II prescription](https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.11) — `21 CFR 1306.11(d)`
- [FDA Orange Book discontinued product listing](https://www.accessdata.fda.gov/scripts/cder/ob/index.cfm) — `NDA 020732 SUBUTEX — discontinued product; generic buprenorphine products remain approved`
- [Federal controlled-substance schedules](https://www.ecfr.gov/current/title-21/chapter-II/part-1308) — `21 CFR 1308.12-1308.15`
- [Initial and minor outpatient opiate quantity limit](https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section19D) — `M.G.L. c. 94C, § 19D`
- [Massachusetts PMP pharmacy reporting](https://www.mass.gov/info-details/pharmacy-reporting-and-data-submission) — `105 CMR 700.012; PMP Data Submission Dispenser Guide v5.2`
- [Massachusetts Schedule II prescription validity](https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section23) — `M.G.L. c. 94C, § 23`
- [Massachusetts Schedule V refill limits](https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download) — `247 CMR 9.04(13)`
- [One-time transfer of electronic controlled-substance prescriptions](https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.08) — `21 CFR 1306.08(e)-(f)`
- [Out-of-state Schedule II narcotic prescriptions](https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section18) — `M.G.L. c. 94C, § 18(c)`
- [Out-of-state Schedule III through VI prescriptions](https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section18) — `M.G.L. c. 94C, § 18(c)`
- [Out-of-state nonnarcotic Schedule II prescriptions](https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section18) — `M.G.L. c. 94C, § 18(c)`
- [Patient- or prescriber-requested partial filling of Schedule II prescriptions](https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.13) — `21 CFR 1306.13(b)`
- [Schedule II and III quantity limits](https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section23) — `M.G.L. c. 94C, § 23(d)`
- [Schedule II patient-requested partial-fill remainder](https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section18) — `M.G.L. c. 94C, § 18(d¾)`
- [Schedule II refills](https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.12) — `21 CFR 1306.12(a)`
- [Schedule III and IV refill limits](https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.22) — `21 CFR 1306.22(a)`
- [XYWAV and XYREM REMS](https://www.accessdata.fda.gov/drugsatfda_docs/label/2025/021196Orig1s047%2C212690Orig1s017lbl.pdf) — `Most Recent REMS Update 05/2025; current XYREM labeling revised 07/2025`

## 독립성 및 hash 보존

각 item은 key를 보기 전에 stem·choices만으로 먼저 풀었고, 그 뒤 frozen key와 비교했다. `question_ids`와 `question_hashes`는 supplied `Batch A` input에서 byte-for-byte value copy했고 canonical question/rule/drug files는 수정하지 않았다.
