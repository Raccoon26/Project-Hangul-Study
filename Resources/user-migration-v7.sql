CREATE TABLE production_sessions (
 id TEXT PRIMARY KEY NOT NULL, scope_id TEXT NOT NULL, state_json TEXT NOT NULL,
 completed INTEGER NOT NULL CHECK(completed IN (0,1))
);
CREATE UNIQUE INDEX idx_production_active ON production_sessions(scope_id) WHERE completed=0;
PRAGMA user_version=7;
