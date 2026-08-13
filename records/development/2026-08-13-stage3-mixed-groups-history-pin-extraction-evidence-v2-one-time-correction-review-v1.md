# 第3段 混在三群の履歴固定候補抽出 v2 一回限り修正後確認 v1

- 確認日：2026-08-13
- 状態：`verified`
- 修正commit：`20cc48d40cfc60f7a260d4c52c7e52be1fc0a3fb`
- 対象：`records/development/2026-08-13-stage3-mixed-groups-history-pin-extraction-evidence-v2.md`
- 対象SHA-256：`d74a2a202f78273e1cfb6aabc0097098a1820c56db32b8f38060c95d4cd9ba34`
- 先行レビュー：`records/development/2026-08-13-stage3-mixed-groups-history-pin-extraction-independent-completion-review-v1.md`
- 先行レビューSHA-256：`3a5744c0ad210ea86db9e618d12bf5c59599fd66f098b119c75babc4570e80af`

## 1. 判定

【判断】`verified`。先行レビューが指摘したG11三件だけが第一候補へ追加され、現在利用者、追加履歴、
役割終了候補とする理由、実施時の意味単位が補われた。母集団110件、既確認13件の現在保証、未実施境界は
変わっていない。限定修正後の成果として採用できる。

## 2. 修正範囲

【実測】修正commitの変更はv2一件の追加だけだった。置換元v1のSHA-256は
`408079c8f9e2834bc5d3cd463f4fc77ab909247a16960f38dd948cf927dc6313`のままで、先行レビュー記録も不変だった。

【実測】v2は次の三件だけを追加の第一候補とした。

- `test_change_scope_ignores_later_record_and_todo_commits`
- `test_change_scope_rejects_forbidden_commit_before_later_allowed_commit`
- `test_change_scope_does_not_hide_code_inside_handoff_directory`

【実測】数値は、G06が4件、G07が1件、G11が11件で第一候補16件、そのうち現在保証13件、役割終了候補3件で
一致する。母集団はG06が24件、G07が8件、G11が78件、合計110件、重複0件のままで、残りは94件となる。

## 3. 先行指摘の解消

【実測】三件が呼ぶ`_implementation_paths_since_base`、`_is_followup_record`、`_commit_changed_paths`、
一時リポジトリ生成処理は同じ試験ファイル内にあり、製品コード、設定、正規入口に同名の利用箇所はない。
三件は現在の作業場所ではなく、一時Gitリポジトリ内で試験専用の変更範囲計算を確認する。

【記録】追加履歴は、`df48bba`にあった固定基準commitから現在の作業場所へ計算を適用する元試験が、後続の
`f2e4be9`、`7816df1`、`6cb26e7`で一時入力三件へ展開され、`354c57e`で元試験と固定`BASE_COMMIT`だけを
削除した経過を示す。

【判断】現在製品の変更範囲処理を検査する三件ではなく、完了した実装時点の範囲確認から残った試験専用処理を
検査する三件であるため、`役割終了候補`という分類は妥当である。削除の承認とは区別されている。

## 4. 意味単位と維持範囲

【実測】三件を除くと、`ALLOWED_PATHS`、`_git`、`_commit_changed_paths`、`_is_followup_record`、
`_implementation_paths_since_base`、`_initialize_test_repository`、`_commit_test_change`、`subprocess`の取込は
同ファイル内で利用者を失う。

【判断】実施する場合に三試験と上記の試験専用処理・取込を同じ一ファイル内の意味単位とする境界は妥当である。
現在の入口三試験、案内文書、Pilot製品コード、G11の他75件を変更しない境界も明記されている。

【判断】G06の4件、G07の1件、G11の既確認8件を現在保証として残す先行判断は変更されていない。v2は残り94件を
すべて現在製品へ直接接続すると再主張せず、今回未整理の現役集合へ残すだけに限定している。

## 5. 残る止める指摘と報告不一致

【判断】残る止める指摘は0件。報告不一致は0件。先行レビューで影響を受けた第一候補件数、履歴専用候補0件、
G11除外理由、実施計画の境界は、三件を役割終了候補として追加することで訂正された。

## 6. 確認範囲と未実施

【実測】本確認は、先行指摘三件の追加、利用箇所、履歴、分類、意味単位、13件の維持、110件の集計、
未実施宣言だけを確認した。新しい反証は作らず、先行レビューで使った読取り結果を変更点へ再適用した。

【未実施】対象成果、置換元、先行レビュー、試験、試験専用処理、製品コード、設定、証跡、対応表の変更、
削除案、試験実行、全試験、変異検査、他群、新機構、実施計画の作成・承認、Claude確認、外部送信、push、
履歴書換え、第3段完了判断は行っていない。
