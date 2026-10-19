-- Grammar attempts live in the same UserProgress DB; schedules stay in srs_state.
CREATE TABLE grammar_sessions (
 id TEXT PRIMARY KEY NOT NULL, lesson_id TEXT NOT NULL,
 state_json TEXT NOT NULL, revision INTEGER NOT NULL CHECK(revision>=0),
 status TEXT NOT NULL CHECK(status IN ('active','completed')),
 updated_at REAL NOT NULL
);
CREATE UNIQUE INDEX idx_grammar_active ON grammar_sessions(lesson_id) WHERE status='active';
CREATE INDEX idx_grammar_lesson ON grammar_sessions(lesson_id,status);
CREATE TABLE grammar_review_questions (
 session_id TEXT NOT NULL, content_id TEXT NOT NULL,
 question_json TEXT NOT NULL, selected_choice TEXT, correct INTEGER CHECK(correct IN (0,1)),
 PRIMARY KEY(session_id,content_id),
 FOREIGN KEY(session_id,content_id) REFERENCES review_items(session_id,content_id),
 CHECK((selected_choice IS NULL AND correct IS NULL) OR (selected_choice IS NOT NULL AND correct IS NOT NULL))
);
PRAGMA user_version=6;
