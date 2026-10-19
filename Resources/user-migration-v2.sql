-- Additive migration; does not rewrite IDs, events, favorites, or SRS data.
ALTER TABLE item_progress ADD COLUMN acquisition_status TEXT NOT NULL DEFAULT 'unassessed'
 CHECK(acquisition_status IN ('unassessed','learning','acquired','maintaining'));
ALTER TABLE item_progress ADD COLUMN perceived_difficulty INTEGER CHECK(perceived_difficulty BETWEEN 1 AND 5);
PRAGMA user_version = 2;
