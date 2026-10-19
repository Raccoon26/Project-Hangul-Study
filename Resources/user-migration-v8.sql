CREATE TABLE listening_sessions (
 id TEXT PRIMARY KEY NOT NULL, scope TEXT NOT NULL, state_json TEXT NOT NULL,
 completed INTEGER NOT NULL CHECK(completed IN (0,1))
);
CREATE UNIQUE INDEX idx_listening_active ON listening_sessions(scope) WHERE completed=0;
CREATE TABLE listening_attempts (
 session_id TEXT NOT NULL REFERENCES listening_sessions(id), question_id TEXT NOT NULL,
 attempt INTEGER NOT NULL CHECK(attempt IN (0,1)), item_id TEXT NOT NULL,
 task TEXT NOT NULL, answer TEXT NOT NULL, result TEXT NOT NULL,
 is_review INTEGER NOT NULL CHECK(is_review IN (0,1)), occurred_at REAL NOT NULL,
 next_due_at REAL, PRIMARY KEY(session_id,question_id,attempt)
);
CREATE INDEX idx_listening_attempt_item ON listening_attempts(item_id,occurred_at);
CREATE TABLE listening_plays (
 session_id TEXT NOT NULL REFERENCES listening_sessions(id), question_id TEXT NOT NULL,
 normal_count INTEGER NOT NULL DEFAULT 0, slow_count INTEGER NOT NULL DEFAULT 0,
 last_played_at REAL NOT NULL, PRIMARY KEY(session_id,question_id)
);
CREATE INDEX idx_srs_skill_date ON srs_state(skill,due_at,content_id) WHERE due_at IS NOT NULL;
PRAGMA user_version=8;
