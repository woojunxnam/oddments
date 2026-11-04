"""Export original visible question content without hidden author conclusions."""
import argparse
import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE_FIELDS = ('question_id', 'question_type', 'stem', 'choices',
               'correct_choice_ids', 'explanation')
EXPLANATION_FIELDS = {'core_reasoning', 'choice_analysis', 'choice_authorities', 'learning_boundary'}


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                    separators=(',', ':')).encode()).hexdigest()


def export(assignment, root=ROOT):
    if assignment.get('stage') != 'independent-legacy':
        raise ValueError('Independent legacy assignment required')
    hashes = assignment['question_hashes']
    if not hashes:
        raise ValueError('Empty independent assignment')
    config = json.loads((root/'site/practice-expansion/publication.json').read_bytes())
    paths = ['practice_expansion/2026-10-23/candidates/questions.json'] + [a['path'] for a in config['additional_banks']]
    originals = {}
    for path in paths:
        for question in json.loads((root/path).read_bytes())['questions']:
            qid = question['question_id']
            if qid in originals:
                raise ValueError('Duplicate original question: ' + qid)
            originals[qid] = question
    records = []
    for qid, expected in hashes.items():
        question = originals[qid]
        if digest(question) != expected:
            raise ValueError('Stale independent assignment: ' + qid)
        if any(set(c) != {'id', 'text'} for c in question['choices']):
            raise ValueError('Unrecognized visible choice structure: ' + qid)
        if set(question['explanation']) - EXPLANATION_FIELDS:
            raise ValueError('Unrecognized explanation structure: ' + qid)
        core = {k:copy.deepcopy(question[k]) for k in CORE_FIELDS}
        records.append(dict(question_id=qid, record_sha256=expected,
                            visible_content_sha256=digest(core), original_visible_content=core))
    return dict(schema_version='independent-legacy-visible-input/1',
                stage='independent-legacy', job_id=assignment['job_id'],
                question_hashes=hashes, records=records,
                scope='Original stem, every choice, key and complete visible explanation; '
                      'hidden author truth fields and prior review metadata are excluded. '
                      'This export is not legal evidence or an independence certificate.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--assignment', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    packet = export(json.loads(args.assignment.read_bytes()))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(packet, ensure_ascii=False, indent=2)+'\n')
    print(f"Exported {len(packet['records'])} complete visible questions; no review credit.")
