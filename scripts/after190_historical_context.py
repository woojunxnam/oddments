"""Four exact historical input receipts; never aliases for current/primary data.

Original Git objects were resolved during preparation. Runtime uses committed
HEAD-retained bytes only and cannot discover or enroll another historical input.
"""
import hashlib
import json

REGISTRY='reports/full-corpus-review/after190-historical-context/registry-v2.json'
REGISTRY_SHA='6e33c9d2119706752646e342eb1615fddd526935cb54dc260ea1e384ddf6652c'
PREVIOUS_REGISTRY='reports/full-corpus-review/after190-historical-context/registry.json'
PREVIOUS_REGISTRY_SHA='989354cc809d64afc20d8f0108cf7937151bb01cdb2459f77a1697d056e30536'
PROGRESS='reports/full-corpus-review/progress.json'
RUNBOOK='docs/INDEPENDENT_DEFAULT_WAVE9_RUNBOOK.md'
SELECTION='practice_expansion/2026-10-28-representative/selection.json'
OLD_PROGRESS='ec8518f63f78ea7003730d305e6914dcb5d4b5d9ba3eaf82a6e16f957824fe51'
OLD_RUNBOOK='daac6213ebbb2f1c22d141a7b2d2cda6c00893ff4a91b1fefc6033e2425600f3'
OLD_SELECTION='a2908ebf508c3ae6ef1c728d1cda84b6db41d834208e1f5d6b2929bd36654b46'
PREFIX='reports/full-corpus-review/after190-historical-context/snapshots/'
ALLOWED=(
 ('review-independent-legacy-1ccd0d652abebe82',30,'reports/full-corpus-review/independent-phase9-a-review.json','b0d96c5fcc2aef545b5c0535a8e01d03416f7ccb84e9008867df59a7ba94e554',PROGRESS,OLD_PROGRESS,
  ('/policy_bindings/6/path',),PREFIX+'progress-ec8518.json','HISTORICAL_NONLEGAL_PROGRESS_READ_RECEIPT'),
 ('review-independent-legacy-1ccd0d652abebe82',30,'reports/full-corpus-review/independent-phase9-a-review.json','b0d96c5fcc2aef545b5c0535a8e01d03416f7ccb84e9008867df59a7ba94e554',RUNBOOK,OLD_RUNBOOK,
  ('/policy_bindings/0/path',),PREFIX+'wave9-operational-runbook-daac621.md','HISTORICAL_OPERATIONAL_INSTRUCTION_READ_RECEIPT_NOT_GOVERNANCE'),
 ('review-independent-legacy-3f7eb071e35ba44e',31,'reports/full-corpus-review/independent-phase9-b-review.json','9cda0d5da313a5b4a7592affcf8a081afefec515fa10594e8f38429009484ece',SELECTION,OLD_SELECTION,
  tuple(f'/records/{i}/realism_review/nearest_current_default_status/selection_path'for i in range(40)),
  'reports/full-corpus-review/phase9-before-selection.json','HISTORICAL_NEAREST_DEFAULT_COMPARISON_CONTEXT'),
 ('review-independent-legacy-2afb2b3095530da6',33,'reports/full-corpus-review/independent-phase9-d-review.json','d6571f097d57da4aed2ba824f624a842ef96aade83b700209feecd85702a3d4c',SELECTION,OLD_SELECTION,
  ('/input_binding/selection_path',),'reports/full-corpus-review/phase9-before-selection.json','HISTORICAL_ASSIGNED_DEFAULT_INPUT_CONTEXT'),
)

PRIVATE_FIELDS=('source_index', 'source_id', 'official_url', 'source_type', 'extracted_path', 'extracted_sha256', 'original_raw_sha256', 'retained_memo_path', 'retained_memo_sha256')
PRIVATE_ALLOWED=((8,
  'src-b2350e40af92',
  'https://www.mass.gov/doc/pmp-data-submission-dispenser-guide-version-52-pdf/download',
  'OFFICIAL_PRIMARY',
  '/tmp/phase9-b-private/src-b2350e40af92.txt',
  '6f6b10edf7b95393b39f0e708491f9e522c062b5a724dd16f28e21c597ff2006',
  'f3046fbd12822ed8f6d1bf73f61d907a74883db4ef6e67c663decdc6a9edc13b',
  'reports/full-corpus-review/phase9-b-evidence/src-b2350e40af92.memo.json',
  '189bb6143b1d0fff704c28b28dcc0c95f5c4cb9e5b05bf7a2e9b8e8481872a58'),
 (12,
  'src-97192fc77578',
  'https://nabp.pharmacy/wp-content/uploads/2026/02/March-2026-Massachusetts-State-Newsletter.pdf',
  'OFFICIAL_PRIMARY',
  '/tmp/phase9-b-private/src-97192fc77578.txt',
  'e9caf0968bb90b16bef3fe26d0c92f4b79c0da223dc20dc482fcc6541fe619c4',
  'f005b1dbecf9398ea5d98741477bb32c1029b7220a64c96d84f83019f04e6800',
  'reports/full-corpus-review/phase9-b-evidence/src-97192fc77578.memo.json',
  '2676c3b0463fbd44640a70a11f979cbe06a423a44f8454ae4a230ee0e293feb5'),
 (39,
  'nabp-sample',
  'https://nabp.pharmacy/wp-content/uploads/2020/07/MPJE-Sample-Questions.pdf',
  'PUBLIC_OFFICIAL_STYLE_ONLY',
  '/tmp/phase9-b-private/nabp-sample.txt',
  '4ce8167899f4de5df65940b61f024145a446237090ada8e8788d15a1ad9072d1',
  'b8544f403990191075747b231c81cde4449c6eb83333cfb1d9f05b5e1273d30d',
  'reports/full-corpus-review/phase9-b-evidence/nabp-sample.memo.json',
  '0ec8427e3eb12bd109c2439d8232a46bd9455bd477bd8932c7305ddb197b1636'),
 (40,
  'nabp-competency',
  'https://nabp.pharmacy/programs/examinations/mpje/competency-statements/',
  'PUBLIC_OFFICIAL_STYLE_ONLY',
  '/tmp/phase9-b-private/nabp-competency.txt',
  'cb1e0f0f11c8a0e8f8535c3aa4558642bab057651a76d3fdf73a7365b0b263c0',
  '8fbe3eeb412a18a62650dd2f5e9b8b2d72392e21b57b4c04be6762959e2de061',
  'reports/full-corpus-review/phase9-b-evidence/nabp-competency.memo.json',
  '6a4f0c60b8df22eb083b2bdd15d0f01dac7eaf2192e0cc5985c78db3b0af4f7f'))


def require(ok,message):
    if not ok:raise ValueError(message)


def sha(raw):return hashlib.sha256(raw).hexdigest()


def identity(entry):
    return (entry['job_id'],entry['sequence'],entry['report_path'],entry['report_raw_sha256'],
            entry['origin_path'],entry['origin_raw_sha256'],tuple(entry['reference_pointers']),
            entry['retained_path'],entry['reference_semantics'])


def registry(root,bindings,committed):
    raw=committed(root,REGISTRY,bindings)
    require(sha(raw)==REGISTRY_SHA,'Historical context registry raw SHA changed')
    data=json.loads(raw)
    require(data.get('schema_version')=='after190-input-retention/2'and
            data.get('purpose')=='EXACT_HISTORICAL_RECEIPTS_AND_UNRETAINED_PRIVATE_DESCRIPTORS'and
            data.get('canonical_audit')is False and all(type(data.get(k))is int and data[k]==0 for k in
                ('canonical_release_credit','question_audit_credit','new_independent_legal_audit_credit')),
            'Historical context purpose/credit changed')
    require(data.get('previous_registry')=={'path':PREVIOUS_REGISTRY,'raw_sha256':PREVIOUS_REGISTRY_SHA},
            'Original historical receipt registry binding changed')
    old_raw=committed(root,PREVIOUS_REGISTRY,bindings)
    require(sha(old_raw)==PREVIOUS_REGISTRY_SHA and data['entries']==json.loads(old_raw)['entries'],
            'Original four historical receipts changed')
    require([identity(e)for e in data['entries']]==list(ALLOWED),'Historical context scope expanded or changed')
    for e in data['entries']:
        require(e['retained_raw_sha256']==e['origin_raw_sha256']and e['current_binding_override']is False and
                all(type(e.get(k))is int and e[k]==0 for k in ('canonical_release_credit','question_audit_credit')),
                'Historical context cannot override current bindings or create audit credit')
    require(data.get('private_extracted_descriptors')==[private_entry(x)for x in PRIVATE_ALLOWED],
            'Private descriptor scope/index/memo/hash/credit changed')
    require(all(e['public_raw_redistribution']is False and e['runtime_text_bytes_verified']is False and
                all(type(e[k])is int and e[k]==0 for k in ('canonical_release_credit','question_audit_credit'))
                for e in data['private_extracted_descriptors']),'Private descriptor cannot claim verification/credit')
    return data


def private_entry(values):
    return dict(job_id=ALLOWED[2][0],sequence=31,report_path=ALLOWED[2][2],report_raw_sha256=ALLOWED[2][3],
        **dict(zip(PRIVATE_FIELDS,values)),public_raw_redistribution=False,
        public_evidence_mode='copyright-restricted memo only',runtime_text_bytes_verified=False,
        verification_scope='HEAD_RETAINED_MEMO_ONLY; PRIVATE_EXTRACTED_TEXT_SHA_IS_ORIGINAL_WORKER_DECLARATION',
        canonical_release_credit=0,question_audit_credit=0)


def resolve(root,job,report_path,report_sha,origin,old_sha,pointers,bindings,committed):
    """Return a descriptor only for an exact report-local historical reference.

    No match means the caller retains its ordinary current-byte validation.
    Matching a known receipt with changed/missing evidence fails closed.
    """
    matches=[a for a in ALLOWED if (job['job_id'],job['sequence'],report_path,report_sha,origin,old_sha)==a[:6]]
    if not matches:return None
    require(len(matches)==1,'Duplicate historical context scope')
    expected=matches[0]
    require(set(pointers)==set(expected[6]),'Historical context reference location changed; not a primary/current alias')
    entries=registry(root,bindings,committed)['entries']
    entry=next(e for e in entries if identity(e)==expected)
    raw=committed(root,entry['retained_path'],bindings)
    require(sha(raw)==old_sha,'SOURCE_BLOCKED: retained historical input bytes changed or unavailable')
    provenance=entry['preparation_provenance']
    blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    require(provenance['method']=='EXACT_KNOWN_GIT_BLOB_READ_DURING_PREPARATION_ONLY'and
            provenance['source_path']==origin and provenance['source_raw_sha256']==old_sha and
            provenance['source_commit']==('ac5b1819da12f5a8d186d5693801201f413f21d3'if origin==RUNBOOK else job['result']['worker_commit'])and
            provenance['source_git_blob_sha1']==blob and provenance['worker_commit']==job['result']['worker_commit'],
            'Historical input preparation/report worker binding changed')
    return dict(origin_path=origin,origin_raw_sha256=old_sha,retained_path=entry['retained_path'],
        retained_raw_sha256=old_sha,reference_pointers=entry['reference_pointers'],
        reference_semantics=entry['reference_semantics'],registry_path=REGISTRY,
        registry_raw_sha256=REGISTRY_SHA,current_binding_override=False,question_audit_credit=0,canonical_release_credit=0)


def resolve_private(root,job,report_path,report_sha,report,origin,expected_sha,pointers,bindings,committed):
    """Four declared copyrighted full-text descriptors, without reading that text."""
    if (job['job_id'],job['sequence'],report_path,report_sha)!=ALLOWED[2][:4]:return None
    matches=[x for x in PRIVATE_ALLOWED if (origin,expected_sha)==(x[4],x[5])]
    if not matches:return None
    values=matches[0];entry=private_entry(values);index=entry['source_index']
    require(set(pointers)=={f'/sources/{index}/extracted_path'},'Private descriptor index/reference location changed')
    registry(root,bindings,committed)
    source=report['sources'][index]
    require(all(source.get(k)==entry[k]for k in ('source_id','official_url','source_type','extracted_path','extracted_sha256',
                                               'public_raw_redistribution','public_evidence_mode'))and
            source.get('public_raw_redistribution')is False and
            source.get('raw_sha256')==entry['original_raw_sha256']and
            source.get('evidence_path')==entry['retained_memo_path']and
            source.get('evidence_sha256')==entry['retained_memo_sha256'],
            'Private descriptor/source/copyright/memo binding changed')
    raw=committed(root,entry['retained_memo_path'],bindings)
    require(sha(raw)==entry['retained_memo_sha256'],'Private descriptor retained memo SHA changed')
    memo=json.loads(raw)
    require(memo.get('source_id')==entry['source_id']and memo.get('official_url')==entry['official_url']and
            memo.get('raw_sha256')==entry['original_raw_sha256']and memo.get('public_raw_redistribution')is False and
            (entry['source_type']!='PUBLIC_OFFICIAL_STYLE_ONLY'or memo.get('not_legal_proof')is True),
            'Private descriptor retained memo identity/proof scope changed')
    return dict(entry,registry_path=REGISTRY,registry_raw_sha256=REGISTRY_SHA)
