# codex-cli第3 backend 契約採用・実装開始判断 v1

- Decision ID：`DEC-CODEX-CLI-BACKEND-CONTRACT-ADOPTION-2026-08-20-V1`
- 判断日：2026-08-20
- 判断主体：利用者
- 利用者の文言：`契約015を採用する。TODO更新のうえ、RED先行で実装へ進めてください`
- 採用契約：`TC-RC3-PRODUCT-CODEX-CLI-BACKEND-015` version 2
- 契約path：`records/task-contract/2026-08-20-codex-cli-backend-candidate-v2.md`
- 契約SHA-256：`e2c8b5b1aeadb3d7e295f78e4b92ea8a6edd5f878180ffbccfa471c237b8dccc`
- 独立確認path：`records/session-handoffs/2026-08-20-codex-cli-backend-contract-review-verdict-v1.md`
- 独立確認SHA-256：`d82b0b370d1f91fdd88cfb8c81e1a4570c05300876e7194105dab97e610bec0a`
- 関連承認：許可model承認record
  `records/development/2026-08-20-codex-allowed-models-approval-v1.md`
  （SHA-256 `f0f0536ccda07d942e06c1d96fa75c2781387763f63afd0439a5d9c9f7d67c99`）
- 判断：`contract_adopted_implementation_authorized`

## 1. 判断

【記録】利用者は、事前走査・範囲案・自己レビュー（SR-C15-1〜4）・独立確認結果（`verified`・
blocking 0件・事後照合4点合格）の報告を受けた後、上記文言で採用を明示した。

【判断】契約015 v2と案B（登録簿深化＋codex-cli追加）を採用し、失敗試験を先に作る実装（RED先行）を
開始してよい。TODO更新を実装より先に行う。

## 2. 採用した範囲（契約v2 §5.1の要約）

1. backend登録簿の深化（name分岐6箇所の登録参照化・agy／claude現行値の不変移設・byte不変golden）。
2. codex-cli backendの追加（provider openai・Tier 1・§7.2起動固定形・§7.3認証遮断）。
3. 許可model 2値`gpt-5.6-sol`・`gpt-5.6-terra`の直書き固定（起動は一覧先頭）。
4. RED先行の対象試験と実E2E 1回（E2E起動は別途の明示指示による＝契約§2）。
5. 導線文書（reviewer-launch-run.md）への追記。

## 3. 採用していない範囲

- `tools/request_builder/`の変更（`IC-REQUEST-BUILDER-MODEL-CHECK-SCOPE-001`は(b)裁定＝
  契約015受入後の独立小作業単位）。
- terraの起動時選択機構・縦C合議・session_logs系の変更・外部API後続（契約v2 §5.2）。
- 製品受入（§9-8実E2E・§9-10完了レビュー・§9-11残余risk 6点の確認の後に別途判断する）。

## 4. 開始条件

【実測】独立確認は`verified`・blocking 0件・unexamined空・事後照合4点`passed`（判定record参照）。
正式再利用検索は`start_allowed: true`（証明書record参照）。作業単位遷移検査`passed`・worktree clean。

## 5. 未実施

- TODO更新（本record直後に共通手順で実施）。RED先行の実装。実E2E（明示指示待ち）。完了レビュー。
  製品受入。
