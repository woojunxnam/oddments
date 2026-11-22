/* Exact, explicitly archived question-bank compatibility. Never rewrites saved answers. */
(() => {
  'use strict';
  const validQuestion = (q, id) => q && q.id === id && typeof q.stem === 'string' &&
    Array.isArray(q.choices) && q.choices.length === 4 &&
    q.choices.every(c => c && typeof c.text === 'string' && typeof c.why === 'string') &&
    Array.isArray(q.correct) && q.correct.length > 0 &&
    q.correct.every(k => ['A', 'B', 'C', 'D'].includes(k));

  function create(manifest, byId) {
    const registry = window.MPJE_CH30_BANK_REVISIONS;
    const target = registry?.targets?.[manifest?.schema];
    const targetMatches = !!target && target.currentSignature === manifest?.bankSignature &&
      Array.isArray(target.priorSignatures) && Array.isArray(target.archivedQuestionIds) &&
      Array.isArray(target.excludedQuestionIds);
    const archived = new Set(targetMatches ? target.archivedQuestionIds : []);
    const excluded = new Set(targetMatches ? target.excludedQuestionIds : []);
    const idsFor = s => manifest?.forms?.[s?.form];
    const snapshot = (s, id) => target?.snapshotsBySignature?.[s.bankSignature]?.[id] || registry?.snapshots?.[id];
    function canUse(s) {
      if (!s || !Array.isArray(idsFor(s)) || !idsFor(s).every(id => byId.has(id))) return false;
      if (s.bankSignature === manifest?.bankSignature) return true;
      // A future manifest cannot inherit old permissions, and a partial archive cannot be scored.
      return targetMatches && target.priorSignatures.includes(s.bankSignature) &&
        [...archived].every(id => byId.has(id) && validQuestion(snapshot(s, id), id)) &&
        [...excluded].every(id => archived.has(id));
    }
    const isHistorical = s => canUse(s) && s.bankSignature !== manifest.bankSignature;
    function question(s, id) {
      if (!canUse(s) || !idsFor(s).includes(id)) return null;
      return isHistorical(s) && archived.has(id) ? snapshot(s, id) : byId.get(id);
    }
    const excludedIds = s => isHistorical(s) ? idsFor(s).filter(id => excluded.has(id)) : [];
    const reason = (s, id) => excludedIds(s).includes(id) ?
      target.reasons?.[id] || 'This earlier question was corrected and is excluded from readiness evidence.' : '';
    function changed(s, id) {
      return isHistorical(s) && archived.has(id) &&
        JSON.stringify(question(s, id)) !== JSON.stringify(byId.get(id));
    }
    function describe(s) {
      const ids = excludedIds(s);
      return {bankSignature: s?.bankSignature || null, currentBankSignature: manifest?.bankSignature || null,
        historical: isHistorical(s), originalRawGradePreserved: isHistorical(s),
        excludedQuestionIds: ids, readinessEligibleTotal: canUse(s) ? idsFor(s).length - ids.length : null,
        exclusionReasons: Object.fromEntries(ids.map(id => [id, reason(s, id)]))};
    }
    return Object.freeze({canUse, isHistorical, question, excludedIds, reason, changed, describe});
  }
  window.MPJE_CH30_VERSION_HISTORY = Object.freeze({create});
})();
