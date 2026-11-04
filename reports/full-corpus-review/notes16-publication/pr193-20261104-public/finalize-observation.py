"""Assemble only observed public results; incomplete CI remains PENDING."""
from datetime import datetime,timezone
import hashlib,json
from pathlib import Path

OUT=Path(__file__).resolve().parent
def load(name):return json.loads((OUT/name).read_bytes())
def write(name,value):(OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
api=load('api-final-summary.json');assets=load('https40-final.json');runs=load('browser-runs.json')
assert api['merged']and api['tree_equivalent']and api['pages_status']=='completed'and api['pages_conclusion']=='success'
assert api['pages_head']==api['merge_sha']
assert assets['matched']==assets['total']==40 and not assets['failures']
assert len(runs)==5 and all(r['exit_code']==0 and r['actual_origin']=='https://woojunxnam.github.io/oddments/'for r in runs)
reports={name:load(name+'/report.json')for name in ('public-practice','notes','refresh','q0012-withdrawal','representative-rewrites','public-state')}
assert reports['representative-rewrites']['status']=='passed'
pending=[r for r in api['merge_workflows']if r['status']!='completed']
failed=[r for r in api['merge_workflows']if r['status']=='completed'and r['conclusion']!='success']
observation=dict(observed_at_utc=datetime.now(timezone.utc).isoformat(),
    purpose='ACTUAL_PUBLIC_CANONICAL_HTTPS_BYTES_AND_ISOLATED_BROWSER_VERIFICATION_NOT_LEGAL_AUDIT',
    source_merge=api['merge_sha'],tested_candidate=api['candidate_sha'],tree=api['api_merge_tree'],tree_equivalent=True,
    origin='https://woojunxnam.github.io/oddments/',pages_run=41907593476,pages_status='SUCCESS',
    canonical_https_assets=dict(count=40,matched=40,query_parameters_used=False,tls_verification=True,critical14_subset=load('critical14-subset.json')),
    public_state=dict(question_key_assessments=1793,independent_notes_complete=100,default_practice_questions=202,
       note_total_units=306,practice_total_questions=2349,n1_unit='w3-a-3',n1_011_legal_hold_preserved=True,
       n1_review_history_preserved=True,future_root_question2296_and_complete_notes306_and_realism146_not_deployed_or_expected=True),
    browser_suites=dict(passed=5,failed=0,runs='browser-runs.json',
      public_practice_checks=reports['public-practice']['passed'],notes_checks=len(reports['notes']['checks_passed']),
      refresh_checks=reports['refresh']['count'],representative_checks=len(reports['representative-rewrites']['checks']),
      representative_new_cases_exercised=reports['representative-rewrites']['new_cases_exercised'],
      q0012_withdrawal=reports['q0012-withdrawal']['status']),
    observed_javascript_errors={name:r.get('page_errors',r.get('errors',r.get('javascript_errors',[])))for name,r in reports.items()},
    postmerge_workflows=dict(source_commit=api['merge_sha'],snapshot='api-final-summary.json',
      status='FAILED'if failed else 'PENDING'if pending else 'ALL_SUCCESS',pending=pending,failed=failed,runs=api['merge_workflows']),
    software_only=True,physical_device_testing=False,real_user_browser_profile_used=False,
    question_audit_credit=0,canonical_release_credit=0,
    limitations=[
      'Headless Chromium desktop/mobile viewport emulation; no physical iOS/Android/Safari test.',
      'All browser checks use actual public HTTPS origin and isolated synthetic storage; no existing loopback proof was relabelled.',
      'Notes/refresh original CLIs lack --base-url; recorded in-memory origin-only adapters replace loopback server selection while preserving assertions.',
      'Browser negative cases intentionally deny synthetic storage or abort a payload; these test fallback behavior, not an observed production outage.',
      'Published existing audit statuses and holds are observed, not new law/style judgments or canonical-release approval.',
      'Candidate/full-CI earlier success is not substituted for still-pending postmerge workflows.'
    ])
assert all(not errors for errors in observation['observed_javascript_errors'].values())
write('observation.json',observation)
(OUT/'README.md').write_text(
    '# PR193 actual public verification\n\n'
    'Verified merge `'+api['merge_sha']+'` and tested candidate `'+api['candidate_sha']+'` share tree `'+api['api_merge_tree']+'`.\n\n'
    'Pages run [41907593476](https://github.com/woojunxnam/oddments/actions/runs/41907593476) succeeded for that exact merge. '
    'All 40 normal public asset URLs matched exact candidate bytes, including the historical critical14 path subset. No query cachebuster was used.\n\n'
    'All five browser suites passed against [the actual public origin](https://woojunxnam.github.io/oddments/). '
    'Original notes/refresh scripts have no production URL option: `production-browser-adapter.py` records their source hashes and replaces only the server/origin selection in memory. '
    'Their assertions and actual navigation/storage branches remain intact. No source script, protected gate or generated site file was edited.\n\n'
    'Published observations: key assessments1793, independent-note completion100, default practice202. '
    'N1 original011 HOLD/blocker/history remain visible; future root work is not treated as published.\n\n'
    'Postmerge workflow status at the final API observation: **'+observation['postmerge_workflows']['status']+'**. '
    'See `api-final-summary.json`; pending is not presented as passing.\n\n'
    'Evidence: `observation.json`, `https40-{initial,final}.json`, `api/`, `browser-runs.json`, per-suite reports/logs/screenshots, '
    '`public-state/report.json`, CLI help, adapter source/provenance and `artifact-sha256.json`.\n\n'
    'This is read-only public software/deployment verification using isolated synthetic browser storage. '
    'It grants no legal-audit or canonical-release credit and includes no physical-device testing.\n')
manifest={p.relative_to(OUT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()for p in sorted(OUT.rglob('*'))if p.is_file()and p.name!='artifact-sha256.json'}
write('artifact-sha256.json',manifest)
print(json.dumps({'public_status':'PASS','postmerge_ci_status':observation['postmerge_workflows']['status'],
                  'artifacts':len(manifest),'screenshots':len(list(OUT.rglob('*.png')))},ensure_ascii=False),flush=True)
