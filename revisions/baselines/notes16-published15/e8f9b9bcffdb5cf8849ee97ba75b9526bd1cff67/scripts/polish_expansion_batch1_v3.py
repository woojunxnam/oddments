from __future__ import annotations

from qa_common import DATA, load_json, write_json


def update_choice(question: dict, choice_id: str, text: str) -> None:
    for choice in question["choices"]:
        if choice["id"] == choice_id:
            choice["text"] = text
            return
    raise KeyError(f"missing choice {choice_id} in {question['question_id']}")


def main() -> int:
    path = DATA / "questions" / "ma-q-0111.json"
    q = load_json(path)
    update_choice(
        q,
        "B",
        "No. The statute excepts Schedule II or III drugs prescribed for substance use disorder or opioid-dependence treatment.",
    )
    q["explanation"]["choice_analysis"]["B"] = (
        "This dispensing fits the statutory exception for treatment of substance use disorder or opioid dependence."
    )
    write_json(path, q)

    path = DATA / "questions" / "ma-q-0129.json"
    q = load_json(path)
    update_choice(
        q,
        "A",
        "Send the supplier written cancellation of the identified line; the supplier documents the cancellation on the original Form 222.",
    )
    q["explanation"]["choice_analysis"]["A"] = (
        "DEA permits written cancellation of part or all of a submitted paper Form 222, with the supplier documenting it on the original."
    )
    write_json(path, q)

    print("polished v3 answer-cue balance: MA-Q-0111, MA-Q-0129")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
