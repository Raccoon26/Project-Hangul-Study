-- Local set identity and immutable membership, independent of Content.sqlite/order/version.
CREATE TABLE vocabulary_sets (
 id TEXT PRIMARY KEY NOT NULL, level TEXT NOT NULL, ordinal INTEGER NOT NULL CHECK(ordinal>0),
 created_at REAL NOT NULL, completed_count INTEGER NOT NULL DEFAULT 0 CHECK(completed_count>=0),
 UNIQUE(level,ordinal)
);
CREATE TABLE vocabulary_set_items (
 set_id TEXT NOT NULL REFERENCES vocabulary_sets(id), content_id TEXT NOT NULL UNIQUE,
 ordinal INTEGER NOT NULL CHECK(ordinal>=0), PRIMARY KEY(set_id,content_id), UNIQUE(set_id,ordinal)
);
CREATE TABLE vocabulary_sessions (
 id TEXT PRIMARY KEY NOT NULL, set_id TEXT NOT NULL REFERENCES vocabulary_sets(id),
 state_json TEXT NOT NULL, revision INTEGER NOT NULL CHECK(revision>=0),
 status TEXT NOT NULL CHECK(status IN ('active','completed')),
 updated_at REAL NOT NULL
);
CREATE UNIQUE INDEX idx_vocabulary_active ON vocabulary_sessions(set_id) WHERE status='active';
CREATE INDEX idx_vocabulary_session_set ON vocabulary_sessions(set_id,updated_at DESC);
CREATE TABLE vocabulary_events (
 id TEXT PRIMARY KEY NOT NULL, session_id TEXT NOT NULL REFERENCES vocabulary_sessions(id),
 content_id TEXT, round INTEGER NOT NULL CHECK(round>0),
 kind TEXT NOT NULL CHECK(kind IN ('exposure','learn','known','round_completed','set_completed')),
 occurred_at REAL NOT NULL,
 CHECK((kind IN ('exposure','learn','known') AND content_id IS NOT NULL) OR (kind IN ('round_completed','set_completed') AND content_id IS NULL)),
 UNIQUE(session_id,round,content_id,kind)
);
CREATE INDEX idx_vocabulary_event_item ON vocabulary_events(content_id,occurred_at);
CREATE UNIQUE INDEX idx_vocabulary_round_event ON vocabulary_events(session_id,round,kind) WHERE content_id IS NULL;
PRAGMA user_version=4;
