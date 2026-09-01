"use strict";

const DATA_URL = "generated/questions.json";
const GUIDE_URL = "generated/study_guide.json";
const requestedSeed = new URLSearchParams(window.location.search).get("seed");
let sessionCounter = 0;

const elements = {
  fixtureWarning: document.querySelector("#fixture-warning"), dataSummary: document.querySelector("#data-summary"),
  areaFilter: document.querySelector("#area-filter"), topicFilter: document.querySelector("#topic-filter"),
  difficultyFilter: document.querySelector("#difficulty-filter"), typeFilter: document.querySelector("#type-filter"),
  drugFilter: document.querySelector("#drug-filter"), emptyState: document.querySelector("#empty-state"),
  questionPanel: document.querySelector("#question-panel"), questionPosition: document.querySelector("#question-position"),
  questionArea: document.querySelector("#question-area"), questionDifficulty: document.querySelector("#question-difficulty"),
  questionType: document.querySelector("#question-type"), questionStem: document.querySelector("#question-stem"),
  orderedHelp: document.querySelector("#ordered-help"), choiceForm: document.querySelector("#choice-form"),
  selectedOrder: document.querySelector("#selected-order"), checkAnswer: document.querySelector("#check-answer"),
  revealAnswer: document.querySelector("#reveal-answer"), resetOrder: document.querySelector("#reset-order"),
  previousQuestion: document.querySelector("#previous-question"), nextQuestion: document.querySelector("#next-question"),
  result: document.querySelector("#result"), explanation: document.querySelector("#explanation"),
  correctAnswer: document.querySelector("#correct-answer"), coreReasoning: document.querySelector("#core-reasoning"),
  choiceAnalysis: document.querySelector("#choice-analysis"), drugCheckSection: document.querySelector("#drug-check-section"),
  drugChecks: document.querySelector("#drug-checks"), relatedFacts: document.querySelector("#related-facts"),
  mpjeTrap: document.querySelector("#mpje-trap"), authorities: document.querySelector("#authorities"),
  bookmarkButton: document.querySelector("#bookmark-button"), dashboardMetrics: document.querySelector("#dashboard-metrics"),
  storageStatus: document.querySelector("#storage-status"), examResults: document.querySelector("#exam-results"),
  resultSummary: document.querySelector("#result-summary"), areaBreakdown: document.querySelector("#area-breakdown"),
  topicBreakdown: document.querySelector("#topic-breakdown"), missedQuestions: document.querySelector("#missed-questions"),
  historyPanel: document.querySelector("#history-panel"), historyList: document.querySelector("#history-list"),
  historyDetail: document.querySelector("#history-detail"), studyGuidePanel: document.querySelector("#study-guide-panel"),
  guideSections: document.querySelector("#guide-sections"), guideSearch: document.querySelector("#guide-search"),
  guideAreaFilter: document.querySelector("#guide-area-filter"),
};

const state = {
  payload: null, guide: null, mode: null, sessionSeed: null, startedAt: null, queue: [], responses: [], index: 0,
  question: null, selected: new Set(), order: [], answered: false, revealed: false, correct: null,
  lastSession: null, progress: MpjeStorage.loadProgress(),
};

function createSessionSeed(mode) {
  sessionCounter += 1;
  if (requestedSeed) return `${requestedSeed}:${mode}:${sessionCounter}`;
  const randomPart = globalThis.crypto?.randomUUID?.() || `${Date.now()}:${Math.random()}`;
  return `${mode}:${randomPart}:${sessionCounter}`;
}

function createSessionId() {
  const randomPart = globalThis.crypto?.randomUUID?.() || `${Date.now()}-${Math.random().toString(16).slice(2)}`;
  return `session-${randomPart}`;
}

function saveProgress() { MpjeStorage.saveProgress(state.progress); }
function addUnique(list, value) { if (!list.includes(value)) list.push(value); }
function removeValue(list, value) { const index = list.indexOf(value); if (index >= 0) list.splice(index, 1); }
function escapeHtml(value) { return String(value).replace(/[&<>'"]/g, (character) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;" }[character])); }

function fillSelect(select, values, formatter = (value) => value) {
  values.forEach((value) => {
    const option = document.createElement("option"); option.value = value; option.textContent = formatter(value); select.append(option);
  });
}

function populateFilters(questions) {
  fillSelect(elements.areaFilter, [...new Set(questions.map((question) => question.area))].sort(), (value) => `Area ${value}`);
  fillSelect(elements.topicFilter, [...new Set(questions.map((question) => question.topic))].sort());
  fillSelect(elements.difficultyFilter, [...new Set(questions.map((question) => question.difficulty))].sort(), (value) => `${value}/5`);
  fillSelect(elements.typeFilter, [...new Set(questions.map((question) => question.question_type))].sort());
}

function filteredQuestions() {
  const area = elements.areaFilter.value; const topic = elements.topicFilter.value;
  const difficulty = elements.difficultyFilter.value; const type = elements.typeFilter.value; const drugOnly = elements.drugFilter.checked;
  return state.payload.questions.filter((question) => MpjeSessions.isReleaseUsable(question)
    && (!area || String(question.area) === area) && (!topic || question.topic === topic)
    && (!difficulty || String(question.difficulty) === difficulty) && (!type || question.question_type === type)
    && (!drugOnly || question.drug_ids.length > 0));
}

function examTypeForMode(mode) {
  return { quick20: "QUICK_20", mock: "MOCK_120", random: "TOPIC_QUIZ", drug: "TOPIC_QUIZ", browse: "TOPIC_QUIZ", wrong: "WRONG_ANSWER_QUIZ", bookmarked: "BOOKMARKED_QUIZ" }[mode] || null;
}

function hideSecondaryPanels() {
  elements.examResults.hidden = true; elements.historyPanel.hidden = true; elements.studyGuidePanel.hidden = true;
}

function startMode(mode, overrideQuestions = null) {
  state.mode = mode; state.sessionSeed = createSessionSeed(mode); state.startedAt = new Date().toISOString();
  state.responses = []; state.lastSession = null; hideSecondaryPanels();
  document.querySelectorAll("[data-mode]").forEach((button) => button.classList.toggle("active", button.dataset.mode === mode));
  let questions = overrideQuestions ? [...overrideQuestions] : filteredQuestions();
  try {
    if (mode === "quick20") questions = MpjeSessions.createQuick20(questions, state.sessionSeed);
    if (mode === "drug") questions = questions.filter((question) => question.drug_ids.length > 0);
    if (mode === "wrong") questions = questions.filter((question) => state.progress.wrong.includes(question.question_id));
    if (mode === "bookmarked") questions = questions.filter((question) => state.progress.bookmarks.includes(question.question_id));
    if (["random", "mock", "drug", "browse", "wrong", "bookmarked"].includes(mode)) questions = MpjeShuffle.seededShuffle(questions, state.sessionSeed);
    if (mode === "mock") questions = questions.slice(0, state.payload.blueprint.target_question_count_per_mock);
    if (["random", "drug", "browse"].includes(mode)) questions = questions.slice(0, 10);
    if (["wrong", "bookmarked"].includes(mode)) questions = questions.slice(0, 20);
  } catch (error) {
    elements.emptyState.hidden = false; elements.emptyState.innerHTML = `<h2>Unable to start this session</h2><p>${escapeHtml(error.message)}</p>`;
    elements.questionPanel.hidden = true; return;
  }
  if (!questions.length) {
    elements.emptyState.hidden = false; elements.emptyState.innerHTML = "<h2>No matching questions</h2><p>Adjust the filters or choose another mode.</p>";
    elements.questionPanel.hidden = true; return;
  }
  state.queue = questions; state.index = 0; renderCurrentQuestion();
}

function saveCurrentResponse() {
  if (!state.question || !state.queue.length) return;
  state.responses[state.index] = { selected: [...state.selected], order: [...state.order], answered: state.answered, revealed: state.revealed, correct: state.correct };
}

function renderCurrentQuestion() {
  const canonical = state.queue[state.index]; const response = state.responses[state.index];
  state.question = MpjeShuffle.shuffleQuestionChoices(canonical, state.sessionSeed);
  state.selected = new Set(response?.selected || []); state.order = [...(response?.order || [])];
  state.answered = Boolean(response?.answered); state.revealed = Boolean(response?.revealed); state.correct = response?.correct ?? null;
  elements.emptyState.hidden = true; elements.questionPanel.hidden = false; elements.examResults.hidden = true;
  elements.questionPosition.textContent = `${state.index + 1} / ${state.queue.length}`; elements.questionArea.textContent = `Area ${state.question.area}`;
  elements.questionDifficulty.textContent = `Difficulty ${state.question.difficulty}/5`; elements.questionType.textContent = state.question.question_type;
  elements.questionStem.textContent = state.question.stem; elements.choiceForm.replaceChildren();
  const ordered = state.question.question_type === "ORDERED_RESPONSE";
  elements.orderedHelp.hidden = !ordered; elements.selectedOrder.hidden = !ordered; elements.resetOrder.hidden = !ordered;
  elements.revealAnswer.hidden = state.mode !== "study"; elements.result.hidden = true; elements.result.className = "result";
  elements.explanation.hidden = true; elements.explanation.open = false; elements.previousQuestion.disabled = state.index === 0;
  elements.nextQuestion.disabled = !state.answered;
  elements.nextQuestion.textContent = state.index === state.queue.length - 1 && examTypeForMode(state.mode) ? "Finish Exam" : "Next";
  elements.checkAnswer.disabled = state.answered; elements.bookmarkButton.disabled = false; updateBookmarkButton();

  state.question.choices.forEach((choice) => {
    const label = document.createElement("label"); label.className = "choice"; label.dataset.choiceId = choice.id;
    if (ordered) {
      const button = document.createElement("button"); button.type = "button"; button.className = "ghost-button";
      button.innerHTML = `<span class="choice-id">${choice.id}</span><span>${escapeHtml(choice.text)}</span>`; button.disabled = state.answered;
      button.addEventListener("click", () => selectOrdered(choice.id)); label.append(button);
    } else {
      const input = document.createElement("input"); input.type = state.question.question_type === "SBA" ? "radio" : "checkbox";
      input.name = "answer"; input.value = choice.id; input.checked = state.selected.has(choice.id); input.disabled = state.answered;
      input.addEventListener("change", () => selectChoice(choice.id, input.checked));
      const text = document.createElement("span"); text.innerHTML = `<span class="choice-id">${choice.id}</span>${escapeHtml(choice.text)}`;
      label.append(input, text);
    }
    elements.choiceForm.append(label);
  });
  updateSelectedOrder();
  document.querySelectorAll(".choice").forEach((label) => label.classList.toggle("selected", state.selected.has(label.dataset.choiceId)));
  if (state.answered) {
    const selected = selectedAnswer(); elements.result.hidden = false; elements.result.className = `result ${state.correct ? "correct" : "incorrect"}`;
    elements.result.textContent = state.revealed ? "Answer revealed for study." : state.correct ? "Correct." : "Not correct. Review the reasoning below.";
    elements.explanation.hidden = false; elements.explanation.open = true; markChoices(selected, ordered); renderExplanation();
  }
  elements.questionPanel.scrollIntoView({ behavior: "smooth", block: "start" });
}

function selectChoice(choiceId, checked) {
  if (state.answered) return; if (state.question.question_type === "SBA") state.selected.clear();
  checked ? state.selected.add(choiceId) : state.selected.delete(choiceId);
  document.querySelectorAll(".choice").forEach((label) => label.classList.toggle("selected", state.selected.has(label.dataset.choiceId)));
}

function selectOrdered(choiceId) { if (!state.answered && !state.order.includes(choiceId)) { state.order.push(choiceId); updateSelectedOrder(); } }

function updateSelectedOrder() {
  if (state.question?.question_type !== "ORDERED_RESPONSE") return;
  elements.selectedOrder.textContent = state.order.length ? `Selected order: ${state.order.join(" -> ")}` : "Selected order: none";
  document.querySelectorAll(".choice").forEach((label) => {
    const rank = state.order.indexOf(label.dataset.choiceId); label.classList.toggle("selected", rank >= 0); label.querySelector(".order-rank")?.remove();
    if (rank >= 0) { const marker = document.createElement("span"); marker.className = "order-rank"; marker.textContent = `#${rank + 1}`; label.append(marker); }
  });
}

function selectedAnswer() { return state.question.question_type === "ORDERED_RESPONSE" ? state.order : [...state.selected].sort(); }
function answersMatch(left, right, ordered) {
  if (left.length !== right.length) return false; if (ordered) return left.every((value, index) => value === right[index]);
  const expected = [...right].sort(); return [...left].sort().every((value, index) => value === expected[index]);
}

function checkAnswer(revealed = false) {
  if (state.answered) return; const selected = selectedAnswer();
  if (!revealed && selected.length === 0) { elements.result.hidden = false; elements.result.className = "result incorrect"; elements.result.textContent = "Select an answer before checking."; return; }
  const ordered = state.question.question_type === "ORDERED_RESPONSE"; const correct = answersMatch(selected, state.question.correct_choice_ids, ordered);
  state.answered = true; state.revealed = revealed; state.correct = correct; elements.result.hidden = false;
  elements.result.className = `result ${correct ? "correct" : "incorrect"}`;
  elements.result.textContent = revealed ? "Answer revealed for study." : correct ? "Correct." : "Not correct. Review the reasoning below.";
  elements.explanation.hidden = false; elements.explanation.open = true; elements.nextQuestion.disabled = false; elements.checkAnswer.disabled = true;
  document.querySelectorAll(".choice input, .choice button").forEach((control) => { control.disabled = true; });
  markChoices(selected, ordered); renderExplanation(); saveCurrentResponse(); if (!revealed) updateProgress(correct);
}

function markChoices(selected, ordered) {
  const correctIds = new Set(state.question.correct_choice_ids);
  document.querySelectorAll(".choice").forEach((label) => {
    const id = label.dataset.choiceId; if (!ordered && correctIds.has(id)) label.classList.add("correct");
    if (!ordered && selected.includes(id) && !correctIds.has(id)) label.classList.add("incorrect");
  });
}

function renderExplanation() {
  const question = state.question; elements.correctAnswer.textContent = question.correct_choice_ids.join(question.question_type === "ORDERED_RESPONSE" ? " -> " : ", ");
  elements.coreReasoning.textContent = question.explanation.core_reasoning; elements.choiceAnalysis.replaceChildren();
  question.choices.forEach((choice) => { const term = document.createElement("dt"); term.textContent = choice.id; const definition = document.createElement("dd"); definition.textContent = question.explanation.choice_analysis[choice.id]; elements.choiceAnalysis.append(term, definition); });
  elements.relatedFacts.replaceChildren(...question.explanation.related_facts.map((fact) => { const item = document.createElement("li"); item.textContent = fact; return item; }));
  elements.mpjeTrap.textContent = question.explanation.mpje_trap;
  elements.authorities.replaceChildren(...question.authorities.map((authority) => { const item = document.createElement("li"); const link = document.createElement("a"); link.href = authority.url; link.target = "_blank"; link.rel = "noreferrer"; link.textContent = `${authority.name}, ${authority.section}`; item.append(link, ` - verified ${authority.last_verified}`); return item; }));
  renderDrugChecks(question.drug_checks);
}

function renderDrugChecks(drugs) {
  elements.drugCheckSection.hidden = drugs.length === 0;
  elements.drugChecks.replaceChildren(...drugs.map((drug) => {
    const card = document.createElement("article"); card.className = "drug-card";
    card.innerHTML = `<h3>${escapeHtml(drug.generic_name)}</h3><dl><dt>Brand</dt><dd>${drug.brand_names.map(escapeHtml).join(", ")}</dd><dt>Indication</dt><dd>${drug.main_indications.map(escapeHtml).join("; ")}</dd><dt>Federal</dt><dd>${escapeHtml(drug.federal_status.schedule)}</dd><dt>Massachusetts</dt><dd>${escapeHtml(drug.massachusetts_status.schedule)}</dd><dt>MassPAT</dt><dd>${drug.massachusetts_status.masspat_reportable ? "Reportable" : "Not reportable on status alone"}</dd><dt>Consequence</dt><dd>${escapeHtml(drug.legal_consequences.masspat.summary)} ${escapeHtml(drug.legal_consequences.quantity_limit.summary)}</dd><dt>Rule IDs</dt><dd>${[...new Set([...drug.legal_consequences.masspat.rule_ids, ...drug.legal_consequences.quantity_limit.rule_ids])].map(escapeHtml).join(", ")}</dd></dl>`;
    return card;
  }));
}

function updateProgress(correct) {
  const question = state.question; addUnique(state.progress.completed, question.question_id);
  correct ? removeValue(state.progress.wrong, question.question_id) : addUnique(state.progress.wrong, question.question_id);
  [[state.progress.byArea, String(question.area)], [state.progress.byTopic, question.topic], [state.progress.byDifficulty, String(question.difficulty)]].forEach(([bucket, key]) => {
    bucket[key] ||= { correct: 0, attempted: 0 }; bucket[key].attempted += 1; if (correct) bucket[key].correct += 1;
  });
  saveProgress(); renderDashboard();
}

function updateBookmarkButton() { if (state.question) elements.bookmarkButton.textContent = state.progress.bookmarks.includes(state.question.question_id) ? "Bookmarked" : "Bookmark"; }

function renderBreakdownTable(breakdown) {
  const rows = Object.entries(breakdown).sort(([left], [right]) => left.localeCompare(right));
  if (!rows.length) return "<p class=\"muted\">No attempts recorded.</p>";
  return `<table class="breakdown-table"><thead><tr><th>Group</th><th>Score</th><th>%</th></tr></thead><tbody>${rows.map(([label, item]) => `<tr><td>${escapeHtml(label)}</td><td>${item.correct}/${item.total}</td><td>${item.percentage}%</td></tr>`).join("")}</tbody></table>`;
}

function formatElapsed(seconds) { return `${Math.floor(seconds / 60)}:${String(seconds % 60).padStart(2, "0")}`; }

async function finishSession() {
  saveCurrentResponse();
  const record = MpjeSessions.buildCompletedSession({ sessionId: createSessionId(), examType: examTypeForMode(state.mode), sessionSeed: state.sessionSeed, startedAt: state.startedAt, completedAt: new Date().toISOString(), queue: state.queue, responses: state.responses });
  await MpjeStorage.saveSession(record); state.lastSession = record; renderResults(record); await renderDashboard();
}

function renderResults(record) {
  elements.questionPanel.hidden = true; elements.emptyState.hidden = true; elements.examResults.hidden = false;
  elements.resultSummary.innerHTML = `<strong>${record.score.correct}/${record.score.total}</strong><span>${record.score.percentage}% · ${formatElapsed(record.elapsed_seconds)} elapsed</span>`;
  elements.areaBreakdown.innerHTML = renderBreakdownTable(record.area_breakdown); elements.topicBreakdown.innerHTML = renderBreakdownTable(record.topic_breakdown);
  elements.missedQuestions.replaceChildren(...record.missed_question_ids.map((questionId) => { const item = document.createElement("li"); const question = state.payload.questions.find((candidate) => candidate.question_id === questionId); item.textContent = `${questionId}${question ? ` — ${question.topic}` : ""}`; return item; }));
  if (!record.missed_question_ids.length) { const item = document.createElement("li"); item.textContent = "No missed questions."; elements.missedQuestions.append(item); }
  document.querySelector("#retry-wrong").disabled = record.missed_question_ids.length === 0;
  document.querySelector("#practice-topic").disabled = record.missed_question_ids.length === 0;
  document.querySelector("#open-related-guide").disabled = record.missed_question_ids.length === 0;
  elements.examResults.scrollIntoView({ behavior: "smooth", block: "start" });
}

function metricCard(value, label) { return `<article class="metric-card"><strong>${escapeHtml(value)}</strong><span>${escapeHtml(label)}</span></article>`; }

async function renderDashboard() {
  const sessions = await MpjeStorage.listSessions(); const areaTotals = Object.values(state.progress.byArea);
  const correct = areaTotals.reduce((sum, item) => sum + item.correct, 0); const attempted = areaTotals.reduce((sum, item) => sum + item.attempted, 0);
  const quick = sessions.find((session) => session.exam_type === "QUICK_20"); const mock = sessions.find((session) => session.exam_type === "MOCK_120");
  elements.dashboardMetrics.innerHTML = [metricCard(attempted ? `${Math.round((100 * correct) / attempted)}%` : "—", "Overall accuracy"), metricCard(quick ? `${quick.score.correct}/${quick.score.total}` : "—", "Recent Quick 20"), metricCard(mock ? `${mock.score.correct}/${mock.score.total}` : "—", "Recent Mock 120"), metricCard(String(state.progress.wrong.length), "Wrong questions"), metricCard(String(state.progress.bookmarks.length), "Bookmarks")].join("");
}

function examTypeLabel(type) { return { QUICK_20: "Quick 20", MOCK_120: "Mock 120", TOPIC_QUIZ: "Topic Quiz", WRONG_ANSWER_QUIZ: "Wrong Answers", BOOKMARKED_QUIZ: "Bookmarked" }[type] || type; }

async function showHistory() {
  hideSecondaryPanels(); elements.questionPanel.hidden = true; elements.historyPanel.hidden = false; const sessions = await MpjeStorage.listSessions();
  if (!sessions.length) { elements.historyList.innerHTML = "<p class=\"muted\">No completed sessions are stored on this device.</p>"; elements.historyDetail.replaceChildren(); return; }
  elements.historyList.innerHTML = `<table class="history-table"><thead><tr><th>Date</th><th>Type</th><th>Score</th><th>Time</th><th></th></tr></thead><tbody>${sessions.map((session) => `<tr><td>${escapeHtml(session.completed_at.slice(0, 10))}</td><td>${escapeHtml(examTypeLabel(session.exam_type))}</td><td>${session.score.correct}/${session.score.total} ${session.score.percentage}%</td><td>${formatElapsed(session.elapsed_seconds)}</td><td><button type="button" data-history-id="${escapeHtml(session.session_id)}">Open</button></td></tr>`).join("")}</tbody></table>`;
  elements.historyList.querySelectorAll("[data-history-id]").forEach((button) => button.addEventListener("click", async () => renderHistoryDetail(await MpjeStorage.getSession(button.dataset.historyId))));
  elements.historyPanel.scrollIntoView({ behavior: "smooth", block: "start" });
}

function renderHistoryDetail(session) {
  if (!session) return;
  elements.historyDetail.innerHTML = `<article class="guide-section"><h3>${escapeHtml(examTypeLabel(session.exam_type))} — ${session.score.correct}/${session.score.total} (${session.score.percentage}%)</h3><p>${escapeHtml(session.completed_at)} · ${formatElapsed(session.elapsed_seconds)}</p><h4>Area breakdown</h4>${renderBreakdownTable(session.area_breakdown)}<h4>Topic breakdown</h4>${renderBreakdownTable(session.topic_breakdown)}<h4>Missed question IDs</h4><p>${session.missed_question_ids.map(escapeHtml).join(", ") || "None"}</p><details><summary>Stored content hashes</summary><pre>${escapeHtml(JSON.stringify(session.question_content_hashes, null, 2))}</pre></details></article>`;
}

function renderGuide(sectionIds = null) {
  const search = elements.guideSearch.value.trim().toLowerCase(); const area = elements.guideAreaFilter.value; let sections = state.guide?.sections || [];
  if (sectionIds) sections = sections.filter((section) => sectionIds.includes(section.section_id));
  sections = sections.filter((section) => (!area || section.areas.includes(Number(area))) && (!search || `${section.title} ${section.topic} ${section.subtopic}`.toLowerCase().includes(search)));
  if (!sections.length) { const pending = state.guide?.meta?.pending_section_count || 0; elements.guideSections.innerHTML = `<p class="muted">No independently verified guide section is public for this selection.${pending ? ` ${pending} pilot section(s) remain audit-pending and are intentionally hidden.` : ""}</p>`; return; }
  elements.guideSections.innerHTML = sections.map((section) => `<details class="guide-section"><summary>${escapeHtml(section.title)}</summary><p>${escapeHtml(section.topic)} · Areas ${section.areas.join(", ")}</p><h4>Quick Review</h4><ul>${section.quick_review.map((item) => `<li>${escapeHtml(item.text)}</li>`).join("")}</ul><h4>Common Traps</h4><ul>${section.common_traps.map((item) => `<li>${escapeHtml(item.text)}</li>`).join("")}</ul><h4>Official sources</h4><ul class="guide-source-list">${section.authorities.map((authority) => `<li><a href="${escapeHtml(authority.url)}" target="_blank" rel="noreferrer">${escapeHtml(authority.name)}, ${escapeHtml(authority.section)}</a></li>`).join("")}</ul><button type="button" data-guide-quiz="${escapeHtml(section.section_id)}">Quick Quiz 10</button></details>`).join("");
  elements.guideSections.querySelectorAll("[data-guide-quiz]").forEach((button) => button.addEventListener("click", () => { const section = sections.find((candidate) => candidate.section_id === button.dataset.guideQuiz); const questions = section.practice_question_ids.map((id) => state.payload.questions.find((question) => question.question_id === id)).filter(Boolean).slice(0, 10); startMode("browse", questions); }));
}

function showStudyGuide(sectionIds = null) { hideSecondaryPanels(); elements.questionPanel.hidden = true; elements.studyGuidePanel.hidden = false; renderGuide(sectionIds); elements.studyGuidePanel.scrollIntoView({ behavior: "smooth", block: "start" }); }

async function exportStudyData() {
  const bundle = await MpjeStorage.exportData({ area_filter: elements.areaFilter.value, topic_filter: elements.topicFilter.value });
  const blob = new Blob([`${JSON.stringify(bundle, null, 2)}\n`], { type: "application/json" }); const url = URL.createObjectURL(blob); const link = document.createElement("a");
  link.href = url; link.download = `ma-mpje-study-data-${new Date().toISOString().slice(0, 10)}.json`; link.click(); URL.revokeObjectURL(url);
  elements.storageStatus.textContent = `Exported ${bundle.exam_history.length} session(s).`;
}

async function importStudyFile(file) {
  const bundle = JSON.parse(await file.text()); const error = MpjeStorage.validateExportBundle(bundle); if (error) throw new Error(error);
  if (!window.confirm(`Import compatible version ${bundle.version} data with ${bundle.exam_history.length} session(s)? Existing session IDs will be updated.`)) return;
  const result = await MpjeStorage.importData(bundle); state.progress = result.progress; elements.storageStatus.textContent = `Imported ${result.imported_sessions} session(s).`; await renderDashboard();
}

function weakestArea() { return Object.entries(state.progress.byArea).filter(([, value]) => value.attempted).sort((left, right) => (left[1].correct / left[1].attempted) - (right[1].correct / right[1].attempted))[0]?.[0] || "1"; }
function mostMissedTopic(record) { return Object.entries(record?.topic_breakdown || {}).sort((left, right) => right[1].incorrect - left[1].incorrect)[0]?.[0] || ""; }

document.querySelectorAll("[data-mode]").forEach((button) => button.addEventListener("click", () => startMode(button.dataset.mode)));
elements.checkAnswer.addEventListener("click", () => checkAnswer(false)); elements.revealAnswer.addEventListener("click", () => checkAnswer(true));
elements.resetOrder.addEventListener("click", () => { if (!state.answered) { state.order = []; updateSelectedOrder(); } });
elements.previousQuestion.addEventListener("click", () => { if (state.index === 0) return; saveCurrentResponse(); state.index -= 1; renderCurrentQuestion(); });
elements.nextQuestion.addEventListener("click", async () => { saveCurrentResponse(); if (state.index === state.queue.length - 1 && examTypeForMode(state.mode)) { await finishSession(); return; } state.index = (state.index + 1) % state.queue.length; renderCurrentQuestion(); });
elements.bookmarkButton.addEventListener("click", () => { if (!state.question) return; const bookmarks = state.progress.bookmarks; bookmarks.includes(state.question.question_id) ? removeValue(bookmarks, state.question.question_id) : addUnique(bookmarks, state.question.question_id); saveProgress(); updateBookmarkButton(); renderDashboard(); });

document.querySelector("#review-answers").addEventListener("click", () => { state.index = 0; renderCurrentQuestion(); });
document.querySelector("#retry-wrong").addEventListener("click", () => { const questions = state.lastSession.missed_question_ids.map((id) => state.payload.questions.find((question) => question.question_id === id)).filter(Boolean); startMode("wrong", questions); });
document.querySelector("#practice-topic").addEventListener("click", () => { elements.topicFilter.value = mostMissedTopic(state.lastSession); startMode("browse"); });
document.querySelector("#open-related-guide").addEventListener("click", () => { const ids = [...new Set(state.lastSession.missed_question_ids.flatMap((id) => state.guide.question_to_sections[id] || []))]; showStudyGuide(ids.length ? ids : null); });
document.querySelector("#new-quick20").addEventListener("click", () => startMode("quick20")); document.querySelector("#history-button").addEventListener("click", showHistory);
document.querySelector("#close-history").addEventListener("click", () => { elements.historyPanel.hidden = true; }); document.querySelector("#study-guide-button").addEventListener("click", () => showStudyGuide());
document.querySelector("#close-study-guide").addEventListener("click", () => { elements.studyGuidePanel.hidden = true; }); elements.guideSearch.addEventListener("input", () => renderGuide()); elements.guideAreaFilter.addEventListener("change", () => renderGuide());
document.querySelector("#export-study-data").addEventListener("click", () => exportStudyData().catch((error) => { elements.storageStatus.textContent = error.message; }));
document.querySelector("#import-study-data").addEventListener("click", () => document.querySelector("#import-study-file").click());
document.querySelector("#import-study-file").addEventListener("change", (event) => { const [file] = event.target.files; if (file) importStudyFile(file).catch((error) => { elements.storageStatus.textContent = `Import rejected: ${error.message}`; }); event.target.value = ""; });
document.querySelectorAll("[data-dashboard-action]").forEach((button) => button.addEventListener("click", () => { if (button.dataset.dashboardAction === "quick20") startMode("quick20"); if (button.dataset.dashboardAction === "mistakes") startMode("wrong"); if (button.dataset.dashboardAction === "weakest") { elements.areaFilter.value = weakestArea(); startMode("browse"); } }));

Promise.all([
  fetch(DATA_URL).then((response) => { if (!response.ok) throw new Error(`Question data HTTP ${response.status}`); return response.json(); }),
  fetch(GUIDE_URL).then((response) => { if (!response.ok) throw new Error(`Study Guide HTTP ${response.status}`); return response.json(); }),
]).then(([payload, guide]) => {
  state.payload = payload; state.guide = guide; populateFilters(payload.questions); elements.fixtureWarning.hidden = !payload.meta.development_fixture_mode;
  elements.dataSummary.textContent = `${payload.meta.question_count} ${payload.meta.development_fixture_mode ? "development fixtures" : "released questions"} loaded`; renderDashboard();
}).catch((error) => { elements.dataSummary.textContent = "Site data failed to load."; elements.emptyState.innerHTML = `<h2>Unable to load data</h2><p>Serve the site over HTTP and rebuild generated data. ${escapeHtml(error.message)}</p>`; });
