# 読み取り専用argv executor最小slice 承認Decision v1

- decision ID：`DEC-MACHINE-OPERATION-ROUTING-READ-ONLY-ARGV-001`
- decision maker：Human
- decided at：2026-08-05
- 対象Issue：`ISSUE-HTC-C9F6C917`
- 指示：`records/session-handoffs/2026-08-05-codex-to-claude-implement-read-only-argv-executor-slice.md`

## 1. Humanの承認文言

> Humanは、`ISSUE-HTC-C9F6C917`の後続Planのうち、読み取り専用の構造化argv executor最小sliceだけを
> 承認した。

## 2. 承認した範囲

- shell文字列を使わず、**argv配列のまま**読み取り専用操作を起動する経路。
- 最初に扱う実行templateは`git status --porcelain`**だけ**。`--`の後ろにpathspecを0個以上置ける。
- `operation_routing.py`のinventory／preflight／receiptを**そのまま利用する**。
  executorは新たな権限判定・付与・再分類をしない。
- cache rootは**次の別slice**に分ける。

## 3. 対象外（この承認に含まれない）

- cache rootの決定的な固定
- Git metadata書込み、project成果物書込み、external操作
- host側tool構文、外部送信
- 既存の直接操作の移行、移行inventoryの作成
- 環境変数の設定、既存call siteの置換
- hook、watcher、scheduler、push、tag、外部送信

これは**後続Plan全体の承認ではない**。後続Plan提案
`docs/design/2026-08-05-machine-operation-routing-follow-on-plan-proposal.md`の他のHuman判断点
（cache rootの配置と保持方針、移行対象の優先順、host境界の確認）は未承認のままである。

`ISSUE-HTC-C9F6C917`のIssue recordのstateは`registered`のまま変更しない。
正式なIssue Resolution Plan、Task Contract、Workflow permitも作らない。

## 4. 参照入力と作成時のSHA-256

| 種別 | path | SHA-256 |
| --- | --- | --- |
| 後続Plan提案 | `docs/design/2026-08-05-machine-operation-routing-follow-on-plan-proposal.md` | `ab6d9b3bf33a6348a5718062930a7d58aa1bf8df75c22fc415a7221ba29d024c` |
| 最小縦切りの既存設計 | `docs/design/2026-08-05-machine-operation-routing-issue-plan-proposal-v2.md` | `e01c3aaf8039377da2b43dab7f735d28a2f86bf10aa83f5bb22e5dd1eefa8572` |
| 既存承認 | `records/development/2026-08-05-machine-operation-routing-v2-approval-decision-v1.md` | `c73cdc69b3ca3251b9de9480867c9677e0de4312f7bedff138a407af297cd969` |
| receipt整合性の訂正 | `records/development/2026-08-05-machine-operation-routing-v2-receipt-integrity-correction-decision-v1.md` | `f73f06e12f464a27ded059522e37015acbd2f9487d7d65d55ed96823a6f8033b` |
| 既存module | `tools/development/operation_routing.py` | `0fb5636feac3e12c42104830cd710bdb2a6f9398b784edf211c57128e1cd9178` |
| 対象Issue | `.reviewcompass/workflow/issues-v4/issue-htc-c9f6c917--v1.json` | `66cfe50ce79136bca5e92b35b72502cedfb8b6f6f3e20ade1e027bcbf1fec0ed` |

承認範囲は、後続Plan提案の**§2.1（argv executorの責任境界）と§3.2（各段階で実装しないこと）に
定めたargv executor最小slice**に対応する。

## 5. 維持する停止原則

最小縦切りで固定した原則は変えない。

- `unknown`分類はfail-closedで停止する。
- 未取得権限では、書込みを一度も試さず停止する。
- `external`操作はこのrunnerで実行しない。
- inventory／preflight／receiptのidentityが一致しなければ停止する。
- host側の問題をproject内で解決したと書かない。

executorは、入力・template・cwd・分類・preflightのいずれかで失敗した場合、
**runnerを一度も呼ばない**。
