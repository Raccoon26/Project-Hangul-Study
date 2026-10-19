-- Scheduling remains in existing srs_state. These are sessions/results, not a second SRS store.
CREATE INDEX idx_srs_skill_due ON srs_state(skill,algorithm,algorithm_version,due_at,content_id) WHERE due_at IS NOT NULL;
CREATE TABLE srs_enrolled_passes (
 session_id TEXT PRIMARY KEY NOT NULL REFERENCES vocabulary_sessions(id)
);
CREATE TABLE review_sessions (
 id TEXT PRIMARY KEY NOT NULL, skill TEXT NOT NULL,
 status TEXT NOT NULL CHECK(status IN ('active','completed')),
 started_at REAL NOT NULL, updated_at REAL NOT NULL, completed_at REAL
);
CREATE UNIQUE INDEX idx_review_active ON review_sessions(skill) WHERE status='active';
CREATE TABLE review_items (
 session_id TEXT NOT NULL REFERENCES review_sessions(id), content_id TEXT NOT NULL,
 ordinal INTEGER NOT NULL CHECK(ordinal>=0), exposed_at REAL, revealed_at REAL,
 result TEXT CHECK(result IN ('difficult','unsure','remembered')), reviewed_at REAL,
 next_due_at REAL, previous_stage INTEGER, next_stage INTEGER,
 time_zone TEXT, local_day TEXT, study_event_id TEXT REFERENCES study_events(id),
 PRIMARY KEY(session_id,content_id), UNIQUE(session_id,ordinal),
 CHECK(revealed_at IS NULL OR exposed_at IS NOT NULL),
 CHECK((result IS NULL AND reviewed_at IS NULL AND next_due_at IS NULL) OR
       (result IS NOT NULL AND reviewed_at IS NOT NULL AND next_due_at IS NOT NULL AND revealed_at IS NOT NULL AND previous_stage IS NOT NULL AND next_stage IS NOT NULL AND time_zone IS NOT NULL AND local_day IS NOT NULL))
);
CREATE INDEX idx_review_day ON review_items(reviewed_at) WHERE reviewed_at IS NOT NULL;
PRAGMA user_version=5;
