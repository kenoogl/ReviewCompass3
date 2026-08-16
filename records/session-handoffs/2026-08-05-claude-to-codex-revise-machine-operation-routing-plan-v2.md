# Claude → Codex：機械操作routing Plan提案 v2 の作成 完了報告

指示：`records/session-handoffs/2026-08-05-codex-to-claude-revise-machine-operation-routing-plan-v2.md`

指示どおり、v2提案、test receipt、TODOだけを作成し、一つの意味単位commitとして確定した。

## commit

- commit SHA：`8777799e45c0cdc5aeb86ca3a93f5c9358a249e9`
- message：`Revise machine operation routing plan proposal`
- 3 file、283行追加・9行削除
- stageは`docs/design/2026-08-05-machine-operation-routing-issue-plan-proposal-v2.md`、
  `TODO_NEXT_SESSION.md`、
  `records/development/2026-08-05-machine-operation-routing-plan-v2-proposal-test-receipt-v1.json`
  の3 pathだけを明示列挙した。`git add -A`と`git add .`は使っていない。
- commit後のread-only確認：`git status --short`は空。
  `python3 tools/development/work_unit_transition.py --work-status completed`は
  `{"findings": [], "next_work_allowed": true, "reminder": null, "status": "passed"}`

## v2提案のpathとDigest

| 種別 | path | SHA-256 |
| --- | --- | --- |
| v2提案 | `docs/design/2026-08-05-machine-operation-routing-issue-plan-proposal-v2.md` | `57f5b98d4f54138c37aa780da00fc6a2bb288a3760ab7bf548ade9156afbc5b0` |
| v1提案（superseded、履歴） | `docs/design/2026-08-05-machine-operation-routing-issue-plan-proposal.md` | `722e9448971bcf3e97423ab1b9b137ca202f1f1c0ed7afdd92a619738e608bfa` |
| test receipt | `records/development/2026-08-05-machine-operation-routing-plan-v2-proposal-test-receipt-v1.json` | `7b81f927915292d67f5eaf99a5f47096733f10959ffa8aafeabf5b01f56d2d8f` |

v2提案の状態は`awaiting_human_approval`であり、冒頭に「正式なPlan、Decision、Task Contractではない」
「承認までrunner、executor、preflight、cache routing、config、policy evaluator、Test code、
Issueのstate、Task Contractを変更しない」と明記した。

旧v1提案は上書き・削除・状態変更をしていない。file digestは作成時と同一で、状態も
`awaiting_human_approval`のままである。v2の固定入力表に「superseded proposal」として記載した。

## v2で改訂した点

- 固定入力を機械再取得し、対象Issue、主triage decision、関連4 decision、開発方針、
  `DEC-SEMANTIC-COMMIT-MINIMAL-GUARDS-001`、V4承認Decision、V4閉鎖Evidence、隣接Issue、
  旧提案の12件を現在のSHA-256で表にした。作成後に再読込し、12件すべての一致と、
  本文で挙げた13 pathの存在を機械確認した（不一致0、欠落0）。
- 権限の扱いを改めた。v1の「書込みのたびに止めて要求する」を、
  「作業単位の開始前に機械がinventory全体を一度走査し、必要な権限種別を一回で出す。
  未取得なら最初の書込みを一度も試さず停止し、hostへ一回だけ要求を渡す。取得済みならそのまま続行する」
  に変えた。
- 通常commitは最小4条件を満たせばHuman個別承認を要さないことを明記し、あわせて
  「これはsandboxの権限承認を自動化・迂回する意味ではない」ことを明記した。
- host側のJavaScript tool構文、外部toolのAPI schema、sandbox承認の決定はproject内では解けないと
  明記し、`HTC-A5D1BCCA`を解決済みと書かない境界を提案自体に残した。

### v2の最小縦切り（3部）

1. **versioned operation inventory**：操作を`read_only`／`project_artifact_write`／
   `git_metadata_write`／`external`／`unknown`に分類する。`unknown`はfail-closed。
2. **permission preflight**：実行前にinventory全体を走査し、必要な権限種別を一回で出す。
   未取得なら書込みを一度も試さず停止し、hostへ一回の承認要求を渡す。
3. **execution receipt**：inventory、preflight verdict、実行結果を結ぶ。

### 最初に含めないもの

構造化argv executor、shell特殊文字対策の全面移行、cache root固定、既存直接shell操作の一括置換、
host側tool構文の解決、外部送信、`ISSUE-HTC-66C3E6CA`の定型record生成。

### 受入条件

6件を正常例・負例・境界例と検証手段付きで示した。分類の誤りと`unknown`のfail-closed、
最初のwrite前に全必要権限を一回で列挙すること、権限未取得ならexecutorが一度も呼ばれないこと、
最小4条件を満たす通常commitがHuman個別承認を待たないこと、inventoryとreceiptのidentity一致、
host側の問題を解決済みと誤報しないことである。**実際のTestは作っていない。**

## Human判断（3点）

1. v2の最小縦切り（inventory＋preflight＋receiptの3部）を承認するか。
2. project内runnerを、既存のpolicy runnerと分けるか、統合するか。
3. 取得済み権限の確認をhost側へどう渡すか。project内は必要な権限種別を出すだけとし、
   取得済み判定と承認はhost側に置く前提でよいか。

既存直接操作の移行順、argv executor、cache rootは後続の個別Planで決めるため、判断項目に入れていない。

## 検証結果

| 対象 | 結果 |
| --- | --- |
| 公式runner全test | `829 passed`（exit 0） |
| TODO validator `python3 tools/development/todo_handoff.py TODO_NEXT_SESSION.md` | `{"findings": [], "status": "passed"}`（TODO更新後と最終stage前の2回とも合格） |
| `git diff --check` | 合格（stage前後とも） |
| 新旧提案・TODOの参照Digest再計算 | 不一致0件 |

## TODO更新

共通手順で現在位置だけを更新した。v2提案がHuman判断待ちで旧提案は履歴であること、次の一作業が
v2最小縦切りに関する3点のHuman判断であることを記載し、v2提案・旧提案・今回のtest receipt・
semantic commit Decisionの実SHA-256を機械取得して記録した。receipt linkは今回のものへ差し替えた。

## 変更していないこと

- 実装：operation runner、argv executor、Git preflight、cache routingのいずれも作っていない。
- `config/development-policy.json`、policy evaluator、Test codeは変更していない。
  今回のcommitに含まれるのはv2提案、TODO、receiptの3 fileだけである。
- Issueのstate：V4 Issue 3件はいずれも`registered`のままで、file digestも変わっていない
  （`a4a1511e6090…`、`66cfe50ce791…`、`56e0911d6f56…`）。active Issueは0件。
- Task Contract、既存Decision、既存Evidence、旧v1提案：変更していない。
- push、tag、amend、rebase、reset、force push、外部送信：行っていない。
- 本完了報告はcommitに含めていない（`.gitignore`により無視される）。
