"""Machine-readable controller ledger for the Issue #83 Claude Code controller run.

The ledger is append-structured: each phase records its own exact SHAs, commands,
outputs and gate results so the whole run is reproducible from the repository alone.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from qa_common import ROOT, load_json, write_json


LEDGER_PATH = ROOT / "audits" / "controller" / "ISSUE-83-CONTROLLER-LEDGER.json"

CONTROLLER_ISSUE = 83
START_BRANCH = "repair/pre-batch3-coverage-t2-r1"
START_HEAD = "bfc1be694053f84bf688126246131f16df1374d1"


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def empty_ledger() -> dict:
    return {
        "ledger_type": "CLAUDE_CODE_CONTROLLER_LEDGER",
        "controller_issue": CONTROLLER_ISSUE,
        "controller": "Claude Code (mechanical/governance controller, not an auditor)",
        "independence_wall": (
            "This controller performs mechanical and governance work only. It does not act as, "
            "or impersonate, a fresh independent auditor for any substantive content it authored "
            "or repaired. Existing accepted T2 audits were represented, never re-judged."
        ),
        "start_boundary": {
            "branch": START_BRANCH,
            "required_head": START_HEAD,
            "verified": None,
        },
        "current_phase": None,
        "phases": [],
    }


def load_ledger() -> dict:
    if LEDGER_PATH.exists():
        return load_json(LEDGER_PATH)
    return empty_ledger()


def record_phase(phase_id: str, payload: dict) -> dict:
    ledger = load_ledger()
    entry = {"phase": phase_id, **payload}
    ledger["phases"] = [item for item in ledger["phases"] if item.get("phase") != phase_id]
    ledger["phases"].append(entry)
    ledger["phases"].sort(key=lambda item: item["phase"])
    ledger["current_phase"] = phase_id
    write_json(LEDGER_PATH, ledger)
    return ledger


def main() -> int:
    if len(sys.argv) < 3:
        print("usage: controller_ledger.py <PHASE_ID> <payload.json|->", file=sys.stderr)
        return 2
    phase_id = sys.argv[1]
    source = sys.argv[2]
    payload = json.loads(sys.stdin.read() if source == "-" else Path(source).read_text(encoding="utf-8"))
    record_phase(phase_id, payload)
    print(f"ledger: recorded {phase_id} -> {LEDGER_PATH.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
