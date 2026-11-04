"""Independent exact-cdd read-only follow-up; all synthetic bytes stay in memory."""
from pathlib import Path
helpers = Path('/workspace/scratch/realism-completion-readonly-review-repro.py').read_text().split('r = exact_module')[0]
exec(helpers.replace("COMMIT = '78d34b823a17dba462b4da393431f009002e26f0'", "COMMIT = 'cdd3617c91c307eb8571708fcd19eb5643ff4d72'"), globals())
import copy
r = exact_module('realism_completion_review')
lm = exact_module('realism_completion_legal4')
m = exact_module('realism_completion_metadata')
closure = sys.modules['notes_published15_closure']
builder = exact_module('build_full_corpus_review')
results = {'audited_commit': COMMIT, 'repository_mutated': False, 'checks': []}

scope = obj('reports/full-corpus-review/engineering/realism-completion-native-20261104/proposed-controller-scope-NOT_ACTIVATED.json')
scope['static_primary_sources'] = {p:r.sha(read(p)) for p in r.STATIC_PRIMARY_PATHS}
scope['format_cache_origin'] = copy.deepcopy(r.APPROVED_ORIGIN)
config = obj('site/practice-expansion/publication.json')
banks = ['practice_expansion/2026-10-23/candidates/questions.json'] + [a['path'] for a in config['additional_banks']]
public = {row['question_id']:row for path in banks for row in obj(path)['questions']}
state = obj('reports/full-corpus-review/independent-legacy-work-queue.json')
report_paths = {row['evidence_path'] for job in state['jobs'] if job['status']=='INTEGRATED' for row in job['result']['results']}
primary = {row['question_id']:row for path in report_paths for row in obj(path)['records']}
complete = m.fill_static_primary(REPO, list(primary.values()), read)
r.validate_scope(scope,{row['question_id']:row for row in complete},public,read,scope['prior_supplementary'])
results['checks'].append({'id':'P1_STATIC_INVENTORY_FIXED','result':'PASS'})
try:
    r.validate_scope(scope,primary,public,read,scope['prior_supplementary'])
    raise AssertionError('Incomplete inventory must fail explicitly')
except ValueError as error:
    assert 'Complete static3/native primary inventory' in str(error)

# Reuse the original synthetic authority report, now with the required lead.
synthetic = Path('/workspace/scratch/realism-completion-readonly-review-repro.py').read_text().split('# Synthetic authority bytes')[1].split('for supported in (None, False):')[0]
exec('# Synthetic authority bytes'+synthetic, globals())
question['stem'] = 'Synthetic neutral context.\n\nWhich action is correct?'
for supported in (None,False):
    for choice in legal['per_choice_findings']:choice['proposition_supported']=supported
    try:
        lm.validate_legal({'question_id':'MA-RW-0051','legal_review':legal},question,synthetic_read,prefix,datetime.fromisoformat('2026-11-04T12:06:00+00:00'))
        raise AssertionError('Incomplete or inconsistent option truth accepted')
    except ValueError as error:
        results['checks'].append({'id':'P2_LEGAL_TRUTH_FIXED','all_options':supported,'result':'REJECTED','reason':str(error)})
for choice in legal['per_choice_findings']:choice['proposition_supported']=choice['choice_id']=='A'
lm.validate_legal({'question_id':'MA-RW-0051','legal_review':legal},question,synthetic_read,prefix,datetime.fromisoformat('2026-11-04T12:06:00+00:00'))
results['checks'].append({'id':'P2_CONSISTENT_KEY_STILL_ALLOWED','result':'PASS'})

# Exact typed-dispatch and containment routines with in-memory committed metadata.
# load_metadata itself is separately exercised by repository fixture tests.
uid='MA-EXP-0497'; report_path=r.PREFIX+'a/report.json'
row={'question_id':uid,'record_sha256':'a'*64,'realism_review':{'verdict':'PASS'}}
report={'records':[row]}; report_raw=r.encoded(report)
binding={'source_path':report_path,'source_sha256':r.sha(report_raw),'review_kind':'REALISM_COMPLETION'}
proof={'record':row,'report_path':report_path,'report_sha256':r.sha(report_raw)}
metadata={'assessments':{uid:proof}}
selection={'recommended_ids':[],'holds':[],'safety_holds':[],'archive_review_notices':[]}
validated={'primary_records':[],'supplementary_sources':{uid:binding}}
closure.committed=lambda root,path,expected=None: report_raw
r.questions=lambda root,read: ({},{},{})
m.load_metadata=lambda root,primary,public: metadata
closure.validate_publication_default_safety(REPO,{'full_source_files':{}},selection,validated)
results['checks'].append({'id':'P1_STYLE_ONLY_DISPATCH_FIXED','result':'PASS'})
selection['recommended_ids']=[uid]
try:
    closure.validate_publication_default_safety(REPO,{'full_source_files':{}},selection,validated)
    raise AssertionError('Default return accepted')
except ValueError as error:
    assert 'cannot return to default' in str(error)
selection['recommended_ids']=[]; row['realism_review']['verdict']='FAIL'
report_raw=r.encoded(report)
binding['source_sha256']=proof['report_sha256']=r.sha(report_raw)
try:
    closure.validate_publication_default_safety(REPO,{'full_source_files':{}},selection,validated)
    raise AssertionError('FAIL without source-bound notice accepted')
except ValueError as error:
    assert 'actual source-bound archive notice' in str(error)
selection['archive_review_notices']=[dict(question_ids=[uid],issue_type='INDEPENDENT_REVIEW_FINDING',review_source=report_path,review_source_sha256=proof['report_sha256'],question_record_hashes={uid:row['record_sha256']})]
closure.validate_publication_default_safety(REPO,{'full_source_files':{}},selection,validated)
results['checks'].append({'id':'DEFAULT_AND_FAIL_CONTAINMENT_PRESERVED','result':'PASS'})

origin_raw=read(r.APPROVED_ORIGIN['path'],r.APPROVED_ORIGIN['raw_sha256'])
origin=json.loads(origin_raw)
assert origin['retrieved_at']=='2026-11-04T18:19:26.088117+00:00'
assert origin['official_url']==origin['final_url']==r.FORMAT_URL and origin['status']==200
assert origin['public_raw_redistribution'] is False
results['checks'].append({'id':'CACHE_ORIGIN_EXACT_PIN_AND_ORIGINAL_TIME','result':'PASS','origin_retrieved_at':origin['retrieved_at'],'raw_sha256':r.sha(origin_raw)})
print(json.dumps(results,ensure_ascii=False,indent=2))
