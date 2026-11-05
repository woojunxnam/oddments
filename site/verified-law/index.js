"use strict";

(async () => {
  const status = document.querySelector("#collection-status");
  const error = document.querySelector("#collection-error");
  const container = document.querySelector("#collections");
  function link(text, href) {
    const anchor = document.createElement("a"); anchor.textContent = text; anchor.href = href; return anchor;
  }
  try {
    const [payload, manifest, overlay] = await Promise.all(["../generated/questions.json", "sets.json", "delivery-holds.json"].map(async (path) => {
      const response = await fetch(path, { cache: "no-store" });
      if (!response.ok) throw new Error("학습 목록을 불러오지 못했습니다. 잠시 후 다시 시도해 주세요.");
      return response.json();
    }));
    const delivery = MpjeCollections.validateDeliveryHolds(payload, overlay, MpjeSessions.isReleaseUsable);
    const sets = MpjeCollections.validateManifest(payload, manifest, MpjeSessions.isReleaseUsable, delivery);
    for (const set of sets) {
      const card = document.createElement("article"); card.className = "collection-card"; card.dataset.setId = set.id;
      const heading = document.createElement("h2"); heading.textContent = set.title;
      const description = document.createElement("p"); description.textContent = set.description;
      const count = document.createElement("p"); count.textContent = `기존 승인 문항 ${set.questionIds.length}개`;
      const start = link("이 묶음 학습 시작 →", `../?${new URLSearchParams({ set: set.id })}`); start.className = "collection-start ghost-button";
      const list = document.createElement("ol");
      for (const question of set.resolvedQuestions) {
        const item = document.createElement("li");
        item.append(link(question.subtopic || question.topic, `../?${new URLSearchParams({ set: set.id, question: question.question_id })}`)); list.append(item);
      }
      card.append(heading, description, count, start, list);
      if (set.notes.length) {
        const label = document.createElement("h3"); label.textContent = "연결된 통합 노트";
        const notes = document.createElement("ul");
        for (const note of set.notes) {
          const item = document.createElement("li");
          item.append(link(note.title, `../notes/#chapter/${encodeURIComponent(note.chapter_id)}/${encodeURIComponent(note.unit_id)}`)); notes.append(item);
        }
        card.append(label, notes);
      }
      container.append(card);
    }
    const unique = new Set(sets.flatMap((set) => set.questionIds));
    status.textContent = `${sets.length}개 학습 묶음 · 기존 승인 문항 ${unique.size}개`;
  } catch (failure) {
    container.replaceChildren(); status.textContent = "학습 목록을 열 수 없습니다.";
    error.hidden = false; error.textContent = failure.message || "학습 목록을 확인해 주세요.";
  }
})();
