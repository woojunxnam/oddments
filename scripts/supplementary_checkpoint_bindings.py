"""Exact three supplementary consumers' validated, retained current-HEAD inputs.

This collects actual successful reads, not arbitrary nested path declarations.
Pending queues are bound with zero new credit; parent findings are never edited.
"""
import json
from pathlib import Path

import procedural_secondary_metadata as procedural
import phase11_secondary_metadata as phase11
import phase11_context38_metadata as context38

CONSUMERS=((procedural,'reports/full-corpus-review/procedural-recheck-work-queue.json'),
           (phase11,'reports/full-corpus-review/phase11-procedural-recheck-work-queue.json'),
           (context38,'reports/full-corpus-review/phase11-context38-recheck-work-queue.json'))


def validated_sources(root,primary_records,*,source_bindings=None):
    root=Path(root)
    for consumer,relative in CONSUMERS:
        procedural.require(consumer.STATE==relative,'Supplementary consumer checkpoint scope changed')
    # A retained context disclosure must still reach its strict consumer when
    # its queue is deleted; that deletion may never revive conditioned credit.
    present=[consumer for consumer,relative in CONSUMERS if (root/relative).exists()or
             (consumer is context38 and (root/context38.DISCLOSURE).exists())]
    if not present:return {}
    staged={};read=procedural.committed_reader(root,source_bindings=staged)
    config=json.loads(read('site/practice-expansion/publication.json'))
    paths=['practice_expansion/2026-10-23/candidates/questions.json']+[a['path']for a in config['additional_banks']]
    procedural.require(len(paths)==len(set(paths)),'Repeated supplementary public bank path')
    required={qid for consumer in present for qid in consumer.IDS}
    questions={};collections={}
    for relative in paths:
        procedural.require(relative.startswith('practice_expansion/')and relative.endswith('/questions.json'),
                           'Supplementary question source is outside the published bank scope')
        for record in json.loads(read(relative))['questions']:
            qid=record['question_id']
            if qid in required:
                procedural.require(qid not in questions,'Repeated supplementary current question ID')
                questions[qid]=record;collections[qid]=relative
    procedural.require(set(questions)==required,'Supplementary current question source is incomplete')
    sources={}
    for consumer in present:
        metadata=consumer.load_metadata(root,primary_records,questions,collections,source_bindings=staged)
        for qid,assessment in metadata['assessments'].items():
            procedural.require(qid not in sources,'Repeated supplementary assessed source')
            report=json.loads(read(assessment['report_path'],assessment['report_sha256']))
            row=assessment['record'];legal=row['legal_review'];realism=row['realism_review']
            negative=(legal['verdict']in {'MINOR_EDIT','MAJOR_REWRITE','HOLD','DELETE','REPLACE'}or
                      legal['existing_answer_correct']in {'NO','AMBIGUOUS','NOT_ASSESSED'}or
                      realism['verdict']in {'FAIL','MINOR_EDIT','MAJOR_REWRITE'})
            sources[qid]=dict(source_path=assessment['report_path'],source_sha256=assessment['report_sha256'],
                              record_sha256=row['record_sha256'],reviewed_at=report.get('reviewed_at'),
                              negative=negative,supplementary_only=True,does_not_override_primary=True,
                              canonical_release_credit=0)
    procedural.retained_result(None,staged,source_bindings)
    return sources
