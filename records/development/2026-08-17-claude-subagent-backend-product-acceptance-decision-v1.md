# 利用者による契約012の製品受入判断（残余risk 4点の受容） v1

- 判断日：2026-08-17
- 判断者：利用者（Human）
- 記録者：Claude
- 判断の種別：Task Contractの製品受入（契約012 §9-11）。残余riskの最終受容を含む

## 1. 承認文言【記録】

> 残余risk 4点を受容し、契約012の製品受入を承認する。受入判断record作成→TODO更新まで進めて

（2026-08-17 chat。Claudeが提示した推奨文言と同一）

## 2. 判断対象の束縛

| 対象 | path | SHA-256 |
| --- | --- | --- |
| 契約012候補v2（受入対象） | `records/task-contract/2026-08-17-claude-subagent-backend-candidate-v2.md` | `f95446a96b132c9dda5e225460cc4ab0214e535ebbc7ef9b79fdc953d936994d` |
| 実装Evidence（§9-1〜7） | `records/development/2026-08-17-claude-subagent-backend-implementation-evidence-v1.md` | `979b48868bdc69751c60fec4bb3f5e9abdf910b4c7d30b941b5cd7fe0922a7de` |
| §7.2訂正record（--verbose） | `records/development/2026-08-17-claude-subagent-verbose-argument-correction-decision-v1.md` | `3e96a358ea21c7c8a7e08a2436d3546d16dfb6e577706de29ddb1c96e6645375` |
| §7.2訂正record（通過変数） | `records/development/2026-08-17-claude-subagent-passthrough-environment-correction-decision-v1.md` | `d80b03d55ea1a75b742aa51f89f3428429eba51fd5bb55986037e808b42b3175` |
| §7.2訂正record（抑制注入） | `records/development/2026-08-17-claude-subagent-child-injection-correction-decision-v1.md` | `db84857854cda3bb8381535bd872653d5d82032d5f59d2a7799d023efad1d199` |
| 実運用E2E Evidence（§9-8・2往復） | `records/development/2026-08-17-claude-subagent-e2e-evidence-v1.md` | `64a40fb7fdb67bb43de08f0a5b777f41aab80ff5f39778b58d30633da72c9407` |
| E2E二往復目判定record（e2e-012-002・verified_with_findings・blocking 0） | `records/session-handoffs/2026-08-17-claude-subagent-backend-implementation-completion-rereview-subagent-verdict-v1.md` | `8af6f9acc49afaecdb0034cc5fae31c8c308fabb5ea71b4720a672d0bd10fcb6` |
| §9-10完了レビュー判定record（cr-012-002・agy・verified・blocking 0） | `records/session-handoffs/2026-08-17-claude-subagent-backend-implementation-completion-review-verdict-v1.md` | `5f0ba930d3c478609b12dd573a87c6815350d159630440dcc971391cbe70441c` |

## 3. 本判断が確定する事項

1. 契約`TC-RC3-PRODUCT-CLAUDE-SUBAGENT-BACKEND-012 / v2＋§7.2訂正record3件`を**製品として
   受け入れる**。受入条件§9-1〜10の充足はEvidence（§2の表）に固定済みであり、本判断により§9-11が
   成立、契約は完了する。
2. **§7.4残余risk 4点の受容**：(1) Tier 3の独立性は限定的（緩和：唯一oracle禁止の不変制約・
   機械反証併用・判定recordへのtier明記）、(2) claude CLI仕様変更への追随risk（緩和：安全側停止・
   raw完全保存。`--verbose`必須化の検出→契約訂正の追随実例が一巡済み）、(3) subagent起動も
   anthropicへの内容送出を伴う（事実の明示：操縦Claudeが同一provider下で常時repositoryを読んでおり
   新規の露出先は増えない。緩和：利用者指示起点・起動record台帳）、(4) 2 oracle不一致時の裁定は
   手動（合議の機械化は縦Cへ持ち越し）。
3. **正式経路化**：以後、`claude-subagent`はレビュー起動の正式な第2 backendとする。Tier 3のため
   起動ごとに`--accept-tier 3`の一致と受容根拠record（repo相対path・実在）を要し、恒久の無条件
   受容ではない。「`high` risk作業でTier 2／3を唯一の独立oracleにしない」不変制約は維持する。
4. E2E一往復目のblocking所見F-1（agy照合の和集合使用）は、利用者採用の修正（`b55903d`）と
   2 oracle（e2e-012-002・cr-012-002）の両確認で解消済み。同一対象集合（digest表13行完全一致）への
   初の2 oracle比較は両判定役一致（blocking 0）で成立した。

## 4. 持ち越し事項（本判断に含まれない）

- 非blocking所見の仕分け6件：`F-4`〜`F-7`（e2e-012-001判定record）・`R-1`〜`R-2`（e2e-012-002
  判定record）。
- 後続縦切りの順序選択（縦C合議・codex-cli第3 backend（疎通回復待ち）・自由文類型・API pending解除）。
- 実装経路確認部品の`CLAUDE_VERSION`更新（次回その経路使用時に自経路の手続きで実施）。
- 機械gate接続の改善候補`IC-REUSE-SEARCH-GATE-CONNECTION-001`（Human仕分け待ち）。

## 5. 未実施

- 後続契約の定義・実装、TODO更新（本record直後に共通手順で実施）。
