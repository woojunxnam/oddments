from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path

from qa_common import DATA, ROOT, dependency_snapshot, load_records, question_audit_hash, write_json

POST_BATCH2_SHA = "beeb96d71768b9fb275bdb0005d9cd012e0d1328"
NABP_URL = "https://nabp.pharmacy/programs/examinations/mpje/competency-statements/"
OUT_DIR = ROOT / "audits" / "coverage" / "2026-08-17"
TARGET = {1: 26, 2: 40, 3: 29, 4: 25}

# A PASS here means direct semantic coverage by at least one current RELEASED question.
# FAIL rows either have no direct question or only a direct legacy question that is not release-usable.
ROWS = {
    "1.1a": (1, "Qualifications/duties/limits/conditions for PICs and pharmacists", "PASS_FORMAL_MAP", ["MA-Q-0173", "MA-Q-0162"], [], "Current released items directly test a pharmacist qualification/condition to administer and a pharmacist's corresponding-responsibility duty. They are cross-area evidence and are formally mapped here rather than retagged."),
    "1.1b": (1, "Qualifications/duties/limits/conditions for non-pharmacist personnel", "PASS_DIRECT", ["MA-Q-0138", "MA-Q-0140"], [], "Technician-trainee and certified-technician ADD pathways directly test credential-dependent scope and supervision limits."),
    "1.2a": (1, "Personnel licensure/registration/certification, examinations, internships, competency, renewal", "PASS_DIRECT", ["MA-Q-0138", "MA-Q-0140"], ["MA-Q-0077", "MA-Q-0078", "MA-Q-0079", "MA-Q-0080"], "Released Batch 2 technician-credential questions provide direct current evidence. Legacy intern/CE items remain useful salvage targets for breadth and Area-1 capacity."),
    "1.2b": (1, "Personnel disciplinary classifications/processes", "FAIL_NO_DIRECT_QUESTION", [], [], "No canonical question directly tests classifications/processes of discipline against an individual pharmacist/technician. Keyword hits such as a revoked CSOS certificate are not personnel discipline."),
    "1.2c": (1, "Impairment/inability-to-practice reporting or participation programs", "FAIL_NO_DIRECT_QUESTION", [], [], "No canonical question directly tests reporting/participation in the current impairment/recovery framework (URAMP)."),

    "2.1a": (2, "Drug-use requirements/limitations/restrictions", "PASS_DIRECT", ["MA-Q-0141", "MA-Q-0194"], [], "EPT diagnosis limits and the methadone OUD pathway directly test use-dependent legal restrictions."),
    "2.1b": (2, "Practitioner authority/scope/registration to prescribe/dispense/administer", "PASS_DIRECT", ["MA-Q-0167", "MA-Q-0168"], [], "MCSR/DEA authority matrix and Schedule-VI-without-DEA scenario directly test registration-dependent practitioner authority."),
    "2.1c": (2, "Issuing non-controlled prescriptions/orders", "PASS_DIRECT", ["MA-Q-0142", "MA-Q-0178"], [], "EPT prescription identity/construction directly tests issuance requirements for non-controlled therapy."),
    "2.1d": (2, "Issuing controlled prescriptions/orders", "PASS_DIRECT", ["MA-Q-0158", "MA-Q-0192"], [], "Multiple Schedule-II prescription scenarios directly test controlled-prescription issuance conditions."),
    "2.1e": (2, "Practitioner refill-authorization limits", "FAIL_NOT_RELEASE_USABLE", [], ["MA-Q-0028", "MA-Q-0032"], "Direct legacy questions test the federal refill-count ceiling, but they are AUDIT_PENDING and therefore cannot satisfy the release-usable gate."),
    "2.2": (2, "Pharmacist/non-pharmacist drug-administration conditions", "PASS_DIRECT", ["MA-Q-0145", "MA-Q-0172"], [], "Current administration-category and applied eligibility matrix questions directly test administration conditions."),
    "2.3a": (2, "Counseling or offer-to-counsel requirements", "PASS_FORMAL_MAP", ["MA-Q-0092"], ["MA-Q-0086"], "Q0092 directly distinguishes the Massachusetts counseling duty from a federal Medication Guide duty. Q0086 is a stronger legacy counseling-workflow item but is not release-usable."),
    "2.3b": (2, "Documentation of counseling/offer", "FAIL_NO_DIRECT_QUESTION", [], [], "No canonical question directly adjudicates whether/how counseling or the offer/refusal must be documented. Generic documentation references do not qualify."),
    "2.4": (2, "Returning or reusing drugs", "FAIL_NOT_RELEASE_USABLE", [], ["MA-Q-0088"], "Q0088 directly tests return/quarantine/no-reuse but remains AUDIT_PENDING; Q0098 is about naloxone product status and is not a return/reuse substitute."),
    "2.5a": (2, "Public-health quality/safety regulations and agencies", "PASS_DIRECT", ["MA-Q-0097", "MA-Q-0141"], [], "Naloxone third-party access and EPT public-health pathways provide distinct direct scenarios."),
    "2.5b": (2, "Patient/health-record confidentiality", "PASS_DIRECT", ["MA-Q-0147"], [], "The MH/SUD administration workflow directly tests that ordinary privacy duties remain applicable; headline 2.5 has multiple other families through 2.5a."),

    "3.1": (3, "Legitimate medical purpose/restrictions and corresponding responsibility", "PASS_DIRECT", ["MA-Q-0162", "MA-Q-0164"], [], "Generic red-flag/corresponding-responsibility and methadone-indication conflict scenarios provide distinct direct coverage."),
    "3.2": (3, "Prescription/order transfer by authorized personnel", "PASS_DIRECT", ["MA-Q-0120"], ["MA-Q-0030", "MA-Q-0036"], "Q0120 is direct and release-usable, but this headline currently has only one released family; legacy transfer items are remediation targets for required scenario diversity."),
    "3.3a": (3, "Prospective drug utilization review", "FAIL_NOT_RELEASE_USABLE", [], ["MA-Q-0085"], "Q0085 directly tests prospective DUR but is AUDIT_PENDING and is currently tagged Area 2 rather than NABP Area 3."),
    "3.3b": (3, "PMP reporting/access", "PASS_DIRECT", ["MA-Q-0198", "MA-Q-0199"], [], "MassPAT reporting matrix and naloxone/PMP profile scenarios directly test PMP consequences."),
    "3.4": (3, "Exceptions to dispensing/refilling", "PASS_DIRECT", ["MA-Q-0155", "MA-Q-0160"], [], "LTCF fax and LTCF/terminal partial-fill exceptions provide distinct direct coverage."),
    "3.5": (3, "Labeling of dispensed drugs", "PASS_DIRECT", ["MA-Q-0117", "MA-Q-0143"], [], "Compounded-product and EPT-label scenarios directly test dispensed-drug labeling requirements."),
    "3.6": (3, "Packaging of dispensed drugs", "PASS_FORMAL_MAP", ["MA-Q-0169", "MA-Q-0202"], [], "Released compliance-packaging questions directly test packaging, though they are currently tagged Area 4; this matrix formally maps them to NABP 3.6."),
    "3.7": (3, "Drug-product conditions prohibiting dispensing", "PASS_DIRECT", ["MA-Q-0093", "MA-Q-0106"], [], "Storage excursion and REMS-gate scenarios directly test product/status conditions that prohibit dispensing."),
    "3.8a": (3, "Nonprescription product dispensing/administration", "PASS_DIRECT", ["MA-Q-0098", "MA-Q-0107"], [], "OTC naloxone status and restricted pseudoephedrine sale pathways directly test nonprescription dispensing."),
    "3.8b": (3, "Nonprescription drug/device labeling", "PASS_FORMAL_MAP", ["MA-Q-0098"], [], "Q0098 directly contrasts an FDA-labeled OTC Drug Facts package with a prescription-labeled naloxone package; it is formally cross-mapped from its current Area-2 tag."),
    "3.8c": (3, "Nonprescription/behind-counter packaging or repackaging", "PASS_DIRECT", ["MA-Q-0107"], [], "The single-sales-package <=60 mg pseudoephedrine exception makes packaging itself outcome-determinative; repackaging remains thin but the atomic packaging concept is directly tested."),
    "3.8d": (3, "Dispensing-restricted nonprescription products", "PASS_DIRECT", ["MA-Q-0107", "MA-Q-0108"], [], "Pseudoephedrine purchaser-ID/logbook exception and seller self-certification directly test restricted nonprescription sales."),

    "4.1a": (4, "Ordering/acquisition and records", "PASS_DIRECT", ["MA-Q-0125", "MA-Q-0128"], [], "Form-222 defect and CSOS certificate validation directly test controlled acquisition/order requirements."),
    "4.1b": (4, "Distribution and records", "PASS_DIRECT", ["MA-Q-0130", "MA-Q-0132"], [], "Reverse-distribution/destruction and ADD ownership/distribution accountability provide direct distribution-pathway coverage."),
    "4.2a": (4, "Non-dispensing pharmacy/practice-setting operations records", "PASS_DIRECT", ["MA-Q-0134"], [], "ADD required-record systems directly test non-dispensing operational records; headline 4.2 has multiple other families."),
    "4.2b": (4, "Possession/storage/handling of non-hazardous drugs", "PASS_DIRECT", ["MA-Q-0150", "MA-Q-0152"], [], "LTC emergency-kit and hospice ADD safeguards directly test storage/security/possession controls."),
    "4.2c": (4, "Hazardous-drug training/possession/handling/storage/disposal", "FAIL_NO_DIRECT_QUESTION", [], [], "No canonical question directly tests hazardous-drug training, possession, handling, storage, or disposal. Generic controlled-substance security is not equivalent."),
    "4.2d": (4, "Non-pharmacist personnel access to drugs", "PASS_DIRECT", ["MA-Q-0138", "MA-Q-0140"], [], "Credential-dependent technician ADD access/stocking pathways directly test non-pharmacist drug access."),
    "4.2e": (4, "Controlled-substance inventories", "FAIL_NOT_RELEASE_USABLE", [], ["MA-Q-0059", "MA-Q-0060"], "Direct initial/biennial controlled-inventory questions exist but remain AUDIT_PENDING; ADD accountability is not a substitute for the required registrant inventory event."),
    "4.3": (4, "Delivery of drugs", "FAIL_NO_DIRECT_QUESTION", [], [], "Q0209 merely assumes later pharmacy delivery as part of a hospice bridge; it does not test delivery/shipping requirements. No direct release-usable delivery item exists."),
    "4.4": (4, "Permitted/mandated product selection", "FAIL_NOT_RELEASE_USABLE", [], ["MA-Q-0087"], "Q0087 directly tests Massachusetts interchangeable-product selection but remains AUDIT_PENDING and is currently tagged Area 3; Q0209 is not a substitution/product-selection question."),
    "4.5a": (4, "Sterile compounding", "FAIL_NO_DIRECT_QUESTION", [], [], "Q0117 tests compounded-product labeling, not substantive sterile-compounding practice. No direct substantive sterile-compounding item exists."),
    "4.5b": (4, "Nonsterile compounding", "FAIL_NO_DIRECT_QUESTION", [], [], "No direct substantive nonsterile-compounding practice item exists."),
    "4.5c": (4, "Hazardous compounding", "FAIL_NO_DIRECT_QUESTION", [], [], "No direct hazardous-compounding practice item exists."),
    "4.5d": (4, "Non-hazardous compounding", "FAIL_NO_DIRECT_QUESTION", [], [], "No direct non-hazardous compounding practice item exists."),
    "4.6": (4, "Centralized prescription processing / central fill", "FAIL_NO_DIRECT_QUESTION", [], [], "No canonical question directly tests the Board's shared-pharmacy-service/central-fill pathway."),
    "4.7a": (4, "Practice-setting/business registration/licensure/certification/permitting", "PASS_DIRECT", ["MA-Q-0131"], [], "Q0131 directly requires licensing-body approval before ADD use/placement at a licensed health-care facility."),
    "4.7b": (4, "Practice-setting license/registration renewal or reinstatement", "FAIL_NO_DIRECT_QUESTION", [], [], "No canonical question directly tests pharmacy/practice-setting renewal or reinstatement; personal pharmacist renewal is a different competency."),
    "4.7c": (4, "Practice-setting inspection requirements", "FAIL_NO_DIRECT_QUESTION", [], [], "The legacy phrase 'available for inspection' in Q0062 concerns record availability, not requirements for inspection of a licensed practice setting."),
    "4.7d": (4, "Practice-setting disciplinary actions", "FAIL_NO_DIRECT_QUESTION", [], [], "No canonical question directly tests classifications/processes of disciplinary action against a pharmacy or other practice-setting license."),
}

OFFICIAL_REMEDIATION_SOURCES = {
    "1.2b": ["https://www.mass.gov/regulations/247-CMR-1000-disciplinary-proceedings"],
    "1.2c": ["https://www.mass.gov/orgs/unified-recovery-and-monitoring-program"],
    "2.1e": ["https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.22"],
    "2.3b": ["https://www.mass.gov/regulations/247-CMR-900-professional-practice-standards"],
    "2.4": ["https://www.mass.gov/regulations/247-CMR-900-professional-practice-standards"],
    "3.3a": ["https://www.mass.gov/regulations/247-CMR-900-professional-practice-standards"],
    "4.2c": ["https://www.mass.gov/lists/laws-and-regulations-of-the-board-of-registration-in-pharmacy"],
    "4.2e": ["https://www.ecfr.gov/current/title-21/chapter-II/part-1304/section-1304.11"],
    "4.3": ["https://www.mass.gov/lists/pharmacy-practice-resources"],
    "4.4": ["https://www.mass.gov/lists/laws-and-regulations-of-the-board-of-registration-in-pharmacy"],
    "4.5a": ["https://www.mass.gov/lists/mass-general-laws-c112-ssss-23a-53", "https://www.mass.gov/lists/pharmacy-practice-resources"],
    "4.5b": ["https://www.mass.gov/lists/mass-general-laws-c112-ssss-23a-53", "https://www.mass.gov/lists/pharmacy-practice-resources"],
    "4.5c": ["https://www.mass.gov/lists/mass-general-laws-c112-ssss-23a-53", "https://www.mass.gov/lists/pharmacy-practice-resources"],
    "4.5d": ["https://www.mass.gov/lists/mass-general-laws-c112-ssss-23a-53", "https://www.mass.gov/lists/pharmacy-practice-resources"],
    "4.6": ["https://www.mass.gov/lists/pharmacy-practice-resources"],
    "4.7b": ["https://www.mass.gov/regulations/247-CMR-600-licensure-of-pharmacies", "https://www.mass.gov/lists/pharmacy-practice-resources"],
    "4.7c": ["https://www.mass.gov/lists/pharmacy-practice-resources", "https://www.mass.gov/lists/mass-general-laws-c112-ssss-23a-53"],
    "4.7d": ["https://www.mass.gov/regulations/247-CMR-1000-disciplinary-proceedings"],
}


def evidence(qid: str, questions: dict, rules: dict, drugs: dict) -> dict:
    q = questions[qid]
    return {
        "question_id": qid,
        "family_id": q["family_id"],
        "current_area": q["area"],
        "topic": q["topic"],
        "subtopic": q["subtopic"],
        "question_hash": question_audit_hash(q),
        "verification_status": q["verification_status"],
        "lifecycle_status": q["lifecycle_status"],
        "independent_audit_status": q["independent_audit_status"],
        "duplicate_review_status": q["duplicate_review_status"],
        "final_decision": (q.get("final_adjudication") or {}).get("decision"),
        "rule_dependencies": {
            rid: {
                **dependency_snapshot(rules[rid]),
                "status": rules[rid].get("status"),
                "verification_status": rules[rid].get("verification_status"),
                "authority": rules[rid].get("authority", []),
            }
            for rid in q.get("rule_ids", []) if rid in rules
        },
        "drug_dependencies": {
            did: dependency_snapshot(drugs[did]) for did in q.get("drug_ids", []) if did in drugs
        },
    }


def main() -> int:
    if len(ROWS) != 46:
        raise RuntimeError(f"expected 46 atomic rows, found {len(ROWS)}")
    questions = {record["question_id"]: record for _, record in load_records(DATA / "questions")}
    rules = {record["rule_id"]: record for _, record in load_records(DATA / "rules")}
    drugs = {record["drug_id"]: record for _, record in load_records(DATA / "drugs")}

    matrix_rows = []
    headline_families: dict[str, set[str]] = defaultdict(set)
    taxonomy_maps = []
    failed_atoms = []

    for atomic_id, (area, label, status, selected, salvage, rationale) in ROWS.items():
        selected_evidence = [evidence(qid, questions, rules, drugs) for qid in selected]
        salvage_evidence = [evidence(qid, questions, rules, drugs) for qid in salvage]
        for item in selected_evidence:
            if item["verification_status"] != "RELEASED" or item["lifecycle_status"] != "RELEASED":
                raise RuntimeError(f"selected evidence is not release-usable: {atomic_id} {item['question_id']}")
            if item["independent_audit_status"] != "PASSED" or item["final_decision"] != "KEEP":
                raise RuntimeError(f"selected evidence lacks mature audit/adjudication: {atomic_id} {item['question_id']}")
            headline = atomic_id[:-1] if atomic_id[-1].isalpha() else atomic_id
            headline_families[headline].add(item["family_id"])
            if item["current_area"] != area:
                taxonomy_maps.append({
                    "atomic_id": atomic_id,
                    "question_id": item["question_id"],
                    "current_area": item["current_area"],
                    "mapped_nabp_area": area,
                    "basis": "formal coverage-evidence mapping; canonical question is not edited by this audit",
                })
        for item in salvage_evidence:
            if item["verification_status"] == "RELEASED" and item["lifecycle_status"] == "RELEASED":
                raise RuntimeError(f"salvage evidence unexpectedly already released: {atomic_id} {item['question_id']}")
        if status.startswith("FAIL"):
            failed_atoms.append(atomic_id)

        matrix_rows.append({
            "atomic_id": atomic_id,
            "nabp_area": area,
            "label": label,
            "semantic_status": status,
            "direct_release_usable_count": len(selected_evidence),
            "selected_release_evidence": selected_evidence,
            "legacy_salvage_candidates": salvage_evidence,
            "rationale": rationale,
            "official_remediation_sources": OFFICIAL_REMEDIATION_SOURCES.get(atomic_id, []),
        })

    # Headline diversity: default >=2 distinct families. Failed headlines stay failed regardless.
    headline_atoms: dict[str, list[str]] = defaultdict(list)
    for atomic_id in ROWS:
        headline = atomic_id[:-1] if atomic_id[-1].isalpha() else atomic_id
        headline_atoms[headline].append(atomic_id)
    diversity = []
    diversity_debt = []
    for headline in sorted(headline_atoms):
        atom_ids = headline_atoms[headline]
        atom_fail = any(ROWS[aid][2].startswith("FAIL") for aid in atom_ids)
        families = sorted(headline_families.get(headline, set()))
        if atom_fail:
            status = "FAIL_ATOMIC_COVERAGE"
        elif len(families) >= 2:
            status = "PASS_TWO_PLUS_FAMILIES"
        else:
            status = "FAIL_FAMILY_DIVERSITY"
            diversity_debt.append(headline)
        diversity.append({
            "headline": headline,
            "atomic_ids": atom_ids,
            "distinct_selected_families": families,
            "family_count": len(families),
            "status": status,
            "exception_justification": None,
        })

    canonical_area = Counter(q["area"] for q in questions.values())
    released_area = Counter(
        q["area"] for q in questions.values()
        if q.get("verification_status") == "RELEASED" and q.get("lifecycle_status") == "RELEASED"
    )
    legacy = [q for q in questions.values() if int(q["question_id"][-4:]) <= 90]
    legacy_priority = {
        str(area): [
            {
                "question_id": q["question_id"],
                "family_id": q["family_id"],
                "topic": q["topic"],
                "subtopic": q["subtopic"],
                "question_hash": question_audit_hash(q),
                "verification_status": q["verification_status"],
            }
            for q in sorted(legacy, key=lambda x: x["question_id"]) if q["area"] == area
        ]
        for area in (1, 2)
    }
    legacy_counts = {area: len(legacy_priority[str(area)]) for area in (1, 2)}
    post_full_legacy = {area: released_area[area] + legacy_counts.get(area, 0) for area in (1, 2)}
    irreducible_new = {area: max(0, TARGET[area] - post_full_legacy[area]) for area in (1, 2)}

    direct_new_atoms = [
        aid for aid in failed_atoms if ROWS[aid][2] == "FAIL_NO_DIRECT_QUESTION"
    ]
    salvage_atoms = [
        aid for aid in failed_atoms if ROWS[aid][2] == "FAIL_NOT_RELEASE_USABLE"
    ]

    matrix = {
        "gate": "PRE_BATCH3_FULL_COMPETENCY_COVERAGE_DEBT",
        "verdict": "FAIL",
        "audit_date": "2026-08-17",
        "post_batch2_source_sha": POST_BATCH2_SHA,
        "nabp_competency_source": NABP_URL,
        "nabp_profile": "MPJE competency statements applicable before 2027-03-01",
        "atomic_count": 46,
        "atomic_pass_count": 46 - len(failed_atoms),
        "atomic_fail_count": len(failed_atoms),
        "failed_atomic_ids": failed_atoms,
        "rows": matrix_rows,
        "headline_family_diversity": diversity,
        "headline_family_diversity_debt": diversity_debt,
        "formal_taxonomy_mappings": taxonomy_maps,
        "mock_capacity": {
            "required_area_counts": {str(a): TARGET[a] for a in range(1, 5)},
            "release_usable_area_counts": {str(a): released_area[a] for a in range(1, 5)},
            "release_usable_total": sum(released_area.values()),
            "deficits": {str(a): max(0, TARGET[a] - released_area[a]) for a in range(1, 5)},
            "blueprint_faithful_120_without_reuse": all(released_area[a] >= TARGET[a] for a in range(1, 5)),
        },
        "gate_fail_reasons": [
            f"{len(failed_atoms)} of 46 atomic competencies lack qualifying direct release-usable coverage",
            f"Area 1 release-usable count {released_area[1]} is below required {TARGET[1]}",
            f"Area 2 release-usable count {released_area[2]} is below required {TARGET[2]}",
            *( [f"headline family-diversity debt: {', '.join(diversity_debt)}"] if diversity_debt else [] ),
        ],
    }

    remediation = {
        "gate_source_sha": POST_BATCH2_SHA,
        "gate_verdict": "FAIL",
        "batch3": "BLOCKED",
        "locked_sequence": [
            "legacy salvage first",
            "repair/current-law update if required",
            "freeze/hash",
            "independent legal + realism audit",
            "adjudication/release governance",
            "recompute full 46-atomic matrix and mock capacity",
            "targeted new questions only for residual gaps/capacity debt",
            "same freeze/audit/adjudication/release process",
            "rerun full pre-Batch3 gate; only PASS unlocks Batch 3",
        ],
        "legacy_area_1_and_2_priority": legacy_priority,
        "legacy_priority_counts": {str(a): legacy_counts[a] for a in (1, 2)},
        "capacity_after_perfect_legacy_area_1_2_salvage": {str(a): post_full_legacy[a] for a in (1, 2)},
        "irreducible_minimum_new_questions_for_capacity": {str(a): irreducible_new[a] for a in (1, 2)},
        "failed_atoms_with_direct_legacy_salvage": salvage_atoms,
        "failed_atoms_requiring_new_direct_content": direct_new_atoms,
        "specific_semantic_salvage_targets": {
            "2.1e": ["MA-Q-0028", "MA-Q-0032"],
            "2.4": ["MA-Q-0088"],
            "3.2_diversity": ["MA-Q-0030", "MA-Q-0036"],
            "3.3a": ["MA-Q-0085"],
            "4.2e": ["MA-Q-0059", "MA-Q-0060"],
            "4.4": ["MA-Q-0087"],
        },
        "minimum_targeted_new_design_lower_bound": {
            "count": 11,
            "assumptions": [
                "all 6 legacy Area-1 and all 16 legacy Area-2 questions are successfully salvaged",
                "legacy semantic targets listed above are successfully salvaged",
                "one hazardous sterile-compounding family may directly cover 4.2c + 4.5a + 4.5c",
                "one nonsterile non-hazardous family may directly cover 4.5b + 4.5d",
                "one practice-setting reinstatement/discipline family may directly cover 4.7b + 4.7d",
                "an additional new Area-1 item and an additional new Area-2 item are still needed to meet irreducible mock capacity",
            ],
            "proposed_families": [
                "Area1 personnel disciplinary process",
                "Area1 URAMP/impairment reporting-participation",
                "Area1 additional licensure/personnel family for capacity/diversity",
                "Area2 counseling-offer documentation",
                "Area2 additional practitioner/counseling family for capacity/diversity",
                "Area4 hazardous sterile compounding + hazardous handling",
                "Area4 nonsterile non-hazardous compounding",
                "Area4 medication delivery/shipping",
                "Area4 central fill/shared pharmacy service",
                "Area4 practice-setting inspection",
                "Area4 practice-setting reinstatement + disciplinary process",
            ],
            "warning": "This is a lower bound, not an authoring quota. Every failed legacy salvage adds at least one replacement question, and realism/family-diversity review may require additional items.",
        },
    }

    report_lines = [
        "# Final Pre-Batch3 Competency Coverage-Debt Gate",
        "",
        f"- Exact post-Batch2 source SHA: `{POST_BATCH2_SHA}`",
        "- Verdict: **FAIL — Batch 3 remains blocked**",
        f"- Atomic competency result: **{46-len(failed_atoms)}/46 PASS; {len(failed_atoms)}/46 FAIL**",
        f"- Failed atoms: {', '.join(failed_atoms)}",
        "- Release-usable Area counts: " + "/".join(str(released_area[a]) for a in range(1,5)),
        "- Required 120-question Area allocation: 26/40/29/25",
        "- Capacity deficits: " + "/".join(str(max(0, TARGET[a]-released_area[a])) for a in range(1,5)),
        "",
        "## Why the gate fails",
        "",
        "The bank now contains 120 released questions, but question count alone is insufficient. Area 1 and Area 2 remain below the blueprint allocation, and 18 atomic competencies still lack a direct current-law, independently audited, release-usable question.",
        "",
        "## Failed atomic competencies",
        "",
    ]
    for aid in failed_atoms:
        row = next(item for item in matrix_rows if item["atomic_id"] == aid)
        report_lines.append(f"- **{aid} — {row['label']}**: {row['semantic_status']}. {row['rationale']}")
    report_lines += [
        "",
        "## Legacy-first consequence",
        "",
        f"Legacy Q0001–Q0090 contains exactly {legacy_counts[1]} Area-1 and {legacy_counts[2]} Area-2 questions. To minimize new authoring, all {legacy_counts[1]+legacy_counts[2]} must be attempted for salvage. Even perfect salvage raises Area 1 only to {post_full_legacy[1]} and Area 2 only to {post_full_legacy[2]}, so at least {irreducible_new[1]} new Area-1 and {irreducible_new[2]} new Area-2 questions are mathematically unavoidable.",
        "",
        "## Taxonomy / diversity debt",
        "",
        "Formal cross-area evidence mappings are recorded in the JSON matrix rather than silently rewriting canonical question areas. Headline competency 3.2 currently has only one released direct family and therefore also needs a second distinct transfer family; Q0030/Q0036 are legacy candidates.",
        "",
        "## Next locked action",
        "",
        "Create a separately named pre-Batch3 coverage-remediation tranche. Salvage legacy content first, beginning with all Area-1/Area-2 legacy questions and the specific semantic salvage targets. Do not author Batch 3. Only after legacy salvage is audited/released and the matrix is recomputed should targeted new coverage questions be authored.",
        "",
    ]

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUT_DIR / "FINAL-PRE-BATCH3-COVERAGE-MATRIX.json", matrix)
    write_json(OUT_DIR / "FINAL-PRE-BATCH3-REMEDIATION-PLAN.json", remediation)
    (OUT_DIR / "FINAL-PRE-BATCH3-COVERAGE-DEBT.md").write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    print(
        f"final coverage gate: FAIL pass={46-len(failed_atoms)}/46 fail={len(failed_atoms)}/46 "
        f"released={sum(released_area.values())} areas={dict(sorted(released_area.items()))} "
        f"legacyA1A2={legacy_counts} irreducible_new={irreducible_new} diversity_debt={diversity_debt}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
