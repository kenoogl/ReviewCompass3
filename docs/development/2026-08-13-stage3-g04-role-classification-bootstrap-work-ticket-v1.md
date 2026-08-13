# 第3段 G04六試験の役割分類 軽量作業票 v1

- 作成日：2026-08-13
- 状態：`proposed_pending_start_check`
- 基準commit：`e499a45`
- 危険度案：`low`
- 作業担当：操縦役
- 完了レビュー担当：作業担当とは異なる新規サブエージェント一者
- 他社モデル確認：本作業では行わない
- 対象Issue：`ISSUE-TEST-GROWTH-STATE-PINNING-001`

## 1. 目的

意味群G04の六試験を同じ2026-08-11作業文脈で比較し、各試験を`現在の動作保証`、`履歴・監査資料`、
`両方`、`役割終了`のいずれかへ分類する。六件をまとめて削除する案は作らず、後続の実施計画に使える
意味的な単位を明らかにする。

## 2. 入力と根拠

- 意味群分類Evidence：`records/development/2026-08-13-stage3-test-cleanup-semantic-grouping-evidence-v1.md`
  - SHA-256：`cc77c218bc4baefc5e734ad7310824235900f32c122bd5f3c5ecdb786cb9399e`
- 意味群分類の独立完了レビュー：
  `records/development/2026-08-13-stage3-test-cleanup-semantic-grouping-independent-completion-review-v1.md`
  - SHA-256：`fe740db405e7bba70feb8dc7fd47673fb679903a40c4682c973a5765fc2df547`
- 最初の一件の再評価v3：
  `records/development/2026-08-13-stage3-first-test-cleanup-lifecycle-reassessment-v3.md`
  - SHA-256：`d7c51c08221825786cc443815f6c7c44cf11797b8a3bd47ef7114a6e92ef7476`
- 手動の他社モデル確認回数Decision：
  `records/development/2026-08-13-stage3-manual-external-review-limit-decision-v1.md`
  - SHA-256：`9c0bd9d371b1f6b59be49818b759d17e3877d645f42ff6dc4a4c0eacbeb05136`
- 対象試験ファイル：`tests/test_claude_bootstrap_entrypoints.py`
- 当時の宣言対応表：
  `records/development/2026-08-11-claude-bootstrap-manifests/declaration-red-map-v1.json`
- 固定実装前commit：`8cdac45c051af24f7c7e2663d74125d24895e726`

## 3. 作業範囲と対象外

対象は次の六試験だけとする。

1. `test_process_inventory_baseline_matches_fixed_commit`
2. `test_existing_pilot_commands_and_six_egress_files_remain_unchanged`
3. `test_red_suite_uses_only_fake_process_and_never_launches_claude`
4. `test_scope_review_human_red_approval_and_all_fixed_inputs_are_pinned`
5. `test_declaration_map_keys_equal_scope_requirement_ids`
6. `test_red_evidence_keeps_green_fields_explicitly_unimplemented`

各試験について、現在の入力と利用者、検出する欠陥、同じ保証を持つ現役試験、参照する履歴資料、固定commitからの
回復可能性、削除時に連鎖する修正、同型試験を増やす誘因を調べる。

対象外は、六試験または他試験の削除・統合・変更、製品コード、設定、証跡、対応表の変更、全試験、変異検査、
新しい台帳・検査器・試験の追加、401件の再分類、実施計画の確定、Claudeへの手動受け渡し、第3段完了である。

## 4. 期待する成果

`records/development/`に役割分類Evidenceを一件作る。各試験について次を短く示す。

- 四分類の判定と根拠
- 現在の利用者と検出する欠陥
- 履歴資料または固定commitとの関係
- 他の現役保証との重複または固有性
- 維持、削除、統合を後で比較するときに残る不確かさ

六件を一括処理せず、後続で同じ実施単位にできる候補と、分離すべき候補を示す。承認済みの六番目は
`削除判断済み・実施待ち`を維持し、分類結果と矛盾が見つかった場合だけ停止する。

## 5. 機械で確認する事実と正規入口

- 対象六試験がG04の六件と完全一致することを既存401件一覧と分類Evidenceから確認する。
- `rg`とGitの読み取り機能で、試験名、参照資料、製品処理、固定commit、現在の参照元を列挙する。
- 各試験本文が実際に読む入力と確認条件をPython構文木または本文検索で抽出する。
- 対応表の要求識別子と対象試験名の対応を機械抽出する。
- 成果物の再読込み、参照解決、記載件数六件、`git diff --check`を確認する。
- 読み取り・文書作業なので、試験実行と形式的な赤緑は行わない。

## 6. レビューで判断する事項

- 試験が欠陥を検出できる事実と、その保証を現役集合へ残す必要性を分けているか。
- 現在の安全境界を履歴専用と誤分類していないか。
- 当時の対応表を現在状態の合否判定器にしていないか。
- 六件を一括削除する結論へ飛躍していないか。
- 承認済み一件の判断と実施待ちの順序を保っているか。
- 実行時間ではなく、理解負担、調査範囲、修正連鎖、回復可能性、増加誘因を比較しているか。
- 本作業に不要な新しい仕組みや高価な確認を追加していないか。

## 7. 停止条件と完了条件

次の場合は停止する。

- 対象六件がG04と一致しない。
- 承認済み一件が現在の製品安全に必要という新しい反証が成立する。
- 分類のために試験、製品コード、設定、証跡、対応表の変更が必要になる。
- 外部送信、不可逆操作、未承認の意味変更が必要になる。

次をすべて満たしたとき完了候補とする。

- 六件すべてを四分類のいずれかへ根拠付きで分類した。
- 現在保証、履歴資料、重複、固有性、回復可能性を区別した。
- 同じ実施単位の候補と分離すべき候補を示した。
- 削除・統合・試験実行・成果物変更を行っていない。
- 新規サブエージェント一者へ渡す固定材料を作れる。
