"""Exactly four prior-key-exposure retries; independent of the 91 realism-only rows."""
from urllib.parse import urlsplit
import re

LEGAL_IDS=('MA-RW-0051','MA-RW-0061','MA-RW-0062','MA-RW-0064')


def require(test,message):
    if not test:raise ValueError(message)


def bind_parent(uid,row):
    if uid not in LEGAL_IDS:return None
    legal=row['legal_review']
    require(legal.get('verdict')=='HOLD'and legal.get('existing_answer_correct')=='NOT_ASSESSED'and
        'PROCEDURAL_PRIOR_SOURCE_CONCLUSION_EXPOSURE'in legal.get('blocker',''),
        'Fixed4 requires the original procedural-exposure HOLD/NOT_ASSESSED')
    return {'verdict':'HOLD','existing_answer_correct':'NOT_ASSESSED','blocker':legal['blocker']}


def validate_legal(row,question,read,prefix,completed):
    from realism_completion_review import moment,nonempty,sha
    legal=row['legal_review'];key=legal.get('existing_answer_correct');verdict=legal.get('verdict')
    require(row['question_id']in LEGAL_IDS,'Legal retry is bounded to fixed4')
    require(key in {'YES','NO','AMBIGUOUS','NOT_ASSESSED'}and verdict in {'KEEP','MINOR_EDIT','MAJOR_REWRITE','HOLD','DELETE'},'Unknown legal4 assessment')
    require(legal.get('stored_key')==question['correct_choice_ids']and legal.get('question_type')==question['question_type']and
        legal.get('polarity')in {'CORRECT','INCORRECT'}and nonempty(legal.get('finding_ko')),'Actual stored key/type/polarity/finding required')
    require(legal.get('prior_conclusions_read')is False and legal.get('hidden_truth_read')is False,'Exposure cannot gain a new key assessment')
    expected=legal.get('independently_expected_key');require(isinstance(expected,list)and len(expected)==len(set(expected))and
        set(expected)<={c['id']for c in question['choices']},'Independent expected key must use actual options')
    if key=='YES':require(expected==question['correct_choice_ids'],'YES requires the complete independently expected stored combination')
    if key=='NO':require(expected!=question['correct_choice_ids'],'NO must identify a distinct independent combination')
    if key=='NOT_ASSESSED':require(verdict=='HOLD'and not expected,'Unassessed remains HOLD with no invented key')
    explanation=legal.get('original_explanation_review',{});options=[c['id']for c in question['choices']]
    require(explanation.get('core_reasoning_read')is True and explanation.get('all_choice_rationales_read')==options and
        explanation.get('learning_boundary_read')is True and nonempty(explanation.get('finding_ko')),'Complete Korean core/each-rationale review required')
    authorities=legal.get('authorities',[]);require(isinstance(authorities,list)and(key=='NOT_ASSESSED'or bool(authorities)),'Assessed legal4 needs official primary evidence')
    paths=[];ids=set()
    for authority in authorities:
        sid=authority['source_id'];require(sid not in ids,'Repeated legal authority');ids.add(sid)
        url=urlsplit(authority.get('official_url',''));require(url.scheme=='https'and url.hostname and
            (url.hostname.endswith('.gov')or url.hostname=='mass.gov'),'Only official government legal primary sources')
        require(nonempty(authority.get('exact_section'))and nonempty(authority.get('effective_date_or_version_basis'))and
            authority.get('law_checked_date')==completed.date().isoformat(),'Exact section/version/effect-date limitation and review date required')
        for field,hashfield in [('raw_path','raw_sha256'),('text_path','text_sha256'),('metadata_path','metadata_sha256')]:
            path=authority[field];require(path.startswith(prefix),'Legal evidence must stay in own prefix')
            require(re.fullmatch('[0-9a-f]{64}',authority.get(hashfield,'')),'Legal raw/text/meta SHA required')
            read(path,authority[hashfield]);paths.append(path)
        import json
        meta=json.loads(read(authority['metadata_path'],authority['metadata_sha256']))
        require(meta.get('official_url')==authority['official_url']and meta.get('raw_sha256')==authority['raw_sha256']and
            meta.get('text_sha256')==authority['text_sha256']and meta.get('raw_path')==authority['raw_path']and
            meta.get('text_path')==authority['text_path'],'Official source metadata/raw/text binding changed')
        fetched=moment(meta['retrieved_at']);read_at=moment(meta['read_at'])
        require(fetched<=read_at<=completed and fetched.date()==read_at.date()==completed.date(),'Actual legal retrieval/read/review chronology required')
        require(meta.get('status')==200 and nonempty(meta.get('method'))and
            meta.get('document_identity_status')=='OFFICIAL_TARGET_PROVISIONS_DIRECTLY_READ','Legal key credit requires actual official target document read')
    choices=legal.get('per_choice_findings',[])
    require(len(choices)==len(options)and{c['choice_id']for c in choices}==set(options),'Every original option requires a legal finding')
    by_id={c['id']:c for c in question['choices']}
    for choice in choices:
        require(choice.get('option_text_sha256')==sha(by_id[choice['choice_id']]['text'].encode())and
            nonempty(choice.get('finding_ko')),'Exact option hash and individual Korean finding required')
        require(choice.get('proposition_supported')is None or type(choice['proposition_supported'])is bool,'Unknown option assessment')
        refs=choice.get('authority_refs',[])
        require(isinstance(refs,list)and set(refs)<=ids and(key=='NOT_ASSESSED'or bool(refs)),'Every assessed option needs exact official authority references')
    return paths
