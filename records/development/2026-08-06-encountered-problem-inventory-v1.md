# 2026-08-06に発生した問題の全件一覧 v1

- record kind：`encountered_problem_inventory`
- record version：1
- recorded at：`2026-08-06T13:43:31+09:00`（`date -Iseconds`による機械取得値）
- 作成時点のHEAD：`7c0d087d6febcdd9b4ce43d43a83c9ed6dde3b35`（`Stop deep dives before they reach unapproved redesign`）
- 実行環境：Python 3.9.6、pytest 8.4.2、fallback `false`
- 公式全Test（本record作成時に実測）：`1020 passed`（failed 0、errors 0）

## 0. この記録は何のためにあるか

2026-08-06の作業では、本線（Work 6A）の進行と並行して複数の問題が発生した。そのうちいくつかは、
**正式なIssueへ挙げることができない**。改善候補に対するHumanの仕分け判断を機械可読な形で置ける
場所が現在無く（本一覧§2-8）、その原因であるIssue Intake V4設計の欠陥（§2-9）自身も、
同じ理由でIssueにできないからである。

正式レーンへ載せられない問題は、放置すればどこにも記録されないまま失われる。
**本recordは、その消失を防ぐためだけに作った事実の一覧である。**

### この記録の位置づけ

**本recordはIssueではない。Task Contractでもない。正式なWorkflow stateでもない。**

- 何の作業の開始も完了も宣言しない。
- 何のcheckboxも動かさない。
- どの問題も、分類、route、優先度、blocking判定を決めない（§4）。
- 機械が読む前提の形式ではない。Humanが1画面で見渡すための人向け記録である。

正式レーンへ取り込む判断は、すべてHumanが別途行う。

### 事実確認の方法

本recordに書いたcommit SHA、path、test名、件数、SHA-256は、すべて作成時にrepositoryへ対して
機械確認した（§5）。確認できなかったものは「**未確認**」と明記してある。

---

## 1. 未解決の問題だけの再掲（Humanが次に何を判断するか）

全14件のうち、状態が`unresolved`のものだけを再掲する。番号は§2の詳細に対応する。

| # | 未解決の問題 | Humanに求められる判断 |
| --- | --- | --- |
| 8 | 改善候補の仕分け判断を機械可読な形で置ける場所が無い。旧レーンは2 testで1件に凍結、V4レーンは固定bundle参照しか受け付けない | 置き場所を直すか、代替形式（`records/development/`のDecision record）を正式手順として認めるか |
| 9 | Issue Intake V4設計の欠陥8点（受入条件の漏れ、設計に根拠の無いbundle参照形、実装の逸脱、検査の不在） | 設計やり直しの範囲と着手可否。既存41 decision、3 Issue、閉鎖Evidenceの扱いを含む |
| 10 | 「1件限定の契約に2件目をぶつけて初めて気づく」失敗が**3回**起きている（2026-08-05に2回、2026-08-06に1回） | 同型の凍結が他に無いかを調べるか、凍結を機械可読に宣言する仕組みを作るか |
| 11 | 深掘りの停止規則は`AGENTS.md`へ追記したが、機械では守らせられない | 改善候補recordへ「発見の深さ」「派生元」を持たせる案を、設計やり直しの範囲へ含めるか |
| 12 | 共有workspaceでの並行session作業について、合意がどこにも記録されていない | 並行作業の合意を記録するか、branch分離などの運用を決めるか |
| 13 | `TODO_NEXT_SESSION.md`がHEADに追随していない（全Test件数`1017`は実測`1020`と不一致、「次に行う一作業」は既に裁定済み） | TODOの更新をどの作業単位の完了条件に含めるか |
| 14 | `.reviewcompass/workflow/improvement-candidates/`の改善候補record 3件のうち、Testで検証されているのは1件だけである | 残り2件を検証対象へ入れるか、改善候補の検証範囲を宣言するか |

`resolved`（7件：#1、#3、#4、#5、#7、および#2・#6の一部）と`recorded_only`は、この表に含めない。

---

## 2. 全件の詳細

### 2-1. checklist front matterの参照Digest drift

| 項目 | 内容 |
| --- | --- |
| 何が起きたか | `docs/development/2026-08-03-initial-development-checklist.md`のfront matterで、参照Digest **2件**が実fileのbytesと食い違っていた。`authority_order[2].sha256`（`docs/current/reviewcompass3-plan-current.md`、記載`0ab828f4…9bf2694`／実値`1a735976…d0962f`）と`operational_policy.sha256`（`docs/development/2026-08-02-development-policy.md`、記載`9078276d…f739a0`／実値`0d348803…f8ac18`）。commit `e732995`で修復した。当該欄が最後に更新されたのは2026-08-04の`c475bec`であり、そこから測定commit `21e3d821b398e3b101f296f4f702e620a151e624`までにCurrent Planは7 commit、Development Policyは3 commit改定されたが、参照欄に触れたcommitは修復の1件だけであった |
| 発見の経緯 | Claude開発継続引き継ぎ後の照合報告の副産物。**深さ1** |
| 現在の状態 | `resolved` |
| 記録先 | `records/development/2026-08-06-checklist-authority-reference-digest-repair-evidence-v1.md`（SHA-256 `b7b280e7c61b193f6ed19f798279fc19a0942e8daa7a99ee7dcaf5549420c373`）／観測record `records/development/2026-08-06-authority-reference-digest-drift-observation-v1.json`（SHA-256 `6ccf3d15c28c56a5b74730a9ac056ef3abe13967da0427549e05308cc0ab3841`） |
| 次に必要なこと | なし |
| 正式Issueへ挙げられるか | 挙げる必要が無い（修復済み）。再発防止は#2として改善候補になっている |

### 2-2. 恒久的な参照Digest検査器が存在しない

| 項目 | 内容 |
| --- | --- |
| 何が起きたか | front matterのYAMLを解析して記載Digestを参照先の現行bytesと突き合わせる恒久的な検査器が、repository内に存在しない。`tools/`配下にfront matter YAML parserは無い。類似の照合は`tools/development/todo_record_generation.py`（SHA-256 `f5ae4328b211b0d140856a5e29663673f604ba69623b65c13848e432896e37ea`）にあるが、対象は`TODO_NEXT_SESSION.md`の`## 最新のauthority／Evidence`節に限られる（測定commitで参照8件・不一致0件） |
| 発見の経緯 | #1の原因調査。**深さ2** |
| 現在の状態 | `recorded_only`（改善候補として記録済み。実装は未着手であり、Humanが「対処すべきだが急ぎではない」と裁定した） |
| 記録先 | 改善候補`IC-AUTHORITY-REFERENCE-DIGEST-CHECK-001`：`.reviewcompass/workflow/improvement-candidates/ic-authority-reference-digest-check-001--v1.json`（SHA-256 `d4e801aa35e4bd1ad2c17917d0cfd57b60e7e1aec93e7d1259bf8321285824c6`、`content_digest` `760d9ef9811e6d95c9af406a6664e0e2ef5df9c33e32aa6ebbc33721c931753f`）／仕分け判断`DEC-AUTHORITY-REFERENCE-DIGEST-CHECK-001`：`records/development/2026-08-06-authority-reference-digest-check-triage-decision-v1.md`（SHA-256 `be9e7d3a2af88a4452a5055d39be8a6e2f77514a5529a134db2086fb49664fb9`、本record作成時点で**未追跡**） |
| 次に必要なこと | 検査器を作る前に「どのfront matter keyが現在有効を意味するか」の判別規則（対象keyのallowlist）を機械可読に宣言し、その宣言自体のHuman承認を得ること。ただし仕分け判断は「正式Issue登録は経路が直るまで保留」としており、経路の問題（#8）が先行する |
| 正式Issueへ挙げられるか | **挙げられない**。理由は#8。仕分け判断を機械可読な形で置ける場所が無いため、Issue昇格を保留した |

### 2-3. 手編集sourceの拒否対象が1件限定であることに上位文書の根拠が無かった

| 項目 | 内容 |
| --- | --- |
| 何が起きたか | Current Work Projectionの固定入力から拒否する対象が`TODO_NEXT_SESSION.md`の1件だけに限定されていた。この限定はRED test `tests/test_work6a_current_work_projection_negative.py::test_hand_editable_handoff_is_not_accepted_as_authority`で初めて具体化されたものであり、上位文書（Current Plan、checklist、案Aの提案とDecision、`AGENTS.md`、TODO更新手順）へ遡れない。上位文書が「手編集する正本を作らない」対象として名指ししているのは`STATUS.md`であり、`TODO_NEXT_SESSION.md`というfile名は上位文書のどこにも現れない。`DEC-WORK6A-PROJECTION-NON-AUTHORITY-SCOPE-001`で拒否対象を**4件**の限定列挙へ拡大した。実装`tools/development/session_log_bootstrap.py`（SHA-256 `b97bd5eec6f6ae4fedd7a719089a8af0f642ddfb59e6ee4e29f851993db02a97`）529-534行の`_NON_AUTHORITY_FIXED_INPUT_IDENTITIES`に4件（`TODO_NEXT_SESSION.md`、`STATUS.md`、`docs/development/templates/TODO_NEXT_SESSION.template.md`、`docs/development/2026-08-03-initial-development-checklist.md`）を確認した。あわせて判定語彙を「手編集できるか」から「現在位置のauthorityとして宣言されていない成果物か」へ改めた |
| 発見の経緯 | 本線（Work 6A）に対するHumanの追跡指示。**深さ1** |
| 現在の状態 | `resolved` |
| 記録先 | `records/development/2026-08-06-work6a-non-authority-input-scope-decision-v1.md`（SHA-256 `2991aed38dd7e6f294774baa0ff98d664168bd8f2fffdc3337e7228938109af8`）／GREEN Evidence `records/development/2026-08-06-work6a-non-authority-input-green-evidence-v1.md`（SHA-256 `79c5783c6f759c631aeabc41916fcc93f914984e2278ab1acb29589e1119a5ac`）。commitは`a2a90a7`（RED）と`7055ed9`（GREEN） |
| 次に必要なこと | なし。ただし「入力側にauthorityを宣言させる方式」は同Decision §3で非承認範囲として明示的に残されている |
| 正式Issueへ挙げられるか | 挙げる必要が無い（Human承認済みのDecisionで解決） |

### 2-4. RED Evidence §8-2の事実誤り

| 項目 | 内容 |
| --- | --- |
| 何が起きたか | `records/development/2026-08-06-work6a-projection-negative-red-evidence-v1.md`の§8-2（当該fileの196-201行）が、素朴な一般化で壊れる既存testとして`test_projection_renders_fixed_short_and_detailed_text`を挙げていた。このtestは`project_current_work()`を呼ばないため壊れない。実測（pytest pluginで素朴版を実行時に差し込む方法、`7 failed, 1010 passed`）で実際に壊れる既存testは**6件**であった（`tests/test_session_bootstrap_e2e.py`の2件、`tests/test_session_log_bootstrap.py`の2件、`tests/test_session_log_completed_next.py`の2件）。7件目の失敗は同時に追加した境界例`test_plan_authority_markdown_is_still_accepted`である |
| 発見の経緯 | #3の追跡調査の中で、RED Evidenceの根拠を自分で再確認した際。**深さ2** |
| 現在の状態 | `resolved` |
| 記録先 | `records/development/2026-08-06-work6a-evidence-correction-v1.md`（SHA-256 `219eefc14dcda02d4ea72e70682bcaf0fe9ea98d752cb25aacc79dcee64871b7`）。旧記録`records/development/2026-08-06-work6a-projection-negative-red-evidence-v1.md`（SHA-256 `8dcff9e7f08a2098c6be6175cd940291f8f93a99903691dd0b94542671896d20`）はin-placeで書き換えず、new-onlyで訂正した |
| 次に必要なこと | なし。結論（Plan authority自身が拒否されて既存Testが壊れる）は変わらず、下流のDecisionと実装への影響も無しと評価済み |
| 正式Issueへ挙げられるか | 挙げる必要が無い（訂正record済み） |

### 2-5. 対応inventoryの`recorded_at`が機械計測でない値だった

| 項目 | 内容 |
| --- | --- |
| 何が起きたか | `records/development/2026-08-06-work6a-negative-path-test-inventory-v1.json`の`recorded_at`に、機械計測でない未来時刻が書かれていた。レビューで差し戻し、機械取得値へ訂正した。現行値は`2026-08-06T08:53:06+0900`であり、fileはこの訂正後の状態で1度だけcommitされた（`9a39365`、2026-08-06T08:55:20+09:00）。現行file SHA-256は`51674c143858b37608c7914c5bc2a8973be8221e2d5bde9707d89d082f995a16` |
| 発見の経緯 | 本線（Work 6A）成果物のレビュー。**深さ1** |
| 現在の状態 | `resolved` |
| 記録先 | **本recordが初出。** 訂正の経緯を記録した専用recordは存在しない。訂正前の捏造値そのものはcommit前に置き換えられたためrepositoryへ残っておらず、**機械確認できない（未確認）** |
| 次に必要なこと | なし |
| 正式Issueへ挙げられるか | 挙げる必要が無い（訂正済み）。ただし「時刻を機械取得する」規律に対する機械検査は無く、#9の「宣言はあるが検査が無い」型（§3-2）に属する |

### 2-6. Claudeの推奨誤り（既存testに触らずに済むという説明）

| 項目 | 内容 |
| --- | --- |
| 何が起きたか | Claudeが「新しいbundleを作れば既存testに触らずに済む」と説明したが、実際には`tests/test_issue_intake_v4.py`の`test_k7_repository_decision_set_has_no_conflict`（789行）と`test_l6_repository_issue_set_is_consistent`（1130行）が壊れる。両testはいずれも`assert …["candidate_ref"]["bundle_sha256"] == BUNDLE_SHA`により、全decision／全Issueが**同一bundle**を指すことを要求しているためである。会話中に訂正した |
| 発見の経緯 | #8の解決策検討の中で、自分の推奨をtestに対して再確認した際。**深さ3** |
| 現在の状態 | `resolved`（誤りは訂正済み）。ただし経緯は`recorded_only`ですらない（下記） |
| 記録先 | **推奨誤りの経緯そのものは本recordが初出。** `test_k7`と`test_l6`が壊れるという**事実だけ**は`records/development/2026-08-06-frozen-lane-guidance-correction-decision-v1.md`（SHA-256 `9c0b58bdfc868e03d9d4a3dd05c179157ec05324c88bffdc9a51a12fce2e8994`）§5に「schema変更と既存Test（`test_k7`、`test_l6`）の改定を伴う」として残っている。誤って推奨し、後から訂正したという経緯はどのrecordにも無い |
| 次に必要なこと | なし |
| 正式Issueへ挙げられるか | 会話中の誤りであり、Issueの対象になる成果物の欠陥ではない |

### 2-7. `AGENTS.md`が凍結レーンへ案内する行き止まりだった

| 項目 | 内容 |
| --- | --- |
| 何が起きたか | `DEC-IMPROVEMENT-CANDIDATE-LANE-GUIDANCE-001`（commit `b8ccc1a`）で`AGENTS.md`へ追記した改善候補の登録手順が、検証までしか書いておらず、Humanの仕分け判断をどこへ記録するかを示していなかった。その先の旧Pilotレーンは各1件で凍結されており、追記した手順は凍結レーンへ案内する行き止まりになっていた。実際に`IC-AUTHORITY-REFERENCE-DIGEST-CHECK-001`の仕分け判断を記録しようとして停止した。`DEC-FROZEN-LANE-GUIDANCE-CORRECTION-001`で訂正し、再発防止Test `tests/test_agents_lane_guidance.py`（SHA-256 `2916ba1ae0bcfdffffefc6248c239324e11271227fa4411b7eba788b03071000`、3 test）をRED先行で追加した。RED時点`1 failed, 1019 passed`、訂正後`1020 passed` |
| 発見の経緯 | #2の改善候補を登録した直後、仕分け判断を記録しようとして。**深さ4** |
| 現在の状態 | `resolved`（案内の行き止まりは解消）。ただし案内先が凍結されているという根本（#8）は未解決 |
| 記録先 | `records/development/2026-08-06-frozen-lane-guidance-correction-decision-v1.md`（SHA-256 `9c0b58bdfc868e03d9d4a3dd05c179157ec05324c88bffdc9a51a12fce2e8994`）／訂正対象`records/development/2026-08-06-improvement-candidate-lane-guidance-decision-v1.md`（SHA-256 `3603549405c8f4962410fa4c4d301a94fac6b79fea1b16f9f2f41b3f79b265af`）。commitは`ff20380`（RED）と`4c54f1d`（GREEN） |
| 次に必要なこと | なし（#8へ引き継ぐ） |
| 正式Issueへ挙げられるか | 挙げる必要が無い（Human承認済みのDecisionとTestで解決） |

### 2-8. 改善候補の仕分け判断を機械可読な形で置けない

| 項目 | 内容 |
| --- | --- |
| 何が起きたか | 改善候補に対するHumanの仕分け判断を、機械可読なrecordとして置ける場所が無い。旧V1レーン`.reviewcompass/workflow/triage-decisions`は`tests/test_issue_resolution_pilot.py::test_repository_contains_only_the_single_valid_pilot_subject`が`assert len(decision_files) <= 1`（191行）を、`tests/test_issue_intake_v4.py::test_k6_legacy_v1_decision_and_pilot_validation_keep_passing`がfile名の完全一致（`["dec-pilot-todo-growth-001--v1.json"]`、784-786行）を要求しており、**2 testで1件に凍結**されている。V4レーン`.reviewcompass/workflow/triage-decisions-v4`は`candidate_ref`のkey集合が`bundle_path`／`bundle_sha256`／`bundle_schema_version`／`candidate_id`／`candidate_content_digest`の5keyに厳密固定（`tools/development/issue_intake_v4.py` 764-769行）されており、単体候補recordを指す形が無い。さらに`test_k7`が全decisionの同一bundle参照を要求する |
| 発見の経緯 | #7の原因調査。**深さ4**（#2 → #3的な登録入口 → #7 → 本件） |
| 現在の状態 | **`unresolved`** |
| 記録先 | `records/development/2026-08-06-frozen-lane-guidance-correction-decision-v1.md`（SHA-256 `9c0b58bdfc868e03d9d4a3dd05c179157ec05324c88bffdc9a51a12fce2e8994`）§5「V4の置き場所が単体候補を直接参照できるようにする変更」として非承認範囲に記載。回避策として`records/development/2026-08-06-authority-reference-digest-check-triage-decision-v1.md`（SHA-256 `be9e7d3a2af88a4452a5055d39be8a6e2f77514a5529a134db2086fb49664fb9`、**未追跡**）が「正規の手順ではなく、正規の置き場所が使えないための代替である」と明示したうえで仕分け判断を人向けMarkdownで残している |
| 次に必要なこと | Humanが次のいずれかを判断する。(a) V4 `candidate_ref`を単体候補も指せる形へ拡張する（schema変更と`test_k7`／`test_l6`の改定を伴う）。(b) `records/development/`のDecision recordを正式手順として認め、その形式と検査を定める。(c) Issue Intake設計のやり直し（#9）の中で扱う |
| 正式Issueへ挙げられるか | **挙げられない**。Issue昇格には仕分け判断recordが要り、その仕分け判断を置けないことが本件そのものである（循環） |

### 2-9. Issue Intake V4設計の欠陥（8点）

対象設計：`docs/design/2026-08-05-historical-todo-issue-intake-proposal.md`（SHA-256 `8475cd94b449e0709eb97e6d487b86cceef86e0307b3bbb7e78351d8f43147a9`）
対象実装：`tools/development/issue_intake_v4.py`（SHA-256 `7a1d557e82acd6554c3e137345f02ba476cbf448184a9a0348dca6beec26e27a`）
対象config：`config/development-issue-resolution-pilot-v4.json`（SHA-256 `ed274e487318d44baed701ffbc8a1130df3e9d81cadca96515848a2bea228a8e`）

| # | 欠陥 | 機械確認した内容 |
| --- | --- | --- |
| 9-a | 設計§1.3「候補の総数ではなく**未triageの候補が滞留していないか**を検査対象にする」が、実装にもtestにも無い | `untriaged`の出現は`config/development-issue-resolution-pilot-v4.json` 147行（Issue状態語彙の一要素）と`tests/test_issue_intake_v4.py` 107行（Issue状態のfixture）の2箇所だけで、いずれも**候補**の滞留検査ではない |
| 9-b | 設計§5のTDD受入条件一覧（I1〜I9、J1〜J16の計25件）に、§1.3の受入条件が1件も載っていない | §5全体を読み、候補の未triage滞留を要求する項目が無いことを確認した |
| 9-c | §2.3のX4は「既存の解決済みIssue（`ISSUE-PILOT-TODO-GROWTH-001`）と同一主題である」候補を**除外する**と宣言しているが、実装は除外しない | `_excluded_rule()`（`issue_intake_v4.py` 408-430行）が返すのは`X1`／`X2`／`X3`／`X5`だけで、`X4`を返す枝が無い。`build_intake_candidate()`が書き込む`applied_rules`も`["X1:pass", "X2:pass", "X3:pass", "X5:pass"]`の固定4件で、X4を含まない。同一主題の扱いは`evaluate_duplicate_suspect()`（474行）の**「重複疑い」**に化けている。X4という文字列は`config/development-issue-resolution-pilot-v4.json` 50行に規則文としてのみ残っている |
| 9-d | 設計§3.1（一括判断してよい条件）と§3.2（一件ずつ判断が必要な条件）が、実装にもtestにも無い | `tools/`と`tests/`の全体に一括判断（bulk／batch）の実装は無い。`tools/extraction/stage_two_completion.py`の「一括」は無関係の別機能である |
| 9-e | 設計§4.1の経路`candidate → improvement_candidate → human_triage_decision → issue_record`から実装が逸脱し、`improvement_candidate`段を通らずbundle直結になった | `build_human_triage_decision()`（`issue_intake_v4.py` 657-708行）は`bundle_path`と`candidate_id`から直接`candidate_ref`を組み立てる。`improvement_candidate`という語はconfigのdirectory定義（19行）にあるだけで、V4のdecision経路には現れない |
| 9-f | bundle参照形は設計文書に根拠が無く、実装指示書で初めて導入された | 設計文書中の文字列`bundle`の出現回数は**0**である。`candidate_ref`をbundle参照として定義した最初の追跡可能な文書は`records/session-handoffs/2026-08-05-codex-to-claude-v4-human-triage-persistence.md`（SHA-256 `65b7f6601540b1b068c5bdcc29ccfcc4917732705f182a676a62e818e79dfcbc`、commit `0a5411c`、2026-08-05T12:37:24+09:00）の41-45行である |
| 9-g | GREEN Evidenceが「設計§1.3に従い置き換えた」と主張しているが、置き換え後の検査は§1.3の内容ではない | `records/development/2026-08-05-issue-intake-v4-green-evidence-v1.md`（SHA-256 `28809b220e8e5b16f3f643c8994ea9bdeb73ac83d3e506daaea6baceb751e75f`）47行が「設計§1.3に従い」と書くが、49-51行に挙げた置換後の検査は「Issue recordがちょうど1件」「v2規約の候補が引き続きv2 configで検証を通る」であり、§1.3が求める「未triage候補の滞留検査」ではない。現行の`tests/test_issue_resolution_pilot.py` 188行は`assert len(issue_files) == 1`である |
| 9-h | 閉鎖Evidenceの「未判断0件」を維持する機械検査が無い | `records/development/2026-08-05-historical-todo-issue-intake-v4-closure-evidence-v1.md`（SHA-256 `b942a9d17ea4c2818c6adb5f3ceabc0063f9b447c7ddb88ccc5baf3d1302d60e`）37-40行が「有効decision 41件、未判断0件」と述べるが、`test_k7`（789-806行）が確認するのは有効decisionどうしの整合と件数一致だけで、**bundleの41候補すべてにdecisionがあること**は検査していない |

| 項目 | 内容 |
| --- | --- |
| 発見の経緯 | #8の原因調査。**深さ5** |
| 現在の状態 | **`unresolved`（8点すべて）** |
| 記録先 | **本recordが初出。** 関連する言及として`records/development/2026-08-06-deep-dive-stop-rule-decision-v1.md`（SHA-256 `b28e5b2de79f6ccb6df413f4ecc33c64fc29ab55f7f44f944460bba1e4c82401`）21-22行が「Issue Intake V4の設計自身に、受入条件一覧の漏れと、設計に根拠のないbundle参照形が見つかった」と1文で触れているだけで、8点の内訳はどこにも無い |
| 次に必要なこと | Humanが設計やり直しの範囲を確定する。既存41 decision、3 Issue、承認・閉鎖Evidenceの扱いを含む。同Decision §4はこの範囲確定が未了であることを明記している |
| 正式Issueへ挙げられるか | **挙げられない**。Issue登録経路そのもの（#8）が本件の欠陥に起因しており、この設計の欠陥をこの設計の作ったレーンへ登録することができない |

### 2-10. 「1件限定の契約に2件目をぶつけて初めて気づく」失敗が3回起きている

| 項目 | 内容 |
| --- | --- |
| 何が起きたか | 同型の失敗が**3回**発生している。**1回目**：2026-08-05T11:18（commit `10fc356`）に改善候補の2件目`ic-historical-todo-issue-intake-001--v1.json`を置いたことで、`tests/test_issue_resolution_pilot.py::test_repository_contains_only_the_single_valid_pilot_subject`の「候補file数が1件」検査が成立しなくなり、commit `c7f3712`（11:53）で検査対象を置き換えた。**2回目**：2026-08-05にV4 Issueの2件目`ISSUE-HTC-C9F6C917`を登録した際、`tests/test_issue_intake_v4.py::test_l6_repository_issue_set_is_consistent`の1件決め打ちが落ちた。commit `b6ac2c8`（13:50）で一般則へ直した。**3回目**：2026-08-06、仕分け判断の2件目を置こうとして#8で停止した。1回目・2回目の対処はいずれも当該レーン内の1 testを直しただけで、他に同型の凍結が無いかを調べていない |
| 発見の経緯 | 3回目（#8）の原因調査で、過去に同型が起きていたことに気づいた。**深さ5** |
| 現在の状態 | **`unresolved`**（3回目が未解決であり、同型の探索も未実施） |
| 記録先 | 1回目：`records/development/2026-08-05-issue-intake-v4-green-evidence-v1.md`（SHA-256 `28809b220e8e5b16f3f643c8994ea9bdeb73ac83d3e506daaea6baceb751e75f`）44-54行。2回目：`records/session-handoffs/2026-08-05-codex-to-claude-repair-v4-issue-set-test-and-commit.md`（SHA-256 `1cd51ef060e7db3f25c514f88dbcc7dd34202fca160dee9d642104a71930472d`、commit `4939fa3`）。3回目：#8を参照。**3回が同型であるという認識は本recordが初出** |
| 次に必要なこと | 「1件」「完全一致」を要求する既存assertを横断的に洗い出し、意図的な凍結と暫定の決め打ちを区別すること。凍結の宣言を機械可読にする案（`DEC-FROZEN-LANE-GUIDANCE-CORRECTION-001` §5の③）は非承認範囲として保留されている |
| 正式Issueへ挙げられるか | **挙げられない**。#8と同じ理由 |

### 2-11. 深掘りによる隘路

| 項目 | 内容 |
| --- | --- |
| 何が起きたか | 本線（Work 6A）の副産物から4段の連鎖で、未承認の設計変更が必要な地点へ到達して動けなくなった。連鎖は深さ1＝参照Digest drift（`e732995`）、深さ2＝恒久検査器の不在と改善候補作成（`235a7d3`）、深さ3＝候補1件を登録する入口が無く`AGENTS.md`へ追記（`b8ccc1a`）、深さ4＝その手順が凍結レーンへ案内する行き止まり（`ff20380`、`4c54f1d`）である。`DEC-DEEP-DIVE-STOP-RULE-001`で`AGENTS.md`へ「深掘りの停止規則」節を追記した（`AGENTS.md` SHA-256 `30704aad10b316b3a2ec2456d6878b4a8ecbfbf589bbddf9e8f0f7461b0b8741`、commit `7c0d087`） |
| 発見の経緯 | 深さ4で停止したこと自体をHumanが問題として指摘した。**深さ4の観測** |
| 現在の状態 | **`unresolved`**（規則は追記済みだが、機械では守らせられない） |
| 記録先 | `records/development/2026-08-06-deep-dive-stop-rule-decision-v1.md`（SHA-256 `b28e5b2de79f6ccb6df413f4ecc33c64fc29ab55f7f44f944460bba1e4c82401`）。§3が「本規則は判断の規則であり、機械では守らせられない」と限界を明記している |
| 次に必要なこと | 機械化しうる部分として、改善候補recordへ「発見の深さ」と「派生元」を持たせる案がある。この案をIssue Intake設計やり直し（#9）の範囲へ含めるかは同Decisionで決まっていない。Humanの判断が要る |
| 正式Issueへ挙げられるか | **挙げられない**。機械化案は改善候補recordのschema変更を伴い、#8・#9と同じ経路の問題に突き当たる |

### 2-12. 並行sessionによるcommit

| 項目 | 内容 |
| --- | --- |
| 何が起きたか | 本線の作業中に、Codex側の別sessionが同じbranch `main`へ`af33340`（2026-08-06T09:16:19、3 file追加）と`5ab8668`（09:26:45、2 file追加）をcommitした。両commitが触れたのはsession transcript関連の5 fileであり、同時間帯のWork 6A commit（`9a39365`、`a2a90a7`、`7055ed9`）が触れたfileとは**1件も重複していない**（機械確認済み）。実害は生じていない。さらに本record作成の直前（2026-08-06T13:33:25）にも、同じworkspaceへ未追跡fileが1件現れている（`records/development/2026-08-06-authority-reference-digest-check-triage-decision-v1.md`） |
| 発見の経緯 | `DEC-WORK6A-PROJECTION-NON-AUTHORITY-SCOPE-001` §5でGit状態を固定する際に気づいた。**深さ1**（本線のEvidence固定の副産物） |
| 現在の状態 | **`unresolved`**（file重複が無かったことは確認したが、並行作業の合意そのものは未記録） |
| 記録先 | `records/development/2026-08-06-work6a-non-authority-input-scope-decision-v1.md`（SHA-256 `2991aed38dd7e6f294774baa0ff98d664168bd8f2fffdc3337e7228938109af8`）§5に「なお`af33340`と`5ab8668`は並行する別session（Codex）のcommitであり、本Decisionの対象範囲とはfileが重ならない」という1文がある。**共有workspaceでの並行作業をどう扱うかの合意は、どのrecordにも無い（本recordが初出）** |
| 次に必要なこと | 同一branchでの並行session作業を許すのか、許すなら衝突をどう検出するのかをHumanが決めること。現状は「たまたまfileが重ならなかった」だけである |
| 正式Issueへ挙げられるか | **挙げられない**。#8と同じ理由（仕分け判断を置けない） |

### 2-13. `TODO_NEXT_SESSION.md`がHEADに追随していない

| 項目 | 内容 |
| --- | --- |
| 何が起きたか | `TODO_NEXT_SESSION.md`（SHA-256 `8fc3f77a4097ad3c5f109188ee82d9e3715dea8aebf947ba1f36644946bc408e`）を最後に更新したcommitは`235a7d3`（2026-08-06T10:13:11）である。その後の4 commit（`b8ccc1a`、`ff20380`、`4c54f1d`、`7c0d087`）はTODOを更新していない。結果として次のずれがある。(a) 61行「直近の全Test：venv公式runner **1017 passed**」に対し、本record作成時の実測は**1020 passed**である。(b) 30行「次に行う一作業：Humanが改善候補IC-AUTHORITY-REFERENCE-DIGEST-CHECK-001のtriageを裁定する」は、13:33:25の`DEC-AUTHORITY-REFERENCE-DIGEST-CHECK-001`で既に裁定されている。(c) 10行「現在作業」に`AGENTS.md`の2件の訂正・追記作業が反映されていない。なお17-26行のEvidence節の参照Digest8件は**すべて現行bytesと一致**しており（機械確認済み）、`tools/development/todo_record_generation.py`の照合（`14 passed`）も通る。**照合が届いていない節だけがずれている** |
| 発見の経緯 | 本record作成のための事実確認。**深さ1**（本一覧作成の副産物） |
| 現在の状態 | **`unresolved`** |
| 記録先 | **本recordが初出** |
| 次に必要なこと | TODOの更新をどの作業単位の完了条件に含めるかをHumanが決めること。あわせて、Evidence節以外（現在位置、次に行う一作業、Test件数）に機械照合が無いことをどう扱うかを決めること |
| 正式Issueへ挙げられるか | **挙げられない**。#8と同じ理由 |

### 2-14. 改善候補record 3件のうち2件がどのTestでも検証されていない

| 項目 | 内容 |
| --- | --- |
| 何が起きたか | `.reviewcompass/workflow/improvement-candidates/`には改善候補recordが3件ある。`.reviewcompass/workflow/improvement-candidates/ic-pilot-todo-growth-001--v1.json`、`.reviewcompass/workflow/improvement-candidates/ic-historical-todo-issue-intake-001--v1.json`（SHA-256 `ec6e702fec5804e736306d66be084e10f9dffb0f7e4bcf573f75304ee57d0206`）、`.reviewcompass/workflow/improvement-candidates/ic-authority-reference-digest-check-001--v1.json`（SHA-256 `d4e801aa35e4bd1ad2c17917d0cfd57b60e7e1aec93e7d1259bf8321285824c6`）である。しかしTestが実際にvalidatorへ通しているのは`CANDIDATE_PATH`＝`ic-pilot-todo-growth-001--v1.json`の1件だけである（`tests/test_issue_resolution_pilot.py`、SHA-256 `68dc59f650a7e3b2cf13775f2a56499751199383232a01938f9049f8f8f56c34`、174行でglobして189行で`assert CANDIDATE_PATH in candidate_files`、192-196行でCANDIDATE_PATHのみを`validate_record_file`へ渡す）。198-203行のloopは候補ではなくdecision fileを対象にしている。残り2件は、内容が壊れてもTestでは検出されない |
| 発見の経緯 | #8・#10の調査で凍結testを読んだ際の副産物。**深さ5** |
| 現在の状態 | **`unresolved`** |
| 記録先 | **本recordが初出** |
| 次に必要なこと | 全候補を検証対象にするか、検証対象の範囲を宣言するかをHumanが決めること。なお`ic-authority-reference-digest-check-001--v1.json`の`content_digest`は本record作成時に手作業で再計算し、記載値`760d9ef9811e6d95c9af406a6664e0e2ef5df9c33e32aa6ebbc33721c931753f`と一致することを確認した（Testによる確認ではない） |
| 正式Issueへ挙げられるか | **挙げられない**。#8と同じ理由 |

---

## 3. 同じ根から出ている問題のグループ分け

以下は**原因の型による束ね方の提示**であり、分類でも優先度でもない（§4）。1件が複数の型に属することがある。

### 3-1. 型A：現行か歴史かが機械可読でない

「いま有効なもの」と「過去に固定したもの」を機械が区別できず、区別が人の頭とcommit messageとtestのassertに散らばっている。

| # | この型に属する理由 |
| --- | --- |
| 1 | 「現在有効な上位文書」を指す欄が、上位文書の改定に追随したかどうかを機械が知らない |
| 2 | 同一pathが「現在値」と「生成時点pin」の2つの意味で現れるため、key名以外に判別子が無い（改善候補の`proposed_action`が明示） |
| 7 | 旧Pilotレーンが凍結されていることがどこにも宣言されておらず、`AGENTS.md`が死んだ経路を指した |
| 8 | 凍結が設定にも置き場所にも表示されず、commit message・設計提案の本文・testのassertに散在している |
| 10 | 「1件」という決め打ちが、意図的な凍結なのか暫定なのかを機械が区別できない |
| 13 | TODOのどの節が機械管理でどの節が手編集かの境界が、照合の有無としてしか現れない |

### 3-2. 型B：宣言はあるが検査が無い

文書やEvidenceが「こうする」「こうなっている」と述べているのに、それを維持する機械検査が存在しない。

| # | この型に属する理由 |
| --- | --- |
| 2 | 参照Digestを突き合わせる恒久検査器が無い |
| 5 | 「時刻は機械取得する」という規律に対する機械検査が無く、レビューでしか捕まらなかった |
| 9-a | 設計§1.3の宣言に対応する実装もtestも無い |
| 9-b | 受入条件一覧そのものに§1.3が載っておらず、漏れが構造的に検出されない |
| 9-c | configがX4を規則として宣言しているのに、実装がX4を適用しない |
| 9-d | 設計§3.1／§3.2の宣言に対応する実装もtestも無い |
| 9-g | GREEN Evidenceの「設計§1.3に従い」という主張が、実際の検査内容と照合されていない |
| 9-h | 閉鎖Evidenceの「未判断0件」を維持する検査が無い |
| 11 | 深掘りの停止規則を`AGENTS.md`へ宣言したが、機械では守らせられない（Decision §3が自認） |
| 13 | TODOのEvidence節だけに照合があり、現在位置・次の一作業・Test件数には無い |
| 14 | 改善候補recordの検証範囲が宣言されておらず、3件中1件しか検証されていない |

### 3-3. 型C：1件限定の契約に2件目をぶつけて初めて気づく

「1件しか無い」ことを前提に書かれた検査や形式が、2件目を置こうとした瞬間に破れる。破れるまで問題が見えない。

| # | この型に属する理由 |
| --- | --- |
| 3 | 拒否対象が1件（`TODO_NEXT_SESSION.md`）に限定されており、根拠を問われて初めて上位文書に遡れないと分かった |
| 6 | 「新しいbundleを作れば済む」という推奨が、全decisionの同一bundle参照という1件限定の契約に当たった |
| 8 | 旧レーンの`<= 1`とfile名完全一致、V4の同一bundle固定の両方が、2件目で破れる |
| 9-e／9-f | 設計に無いbundle参照形が、「候補は1つのbundleに入っている」という当時の状況を前提に導入された |
| 10 | 3回とも「2件目を置こうとして初めて気づいた」形である |

### 3-4. どの型にも収まらないもの

| # | 備考 |
| --- | --- |
| 4 | Evidenceの事実誤り。人が根拠を再確認して見つけた。型A〜Cのいずれの構造でもない |
| 12 | 共有workspaceでの並行作業。上記3型とは別の、運用合意の不在に属する |

---

## 4. 本recordが記録していないこと

本recordは**事実だけを記録する**。次はいずれも記録しておらず、Humanの判断に属する。

- 各問題の**分類**（`process_improvement`、`test_or_oracle`、`implementation`などの割当て）。
- 各問題の**route**（`issue_resolution`、`checkpoint`、`defer`、`reject`などの処置）。
- 各問題の**優先度**と**blocking判定**。
- 各問題の**正式Issueへの昇格可否**（§2の「正式Issueへ挙げられるか」欄は、**現在の経路上で技術的に登録できるかどうか**の事実であり、昇格すべきかどうかの判断ではない）。
- 問題どうしの**依存関係**や着手順序。§3のグループ分けは原因の型による束ね方の提示であって、作業単位の提案ではない。
- 未解決問題の**解決方針**。§2の「次に必要なこと」は、Humanが判断するために何が要るかを書いたものであり、解決案の推奨ではない。

## 5. 検証

本record作成時に機械確認した内容である。

| 検証項目 | 結果 |
| --- | --- |
| 引用したcommit SHAの実在（`e732995`、`235a7d3`、`b8ccc1a`、`ff20380`、`4c54f1d`、`7c0d087`、`a2a90a7`、`7055ed9`、`9a39365`、`af33340`、`5ab8668`、`c475bec`、`21e3d821`、`10fc356`、`c7f3712`、`b6ac2c8`、`4939fa3`、`0a5411c`） | 全18件が`git log`で解決可能 |
| 引用したtest名の実在（`test_k7_repository_decision_set_has_no_conflict`、`test_l6_repository_issue_set_is_consistent`、`test_k6_legacy_v1_decision_and_pilot_validation_keep_passing`、`test_repository_contains_only_the_single_valid_pilot_subject`、`test_hand_editable_handoff_is_not_accepted_as_authority`、`test_projection_renders_fixed_short_and_detailed_text`、`test_plan_authority_markdown_is_still_accepted`、`tests/test_agents_lane_guidance.py`の3 test） | 全件、記載した行番号のsourceに存在 |
| 本record中の全pathの実在 | 全件実在（`records/development/2026-08-06-authority-reference-digest-check-triage-decision-v1.md`は未追跡だが実在） |
| 本record中に記載した全SHA-256と実bytesの一致 | `shasum -a 256`で全件一致 |
| `ic-authority-reference-digest-check-001--v1.json`の`content_digest`再計算 | 記載値`760d9ef9…931753f`と一致 |
| 公式全Test | `1020 passed`（failed 0、errors 0、Python 3.9.6、pytest 8.4.2、fallback `false`） |
| `git status --porcelain`（本record作成前） | `?? records/development/2026-08-06-authority-reference-digest-check-triage-decision-v1.md`の1件のみ。これは本recordと同じsessionで、Humanの仕分け判断を残すために作成したものであり、並行sessionの成果物ではない。両fileは同じcommitへ入れる |
| 既存fileの変更 | 0件。本recordはnew-onlyで作成した。実装、Test、fixture、既存記録、TODO、チェックリスト、設定のいずれも変更していない |
| commit、push、外部送信 | いずれも行っていない |

### 確認できなかったもの

- #5の訂正前の`recorded_at`の値。commit前に置き換えられたためrepositoryへ残っておらず、**未確認**である。
- #6の推奨誤りが会話中に行われた正確な時刻と文言。**未確認**である。
- #12の並行sessionが誰の指示で動いていたか。**未確認**である。
