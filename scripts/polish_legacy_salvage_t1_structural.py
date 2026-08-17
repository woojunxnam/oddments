from __future__ import annotations

from qa_common import DATA, load_json, write_json


def update_question(number: int, *, choices=None, correct=None, choice_analysis=None, core_reasoning=None) -> None:
    path = DATA / "questions" / f"ma-q-{number:04d}.json"
    q = load_json(path)
    if choices is not None:
        q["choices"] = choices
    if correct is not None:
        q["correct_choice_ids"] = correct
    if choice_analysis is not None:
        q["explanation"]["choice_analysis"] = choice_analysis
    if core_reasoning is not None:
        q["explanation"]["core_reasoning"] = core_reasoning
    write_json(path, q)


def main() -> int:
    # Q0009: keep the schedule/PMP decision intact while making the CMEA distinction
    # an independently true configuration. This prevents a global three-correct SATA
    # concentration without changing the underlying law being tested.
    update_question(
        9,
        choices=[
            {"id": "A", "text": "Treat pregabalin as Schedule V and submit covered dispensing to MassPAT."},
            {"id": "B", "text": "Treat gabapentin as federally noncontrolled but Massachusetts Schedule VI and MassPAT-reportable."},
            {"id": "C", "text": "Treat methylphenidate as Schedule II and block prescription refills."},
            {"id": "D", "text": "Apply CMEA retail-sale controls to pseudoephedrine without classifying it as Schedule V solely because of those controls."},
            {"id": "E", "text": "Apply the federal Schedule III-IV five-refill/six-month rule to gabapentin solely because Massachusetts places it in Schedule VI."},
        ],
        correct=["A", "B", "C", "D"],
        choice_analysis={
            "A": "Correct. Pregabalin is Schedule V, and covered Massachusetts dispensing is reportable to MassPAT.",
            "B": "Correct. Gabapentin is not federally scheduled, but Massachusetts treats it as Schedule VI and includes it in PMP reporting.",
            "C": "Correct. Methylphenidate is Schedule II, for which refills are prohibited.",
            "D": "Correct. CMEA imposes separate retail-sale controls on pseudoephedrine without making the product Schedule V solely because of those controls.",
            "E": "Incorrect. Massachusetts Schedule VI classification does not by itself trigger the federal Schedule III-IV refill ceiling.",
        },
        core_reasoning="A pharmacy system must keep federal schedule, Massachusetts schedule, MassPAT reporting, refill limits, and CMEA retail controls separate. Pregabalin, gabapentin, and methylphenidate require the stated schedule/PMP/refill configurations, while pseudoephedrine requires its separate CMEA retail controls without being converted into Schedule V. Massachusetts Schedule VI status also does not import the federal Schedule III-IV refill rule into gabapentin.",
    )

    # Q0040: preserve the legal decision while removing a correct-answer length cue.
    q40 = load_json(DATA / "questions" / "ma-q-0040.json")
    choices40 = q40["choices"]
    for choice in choices40:
        if choice["id"] == "E":
            choice["text"] = "The technician is incorrect; Schedule IV status does not exempt tramadol from the separate seven-day opiate rule."
        elif choice["id"] == "A":
            choice["text"] = "The technician is correct because the seven-day statute applies only to Schedule II narcotic prescriptions."
        elif choice["id"] == "B":
            choice["text"] = "The technician is correct because Massachusetts excludes every Schedule IV drug from opiate supply limits."
    update_question(40, choices=choices40)

    # Q0075: preserve the professional-judgment boundary while splitting out an
    # additional independently authorized technical task. Four statements are true.
    update_question(
        75,
        choices=[
            {"id": "A", "text": "Collect and enter nonclinical demographic information while remaining under direct pharmacist supervision."},
            {"id": "B", "text": "Counsel the patient on the interaction after reading the drug-information screen."},
            {"id": "C", "text": "Perform authorized prescription-processing and staging tasks under direct pharmacist supervision, while leaving final verification to the pharmacist."},
            {"id": "D", "text": "Continue other authorized clerical or technical trainee functions while under direct pharmacist supervision."},
            {"id": "E", "text": "Refer the clinical question and unresolved DUR issue to the pharmacist rather than exercising pharmacist professional judgment."},
        ],
        correct=["A", "C", "D", "E"],
        choice_analysis={
            "A": "Correct. Nonclinical data collection/entry is a technical support function when performed within the trainee's direct-supervision framework.",
            "B": "Incorrect. Reading prepared information does not authorize a trainee to provide pharmacist counseling.",
            "C": "Correct. Authorized processing and staging may remain technical work under direct supervision, but final verification remains pharmacist professional judgment.",
            "D": "Correct. The trainee may continue authorized technical work under direct pharmacist supervision.",
            "E": "Correct. Clinical questions and unresolved DUR findings must be referred to the pharmacist.",
        },
        core_reasoning="A technician trainee may perform authorized clerical, prescription-processing, staging, and other technical support functions under the required direct pharmacist supervision, but may not independently counsel, resolve a clinical DUR problem, or perform final pharmacist verification. The clinical question and unresolved alert therefore go to the pharmacist while ordinary nonclinical trainee work may continue.",
    )

    # Q0078: distinguish separate education documentation from internship credit.
    # The daily cap, its recording consequence, and the separate-school-activity point
    # are all independently true, as is the fact that combining activity types does not
    # increase Board internship credit above the cap.
    update_question(
        78,
        choices=[
            {"id": "A", "text": "The preceptor should record no more than 12 qualifying internship hours for that day."},
            {"id": "B", "text": "No more than 12 hours may be credited toward the pharmacy internship in one day."},
            {"id": "C", "text": "The extra seminar may be documented separately as school activity, but it cannot increase that day's Board internship credit."},
            {"id": "D", "text": "Combining internship work with separately documented educational activity does not raise the Board's maximum internship credit above 12 hours for that day."},
            {"id": "E", "text": "All 14 hours may count as internship credit whenever the preceptor signs both the internship log and the seminar attendance record."},
        ],
        correct=["A", "B", "C", "D"],
        choice_analysis={
            "A": "Correct. The daily Board internship-credit record cannot exceed the 12-hour maximum.",
            "B": "Correct. Twelve hours is the maximum pharmacy internship credit for one day.",
            "C": "Correct. Separate educational documentation does not convert the additional seminar time into extra Board internship credit for that day.",
            "D": "Correct. Combining separately documented activities cannot expand the Board's daily internship-credit ceiling.",
            "E": "Incorrect. Signatures on separate records cannot waive the daily internship-credit ceiling.",
        },
        core_reasoning="The question concerns credit toward the Massachusetts pharmacy internship, not whether a student may be present for separate educational activity. Board internship credit is capped at 12 hours in one day. The preceptor therefore records at most 12 internship hours; separate school activity can be documented without increasing that day's Board internship credit, and combining the two activity types does not enlarge the daily cap.",
    )

    # Q0087: add an independent true product-selection checkpoint to diversify SATA correct-count patterns.
    update_question(
        87,
        choices=[
            {"id": "A", "text": "The valid no-substitution direction prevents the pharmacist from applying the usual required interchange on this prescription."},
            {"id": "B", "text": "The lower price automatically overrides a valid no-substitution direction."},
            {"id": "C", "text": "Without a valid no-substitution direction, the Massachusetts interchange framework generally requires use of the reasonably available, less expensive interchangeable product when its conditions are met."},
            {"id": "D", "text": "The patient may erase the prescriber's valid no-substitution direction and compel interchange without prescriber involvement."},
            {"id": "E", "text": "Before interchanging, the pharmacist must still confirm that the alternative satisfies the Massachusetts interchangeable-product framework rather than relying on price alone."},
        ],
        correct=["A", "C", "E"],
        choice_analysis={
            "A": "Correct. A valid prescriber no-substitution direction is a controlling exception to interchange.",
            "B": "Incorrect. Lower price does not nullify a valid no-substitution instruction.",
            "C": "Correct. In the absence of a valid no-substitution instruction, the statutory interchange conditions apply.",
            "D": "Incorrect. The patient cannot simply erase the prescriber's valid direction and convert it into a substitution-authorized prescription.",
            "E": "Correct. Price is not enough by itself; the selected alternative must satisfy the governing interchangeable-product requirements.",
        },
        core_reasoning="Massachusetts product selection depends on interchange eligibility, price/availability conditions, and the prescriber's substitution direction. A valid no-substitution instruction blocks the otherwise applicable interchange rule. When substitution is permitted, the pharmacist still must use a legally interchangeable product rather than treating lower price alone as sufficient.",
    )

    print("structural polish applied to Q0009/Q0040/Q0075/Q0078/Q0087")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
