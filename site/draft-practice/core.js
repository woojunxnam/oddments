/* Public draft practice is a separate delivery channel, never a canonical release. */
(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  else root.MpjeDraftPractice = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";
  const statuses = new Set(["AUDIT_PENDING", "LEGAL_HOLD", "DUPLICATE_DEFERRED"]);
  const hash = /^[a-f0-9]{64}$/;
  const id = /^MA-DRAFT33-\d{3}$/;
  const text = value => typeof value === "string" && value.trim().length > 0;
  const exactKeys = (value, keys) => value && typeof value === "object" && !Array.isArray(value)
    && Object.keys(value).sort().join("|") === [...keys].sort().join("|");
  function requireValue(value, message) { if (!value) throw new Error(message); }
  function stable(value) {
    if (Array.isArray(value)) return "[" + value.map(stable).join(",") + "]";
    if (value && typeof value === "object") return "{" + Object.keys(value).sort().map(k => JSON.stringify(k) + ":" + stable(value[k])).join(",") + "}";
    return JSON.stringify(value);
  }
  function semantic(question) {
    const { content_hash, ...body } = question;
    return stable(body);
  }
  function validate(payload) {
    requireValue(exactKeys(payload, ["schema_version", "edition", "publication_status", "question_count", "gradable_count", "hold_count", "canonical_released_question_count", "publication_date", "authorship", "questions"])
      && payload.schema_version === "mpje-draft-practice/1" && payload.edition === "2026-11-06.draft33"
      && payload.publication_status === "PUBLISHED_DRAFT_PRACTICE" && payload.canonical_released_question_count === 0
      && payload.question_count === 33 && payload.gradable_count === 32 && payload.hold_count === 1
      && payload.publication_date === "2026-11-06" && text(payload.authorship)
      && Array.isArray(payload.questions) && payload.questions.length === 33, "초안 묶음의 버전·공개 상태를 확인할 수 없습니다.");
    const seen = new Set();
    for (const q of payload.questions) {
      requireValue(exactKeys(q, ["id", "title", "stem", "choices", "proposed_key", "core_ko", "analysis_ko", "authorities", "review_status", "scoring_policy", "blockers_ko", "content_hash"])
        && id.test(q.id) && !seen.has(q.id) && text(q.title) && text(q.stem) && text(q.core_ko)
        && statuses.has(q.review_status) && hash.test(q.content_hash), "문항 식별자 또는 초안 상태가 올바르지 않습니다.");
      seen.add(q.id);
      requireValue(Array.isArray(q.choices) && q.choices.length === 4
        && q.choices.every((c, i) => exactKeys(c, ["id", "text"]) && c.id === "ABCD"[i] && text(c.text))
        && Array.isArray(q.proposed_key) && q.proposed_key.length === 1 && "ABCD".includes(q.proposed_key[0]) && q.proposed_key[0].length === 1
        && exactKeys(q.analysis_ko, [..."ABCD"]) && Object.values(q.analysis_ko).every(text), "선택지·제안 답·한국어 해설을 확인해 주세요.");
      requireValue(q.scoring_policy === (q.review_status === "LEGAL_HOLD" ? "NO_GRADE" : "PROPOSED_KEY")
        && Array.isArray(q.blockers_ko) && q.blockers_ko.length > 0 && q.blockers_ko.every(text), "보류 문항의 채점 정책이 일치하지 않습니다.");
      requireValue(Array.isArray(q.authorities) && q.authorities.length > 0 && q.authorities.every(a => {
        if (!exactKeys(a, ["section", "url", "checked", "effective_limit"]) || ![a.section, a.checked, a.effective_limit].every(text)) return false;
        try { const url = new URL(a.url); return url.protocol === "https:" && !url.username && !url.password && (url.hostname.endsWith(".gov") || url.hostname === "mass.gov" || url.hostname.endsWith(".mass.gov")); }
        catch (_) { return false; }
      }), "공식 출처 링크와 확인 한계를 확인할 수 없습니다.");
    }
    requireValue(payload.questions.filter(q => q.scoring_policy === "NO_GRADE").length === 1
      && payload.questions.find(q => q.id === "MA-DRAFT33-010")?.review_status === "LEGAL_HOLD", "법규·시점 보류 문항의 상태가 변경되었습니다.");
    return payload;
  }
  async function verifyHashes(payload, subtle) {
    for (const q of payload.questions) {
      const bytes = await subtle.digest("SHA-256", new TextEncoder().encode(semantic(q)));
      const actual = [...new Uint8Array(bytes)].map(x => x.toString(16).padStart(2, "0")).join("");
      requireValue(actual === q.content_hash, "문항 내용과 버전이 다릅니다. 새로고침 후 다시 시도해 주세요.");
    }
    return payload;
  }
  function grade(question, pick) {
    requireValue(question.choices.some(c => c.id === pick), "답을 하나 선택해 주세요.");
    if (question.review_status === "LEGAL_HOLD" || question.scoring_policy === "NO_GRADE") return { status: "HOLD", matches: null };
    requireValue(question.scoring_policy === "PROPOSED_KEY", "채점할 수 있는 초안 상태가 아닙니다.");
    return { status: "PROPOSED_KEY", matches: question.proposed_key[0] === pick };
  }
  function emptyRecord(question) { return { id: question.id, content_hash: question.content_hash, pick: "", checked: false, bookmarked: false, note: "" }; }
  function validateRecords(records, questions) {
    requireValue(Array.isArray(records) && records.length <= questions.length, "백업의 문항 수가 올바르지 않습니다.");
    const known = new Map(questions.map(q => [q.id, q])); const result = Object.create(null);
    for (const r of records) {
      const q = known.get(r?.id);
      requireValue(exactKeys(r, ["id", "content_hash", "pick", "checked", "bookmarked", "note"])
        && q && !Object.hasOwn(result, r.id) && r.content_hash === q.content_hash
        && (r.pick === "" || q.choices.some(c => c.id === r.pick))
        && typeof r.checked === "boolean" && (!r.checked || r.pick !== "")
        && typeof r.bookmarked === "boolean" && typeof r.note === "string" && r.note.length <= 10000,
      "문항 ID·버전·검토 기록이 일치하지 않습니다. 기존 기록은 변경하지 않았습니다.");
      result[r.id] = { ...r };
    }
    return result;
  }
  function summary(questions, records) {
    let answered = 0, matched = 0, mismatched = 0, held = 0;
    for (const q of questions) {
      const r = records[q.id];
      if (!r?.checked || r.content_hash !== q.content_hash) continue;
      answered++;
      const result = grade(q, r.pick);
      if (result.status === "HOLD") held++;
      else if (result.matches) matched++;
      else mismatched++;
    }
    return { answered, matched, mismatched, held };
  }
  return Object.freeze({ validate, verifyHashes, semantic, grade, emptyRecord, validateRecords, summary });
});
