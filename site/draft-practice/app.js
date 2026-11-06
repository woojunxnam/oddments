"use strict";

(async () => {
  const $ = selector => document.querySelector(selector);
  const core = MpjeDraftPractice;
  const storageKey = "mpje.draft33.practice.v1";
  const backupFormat = "MPJE_DRAFT33_PRACTICE_BACKUP_V1";
  let questions = [], active = [], current = "", records = Object.create(null), order = [];
  let storageAvailable = true;
  const byId = new Map();
  function message(selector, value) { $(selector).textContent = value; }
  function element(tag, value) { const node = document.createElement(tag); if (value !== undefined) node.textContent = value; return node; }
  function record(q) { return records[q.id] || (records[q.id] = core.emptyRecord(q)); }
  function persist() {
    try { if (!storageAvailable) throw new Error("storage unavailable"); localStorage.setItem(storageKey, JSON.stringify(Object.values(records))); }
    catch (_) { storageAvailable = false; $("#storage-warning").hidden = false; }
  }
  function stats() {
    const s = core.summary(questions, records);
    message("#progress", `채점·확인 ${s.answered}/33 · 제안 답 일치 ${s.matched} · 다름 ${s.mismatched} · HOLD 확인 ${s.held} (채점 제외)`);
  }
  function select(id, updateUrl = true, focus = false) {
    current = id; const q = byId.get(id); const r = record(q);
    $("#empty").hidden = true; $("#question-panel").hidden = false;
    message("#position", `${active.indexOf(id) + 1} / ${active.length} · ${q.id}`);
    message("#question-status", q.review_status === "LEGAL_HOLD" ? "법규·시점 HOLD · 채점 제외" : q.review_status === "DUPLICATE_DEFERRED" ? "중복 검토 대기 · 공개 초안" : "미승인 공개 초안");
    message("#question-topic", q.title); message("#question-stem", q.stem);
    $("#hold-notice").hidden = q.review_status !== "LEGAL_HOLD";
    message("#hold-notice", q.review_status === "LEGAL_HOLD" ? q.blockers_ko[0] : "");
    const form = $("#choices"); form.replaceChildren();
    for (const c of q.choices) {
      const label = element("label"); label.className = "choice";
      const input = element("input"); input.type = "radio"; input.name = "answer"; input.value = c.id; input.checked = r.pick === c.id;
      const span = element("span", `${c.id}. ${c.text}`); label.append(input, span); form.append(label);
      input.addEventListener("change", () => { r.pick = c.id; r.checked = false; persist(); $("#result").hidden = true; $("#explanation").hidden = true; stats(); updateList(); });
    }
    message("#check", q.scoring_policy === "NO_GRADE" ? "선택 기록·검토" : "답 확인·채점");
    $("#result").hidden = true; $("#explanation").hidden = true;
    $("#note").value = r.note;
    $("#bookmark").setAttribute("aria-pressed", String(r.bookmarked)); message("#bookmark", r.bookmarked ? "★ 북마크됨" : "☆ 북마크");
    $("#previous").disabled = active.indexOf(id) <= 0;
    $("#next").disabled = active.indexOf(id) >= active.length - 1;
    if (r.checked) showResult(false);
    if (updateUrl) history.replaceState(null, "", "#" + encodeURIComponent(id));
    updateList(); if (focus) $("#question-stem").focus({ preventScroll: true });
  }
  function showExplanation(q) {
    message("#proposed-answer", q.scoring_policy === "NO_GRADE" ? `보류 중인 작성자 제안: ${q.proposed_key.join(", ")} · 확정 정답 아님` : `작성자 제안 답: ${q.proposed_key.join(", ")} · 정식 승인 대기`);
    message("#core-reasoning", q.core_ko); const dl = $("#choice-analysis"); dl.replaceChildren();
    for (const c of q.choices) dl.append(element("dt", `${c.id}. ${c.text}`), element("dd", q.analysis_ko[c.id]));
    const sources = $("#authorities"); sources.replaceChildren();
    for (const a of q.authorities) {
      const li = element("li"); const link = element("a", a.section); link.href = a.url; link.target = "_blank"; link.rel = "noopener noreferrer";
      const limit = element("p", `기존 확인일: ${a.checked} · 효력일·적용 범위: ${a.effective_limit}`); limit.className = "source-limit"; li.append(link, limit); sources.append(li);
    }
    const blockers = $("#blockers"); blockers.replaceChildren(...q.blockers_ko.map(t => element("li", t)));
    $("#explanation").hidden = false;
  }
  function showResult(commit = true) {
    const q = byId.get(current); const r = record(q);
    try {
      const result = core.grade(q, r.pick);
      if (commit) { r.checked = true; persist(); }
      $("#result").className = "result " + (result.status === "HOLD" ? "held" : result.matches ? "matched" : "different");
      message("#result", result.status === "HOLD" ? `선택 ${r.pick}를 기록했습니다. 법규·시점 HOLD로 정답 판정과 점수 집계를 하지 않습니다.` : result.matches ? `선택 ${r.pick}: 작성자 제안 답과 일치합니다. 초안 답 기준이며 정식 검증 완료를 뜻하지 않습니다.` : `선택 ${r.pick}: 작성자 제안 답과 다릅니다. 제안 답 ${q.proposed_key[0]}의 해설과 공식 근거를 검토해 주세요.`);
      $("#result").hidden = false; showExplanation(q); stats(); updateList();
    } catch (error) { message("#result", error.message); $("#result").hidden = false; }
  }
  function matches(q) {
    const scope = $("#scope").value, r = records[q.id];
    if (scope === "unanswered" && r?.checked) return false;
    if (scope === "bookmarked" && !r?.bookmarked) return false;
    if (scope === "hold" && q.review_status !== "LEGAL_HOLD") return false;
    if (scope === "wrong" && (!r?.checked || core.grade(q, r.pick).matches !== false)) return false;
    const query = $("#search").value.trim().toLocaleLowerCase();
    return !query || [q.title, q.stem, q.core_ko, ...q.choices.map(c => c.text), ...Object.values(q.analysis_ko)].join(" ").toLocaleLowerCase().includes(query);
  }
  function updateList() {
    const list = $("#question-list"); list.replaceChildren();
    for (const id of active) {
      const q = byId.get(id), r = records[id]; const button = element("button", String(questions.indexOf(q) + 1)); button.type = "button";
      button.dataset.questionId = id; button.setAttribute("aria-label", `초안 ${questions.indexOf(q) + 1}: ${q.title}`); button.setAttribute("aria-current", String(id === current));
      if (r?.checked) button.classList.add("answered"); if (q.scoring_policy === "NO_GRADE") button.classList.add("held");
      button.addEventListener("click", () => select(id, true, true)); list.append(button);
    }
  }
  function applyFilters(preferred = current) {
    active = order.filter(id => matches(byId.get(id)));
    if (!active.length) { current = ""; $("#question-panel").hidden = true; $("#empty").hidden = false; updateList(); return; }
    select(active.includes(preferred) ? preferred : active[0]);
  }
  $("#choices").addEventListener("submit", e => { e.preventDefault(); if (current) showResult(); });
  $("#check").addEventListener("click", () => showResult());
  $("#reveal").addEventListener("click", () => showExplanation(byId.get(current)));
  $("#previous").addEventListener("click", () => select(active[active.indexOf(current) - 1], true, true));
  $("#next").addEventListener("click", () => select(active[active.indexOf(current) + 1], true, true));
  $("#note").addEventListener("input", () => { record(byId.get(current)).note = $("#note").value; persist(); });
  $("#bookmark").addEventListener("click", () => { const r = record(byId.get(current)); r.bookmarked = !r.bookmarked; persist(); select(current, false); });
  $("#search").addEventListener("input", () => applyFilters()); $("#scope").addEventListener("change", () => applyFilters());
  $("#shuffle").addEventListener("click", () => { for (let i = order.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [order[i], order[j]] = [order[j], order[i]]; } applyFilters(order[0]); });
  $("#export").addEventListener("click", () => {
    const data = { format: backupFormat, edition: "2026-11-06.draft33", exported_at: new Date().toISOString(), records: Object.values(records) };
    const url = URL.createObjectURL(new Blob([JSON.stringify(data, null, 2)], { type: "application/json" })); const link = element("a"); link.href = url; link.download = "mpje-draft33-practice-backup.json"; link.click(); setTimeout(() => URL.revokeObjectURL(url), 1000);
    message("#backup-status", "연습 기록을 파일로 내보냈습니다. 선택·메모는 서버로 전송하지 않습니다.");
  });
  $("#import").addEventListener("change", async event => {
    const file = event.target.files[0]; if (!file) return;
    try {
      if (file.size > 2 * 1024 * 1024) throw new Error("2MB 이하 백업만 불러올 수 있습니다.");
      const data = JSON.parse(await file.text());
      if (data?.format !== backupFormat || data.edition !== "2026-11-06.draft33") throw new Error("이 초안 연습판의 백업 파일을 선택해 주세요. 기존 문제은행 백업은 변경하지 않습니다.");
      const next = core.validateRecords(data.records, questions); records = Object.assign(Object.create(null), records, next); persist(); stats(); applyFilters();
      message("#backup-status", "현재 문항·버전이 일치하는 연습 기록을 불러왔습니다.");
    } catch (error) { message("#backup-status", error.message || "백업을 불러오지 못했습니다."); }
    finally { event.target.value = ""; }
  });
  window.addEventListener("hashchange", () => {
    let id; try { id = decodeURIComponent(location.hash.slice(1)); } catch (_) { id = ""; }
    if (byId.has(id)) { $("#scope").value = "all"; $("#search").value = ""; applyFilters(id); }
    else {
      $("#scope").value = "all"; $("#search").value = ""; applyFilters(order[0]);
      message("#load-status", "요청한 문항을 찾지 못해 첫 문항을 열었습니다. 공개 초안 33개 · 제안 답 채점 32개 · HOLD 1개");
    }
  });
  try {
    const response = await fetch("questions.json", { cache: "no-store" }); if (!response.ok) throw new Error("초안 문항 파일을 불러오지 못했습니다.");
    const payload = core.validate(await response.json()); await core.verifyHashes(payload, crypto.subtle);
    questions = payload.questions; for (const q of questions) byId.set(q.id, q); order = questions.map(q => q.id);
    try { records = core.validateRecords(JSON.parse(localStorage.getItem(storageKey) || "[]"), questions); }
    catch (_) { storageAvailable = false; $("#storage-warning").hidden = false; }
    let requested; try { requested = decodeURIComponent(location.hash.slice(1)); } catch (_) { requested = ""; }
    message("#load-status", requested && !byId.has(requested) ? "요청한 문항을 찾지 못해 첫 문항을 열었습니다. 공개 초안 33개 · 제안 답 채점 32개 · HOLD 1개" : "공개 초안 33개 · 제안 답 채점 32개 · 법규·시점 HOLD 1개");
    applyFilters(byId.has(requested) ? requested : order[0]); stats();
    for (const selector of ["#shuffle", "#export", "#import"]) $(selector).disabled = false;
  } catch (error) {
    $("#question-panel").hidden = true; $("#question-list").replaceChildren(); message("#load-status", "초안 연습을 열 수 없습니다."); message("#load-error", error.message || "새로고침 후 다시 시도해 주세요."); $("#load-error").hidden = false;
  }
})();
