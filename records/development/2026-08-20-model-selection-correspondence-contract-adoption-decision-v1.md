# モデル選択・記載照合 契約採用・実装開始判断 v1

- Decision ID：`DEC-MODEL-SELECTION-CORRESPONDENCE-CONTRACT-ADOPTION-2026-08-20-V1`
- 判断日：2026-08-20
- 判断主体：利用者
- 利用者の文言：`契約016を採用する。TODO更新のうえ、RED先行で実装へ進めてください`
- 採用契約：`TC-RC3-PRODUCT-MODEL-SELECTION-CORRESPONDENCE-016` version 2
- 契約path：`records/task-contract/2026-08-20-model-selection-correspondence-candidate-v2.md`
- 契約SHA-256：`0a4a84032fc7470b88e923ec5508785f81abf6ad3f1bb87b30a3793f1943ddf2`
- 独立確認path：
  `records/session-handoffs/2026-08-20-model-selection-correspondence-contract-review-verdict-v1.md`
- 独立確認SHA-256：`9870d382c07558c18495934a7cf678951d36e9377c8cb2158e8c927995094218`
- 判断：`contract_adopted_implementation_authorized`

## 1. 判断

【記録】利用者は、事前走査・範囲案・自己レビュー（SR-C16-1〜3）・独立確認結果（`verified`・
blocking 0件・事後照合4点合格。severity low 1件＝和集合先頭不変の明記は「§7.4の連結定義で
論理的に保証」とReviewer自身が結論）の報告を受けた後、上記文言で採用を明示した。

【判断】契約016 v2と案B（統合＝依頼先行を軸にした3点セット＋登録定型化）を採用し、失敗試験を
先に作る実装（RED先行）を開始してよい。TODO更新を実装より先に行う。CHK-02（severity low）は
契約訂正を要しない（既定不変golden§9-2と既存pin試験が先頭不変を機械固定済み）。

## 2. 採用した範囲（契約v2 §5.1の要約）

1. `assemble`へ`--backend`・`--model`任意引数（既定＝現行と同一出力・byte不変golden）。
2. 依頼先行のbackend別差し込み（agy既定行は現行文言byte不変）。
3. 正準抽出核を`tools/reviewer_launch/core.py`へ単一実装し、checkの検査をbackend別所属へ強化。
4. `launch`へ`--model`任意引数＋起動前の記載照合（新設2語彙：`request_backend_mismatch`・
   `request_model_mismatch`）。
5. 登録手続きの定型化（データ駆動試験＋backendごとの承認pin＋手順書）。
6. RED先行の対象試験と実E2E 1回（terra指定＝別途の明示指示による）。導線2手順書の追記。

## 3. 採用していない範囲

- 許可model一覧の値の変更・実行時のmodel登録機構（直書き原則の維持）。
- 縦C合議・`record.py`／G30／session_logs／RQ2装置の変更・過去recordの書き換え（契約v2 §5.2）。
- 製品受入（§9-7実E2E・§9-8完了レビュー・§9-9残余risk 4点の確認の後に別途判断する）。

## 4. 開始条件

【実測】独立確認は`verified`・blocking 0件・事後照合4点`passed`。正式再利用検索は
`start_allowed: true`。作業単位遷移検査`passed`・worktree clean。

## 5. 未実施

- TODO更新（本record直後に共通手順で実施）。RED先行の実装。実E2E（明示指示待ち）。完了レビュー。
  製品受入。
