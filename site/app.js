"use strict";

const DATA_URL = "generated/questions.json";
const STORAGE_KEY = "ma-mpje-progress-v1";
const sessionSeed = new URLSearchParams(window.location.search).get("seed") || new Date().toISOString().slice(0, 10);

const elements = {
  fixtureWarning: document.querySelector("#fixture-warning"),
  dataSummary: document.querySelector("#data-summary"),
  areaFilter: document.querySelector("#area-filter"),
  topicFilter: document.querySelector("#topic-filter"),
  difficultyFilter: document.querySelector("#difficulty-filter"),
  typeFilter: document.querySelector("#type-filter"),
  drugFilter: document.querySelector("#drug-filter"),
  emptyState: document.querySelector("#empty-state"),
  questionPanel: document.querySelector("#question-panel"),
  questionPosition: document.querySelector("#question-position"),
  questionArea: document.querySelector("#question-area"),
  questionDifficulty: document.querySelector("#question-difficulty"),
  questionType: document.querySelector("#question-type"),
  questionStem: document.querySelector("#question-stem"),
  orderedHelp: document.querySelector("#ordered-help"),
  choiceForm: document.querySelector("#choice-form"),
  selectedOrder: document.querySelector("#selected-order"),
  checkAnswer: document.querySelector("#check-answer"),
  revealAnswer: document.querySelector("#reveal-answer"),
  resetOrder: document.querySelector("#reset-order"),
  nextQuestion: document.querySelector("#next-question"),
  result: document.querySelector("#result"),
  explanation: document.querySelector("#explanation"),
  correctAnswer: document.querySelector("#correct-answer"),
  coreReasoning: document.querySelector("#core-reasoning"),
  choiceAnalysis: document.querySelector("#choice-analysis"),
  drugCheckSection: document.querySelector("#drug-check-section"),
  drugChecks: document.querySelector("#drug-checks"),
  relatedFacts: document.querySelector("#related-facts"),
  mpjeTrap: document.querySelector("#mpje-trap"),
  authorities: document.querySelector("#authorities"),
  bookmarkButton: document.querySelector("#bookmark-button"),
};

const state = {
  payload: null,
  mode: null,
  queue: [],
  index: 0,
  question: null,
  selected: new Set(),
  order: [],
  answered: false,
  progress: loadProgress(),
};

function loadProgress() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY)) || { wrong: [], bookmarks: [], completed: [], byArea: {}, byDifficulty: {} };
  } catch (_error) {
    return { wrong: [], bookmarks: [], completed: [], byArea: {}, byDifficulty: {} };
  }
}

function saveProgress() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state.progress));
}

function addUnique(list, value) {
  if (!list.includes(value)) list.push(value);
}

function removeValue(list, value) {
  const index = list.indexOf(value);
  if (index >= 0) list.splice(index, 1);
}

function fillSelect(select, values, formatter = (value) => value) {
  values.forEach((value) => {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = formatter(value);
    select.append(option);
  });
}

function populateFilters(questions) {
  fillSelect(elements.areaFilter, [...new Set(questions.map((question) => question.area))].sort(), (value) => `Area ${value}`);
  fillSelect(elements.topicFilter, [...new Set(questions.map((question) => question.topic))].sort());
  fillSelect(elements.difficultyFilter, [...new Set(questions.map((question) => question.difficulty))].sort(), (value) => `${value}/5`);
  fillSelect(elements.typeFilter, [...new Set(questions.map((question) => question.question_type))].sort());
}

function filteredQuestions() {
  const area = elements.areaFilter.value;
  const topic = elements.topicFilter.value;
  const difficulty = elements.difficultyFilter.value;
  const type = elements.typeFilter.value;
  const drugOnly = elements.drugFilter.checked;
  return state.payload.questions.filter((question) =>
    (!area || String(question.area) === area) &&
    (!topic || question.topic === topic) &&
    (!difficulty || String(question.difficulty) === difficulty) &&
    (!type || question.question_type === type) &&
    (!drugOnly || question.drug_ids.length > 0)
  );
}

function startMode(mode) {
  state.mode = mode;
  document.querySelectorAll("[data-mode]").forEach((button) => button.classList.toggle("active", button.dataset.mode === mode));
  let questions = filteredQuestions();
  if (mode === "drug") questions = questions.filter((question) => question.drug_ids.length > 0);
  if (["random", "mock", "drug"].includes(mode)) {
    questions = MpjeShuffle.seededShuffle(questions, `${sessionSeed}:${mode}`);
  }
  if (mode === "mock") questions = questions.slice(0, state.payload.blueprint.target_question_count_per_mock);
  if (!questions.length) {
    elements.emptyState.hidden = false;
    elements.emptyState.innerHTML = "<h2>No matching questions</h2><p>Adjust the filters or choose another mode.</p>";
    elements.questionPanel.hidden = true;
    return;
  }
  state.queue = questions;
  state.index = 0;
  renderCurrentQuestion();
}

function renderCurrentQuestion() {
  const canonical = state.queue[state.index];
  state.question = MpjeShuffle.shuffleQuestionChoices(canonical, `${sessionSeed}:${state.mode}`);
  state.selected = new Set();
  state.order = [];
  state.answered = false;
  elements.emptyState.hidden = true;
  elements.questionPanel.hidden = false;
  elements.questionPosition.textContent = `${state.index + 1} / ${state.queue.length}`;
  elements.questionArea.textContent = `Area ${state.question.area}`;
  elements.questionDifficulty.textContent = `Difficulty ${state.question.difficulty}/5`;
  elements.questionType.textContent = state.question.question_type;
  elements.questionStem.textContent = state.question.stem;
  elements.choiceForm.replaceChildren();
  const ordered = state.question.question_type === "ORDERED_RESPONSE";
  elements.orderedHelp.hidden = !ordered;
  elements.selectedOrder.hidden = !ordered;
  elements.resetOrder.hidden = !ordered;
  elements.revealAnswer.hidden = state.mode !== "study";
  elements.result.hidden = true;
  elements.result.className = "result";
  elements.explanation.hidden = true;
  elements.explanation.open = false;
  elements.nextQuestion.disabled = true;
  elements.checkAnswer.disabled = false;
  elements.bookmarkButton.disabled = false;
  updateBookmarkButton();

  state.question.choices.forEach((choice) => {
    const label = document.createElement("label");
    label.className = "choice";
    label.dataset.choiceId = choice.id;
    if (ordered) {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "ghost-button";
      button.innerHTML = `<span class="choice-id">${choice.id}</span><span>${choice.text}</span>`;
      button.addEventListener("click", () => selectOrdered(choice.id, label));
      label.append(button);
    } else {
      const input = document.createElement("input");
      input.type = state.question.question_type === "SBA" ? "radio" : "checkbox";
      input.name = "answer";
      input.value = choice.id;
      input.addEventListener("change", () => selectChoice(choice.id, input.checked));
      const text = document.createElement("span");
      text.innerHTML = `<span class="choice-id">${choice.id}</span>${escapeHtml(choice.text)}`;
      label.append(input, text);
    }
    elements.choiceForm.append(label);
  });
  updateSelectedOrder();
  elements.questionPanel.scrollIntoView({ behavior: "smooth", block: "start" });
}

function selectChoice(choiceId, checked) {
  if (state.answered) return;
  if (state.question.question_type === "SBA") state.selected.clear();
  checked ? state.selected.add(choiceId) : state.selected.delete(choiceId);
  document.querySelectorAll(".choice").forEach((label) => label.classList.toggle("selected", state.selected.has(label.dataset.choiceId)));
}

function selectOrdered(choiceId) {
  if (state.answered || state.order.includes(choiceId)) return;
  state.order.push(choiceId);
  updateSelectedOrder();
}

function updateSelectedOrder() {
  if (state.question?.question_type !== "ORDERED_RESPONSE") return;
  elements.selectedOrder.textContent = state.order.length ? `Selected order: ${state.order.join(" -> ")}` : "Selected order: none";
  document.querySelectorAll(".choice").forEach((label) => {
    const rank = state.order.indexOf(label.dataset.choiceId);
    label.classList.toggle("selected", rank >= 0);
    const oldRank = label.querySelector(".order-rank");
    if (oldRank) oldRank.remove();
    if (rank >= 0) {
      const marker = document.createElement("span");
      marker.className = "order-rank";
      marker.textContent = `#${rank + 1}`;
      label.append(marker);
    }
  });
}

function selectedAnswer() {
  return state.question.question_type === "ORDERED_RESPONSE" ? state.order : [...state.selected].sort();
}

function answersMatch(left, right, ordered) {
  if (left.length !== right.length) return false;
  if (ordered) return left.every((value, index) => value === right[index]);
  const expected = [...right].sort();
  return [...left].sort().every((value, index) => value === expected[index]);
}

function checkAnswer(revealed = false) {
  if (state.answered) return;
  const selected = selectedAnswer();
  if (!revealed && selected.length === 0) {
    elements.result.hidden = false;
    elements.result.className = "result incorrect";
    elements.result.textContent = "Select an answer before checking.";
    return;
  }
  const ordered = state.question.question_type === "ORDERED_RESPONSE";
  const correct = answersMatch(selected, state.question.correct_choice_ids, ordered);
  state.answered = true;
  elements.result.hidden = false;
  elements.result.className = `result ${correct ? "correct" : "incorrect"}`;
  elements.result.textContent = revealed ? "Answer revealed for study." : correct ? "Correct." : "Not correct. Review the reasoning below.";
  elements.explanation.hidden = false;
  elements.explanation.open = true;
  elements.nextQuestion.disabled = false;
  elements.checkAnswer.disabled = true;
  document.querySelectorAll(".choice input, .choice button").forEach((control) => { control.disabled = true; });
  markChoices(selected, ordered);
  renderExplanation();
  if (!revealed) updateProgress(correct);
}

function markChoices(selected, ordered) {
  const correctIds = new Set(state.question.correct_choice_ids);
  document.querySelectorAll(".choice").forEach((label) => {
    const id = label.dataset.choiceId;
    if (!ordered && correctIds.has(id)) label.classList.add("correct");
    if (!ordered && selected.includes(id) && !correctIds.has(id)) label.classList.add("incorrect");
  });
}

function renderExplanation() {
  const question = state.question;
  elements.correctAnswer.textContent = question.correct_choice_ids.join(question.question_type === "ORDERED_RESPONSE" ? " -> " : ", ");
  elements.coreReasoning.textContent = question.explanation.core_reasoning;
  elements.choiceAnalysis.replaceChildren();
  question.choices.forEach((choice) => {
    const term = document.createElement("dt");
    term.textContent = choice.id;
    const definition = document.createElement("dd");
    definition.textContent = question.explanation.choice_analysis[choice.id];
    elements.choiceAnalysis.append(term, definition);
  });
  elements.relatedFacts.replaceChildren(...question.explanation.related_facts.map((fact) => {
    const item = document.createElement("li");
    item.textContent = fact;
    return item;
  }));
  elements.mpjeTrap.textContent = question.explanation.mpje_trap;
  elements.authorities.replaceChildren(...question.authorities.map((authority) => {
    const item = document.createElement("li");
    const link = document.createElement("a");
    link.href = authority.url;
    link.target = "_blank";
    link.rel = "noreferrer";
    link.textContent = `${authority.name}, ${authority.section}`;
    item.append(link, ` - verified ${authority.last_verified}`);
    return item;
  }));
  renderDrugChecks(question.drug_checks);
}

function renderDrugChecks(drugs) {
  elements.drugCheckSection.hidden = drugs.length === 0;
  elements.drugChecks.replaceChildren(...drugs.map((drug) => {
    const card = document.createElement("article");
    card.className = "drug-card";
    card.innerHTML = `
      <h3>${escapeHtml(drug.generic_name)}</h3>
      <dl>
        <dt>Brand</dt><dd>${drug.brand_names.map(escapeHtml).join(", ")}</dd>
        <dt>Indication</dt><dd>${drug.main_indications.map(escapeHtml).join("; ")}</dd>
        <dt>Federal</dt><dd>${escapeHtml(drug.federal_status.schedule)}</dd>
        <dt>Massachusetts</dt><dd>${escapeHtml(drug.massachusetts_status.schedule)}</dd>
        <dt>MassPAT</dt><dd>${drug.massachusetts_status.masspat_reportable ? "Reportable" : "Not reportable on status alone"}</dd>
        <dt>Consequence</dt><dd>${escapeHtml(drug.legal_consequences.masspat.summary)} ${escapeHtml(drug.legal_consequences.quantity_limit.summary)}</dd>
        <dt>Rule IDs</dt><dd>${[...new Set([...drug.legal_consequences.masspat.rule_ids, ...drug.legal_consequences.quantity_limit.rule_ids])].map(escapeHtml).join(", ")}</dd>
      </dl>`;
    return card;
  }));
}

function updateProgress(correct) {
  const question = state.question;
  addUnique(state.progress.completed, question.question_id);
  correct ? removeValue(state.progress.wrong, question.question_id) : addUnique(state.progress.wrong, question.question_id);
  const areaKey = String(question.area);
  const difficultyKey = String(question.difficulty);
  state.progress.byArea[areaKey] ||= { correct: 0, attempted: 0 };
  state.progress.byDifficulty[difficultyKey] ||= { correct: 0, attempted: 0 };
  state.progress.byArea[areaKey].attempted += 1;
  state.progress.byDifficulty[difficultyKey].attempted += 1;
  if (correct) {
    state.progress.byArea[areaKey].correct += 1;
    state.progress.byDifficulty[difficultyKey].correct += 1;
  }
  saveProgress();
}

function updateBookmarkButton() {
  if (!state.question) return;
  elements.bookmarkButton.textContent = state.progress.bookmarks.includes(state.question.question_id) ? "Bookmarked" : "Bookmark";
}

function escapeHtml(value) {
  return String(value).replace(/[&<>'"]/g, (character) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;" }[character]));
}

document.querySelectorAll("[data-mode]").forEach((button) => button.addEventListener("click", () => startMode(button.dataset.mode)));
elements.checkAnswer.addEventListener("click", () => checkAnswer(false));
elements.revealAnswer.addEventListener("click", () => checkAnswer(true));
elements.resetOrder.addEventListener("click", () => { if (!state.answered) { state.order = []; updateSelectedOrder(); } });
elements.nextQuestion.addEventListener("click", () => {
  state.index = (state.index + 1) % state.queue.length;
  renderCurrentQuestion();
});
elements.bookmarkButton.addEventListener("click", () => {
  if (!state.question) return;
  const bookmarks = state.progress.bookmarks;
  bookmarks.includes(state.question.question_id) ? removeValue(bookmarks, state.question.question_id) : addUnique(bookmarks, state.question.question_id);
  saveProgress();
  updateBookmarkButton();
});

fetch(DATA_URL)
  .then((response) => {
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return response.json();
  })
  .then((payload) => {
    state.payload = payload;
    populateFilters(payload.questions);
    elements.fixtureWarning.hidden = !payload.meta.development_fixture_mode;
    elements.dataSummary.textContent = `${payload.meta.question_count} ${payload.meta.development_fixture_mode ? "development fixtures" : "released questions"} loaded`;
  })
  .catch((error) => {
    elements.dataSummary.textContent = "Site data failed to load.";
    elements.emptyState.innerHTML = `<h2>Unable to load data</h2><p>Serve the site over HTTP and rebuild generated data. ${escapeHtml(error.message)}</p>`;
  });
