from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "data" / "questions"

PATCHES = {
    "MA-Q-0138": [
        ("Yes; trainee status is enough when the clinic is licensed and the pharmacist provides remote direction.", "Facility prerequisites still apply to the trainee pathway."),
        ("Yes; limiting the cabinet to Schedule VI removes the location conditions for trainee stocking.", "Schedule does not replace the facility-location requirements."),
        ("No; the pathway requires an on-site pharmacy and an ADD at the same physical address listed on the facility MCSR.", "Both required location conditions are missing in the scenario."),
        ("No; trainees may work with ADD inventory only after becoming nationally certified technicians.", "Eligible trainees have a defined stocking pathway without national certification."),
        ("Yes; a personal DEA registration for the trainee would substitute for the facility-location conditions.", "A personal DEA registration does not cure the facility-location defect."),
    ],
    "MA-Q-0141": [
        ("The cited pharmacy EPT policy covers gonorrhea and chlamydia whenever the partner has not been examined.", "The cited Massachusetts pharmacy EPT policy is not a general STI pathway."),
        ("It does not fit; the cited Massachusetts pharmacy EPT policy is limited to chlamydia treatment.", "The diagnosis in the scenario is outside the policy's chlamydia scope."),
        ("It fits only when gonorrhea is treated with a federally controlled antibiotic.", "Federal controlled-substance status is not the EPT eligibility criterion."),
        ("It fits when the prescription is electronic, even though the diagnosis is gonorrhea alone.", "Prescription format does not expand the policy's diagnosis scope."),
        ("It fits after the partner gives the pharmacy identifying information, regardless of diagnosis.", "Providing identity information does not convert gonorrhea-only treatment into this EPT pathway."),
    ],
    "MA-Q-0151": [
        ("It is a limited bridge for timely palliation until the pharmacy can fill and deliver the full patient prescription.", "The acute-use supply is a bridge to the pharmacy's full patient-specific dispensing."),
        ("It is intended to reduce routine pharmacy deliveries by functioning as standing floor stock for chronic therapy.", "The pathway is not a substitute for routine chronic-medication dispensing."),
        ("It is intended primarily to hold larger reserve quantities when the hospice has frequent Schedule VI use.", "The purpose is timely acute palliation, not inventory expansion based on schedule."),
        ("It is intended mainly for resuscitation drugs used during immediately life-threatening emergencies.", "The circular addresses acute palliative needs rather than a resuscitation-only stock model."),
        ("It transfers ordinary dispensing responsibility from the pharmacy to hospice nursing staff during off-hours.", "The pharmacy remains responsible for the dispensing system and patient-specific supply."),
    ],
    "MA-Q-0162": [
        ("Dispense after confirming the DEA number because registration establishes the prescriber's responsibility for medical purpose.", "A valid registration does not remove the pharmacist's corresponding responsibility."),
        ("Resolve the red flags before dispensing; if legitimacy cannot be established, do not fill the prescription.", "Corresponding responsibility requires an independent pre-dispensing validity judgment."),
        ("Dispense the first fill, document the concerns, and investigate the red flags before the next dispensing.", "Material red flags must be addressed before the questioned dispensing."),
        ("Change the quantity or directions to a safer-looking regimen without contacting the prescriber, then dispense.", "Unilateral alteration does not establish legitimate medical purpose."),
        ("Transfer the final validity decision to a technician who reviewed the patient's profile and identification.", "The pharmacist retains the professional responsibility for the dispensing decision."),
    ],
    "MA-Q-0166": [
        ("Qualifying Schedule III-V narcotic OUD drugs can use a prescription pathway when otherwise lawful; methadone maintenance follows a different framework.", "Federal law distinguishes the qualifying Schedule III-V prescription pathway from methadone maintenance."),
        ("A Schedule III narcotic used for OUD is reclassified as Schedule II for the duration of treatment.", "Indication does not reclassify a Schedule III drug."),
        ("Schedule III narcotic OUD therapy must be dispensed through the same OTP pathway used for methadone maintenance.", "The federal framework distinguishes qualifying Schedule III-V prescribing from methadone maintenance."),
        ("The first OUD dose converts the Schedule III medication to noncontrolled status for later outpatient fills.", "Treatment does not remove the drug's federal controlled status."),
        ("The federal OUD rule gives pharmacists independent prescribing authority for qualifying Schedule III-V narcotics.", "The treatment rule does not independently create pharmacist prescriptive authority."),
    ],
    "MA-Q-0168": [
        ("The prescription is invalid because a DEA registration is required for every Massachusetts prescription drug, including Schedule VI.", "Massachusetts Schedule VI status alone does not require a federal DEA registration."),
        ("The MCSR supports Schedule VI-only activity; DEA registration is needed when the practitioner conducts federally controlled Schedule II-V activity.", "The scenario fits the state-only registration distinction for Schedule VI activity."),
        ("The MCSR is relevant only to Schedule I activity, so it does not authorize this Schedule VI prescription.", "The MCSR governs Massachusetts controlled-substance activity beyond Schedule I."),
        ("The pharmacy may place its DEA number on the prescription to cover the practitioner's missing federal registration.", "A pharmacy cannot supply prescriber registration authority by substituting its own DEA number."),
        ("Schedule VI prescribing requires neither an MCSR nor DEA registration when the drug is not federally controlled.", "Schedule VI activity still requires the appropriate Massachusetts registration."),
    ],
    "MA-Q-0180": [
        ("Alprazolam", "Alprazolam is Schedule IV, which falls within the trainee's permitted Schedule III-VI range."),
        ("Pregabalin", "Pregabalin is Schedule V, so pharmacist-verified stock is within the trainee stocking boundary."),
        ("Gabapentin", "Gabapentin is Massachusetts Schedule VI; its PMP status does not move it outside the verified-stock trainee range."),
        ("Warfarin", "Warfarin is an ordinary Massachusetts Schedule VI prescription drug and therefore fits the verified-stock range."),
        ("Methylphenidate", "Methylphenidate is Schedule II, which is outside the trainee's Schedule III-VI stocking authority."),
    ],
    "MA-Q-0186": [
        ("The hospice Schedule II narcotic exception treats this fax as the original prescription.", "Oxycodone is a Schedule II narcotic and the prescription carries the required hospice status fact."),
        ("The fax can be used as the original after oxycodone is changed to Schedule III for hospice dispensing.", "Hospice use does not reclassify oxycodone from Schedule II."),
        ("The fax requires the seven-day follow-up process used for an emergency oral Schedule II authorization.", "That follow-up rule belongs to emergency oral authorization, not this hospice fax exception."),
        ("The fax exception also permits refills because the patient is receiving hospice care.", "The transmission exception does not create Schedule II refill authority."),
        ("The fax exception excludes opioid narcotics and applies to nonnarcotic Schedule II drugs instead.", "The hospice exception is specifically relevant to Schedule II narcotics."),
    ],
    "MA-Q-0195": [
        ("The provision creates a three-day retail prescription that the pharmacy may dispense in one fill.", "The emergency provision is not a routine retail-prescription exception."),
        ("The practitioner dispenses one day at a time for up to three days while arranging referral; the rule does not authorize a retail prescription.", "The rule is a narrow practitioner-dispensing bridge with daily and three-day limits."),
        ("The pharmacy may create a three-day methadone prescription after documenting the practitioner's telephone request.", "A pharmacy cannot create the practitioner's controlled-substance prescribing authority."),
        ("The practitioner cannot use emergency dispensing outside an OTP even while arranging an immediate treatment referral.", "Federal law contains the narrow non-OTP emergency dispensing pathway."),
        ("The practitioner may issue a 30-day prescription and mark the first three days as emergency supply.", "That structure does not comply with the dispense-only emergency pathway."),
    ],
}


def main() -> int:
    for qid, rows in PATCHES.items():
        path = QUESTIONS / f"{qid.lower()}.json"
        question = json.loads(path.read_text(encoding="utf-8"))
        if len(question["choices"]) != len(rows):
            raise RuntimeError(f"{qid}: choice count changed")
        for choice, (text, analysis) in zip(question["choices"], rows):
            choice["text"] = text
            question["explanation"]["choice_analysis"][choice["id"]] = analysis
        path.write_text(json.dumps(question, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"repaired construction cues for {len(PATCHES)} Batch 2 questions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
