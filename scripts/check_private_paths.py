from __future__ import annotations

import subprocess
from pathlib import PurePosixPath

from qa_common import ROOT, QAReport, print_report


PRIVATE_PARTS = {"local_private", "private_sources", "licensed_sources"}
PRIVATE_SUFFIXES = (".private.pdf", ".licensed.pdf")


def tracked_paths() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=ROOT,
        capture_output=True,
        check=True,
    )
    return [item.decode("utf-8") for item in result.stdout.split(b"\0") if item]


def check_private_paths(paths: list[str] | None = None) -> QAReport:
    report = QAReport()
    for raw_path in paths if paths is not None else tracked_paths():
        path = PurePosixPath(raw_path.replace("\\", "/"))
        lowered_parts = {part.casefold() for part in path.parts}
        lowered_name = path.name.casefold()
        if PRIVATE_PARTS & lowered_parts or lowered_name.endswith(PRIVATE_SUFFIXES):
            report.error(f"restricted private-source path is tracked: {raw_path}")
    return report


def main() -> int:
    return print_report("private paths", check_private_paths())


if __name__ == "__main__":
    raise SystemExit(main())
