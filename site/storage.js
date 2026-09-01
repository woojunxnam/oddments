(function (globalScope) {
  "use strict";

  const EXPORT_SCHEMA = "MA_MPJE_STUDY_DATA";
  const EXPORT_VERSION = 2;
  const DB_NAME = "ma-mpje-study-v2";
  const SESSION_STORE = "exam_sessions";
  const PROGRESS_KEY = "ma-mpje-progress-v2";
  const LEGACY_PROGRESS_KEY = "ma-mpje-progress-v1";
  const FALLBACK_SESSION_KEY = "ma-mpje-sessions-v2";

  function defaultProgress() {
    return { wrong: [], bookmarks: [], completed: [], byArea: {}, byTopic: {}, byDifficulty: {} };
  }

  function getLocalStorage() {
    return globalScope.localStorage;
  }

  function normalizeProgress(value) {
    const base = defaultProgress();
    if (!value || typeof value !== "object") return base;
    ["wrong", "bookmarks", "completed"].forEach((field) => {
      if (Array.isArray(value[field])) base[field] = [...new Set(value[field].filter((item) => typeof item === "string"))];
    });
    ["byArea", "byTopic", "byDifficulty"].forEach((field) => {
      if (value[field] && typeof value[field] === "object" && !Array.isArray(value[field])) base[field] = value[field];
    });
    return base;
  }

  function loadProgress() {
    const storage = getLocalStorage();
    try {
      const current = storage.getItem(PROGRESS_KEY);
      if (current) return normalizeProgress(JSON.parse(current));
      const legacy = storage.getItem(LEGACY_PROGRESS_KEY);
      const migrated = normalizeProgress(legacy ? JSON.parse(legacy) : null);
      storage.setItem(PROGRESS_KEY, JSON.stringify(migrated));
      return migrated;
    } catch (_error) {
      return defaultProgress();
    }
  }

  function saveProgress(progress) {
    getLocalStorage().setItem(PROGRESS_KEY, JSON.stringify(normalizeProgress(progress)));
  }

  function openDatabase() {
    if (!globalScope.indexedDB) return Promise.resolve(null);
    return new Promise((resolve, reject) => {
      const request = globalScope.indexedDB.open(DB_NAME, 1);
      request.onupgradeneeded = () => {
        const database = request.result;
        if (!database.objectStoreNames.contains(SESSION_STORE)) {
          const store = database.createObjectStore(SESSION_STORE, { keyPath: "session_id" });
          store.createIndex("completed_at", "completed_at");
        }
      };
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
  }

  function fallbackSessions() {
    try {
      return JSON.parse(getLocalStorage().getItem(FALLBACK_SESSION_KEY)) || [];
    } catch (_error) {
      return [];
    }
  }

  async function saveSession(session) {
    const error = globalScope.MpjeSessions?.validateSessionRecord(session);
    if (error) throw new Error(error);
    const database = await openDatabase();
    if (!database) {
      const sessions = fallbackSessions().filter((item) => item.session_id !== session.session_id);
      sessions.push(session);
      getLocalStorage().setItem(FALLBACK_SESSION_KEY, JSON.stringify(sessions));
      return session;
    }
    return new Promise((resolve, reject) => {
      const transaction = database.transaction(SESSION_STORE, "readwrite");
      transaction.objectStore(SESSION_STORE).put(session);
      transaction.oncomplete = () => { database.close(); resolve(session); };
      transaction.onerror = () => { database.close(); reject(transaction.error); };
    });
  }

  async function listSessions() {
    const database = await openDatabase();
    if (!database) return fallbackSessions().sort((left, right) => right.completed_at.localeCompare(left.completed_at));
    return new Promise((resolve, reject) => {
      const transaction = database.transaction(SESSION_STORE, "readonly");
      const request = transaction.objectStore(SESSION_STORE).getAll();
      request.onsuccess = () => resolve(request.result.sort((left, right) => right.completed_at.localeCompare(left.completed_at)));
      request.onerror = () => reject(request.error);
      transaction.oncomplete = () => database.close();
    });
  }

  async function getSession(sessionId) {
    const database = await openDatabase();
    if (!database) return fallbackSessions().find((session) => session.session_id === sessionId) || null;
    return new Promise((resolve, reject) => {
      const transaction = database.transaction(SESSION_STORE, "readonly");
      const request = transaction.objectStore(SESSION_STORE).get(sessionId);
      request.onsuccess = () => resolve(request.result || null);
      request.onerror = () => reject(request.error);
      transaction.oncomplete = () => database.close();
    });
  }

  function validateExportBundle(bundle) {
    if (!bundle || typeof bundle !== "object") return "Import must be a JSON object";
    if (bundle.schema !== EXPORT_SCHEMA) return `Expected schema ${EXPORT_SCHEMA}`;
    if (bundle.version !== EXPORT_VERSION) return `Unsupported study-data version ${bundle.version}`;
    if (!bundle.progress || typeof bundle.progress !== "object") return "Import is missing progress";
    if (!Array.isArray(bundle.exam_history)) return "Import is missing exam_history";
    for (const session of bundle.exam_history) {
      const error = globalScope.MpjeSessions?.validateSessionRecord(session);
      if (error) return `Invalid session ${session?.session_id || "unknown"}: ${error}`;
    }
    if (bundle.preferences && (typeof bundle.preferences !== "object" || Array.isArray(bundle.preferences))) return "Import preferences are invalid";
    return null;
  }

  async function exportData(preferences = {}) {
    return {
      schema: EXPORT_SCHEMA,
      version: EXPORT_VERSION,
      exported_at: new Date().toISOString(),
      preferences,
      progress: loadProgress(),
      bookmarks: loadProgress().bookmarks,
      wrong_questions: loadProgress().wrong,
      exam_history: await listSessions(),
    };
  }

  async function importData(bundle) {
    const error = validateExportBundle(bundle);
    if (error) throw new Error(error);
    saveProgress(normalizeProgress(bundle.progress));
    for (const session of bundle.exam_history) await saveSession(session);
    return { imported_sessions: bundle.exam_history.length, progress: loadProgress() };
  }

  const api = {
    EXPORT_SCHEMA,
    EXPORT_VERSION,
    defaultProgress,
    normalizeProgress,
    loadProgress,
    saveProgress,
    saveSession,
    listSessions,
    getSession,
    validateExportBundle,
    exportData,
    importData,
  };
  globalScope.MpjeStorage = api;
  if (typeof module !== "undefined" && module.exports) module.exports = api;
})(typeof window !== "undefined" ? window : globalThis);
