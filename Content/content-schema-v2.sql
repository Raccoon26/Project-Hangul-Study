PRAGMA foreign_keys = ON;
PRAGMA user_version = 2;
CREATE TABLE content_metadata (
 singleton INTEGER PRIMARY KEY CHECK(singleton=1), schema_version INTEGER NOT NULL CHECK(schema_version=2),
 content_version INTEGER NOT NULL CHECK(content_version>=1), min_reader_version INTEGER NOT NULL CHECK(min_reader_version>=1),
 dataset_id TEXT NOT NULL, is_fixture INTEGER NOT NULL CHECK(is_fixture IN (0,1)), source_locale TEXT NOT NULL, target_locale TEXT NOT NULL
);
-- UUID identities are authored once in source JSON. Never derive IDs from text or position.
CREATE TABLE content_items (
 id TEXT PRIMARY KEY NOT NULL, kind TEXT NOT NULL CHECK(kind IN ('vocabulary','meaning','example','grammar','pronunciation','conjugation','listening','question','course','lesson','tag','hangul','note')),
 revision INTEGER NOT NULL CHECK(revision>=1), is_active INTEGER NOT NULL DEFAULT 1 CHECK(is_active IN (0,1)),
 level TEXT NOT NULL CHECK(level IN ('hangul','intro','beginner','lower_intermediate','intermediate','upper_intermediate','advanced','master','maintenance')), difficulty INTEGER CHECK(difficulty BETWEEN 1 AND 5), created_at TEXT NOT NULL, updated_at TEXT NOT NULL
);
CREATE INDEX idx_content_level ON content_items(kind,is_active,level,id);
CREATE INDEX idx_content_kind_active ON content_items(kind,is_active,id);
CREATE TABLE vocabulary (id TEXT PRIMARY KEY NOT NULL REFERENCES content_items(id), headword TEXT NOT NULL, reading TEXT, part_of_speech TEXT NOT NULL CHECK(part_of_speech IN ('noun','pronoun','numeral','verb','adjective','determiner','adverb','particle','interjection','auxiliary_verb','auxiliary_adjective','bound_noun','prefix','suffix','ending','expression')), sort_key TEXT NOT NULL, has_batchim INTEGER CHECK(has_batchim IN (0,1)), irregular_type TEXT CHECK(irregular_type IN ('none','d','b','s','h','reu','reu_special','u','other')), learning_priority INTEGER CHECK(learning_priority>=0), topik_level INTEGER CHECK(topik_level BETWEEN 1 AND 6), topik_source_id TEXT REFERENCES sources(id), frequency_rank INTEGER CHECK(frequency_rank>0), frequency_source_id TEXT REFERENCES sources(id), CHECK(topik_level IS NULL OR topik_source_id IS NOT NULL), CHECK(frequency_rank IS NULL OR frequency_source_id IS NOT NULL));
CREATE INDEX idx_vocabulary_sort ON vocabulary(sort_key,id);
CREATE INDEX idx_vocabulary_headword ON vocabulary(headword);
CREATE TABLE meanings (id TEXT PRIMARY KEY NOT NULL REFERENCES content_items(id), vocabulary_id TEXT NOT NULL REFERENCES vocabulary(id), meaning_ja TEXT NOT NULL, part_of_speech TEXT, nuance_ja TEXT, usage_ja TEXT, ordinal INTEGER NOT NULL CHECK(ordinal>=0), UNIQUE(vocabulary_id,ordinal));
CREATE TABLE examples (id TEXT PRIMARY KEY NOT NULL REFERENCES content_items(id), korean TEXT NOT NULL, japanese TEXT NOT NULL, learning_point_ja TEXT, audio_asset_id TEXT REFERENCES media_assets(id));
CREATE TABLE vocabulary_examples (meaning_id TEXT NOT NULL REFERENCES meanings(id), example_id TEXT NOT NULL REFERENCES examples(id), PRIMARY KEY(meaning_id,example_id));
CREATE TABLE grammar (id TEXT PRIMARY KEY NOT NULL REFERENCES content_items(id), pattern TEXT NOT NULL, title_ja TEXT NOT NULL, explanation_ja TEXT NOT NULL, meaning_ja TEXT, form_ko TEXT, usage_constraints_ja TEXT, confusion_ja TEXT);
CREATE TABLE grammar_examples (grammar_id TEXT NOT NULL REFERENCES grammar(id), example_id TEXT NOT NULL REFERENCES examples(id), PRIMARY KEY(grammar_id,example_id));
CREATE TABLE pronunciation_rules (id TEXT PRIMARY KEY NOT NULL REFERENCES content_items(id), title_ja TEXT NOT NULL, rule_type TEXT NOT NULL, explanation_ja TEXT NOT NULL);
CREATE TABLE hangul (id TEXT PRIMARY KEY NOT NULL REFERENCES content_items(id), symbol TEXT NOT NULL, category TEXT NOT NULL CHECK(category IN ('consonant','vowel','final','syllable')), name_ko TEXT NOT NULL, explanation_ja TEXT NOT NULL, audio_asset_id TEXT REFERENCES media_assets(id));
CREATE TABLE conjugations (id TEXT PRIMARY KEY NOT NULL REFERENCES content_items(id), vocabulary_id TEXT NOT NULL REFERENCES vocabulary(id), form TEXT NOT NULL, form_type TEXT NOT NULL, politeness TEXT NOT NULL, explanation_ja TEXT NOT NULL, irregular_type TEXT, rule_id TEXT REFERENCES pronunciation_rules(id));
CREATE TABLE media_assets (id TEXT PRIMARY KEY NOT NULL, relative_path TEXT NOT NULL UNIQUE, sha256 TEXT NOT NULL, media_type TEXT NOT NULL, duration_ms INTEGER CHECK(duration_ms>=0), license TEXT NOT NULL);
CREATE TABLE listening_items (id TEXT PRIMARY KEY NOT NULL REFERENCES content_items(id), audio_asset_id TEXT NOT NULL REFERENCES media_assets(id), transcript_ko TEXT NOT NULL, explanation_ja TEXT NOT NULL);
CREATE TABLE questions (id TEXT PRIMARY KEY NOT NULL REFERENCES content_items(id), question_type TEXT NOT NULL CHECK(question_type IN ('multiple_choice','text_input','sentence_order','listening_choice','listening_input','writing')), direction TEXT CHECK(direction IN ('ko_ja','ja_ko','ko_ko')), answer_schema_version INTEGER NOT NULL DEFAULT 1 CHECK(answer_schema_version=1), prompt_ja TEXT NOT NULL, prompt_ko TEXT, explanation_ja TEXT NOT NULL, answer_json TEXT NOT NULL, rubric_json TEXT, listening_id TEXT REFERENCES listening_items(id), topik_level INTEGER CHECK(topik_level BETWEEN 1 AND 6));
CREATE TABLE question_choices (question_id TEXT NOT NULL REFERENCES questions(id), choice_id TEXT NOT NULL, ordinal INTEGER NOT NULL CHECK(ordinal>=0), text TEXT NOT NULL, PRIMARY KEY(question_id,choice_id), UNIQUE(question_id,ordinal));
CREATE TABLE courses (id TEXT PRIMARY KEY NOT NULL REFERENCES content_items(id), title_ja TEXT NOT NULL, description_ja TEXT NOT NULL, ordinal INTEGER NOT NULL CHECK(ordinal>=0));
CREATE TABLE lessons (id TEXT PRIMARY KEY NOT NULL REFERENCES content_items(id), course_id TEXT NOT NULL REFERENCES courses(id), title_ja TEXT NOT NULL, ordinal INTEGER NOT NULL CHECK(ordinal>=0), UNIQUE(course_id,ordinal));
CREATE TABLE lesson_items (lesson_id TEXT NOT NULL REFERENCES lessons(id), content_id TEXT NOT NULL REFERENCES content_items(id), ordinal INTEGER NOT NULL CHECK(ordinal>=0), PRIMARY KEY(lesson_id,content_id), UNIQUE(lesson_id,ordinal));
CREATE TABLE tags (id TEXT PRIMARY KEY NOT NULL REFERENCES content_items(id), label_ja TEXT NOT NULL, namespace TEXT NOT NULL);
CREATE TABLE item_tags (content_id TEXT NOT NULL REFERENCES content_items(id), tag_id TEXT NOT NULL REFERENCES tags(id), PRIMARY KEY(content_id,tag_id));
CREATE INDEX idx_tags_content ON item_tags(tag_id,content_id);
CREATE TABLE learner_notes (id TEXT PRIMARY KEY NOT NULL REFERENCES content_items(id), title_ja TEXT NOT NULL, explanation_ja TEXT NOT NULL, confusion_type TEXT NOT NULL);
CREATE TABLE content_links (source_id TEXT NOT NULL REFERENCES content_items(id), target_id TEXT NOT NULL REFERENCES content_items(id), relation TEXT NOT NULL, PRIMARY KEY(source_id,target_id,relation));
CREATE INDEX idx_content_links_target ON content_links(target_id);
CREATE TABLE content_aliases (old_id TEXT PRIMARY KEY NOT NULL REFERENCES content_items(id), canonical_id TEXT NOT NULL REFERENCES content_items(id), CHECK(old_id<>canonical_id));

-- Provenance is bibliographic evidence, not an inferred TOPIK/frequency rank.
CREATE TABLE sources (id TEXT PRIMARY KEY NOT NULL, title TEXT NOT NULL, citation TEXT NOT NULL, url TEXT, accessed_at TEXT);
CREATE TABLE item_sources (content_id TEXT NOT NULL REFERENCES content_items(id), source_id TEXT NOT NULL REFERENCES sources(id), note TEXT, PRIMARY KEY(content_id,source_id));
CREATE TABLE pronunciation_examples (rule_id TEXT NOT NULL REFERENCES pronunciation_rules(id), example_id TEXT NOT NULL REFERENCES examples(id), spelling_ko TEXT NOT NULL, pronunciation_ko TEXT NOT NULL, PRIMARY KEY(rule_id,example_id));
CREATE INDEX idx_vocab_examples_reverse ON vocabulary_examples(example_id,meaning_id);
CREATE INDEX idx_grammar_examples_reverse ON grammar_examples(example_id,grammar_id);
CREATE INDEX idx_pronunciation_examples_reverse ON pronunciation_examples(example_id,rule_id);
-- Derived at import time. Source files cannot write this table.
CREATE TABLE vocabulary_search (term TEXT NOT NULL, vocabulary_id TEXT NOT NULL REFERENCES vocabulary(id), PRIMARY KEY(term,vocabulary_id)) WITHOUT ROWID;
