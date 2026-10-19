-- Content IDs intentionally have no foreign keys into Content.sqlite.
ALTER TABLE lesson_progress ADD COLUMN completed_count INTEGER NOT NULL DEFAULT 0 CHECK(completed_count>=0);
UPDATE lesson_progress SET completed_count=1 WHERE status='completed';
CREATE TABLE lesson_sessions (
 id TEXT PRIMARY KEY NOT NULL, lesson_id TEXT NOT NULL, content_version INTEGER NOT NULL CHECK(content_version>0),
 seed INTEGER NOT NULL CHECK(seed>=0), step_ids_json TEXT NOT NULL,
 current_content_id TEXT NOT NULL, status TEXT NOT NULL CHECK(status IN ('active','completed','abandoned')),
 started_at REAL NOT NULL, updated_at REAL NOT NULL, completed_at REAL
);
CREATE UNIQUE INDEX idx_one_active_lesson ON lesson_sessions(lesson_id) WHERE status='active';
CREATE INDEX idx_lesson_sessions ON lesson_sessions(lesson_id,started_at);
CREATE TABLE lesson_step_results (
 session_id TEXT NOT NULL REFERENCES lesson_sessions(id), content_id TEXT NOT NULL,
 event_id TEXT NOT NULL UNIQUE REFERENCES study_events(id),
 outcome TEXT NOT NULL CHECK(outcome IN ('viewed','correct','incorrect')), selected_choice_id TEXT,
 PRIMARY KEY(session_id,content_id),
 CHECK((outcome='viewed' AND selected_choice_id IS NULL) OR (outcome IN ('correct','incorrect') AND selected_choice_id IS NOT NULL))
);
PRAGMA user_version = 3;
