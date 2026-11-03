import copy
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from export_legacy_review_input import export, digest, CORE_FIELDS


def assignment_and_question():
    question = json.loads((ROOT/'practice_expansion/2026-10-26-plus/questions.json').read_bytes())['questions'][0]
    return dict(stage='independent-legacy', job_id='fixture',
                question_hashes={question['question_id']:digest(question)}), question


def test_original_visible_input_is_complete_and_hidden_truth_never_leaks():
    assignment, question = assignment_and_question()
    before = copy.deepcopy(question)
    record = export(assignment)['records'][0]
    core = record['original_visible_content']
    assert core == {k:question[k] for k in CORE_FIELDS}
    assert set(core) == set(CORE_FIELDS)
    assert '_statement_truth' in question and '_statement_truth' not in json.dumps(core)
    assert record['record_sha256'] == digest(question)
    assert record['visible_content_sha256'] == digest(core)
    assert question == before


def test_stale_or_nonindependent_assignment_cannot_produce_review_input():
    assignment, _ = assignment_and_question()
    assignment['question_hashes'] = {next(iter(assignment['question_hashes'])):'0'*64}
    with pytest.raises(ValueError, match='Stale independent assignment'):
        export(assignment)
    assignment['stage'] = 'author'
    with pytest.raises(ValueError, match='Independent legacy assignment required'):
        export(assignment)
