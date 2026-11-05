(function (globalScope) {
  "use strict";

  const QUESTION_ID = /^MA-Q-\d{4}$/;
  const CONTENT_HASH = /^[a-f0-9]{64}$/;
  const SET_ID = /^[a-z][a-z0-9-]{1,63}$/;
  const NOTE_ID = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
  const PRIVATE_REFERENCE = /\bIMG[_-]?\d{4}\b|\bMA-PRIVATE-REPAIR-\d+\b|(?:drive|docs)\.google\.com/i;
  const deliveryContexts = new WeakMap();

  function requireValue(condition, message) {
    if (!condition) throw new Error(message);
  }

  function onlyKeys(value, allowed) {
    return value && typeof value === "object" && !Array.isArray(value)
      && Object.keys(value).every((key) => allowed.includes(key));
  }

  function questionIndex(payload, isReleaseUsable) {
    requireValue(typeof isReleaseUsable === "function", "승인 상태를 확인할 수 없습니다.");
    requireValue(payload?.meta?.release_status === "RELEASE_AVAILABLE"
      && payload.meta.development_fixture_mode === false && Array.isArray(payload.questions),
    "공개 승인 문제은행을 확인할 수 없습니다.");
    const index = new Map();
    for (const question of payload.questions) {
      requireValue(QUESTION_ID.test(question?.question_id || "") && !index.has(question.question_id),
        "문항 식별자를 확인할 수 없습니다.");
      requireValue(CONTENT_HASH.test(question.question_content_hash || ""),
        "문항 버전을 확인할 수 없습니다.");
      index.set(question.question_id, question);
    }
    return index;
  }

  function validateDeliveryHolds(payload, manifest, isReleaseUsable) {
    const index = questionIndex(payload, isReleaseUsable);
    requireValue(manifest?.schema_version === "canonical-delivery-holds/1"
      && manifest.status === "DELIVERY_HOLD_NOT_CANONICAL_CHANGE"
      && onlyKeys(manifest, ["schema_version", "status", "reviews", "holds"])
      && Array.isArray(manifest.reviews) && Array.isArray(manifest.holds),
    "문항 보류 안내를 확인할 수 없어 자동 학습을 중지했습니다.");
    requireValue(!PRIVATE_REFERENCE.test(JSON.stringify(manifest)), "공개 보류 안내에 허용되지 않은 비공개 참조가 있습니다.");
    const reviews = new Map();
    for (const review of manifest.reviews) {
      requireValue(onlyKeys(review, ["id", "url", "source_sha256", "reviewed_date"])
        && /^[A-Z][A-Z0-9-]+$/.test(review?.id || "") && !reviews.has(review.id)
        && /^https:\/\/github\.com\/woojunxnam\/oddments\/blob\/(?:main|[a-f0-9]{40})\/reports\/[A-Za-z0-9/_-]+\.json$/.test(review.url || "")
        && CONTENT_HASH.test(review.source_sha256 || "") && /^\d{4}-\d{2}-\d{2}$/.test(review.reviewed_date || ""),
      "문항 보류 안내의 검토 기록을 확인해야 합니다.");
      reviews.set(review.id, Object.freeze({ ...review }));
    }
    const holds = new Map();
    for (const hold of manifest.holds) {
      requireValue(onlyKeys(hold, ["question_id", "question_content_hash", "category", "reason", "review_reason", "review_id"])
        && QUESTION_ID.test(hold?.question_id || "") && !holds.has(hold.question_id)
        && CONTENT_HASH.test(hold.question_content_hash || "")
        && ["LEGAL_HOLD", "REALISM_REVIEW_REQUIRED", "EDITORIAL_HOLD"].includes(hold.category)
        && typeof hold.reason === "string" && hold.reason.trim()
        && typeof hold.review_reason === "string" && hold.review_reason.trim()
        && reviews.has(hold.review_id), "문항 보류 안내에 확인이 필요한 항목이 있습니다.");
      const question = index.get(hold.question_id);
      requireValue(question && question.question_content_hash === hold.question_content_hash,
        "보류된 문항이 변경되어 안내를 다시 확인해야 합니다. 확인 전에는 자동 학습을 제공하지 않습니다.");
      holds.set(hold.question_id, Object.freeze({ ...hold, review: reviews.get(hold.review_id) }));
    }
    const context = Object.freeze({ heldCount: holds.size });
    deliveryContexts.set(context, holds);
    return context;
  }

  function deliveryMap(context) {
    const holds = context && deliveryContexts.get(context);
    requireValue(holds, "문항 보류 안내를 확인할 때까지 자동 학습을 제공하지 않습니다.");
    return holds;
  }

  function getDeliveryHold(question, context) {
    const hold = deliveryMap(context).get(question?.question_id);
    if (!hold) return null;
    if (hold.question_content_hash !== question.question_content_hash) {
      return { ...hold, reason: "문항이 변경되어 검토를 마칠 때까지 학습·채점을 보류합니다.", stale: true };
    }
    return hold;
  }

  function isDeliveryUsable(question, isReleaseUsable, context) {
    deliveryMap(context);
    return isReleaseUsable(question) && !getDeliveryHold(question, context);
  }

  function holdError(hold) {
    const error = new Error("이 문항의 학습·채점을 보류합니다. " + hold.reason + " 기존 학습 기록은 유지됩니다.");
    error.deliveryHold = hold;
    return error;
  }

  function validateManifest(payload, manifest, isReleaseUsable, delivery) {
    deliveryMap(delivery);
    const index = questionIndex(payload, isReleaseUsable);
    requireValue(manifest?.schema_version === "verified-law-collections/1"
      && manifest.selection_basis === "EXISTING_CANONICAL_RELEASED_CONTENT"
      && onlyKeys(manifest, ["schema_version", "selection_basis", "sets"])
      && Array.isArray(manifest.sets) && manifest.sets.length > 0,
    "주제별 학습 목록을 확인할 수 없습니다.");
    requireValue(!PRIVATE_REFERENCE.test(JSON.stringify(manifest)),
      "공개 학습 목록에 허용되지 않은 비공개 참조가 있습니다.");
    const seen = new Set();
    return manifest.sets.map((set) => {
      requireValue(onlyKeys(set, ["id", "title", "description", "questions", "notes"])
        && SET_ID.test(set?.id || "") && !seen.has(set.id), "학습 묶음 식별자를 확인할 수 없습니다.");
      seen.add(set.id);
      requireValue(typeof set.title === "string" && set.title.trim()
        && typeof set.description === "string" && set.description.trim()
        && Array.isArray(set.questions) && set.questions.length > 0,
      "학습 묶음의 내용을 확인할 수 없습니다.");
      const ids = new Set();
      const questions = set.questions.map((reference) => {
        requireValue(onlyKeys(reference, ["question_id", "question_content_hash"])
          && QUESTION_ID.test(reference?.question_id || "") && !ids.has(reference.question_id),
          "학습 묶음에 잘못되거나 중복된 문항이 있습니다.");
        ids.add(reference.question_id);
        const question = index.get(reference.question_id);
        requireValue(question && isReleaseUsable(question), "승인되지 않은 문항은 학습 묶음에서 열 수 없습니다.");
        const hold = getDeliveryHold(question, delivery);
        if (hold) throw holdError(hold);
        requireValue(CONTENT_HASH.test(reference.question_content_hash || "")
          && reference.question_content_hash === question.question_content_hash,
        "문항이 갱신되어 이 학습 묶음을 확인해야 합니다.");
        return question;
      });
      requireValue(Array.isArray(set.notes) && set.notes.length > 0 && set.notes.every((note) =>
        onlyKeys(note, ["chapter_id", "unit_id", "title"])
        && NOTE_ID.test(note?.chapter_id || "") && NOTE_ID.test(note?.unit_id || "")
        && typeof note.title === "string" && note.title.trim()),
      "연결된 노트를 확인할 수 없습니다.");
      return { ...set, questionIds: questions.map((question) => question.question_id), resolvedQuestions: questions };
    });
  }

  function resolveSelection(payload, manifest, search, isReleaseUsable, delivery) {
    deliveryMap(delivery);
    const parameters = new URLSearchParams(search);
    const requested = parameters.has("set") || parameters.has("question");
    if (!requested) return { requested: false, questionIds: null, initialQuestionId: null, set: null };
    requireValue(parameters.getAll("set").length <= 1 && parameters.getAll("question").length <= 1,
      "학습 링크의 선택 조건이 중복되었습니다.");
    const requestedSet = parameters.get("set");
    const requestedQuestion = parameters.get("question");
    if (parameters.has("set")) requireValue(SET_ID.test(requestedSet || ""), "학습 묶음 링크를 확인해 주세요.");
    if (parameters.has("question")) requireValue(QUESTION_ID.test(requestedQuestion || ""), "문항 링크를 확인해 주세요.");
    const index = questionIndex(payload, isReleaseUsable);
    if (requestedQuestion) {
      const hold = getDeliveryHold(index.get(requestedQuestion), delivery);
      if (hold) throw holdError(hold);
    }
    const sets = validateManifest(payload, manifest, isReleaseUsable, delivery);
    const selectedSet = requestedSet ? sets.find((set) => set.id === requestedSet) : null;
    requireValue(!requestedSet || selectedSet, "요청한 학습 묶음을 사용할 수 없습니다.");
    if (requestedQuestion) {
      const question = index.get(requestedQuestion);
      requireValue(question && isReleaseUsable(question), "요청한 문항은 현재 공개 승인 목록에 없습니다.");
      requireValue(!selectedSet || selectedSet.questionIds.includes(requestedQuestion),
        "요청한 문항은 선택한 학습 묶음에 포함되지 않습니다.");
    }
    return {
      requested: true,
      questionIds: selectedSet ? [...selectedSet.questionIds] : [requestedQuestion],
      initialQuestionId: requestedQuestion || null,
      set: selectedSet,
    };
  }

  const api = { validateDeliveryHolds, getDeliveryHold, isDeliveryUsable, validateManifest, resolveSelection };
  globalScope.MpjeCollections = api;
  if (typeof module !== "undefined" && module.exports) module.exports = api;
})(typeof window !== "undefined" ? window : globalThis);
