# Claude → Codex：機械操作routing IssueのPlan提案作成 完了報告

指示：`records/session-handoffs/2026-08-05-codex-to-claude-design-machine-operation-routing-plan.md`

指示の実施範囲をすべて完了した。作成したのはHuman承認待ちのPlan提案、test receipt、TODO更新だけである。
正式Plan、Decision、Task Contract、code、test、config、policyは作成・変更していない。
`ISSUE-HTC-C9F6C917`のstateは`registered`のままである。

## commit

- commit SHA：`8deb99ae6b8e329c1b2946c97e5ede139985580b`
- 内容：Plan提案、TODO更新、全test receipt（計3file、262行追加・7行削除）
- `git diff --check`：stage前後とも合格
- commit後の追跡fileのworktree：clean（未追跡のまま残るのは、commitへ混ぜないsession-handoffsの
  完了報告14件のみ。本報告を含む）

## 提案のpathとDigest

| 種別 | path | SHA-256 |
| --- | --- | --- |
| Plan提案 | `docs/design/2026-08-05-machine-operation-routing-issue-plan-proposal.md` | `722e9448971bcf3e97423ab1b9b137ca202f1f1c0ed7afdd92a619738e608bfa` |
| 全test receipt | `records/development/2026-08-05-machine-operation-routing-issue-plan-proposal-test-receipt-v1.json` | `ab00e2d552361377b4a116b9607305daf37e31d3102da95ea7fadd135b0ae849` |

提案の状態は`awaiting_human_approval`であり、冒頭に「正式なIssue Resolution Plan、Decision、
Task Contractではない」「Humanが承認するまでcode、test、config、policy、runnerを変更しない」
「Issueのstateは`registered`のまま」「本書のどの記述も実装着手の許可にならない」と明記した。

## 固定入力（提案§0に表として固定）

対象Issue、主decision、関連4 decision、開発方針、V4承認・閉鎖recordをすべて読み、pathと実SHA-256を
提案へ固定した。作成後に再読込し、10件のdigest行がすべて実fileと一致すること、本文で言及した11 pathが
すべて存在することを機械確認した（不一致0件、欠落0件）。

| 種別 | path | SHA-256 |
| --- | --- | --- |
| 対象Issue | `.reviewcompass/workflow/issues-v4/issue-htc-c9f6c917--v1.json` | `66cfe50ce79136bca5e92b35b72502cedfb8b6f6f3e20ade1e027bcbf1fec0ed` |
| 主decision | `.reviewcompass/workflow/triage-decisions-v4/dec-htc-c9f6c917--v1.json` | `5b698bd0e9069128710bef161e3d60475002c89c4a4b70cce015a39c31bbf444` |
| 関連decision | `.reviewcompass/workflow/triage-decisions-v4/dec-htc-477ea1a4--v1.json` | `9e4d76f2e791deaa8c8bfd5fbb97e2ff01aff4449828a01d439e29cac3498d78` |
| 関連decision | `.reviewcompass/workflow/triage-decisions-v4/dec-htc-186e9b83--v1.json` | `94c102c1313f21e799df8e4bca992663238b605c561c75869a55a3024d0aff62` |
| 関連decision | `.reviewcompass/workflow/triage-decisions-v4/dec-htc-9dce8503--v1.json` | `8088e41b42a2e59b78bcb5717c9328c6e0a0eb0f50914efb518097c65844c606` |
| 関連decision | `.reviewcompass/workflow/triage-decisions-v4/dec-htc-a5d1bcca--v1.json` | `5f8c771d6bf70b834e759b4c960debee7279906f2673090d16534e75f218628f` |
| 開発方針 | `docs/development/2026-08-02-development-policy.md` | `9078276d7ba1f540495a9679a75f12f9dac0c7717fcfd637e883f41b6bf739a0` |
| V4承認Decision | `records/development/2026-08-05-historical-todo-issue-intake-v4-approval-decision-v1.md` | `019879235577b39489e4383cd0fa092c562631d3c1b1e1ffa311056c8d1d9f7c` |
| V4閉鎖Evidence | `records/development/2026-08-05-historical-todo-issue-intake-v4-closure-evidence-v1.md` | `b942a9d17ea4c2818c6adb5f3ceabc0063f9b447c7ddb88ccc5baf3d1302d60e` |
| 隣接Issue | `.reviewcompass/workflow/issues-v4/issue-htc-66c3e6ca--v1.json` | `56e0911d6f565915ca0ad7737eae7befbb30d686d344eb5367ecc95598a8c732` |

## 提案した最小縦切り案

3案を比較した。

| 案 | 範囲 | 閉じる観測 | 大きさ |
| --- | --- | --- | --- |
| 案A | 最小のoperation spec ＋ Git preflight ＋ receipt | `HTC-C9F6C917` | 小 |
| 案B | 最小のoperation spec ＋ 構造化argv executor ＋ cache root固定 ＋ receipt | `HTC-186E9B83`、`HTC-9DCE8503`、`HTC-477EA1A4` | 中 |
| 案C | spec ＋ executor ＋ preflight ＋ cache root ＋ post-write検証を一括 | 上記4件 | 大 |

**推奨は案A**とし、理由を4点記した。主候補`HTC-C9F6C917`が記録している恒久対策そのものと一致すること、
開発方針が権限を`high` riskに分類していること、権限だけは正しい振る舞いが「やり直す」ではなく
「実行する前に止めて要求する」であり汎用executorより先にこの境界を固定すべきこと、範囲が小さいこと
である。案Bを次の縦切り、案Cを統合として位置づけた。**推奨は提案であり、Humanが承認するまで
確定しない**旨を明記した。

5観測の対応表では、`HTC-A5D1BCCA`（tool呼出のJavaScript構文）を**project内では解けないhost側の
入力境界**として明示し、「5件すべてをproject内で閉じる」と書かない境界を提案自体に固定した。
sandboxの承認を迂回・無効化しないこと、Git metadata書込みは最初の実行前に必要権限を宣言・要求して
止まるだけであることも§1に明記した。

受入条件は6件（Git分類の誤りなし、権限は実行前に停止・要求、特殊文字がshell解釈へ流れない、
cache rootが成果物や外部rootを汚さない、specとreceiptのidentity一致、host側をproject runnerで
解決したと誤報しない）を、正常例・負例・境界例と検証手段（Test、fault injection、独立確認）付きで
提案した。**実際のTestは作っていない。**

## Human判断が必要な点（提案§6）

1. 最初の縦切りをどれにするか（案A推奨／案B／案C）
2. project内runnerの責任範囲。既存policy runnerと統合するか分けるか
3. host側操作（`HTC-A5D1BCCA`）の扱い
4. 既存の直接shell／Git操作の移行順。新規分だけか、既存分も置換するか
5. `ISSUE-HTC-66C3E6CA`とのreceipt責務の寄せ先
6. 実装に着手してよいか。着手する場合のTest先行の作業単位の切り方

## 全test結果

指示のとおりpolicy runnerで実行した。

- receipt：`records/development/2026-08-05-machine-operation-routing-issue-plan-proposal-test-receipt-v1.json`
- status：`passed`、exit code：`0`、結果：`815 passed`
- command：`.venv/bin/python3 -m pytest -q`（policy runner内部）、Python 3.9.6、pytest 8.4.2、fallback false

TODO更新後にも全testを再実行し、`815 passed`を確認した。TODOの参照digest31件はすべて一致し、
commit安定Git節も合格。10,291 bytesで上限内。active ID projectionは`ISSUE-PILOT-TODO-GROWTH-001`の
1件のままである。

## TODO更新

現在位置だけを更新した。`ISSUE-HTC-C9F6C917`が`registered`かつnonblockingであること、そのPlan提案が
Human承認待ちで正式Planではないことを示した。次の一作業を「Plan提案に対するHuman判断」とし、
判断項目（最初の縦切り、runnerの責任範囲、host側操作の扱い、既存直接操作の移行順、実装着手可否）を
並べた。Plan提案と今回のreceiptへのlink・digestを追加し、前回のreceipt linkを差し替えた。

## 未実施事項（指示どおり行っていないこと）

- 正式Plan、Decision、Task Contract、code、test、config、policyの作成・変更：行っていない。
- Git／shell／Python cacheの自動化の実装、RED testの作成：行っていない。
- 3 Issueのstate変更：行っていない。3件とも`registered`のままで、file digestも変更前と同一
  （`66cfe50c…`、`a4a1511e…`、`56e0911d…`）。active Issueは0件である。
- 既存3 Issue、41 decision、候補bundle、V4承認・閉鎖recordの変更：行っていない。
  候補bundleのSHA-256は`e01c0feb…79a3e`のまま、有効decisionは41件のままである。
- 権限昇格、外部操作、push、PR、外部送信、hook、watcher、scheduler、background service：
  開始していない。
- 本完了報告はcommitに混ぜていない。
