(function (globalScope) {
  "use strict";

  const QUICK_20_QUOTAS = Object.freeze({ 1: 4, 2: 7, 3: 5, 4: 4 });
  const EXAM_TYPES = Object.freeze([
    "QUICK_20",
    "MOCK_120",
    "TOPIC_QUIZ",
    "WRONG_ANSWER_QUIZ",
    "BOOKMARKED_QUIZ",
  ]);

  function getShuffle() {
    if (globalScope.MpjeShuffle) return globalScope.MpjeShuffle;
    if (typeof require === "function") return require("./shuffle.js");
    throw new Error("MpjeShuffle is required");
  }

  function isReleaseUsable(question) {
    return question?.verification_status === "RELEASED" && question?.lifecycle_status === "RELEASED";
  }

  function createQuick20(questions, seed) {
    if (!seed) throw new Error("Quick Exam requires a stable session seed");
    const shuffle = getShuffle();
    const selected = [];
    Object.entries(QUICK_20_QUOTAS).forEach(([area, quota]) => {
      const pool = questions.filter((question) => isReleaseUsable(question) && String(question.area) === area);
      if (pool.length < quota) throw new Error(`Area ${area} requires ${quota} RELEASE-usable questions; found ${pool.length}`);
      selected.push(...shuffle.seededShuffle(pool, `${seed}:area:${area}`).slice(0, quota));
    });
    return shuffle.seededShuffle(selected, `${seed}:question-order`);
  }

  function emptyBreakdown() {
    return { correct: 0, incorrect: 0, attempted: 0, total: 0, percentage: 0 };
  }

  function addBreakdown(target, key, correct) {
    target[key] ||= emptyBreakdown();
    target[key].total += 1;
    target[key].attempted += 1;
    correct ? target[key].correct += 1 : target[key].incorrect += 1;
    target[key].percentage = Math.round((100 * target[key].correct) / target[key].total);
  }

  function buildCompletedSession({ sessionId, examType, sessionSeed, startedAt, completedAt, queue, responses }) {
    if (!EXAM_TYPES.includes(examType)) throw new Error(`Unsupported exam type: ${examType}`);
    if (queue.length !== responses.length || responses.some((response) => !response?.answered)) {
      throw new Error("Every session question must have one completed response");
    }
    const areaBreakdown = {};
    const topicBreakdown = {};
    const difficultyBreakdown = {};
    const answers = queue.map((question, index) => {
      const response = responses[index];
      addBreakdown(areaBreakdown, String(question.area), response.correct);
      addBreakdown(topicBreakdown, question.topic, response.correct);
      addBreakdown(difficultyBreakdown, String(question.difficulty), response.correct);
      return {
        question_id: question.question_id,
        question_content_hash: question.question_content_hash,
        selected_choice_ids: question.question_type === "ORDERED_RESPONSE" ? [...response.order] : [...response.selected].sort(),
        correct: Boolean(response.correct),
      };
    });
    const correct = answers.filter((answer) => answer.correct).length;
    const started = new Date(startedAt);
    const completed = new Date(completedAt);
    const record = {
      session_id: sessionId,
      exam_type: examType,
      session_seed: sessionSeed,
      started_at: started.toISOString(),
      completed_at: completed.toISOString(),
      elapsed_seconds: Math.max(0, Math.round((completed.getTime() - started.getTime()) / 1000)),
      question_ids: queue.map((question) => question.question_id),
      question_content_hashes: Object.fromEntries(queue.map((question) => [question.question_id, question.question_content_hash])),
      answers,
      score: {
        correct,
        incorrect: answers.length - correct,
        total: answers.length,
        percentage: Math.round((100 * correct) / Math.max(1, answers.length)),
      },
      area_breakdown: areaBreakdown,
      topic_breakdown: topicBreakdown,
      difficulty_breakdown: difficultyBreakdown,
      missed_question_ids: answers.filter((answer) => !answer.correct).map((answer) => answer.question_id),
    };
    const error = validateSessionRecord(record);
    if (error) throw new Error(error);
    return record;
  }

  function validateSessionRecord(record) {
    if (!record || typeof record !== "object") return "Session must be an object";
    if (typeof record.session_id !== "string" || !record.session_id) return "Session requires session_id";
    if (!EXAM_TYPES.includes(record.exam_type)) return "Session has unsupported exam_type";
    if (typeof record.session_seed !== "string" || !record.session_seed) return "Session requires session_seed";
    if (!Number.isInteger(record.elapsed_seconds) || record.elapsed_seconds < 0) return "Session elapsed_seconds is invalid";
    if (!Array.isArray(record.question_ids) || !record.question_ids.length) return "Session requires question_ids";
    if (new Set(record.question_ids).size !== record.question_ids.length) return "Session question_ids must be unique";
    if (!record.question_content_hashes || typeof record.question_content_hashes !== "object") return "Session requires question_content_hashes";
    if (!record.question_ids.every((id) => /^[A-Z]{2}-Q-\d{4}$/.test(id) && /^[a-f0-9]{64}$/.test(record.question_content_hashes[id] || ""))) {
      return "Session question IDs and hashes are invalid";
    }
    if (!Array.isArray(record.answers) || record.answers.length !== record.question_ids.length) return "Session answers do not match question count";
    if (!record.score || record.score.total !== record.question_ids.length) return "Session score total is invalid";
    return null;
  }

  const api = { QUICK_20_QUOTAS, EXAM_TYPES, isReleaseUsable, createQuick20, buildCompletedSession, validateSessionRecord };
  globalScope.MpjeSessions = api;
  if (typeof module !== "undefined" && module.exports) module.exports = api;
})(typeof window !== "undefined" ? window : globalThis);
