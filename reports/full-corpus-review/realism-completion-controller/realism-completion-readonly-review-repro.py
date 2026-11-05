"""Read-only reproductions against exact audited commit; creates no repo files."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import types
from datetime import datetime

sys.dont_write_bytecode = True
REPO = Path('/workspace/oddments')
COMMIT = '78d34b823a17dba462b4da393431f009002e26f0'
sys.path.insert(0, '/workspace/mpje-realism95-native/scripts')
CACHE = {}


def read(path, expected=None):
    if path not in CACHE:
        CACHE[path] = subprocess.check_output(['git', '-C', str(REPO), 'show', COMMIT + ':' + path])
    raw = CACHE[path]
    if expected is not None:
        assert hashlib.sha256(raw).hexdigest() == expected, path
    return raw


def obj(path):
    return json.loads(read(path))


def exact_module(name):
    module = types.ModuleType(name)
    module.__file__ = '/workspace/mpje-realism95-native/scripts/' + name + '.py'
    sys.modules[name] = module
    exec(compile(read('scripts/' + name + '.py'), COMMIT + ':scripts/' + name + '.py', 'exec'), module.__dict__)
    return module


r = exact_module('realism_completion_review')
legal_module = exact_module('realism_completion_legal4')
builder = exact_module('build_full_corpus_review')
results = {'audited_commit': COMMIT, 'repository_mutated': False, 'reproductions': []}

# Exact retained proposal, current questions and native-only caller inventory.
scope = obj('reports/full-corpus-review/engineering/realism-completion-native-20261104/proposed-controller-scope-NOT_ACTIVATED.json')
config = obj('site/practice-expansion/publication.json')
banks = ['practice_expansion/2026-10-23/candidates/questions.json'] + [a['path'] for a in config['additional_banks']]
public = {row['question_id']: row for path in banks for row in obj(path)['questions']}
state = obj('reports/full-corpus-review/independent-legacy-work-queue.json')
report_paths = {row['evidence_path'] for job in state['jobs'] if job['status'] == 'INTEGRATED' for row in job['result']['results']}
primary = {row['question_id']: row for path in report_paths for row in obj(path)['records']}
try:
    r.validate_scope(scope, primary, public, read, scope['prior_supplementary'])
    raise AssertionError('Expected incomplete caller inventory rejection')
except KeyError as error:
    assert error.args == ('MA-CASE-0001',)
    results['reproductions'].append({'id': 'P1_INCOMPLETE_PARENT_INVENTORY', 'observed': repr(error)})

# The current old guard cannot accept a permitted new realism-only row.
try:
    builder.validate_independent_archive_safety(
        {'archive_review_notices': [], 'holds': [], 'safety_holds': []},
        [{'question_id': 'MA-EXP-0497', 'realism_review': {'verdict': 'PASS'}}])
    raise AssertionError('Expected absent legal_review failure')
except KeyError as error:
    assert error.args == ('legal_review',)
    results['reproductions'].append({'id': 'P1_UNTYPED_LEGACY_GUARD', 'observed': repr(error)})

# Synthetic authority bytes are intentionally fixtures, not actual legal evidence.
prefix = r.PREFIX + 'd/'
question = {'question_type': 'SBA', 'correct_choice_ids': ['A'], 'choices': [{'id': c, 'text': 'Synthetic option ' + c} for c in 'ABCD']}
raw, text = b'SYNTHETIC authority bytes', b'SYNTHETIC authority text'
meta = dict(official_url='https://www.ecfr.gov/current/title-21', raw_path=prefix+'raw', text_path=prefix+'text',
            raw_sha256=r.sha(raw), text_sha256=r.sha(text), status=200, method='SYNTHETIC',
            document_identity_status='OFFICIAL_TARGET_PROVISIONS_DIRECTLY_READ',
            retrieved_at='2026-11-04T12:01:00+00:00', read_at='2026-11-04T12:02:00+00:00')
evidence = {prefix+'raw': raw, prefix+'text': text, prefix+'meta': r.encoded(meta)}
authority = dict(source_id='official', official_url=meta['official_url'], exact_section='SYNTHETIC',
                 effective_date_or_version_basis='SYNTHETIC', law_checked_date='2026-11-04',
                 raw_path=prefix+'raw', raw_sha256=r.sha(raw), text_path=prefix+'text', text_sha256=r.sha(text),
                 metadata_path=prefix+'meta', metadata_sha256=r.sha(evidence[prefix+'meta']))
legal = dict(existing_answer_correct='YES', verdict='KEEP', stored_key=['A'], independently_expected_key=['A'],
             question_type='SBA', polarity='CORRECT', finding_ko='SYNTHETIC', prior_conclusions_read=False,
             hidden_truth_read=False, authorities=[authority],
             original_explanation_review=dict(core_reasoning_read=True, all_choice_rationales_read=list('ABCD'),
                                              learning_boundary_read=True, finding_ko='SYNTHETIC'),
             per_choice_findings=[dict(choice_id=c['id'], option_text_sha256=r.sha(c['text'].encode()),
                                      proposition_supported=None, finding_ko='SYNTHETIC unresolved option',
                                      authority_refs=['official']) for c in question['choices']])


def synthetic_read(path, expected=None):
    value = evidence[path]
    assert expected is None or expected == r.sha(value)
    return value


for supported in (None, False):
    for choice in legal['per_choice_findings']:
        choice['proposition_supported'] = supported
    legal_module.validate_legal({'question_id': 'MA-RW-0051', 'legal_review': legal}, question,
                               synthetic_read, prefix, datetime.fromisoformat('2026-11-04T12:06:00+00:00'))
    results['reproductions'].append({'id': 'P2_INCONSISTENT_ASSESSED_KEY', 'all_options_supported': supported,
                                     'key': 'YES', 'verdict': 'KEEP', 'polarity': 'CORRECT',
                                     'expected_key': ['A'], 'observed': 'ACCEPTED'})

print(json.dumps(results, ensure_ascii=False, indent=2))
