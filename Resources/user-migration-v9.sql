-- DEV-11: legacy favorites were vocabulary-only. Global content UUIDs remain unique.
ALTER TABLE favorites ADD COLUMN content_type TEXT NOT NULL DEFAULT 'vocabulary' CHECK(content_type IN ('vocabulary','grammar'));
CREATE INDEX idx_favorites_type_date ON favorites(content_type,created_at DESC,content_id);
CREATE TABLE recent_content (
 content_id TEXT NOT NULL, content_type TEXT NOT NULL CHECK(content_type IN ('vocabulary','grammar')),
 viewed_at REAL NOT NULL, PRIMARY KEY(content_id,content_type)
);
CREATE INDEX idx_recent_date ON recent_content(viewed_at DESC,content_id);
PRAGMA user_version=9;
