"""Exact note-to-practice navigation counts, without a legal-review assertion."""
from __future__ import annotations

from urllib.parse import quote


def build_note_practice_index(questions, recommended_ids, notes):
    """Count each question once per cited unit; never infer a link from its topic."""
    units = {u['id']: (chapter, u) for chapter in notes['chapters'] for u in chapter['units']}
    question_ids = [q['question_id'] for q in questions]
    if len(question_ids) != len(set(question_ids)):
        raise ValueError('Duplicate question ID in note-practice index')
    recommended = set(recommended_ids)
    if not recommended <= set(question_ids):
        raise ValueError('Unknown recommendation in note-practice index')
    linked = {uid: [] for uid in units}
    for question in questions:
        for uid in {e['unit_id'] for e in question['note_evidence']}:
            if uid not in units:
                raise ValueError('Unknown note unit in practice evidence: ' + uid)
            linked[uid].append(question)
    result = {}
    for uid, (chapter, unit) in units.items():
        rows = linked[uid]
        selected = [q for q in rows if q['question_id'] in recommended]
        result[uid] = dict(
            title=unit['title'], chapter_id=chapter['id'],
            total=len(rows), recommended=len(selected),
            families=len({q['family_id'] for q in rows}),
            recommended_families=len({q['family_id'] for q in selected}),
            note_url='../notes/#chapter/' + quote(chapter['id'], safe='') + '/' + quote(uid, safe=''),
            practice_url='../practice-expansion/?note=' + quote(uid, safe=''),
        )
    return result
