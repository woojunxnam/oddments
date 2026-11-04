"use strict";

(() => {
  const originalFetch = window.fetch.bind(window);
  const QUESTIONS_PATH = "generated/questions.json";
  const ALLOWLIST_PATH = "generated/preview_allowlist.json";

  window.fetch = async (input, init) => {
    const url = typeof input === "string" ? input : input?.url || "";
    if (!url.endsWith(QUESTIONS_PATH)) return originalFetch(input, init);

    const [questionsResponse, allowlistResponse] = await Promise.all([
      originalFetch(input, init),
      originalFetch(ALLOWLIST_PATH, { cache: "no-store" }),
    ]);

    if (!questionsResponse.ok || !allowlistResponse.ok) return questionsResponse;

    const payload = await questionsResponse.json();
    const allowlist = await allowlistResponse.json();
    const allowed = new Set(allowlist.question_ids || []);
    const filteredQuestions = (payload.questions || []).filter((question) => allowed.has(question.question_id));

    payload.questions = filteredQuestions;
    payload.meta = {
      ...(payload.meta || {}),
      question_count: filteredQuestions.length,
      development_fixture_mode: true,
      preview_mode: allowlist.mode || "GPT_AUDITED_PREVIEW",
      preview_notice: allowlist.notice || "",
    };

    return new Response(JSON.stringify(payload), {
      status: 200,
      headers: { "Content-Type": "application/json; charset=utf-8" },
    });
  };
})();
