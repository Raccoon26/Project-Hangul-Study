"""Repository evidence + actual SQL routing audit; never a Swift/iOS certification."""
import argparse
import collections
import hashlib
import json
import re
import sqlite3
import subprocess
from pathlib import Path
from audit_data08_final import audit, cohorts
from build_content import ROOT
from test_data05_content import query


def run():
    source=json.loads((ROOT/'Content/production.json').read_text());db=sqlite3.connect((ROOT/'Resources/content.sqlite').as_uri()+'?mode=ro',uri=True)
    structural=audit(source,ROOT/'Resources/content.sqlite');assert structural['validation']['error_count']==0
    sha=lambda p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
    inventory=[]
    for prefix,end in [('DEV',14),('DATA',7)]:
        for n in range(1,end+1):
            filename=f'Docs/{prefix}-{n:02}_STATUS.md' if not(prefix=='DATA'and n==7)else'Docs/DATA07_REVIEW.md'
            text=(ROOT/filename).read_text()
            inventory.append(dict(stage=f'{prefix}-{n:02}',evidence=filename,sha256=sha(filename),kind='archived implementation/review report, not original task specification',original_task_specification='NOT LOCATED',headings=[l for l in text.splitlines()if l.startswith('#')],reported_limitations=[l for l in text.splitlines()if any(w in l for w in ('미구현','미완료','未実施','미실행','아직','한계'))]))
    rows={t:{r['id']:r for r in values if'id'in r}for t,values in source['tables'].items()}
    words=[w for b in cohorts().values()for w in b['vocabulary']]
    editorial=json.loads((ROOT/'Docs/DATA08_FINAL_EDITORIAL.json').read_text())
    approved={r['id']:r['payload_sha256']for r in editorial['records']}
    for w in words:
        payload=dict(vocabulary=rows['vocabulary'][w['id']],meanings=[rows['meanings'][i]for i in w['meaning_ids']],examples=[rows['examples'][i]for i in w['example_ids']],note=rows['learner_notes'].get(w['note_id']))
        assert hashlib.sha256(json.dumps(payload,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()==approved[w['id']]
    vocab_ids=[r[0]for r in db.execute('SELECT id FROM vocabulary')]
    meanings=0;visible_examples=set()
    for wid in vocab_ids:
        assert db.execute(query('SQLiteVocabularyContent','SELECT v.headword'),[wid]).fetchone()
        m=db.execute(query('SQLiteVocabularyContent','SELECT m.*'),[wid]).fetchall();assert m
        for meaning in m:
            assert db.execute(query('SQLiteVocabularyContent','SELECT e.id'),[meaning[0]]).fetchone();meanings+=1
        assert db.execute(query('SQLiteLookup','SELECT i.level'),[wid,'vocabulary']).fetchone()
        visible_examples.update(r[0]for r in db.execute(query('SQLiteContentRepository','SELECT DISTINCT e.id'),[wid]))
    courses=db.execute(query('SQLiteContentRepository','SELECT c.*')).fetchall();generic_lessons=set();generic_questions=set();kinds=collections.Counter()
    for course in courses:
        for lesson in db.execute(query('SQLiteContentRepository','SELECT l.id,l.title_ja'),[course[0]]):
            generic_lessons.add(lesson[0]);steps=db.execute(query('SQLiteContentRepository','SELECT i.id,i.kind'),[lesson[0]]).fetchall();assert 1<=len(steps)<=200
            for step in steps:
                assert step[1]in ('hangul','note','question','pronunciation','vocabulary');kinds[step[1]]+=1
                if step[1]=='question':generic_questions.add(step[0])
    grammar_ids=[r[0]for r in db.execute('SELECT id FROM grammar')];grammar_lessons=set();grammar_questions=set();level_stats={}
    for level in ('hangul','intro','beginner','lower_intermediate','intermediate','upper_intermediate','advanced','master','maintenance'):
        level_stats[level]={}
        for kind in ('vocabulary','grammar','listening','lesson'):
            seen=[];after=''
            while True:
                page=db.execute(query('SQLiteCurriculum','SELECT id FROM content_items'),[level,kind,after,kind]).fetchall()
                if not page:break
                assert len(page)<=200;seen.extend(r[0]for r in page);after=page[-1][0]
            assert len(seen)==len(set(seen));level_stats[level][kind]=len(seen)
        after=-1
        while True:
            page=db.execute(query('SQLiteGrammarContent','SELECT l.id,l.title_ja'),[level,after,30]).fetchall()
            if not page:break
            grammar_lessons.update(r[0]for r in page);after=page[-1][2]
    for gid in grammar_ids:
        assert db.execute(query('SQLiteGrammarContent','SELECT g.*,i.revision'),[gid]).fetchone()
        examples=db.execute(query('SQLiteGrammarContent','SELECT e.id'),[gid]).fetchall();assert examples
        visible_examples.update(r[0]for r in examples)
        q=db.execute(query('SQLiteGrammarContent','SELECT q.*,i.revision'),[gid]).fetchall();assert 1<=len(q)<=20;grammar_questions.update(r[0]for r in q)
        assert db.execute(query('SQLiteLookup','SELECT i.level'),[gid,'grammar']).fetchone()
    productions=set();production_questions=set();after=''
    while True:
        page=db.execute(query('SQLiteProduction','SELECT DISTINCT v.id,v.headword'),[after]).fetchall()
        if not page:break
        assert len(page)<=30;productions.update(r[0]for r in page);after=page[-1][0]
    for wid in productions:
        q=db.execute(query('SQLiteProduction','SELECT q.*'),[wid]).fetchall();assert 1<=len(q)<=20;production_questions.update(r[0]for r in q)
    listening=set();listening_questions=set();listening_batches=0
    for level in level_stats:
        after=-1
        while True:
            page=db.execute(query('SQLiteListening','SELECT l.learning_order/20'),[level,after]).fetchall()
            if not page:break
            assert len(page)<=30
            for batch,count in page:
                ids=[r[0]for r in db.execute(query('SQLiteListening','SELECT l.id FROM listening_items'),[level,batch*20,(batch+1)*20])];assert len(ids)==count<=20
                q=db.execute(query('SQLiteListening','SELECT q.*,l.id')+' AND l.id IN ('+','.join('?'for _ in ids)+') ORDER BY l.learning_order,l.id LIMIT 20',ids).fetchall();assert len(q)==count
                listening.update(ids);listening_questions.update(r[0]for r in q);listening_batches+=1
            after=page[-1][0]
    visible_examples.update(r[0]for r in db.execute('SELECT example_id FROM pronunciation_examples'))
    visible_examples.update(r[0]for r in db.execute('SELECT source_example_id FROM listening_items'))
    all_examples={r[0]for r in db.execute('SELECT id FROM examples')};assert visible_examples==all_examples
    guard_checked=0
    for lemma,pos,irregular,rubric in db.execute("SELECT v.headword,v.part_of_speech,v.irregular_type,q.rubric_json FROM questions q JOIN content_links l ON l.source_id=q.id JOIN vocabulary v ON v.id=l.target_id WHERE l.relation='question_target' AND json_extract(q.rubric_json,'$.production')=1"):
        rubric=json.loads(rubric);form=rubric['form'];override=rubric['overrides'].get(form)
        assert pos in ('verb','adjective') and lemma.endswith('다') and len(lemma)>1 and irregular in ('none','other','b','d','s','reu','h')
        if not override:
            assert lemma!='푸다' and (irregular!='other' or lemma.endswith('하다'))
            assert not(form=='wish'and pos!='verb')
            assert not(form=='negativeShort'and lemma.endswith('하다')and lemma!='하다')
            assert not(irregular=='h'and form in ('present','past','reason','negativeShort'))
        guard_checked+=1
    allq={r[0]for r in db.execute('SELECT id FROM questions')};covered=generic_questions|grammar_questions|production_questions|listening_questions;assert allq==covered
    # Meaning/Example association for the 581 reused sentence questions is exact.
    integration=json.loads((ROOT/'Content/data08-integration-ids.json').read_text())
    for item in integration['production']:
        first=db.execute('SELECT id FROM meanings WHERE vocabulary_id=? ORDER BY ordinal,id LIMIT 1',[item['vocabulary_id']]).fetchone()[0]
        assert db.execute('SELECT 1 FROM vocabulary_examples WHERE meaning_id=? AND example_id=?',[first,item['example_id']]).fetchone()
    # Typed dictionary + literal/ranked Korean headword queries for all lexical IDs.
    searched=0
    for wid,headword in db.execute('SELECT id,headword FROM vocabulary'):
        found=set();offset=0
        while True:
            page=db.execute(query('SQLiteLookup','WITH terms'),[headword]*3+[offset]).fetchall();found.update(page)
            if len(page)<30:break
            offset+=30
        assert (wid,'vocabulary')in found;searched+=1
    ja_samples=[]
    for index,(wid,term)in enumerate(db.execute('SELECT vocabulary_id,meaning_ja FROM meanings ORDER BY id')):
        if index%34:continue
        page=db.execute(query('SQLiteLookup','WITH terms'),[term]*3+[0]).fetchall()
        assert (wid,'vocabulary')in page
        ja_samples.append(dict(vocabulary_id=wid,term=term))
    native=sum(len(re.findall(r'func test\w+\s*\(',p.read_text()))for p in (ROOT/'Tests').glob('*.swift'))
    result=dict(baseline_commit='42441768ea3ce39490350ed217021cfad58eae71',source_sha256=sha('Content/production.json'),bundle_sha256=sha('Resources/content.sqlite'),metadata=source['metadata'],structural=structural,specification_inventory=inventory,original_specification_limit='No complete original DEV01–14/DATA01–07 task specifications found; archived reports are evidence of recorded contracts only. DATA08 requests are available in the current conversation, AGENTS.md, and cumulative DATA08_PROGRESS.md.',coverage=dict(vocabulary_cards=len(vocab_ids),meaning_examples=meanings,reachable_examples=len(visible_examples),unreachable_examples=len(all_examples-visible_examples),published_production_guard_checked=guard_checked,typed_dictionary=len(vocab_ids)+len(grammar_ids),generic_courses=len(courses),generic_lessons=len(generic_lessons),generic_steps_by_kind=dict(kinds),grammar_lessons=len(grammar_lessons),grammar_cards=len(grammar_ids),production_entries=len(productions),production_questions=len(production_questions),listening_items=len(listening),listening_questions=len(listening_questions),listening_batches=listening_batches,routed_questions=len(covered),unrouted_questions=len(allq-covered),korean_headword_queries=searched,japanese_meaning_queries=len(ja_samples),data08_current_editorial_payload_hash_matches=len(words),data08_sentence_first_meaning_matches=len(integration['production'])),levels=level_stats,japanese_samples=ja_samples,native=dict(definitions=native,executed=0,status='BLOCKED: no Xcode/Swift/iOS SDK'),independent_language_review='NOT TESTED; previous assistant review is not human certification')
    db.close();return result


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--report',type=Path,required=True);args=parser.parse_args()
    result=run();args.report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result['coverage'],ensure_ascii=False))
