# 利用者による契約011の製品受入判断（残余risk 4点の受容） v1

- 判断日：2026-08-17
- 判断者：利用者（Human）
- 記録者：Claude
- 判断の種別：Task Contractの製品受入（契約011 §9-11）。残余riskの最終受容を含む

## 1. 承認文言【記録】

> 契約011を製品として受け入れる。残余risk 4点を受容する

（2026-08-17 chat。Claudeが提示した推奨文言と同一）

## 2. 判断対象の束縛

| 対象 | path | SHA-256 |
| --- | --- | --- |
| 契約011候補v3（受入対象） | `records/task-contract/2026-08-17-request-builder-candidate-v3.md` | `146344498d7c5ce3c228a9eccb5f7a985f260691589688b6447385236273c6a1` |
| 実運用E2E・完了レビューEvidence（2往復・fence修正） | `records/development/2026-08-17-request-builder-e2e-evidence-v1.md` | `fac5a19072ef241a24c248a9d09cb4efd92d11ccd5e8ba62434cc37492ceba09` |
| 完了レビュー判定record（e2e-011-002・verified・blocking 0） | `records/session-handoffs/2026-08-17-request-builder-implementation-completion-rereview-verdict-v1.md` | `16f8adecc4a6cafd9d4781695adf9db85a80d2fe95c65472a84b5c90cef6d2de` |
| 実装Evidence（§9-1〜7） | `records/development/2026-08-17-request-builder-implementation-evidence-v1.md` | `939d54afb56d4a481b9ece80d926dfbc2cc83c19981b416c0580970f854fd6ba` |

## 3. 本判断が確定する事項

1. 契約`TC-RC3-PRODUCT-REQUEST-BUILDER-011 / v3`を**製品として受け入れる**。受入条件§9-1〜10の充足は
   Evidence（§2の表）に固定済みであり、本判断により§9-11が成立、契約は完了する。
2. **§7.4残余risk 4点の受容**：(1) 機械検査は形式の守りであり、依頼内容の質はLLMと独立確認の守りに
   残る、(2) 除外3形式定数は契約009側の将来改定で乖離しうる（緩和：同値性試験が乖離を検出して停止）、
   (3) 雛形は実測2通に基づく（緩和：類型登録形が追加を局所化）、(4) 除外と同形の実鍵の既知すり抜け
   （契約009 v2 §7.2で受容済みの既知限界と同一。緩和：通過明示試験による可視化・既定5 pattern不変）。
3. **依頼record作成の正式経路**：以後、レビュー依頼recordの作成は`reviewcompass3-request-builder`
   （assemble→LLM記入→check合格）を正式経路とする。手書きはfallbackとして残るが、check合格を経ない
   依頼recordを headless起動の対象にしない。
4. e2e-011-001のblocking所見（fenceの内外非区別）は、利用者採用の修正（`442b05f`）と再レビュー
   `verified`で解消済み。再発類型の教訓（構造要素は正準位置だけを正とし他は拒否）は
   `records/development/2026-08-17-request-builder-e2e-evidence-v1.md` §2に前例参照つきで固定した。

## 4. 持ち越し事項（本判断に含まれない）

- 後続縦切りの順序選択（claude-subagent第2 backend・縦C合議・自由文類型の追加・API pending解除）。
- 機械gate接続の改善候補`IC-REUSE-SEARCH-GATE-CONNECTION-001`（Human仕分け待ち）。
- codex CLIの疎通回復時の第3 backend追加。

## 5. 未実施

- 後続契約の定義・実装、TODO更新（本record直後に共通手順で実施）。
