# Issue Intake V4 単体候補参照と候補全件検証 設計提案

状態：`human_decision_candidate`

対象：改善候補の仕分け判断を機械可読に置けない行き止まり（問題一覧#8）と、
候補が検証されずに腐る経路（#14）の最小修正。あわせて設計と実装の食い違い（#9）の処置を確定する。

前提記録：`records/development/2026-08-06-encountered-problem-inventory-v1.md`（問題一覧）、
`records/development/2026-08-06-authority-reference-digest-check-triage-decision-v1.md`（Human仕分け判断）

## 1. 結論（推奨）

全面的な作り直しをせず、次の4変更と、設計文書の食い違い5点の処置だけを行う。

1. V4の仕分け判断recordが**単体の候補fileを直接指せる**参照形式を1つ追加する。
2. 既存Test 2件の条件を「bundleを指すものは、既知のbundleを指す」へ狭める。
3. 候補置き場の**全件検証**Testを追加し、歴史recordは機械可読なallowlistで明示宣言する。
4. 2026-08-06のHuman仕分け判断を、新形式でV4レーンへ機械可読に置き直す。

既存の41 decision、3 Issue、候補bundle、bundle指紋を参照する58 file、V1凍結レーンには一切触れない。

## 2. 固定した現在地（すべて2026-08-06に実測）

| 事実 | 値 |
| --- | --- |
| 対象module規模 | `issue_intake_v4.py` 1,212行、`issue_resolution_pilot.py` 1,755行、Test 2 file 1,592行、計4,559行 |
| 対象Test件数 | 47件（`test_issue_intake_v4.py` 38、`test_issue_resolution_pilot.py` 9） |
| bundle指紋`e01c0feb…`を参照するfile | 58件 |
| 候補／V4 decision／V4 Issue | 3件／41件／3件、`in_progress` 0件 |
| 候補のTest検証状況 | 3件中1件のみ（`ic-pilot-todo-growth-001--v1.json`だけ） |
| 「対処するが昇格保留」の表現可能性 | 既存validatorで表現できる。`validate_human_triage_decision`は、昇格しない場合`issue_promotion == {"approved": False, "issue_id": None}`を要求する（`issue_intake_v4.py` 843-847行） |
| 単体候補を指せない原因 | `candidate_ref`のkey集合が`{bundle_path, bundle_sha256, bundle_schema_version, candidate_id, candidate_content_digest}`に厳密固定（同 743-744行付近） |
| 同一bundle強制 | `test_k7_repository_decision_set_has_no_conflict`と`test_l6_repository_issue_set_is_consistent`が全recordに既知bundle SHAを要求 |

固定入力：

| path | SHA-256 |
| --- | --- |
| `records/development/2026-08-06-encountered-problem-inventory-v1.md` | `f6d8da5e6d95767a732e2280ec101df5188d9faac4d55621003c8bb5beb4763b` |
| `records/development/2026-08-06-authority-reference-digest-check-triage-decision-v1.md` | `be9e7d3a2af88a4452a5055d39be8a6e2f77514a5529a134db2086fb49664fb9` |
| `.reviewcompass/workflow/improvement-candidates/ic-authority-reference-digest-check-001--v1.json` | `d4e801aa35e4bd1ad2c17917d0cfd57b60e7e1aec93e7d1259bf8321285824c6` |

## 3. 規範宣言（N1〜N11）

以下が本提案の規範宣言のすべてである。**この節に無い振る舞い変更は本提案の範囲外**とする。

### (a) 単体候補参照

- **N1**：`candidate_ref`は2形式とする。既存のbundle形式（5 key厳密一致、無変更）と、新設の単体形式
  `{record_path, record_sha256, candidate_id, candidate_content_digest}`（4 key厳密一致）。
  key集合で形式を判別し、過不足・混在は拒否する。
- **N2**：単体形式は、fileの実在、実bytesのSHA-256一致、record内`candidate_id`一致、
  record内`content_digest`一致を、すべてfail-closedで検証する。
- **N3**：既存41 decisionのbundle形式は、変更なしで合格し続ける。
- **N4**：decision ID規則（`DEC-<candidate_id>`）、保存path規則、`human_fields`検証、
  昇格整合検査は、既存のまま両形式に適用する。

### (b) 既存Testの条件変更

- **N5**：`test_k7`を「**bundle形式の**decisionはすべて既知bundle（SHA `e01c0feb…`）を指す」へ狭める。
  単体形式は対象外。既存41件の保護は変わらない。
- **N6**：`test_l6`のIssue側も同じ向きへ狭める。将来、単体候補由来のIssueが同じ壁に当たらないため。
  （正式Issue登録そのものは本提案では行わない。）

### (c) 候補置き場の全件検証

- **N7**：`.reviewcompass/workflow/improvement-candidates/`の全JSON recordは、
  対応するconfig版のvalidatorに合格するか、歴史recordとしてallowlistに明示宣言されているかの
  **どちらか**でなければならない。これをTestで固定する。
- **N8**：歴史allowlistは機械可読fileとし、entryごとに理由と後継recordへの参照を持つ。
  初期entryは`ic-historical-todo-issue-intake-001--v1.json`の1件
  （V4成立の起点。`DEC-HISTORICAL-TODO-ISSUE-INTAKE-001`で閉鎖済み。現行のどのvalidatorにも
  合格しないことが実測済み）。
- **N9**：`ic-authority-reference-digest-check-001--v1.json`はv3 validatorで合格し続ける。
- **N11**：候補bundle内41件すべてに有効decisionが存在することをTestで固定する
  （閉鎖Evidenceの「未判断0件」を、以後は機械が維持する）。

### (d) 仕分け判断の機械可読化

- **N10**：`DEC-IC-AUTHORITY-REFERENCE-DIGEST-CHECK-001`（version 1）を
  `triage-decisions-v4/`へ単体形式で作成する。値はMarkdown裁定
  （`DEC-AUTHORITY-REFERENCE-DIGEST-CHECK-001`）の§3の写しとする：
  `disposition: issue_resolution`、`blocking: false`、`promote_to_issue: false`、
  `issue_promotion: {approved: false, issue_id: null}`、`unresolved: true`、`recurrence: true`、
  `impact: medium`、`priority: low`。Markdown裁定は履歴として保持し、上書きしない。

## 4. 設計と実装の食い違い（#9）の処置

旧設計提案`docs/design/2026-08-05-historical-todo-issue-intake-proposal.md`の宣言との食い違いを、
次のとおり確定する。**旧文書はin-placeで書き換えず、本提案の承認をもって処置の正本とする。**

| 対象 | 処置 |
| --- | --- |
| §1.3「未triage候補の滞留を検査する」 | **趣旨を狭く実装**（N7・N8・N11）。ただし「各候補が`triage_decision_ref`を持つ」形は採らない。候補recordは不変であり、後から増える判断を候補側へ書けないためである。判断側から候補を引く現行の向きを正とする設計改定 |
| §2.3 X4「解決済みIssueと同一主題は除外」 | 実装（重複の**疑いを立てて保持**）へ設計を合わせる**改定**。除外は情報を失い、疑い保持は失わないため |
| §3.1／§3.2（一括判断の条件） | **Work 8の手作業Pilot評価へ延期**を明示する。実装しない |
| §4.1経路（`improvement_candidate`経由） | 実装形（bundle直結＋本提案の単体直結）を正式とする**改定**。中間変換recordは作らない |
| GREEN Evidenceの「設計§1.3に従い置き換えた」という記述 | 事実と異なるため、**訂正recordをnew-onlyで作成**（実際の置き換え内容はIssue件数検査であった）。閉鎖Evidenceの「未判断0件」は当時の手作業観測として保持し、以後はN11が機械維持する |

## 5. 宣言→RED対応表の義務（実装開始の関門）

- 実装開始前に、N1〜N11それぞれへREDテストを結んだ**対応表record**を作成する。
- 対応表で「REDの無いN」が**0件**であることを機械で数える。1件でも残れば実装を開始しない。
- これは、旧設計で§1.3が受入条件一覧（I/J項目）から漏れて未実装のまま「完了」とされた失敗
  （問題一覧#9-b）の再発防止である。

## 6. 変更しないもの

候補bundle本体、既存41 decision、既存3 Issue、bundle指紋を参照する58 file、V1凍結レーン
（`triage-decisions`、`issues`）、config v1〜v3、`improvement_candidate`のschema、checklist、
Current Plan、正式Issue登録（保留のまま）、製品schema、UI、automation。

## 7. 危険と緩和

| 危険 | 緩和 |
| --- | --- |
| validator変更により旧合格がstaleになる（開発方針） | 実装後に`validate_triage_decision_repository`と`validate_v4_issue_repository`を全件再実行し、41 decision・3 Issueの合格を再確認する（機械、低費用） |
| Test 2件（k7・l6）の書き換えは「承認済み設計変更」を要する | 本提案のHuman承認をその承認とし、変更理由を本文書とcommitへ記録する |
| 新形式の乱用（何でも単体で指せる） | 保存先は`triage-decisions-v4`のみ、ID規則・実在検証・digest束縛は既存のまま適用（N4） |
| 本作業のPlan上の位置づけが無い | 事実として明示する。Human承認（2026-08-06「推奨案に従おう」）を実施根拠とする |

## 8. Human判断事項

1. N1〜N11の承認。
2. `test_k7`・`test_l6`の条件変更（N5・N6）の承認。既存Testの書き換えにあたる。
3. N10の`impact: medium`・`priority: low`の確認。Markdown裁定に記したとおり、この2値は
   Humanの「対処すべきだが急ぎではない」という文言からClaudeが翻訳した値であり、
   **Humanがこの2語を直接述べたわけではない**。
4. §4の処置5点（改定2、延期1、訂正1、実装3件分）の承認。
5. 非対象（§6）の確認。

## 9. 非対象

正式Issue登録の実行、V1凍結レーンの解除、bundleの変更・再生成、深さ・派生元fieldの追加
（別途判断）、Work 6A残り10項目、Work 8前倒し、外部送信、push。
