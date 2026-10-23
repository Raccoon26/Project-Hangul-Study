import XCTest
import SQLite3

/// Uses the real app, bundled Production database and persistent app container.
/// Use a dedicated Simulator, or the opt-in Release UI-only device scheme.
/// Never erases/replaces a user's database or clears their purchase cache.
@MainActor
final class StudyJourneyTests: XCTestCase {
    private let app = XCUIApplication()
    override func setUp() async throws {
        await MainActor.run {
        continueAfterFailure = false
        app.launch()
        XCTAssertTrue(app.tabBars.buttons["学ぶ"].waitForExistence(timeout:30))
        }
    }
    override func tearDown() async throws {
        await MainActor.run {
        let screenshot = XCTAttachment(screenshot:app.screenshot())
        screenshot.name = name; screenshot.lifetime = .keepAlways; add(screenshot)
        let tree = XCTAttachment(string:app.debugDescription)
        tree.name = name+" accessibility tree"; tree.lifetime = .keepAlways; add(tree)
        app.terminate()
        }
    }
    private func tap(_ title: String, contains: Bool = false, file: StaticString = #filePath, line: UInt = #line) {
        let predicate = NSPredicate(format:contains ? "label CONTAINS %@" : "label == %@",title)
        let target = app.buttons.matching(predicate).firstMatch
        XCTAssertTrue(reveal(target),"Button unavailable: "+title+"\n"+app.debugDescription,file:file,line:line)
        if target.exists && target.isHittable {
            let enabled = XCTNSPredicateExpectation(predicate:NSPredicate(format:"enabled == true"),object:target)
            XCTAssertEqual(XCTWaiter.wait(for:[enabled],timeout:10),.completed,"Button must finish its transaction before accepting another action",file:file,line:line)
            // SwiftUI can retain an old AX activation point after the keyboard
            // moves a bottom inset. Tap the current, verified visible frame.
            target.coordinate(withNormalizedOffset:CGVector(dx:0.5,dy:0.5)).tap()
        }
    }
    private func reveal(_ target: XCUIElement) -> Bool {
        for _ in 0..<40 {
            if fullyVisible(target) { return true }
            scrollToward(target)
        }
        return fullyVisible(target)
    }
    private func fullyVisible(_ target: XCUIElement) -> Bool {
        guard target.exists, target.isHittable else { return false }
        let frame = target.frame
        let top = app.navigationBars.firstMatch.exists ? app.navigationBars.firstMatch.frame.maxY : app.frame.minY
        var bottom = app.frame.maxY
        let sameLabel = NSPredicate(format:"label == %@",target.label)
        let inScroll = app.scrollViews.buttons.matching(sameLabel).firstMatch.exists
        let inList = app.collectionViews.buttons.matching(sameLabel).firstMatch.exists
        let tabs = app.tabBars.firstMatch
        // A covered root tab bar can remain in the AX tree of a full-screen
        // session. It is not the viewport boundary of that session's buttons.
        if inList && !inScroll && tabs.exists && tabs.isHittable && !tabs.frame.isEmpty { bottom = min(bottom,tabs.frame.minY) }
        if inScroll {
            for title in ["次へ","答える","意味を見る","覚える","覚えてる"] {
                let sticky = app.buttons[title]
                if sticky.exists && sticky.isHittable && !app.scrollViews.buttons[title].exists {
                    bottom = min(bottom,sticky.frame.minY-8)
                }
            }
        }
        let keyboard = app.keyboards.firstMatch
        if keyboard.exists { bottom = min(bottom,keyboard.frame.minY) }
        return frame.minY >= top && frame.maxY <= bottom
    }
    private func scrollToward(_ target: XCUIElement, alignEnd: Bool = false) {
        // A full-screen swipe can jump past a short row at accessibility sizes.
        // Use a bounded drag and reverse direction if its frame is above us.
        let above = target.exists && (alignEnd ? target.frame.maxY < app.navigationBars.firstMatch.frame.maxY+44 : target.frame.midY < app.frame.midY)
        let start = app.coordinate(withNormalizedOffset:CGVector(dx:0.5,dy:above ? 0.4 : 0.7))
        let end = app.coordinate(withNormalizedOffset:CGVector(dx:0.5,dy:above ? 0.7 : 0.4))
        start.press(forDuration:0.05,thenDragTo:end)
    }
    private func level(_ title: String) {
        app.terminate(); app.launch()
        XCTAssertTrue(app.tabBars.buttons["学ぶ"].waitForExistence(timeout:30))
        tap("すべての学習段階")
        XCTAssertTrue(app.navigationBars["学習コース"].waitForExistence(timeout:10))
        let row = app.collectionViews.buttons[title]
        for _ in 0..<40 { if row.exists && row.isHittable { break }; scrollToward(row) }
        XCTAssertTrue(row.waitForExistence(timeout:10)); row.tap()
        XCTAssertTrue(app.navigationBars[title].waitForExistence(timeout:10))
    }
    private func rows(_ sql: String) throws -> [[String:String]] {
        let url = try XCTUnwrap(Bundle(for:Self.self).url(forResource:"content",withExtension:"sqlite"))
        var db: OpaquePointer?, statement: OpaquePointer?
        XCTAssertEqual(sqlite3_open_v2(url.path,&db,SQLITE_OPEN_READONLY,nil),SQLITE_OK)
        defer { sqlite3_finalize(statement); sqlite3_close(db) }
        XCTAssertEqual(sqlite3_prepare_v2(db,sql,-1,&statement,nil),SQLITE_OK)
        var result: [[String:String]] = []
        while sqlite3_step(statement) == SQLITE_ROW {
            var row: [String:String] = [:]
            for column in 0..<sqlite3_column_count(statement) {
                if let value = sqlite3_column_text(statement,column) {
                    row[String(cString:sqlite3_column_name(statement,column))] = String(cString:value)
                }
            }
            result.append(row)
        }
        return result
    }
    private var searchInput: XCUIElement { app.textFields["dictionary-search"] }
    private var input: XCUIElement {
        app.textFields.matching(NSPredicate(format:"label IN %@",["韓国語の答え","聞こえた韓国語を入力"])).firstMatch
    }
    private func replaceInput(_ value: String) {
        let field = input
        XCTAssertTrue(field.waitForExistence(timeout:10)); XCTAssertTrue(field.isEnabled); field.tap()
        let previous = field.value as? String ?? ""
        if !previous.isEmpty && previous != field.placeholderValue {
            // Tapping a restored field can put the caret at the beginning.
            // Select the actual text; backspace-counting from an unknown caret
            // position could append a second answer and test the wrong input.
            field.press(forDuration:1.2)
            let selectAll = app.descendants(matching:.any).matching(NSPredicate(
                format:"label IN %@ AND (elementType == %d OR elementType == %d)",
                ["すべてを選択","Select All","모두 선택"],XCUIElement.ElementType.menuItem.rawValue,XCUIElement.ElementType.button.rawValue)).firstMatch
            for _ in 0..<5 {
                if selectAll.waitForExistence(timeout:1) { break }
                // At accessibility sizes UIKit puts Select All on the next page.
                let next = app.buttons.matching(NSPredicate(format:"label IN %@",["進む","Next","다음"])).firstMatch
                if next.exists { next.tap() } else { break }
            }
            XCTAssertTrue(selectAll.exists,"Restored text must be selected before replacement\n"+app.debugDescription)
            selectAll.tap()
            field.typeText(XCUIKeyboardKey.delete.rawValue)
        }
        field.typeText(value)
        XCTAssertEqual(field.value as? String,value,"The UI must receive exactly the intended test answer")
    }
    private func answerText(_ row: [String:String]) throws -> String {
        let data = Data(try XCTUnwrap(row["answer_json"]).utf8)
        let answer = try XCTUnwrap(JSONSerialization.jsonObject(with:data) as? [String:Any])
        return try XCTUnwrap((answer["accepted"] as? [String])?.first)
    }
    private func completeLesson(level name: String,title: String,id: String) throws {
        level(name); tap(title,contains:true)
        if app.buttons["もう一度"].waitForExistence(timeout:1) { tap("もう一度") }
        let steps = try rows("SELECT i.id,i.kind FROM lesson_items li JOIN content_items i ON i.id=li.content_id WHERE li.lesson_id='\(id)' AND i.is_active=1 ORDER BY li.ordinal")
        XCTAssertFalse(steps.isEmpty)
        for (index,step) in steps.enumerated() {
            XCTAssertTrue(app.staticTexts["\(index+1) / \(steps.count)"].waitForExistence(timeout:10))
            if step["kind"] == "question" {
                let question = try XCTUnwrap(step["id"])
                let correct = try XCTUnwrap(rows("SELECT c.text FROM question_choices c JOIN questions q ON q.id=c.question_id WHERE q.id='\(question)' AND c.choice_id=json_extract(q.answer_json,'$.correct_choice_ids[0]')").first?["text"])
                tap(correct); tap("答える")
                XCTAssertTrue(app.staticTexts.matching(NSPredicate(format:"label CONTAINS %@","正解")).firstMatch.waitForExistence(timeout:10))
            }
            tap(index+1 == steps.count ? "レッスンを完了する" : "次へ")
        }
        XCTAssertTrue(app.staticTexts["完了"].waitForExistence(timeout:10))
        app.terminate(); app.launch()
        XCTAssertTrue(app.tabBars.buttons["学ぶ"].waitForExistence(timeout:30))
        tap("すべての学習段階"); tap(name)
        let completed = app.buttons.matching(NSPredicate(format:"label CONTAINS %@ AND label CONTAINS %@",title,"完了")).firstMatch
        for _ in 0..<12 { if completed.exists { break }; app.swipeUp() }
        XCTAssertTrue(completed.exists,"Completed lesson must persist after cold launch")
    }
    func test01OnboardingHangulAndColdResume() throws {
        if app.buttons["学習の開始位置を選ぶ"].exists { tap("学習の開始位置を選ぶ") }
        else { tap("開始位置・レベル診断") }
        tap("韓国語は初めて"); tap("この位置を保存")
        XCTAssertTrue(app.buttons["保存しました"].waitForExistence(timeout:10))
        tap("ここから始める：ハングル")
        tap("基本母音①")
        XCTAssertTrue(app.staticTexts["母音"].waitForExistence(timeout:10))
        tap("次へ")
        let before = app.staticTexts.matching(NSPredicate(format:"label CONTAINS %@"," / ")).allElementsBoundByIndex.map(\.label)
        app.terminate(); app.launch()
        XCTAssertTrue(app.tabBars.buttons["学ぶ"].waitForExistence(timeout:30))
        tap("文字・発音の続き")
        XCTAssertTrue(app.staticTexts["母音"].waitForExistence(timeout:10))
        let after = app.staticTexts.matching(NSPredicate(format:"label CONTAINS %@"," / ")).allElementsBoundByIndex.map(\.label)
        XCTAssertEqual(before,after)
        XCTAssertFalse(app.buttons["意味を見る"].exists)
    }
    func test02SearchDictionaryFavoriteAndSettingsPersist() throws {
        app.tabBars.buttons["調べる"].tap()
        let search = searchInput
        XCTAssertTrue(search.waitForExistence(timeout:10)); search.tap(); search.typeText("시작되다\n")
        tap("시작되다",contains:true)
        tap("主な活用")
        XCTAssertTrue(app.staticTexts["시작돼요"].waitForExistence(timeout:10))
        XCTAssertTrue(app.staticTexts["시작됐어요"].exists)
        if app.buttons["保存する"].exists { tap("保存する") }
        XCTAssertTrue(app.buttons["保存を解除"].waitForExistence(timeout:10))
        app.terminate(); app.launch()
        XCTAssertTrue(app.tabBars.buttons["調べる"].waitForExistence(timeout:30))
        app.tabBars.buttons["調べる"].tap(); tap("保存した項目・苦手な項目")
        tap("시작되다",contains:true)
        XCTAssertTrue(app.buttons["保存を解除"].waitForExistence(timeout:10),"The saved entry must reopen with its persisted favorite state")
        app.tabBars.buttons["設定"].tap(); tap("新しく始める復習の量",contains:true)
        tap("多め · 20語")
        app.terminate(); app.launch()
        XCTAssertTrue(app.tabBars.buttons["設定"].waitForExistence(timeout:30))
        app.tabBars.buttons["設定"].tap()
        XCTAssertTrue(app.buttons.matching(NSPredicate(format:"label CONTAINS %@","20語")).firstMatch.waitForExistence(timeout:10))
        app.terminate(); app.launch()
        XCTAssertTrue(app.tabBars.buttons["調べる"].waitForExistence(timeout:30)); app.tabBars.buttons["調べる"].tap()
        let colorSearch = searchInput
        XCTAssertTrue(colorSearch.waitForExistence(timeout:10)); colorSearch.tap(); colorSearch.typeText("파랗다\n")
        tap("파랗다",contains:true); tap("主な活用")
        XCTAssertTrue(app.staticTexts["파래요"].waitForExistence(timeout:10))
        XCTAssertTrue(app.staticTexts["파랬어요"].exists)
    }
    func test03JamoBatchimPronunciationAndLessonCompletionPersist() throws {
        try completeLesson(level:"ハングル",title:"基本子音①",id:"9d7df0d8-14fc-4b17-8e01-d7ff6b6c89ca")
        try completeLesson(level:"入門",title:"パッチムの位置",id:"c4466eef-a47a-495b-821c-87313ada66e0")
        try completeLesson(level:"入門",title:"鼻へつながる・鼻音化",id:"a24aaa34-4cef-4ad2-a928-d5b554a2e35c")
    }
    func test04VocabularyRoundCompletionAndMidSessionResume() throws {
        level("入門"); tap("単語 · 小さなセットで回読"); tap("新しいセットを始める")
        XCTAssertTrue(app.buttons["意味を見る"].waitForExistence(timeout:10))
        XCTAssertGreaterThan(app.staticTexts.matching(NSPredicate(format:"label MATCHES %@",".*[가-힣].*")).count,0)
        for index in 0..<20 {
            XCTAssertTrue(app.staticTexts["\(index+1) / 20"].waitForExistence(timeout:10))
            tap("意味を見る"); tap(index == 0 ? "覚える" : "覚えてる")
            if index == 3 {
                app.terminate(); app.launch()
                XCTAssertTrue(app.tabBars.buttons["学ぶ"].waitForExistence(timeout:30))
                tap("単語の続き")
                XCTAssertTrue(app.staticTexts["5 / 20"].waitForExistence(timeout:10))
                XCTAssertTrue(app.buttons["意味を見る"].exists)
            }
        }
        XCTAssertTrue(app.staticTexts["次は1語"].waitForExistence(timeout:10))
        tap("2周目へ"); tap("意味を見る"); tap("覚えてる")
        XCTAssertTrue(app.staticTexts["完了"].waitForExistence(timeout:10))
        app.terminate(); app.launch()
        XCTAssertTrue(app.tabBars.buttons["記録"].waitForExistence(timeout:30)); app.tabBars.buttons["記録"].tap()
        XCTAssertFalse(app.staticTexts["データを開けませんでした"].exists)
        let evidence = XCTAttachment(string:app.debugDescription); evidence.name = "Vocabulary completion statistics"; evidence.lifetime = .keepAlways; add(evidence)
    }
    func test05GrammarExplanationQuestionsCompletionAndColdResume() throws {
        level("入門"); tap("文法 · 意味と使い方"); tap("名詞と助詞①",contains:true)
        if app.buttons["もう一度学ぶ"].waitForExistence(timeout:1) { tap("もう一度学ぶ") }
        let cards = try rows("SELECT g.id,g.pattern FROM lesson_items li JOIN grammar g ON g.id=li.content_id WHERE li.lesson_id='05a850ab-dfde-46c8-812e-6bc41132f1fa' ORDER BY li.ordinal")
        for (index,card) in cards.enumerated() {
            let pattern = try XCTUnwrap(card["pattern"])
            XCTAssertTrue(app.staticTexts[pattern].waitForExistence(timeout:10))
            tap("次へ"); tap("次へ"); tap("問題へ")
            let id = try XCTUnwrap(card["id"])
            let quizzes = try rows("SELECT q.id,q.prompt_ja,c.text FROM content_links l JOIN questions q ON q.id=l.source_id JOIN question_choices c ON c.question_id=q.id AND c.choice_id=json_extract(q.answer_json,'$.correct_choice_ids[0]') WHERE l.target_id='\(id)' AND l.relation='question_target' ORDER BY q.id")
            XCTAssertFalse(quizzes.isEmpty)
            for quiz in quizzes {
                let prompt = try XCTUnwrap(quiz["prompt_ja"])
                XCTAssertTrue(app.staticTexts[prompt].waitForExistence(timeout:10))
                tap(try XCTUnwrap(quiz["text"]))
                XCTAssertTrue(app.staticTexts["正解"].waitForExistence(timeout:10))
                tap("次へ")
            }
            if index == 0 {
                app.terminate(); app.launch()
                XCTAssertTrue(app.tabBars.buttons["学ぶ"].waitForExistence(timeout:30)); tap("文法の続き")
                XCTAssertTrue(app.buttons["覚えてる"].waitForExistence(timeout:10))
            }
            tap("覚えてる")
        }
        XCTAssertTrue(app.staticTexts["完了"].waitForExistence(timeout:10))
        XCTAssertTrue(app.staticTexts.matching(NSPredicate(format:"label CONTAINS %@","復習予定を保存しました")).firstMatch.exists)
    }
    func test06IrregularConjugationInputDraftColdResumeAndGrading() throws {
        app.tabBars.buttons["調べる"].tap()
        let search = searchInput
        XCTAssertTrue(search.waitForExistence(timeout:10)); search.tap(); search.typeText("걷다\n")
        tap("걷다",contains:true); tap("主な活用")
        XCTAssertTrue(app.staticTexts["걸어요"].waitForExistence(timeout:10))
        tap("活用・入力を練習")
        if app.buttons["もう一度"].waitForExistence(timeout:1) { tap("もう一度") }
        let questions = try rows("SELECT q.* FROM questions q JOIN content_links l ON l.source_id=q.id WHERE l.target_id='1b03a139-026f-42c1-bcc5-9c5d6612ea77' AND l.relation='question_target' AND q.question_type='text_input' ORDER BY q.id")
        XCTAssertEqual(questions.count,3) // Reviewed present, past and condition.
        for (index,q) in questions.enumerated() {
            let answer = try answerText(q)
            if app.buttons["入力してみる"].waitForExistence(timeout:1) {
                XCTAssertTrue(app.staticTexts[answer].waitForExistence(timeout:10))
                tap("入力してみる")
            }
            // An interrupted QA run may already have saved this input phase.
            // It must still show the same real question and be graded below.
            XCTAssertTrue(app.staticTexts[try XCTUnwrap(q["prompt_ja"])].waitForExistence(timeout:10))
            if index == 0 {
                replaceInput(String(answer.prefix(2)))
                app.terminate(); app.launch()
                XCTAssertTrue(app.tabBars.buttons["学ぶ"].waitForExistence(timeout:30)); tap("活用・入力の続き")
                XCTAssertTrue(input.waitForExistence(timeout:10)); XCTAssertEqual(input.value as? String,String(answer.prefix(2)))
            }
            replaceInput(answer)
            XCTAssertGreaterThanOrEqual(app.buttons["答える"].frame.height,44)
            tap("答える")
            XCTAssertTrue(app.staticTexts["✓ 正解"].waitForExistence(timeout:10)); tap("次へ")
        }
        XCTAssertTrue(app.staticTexts["練習完了"].waitForExistence(timeout:10))
    }
    func test07ListeningFourTasksRealNormalSlowTTSAndDictationResume() throws {
        level("入門"); tap("リスニング・書き取り"); tap("練習 1 ·",contains:true)
        if app.buttons["もう一度練習"].waitForExistence(timeout:1) { tap("もう一度練習") }
        let questions = try rows("SELECT q.*,e.korean,e.japanese,json_extract(q.rubric_json,'$.listening_task') AS task FROM listening_items l JOIN content_items i ON i.id=l.id JOIN examples e ON e.id=l.source_example_id JOIN questions q ON q.listening_id=l.id WHERE i.level='intro' AND l.learning_order/20=0 ORDER BY l.learning_order,l.id")
        XCTAssertEqual(questions.count,12)
        XCTAssertEqual(Set(questions.compactMap { $0["task"] }),Set(["meaning","korean","dictation","comprehension"]))
        var resumedDraft = false
        for (index,q) in questions.enumerated() {
            let korean = try XCTUnwrap(q["korean"])
            XCTAssertTrue(app.staticTexts["\(index+1) / \(questions.count)"].waitForExistence(timeout:10))
            XCTAssertFalse(app.staticTexts["韓国語の原文："+korean].exists,"Transcript must be absent before grading")
            if q["task"] == "dictation" && !resumedDraft {
                let prefix = String(korean.prefix(3)); replaceInput(prefix)
                app.terminate(); app.launch()
                XCTAssertTrue(app.tabBars.buttons["学ぶ"].waitForExistence(timeout:30)); tap("リスニングの続き")
                XCTAssertTrue(input.waitForExistence(timeout:10)); XCTAssertEqual(input.value as? String,prefix)
                XCTAssertFalse(app.buttons["答える"].isEnabled); resumedDraft = true
            }
            if q["task"] == "dictation" {
                var answer = try answerText(q)
                while let last = answer.last, ".!?".contains(last) { answer.removeLast() }
                replaceInput(answer)
                tap(index == 1 ? "ゆっくり" : "聞く")
                let ready = XCTNSPredicateExpectation(predicate:NSPredicate(format:"enabled == true"),object:app.buttons["答える"])
                XCTAssertEqual(XCTWaiter.wait(for:[ready],timeout:30),.completed)
                tap("答える")
            } else {
                let id = try XCTUnwrap(q["id"])
                let correct = try XCTUnwrap(rows("SELECT c.text FROM question_choices c JOIN questions q ON q.id=c.question_id WHERE q.id='\(id)' AND c.choice_id=json_extract(q.answer_json,'$.correct_choice_ids[0]')").first?["text"])
                XCTAssertFalse(app.buttons[correct].exists,"Choices must be absent before successful playback")
                tap(index == 1 ? "ゆっくり" : "聞く")
                XCTAssertTrue(app.buttons[correct].waitForExistence(timeout:30)); tap(correct)
            }
            XCTAssertTrue(app.staticTexts["✓ 正解"].waitForExistence(timeout:10))
            XCTAssertTrue(app.staticTexts["韓国語の原文："+korean].exists)
            tap("次へ")
        }
        XCTAssertTrue(resumedDraft)
        XCTAssertTrue(app.staticTexts["練習完了"].waitForExistence(timeout:10))
        XCTAssertTrue(app.staticTexts["12 / 12 正解"].exists)
    }
    func test08Content29ListeningCourseFiveQuestionsContextAndResume() throws {
        let course = "初中級：日常・予定変更・移動・サービス・依頼"
        level("初中級")
        let listening = app.buttons["リスニング・書き取り"]
        XCTAssertTrue(listening.waitForExistence(timeout:10)); XCTAssertTrue(listening.isHittable)
        tap("リスニング・書き取り"); tap(course)
        tap("内容を聞き取る 1 ·",contains:true)
        if app.buttons["もう一度練習"].waitForExistence(timeout:1) { tap("もう一度練習") }
        let questions = try rows("SELECT q.id,e.id AS source,e.korean,e.learning_point_ja FROM lesson_items m JOIN listening_items l ON l.id=m.content_id JOIN examples e ON e.id=l.source_example_id JOIN questions q ON q.listening_id=l.id WHERE m.lesson_id='aea93dca-1d3d-4d3c-a4f8-aa7c5296500a' ORDER BY m.ordinal")
        XCTAssertEqual(questions.count,5)
        for (index,q) in questions.enumerated() {
            let korean = try XCTUnwrap(q["korean"]), id = try XCTUnwrap(q["id"])
            let correct = try XCTUnwrap(rows("SELECT c.text FROM question_choices c JOIN questions q ON q.id=c.question_id WHERE q.id='\(id)' AND c.choice_id=json_extract(q.answer_json,'$.correct_choice_ids[0]')").first?["text"])
            XCTAssertTrue(app.staticTexts["\(index+1) / 5"].waitForExistence(timeout:10))
            if !app.staticTexts["✓ 正解"].exists {
                XCTAssertFalse(app.buttons[correct].exists); XCTAssertFalse(app.staticTexts["韓国語の原文："+korean].exists)
                tap("聞く")
                XCTAssertTrue(app.buttons[correct].waitForExistence(timeout:40)); tap(correct)
            }
            XCTAssertTrue(app.staticTexts["✓ 正解"].waitForExistence(timeout:10))
            XCTAssertTrue(app.staticTexts["韓国語の原文："+korean].exists)
            if index == 0 {
                tap("ゆっくり")
                let finished = XCTNSPredicateExpectation(predicate:NSPredicate(format:"exists == false"),object:app.buttons["停止"])
                XCTAssertEqual(XCTWaiter.wait(for:[finished],timeout:40),.completed)
                app.terminate(); app.launch()
                XCTAssertTrue(app.tabBars.buttons["学ぶ"].waitForExistence(timeout:30)); tap("リスニングの続き")
                XCTAssertTrue(app.staticTexts["韓国語の原文："+korean].waitForExistence(timeout:10))
                XCTAssertTrue(app.staticTexts["✓ 正解"].exists)
                if let point = q["learning_point_ja"] { XCTAssertTrue(app.staticTexts[point].exists) }
                let source = try XCTUnwrap(q["source"])
                let word = try XCTUnwrap(rows("SELECT v.headword FROM content_links l JOIN vocabulary v ON v.id=l.target_id WHERE l.source_id='\(source)' AND l.relation IN ('related','prerequisite') LIMIT 1").first?["headword"])
                tap(word+" ·",contains:true)
                XCTAssertTrue(app.buttons["保存する"].waitForExistence(timeout:10) || app.buttons["保存を解除"].exists)
                app.navigationBars.buttons.firstMatch.tap()
                XCTAssertTrue(app.staticTexts["✓ 正解"].waitForExistence(timeout:10))
            }
            tap("次へ")
        }
        XCTAssertTrue(app.staticTexts["練習完了"].waitForExistence(timeout:10))
        XCTAssertTrue(app.staticTexts["5 / 5 正解"].exists)
        level("初中級"); tap("リスニング・書き取り"); tap(course)
        XCTAssertTrue(app.buttons.matching(NSPredicate(format:"label CONTAINS %@ AND label CONTAINS %@","内容を聞き取る 1 ·","確認済み")).firstMatch.waitForExistence(timeout:10))
    }
    func test09StatisticsMaintenanceAndFreeLearningSettings() throws {
        app.tabBars.buttons["記録"].tap()
        XCTAssertTrue(app.staticTexts.matching(NSPredicate(format:"label == %@","学習アクション")).firstMatch.waitForExistence(timeout:10))
        tap("維持学習")
        XCTAssertTrue(app.staticTexts.matching(NSPredicate(format:"label CONTAINS %@","今は追加の練習候補がありません")).firstMatch.waitForExistence(timeout:10))
        tap("予定された復習をする")
        XCTAssertFalse(app.staticTexts["データを開けませんでした"].exists)
        app.terminate(); app.launch()
        XCTAssertTrue(app.tabBars.buttons["設定"].waitForExistence(timeout:30)); app.tabBars.buttons["設定"].tap()
        tap("広告を削除・購入を復元")
        XCTAssertTrue(app.buttons["購入を復元"].waitForExistence(timeout:10))
        XCTAssertFalse(app.staticTexts["読み込み中"].exists)
        // No real purchase/consent is performed. All learning above remains free.
    }
    private func audit(last: XCUIElement) throws {
        let initial = XCTAttachment(screenshot:app.screenshot())
        initial.name = "Initial viewport before accessibility audit"; initial.lifetime = .keepAlways; add(initial)
        // Audit the stable initial viewport. A separate minimal SwiftUI List
        // passes here but reports offscreen contrast/unsupported fonts if the
        // audit starts at its end and then changes Dynamic Type internally.
        // Keep every audit category and every issue; also verify the real end
        // of this screen below instead of treating the audit as a scroll test.
        let previousFailurePolicy = continueAfterFailure
        continueAfterFailure = true
        defer { continueAfterFailure = previousFailurePolicy }
        try app.performAccessibilityAudit { issue in
            let details = XCTAttachment(string:issue.compactDescription+"\n"+issue.detailedDescription+"\n"+(issue.element?.debugDescription ?? "No element"))
            details.name = "Unfiltered accessibility issue"; details.lifetime = .keepAlways; self.add(details)
            return false // Always report every issue as a failure.
        }
        // Align an actual final item, not an estimated scroll offset. This also
        // prevents a blank overscroll viewport from being mistaken for an audit.
        var aligned = false
        for _ in 0..<60 {
            let top = app.navigationBars.firstMatch.frame.maxY
            let tabs = app.tabBars.firstMatch
            // A pushed screen can hide its tab bar. An absent/zero frame is not
            // a viewport boundary at y=0; align against the real screen instead.
            let bottom = tabs.exists && !tabs.frame.isEmpty ? tabs.frame.minY : app.frame.maxY
            if last.exists && (last.elementType != .button || last.isHittable) && last.frame.maxY <= bottom && last.frame.maxY > top+44 {
                aligned = true; break
            }
            scrollToward(last,alignEnd:true)
        }
        XCTAssertTrue(aligned,"The actual final content must be visible before auditing\n"+app.debugDescription)
        let measured = XCTAttachment(screenshot:app.screenshot())
        measured.name = "Final content visibility (separate from initial viewport audit)"; measured.lifetime = .keepAlways; add(measured)
    }
    func test10AccessibilityAuditHomeAndLearningEntry() throws {
        try audit(last:app.buttons["開始位置・レベル診断"])
        level("入門")
        try audit(last:app.staticTexts["curriculum-progress-note"])
    }
    func test11SearchSubmitDismissesKeyboardWithoutClearingResults() throws {
        app.tabBars.buttons["調べる"].tap()
        let search = searchInput
        XCTAssertTrue(search.waitForExistence(timeout:10)); search.tap(); search.typeText("시작되다\n")
        let hidden = XCTNSPredicateExpectation(predicate:NSPredicate(format:"exists == false"),object:app.keyboards.firstMatch)
        XCTAssertEqual(XCTWaiter.wait(for:[hidden],timeout:10),.completed)
        XCTAssertEqual(search.value as? String,"시작되다")
        tap("시작되다",contains:true)
        XCTAssertTrue(app.buttons["保存する"].waitForExistence(timeout:10) || app.buttons["保存を解除"].exists)
    }
    func test12BackgroundInterruptsRealSpeechWithoutRevealingAnswer() throws {
        level("初中級"); tap("リスニング・書き取り")
        tap("初中級：日常・予定変更・移動・サービス・依頼")
        tap("内容を聞き取る 2 ·",contains:true)
        let items = try rows("SELECT q.id,e.korean,c.text AS correct FROM lesson_items m JOIN listening_items l ON l.id=m.content_id JOIN examples e ON e.id=l.source_example_id JOIN questions q ON q.listening_id=l.id JOIN question_choices c ON c.question_id=q.id AND c.choice_id=json_extract(q.answer_json,'$.correct_choice_ids[0]') WHERE m.lesson_id='1012e5a4-5112-4c0f-bc5c-26d677f0c454' ORDER BY m.ordinal")
        XCTAssertEqual(items.count,5)
        var selected: [String:String]?
        // A repeated device run must honor the saved session. Advance already
        // heard/graded questions through the real UI rather than deleting data
        // or assuming the first question is still unheard.
        for _ in 0...items.count {
            if app.buttons["もう一度練習"].waitForExistence(timeout:1) { tap("もう一度練習") }
            let current = try XCTUnwrap(items.enumerated().first { app.staticTexts["\($0.offset+1) / 5"].exists })
            let answer = try XCTUnwrap(current.element["correct"])
            if app.staticTexts["✓ 正解"].exists { tap("次へ"); continue }
            if app.buttons["もう一度"].exists {
                tap("もう一度")
                XCTAssertTrue(app.buttons[answer].waitForExistence(timeout:40)); tap(answer)
                XCTAssertTrue(app.staticTexts["✓ 正解"].waitForExistence(timeout:10)); tap("次へ")
                continue
            }
            selected = current.element; break
        }
        let q = try XCTUnwrap(selected,"An unheard question is required to verify interruption without premature answer disclosure")
        let korean = try XCTUnwrap(q["korean"]), correct = try XCTUnwrap(q["correct"])
        tap("聞く")
        XCTAssertTrue(app.buttons["停止"].waitForExistence(timeout:5))
        XCUIDevice.shared.press(.home)
        XCTAssertTrue(app.wait(for:.runningBackground,timeout:10))
        app.activate()
        XCTAssertTrue(app.buttons["聞く"].waitForExistence(timeout:10))
        XCTAssertFalse(app.buttons["停止"].exists)
        XCTAssertFalse(app.buttons[correct].exists)
        XCTAssertFalse(app.staticTexts["韓国語の原文："+korean].exists)
        tap("聞く")
        XCTAssertTrue(app.buttons[correct].waitForExistence(timeout:40)); tap(correct)
        XCTAssertTrue(app.staticTexts["✓ 正解"].waitForExistence(timeout:10))
        XCUIDevice.shared.press(.home); app.activate()
        XCTAssertTrue(app.staticTexts["✓ 正解"].waitForExistence(timeout:10))
        XCTAssertTrue(app.staticTexts["韓国語の原文："+korean].exists)
    }
    func test13ColdLaunchToResponsiveLearningHome() {
        let options = XCTMeasureOptions(); options.iterationCount = 3
        measure(metrics:[XCTApplicationLaunchMetric(waitUntilResponsive:true),XCTMemoryMetric(application:app),XCTCPUMetric(application:app)],options:options) {
            app.terminate(); app.launch()
            XCTAssertTrue(app.tabBars.buttons["学ぶ"].waitForExistence(timeout:30))
            XCTAssertFalse(app.staticTexts["データを開けませんでした"].exists)
        }
    }
    func test14AccessibilityAuditLookupRecordsAndSettings() throws {
        // Record every issue; do not filter or accept any audit category.
        continueAfterFailure = true
        defer { continueAfterFailure = false }
        for title in ["調べる","記録","設定"] {
            app.tabBars.buttons[title].tap()
            XCTAssertTrue(app.navigationBars[title].waitForExistence(timeout:10))
            try XCTContext.runActivity(named:"Accessibility: "+title) { _ in
                let last: XCUIElement
                switch title {
                case "調べる": last = app.buttons["最近見た項目"]
                case "記録": last = app.staticTexts["statistics-note"]
                default: last = app.staticTexts["settings-content-version"]
                }
                try audit(last:last)
            }
        }
    }
}
