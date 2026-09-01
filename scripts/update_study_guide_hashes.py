from __future__ import annotations

from qa_common import DATA, load_records, write_json
from study_guide_common import study_guide_content_hash


def main() -> int:
    for path, section in load_records(DATA / "study_guide" / "sections"):
        section["content_hash"] = study_guide_content_hash(section)
        write_json(path, section)
        print(f"updated {path.relative_to(DATA.parent)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
