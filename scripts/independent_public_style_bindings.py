"""Bind one immutable report's three public-style descriptors to its own memo.

Only retained memo/metadata bytes are verified. Original raw/text SHA values
remain historical retrieval identifiers, never assertions of retained payloads.
The projection is temporary validator input, not a changed review or new credit.
"""
import copy
from datetime import datetime
import json
import re

from notes_published15_closure import committed, require, snapshotted

REPORT_PATH='reports/full-corpus-review/independent-phase13-a-review.json'
REPORT_SHA256='94f6f2dd24890968a7ff66e8032f2032e8774221085fe9b09bd486997f685603'
EVIDENCE_PREFIX='reports/full-corpus-review/phase13-a-evidence/'
MEMO_PATH=EVIDENCE_PREFIX+'public-style-own-memo.json'
PUBLIC_STYLE_URLS={
    'nabpcompetency':'https://nabp.pharmacy/programs/examinations/mpje/competency-statements/',
    'nabpformat':'https://nabp.pharmacy/programs/examinations/mpje/take-the-mpje-exam/',
    'nabpsample':'https://nabp.pharmacy/wp-content/uploads/2020/07/MPJE-Sample-Questions.pdf',
}


def timestamp(value):
    require(isinstance(value,str),'Public-style timestamp is missing')
    require(datetime.fromisoformat(value.replace('Z','+00:00')).tzinfo is not None,
            'Public-style timestamp requires timezone')


def validation_sources(root,report,*,source_bindings):
    """Project only sources of the exact report bound by the strict consumer.

    Other reports retain their original descriptors and must satisfy the usual
    byte validator, including its rejection of incomplete government sources.
    """
    records=report.get('records',[])
    bindings=[source_bindings.get(r['question_id'],{})for r in records]
    if not any(b.get('source_path')==REPORT_PATH for b in bindings):return copy.deepcopy(report['sources'])
    return _bound_sources(root,report,bindings)


@snapshotted
def _bound_sources(root,report,bindings):
    require(bindings and all(b.get('source_path')==REPORT_PATH and
            b.get('source_sha256')==REPORT_SHA256 for b in bindings),
            'Public-style report requires exact integrated source bindings')
    require(json.loads(committed(root,REPORT_PATH,REPORT_SHA256))==report,
            'Public-style report differs from its exact integrated HEAD bytes')
    sources=copy.deepcopy(report['sources'])
    require(report.get('public_style_memo_path')==MEMO_PATH,
            'Public-style parent memo path changed')
    memo_sha=report['public_style_memo_sha256']
    require(isinstance(memo_sha,str) and re.fullmatch('[0-9a-f]{64}',memo_sha),
            'Public-style parent memo SHA is invalid')
    memo=json.loads(committed(root,MEMO_PATH,memo_sha))
    require(memo.get('reviewed_at')==report.get('completed_at') and
            isinstance(memo.get('own_abstract_memo_ko'),str) and bool(memo['own_abstract_memo_ko'].strip()),
            'Public-style memo attribution/own abstract is missing or changed')
    timestamp(memo['reviewed_at'])
    require(memo['reviewed_at'].split('T')[0]==report.get('reviewed_at'),
            'Public-style report review date differs from its memo timestamp')
    descriptors=memo.get('official_retrieval_metadata')
    require(isinstance(descriptors,list) and all(isinstance(s,dict)for s in descriptors) and
            len(descriptors)==len(PUBLIC_STYLE_URLS) and
            {s.get('source_id')for s in descriptors}==set(PUBLIC_STYLE_URLS),
            'Public-style memo needs the exact three unique retrieval descriptors')
    selected=[s for s in sources if s.get('source_id')in PUBLIC_STYLE_URLS]
    require(len(selected)==len(PUBLIC_STYLE_URLS) and
            {s['source_id']for s in selected}==set(PUBLIC_STYLE_URLS),
            'Public-style report descriptor scope/uniqueness changed')
    for source in selected:
        sid=source['source_id'];url=PUBLIC_STYLE_URLS[sid]
        require(sum(s==source for s in descriptors)==1,
                'Public-style source must occur exactly once unchanged in its parent memo')
        require(source.get('official_url')==source.get('final_url')==url and
                source.get('raw_path') is None and 'raw_path'in source and
                source.get('text_path') is None and 'text_path'in source and
                source.get('reviewed_at')==memo['reviewed_at'] and source.get('status')==200,
                'Public-style URL/retention/review timestamp changed')
        for key in ('raw_sha256','text_sha256','metadata_sha256'):
            require(isinstance(source.get(key),str) and re.fullmatch('[0-9a-f]{64}',source[key]),
                    'Public-style retrieval SHA identifier is invalid')
        metadata_path=EVIDENCE_PREFIX+'sources/'+sid+'.meta.json'
        require(source.get('metadata_path')==metadata_path,'Public-style metadata path changed')
        metadata=json.loads(committed(root,metadata_path,source['metadata_sha256']))
        required={'source_id','official_url','final_url','status','content_type','retrieved_at',
                  'method','raw_sha256','text_sha256','raw_path','text_path','retention'}
        require(required<=set(metadata) and all(k in source and source[k]==v for k,v in metadata.items()),
                'Public-style retained metadata differs from its report descriptor')
        timestamp(metadata['retrieved_at'])
        source.pop('raw_path');source.pop('text_path')
        source.update(evidence_path=MEMO_PATH,evidence_sha256=memo_sha,
            public_raw_redistribution=False,
            public_evidence_mode='RETAINED_OWN_PUBLIC_STYLE_MEMO_ONLY',
            public_style_parent_binding=dict(source_path=REPORT_PATH,source_sha256=REPORT_SHA256,
                memo_path=MEMO_PATH,memo_sha256=memo_sha,
                metadata_path=metadata_path,metadata_sha256=source['metadata_sha256'],
                raw_payload_verified=False,extracted_text_verified=False,
                legal_authority_credit=0,question_audit_credit=0,canonical_release_credit=0))
    return sources
