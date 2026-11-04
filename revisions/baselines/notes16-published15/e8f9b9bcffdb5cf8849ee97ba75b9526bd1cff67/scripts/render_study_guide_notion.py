"""Render Study Guide sections as Notion-flavored Markdown for the Notion copy of the guide.

The audited prose is copied verbatim; this script only arranges and escapes it. By default it renders
the sections the public site shows -- VERIFIED ones -- so nothing unaudited reaches Notion by accident.

Korean study notes: ``study_aids/notion_ko/<section-id>.json`` holds a Korean translation and summary
of one section, item for item. It is rendered as a collapsible "🇰🇷 한국어 노트" toggle under each
English block. The notes are an unaudited study aid bound to the exact ``content_hash`` they were
written from, so a note file whose hash no longer matches its section is refused and the page renders
in English only until the notes are rewritten.

``render_blocks`` returns the same page as ordered English and Korean blocks, so the Korean notes can
also be placed into a Notion page that holds the English together with the reader's own notes.

    py -X utf8 scripts/render_study_guide_notion.py --out <dir>
    py -X utf8 scripts/render_study_guide_notion.py --out <dir> --section SG-MA-COUNSELING
    py -X utf8 scripts/render_study_guide_notion.py --check-korean
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from qa_common import DATA, load_json, load_records

ROOT = Path(__file__).resolve().parents[1]
KOREAN_DIR = ROOT / "study_aids" / "notion_ko"
KO_SUMMARY = "🇰🇷 한국어 노트"

# Notion documents \ * ~ ` $ [ ] < > { } | ^ as syntax. Underscore is not on that list, but a run of
# them parses as bold markers and silently disappears, which deletes every fill-in blank.
ESCAPE = frozenset("\\*~`$[]<>{}|^_")
HANGUL = re.compile("[가-힣]")
NUMBER = re.compile(r"\d+(?:\.\d+)*")
LIST_FIELDS = ("ma_vs_federal", "exceptions", "forms_records", "common_traps", "quick_review")


def esc(text: Any) -> str:
    return "".join("\\" + ch if ch in ESCAPE else ch for ch in str(text))


def cell(text: Any) -> str:
    # Table cells take rich text only, so keep each on one line.
    return esc(re.sub(r"\s+", " ", str(text)).strip())


def table_lines(columns: list[str], rows: list[list[str]]) -> list[str]:
    lines = ['<table fit-page-width="true" header-row="true">', "\t<tr>"]
    lines += [f"\t\t<td>{cell(column)}</td>" for column in columns]
    lines.append("\t</tr>")
    for row in rows:
        lines.append("\t<tr>")
        lines += [f"\t\t<td>{cell(value)}</td>" for value in row]
        lines.append("\t</tr>")
    lines.append("</table>")
    return lines


def toggle(summary: str, children: list[str]) -> list[str]:
    return ["<details>", f"<summary>{summary}</summary>", *[f"\t{line}" for line in children], "</details>"]


def ko_note(children: list[str]) -> list[str]:
    return toggle(KO_SUMMARY, children)


def authorities_for(section: dict[str, Any], rules: dict[str, dict[str, Any]]) -> list[tuple[str, str, str]]:
    seen: set[tuple[str, str, str]] = set()
    ordered = []
    for rule_id in section["rule_ids"]:
        for authority in rules[rule_id]["authority"]:
            key = (authority["name"], authority["section"], authority["url"])
            if key not in seen:
                seen.add(key)
                ordered.append(key)
    return ordered


def drug_label(drug_id: str) -> str:
    name = drug_id.replace("-", "/")
    return name[0].upper() + name[1:]


def render_blocks(
    section: dict[str, Any], rules: dict[str, dict[str, Any]], korean: dict[str, Any] | None = None
) -> list[tuple[bool, list[str]]]:
    """The page as ordered blocks of lines, each flagged True when it is a Korean note."""
    ko = korean or {}
    verified = section["verification_status"] == "VERIFIED"
    blocks: list[tuple[bool, list[str]]] = []
    number = 0

    def add(line: str) -> None:
        if blocks and not blocks[-1][0]:
            blocks[-1][1].append(line)
        else:
            blocks.append((False, [line]))

    def extend(lines: list[str]) -> None:
        for line in lines:
            add(line)

    def korean_block(lines: list[str]) -> None:
        blocks.append((True, list(lines)))

    def heading(title: str) -> None:
        nonlocal number
        number += 1
        add(f"## {number}. {title}")

    add('<callout icon="🎯" color="blue_bg">')
    add(f"\t**{esc(section['topic'])}**")
    add(f"\t{esc(section['subtopic'])}")
    if verified:
        add(
            f"\tIndependent audit `{esc(section['independent_audit_id'])}` · verified "
            f"{esc(section['last_verified'])} · content version {section['content_version']}"
        )
    else:
        add(f"\tAudit pending · content version {section['content_version']}")
    add("</callout>")
    if korean:
        korean_block(
            [
                '<callout icon="🇰🇷" color="gray_bg">',
                f"\t영어 노트 아래의 **{KO_SUMMARY}** 토글을 펼치면 번역·요약한 한국어 설명을 볼 수 있습니다. "
                "한국어 노트는 이해를 돕는 학습 자료이고 감사 대상이 아니므로, 법적 판단의 기준은 영어 본문입니다.",
                "</callout>",
            ]
        )

    heading("이 장에서 할 수 있어야 하는 것")
    for objective in section["learning_objectives"]:
        add(f"- {esc(objective)}")
    if korean:
        korean_block(ko_note([f"- {esc(text)}" for text in ko["learning_objectives"]]))

    authorities = authorities_for(section, rules)
    heading("근거 법령 (Governing authorities)")
    for name, pinpoint, url in authorities:
        add(f"- [{esc(pinpoint)}]({url}) — {esc(name)}")

    heading("개요 (The big picture)")
    for index, paragraph in enumerate(section["orientation"]):
        add(esc(paragraph["text"]))
        if korean:
            korean_block(ko_note([esc(ko["orientation"][index])]))

    if section["comparison_tables"]:
        heading("비교표 (Side by side)")
        for index, comparison in enumerate(section["comparison_tables"]):
            add(f"### {esc(comparison['title'])}")
            extend(table_lines(comparison["columns"], [row["cells"] for row in comparison["rows"]]))
            if korean:
                note = ko["comparison_tables"][index]
                korean_block(ko_note([f"**{esc(note['title'])}**", *[f"- {esc(text)}" for text in note["row_notes"]]]))

    if section["decision_logic"]:
        heading("판단 흐름 (Decision logic)")
        for step in section["decision_logic"]:
            add(f"1. **{esc(step['condition'])}**")
            add(f"\t{esc(step['action'])}")
        if korean:
            children = []
            for step in ko["decision_logic"]:
                children += [f"1. **{esc(step['condition'])}**", f"\t{esc(step['action'])}"]
            korean_block(ko_note(children))

    if section["worked_examples"]:
        heading("워크드 예제 (Worked examples)")
        for index, example in enumerate(section["worked_examples"], start=1):
            add(f"### 예제 {index}")
            add(esc(example["scenario"]))
            add("<details>")
            add("<summary>먼저 풀어본 다음 펼치기</summary>")
            for step in example["steps"]:
                add(f"\t1. {esc(step)}")
            add(f"\t**답:** {esc(example['resolution'])}")
            add("</details>")
            if korean:
                note = ko["worked_examples"][index - 1]
                solution = [*[f"1. {esc(step)}" for step in note["steps"]], f"**답:** {esc(note['resolution'])}"]
                korean_block(ko_note([f"**상황:** {esc(note['scenario'])}", *toggle("풀이와 답 보기", solution)]))

    if section["timing_deadlines"]:
        heading("기한 (Deadlines)")
        extend(
            table_lines(
                ["사건", "기한", "결과"],
                [[item["event"], item["timeframe"], item["consequence"]] for item in section["timing_deadlines"]],
            )
        )
        if korean:
            korean_block(ko_note([f"- {esc(text)}" for text in ko["timing_deadlines"]]))

    if section["role_duties"]:
        heading("누가 무엇을 하는가 (Who does what)")
        extend(table_lines(["역할", "의무"], [[item["role"], item["duty"]] for item in section["role_duties"]]))
        if korean:
            korean_block(ko_note([f"- {esc(text)}" for text in ko["role_duties"]]))

    list_headings = {
        "ma_vs_federal": "매사추세츠 vs 연방",
        "exceptions": "예외 (Exceptions)",
        "forms_records": "서식과 기록 (Forms and records)",
    }
    for field, title in list_headings.items():
        if section[field]:
            heading(title)
            for item in section[field]:
                add(f"- {esc(item['text'])}")
            if korean:
                korean_block(ko_note([f"- {esc(text)}" for text in ko[field]]))

    if section["drug_examples"]:
        heading("약물 예시")
        for item in section["drug_examples"]:
            add(f"- **{esc(drug_label(item['drug_id']))}:** {esc(item['teaching_point'])}")
        if korean:
            korean_block(
                ko_note(
                    [
                        f"- **{esc(drug_label(item['drug_id']))}:** {esc(text)}"
                        for item, text in zip(section["drug_examples"], ko["drug_examples"])
                    ]
                )
            )

    for field, title in (("common_traps", "함정 (High-yield traps)"), ("quick_review", "Quick review")):
        heading(title)
        for item in section[field]:
            add(f"- {esc(item['text'])}")
        if korean:
            korean_block(ko_note([f"- {esc(text)}" for text in ko[field]]))

    heading("Self-test — 먼저 답하고 펼치기")
    for index, prompt in enumerate(section["retrieval_prompts"], start=1):
        add("<details>")
        add(f"<summary>{index}. {esc(prompt['prompt'])}</summary>")
        add(f"\t{esc(prompt['answer'])}")
        add("</details>")
        if korean:
            note = ko["retrieval_prompts"][index - 1]
            korean_block(
                toggle(
                    f"🇰🇷 {index}번 한국어로 풀기",
                    [f"**문제:** {esc(note['prompt'])}", *toggle("답 보기", [esc(note["answer"])])],
                )
            )

    heading("공식 출처 (Official sources)")
    for name, pinpoint, url in authorities:
        add(f"- [{esc(name)}, {esc(pinpoint)}]({url})")

    heading("검증 기록")
    if verified:
        add('<callout icon="✅" color="green_bg">')
        add(
            f"\t이 장의 모든 법적 명제는 독립 감사자 `{esc(section['independent_audit_id'])}`가 "
            f"{esc(section['last_verified'])}에 공식 원문과 대조해 KEEP 판정한 내용입니다."
        )
    else:
        add('<callout icon="⏳" color="yellow_bg">')
        add("\t이 장은 아직 독립 감사를 통과하지 않았습니다. 공개용이 아닌 미리보기입니다.")
    add(f"\t저장소 섹션 ID `{esc(section['section_id'])}` · content hash `{esc(section['content_hash'][:16])}`")
    add(f"\t연습문제 연결: {', '.join(esc(q) for q in section['practice_question_ids']) or '없음'}")
    add("</callout>")

    return blocks


def render(section: dict[str, Any], rules: dict[str, dict[str, Any]], korean: dict[str, Any] | None = None) -> str:
    return "\n".join(line for _, lines in render_blocks(section, rules, korean) for line in lines) + "\n"


def korean_problems(section: dict[str, Any], notes: dict[str, Any]) -> list[str]:
    """Why these Korean notes cannot be rendered for this section; empty when they can.

    The notes must mirror the section item for item, carry Hangul, and keep every number the English
    item states -- a dropped day count or pinpoint is exactly the kind of loss a summary invites.
    """
    problems: list[str] = []
    if notes.get("section_id") != section["section_id"]:
        problems.append("section_id does not match the section")
    if notes.get("source_content_hash") != section["content_hash"]:
        problems.append("written from a different content hash than the section now has")

    pairs: list[tuple[str, str, Any]] = []

    def parallel(field: str, english: list[Any]) -> list[Any] | None:
        korean = notes.get(field)
        if not isinstance(korean, list) or len(korean) != len(english):
            problems.append(f"{field}: expected {len(english)} item(s)")
            return None
        return korean

    def strings(field: str, english: list[str]) -> None:
        korean = parallel(field, english)
        if korean is not None:
            pairs.extend((f"{field}[{i}]", en, ko) for i, (en, ko) in enumerate(zip(english, korean)))

    strings("learning_objectives", section["learning_objectives"])
    strings("orientation", [item["text"] for item in section["orientation"]])
    for field in LIST_FIELDS:
        strings(field, [item["text"] for item in section[field]])
    strings("drug_examples", [item["teaching_point"] for item in section["drug_examples"]])
    strings(
        "timing_deadlines",
        [" ".join((item["event"], item["timeframe"], item["consequence"])) for item in section["timing_deadlines"]],
    )
    strings("role_duties", [" ".join((item["role"], item["duty"])) for item in section["role_duties"]])

    tables = parallel("comparison_tables", section["comparison_tables"])
    for i, (table, note) in enumerate(zip(section["comparison_tables"], tables or [])):
        if not isinstance(note, dict) or len(note.get("row_notes") or []) != len(table["rows"]):
            problems.append(f"comparison_tables[{i}]: expected a title and {len(table['rows'])} row note(s)")
            continue
        pairs.append((f"comparison_tables[{i}].title", table["title"], note.get("title")))
        pairs.extend(
            (f"comparison_tables[{i}].row_notes[{j}]", " ".join(row["cells"]), text)
            for j, (row, text) in enumerate(zip(table["rows"], note["row_notes"]))
        )

    steps = parallel("decision_logic", section["decision_logic"])
    for i, (step, note) in enumerate(zip(section["decision_logic"], steps or [])):
        note = note if isinstance(note, dict) else {}
        pairs.append((f"decision_logic[{i}].condition", step["condition"], note.get("condition")))
        pairs.append((f"decision_logic[{i}].action", step["action"], note.get("action")))

    examples = parallel("worked_examples", section["worked_examples"])
    for i, (example, note) in enumerate(zip(section["worked_examples"], examples or [])):
        if not isinstance(note, dict) or len(note.get("steps") or []) != len(example["steps"]):
            problems.append(f"worked_examples[{i}]: expected {len(example['steps'])} step(s)")
            continue
        pairs.append((f"worked_examples[{i}].scenario", example["scenario"], note.get("scenario")))
        pairs.extend(
            (f"worked_examples[{i}].steps[{j}]", en, ko) for j, (en, ko) in enumerate(zip(example["steps"], note["steps"]))
        )
        pairs.append((f"worked_examples[{i}].resolution", example["resolution"], note.get("resolution")))

    prompts = parallel("retrieval_prompts", section["retrieval_prompts"])
    for i, (prompt, note) in enumerate(zip(section["retrieval_prompts"], prompts or [])):
        note = note if isinstance(note, dict) else {}
        pairs.append((f"retrieval_prompts[{i}].prompt", prompt["prompt"], note.get("prompt")))
        pairs.append((f"retrieval_prompts[{i}].answer", prompt["answer"], note.get("answer")))

    for location, english, korean in pairs:
        if not isinstance(korean, str) or not korean.strip():
            problems.append(f"{location}: empty")
        elif not HANGUL.search(korean):
            problems.append(f"{location}: no Korean text")
        else:
            missing = sorted(set(NUMBER.findall(english)) - set(NUMBER.findall(korean)))
            if missing:
                problems.append(f"{location}: drops number(s) {', '.join(missing)}")
    return problems


def korean_file(section_id: str) -> Path:
    return KOREAN_DIR / f"{section_id.lower()}.json"


def load_guide() -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]], list[str]]:
    rules = {record["rule_id"]: record for _, record in load_records(DATA / "rules")}
    sections = {record["section_id"]: record for _, record in load_records(DATA / "study_guide" / "sections")}
    order = [entry["section_id"] for entry in load_json(DATA / "study_guide" / "index.json")["sections"]]
    return rules, sections, order


def selected(
    sections: dict[str, dict[str, Any]],
    order: list[str],
    *,
    include_pending: bool = False,
    only: list[str] | None = None,
) -> list[dict[str, Any]]:
    wanted = set(only) if only else None
    chosen = []
    for section_id in order:
        section = sections.get(section_id)
        if section is None or (wanted is not None and section_id not in wanted):
            continue
        if include_pending or section["verification_status"] == "VERIFIED":
            chosen.append(section)
    return chosen


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", type=Path, help="directory to write <SECTION-ID>.md files into")
    parser.add_argument("--section", action="append", help="render only this section id (repeatable)")
    parser.add_argument(
        "--include-pending", action="store_true", help="also render sections still awaiting audit (private preview)"
    )
    parser.add_argument("--english-only", action="store_true", help="ignore Korean study notes")
    parser.add_argument(
        "--check-korean", action="store_true", help="check the Korean study notes against their sections and exit"
    )
    args = parser.parse_args(argv)

    rules, sections, order = load_guide()
    chosen = selected(sections, order, include_pending=args.include_pending, only=args.section)

    if args.check_korean:
        failing = 0
        for section in chosen:
            path = korean_file(section["section_id"])
            if not path.exists():
                print(f"{section['section_id']:40} no Korean notes")
                continue
            problems = korean_problems(section, load_json(path))
            failing += bool(problems)
            print(f"{section['section_id']:40} {'OK' if not problems else f'{len(problems)} problem(s)'}")
            for problem in problems:
                print(f"    {problem}")
        return 1 if failing else 0

    if args.out is None:
        parser.error("--out is required unless --check-korean is given")
    args.out.mkdir(parents=True, exist_ok=True)
    for section in chosen:
        notes = None
        path = korean_file(section["section_id"])
        if not args.english_only and path.exists():
            candidate = load_json(path)
            problems = korean_problems(section, candidate)
            if problems:
                print(
                    f"{section['section_id']}: Korean notes not rendered ({len(problems)} problem(s), "
                    f"first: {problems[0]})",
                    file=sys.stderr,
                )
            else:
                notes = candidate
        text = render(section, rules, notes)
        (args.out / f"{section['section_id']}.md").write_text(text, encoding="utf-8")
        print(f"{section['section_id']:40} {len(text):>7,} chars{'  with Korean notes' if notes else ''}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
