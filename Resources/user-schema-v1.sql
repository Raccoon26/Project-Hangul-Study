-- No foreign keys to the replaceable content database. Missing content must never delete progress.
CREATE TABLE user_metadata (key TEXT PRIMARY KEY NOT NULL, value TEXT NOT NULL);
CREATE TABLE item_progress (
 content_id TEXT PRIMARY KEY NOT NULL, first_seen_at REAL NOT NULL, last_seen_at REAL NOT NULL,
 study_count INTEGER NOT NULL DEFAULT 0 CHECK(study_count>=0), correct_count INTEGER NOT NULL DEFAULT 0 CHECK(correct_count>=0),
 incorrect_count INTEGER NOT NULL DEFAULT 0 CHECK(incorrect_count>=0), completed_passes INTEGER NOT NULL DEFAULT 0 CHECK(completed_passes>=0),
 CHECK(correct_count+incorrect_count<=study_count)
);
CREATE TABLE srs_state (
 content_id TEXT NOT NULL, skill TEXT NOT NULL, algorithm TEXT NOT NULL, algorithm_version INTEGER NOT NULL CHECK(algorithm_version>=1),
 state_json TEXT NOT NULL, due_at REAL, last_review_at REAL, updated_at REAL NOT NULL,
 PRIMARY KEY(content_id,skill)
);
CREATE INDEX idx_srs_due ON srs_state(due_at,content_id) WHERE due_at IS NOT NULL;
CREATE TABLE favorites (content_id TEXT PRIMARY KEY NOT NULL, created_at REAL NOT NULL);
CREATE TABLE study_events (
 id TEXT PRIMARY KEY NOT NULL, content_id TEXT NOT NULL, content_revision INTEGER NOT NULL CHECK(content_revision>=1),
 occurred_at REAL NOT NULL, local_day TEXT NOT NULL, time_zone TEXT NOT NULL, skill TEXT NOT NULL,
 outcome TEXT NOT NULL CHECK(outcome IN ('correct','incorrect','viewed','skipped')), duration_ms INTEGER NOT NULL CHECK(duration_ms>=0),
 session_id TEXT, content_version INTEGER NOT NULL CHECK(content_version>=1)
);
CREATE INDEX idx_events_item_date ON study_events(content_id,occurred_at);
CREATE INDEX idx_events_day ON study_events(local_day,outcome);
CREATE TABLE learning_passes (id TEXT PRIMARY KEY NOT NULL, scope_content_id TEXT NOT NULL, started_at REAL NOT NULL, completed_at REAL, pass_number INTEGER NOT NULL CHECK(pass_number>=1), UNIQUE(scope_content_id,pass_number));
CREATE TABLE pass_items (pass_id TEXT NOT NULL REFERENCES learning_passes(id), content_id TEXT NOT NULL, completed_at REAL, PRIMARY KEY(pass_id,content_id));
CREATE TABLE lesson_progress (lesson_id TEXT PRIMARY KEY NOT NULL, status TEXT NOT NULL CHECK(status IN ('started','completed')), started_at REAL NOT NULL, completed_at REAL, last_content_id TEXT);
CREATE TABLE daily_statistics (local_day TEXT NOT NULL, time_zone TEXT NOT NULL, study_count INTEGER NOT NULL CHECK(study_count>=0), correct_count INTEGER NOT NULL CHECK(correct_count>=0), incorrect_count INTEGER NOT NULL CHECK(incorrect_count>=0), duration_ms INTEGER NOT NULL CHECK(duration_ms>=0), PRIMARY KEY(local_day,time_zone));
PRAGMA user_version = 1;
