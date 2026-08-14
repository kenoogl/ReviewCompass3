# Issue解決処理v4の使用停止と状態反映中止 Decision v1

- 判断日：2026-08-14
- 判断者：利用者
- 対象処理：`tools/development/issue_resolution_v4.py`
- 対象Issue：`ISSUE-AUTHORITY-REFERENCE-DIGEST-CHECK-001`
- 状態：`adopted`

## 1. 利用者判断

【記録】利用者は次のとおり判断した。

> 修正案CとIssue状態更新処理の正式利用は承認しない。本作業は中止する。対象Issueはregistered、処理は暫定・使用停止のまま維持する。G01の実装完了判断は変更しない。今回確認した欠陥と中止判断を証跡へ残し、TODOを更新した後、第3段の方針修正へ戻ること。コード・試験・設定は変更しないこと。

## 2. 確認した欠陥

【実測】成熟度精査では、解決記録の親フォルダ作成が`OSError`（入出力の失敗を表す例外）で失敗した場合、
対象Issueが`resolved`へ変更されたまま残り、解決記録が作成されない欠陥`IR-MAT-001`を再現した。

【記録】この欠陥は次の独立レビューでも別の使い捨て複製と独自の故障注入により再現された。

- 成熟度精査Evidence：
  `records/development/2026-08-14-issue-resolution-v4-maturity-reassessment-evidence-v1.md`
  - SHA-256：`8038ce27b0c3fa41e0ebdb70a860811d4bb7e1649847b16c0a88c25d5834d050`
- 独立完了レビュー：
  `records/development/2026-08-14-issue-resolution-v4-maturity-reassessment-independent-completion-review-v1.md`
  - SHA-256：`893fde2d1d05f438f47b87fe28ac5c5103081ac0eec127019a14f58c7b7aa1fd`
- 限定訂正レビュー：
  `records/development/2026-08-14-issue-resolution-v4-maturity-reassessment-correction-review-v1.md`
  - SHA-256：`7e69b63f1dc34b9920b92acb4a388f6610319670f08550e0aa6cc7870d854470`
  - 判定：`verified`、止める指摘0件、報告不一致0件

【判断】欠陥は正式利用を止めるが、本Decisionにより修正自体を採用しない。修正案C、別案、新しい試験、
新しい機構へ連鎖させない。

## 3. 採用する状態

### 3.1 対象処理

【判断】`issue_resolution_v4.py`は開発支援コードとしてリポジトリに残すが、ReviewCompass3自身には適用しない。
ソースの宣言は次のまま変更しない。

- `lifecycle: provisional`
- `normative_status: non-normative`
- `promotion_required: true`

【判断】運用上は使用停止とする。正式利用化、成熟度宣言変更、修正案Cの実装を行わない。将来の別判断が
明示されるまで、実Issueの状態変更には使わない。

### 3.2 対象Issue

【実測】判断時点の対象Issueはversion 1、state `registered`、SHA-256
`d260ed570598f56ada2cd6b4e54f15543bba0e792db65c14403a038f8100afbe`である。

【判断】対象Issueを`resolved`へ変更せず、`registered`のまま維持する。Human裁定JSON、解決記録、
state変更、`content_digest`更新を行わない。

### 3.3 G01

【記録】G01現役接続の独立完了レビューは`verified`、止める指摘0件、報告不一致0件である。

- `records/development/2026-08-14-stage3-g01-authority-reference-guard-activation-independent-completion-review-v1.md`
- SHA-256：`c441ef796f34959cadf5a111826af50fa02e46a3e367f896768a417940f78515`

【判断】Issue台帳の状態反映を中止しても、G01の実装、19件の試験、実文書2件・11参照、正規全試験の
完了判断は変更しない。G01を未完了または暫定へ戻さない。

## 4. 第3段への復帰

【判断】Issue状態反映の枝をここで終了し、立て直し計画v5の第3段へ戻る。次の作業は、2026-08-14に
追記した第3段完了条件に従い、第3段開始時点から増えたコード、試験、文書の全体列挙と整理へ進むための
範囲を固定することとする。

【判断】最初に第3段開始commitを既存DecisionとGit履歴から確定し、段完了候補までの差分を正本にする。
各成果物の現在の利用先、守る性質、重複、再利用・共通化、四分類を後続で確認する。このDecisionでは
列挙、分類、削除、統合をまだ行わない。

## 5. 変更しない範囲

- `tools/development/issue_resolution_v4.py`を含むコード。
- `tests/test_issue_resolution_v4.py`を含む試験。
- `config/development-issue-resolution-pilot-v4.json`を含む設定。
- 対象Issueと他Issueの台帳record。
- G01のコード、試験、設定、Evidence、完了判断。
- 第3段と第4段の現行計画・追補判断。
- 履歴。rebase、reset、amend等の履歴書換えを行わない。

## 6. 次のHuman判断

【判断】本状態反映作業について追加のHuman判断はない。修正案C、正式利用化、Issue状態反映を
Human判断待ちとして残さない。

【判断】次にHumanへ渡す判断は、第3段成果物の列挙範囲を固定し、意味群ごとの整理候補を作った後に行う。

## 7. 未実施

【未実施】コード・試験・設定の変更、対象Issueと他Issueの状態変更、Human裁定JSON・解決記録の作成、
修正案C、正式利用化、新機構・検査器・試験・関門、G01完了判断の変更、第3段成果物の列挙・分類・整理、
第3段・第4段の完了判断、外部送信、履歴書換え。
