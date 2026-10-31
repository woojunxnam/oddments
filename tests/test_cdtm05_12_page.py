"""CDTM05–12 static learning bridge and immutable-question snapshot regression.

Tests verify IDs, existing answer keys and navigation; they are not a legal audit.
"""
import hashlib
import json
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "site/notes/cdtm05-12.html"
INDEX = ROOT / "site/notes/index.html"
DOC = ROOT / "docs/CDTM05_12_REVIEW_20261030.md"
EXPECTED_ORIGINAL = {
    "CDTM05": ("A", "B", "A", "C"),
    "CDTM06": ("D", "A", "A,C", "B"),
    "CDTM07": ("C", "D", "A,B,D", "A"),
    "CDTM08": ("B", "C", "A,B,C,D", "D"),
    "CDTM09": ("A", "B", "A", "C"),
    "CDTM10": ("D", "A", "B,D", "B"),
    "CDTM11": ("C", "D", "A,B,D", "A"),
    "CDTM12": ("B", "C", "A,B,C,D", "D"),
}
EXPECTED_REWRITES = ("B", "D", "A", "C", "D", "A", "C", "B")


class Anchors(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            assert attrs["id"] not in self.ids
            self.ids.add(attrs["id"])
        if tag == "a":
            self.links.append(attrs.get("href", ""))


def test_all_40_ids_are_linked_and_eight_separate_decisions_are_explained():
    body = PAGE.read_text(encoding="utf-8")
    dom = Anchors()
    dom.feed(body)
    for i, fam in enumerate(EXPECTED_ORIGINAL):
        assert fam.lower() in dom.ids
        assert "#MA-RW-" + str(i + 29).zfill(4) in " ".join(dom.links)
        for j in range(4):
            qid = "MA-EXP-" + str(241 + 4 * i + j).zfill(4)
            assert any(link.endswith("#" + qid) for link in dom.links), qid
    assert "CDTM05–12 · 사례 중심 집중 복습" in INDEX.read_text()
    assert 'href="cdtm05-12.html"' in INDEX.read_text()
    assert len([id for id in dom.ids if id.startswith("cdtm")]) == 8
    assert "NOT_INDEPENDENT" not in body or "독립" in body
    assert "247-cmr-16" in body.lower()
    assert "2021-04" in body
    assert "MA-EXP-0255" in body and "MA-EXP-0271" in body


def test_snapshot_keys_protected_and_editorial_count_exact():
    config = json.loads((ROOT / "site/practice-expansion/publication.json").read_text())
    original_path = ROOT / "practice_expansion/2026-10-23/candidates/questions.json"
    original_data = original_path.read_bytes()
    assert hashlib.sha256(original_data).hexdigest() == config["source_sha256"]
    original = {q["question_id"]: q for q in json.loads(original_data)["questions"]}
    revised = {q["question_id"]: q for q in json.loads(
        (ROOT / "practice_expansion/2026-10-28-representative/questions.json").read_text())["questions"]}
    count = 0
    for i, (family, expected) in enumerate(EXPECTED_ORIGINAL.items()):
        for j, encoded in enumerate(expected):
            qid = "MA-EXP-" + str(241 + 4 * i + j).zfill(4)
            q = original[qid]
            assert q["family_id"] == family
            assert q["correct_choice_ids"] == encoded.split(",")
            assert len(q["choices"]) == 4
            count += 1
        rw_id = "MA-RW-" + str(i + 29).zfill(4)
        rw = revised[rw_id]
        assert rw["family_id"] == family
        assert rw["correct_choice_ids"] == [EXPECTED_REWRITES[i]]
        assert len(rw["choices"]) == 4
        assert rw["verification_status"] == "NOT_INDEPENDENTLY_REVIEWED"
        count += 1
    assert count == 40
    assert sum(len(original["MA-EXP-" + str(n).zfill(4)]["choices"]) for n in range(241, 273)) == 128
    assert sum(len(revised["MA-RW-" + str(n).zfill(4)]["choices"]) for n in range(29, 37)) == 32
    assert original["MA-EXP-0255"]["correct_choice_ids"] == list("ABCD")
    assert original["MA-EXP-0271"]["correct_choice_ids"] == list("ABCD")


def test_editorial_report_does_not_claim_audited_canonical_release():
    report = DOC.read_text(encoding="utf-8")
    assert "40 ID" in report and "160" in report
    assert "NOT_INDEPENDENT_AUDIT" in report
    assert "기존 121개" in report
    assert "OPEN" in report
