(function (globalScope) {
  "use strict";

  function seedToNumber(seed) {
    const text = String(seed);
    let hash = 2166136261;
    for (let index = 0; index < text.length; index += 1) {
      hash ^= text.charCodeAt(index);
      hash = Math.imul(hash, 16777619);
    }
    return hash >>> 0;
  }

  function mulberry32(seed) {
    let state = seed >>> 0;
    return function random() {
      state += 0x6d2b79f5;
      let value = state;
      value = Math.imul(value ^ (value >>> 15), value | 1);
      value ^= value + Math.imul(value ^ (value >>> 7), value | 61);
      return ((value ^ (value >>> 14)) >>> 0) / 4294967296;
    };
  }

  function seededShuffle(values, seed) {
    const shuffled = values.map((value) => ({ ...value }));
    const random = mulberry32(seedToNumber(seed));
    for (let index = shuffled.length - 1; index > 0; index -= 1) {
      const target = Math.floor(random() * (index + 1));
      [shuffled[index], shuffled[target]] = [shuffled[target], shuffled[index]];
    }
    return shuffled;
  }

  function shuffleQuestionChoices(question, seed) {
    const clone = JSON.parse(JSON.stringify(question));
    if (clone.question_type === "ORDERED_RESPONSE") {
      clone.choices = clone.choices.map((choice) => ({ ...choice, source_id: choice.id }));
      return clone;
    }

    const canonicalAnalysis = clone.explanation.choice_analysis;
    const shuffled = seededShuffle(clone.choices, `${seed}:${clone.question_id}`);
    const displayAnalysis = {};
    const sourceToDisplay = {};
    clone.choices = shuffled.map((choice, index) => {
      const displayId = String.fromCharCode(65 + index);
      sourceToDisplay[choice.id] = displayId;
      displayAnalysis[displayId] = canonicalAnalysis[choice.id];
      return { ...choice, source_id: choice.id, id: displayId };
    });
    clone.correct_choice_ids = clone.correct_choice_ids.map((sourceId) => sourceToDisplay[sourceId]).sort();
    clone.explanation.choice_analysis = displayAnalysis;
    return clone;
  }

  const api = { seedToNumber, seededShuffle, shuffleQuestionChoices };
  globalScope.MpjeShuffle = api;
  if (typeof module !== "undefined" && module.exports) {
    module.exports = api;
  }
})(typeof window !== "undefined" ? window : globalThis);
