from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

import pytest


def node_binary() -> str | None:
    return os.environ.get("NODE_BIN") or shutil.which("node")


@pytest.mark.skipif(node_binary() is None, reason="Node.js is required to execute the website shuffle module")
def test_answer_choice_shuffle_preserves_correctness_and_ordered_semantics(root: Path) -> None:
    script = r"""
const fs = require('fs');
const shuffle = require(process.argv[1]);
const sba = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const ordered = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'));
const first = shuffle.shuffleQuestionChoices(sba, 'fixed-seed');
const second = shuffle.shuffleQuestionChoices(sba, 'fixed-seed');
if (JSON.stringify(first) !== JSON.stringify(second)) throw new Error('shuffle is not deterministic');
const canonicalCorrect = new Set(sba.correct_choice_ids);
const remappedCorrectSources = new Set(
  first.choices.filter((choice) => first.correct_choice_ids.includes(choice.id)).map((choice) => choice.source_id)
);
if (canonicalCorrect.size !== remappedCorrectSources.size) throw new Error('correct answer count changed');
for (const answer of canonicalCorrect) {
  if (!remappedCorrectSources.has(answer)) throw new Error('correct answer mapping changed');
}
const orderedResult = shuffle.shuffleQuestionChoices(ordered, 'fixed-seed');
if (JSON.stringify(orderedResult.choices.map((choice) => choice.id)) !== JSON.stringify(ordered.choices.map((choice) => choice.id))) {
  throw new Error('ordered-response choices were shuffled');
}
if (JSON.stringify(orderedResult.correct_choice_ids) !== JSON.stringify(ordered.correct_choice_ids)) {
  throw new Error('ordered-response answer semantics changed');
}
"""
    result = subprocess.run(
        [
            node_binary(),
            "-e",
            script,
            str(root / "site" / "shuffle.js"),
            str(root / "data" / "questions" / "ma-q-0001.json"),
            str(root / "data" / "questions" / "ma-q-0007.json"),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
