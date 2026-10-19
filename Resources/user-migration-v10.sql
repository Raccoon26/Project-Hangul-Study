-- Bounded time-window statistics; no user records are rewritten.
CREATE INDEX idx_study_event_time ON study_events(occurred_at,skill,outcome);
CREATE INDEX idx_listening_attempt_time ON listening_attempts(occurred_at,is_review,attempt);
CREATE INDEX idx_item_last_seen ON item_progress(last_seen_at,content_id);
PRAGMA user_version=10;
