"""원본 워크플로 바이트와 정확히 한 줄의 시간 예산 변경만 있는지 검증합니다."""
from pathlib import Path
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parents[4]
BASE = '91a58a12cc5f12a09a0cba3a1a692e8fabfb7687'
WORKFLOW = '.github/workflows/practice-quality-qa.yml'
EVIDENCE = 'reports/full-corpus-review/engineering/time-budget-practice-quality-20261104/'

def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args])

old = git('show', f'{BASE}:{WORKFLOW}')
new = (ROOT / WORKFLOW).read_bytes()
assert old.count(b'    timeout-minutes: 15\n') == 1
assert new == old.replace(b'    timeout-minutes: 15\n', b'    timeout-minutes: 120\n', 1)
# Exact equality after replacing only the budget is stronger than parsed-YAML
# equality and preserves all existing whitespace, steps and embedded commands.
changed = git('diff', '--name-only', BASE, '--').decode().splitlines()
assert set(p for p in changed if not p.startswith(EVIDENCE)) == {WORKFLOW}, changed
job = json.loads((ROOT / EVIDENCE / 'job.json').read_bytes())
annotations = json.loads((ROOT / EVIDENCE / 'annotations.json').read_bytes())
assert job['head_sha'] == BASE
assert job['id'] == 126695337141 and job['run_id'] == 41864566412
assert job['conclusion'] == 'cancelled'
assert any(a['message'] == 'The job has exceeded the maximum execution time of 15m0s' for a in annotations)
obs = json.loads((ROOT / EVIDENCE / 'observation.json').read_bytes())
for name, expected in obs['artifacts'].items():
    assert hashlib.sha256((ROOT / EVIDENCE / name).read_bytes()).hexdigest() == expected
print(json.dumps({'result': 'PASS', 'base_sha': BASE, 'exact_budget_only_workflow_change': True, 'all_other_tracked_runtime_test_data_files_equal': True, 'original_timeout_evidence_hashes_valid': True, 'new_ci_result': 'NOT_EXECUTED'}, indent=2))
