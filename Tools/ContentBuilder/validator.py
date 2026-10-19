"""Structural/content-contract checks; never claims linguistic correctness."""
import datetime, hashlib, json, sqlite3, unicodedata, uuid
from collections import defaultdict
from source_reader import strict_json

SCHEMA_VERSION=4
READER_VERSION=7
KINDS={'vocabulary':'vocabulary','meanings':'meaning','examples':'example','grammar':'grammar','pronunciation_rules':'pronunciation','conjugations':'conjugation','listening_items':'listening','questions':'question','courses':'course','lessons':'lesson','tags':'tag','hangul':'hangul','learner_notes':'note'}
LEVELS=('hangul','intro','beginner','lower_intermediate','intermediate','upper_intermediate','advanced','master','maintenance')
POS=('noun','pronoun','numeral','verb','adjective','determiner','adverb','particle','interjection','auxiliary_verb','auxiliary_adjective','bound_noun','prefix','suffix','ending','expression')
IRREGULAR=('none','d','b','s','h','reu','reu_special','u','other')
RULE_TYPES=('batchim','liaison','nasalization','liquidization','tensification','aspiration','palatalization','contraction','other')
RELATIONS={'related':None,'related_word':('vocabulary','vocabulary'),'synonym':('vocabulary','vocabulary'),'antonym':('vocabulary','vocabulary'),'confusable':('vocabulary','vocabulary'),'similar_grammar':('grammar','grammar'),'contrast_grammar':('grammar','grammar'),'learner_note':(None,'note'),'pronunciation_example':('pronunciation','example'),'explains':None,'prerequisite':None,'question_target':('question',None)}

def canonical_uuid(value):
    try: return isinstance(value,str) and str(uuid.UUID(value))==value
    except (ValueError,TypeError,AttributeError): return False

def normalize(value): return unicodedata.normalize('NFC',value).strip().lower()

class Report:
    def __init__(self): self.errors=[]; self.warnings=[]; self.error_count=0; self.warning_count=0
    def add(self,severity,code,location,message):
        key='error' if severity=='error' else 'warning'
        setattr(self,key+'_count',getattr(self,key+'_count')+1)
        entries=getattr(self,key+'s')
        if len(entries)<200: entries.append(dict(code=code,location=location,message=message))
    def error(self,code,location,message): self.add('error',code,location,message)
    def warning(self,code,location,message): self.add('warning',code,location,message)
    def as_dict(self): return dict(error_count=self.error_count,warning_count=self.warning_count,errors=self.errors,warnings=self.warnings,details_limit=200)

class ValidationError(ValueError):
    def __init__(self,report): self.report=report.as_dict(); super().__init__(json.dumps(self.report,ensure_ascii=False))

def metadata(meta,report):
    required={'schema_version','content_version','min_reader_version','dataset_id','is_fixture','source_locale','target_locale'}
    if set(meta)!=required: report.error('metadata_fields','metadata',f'Expected fields: {sorted(required)}')
    for field in ('schema_version','content_version','min_reader_version','is_fixture'):
        if type(meta.get(field)) is not int: report.error('metadata_type',field,'Expected integer')
    if meta.get('schema_version') not in (2,3,4): report.error('schema_version','metadata','Expected schema version 2, 3 or 4; migrate v1 source explicitly')
    if type(meta.get('content_version')) is int and not (1<=meta['content_version']<=2**63-1): report.error('content_version','metadata','Must be positive')
    if meta.get('min_reader_version') not in (2,3,4,5,6,READER_VERSION): report.error('reader_version','metadata','Supported reader versions: 2, 3, 4, 5, 6 or 7')
    if meta.get('schema_version')==3 and (type(meta.get('min_reader_version')) is not int or meta['min_reader_version']<4): report.error('reader_version','metadata','Schema 3 requires reader 4')
    if meta.get('schema_version')==4 and meta.get('min_reader_version')!=7: report.error('reader_version','metadata','Schema 4 requires reader 7')
    if meta.get('is_fixture') not in (0,1): report.error('fixture_flag','metadata','Expected 0 or 1')
    for field in ('dataset_id','source_locale','target_locale'):
        if not isinstance(meta.get(field),str) or not meta[field].strip(): report.error('metadata_text',field,'Expected nonempty text')
    if (meta.get('source_locale'),meta.get('target_locale'))!=('ja','ko'): report.error('locale','metadata','This dataset contract is ja → ko')
    if meta.get('is_fixture')==0 and str(meta.get('dataset_id','')).startswith(('dev-','synthetic-')): report.error('fixture_namespace','metadata','Development namespace cannot be production')

def row_fields(table,row,columns,location,report):
    start=report.error_count
    if not isinstance(row,dict): report.error('row_type',location,'Expected object'); return False
    unknown=set(row)-set(columns)
    if unknown: report.error('unknown_fields',location,str(sorted(unknown)))
    for name,col in columns.items():
        _,_,kind,not_null,default,_=col
        value=row.get(name)
        if name not in row and not_null and default is None:
            report.error('required_field',location,f'Missing {name}'); continue
        if value is None:
            if name in row and not_null: report.error('required_field',location,f'{name} cannot be null')
            continue
        if kind=='TEXT':
            if not isinstance(value,str): report.error('field_type',location,f'{name}: expected string'); continue
            if not value.strip(): report.error('empty_text',location,f'{name} is empty')
            limit=2000 if name in ('korean','japanese','headword','reading','meaning_ja','sort_key') else 20000
            if len(value)>limit: report.error('text_too_long',location,f'{name}: max {limit} Unicode characters')
            if '\x00' in value: report.error('nul_character',location,name)
            if any(unicodedata.category(c)=='Cc' and c not in '\t\n\r\x00' for c in value):
                report.error('control_character',location,f'{name}: unexpected control character')
            try: value.encode('utf-8')
            except UnicodeEncodeError: report.error('invalid_unicode',location,f'{name}: unpaired surrogate')
            if any((ord(c) & 0xFFFF) in (0xFFFE,0xFFFF) or 0xFDD0<=ord(c)<=0xFDEF for c in value):
                report.error('invalid_unicode',location,f'{name}: Unicode noncharacter')
            if unicodedata.normalize('NFC',value)!=value: report.warning('non_nfc',location,f'{name}: review Unicode normalization')
        elif kind=='INTEGER':
            if type(value) is not int: report.error('field_type',location,f'{name}: expected integer')
            elif not (-2**63<=value<=2**63-1): report.error('integer_range',location,f'{name}: exceeds SQLite signed 64-bit range')
    if table in KINDS or table in ('media_assets','sources'):
        if not canonical_uuid(row.get('id')): report.error('stable_id',location,'Expected canonical lowercase UUID')
    if table=='content_items':
        if row.get('level') not in LEVELS: report.error('level',location,f'Allowed: {LEVELS}')
        dates=[]
        for key in ('created_at','updated_at'):
            try:
                date=datetime.datetime.fromisoformat(str(row.get(key)).replace('Z','+00:00'))
                if date.tzinfo is None: raise ValueError()
                dates.append(date)
            except ValueError: report.error('timestamp',location,f'{key}: expected ISO-8601 with timezone')
        if len(dates)==2 and dates[1]<dates[0]: report.error('timestamp_order',location,'updated_at precedes created_at')
    if table in ('vocabulary','meanings') and row.get('part_of_speech') is not None and row['part_of_speech'] not in POS:
        report.error('part_of_speech',location,f'Allowed: {POS}')
    if table in ('vocabulary','conjugations') and row.get('irregular_type') is not None and row['irregular_type'] not in IRREGULAR:
        report.error('irregular_type',location,f'Allowed: {IRREGULAR}')
    if table=='pronunciation_rules' and row.get('rule_type') not in RULE_TYPES: report.error('rule_type',location,f'Allowed: {RULE_TYPES}')
    if table=='examples':
        for key in ('korean','japanese'):
            value=row.get(key)
            if isinstance(value,str) and 0<len(value.strip())<2: report.warning('short_sentence',location,f'{key}: single-character sentence needs review')
    if table=='questions':
        for key in ('answer_json','rubric_json'):
            value=row.get(key)
            if value is not None:
                try:
                    parsed=strict_json(value)
                    if not isinstance(parsed,dict): raise ValueError()
                except (ValueError,TypeError): report.error('answer_json',location,f'{key} must encode a JSON object')
    if table=='pronunciation_presentations':
        try:
            readings=strict_json(row.get('readings_json',''))
            if not isinstance(readings,list) or not readings or any(not isinstance(x,str) or not x.strip() for x in readings) or len(set(readings))!=len(readings): raise ValueError()
        except (ValueError,TypeError): report.error('pronunciation_readings',location,'Expected nonempty unique pronunciation string array')
    if table=='content_audio' and row.get('mode')=='tts':
        text=row.get('tts_text','')
        if not isinstance(text,str) or not text.strip() or len(text)>500 or any(0x1100<=ord(c)<=0x11ff or 0x3130<=ord(c)<=0x318f or 0xa960<=ord(c)<=0xa97f or 0xd7b0<=ord(c)<=0xd7ff for c in text) or not any(0xac00<=ord(c)<=0xd7a3 for c in text) or any(c in text for c in '[]/→+'):
            report.error('unsafe_tts',location,'TTS must be reviewed original Korean words/sentences, not jamo or phonetic markup')
    return start==report.error_count

def database(db,reader,report):
    for table,rowid,parent,fkid in db.execute('PRAGMA foreign_key_check'):
        report.error('missing_reference',f'{table}:rowid={rowid}',f'Foreign key {fkid} references missing {parent}')
    for table,kind in KINDS.items():
        for item_id in db.execute(f'SELECT i.id FROM content_items i LEFT JOIN {table} t ON t.id=i.id WHERE i.kind=? AND t.id IS NULL',(kind,)):
            report.error('missing_payload',item_id[0],table)
        for item_id in db.execute(f'SELECT t.id FROM {table} t JOIN content_items i ON i.id=t.id WHERE i.kind<>?',(kind,)):
            report.error('wrong_kind',item_id[0],table)
    for item_id in db.execute('''SELECT v.id FROM vocabulary v JOIN content_items i ON i.id=v.id WHERE i.is_active=1 AND NOT EXISTS
        (SELECT 1 FROM meanings m JOIN content_items mi ON mi.id=m.id WHERE m.vocabulary_id=v.id AND mi.is_active=1)'''):
        report.error('missing_meaning',item_id[0],'Active vocabulary needs at least one active meaning')
    for item_id in db.execute('''SELECT e.id FROM examples e JOIN content_items i ON i.id=e.id WHERE i.is_active=1
        AND NOT EXISTS (SELECT 1 FROM vocabulary_examples WHERE example_id=e.id)
        AND NOT EXISTS (SELECT 1 FROM grammar_examples WHERE example_id=e.id)
        AND NOT EXISTS (SELECT 1 FROM pronunciation_examples WHERE example_id=e.id)
        AND NOT EXISTS (SELECT 1 FROM lesson_items WHERE content_id=e.id)
        AND NOT EXISTS (SELECT 1 FROM content_links WHERE target_id=e.id OR source_id=e.id)'''):
        report.error('orphan_example',item_id[0],'Example needs an explicit content/lesson relationship')
    candidates=defaultdict(list)
    for item_id,word in db.execute('SELECT id,headword FROM vocabulary'):
        candidates[normalize(word)].append(item_id)
    for word,ids in candidates.items():
        if len(ids)>1: report.warning('duplicate_headword_candidate',word,json.dumps(ids))
    grammar_candidates=defaultdict(list)
    for gid,pattern in db.execute('SELECT id,pattern FROM grammar'):
        # Spacing-only notation changes are review candidates, never auto-deletions.
        grammar_candidates[''.join(normalize(pattern).split())].append(gid)
    for pattern,ids in grammar_candidates.items():
        if len(ids)>1: report.warning('duplicate_grammar_candidate',pattern,json.dumps(ids))
    for qid,rubric in db.execute('SELECT id,rubric_json FROM questions WHERE rubric_json IS NOT NULL'):
        try:
            if 'grammar_task' not in strict_json(rubric): continue
        except (ValueError,TypeError): continue  # row validation reports malformed JSON
        targets=list(db.execute("SELECT l.target_id FROM content_links l JOIN grammar g ON g.id=l.target_id JOIN content_items i ON i.id=g.id WHERE l.source_id=? AND l.relation='question_target' AND i.is_active=1",(qid,)))
        if len(targets)!=1:
            report.error('orphan_grammar_question',qid,'Grammar question requires exactly one active grammar target')
    # Only grammar participating in the production learning runner needs its presentation/quiz contract.
    taught=list(db.execute("SELECT DISTINCT g.id,g.meaning_ja,g.form_ko FROM grammar g JOIN lesson_items li ON li.content_id=g.id JOIN content_items i ON i.id=g.id WHERE i.is_active=1"))
    if taught and reader.metadata['min_reader_version']<5:
        report.error('grammar_reader','metadata','Grammar learning requires reader 5')
    for gid,meaning,form in taught:
        if not meaning or not form: report.error('grammar_presentation',gid,'Meaning and human-readable form required')
        if not db.execute('SELECT 1 FROM grammar_examples ge JOIN content_items i ON i.id=ge.example_id WHERE ge.grammar_id=? AND i.is_active=1',(gid,)).fetchone(): report.error('grammar_examples',gid,'Taught grammar needs examples')
        questions=list(db.execute("SELECT q.id,q.question_type,q.rubric_json,q.answer_json FROM content_links l JOIN questions q ON q.id=l.source_id JOIN content_items i ON i.id=q.id WHERE l.target_id=? AND l.relation='question_target' AND i.is_active=1",(gid,)))
        if not 1<=len(questions)<=20: report.error('grammar_questions',gid,'Need 1–20 supported questions')
        for qid,kind,rubric,answer in questions:
            choices=list(db.execute('SELECT text FROM question_choices WHERE question_id=?',(qid,)))
            if not 2<=len(choices)<=6 or len({normalize(c[0]) for c in choices})!=len(choices):
                report.error('grammar_choices',qid,'Need 2–6 distinct answer texts')
            try:
                task=strict_json(rubric).get('grammar_task')
                answers=strict_json(answer).get('correct_choice_ids')
                if kind!='multiple_choice' or task not in ('meaning','context','blank','form','contrast') or not isinstance(answers,list) or len(answers)!=1: raise ValueError()
            except (ValueError,TypeError,AttributeError): report.error('grammar_question_contract',qid,'Expected supported grammar_task and one correct choice')
    for lid,n in db.execute("SELECT li.lesson_id,COUNT(*) FROM lesson_items li JOIN grammar g ON g.id=li.content_id GROUP BY li.lesson_id"):
        if n>20: report.error('grammar_lesson_size',lid,'Max 20 grammar per lesson')
    for level,ordinal,n in db.execute("SELECT i.level,l.ordinal,COUNT(DISTINCT l.id) FROM lessons l JOIN content_items i ON i.id=l.id JOIN lesson_items li ON li.lesson_id=l.id JOIN grammar g ON g.id=li.content_id GROUP BY i.level,l.ordinal HAVING COUNT(DISTINCT l.id)>1"):
        report.error('grammar_lesson_order',level,'Grammar lesson ordinal must be unique within a level')
    kinds=dict(db.execute('SELECT id,kind FROM content_items'))
    for source,target,relation in db.execute('SELECT * FROM content_links'):
        if relation not in RELATIONS: report.error('relation_type',source,relation); continue
        if source==target: report.error('self_relation',source,relation)
        rule=RELATIONS[relation]
        if rule and ((rule[0] and kinds.get(source)!=rule[0]) or (rule[1] and kinds.get(target)!=rule[1])):
            report.error('relation_kind',source,f'{relation} expects {rule}')
    for lesson_id,content_id,kind in db.execute("SELECT li.lesson_id,li.content_id,i.kind FROM lesson_items li JOIN content_items i ON i.id=li.content_id WHERE i.kind IN ('course','lesson','tag')"):
        report.error('lesson_item_kind',lesson_id,f'Lesson cannot contain {kind}: {content_id}')
    for item_id,pos in db.execute("SELECT c.id,v.part_of_speech FROM conjugations c JOIN vocabulary v ON v.id=c.vocabulary_id WHERE v.part_of_speech NOT IN ('verb','adjective','auxiliary_verb','auxiliary_adjective')"):
        report.error('conjugation_base',item_id,f'Cannot conjugate {pos}')
    aliases=dict(db.execute('SELECT old_id,canonical_id FROM content_aliases'))
    active=dict(db.execute('SELECT id,is_active FROM content_items'))
    for start in aliases:
        seen=set(); node=start
        while node in aliases:
            if node in seen: report.error('alias_cycle',start,'Alias cycle'); break
            seen.add(node); node=aliases[node]
        if active.get(start)!=0 or active.get(node)!=1 or kinds.get(start)!=kinds.get(node):
            report.error('alias_target',start,'Alias must connect inactive ID to active ID of same kind')
    for asset_id,path,digest in db.execute('SELECT id,relative_path,sha256 FROM media_assets'):
        from pathlib import Path
        p=Path(path); asset=(reader.root/p).resolve()
        if p.is_absolute() or '..' in p.parts or '\\' in path or not asset.is_relative_to(reader.root):
            report.error('media_path',asset_id,path); continue
        if not asset.is_file() or hashlib.sha256(asset.read_bytes()).hexdigest()!=digest:
            report.error('media_checksum',asset_id,path)
    if reader.metadata['schema_version']>=3:
        for item_id in db.execute("SELECT a.content_id FROM content_audio a JOIN content_items i ON i.id=a.content_id WHERE a.mode='tts' AND i.kind='hangul'"):
            report.error('jamo_tts_policy',item_id[0],'Hangul teaching items require reviewed recordings, not TTS')
        for item_id in db.execute("SELECT li.content_id FROM lesson_items li JOIN content_items i ON i.id=li.content_id LEFT JOIN pronunciation_presentations p ON p.rule_id=li.content_id WHERE i.kind='pronunciation' AND p.rule_id IS NULL"):
            report.error('pronunciation_presentation',item_id[0],'A pronunciation lesson step needs a presentation')
        for item_id in db.execute("SELECT p.rule_id FROM pronunciation_presentations p JOIN content_audio a ON a.content_id=p.rule_id WHERE a.mode='tts' AND a.tts_text<>p.spelling_ko"):
            report.error('tts_orthography',item_id[0],'TTS must use spelling, never educational transcription')
        for item_id in db.execute("SELECT a.question_id FROM audio_questions a JOIN questions q ON q.id=a.question_id JOIN content_audio c ON c.content_id=a.audio_content_id WHERE q.question_type<>'multiple_choice' OR c.mode<>'tts'"):
            report.error('audio_question',item_id[0],'DEV-04 audio questions require single-choice with reviewed TTS')
        for item_id in db.execute("SELECT a.question_id FROM audio_questions a JOIN questions q ON q.id=a.question_id WHERE q.prompt_ko IS NOT NULL"):
            report.error('audio_answer_leak',item_id[0],'Listening prompt must not show its transcript')
    if reader.metadata['schema_version']>=4:
        validate_listening(db,report)
    production_overrides={}
    for item_id,kind,answer,listening_id in db.execute('SELECT id,question_type,answer_json,listening_id FROM questions'):
        try: answer=strict_json(answer)
        except ValueError: continue
        if not isinstance(answer,dict): continue
        if kind in ('multiple_choice','listening_choice'):
            choices={r[0] for r in db.execute('SELECT choice_id FROM question_choices WHERE question_id=?',(item_id,))}
            ids=answer.get('correct_choice_ids')
            if len(choices)<2 or not isinstance(ids,list) or not ids or any(not isinstance(x,str) or x not in choices for x in ids) or len(set(ids))!=len(ids):
                report.error('choice_answer',item_id,'Need >=2 choices and unique existing correct_choice_ids')
        elif kind in ('text_input','listening_input'):
            values=answer.get('accepted')
            if not isinstance(values,list) or not values or any(not isinstance(x,str) or not x.strip() for x in values):
                report.error('input_answer',item_id,'Need nonempty accepted string array')
            rubric_row=db.execute('SELECT rubric_json FROM questions WHERE id=?',(item_id,)).fetchone()
            try: rubric=strict_json(rubric_row[0]) if rubric_row[0] else {}
            except ValueError: rubric={}
            if isinstance(rubric,dict) and rubric.get('production')==1:
                reader=db.execute('SELECT min_reader_version FROM content_metadata').fetchone()[0]
                if reader<6: report.error('production_reader',item_id,'Production drills require reader 6')
                forms={'present','past','future','negativeShort','negativeLong','wish','connective','reason','condition'}
                targets=list(db.execute("SELECT v.headword,v.part_of_speech,v.irregular_type,v.id FROM content_links l JOIN vocabulary v ON v.id=l.target_id WHERE l.source_id=? AND l.relation='question_target'",(item_id,)))
                if len(targets)!=1 or targets[0][1] not in ('verb','adjective'):
                    report.error('production_target',item_id,'Need one verb/adjective vocabulary target')
                if rubric.get('form') not in forms or type(rubric.get('spacing_warning')) is not bool or rubric.get('mode') not in ('form','blank','sentence'):
                    report.error('production_rubric',item_id,'Invalid form/spacing/mode')
                overrides=rubric.get('overrides')
                if not isinstance(overrides,dict) or any(k not in forms or not isinstance(v,str) or not v.strip() for k,v in overrides.items()):
                    report.error('production_override',item_id,'Invalid override')
                if targets and isinstance(overrides,dict):
                    for form,value in overrides.items():
                        key=(targets[0][3],form)
                        if key in production_overrides and production_overrides[key]!=value: report.error('production_override_conflict',item_id,'Conflicting overrides for the same lemma/form')
                        production_overrides[key]=value
                if targets and rubric.get('form')=='wish' and targets[0][1]!='verb': report.error('production_wish',item_id,'Wish requires verb')
                if targets:
                    target_count=db.execute("SELECT COUNT(*) FROM questions q JOIN content_links l ON l.source_id=q.id JOIN vocabulary v ON v.id=l.target_id WHERE l.relation='question_target' AND v.id=? AND q.question_type='text_input' AND CASE WHEN json_valid(q.rubric_json) THEN json_extract(q.rubric_json,'$.production') ELSE 0 END=1",(targets[0][3],)).fetchone()[0]
                    if target_count>20: report.error('production_size',item_id,'At most 20 questions per lemma session')
                    stem=targets[0][0][:-1]; irregular=targets[0][2]
                    if irregular in {'b':'ㅂ','d':'ㄷ','s':'ㅅ','h':'ㅎ'}:
                        tail={'b':17,'d':7,'s':19,'h':27}[irregular]
                        if not stem or (ord(stem[-1])-0xAC00)%28!=tail: report.error('production_irregular',item_id,'Metadata conflicts with stem')
                if isinstance(values,list) and len(set(values))!=len(values): report.error('production_answer_duplicate',item_id,'Duplicate accepted answer')
        elif kind=='sentence_order':
            tokens=answer.get('tokens'); order=answer.get('correct_order')
            if not isinstance(tokens,list) or not tokens or any(not isinstance(x,str) or not x.strip() for x in tokens) or not isinstance(order,list) or any(type(x) is not int for x in order) or sorted(order)!=list(range(len(tokens))):
                report.error('order_answer',item_id,'Need tokens and complete 0-based permutation')
        elif kind=='writing':
            if not isinstance(answer.get('model_answer'),str) or not answer['model_answer'].strip(): report.error('writing_answer',item_id,'Need model_answer')
        if kind.startswith('listening_') and listening_id is None: report.error('listening_reference',item_id,'Listening question needs listening_id')


def signatures(db):
    """Order-independent semantic fingerprints, including both endpoints of relationships."""
    owners={row[0]:hashlib.sha256() for row in db.execute('SELECT id FROM content_items')}
    tables=[row[0] for row in db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")]
    for table in sorted(tables):
        if table in ('content_metadata','vocabulary_search','sources','media_assets'): continue
        columns=[r[1] for r in db.execute(f'PRAGMA table_info("{table}")')]
        if table=='content_items': columns=[c for c in columns if c not in ('revision','updated_at')]
        owner_fields=['id'] if table in KINDS or table=='content_items' else [r[3] for r in db.execute(f'PRAGMA foreign_key_list("{table}")') if r[2] in KINDS or r[2]=='content_items']
        projection=','.join('"'+x+'"' for x in columns)
        for values in db.execute(f'SELECT {projection} FROM "{table}" ORDER BY {projection}'):
            row=dict(zip(columns,values))
            encoded=json.dumps([table,row],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
            for owner in {row.get(field) for field in owner_fields}:
                if owner in owners: owners[owner].update(encoded)
    return {key:value.digest() for key,value in owners.items()}

def previous_release(db,old,meta,report):
    version=old.execute('PRAGMA user_version').fetchone()[0]
    if version not in (1,2,3,4): report.error('previous_schema','previous',str(version)); return
    if meta['schema_version']<version: report.error('schema_downgrade','metadata','Cannot downgrade content schema')
    before=old.execute('SELECT dataset_id,content_version,is_fixture,schema_version FROM content_metadata').fetchone()
    if not before or before[3]!=version: report.error('previous_schema','previous','Inconsistent metadata'); return
    if (before[0],before[2])!=(meta['dataset_id'],meta['is_fixture']) or meta['content_version']<=before[1]:
        report.error('version_order','metadata','Dataset must match and content_version must increase')
    old_signatures=signatures(old); new_signatures=signatures(db)
    current={r[0]:r[1:] for r in db.execute('SELECT id,kind,revision,created_at FROM content_items')}
    for item_id,kind,revision,created in old.execute('SELECT id,kind,revision,created_at FROM content_items'):
        new=current.get(item_id)
        if new is None or new[0]!=kind or new[1]<revision or new[2]!=created:
            report.error('stable_id_policy',item_id,'Deleted/retyped ID, revision downgrade, or changed created_at'); continue
        if old_signatures[item_id]!=new_signatures[item_id] and new[1]<=revision:
            report.error('revision_required',item_id,'Payload/metadata/relationship changed without increased revision')


def validate_listening(db,report):
    for level,order in db.execute("SELECT i.level,l.learning_order FROM listening_items l JOIN content_items i ON i.id=l.id GROUP BY i.level,l.learning_order HAVING COUNT(*)>1"):
        report.error('listening_order',level,'Editorial order must be unique within level')
    for lid,source,mode,asset in db.execute('SELECT id,source_example_id,audio_mode,audio_asset_id FROM listening_items'):
        example=db.execute('SELECT e.korean,e.japanese,i.level,i.is_active FROM examples e JOIN content_items i ON i.id=e.id WHERE e.id=?',(source,)).fetchone()
        level=db.execute('SELECT level FROM content_items WHERE id=?',(lid,)).fetchone()[0]
        if not example or not example[3]:
            report.error('listening_source',lid,'Need active production example reference');continue
        text=example[0]
        if level!=example[2] or level not in LEVELS: report.error('listening_level',lid,'Level must match source example')
        if len(text)>500: report.error('listening_length',lid,'Max 500 characters')
        if mode=='tts':
            if asset is not None or any(c in text for c in '[]/→+') or any(0x1100<=ord(c)<=0x11ff or 0x3130<=ord(c)<=0x318f for c in text) or not any(0xac00<=ord(c)<=0xd7a3 for c in text):
                report.error('listening_audio',lid,'TTS needs original Korean sentence')
        elif mode=='recorded_required' and asset is None: report.error('listening_audio',lid,'Published listening needs a verified recording')
        rows=list(db.execute('SELECT id,question_type,prompt_ko,rubric_json,answer_json FROM questions WHERE listening_id=?',(lid,)))
        if len(rows)!=1: report.error('listening_question',lid,'One question per stable listening item')
        for qid,kind,prompt,rubric,answer in rows:
            try:
                qlevel=db.execute('SELECT level FROM content_items WHERE id=?',(qid,)).fetchone()[0]
                if qlevel!=level: raise ValueError()
                r=strict_json(rubric);a=strict_json(answer);task=r.get('listening_task')
                if task not in ('meaning','korean','dictation','comprehension') or prompt is not None: raise ValueError()
                if task=='dictation':
                    accepted=a.get('accepted')
                    norm=lambda x:' '.join(unicodedata.normalize('NFC',x).split())
                    if kind!='listening_input' or not isinstance(accepted,list) or not accepted or text not in accepted or any(not isinstance(v,str) or not v.strip() for v in accepted): raise ValueError()
                    if len({norm(v) for v in accepted})!=len(accepted): raise ValueError()
                    # Only terminal punctuation variants; synonyms are not dictation answers.
                    if any(norm(v).rstrip('.!?')!=norm(text).rstrip('.!?') for v in accepted): raise ValueError()
                else:
                    choices=list(db.execute('SELECT choice_id,text FROM question_choices WHERE question_id=? ORDER BY ordinal',(qid,)))
                    ids=a.get('correct_choice_ids')
                    if kind!='listening_choice' or not 2<=len(choices)<=6 or len({normalize(v) for _,v in choices})!=len(choices) or not isinstance(ids,list) or len(ids)!=1: raise ValueError()
                    correct=dict(choices).get(ids[0])
                    if task=='korean':
                        if correct!=text or any(not db.execute('SELECT 1 FROM examples WHERE korean=?',(v,)).fetchone() for _,v in choices): raise ValueError()
                    if task=='meaning' and correct!=example[1]: raise ValueError()
            except (ValueError,TypeError,AttributeError): report.error('listening_contract',qid,'Invalid task, transcript leak, accepted answers or distractors')
