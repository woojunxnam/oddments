from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

import pytest


def node_binary() -> str | None:
    return os.environ.get("NODE_BIN") or shutil.which("node")


@pytest.mark.skipif(node_binary() is None, reason="Node.js is required to execute website session modules")
def test_quick20_quotas_freshness_and_result_persistence(root: Path) -> None:
    script = r"""
const fs = require('fs');
const questions = JSON.parse(fs.readFileSync(process.argv[1], 'utf8')).questions;
require(process.argv[2]);
const sessions = require(process.argv[3]);

const first = sessions.createQuick20(questions, 'quick-seed-one');
const repeat = sessions.createQuick20(questions, 'quick-seed-one');
const second = sessions.createQuick20(questions, 'quick-seed-two');
if (first.length !== 20) throw new Error('Quick20 length is not 20');
const counts = first.reduce((result, question) => { result[question.area] = (result[question.area] || 0) + 1; return result; }, {});
if (JSON.stringify(counts) !== JSON.stringify({'1':4,'2':7,'3':5,'4':4})) throw new Error(`Unexpected quotas ${JSON.stringify(counts)}`);
if (!first.every(sessions.isReleaseUsable)) throw new Error('Unreleased question entered Quick20');
if (JSON.stringify(first.map((q) => q.question_id)) !== JSON.stringify(repeat.map((q) => q.question_id))) throw new Error('Same seed is not stable');
if (JSON.stringify(first.map((q) => q.question_id)) === JSON.stringify(second.map((q) => q.question_id))) throw new Error('Fresh seed did not create a new session');

const responses = first.map((question, index) => ({ selected: [question.correct_choice_ids[0]], order: [], answered: true, revealed: false, correct: index % 4 !== 0 }));
const record = sessions.buildCompletedSession({
  sessionId: 'session-test-1', examType: 'QUICK_20', sessionSeed: 'quick-seed-one',
  startedAt: '2026-09-01T12:00:00.000Z', completedAt: '2026-09-01T12:10:00.000Z', queue: first, responses,
});
if (record.score.correct !== 15 || record.score.total !== 20 || record.elapsed_seconds !== 600) throw new Error('Result summary is incorrect');
if (record.missed_question_ids.length !== 5) throw new Error('Missed list is incorrect');
if (!record.question_ids.every((id) => record.question_content_hashes[id])) throw new Error('Question hashes were not preserved');

const memory = new Map();
global.localStorage = { getItem: (key) => memory.has(key) ? memory.get(key) : null, setItem: (key, value) => memory.set(key, String(value)) };
global.indexedDB = undefined;
const storage = require(process.argv[4]);
(async () => {
  await storage.saveSession(record);
  const history = await storage.listSessions();
  if (history.length !== 1 || history[0].session_id !== record.session_id) throw new Error('Fallback history persistence failed');
  const bundle = await storage.exportData({ theme: 'system' });
  if (bundle.version !== 2 || bundle.exam_history.length !== 1) throw new Error('Export bundle is invalid');
  if (!storage.validateExportBundle({...bundle, version: 999})) throw new Error('Incompatible import version was accepted');
  await storage.importData(bundle);
  if ((await storage.listSessions()).length !== 1) throw new Error('Import did not preserve session identity');
})().catch((error) => { console.error(error); process.exit(1); });
"""
    result = subprocess.run(
        [
            node_binary(),
            "-e",
            script,
            str(root / "site" / "generated" / "questions.json"),
            str(root / "site" / "shuffle.js"),
            str(root / "site" / "session.js"),
            str(root / "site" / "storage.js"),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
