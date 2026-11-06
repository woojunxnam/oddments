"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const crypto = require("node:crypto");
const core = require("../site/draft-practice/core.js");
const payload = JSON.parse(fs.readFileSync(path.join(__dirname, "../site/draft-practice/questions.json"), "utf8"));
const copy = value => JSON.parse(JSON.stringify(value));

test("all33 public draft records have exact deterministic hashes and no canonical release credit", async () => {
  assert.equal(core.validate(payload), payload);
  await core.verifyHashes(payload, crypto.webcrypto.subtle);
  assert.equal(payload.canonical_released_question_count, 0);
  assert.equal(new Set(payload.questions.map(q => q.id)).size, 33);
});

test("all32 proposed-key comparisons distinguish matching and nonmatching choices", () => {
  const gradable = payload.questions.filter(q => q.scoring_policy === "PROPOSED_KEY");
  assert.equal(gradable.length, 32);
  for (const q of gradable) {
    for (const c of q.choices) assert.equal(core.grade(q, c.id).matches, q.proposed_key.includes(c.id));
    assert.throws(() => core.grade(q, ""));
  }
});

test("current operating-date HOLD is never graded, including proposed-key/metadata override attempts", () => {
  const q = payload.questions.find(q => q.id === "MA-DRAFT33-010");
  for (const c of q.choices) assert.deepEqual(core.grade(q, c.id), { status: "HOLD", matches: null });
  assert.equal(core.grade({ ...q, scoring_policy: "PROPOSED_KEY" }, "B").status, "HOLD");
  assert.equal(core.grade({ ...q, review_status: "AUDIT_PENDING" }, "B").status, "HOLD");
  const records = Object.fromEntries(payload.questions.map(q => [q.id, { ...core.emptyRecord(q), pick: q.proposed_key[0], checked: true }]));
  assert.deepEqual(core.summary(payload.questions, records), { answered: 33, matched: 32, mismatched: 0, held: 1 });
});

test("source or payload mutations fail closed instead of changing a legal HOLD into a score", async () => {
  const negative = [
    d => d.canonical_released_question_count = 33,
    d => d.questions[9].scoring_policy = "PROPOSED_KEY",
    d => d.questions[9].review_status = "AUDIT_PENDING",
    d => d.questions[0].id = d.questions[1].id,
    d => d.questions[0].authorities[0].url = "javascript:alert(1)",
    d => d.questions[0].authorities[0].url = "https://www.mass.gov.example.com/",
    d => d.questions[0].private_source_path = "unexpected",
    d => d.questions[0].proposed_key = ["AB"],
    d => d.questions[0].analysis_ko = { "A|B|C|D": "합쳐진 잘못된 해설" },
  ];
  for (const mutate of negative) { const d = copy(payload); mutate(d); assert.throws(() => core.validate(d)); }
  const d = copy(payload); d.questions[0].analysis_ko.A += " altered";
  await assert.rejects(core.verifyHashes(d, crypto.webcrypto.subtle));
});

test("backup imports reject stale/foreign/duplicate/forged-score records without mutating current state", () => {
  const q = payload.questions[0]; const original = { ...core.emptyRecord(q), pick: "A", checked: true, note: "원래 메모" };
  const before = JSON.stringify(original);
  const variants = [
    { ...original, content_hash: "0".repeat(64) },
    { ...original, id: "MA-Q-0001" },
    { ...original, pick: "E" },
    { ...original, matched: true },
    { ...original, checked: true, pick: "" },
    { ...original, note: "x".repeat(10001) },
  ];
  for (const r of variants) assert.throws(() => core.validateRecords([r], payload.questions));
  assert.throws(() => core.validateRecords([original, original], payload.questions));
  assert.equal(JSON.stringify(original), before);
});

test("valid comments remain literal and stale stored hashes cannot receive score credit", () => {
  const q = payload.questions[0];
  const r = { ...core.emptyRecord(q), note: '<img onerror="alert(1)"> 의견 😀', bookmarked: true, pick: "A", checked: true };
  const parsed = core.validateRecords([r], payload.questions);
  assert.equal(parsed[q.id].note, r.note);
  assert.notEqual(parsed[q.id], r);
  assert.equal(core.summary(payload.questions, { [q.id]: { ...r, content_hash: "0".repeat(64) } }).answered, 0);
});
