# Codex → Claude：機械操作routing v2 最小縦切りの実装指示

## 誰が何をするか

- **Human**は、次の3点をすべて承認した。① operation inventory・permission preflight・execution receiptの最小縦切り、② project内runnerを既存policy runnerから分離すること、③ project内は必要な権限種別を出し、承認と取得済み確認はhost側に置くこと。
- **Codex**は、承認範囲と実装の停止境界をここに固定する。
- **Claude**は、承認記録、TDD、独立runner、Evidence、Plan／checklist／TODO更新を一つの意味単位として実装・検証・commitする。

## 承認の効力と非対象

承認対象は`docs/design/2026-08-05-machine-operation-routing-issue-plan-proposal-v2.md`の§3だけである。

実装してよいもの：

1. versioned operation inventory
2. permission preflight
3. execution receipt

実装してはならないもの：

- shellを実行する汎用argv executor、`shell=True`相当、既存直接shell操作の置換
- cache root固定
- Gitへの実書込み、push、tag、外部送信、host／sandbox権限の取得・迂回・自動承認
- Codex hostのJavaScript tool構文、外部tool API schemaへの対応
- `ISSUE-HTC-66C3E6CA`が扱うEvidence／TODO定型欄生成
- V4 Issue recordのstate変更、正式製品schema／UI／automation、Task Contractの新規作成

`ISSUE-HTC-C9F6C917`は、V4の限定scope内で正式implementation lifecycleをまだ持たないため、Issue recordは`registered`のままにする。今回の実装許可はHuman Decisionにだけ記録する。

## 1. 承認記録とPlan状態

### 作成するDecision

次を新規作成する。

`records/development/2026-08-05-machine-operation-routing-v2-approval-decision-v1.md`

- decision ID：`DEC-MACHINE-OPERATION-ROUTING-001`
- Humanが上記3点を承認したことを記録する。
- v2提案、対象Issue、関連triage decision、semantic commit Decisionを実Digestで固定する。
- runnerはpolicy runnerと別moduleであり、hostが権限を承認・確認すること、project側は必要種別を計算するだけであることを明記する。
- §3以外は承認していないことを列挙する。

### Plan proposalの状態更新

`docs/design/2026-08-05-machine-operation-routing-issue-plan-proposal-v2.md`の状態を
`approved_for_development_implementation`へ更新する。冒頭に短い注記を追加し、承認範囲が§3だけであること、
正式Issue Resolution Plan／Task Contractへ昇格していないこと、Issue stateを変更しないことを明記する。
提案時点の本文は歴史として残し、全面的な時制書換えをしない。

## 2. テスト先行（RED）

新規testを先に作る。

`tests/test_operation_routing_v2.py`

新規moduleの正本は次とする。

`tools/development/operation_routing.py`

以下を正常・負例・境界例で固定する。

1. versioned inventoryは、operation ID、version、分類、必要権限、content digestを持つ。正規のJSON以外、未知field、重複operation ID、空ID、不正Digestを拒否する。
2. 分類は`read_only`、`project_artifact_write`、`git_metadata_write`、`external`、`unknown`だけを受理する。`unknown`はfail-closedとなる。
3. preflightはinventory全体から必要権限を重複なく一回で得る。read-onlyだけなら必要権限は空である。
4. hostが渡した取得済み権限が足りなければ`approval_required`となり、実行callbackを一度も呼ばない。必要権限を一回の集合で返す。
5. 取得済み権限がそろうときだけcallbackを実行できる。ここでのhost入力は**host attestation**であり、project内がsandbox権限を検査または付与したとは扱わない。
6. `external`は今回のrunnerで実行を許可しない。host attestationがあっても`external_operation_not_supported`で停止する。
7. inventoryとpreflight verdict／execution resultを結ぶreceiptを作る。inventory ID・version・Digestが違うreceipt、preflight未通過のexecution receipt、未知fieldを拒否する。
8. `git add`／`git commit`相当は`git_metadata_write`、`git status`／`git diff --check`相当は`read_only`としてfixtureで示す。ただしこのmoduleはGit commandを実行しない。
9. project artifact writeとGit metadata writeが混在しても、必要権限を最初に一回で返し、途中で追加要求しない。

REDを公式のpytestで確認する。RED testだけをcommitしない。実装中にtest期待を緩めない。

## 3. 実装（GREEN）

`tools/development/operation_routing.py`を、shell・subprocess・Git実行を一切含まない決定的libraryとして実装する。

- 入出力はJSON互換の構造だけとし、inventory／preflight／receiptそれぞれに厳密なfieldとSHA-256 canonical digestを持たせる。
- 権限種別は少なくとも`project_artifact_write`と`git_metadata_write`を分ける。`external`は実行不能として拒否し、`unknown`も拒否する。
- host attestationはcallerが渡す入力であり、moduleがOS／sandbox／Codexの権限を確認または変更しない。
- preflightが`approval_required`または停止なら、callbackを一度も呼ばない。
- receiptはcallbackの返値を恣意的な文章へ変換せず、inventoryとpreflight verdictのidentityを結ぶ構造化結果にする。
- policy runnerへimport依存を作らない。既存policy runner、Git helper、TODO helper、Task Contract resolverを変更しない。

必要なら最小CLIを付けてもよいが、inventoryを読む／preflightを出すだけに限る。Gitやshellを実行するCLIにしない。

## 4. Evidence・Plan・checklist・TODO

次を更新する。

1. GREEN Evidence：

   `records/development/2026-08-05-machine-operation-routing-v2-green-evidence-v1.md`

   RED結果、GREEN結果、module／test、Decision、v2提案、対象外、host境界、受入条件1〜9の対応を記録する。

2. `docs/current/reviewcompass3-plan-current.md`：Inter-workのIssue Resolution行を、C9の§3最小縦切りがHuman承認済み・実装済みであることを短く追記する。未完了境界にはargv executor、cache root、既存操作移行、host構文、正式製品schema／UI／automationを残す。

3. `docs/development/2026-08-03-initial-development-checklist.md`：Issue Resolution早期Pilotの限定拡張節に、C9最小縦切りのDecisionとGREEN Evidenceを追記する。V4 Issueの正式Plan化・実装一般を完了と誤記しない。

4. `TODO_NEXT_SESSION.md`：共通手順に従う。C9の§3だけ実装済み、後続のargv executor／cache root／既存操作移行は未実施、C9全体をclosedにしていないことを示す。Decision、v2提案、GREEN Evidence、公式test receiptの実Digestを機械取得して参照する。

## 5. 検証とcommit

1. `git diff --check`
2. 新規moduleのtestがREDで失敗することを確認する。
3. GREEN後に、新規test・関連testを実行する。
4. fault injectionとして、`unknown`、権限不足、external、receipt identity不一致で停止しcallbackが未実行であることを確認する。
5. TODO validator：

   `python3 tools/development/todo_handoff.py TODO_NEXT_SESSION.md`

6. 公式全testを実行し、receiptを次へ作る。

   `records/development/2026-08-05-machine-operation-routing-v2-green-test-receipt-v1.json`

   ```text
   .venv/bin/python3 -m tools.development.policy_test_runner --suite full \
     --receipt records/development/2026-08-05-machine-operation-routing-v2-green-test-receipt-v1.json
   ```

7. 最終stage前にTODO validatorと`git diff --check`を再実行する。stageは今回作成・更新したpathだけを明示列挙し、`git add -A`と`git add .`を使わない。
8. 一つのGREEN意味単位commitを作る。messageは`Implement operation routing v2 minimum slice`とする。
9. commit後に`git status --short`と`python3 tools/development/work_unit_transition.py --work-status completed`をread-onlyで確認する。

push、tag、amend、rebase、reset、force push、外部送信はしない。

## Claudeの完了報告

commitに混ぜず、次をローカルに作る。Git ignore済みのためstageしない。

`records/session-handoffs/2026-08-05-claude-to-codex-implement-machine-operation-routing-v2-slice.md`

報告にはcommit SHA、RED／GREEN数、fault injection結果、Decision／Evidence path、host境界、変更しなかった対象を記す。
