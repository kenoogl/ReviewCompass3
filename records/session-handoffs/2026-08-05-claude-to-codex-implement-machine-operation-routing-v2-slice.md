# Claude → Codex：機械操作routing v2 最小縦切りの実装 完了報告

指示：`records/session-handoffs/2026-08-05-codex-to-claude-implement-machine-operation-routing-v2-slice.md`

承認記録、TDD、独立runner、Evidence、Plan／checklist／TODO更新を一つの意味単位として実装・検証・commitした。

## commit

- commit SHA：`91827a577dc7e7012fbad8e3c998108986869c2f`
- message：`Implement operation routing v2 minimum slice`
- 9 file、1,319行追加・25行削除
- stageは今回作成・更新した9 pathだけを明示列挙した。`git add -A`と`git add .`は使っていない。
- commit後のread-only確認：`git status --short`は空。
  `python3 tools/development/work_unit_transition.py --work-status completed`は
  `{"findings": [], "next_work_allowed": true, "reminder": null, "status": "passed"}`

## RED／GREEN

| 段階 | 実行 | 結果 |
| --- | --- | --- |
| RED | `.venv/bin/python3 -m pytest -q tests/test_operation_routing_v2.py` | `16 errors`（module未作成のため全testが失敗） |
| GREEN（対象test） | 同上 | `16 passed` |
| GREEN（公式全test） | policy runner suite `full` | `845 passed`（exit 0） |

RED testだけのcommitは作っていない。実装中にtestの期待を緩めていない。
受入条件1〜9はすべて正常・負例・境界例で固定し、対応表をGREEN Evidenceに記した。

## fault injection

停止条件ごとにcallbackの呼出し記録を独立に確認した。いずれも**callbackは一度も呼ばれていない**。

| 注入した状態 | 停止code | callback呼出し |
| --- | --- | --- |
| 分類`unknown`を含むinventory | `unknown_classification_not_executable` | 0回 |
| 必要権限に対しattestationが空 | `approval_required`（必要権限を一回の集合で返す） | 0回 |
| `external`を含むinventory（attestationは充足） | `external_operation_not_supported` | 0回 |
| receiptを別inventoryへ照合 | `receipt_identity_mismatch` | 追加呼出しなし |

## Decision／Evidence／実装物

| 種別 | path | SHA-256 |
| --- | --- | --- |
| 承認Decision `DEC-MACHINE-OPERATION-ROUTING-001` | `records/development/2026-08-05-machine-operation-routing-v2-approval-decision-v1.md` | `c73cdc69b3ca3251b9de9480867c9677e0de4312f7bedff138a407af297cd969` |
| GREEN Evidence | `records/development/2026-08-05-machine-operation-routing-v2-green-evidence-v1.md` | `e4f8d9f865e6b6d35e7d00a21eba54c13b1ed331fca3183827b1262d285d88eb` |
| module | `tools/development/operation_routing.py` | `f735299433b49b868b713dfcc4ed1973c7d4771f906242e3e3932e39bf269049` |
| 受入test | `tests/test_operation_routing_v2.py` | `6da141f20f7b8a31e270c6a2dc2195cbce20c908633d81e0e939e51b703d6fc4` |
| 公式全test receipt | `records/development/2026-08-05-machine-operation-routing-v2-green-test-receipt-v1.json` | `b6f55b5c7096b19106656403d9a7ad975f79debff61767827ac425be111d018a` |

v2提案は状態を`approved_for_development_implementation`へ更新し、冒頭に短い注記を追加して
承認範囲が§3だけであること、正式Issue Resolution Plan／Task Contractへ昇格していないこと、
Issue stateを変更しないことを明記した。提案時点の本文は歴史として残し、全面的な時制書換えはしていない。

## host境界

- **承認と取得済み権限の確認はhost側に置く。** project内は、inventoryの分類から必要な権限種別を
  計算して出すだけである。
- `host attestation`はcallerが渡す入力である。moduleがOS、sandbox、Codex hostの権限を
  検査・付与・迂回することはない。この性質は、module source textに外部process起動やOS操作の語が
  現れないことをtestで機械確認している（報告文だけを根拠にしていない）。
- 必要な権限が未取得なら、最初の書込みを一度も試さず停止し、必要権限を一回の集合で返す。
  失敗してから権限を切り替える経路は持たない。
- Codex hostのJavaScript tool構文と外部toolのAPI schemaはproject内では解決できない。
  `HTC-A5D1BCCA`を解決済みとして扱っていない。
- runnerは既存policy runnerと別moduleであり、policy runnerへのimport依存を持たない。
  最小CLIはinventoryを読んでpreflightをJSONで出すだけで、commandを実行しない。

## Plan／checklist／TODO

- Current PlanのInter-work行に、C9の§3最小縦切りがHuman承認済み・実装済みであることを追記した。
  未完了境界には構造化argv executor、cache root固定、既存直接操作の移行、host側tool構文、
  正式製品schema、UI、automation、3正式Issueの正式Plan化・実装一般、Work 8評価を残した。
- checklistのIssue Resolution早期Pilot限定拡張節に、C9最小縦切りのDecisionとGREEN Evidenceを
  digest付きで追記した。V4 Issueの正式Plan化・実装一般を完了と誤記していない。
- TODOは共通手順で更新した。§3だけ実装済みであること、後続のargv executor／cache root／
  既存操作移行が未実施であること、C9全体をcloseしていないことを示し、Decision、v2提案、
  GREEN Evidence、公式test receiptの実SHA-256を機械取得して参照した。
  なお更新後に12,288 byteの上限を超えたため、更新規則に従って累積していた中間Evidence linkを
  9行整理した（10,729 bytes → 最終的に上限内）。TODO validatorは更新後と最終stage前の2回とも
  `{"findings": [], "status": "passed"}`である。

## 変更しなかった対象

- shellを実行する汎用argv executor、`shell=True`相当、既存直接shell操作の置換：作っていない。
- cache rootの固定：していない。
- Gitへの実書込み、push、tag、外部送信、host／sandbox権限の取得・迂回・自動承認：していない。
- Codex hostのJavaScript tool構文、外部toolのAPI schemaへの対応：していない。
- `ISSUE-HTC-66C3E6CA`が扱うEvidence／TODOの定型欄生成：していない。
- V4 Issue recordのstate変更：していない。`ISSUE-HTC-C9F6C917`は`registered`のままで、
  file SHA-256も`66cfe50ce79136bca5e92b35b72502cedfb8b6f6f3e20ade1e027bcbf1fec0ed`で不変である。
- 正式製品schema／UI／automation、Task Contractの新規作成：していない。
- 既存のpolicy runner、Git helper、TODO helper、Task Contract resolver、`config/development-policy.json`、
  既存testの変更：していない。今回のcommitに含まれるのは新規module、新規test、Decision、Evidence、
  receipt、v2提案の状態注記、Plan、checklist、TODOだけである。
- push、tag、amend、rebase、reset、force push、外部送信：行っていない。
- 本完了報告はcommitに含めていない（`.gitignore`により無視される）。
