const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const crypto = require("node:crypto");
const collections = require("../site/verified-law/collections.js");
const { isReleaseUsable } = require("../site/session.js");
const root = path.resolve(__dirname, "..");
const payload = JSON.parse(fs.readFileSync(path.join(root, "site/generated/questions.json"), "utf8"));
const manifest = JSON.parse(fs.readFileSync(path.join(root, "site/verified-law/sets.json"), "utf8"));
const overlay = JSON.parse(fs.readFileSync(path.join(root, "site/verified-law/delivery-holds.json"), "utf8"));
const clone = (value) => JSON.parse(JSON.stringify(value));
const contextFor = (data = payload, holds = overlay) => collections.validateDeliveryHolds(data, holds, isReleaseUsable);
const validate = (data = payload, sets = manifest) => collections.validateManifest(data, sets, isReleaseUsable, contextFor(data));
const resolve = (search, data = payload, sets = manifest) => collections.resolveSelection(data, sets, search, isReleaseUsable, contextFor(data));

test("actual public selections bind released canonical IDs and exact content hashes without changing source objects", () => {
  const before = JSON.stringify({ payload, manifest });
  const sets = validate();
  assert.ok(sets.length > 0);
  for (const set of sets) {
    assert.equal(new Set(set.questionIds).size, set.questionIds.length);
    assert.ok(set.resolvedQuestions.every(isReleaseUsable));
    assert.deepEqual(resolve(`?set=${set.id}`).questionIds, set.questionIds);
    assert.equal(resolve(`?set=${set.id}&question=${set.questionIds[0]}`).initialQuestionId, set.questionIds[0]);
  }
  assert.equal(JSON.stringify({ payload, manifest }), before);
});

test("direct IDs also support released canonical questions outside the small topic selection", () => {
  const selected = new Set(manifest.sets.flatMap((set) => set.questions.map((question) => question.question_id)));
  const outside = payload.questions.find((question) => !selected.has(question.question_id) && collections.isDeliveryUsable(question, isReleaseUsable, contextFor()));
  assert.ok(outside);
  assert.deepEqual(resolve(`?question=${outside.question_id}`).questionIds, [outside.question_id]);
});

test("ordinary URLs keep the original bank available without loading a collection manifest", () => {
  assert.deepEqual(resolve("?seed=existing", payload, null), { requested: false, questionIds: null, initialQuestionId: null, set: null });
});

test("unknown, quarantined, malformed, empty and repeated query selections fail closed", () => {
  for (const search of ["?question=MA-Q-9999", "?question=MA-Q-0012", "?question=MA-Q-0028", "?question=wrong", "?question=", "?set=", "?set=unknown-set", "?set=../data", "?question=MA-Q-0103&question=MA-Q-0252", "?set=licensing-and-renewal&set=personnel-and-scope"]) {
    assert.throws(() => resolve(search), search);
  }
  const firstIds = new Set(manifest.sets[0].questions.map((question) => question.question_id));
  const outside = payload.questions.find((question) => !firstIds.has(question.question_id));
  assert.throws(() => resolve(`?set=${manifest.sets[0].id}&question=${outside.question_id}`));
});

test("a stale content binding cannot silently drop a question or fall back to the full bank", () => {
  const stale = clone(manifest); stale.sets[0].questions[0].question_content_hash = "0".repeat(64);
  assert.throws(() => resolve(`?set=${stale.sets[0].id}`, payload, stale));
});

test("unreleased status, duplicate IDs and development payloads are rejected", () => {
  const held = clone(payload); const id = manifest.sets[0].questions[0].question_id;
  held.questions.find((question) => question.question_id === id).lifecycle_status = "REVIEW_REQUIRED";
  assert.throws(() => resolve(`?question=${id}`, held));
  const duplicate = clone(payload); duplicate.questions.push(duplicate.questions[0]);
  assert.throws(() => resolve(`?question=${id}`, duplicate));
  const development = clone(payload); development.meta.development_fixture_mode = true;
  assert.throws(() => resolve(`?question=${id}`, development));
  assert.throws(() => collections.validateManifest(payload, manifest));
});

test("duplicate references, unsafe note paths and unknown manifest versions are rejected", () => {
  const duplicate = clone(manifest); duplicate.sets[0].questions.push(duplicate.sets[0].questions[0]);
  assert.throws(() => validate(payload, duplicate));
  const unsafe = clone(manifest); unsafe.sets[0].notes[0].chapter_id = "../other";
  assert.throws(() => validate(payload, unsafe));
  const unknown = clone(manifest); unknown.schema_version = "future";
  assert.throws(() => validate(payload, unknown));
});

test("public collection data rejects hidden extra fields and private reference text", () => {
  const hidden = clone(manifest); hidden.sets[0].private_reference = "unexpected";
  assert.throws(() => validate(payload, hidden));
  const privateText = clone(manifest); privateText.sets[0].description = "IMG_" + String(9999);
  assert.throws(() => validate(payload, privateText));
  const privateLink = clone(manifest); privateLink.sets[0].description = "https://" + "drive.google.com/example";
  assert.throws(() => validate(payload, privateLink));
});

test("actual delivery holds preserve the reviewed negative IDs without changing canonical eligibility fields", () => {
  const original = JSON.parse(fs.readFileSync(path.join(root, "reports/coverage336/public-set-review.json"), "utf8"));
  const addendum = JSON.parse(fs.readFileSync(path.join(root, "reports/coverage336/public-two-item-addendum.json"), "utf8"));
  const knownNegativeIds = [
    ...original.results.filter((item) => item.recommendation !== "INCLUDE_UNCHANGED_PUBLIC_ITEM").map((item) => item.question_id),
    ...addendum.results.filter((item) => item.curated_delivery_recommendation === "EXCLUDE").map((item) => item.question_id),
  ];
  const heldIds = new Set(overlay.holds.map((item) => item.question_id));
  assert.ok(knownNegativeIds.every((id) => heldIds.has(id)), "previously reviewed negatives cannot disappear silently");
  for (const review of overlay.reviews) {
    const relative = new URL(review.url).pathname.split("/").slice(5).join("/");
    const bytes = fs.readFileSync(path.join(root, relative));
    assert.equal(crypto.createHash("sha256").update(bytes).digest("hex"), review.source_sha256);
  }
  const context = contextFor();
  assert.equal(context.heldCount, overlay.holds.length);
  for (const hold of overlay.holds) {
    const question = payload.questions.find((item) => item.question_id === hold.question_id);
    assert.equal(question.question_content_hash, hold.question_content_hash);
    assert.equal(isReleaseUsable(question), true, "the delivery overlay must not edit canonical status");
    assert.equal(collections.isDeliveryUsable(question, isReleaseUsable, context), false);
    assert.throws(() => resolve(`?question=${hold.question_id}`), (error) => error.deliveryHold.question_id === hold.question_id);
  }
});

test("missing, malformed or stale delivery overlays fail closed instead of carrying or removing a hold", () => {
  assert.throws(() => contextFor(payload, null));
  assert.throws(() => collections.resolveSelection(payload, null, "", isReleaseUsable));
  const stale = clone(overlay); stale.holds[0].question_content_hash = "0".repeat(64);
  assert.throws(() => contextFor(payload, stale));
  const changed = clone(payload);
  changed.questions.find((question) => question.question_id === overlay.holds[0].question_id).question_content_hash = "f".repeat(64);
  assert.throws(() => contextFor(changed));
  const unknown = clone(overlay); unknown.holds[0].question_id = "MA-Q-9999";
  assert.throws(() => contextFor(payload, unknown));
  const duplicate = clone(overlay); duplicate.holds.push(duplicate.holds[0]);
  assert.throws(() => contextFor(payload, duplicate));
  const badReview = clone(overlay); badReview.holds[0].review_id = "MISSING-REVIEW";
  assert.throws(() => contextFor(payload, badReview));
  const hidden = clone(overlay); hidden.private_reference = "unexpected";
  assert.throws(() => contextFor(payload, hidden));
  const privateText = clone(overlay); privateText.holds[0].reason = "IMG_" + String(9999);
  assert.throws(() => contextFor(payload, privateText));
});

test("additional editorial holds work without a fixed hold count or silent selected-set inclusion", () => {
  const extra = clone(overlay);
  const reference = manifest.sets[0].questions[0];
  extra.holds.push({ ...extra.holds[0], ...reference, category: "EDITORIAL_HOLD", reason: "Test-only editorial hold", review_reason: "Test-only synthetic hold contract" });
  const context = contextFor(payload, extra);
  assert.equal(context.heldCount, overlay.holds.length + 1);
  assert.throws(() => collections.validateManifest(payload, manifest, isReleaseUsable, context));
  const question = payload.questions.find((item) => item.question_id === reference.question_id);
  assert.equal(collections.isDeliveryUsable(question, isReleaseUsable, context), false);
});
