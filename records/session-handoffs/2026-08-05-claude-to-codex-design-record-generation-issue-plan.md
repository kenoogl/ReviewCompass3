# Claude → Codex：定型記録生成 IssueのPlan提案作成 完了報告

指示：`records/session-handoffs/2026-08-05-codex-to-claude-design-record-generation-issue-plan.md`

Human承認待ちのPlan提案、検証receipt、TODO更新だけを作成し、一つのcommitとして確定した。

## commit

- commit SHA：`35c210e690ee25670a3cd17846ff70bcd10f9b7e`
- message：`Propose a plan for the record generation issue`
- 3 file（提案、TODO、receipt）
- stageは対象3 pathだけを明示列挙した。`git add -A`と`git add .`は使っていない。
- commit後のread-only確認：`git status --short`は空。
  `python3 tools/development/work_unit_transition.py --work-status completed`は
  `{"findings": [], "next_work_allowed": true, "reminder": null, "status": "passed"}`

## 提案のpathとDigest

| 種別 | path | SHA-256 |
| --- | --- | --- |
| Plan提案 | `docs/design/2026-08-05-record-generation-issue-plan-proposal.md` | `746576704f683dba27ce832d64f4a1ad510de211b30f145c9c513ae836d9082d` |
| 全test receipt | `records/development/2026-08-05-record-generation-issue-plan-proposal-test-receipt-v1.json` | `d2320449185d783860312a3cc4b5b232a60d861bf5bf123f4794aaefc9927b92` |

状態は`awaiting_human_approval`であり、冒頭に「正式なPlan、Decision、Task Contractではない」
「承認まで定型記録生成、TODO renderer、receipt parser、監査集計を実装しない」
「RED testも作らない」「既存recordの書換え、Git操作、外部送信も行わない」
「`ISSUE-HTC-66C3E6CA`のstateは`registered`のまま」と明記した。

### 固定入力（作成時の実値で固定し、作成後に機械再計算で照合）

対象Issue、Human triage decision、現行TODO手順、TODO renderer、TODO validator、公式Test receipt生成器、
TODO圧縮validatorの7件をpathとSHA-256で固定した。作成後に再読込し、7件のdigest行と本文で挙げた
8 pathの存在を機械確認した（不一致0、欠落0）。

直近の実例として、TODOの全Test件数が`829 passed`のまま残り実績`852 passed`へ訂正されたこと
（commit `815456e`）を、本Issueが扱う型の代表例として記録した。

## 比較した最小縦切り案と推奨

| 案 | 範囲 |
| --- | --- |
| **案A（推奨）** | TODOだけを対象にし、既存の公式Test receiptと参照fileから構造化projectionを組み立て、既存rendererでTODO本文を描画・検証する |
| 案B | TODOに加えEvidence／Decisionの定型欄にも同時に一般化する |

**推奨は案A**であり、理由は3点である。実際の手戻りがTODOで起きていて最短で再発防止に効くこと、
既存の`todo_handoff_projection.py`と各validatorが既にあり新規範囲を「値を集める部分」に絞れること、
TODOが非権威のprojectionで間違えたときの影響が権威recordより小さいことである。
推奨はHuman承認まで確定しない旨も明記した。

案Bへ進むために先に満たしておく境界（共通入力model、version、record種別ごとのrenderer、
authorityを勝手に変更しない規則）を挙げたうえで、**汎用frameworkを先行実装する提案にはしていない**。

提案の中で明らかにした重要な事実として、`todo_handoff_projection.py`は既にTODO本文を決定的に
描画できるが、現在のTODOはこのrendererを通していないこと、足りないのはrendererへ渡す
**projectionの中身を正本から機械で集める経路**であることを整理した。

また、pytestのstdoutから件数を正規表現で拾う方式は代替案として比較したうえで、
**初期実装の正本には採用しない**と明記した（選択肢A＝receiptへ件数の構造化fieldを追加、
選択肢B＝stdout解析、選択肢C＝件数を出さない、の3案を比較。推奨はAだが
`policy_test_runner`の変更は承認範囲外のためHuman判断項目へ回した）。

## Human判断が必要な点（5点）

1. 最初の対象を案A（TODOだけ）に限定してよいか。
2. 何を「公式Test receipt」として受け付けるか（件数の構造化fieldを追加するか、当面出さないか）。
3. 生成済みTODOの更新をどのcommitへ含めるか。
4. 将来Evidence／Decisionへ拡張する条件。
5. 実装に着手してよいか。着手する場合のTest先行の作業単位の切り方。

## 全test結果

公式runnerで実行した。

- receipt：`records/development/2026-08-05-record-generation-issue-plan-proposal-test-receipt-v1.json`
- status：`passed`、exit code：`0`、結果：**`852 passed`**
- command：`.venv/bin/python3 -m pytest -q`（policy runner内部）、Python 3.9.6、pytest 8.4.2、fallback false

TODO更新後にも全testを再実行し`852 passed`を確認した。TODO validatorは更新後と最終stage前の2回とも
`{"findings": [], "status": "passed"}`。TODOの参照digestに不一致0件、12,258 bytesで上限内。
`git diff --check`はstage前後とも合格した。

## TODO更新

現在位置だけを更新した。`ISSUE-HTC-66C3E6CA`が`registered`かつnonblockingで、Plan提案がHuman承認待ちで
あることを示し、次の一作業をそのPlan提案に対するHuman判断（上記5点）とした。提案と今回のreceiptへの
link・digestを追加し、前回のreceipt linkを差し替えた。

## 未実施事項（指示どおり行っていないこと）

- 正式Plan、Decision、Task Contract、code、test、config、policyの作成・変更：行っていない。
- 定型記録生成、TODO renderer、receipt parser、監査集計の実装：行っていない。RED testも作っていない。
- 既存TODO以外の既存Evidence、Decision、Issue、receiptの変更：行っていない。
  今回のcommitに含まれるのは新規提案、TODO、新規receiptの3 fileだけである。
- 3 Issueのstate変更：行っていない。`ISSUE-HTC-66C3E6CA`、`ISSUE-HTC-BEB5E0BD`、`ISSUE-HTC-C9F6C917`は
  いずれも`registered`のままで、file digestも変わっていない
  （`56e0911d6f56…`、`a4a1511e6090…`、`66cfe50ce791…`）。
- push、PR、外部送信、hook、watcher、scheduler、background service：開始していない。
- 本完了報告はcommitに含めていない（`.gitignore`により無視される）。
