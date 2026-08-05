# Codex → Claude：読み取り専用argv executor最小sliceの実装指示

## Humanが承認した範囲

**Humanは、`ISSUE-HTC-C9F6C917`の後続Planのうち、読み取り専用の構造化argv executor最小sliceだけを承認した。**

承認したのは次である。

- shell文字列を使わず、argv配列のまま読み取り専用操作を起動する経路。
- 最初に扱う実行templateは`git status --porcelain`だけ。`--`の後ろにpathspecを0個以上置ける。
- `operation_routing.py`のinventory／preflight／receiptをそのまま利用する。executorは新たな権限判定・付与・再分類をしない。
- cache rootは次の別sliceに分ける。
- Git metadata書込み、project成果物書込み、external操作、host側tool構文、外部送信、既存直接操作の移行は対象外のままにする。

これは後続Plan全体の承認ではない。上記以外のHuman判断点は未承認のままである。

## 誰が何をするか

- **Human**は、この最小sliceの実装範囲を上記のとおり承認した。
- **Codex**は、承認範囲、受入条件、停止境界をこの指示へ固定する。
- **Claude**は、DecisionとPlan状態注記を先に確定し、TDDでRED→GREENの実装・検証・記録を行う。

## 参照する正本

- 後続Plan提案：`docs/design/2026-08-05-machine-operation-routing-follow-on-plan-proposal.md`
- 最小縦切りの既存設計：`docs/design/2026-08-05-machine-operation-routing-issue-plan-proposal-v2.md`
- 既存承認：`records/development/2026-08-05-machine-operation-routing-v2-approval-decision-v1.md`
- receipt整合性の訂正：`records/development/2026-08-05-machine-operation-routing-v2-receipt-integrity-correction-decision-v1.md`
- 既存module：`tools/development/operation_routing.py`
- 対象Issue：`.reviewcompass/workflow/issues-v4/issue-htc-c9f6c917--v1.json`

## 作業単位1：承認を記録する（codeは変更しない）

1. 次を新規作成する。

   `records/development/2026-08-05-machine-operation-routing-read-only-argv-approval-decision-v1.md`

   Decision IDは`DEC-MACHINE-OPERATION-ROUTING-READ-ONLY-ARGV-001`とする。
   Humanの上記承認文言、承認範囲、対象外、参照入力のpathと作成時SHA-256を記録する。

2. 後続Plan提案へ「実施状態注記」を追記する。
   - 全体は`awaiting_human_approval`のままである（cache root、移行、host境界を含むPlan全体は未承認）。
   - `DEC-MACHINE-OPERATION-ROUTING-READ-ONLY-ARGV-001`により、§2.1と§3.2のargv executor最小sliceだけが実装承認済みである。
   - `git status --porcelain` template、`read_only`のみ、cache root・移行・書込み・externalは対象外、と明記する。

3. 公式policy runnerで全Testを実行し、次のreceiptを作成する。

   `records/development/2026-08-05-machine-operation-routing-read-only-argv-approval-test-receipt-v1.json`

4. TODOを共通手順で更新する。Decision記録、Plan状態、approval test receiptを最新authority／Evidenceへ追加し、機械計測の参照数を更新する。

5. Decision、Plan注記、TODO、approval test receiptだけを明示pathでstageし、最初の意味的commitにする。code／testはこのcommitへ混ぜない。

## 作業単位2：RED testを固定する（実装は書かない）

次を新規作成する。

`tests/test_structured_argv_executor.py`

実装対象moduleはまだ作らない。このTestは、module不在または未実装で失敗しなければならない。

Testは実processを起動しない。runnerをfakeに差し替え、呼出し回数・受け取ったargv・cwdを観測する。
少なくとも次を固定する。

1. **正常例**：`read_only` inventoryの`git status --porcelain -- <pathspec>`が、listのままfake runnerへ一度だけ渡る。pathspecには空白、引用符、backtick、`$`、`*`、非ASCIIを含め、文字列が結合・展開・分割されないことを確認する。execution receiptは既存validatorで検証できる。
2. **template外の拒否**：`git status`以外のGit subcommand、`git`の前置option、`--`より前の余分なargument、`--`無しのpathspecを拒否し、runner呼出し数は0である。
3. **分類境界**：`project_artifact_write`、`git_metadata_write`、`external`、`unknown`を含むinventoryは拒否し、runnerを一度も呼ばない。
4. **argv境界**：空の実行file、非文字列要素、空文字列の先頭要素を拒否する。空文字列の**pathspec**は有効な引数としてそのまま渡してよい。
5. **cwd境界**：cwd入力はproject root基準の相対pathだけを受ける。絶対path、`..`を含むpath、project外へ解決されるpath、symlinkを拒否し、runnerを一度も呼ばない。`.`と実在する通常directoryは受ける。
6. **preflight境界**：既存`operation_routing`によるpreflightが`granted`でない場合、またはinventory／preflightのidentityが不一致の場合、runnerを一度も呼ばない。
7. **実行失敗**：fake runnerが失敗結果を返す場合も、結果をreceiptへ記録し、例外で隠さない。入力検証の失敗とprocess結果の失敗を混同しない。
8. source inspection Testで、executorが`subprocess`を使う場合にも`argv`をshell文字列へ連結せず、`shell=True`を使用しないことを固定する。

REDを実行して失敗を確認し、次を作成する。

`records/development/2026-08-05-machine-operation-routing-read-only-argv-red-evidence-v1.md`

RED testとEvidenceのみを第2の意味的commitにする。既存testを緩めたり変更したりしない。

## 作業単位3：GREEN実装（承認範囲を超えない）

次を新規作成する。

`tools/development/structured_argv_executor.py`

実装の要件：

- `operation_routing`のpublic APIを使用してinventoryとpreflight／receiptを検証・結合する。権限を独自に判定・付与・迂回しない。
- 起動可能なのは、inventory全操作が`read_only`で、かつ正確に`git status --porcelain`＋任意の`-- <pathspec...>` templateに一致する場合だけである。
- `argv`はlistのままrunnerへ渡す。shell文字列へのjoin、`shell=True`、`os.system`、`Popen(..., shell=True)`を使わない。
- runnerはテストで差替可能にする。実装が実process runnerを持つ場合も、受け取る`argv`配列と検証済みcwdだけを渡し、shellを使わない。
- cwdはproject rootから解決する相対pathだけとし、解決後もproject root内の実在する通常directoryであることを確認する。symlinkは拒否する。
- fail-closedの例外型と停止codeを明確にし、入力・template・cwd・分類・preflightのいずれの失敗でもrunnerを呼ばない。
- cache root設定、環境変数設定、既存call siteの置換、Git metadata書込み、project成果物書込み、external起動を追加しない。

GREEN後、次を作成する。

- `records/development/2026-08-05-machine-operation-routing-read-only-argv-green-evidence-v1.md`
- `records/development/2026-08-05-machine-operation-routing-read-only-argv-green-test-receipt-v1.json`

関連test、既存`tests/test_operation_routing_v2.py`、公式policy runnerの全Testを実行する。GREEN Evidenceには、実施内容・結果・判断・未実施を分け、command結果とreceiptを対応付ける。

GREEN実装、test、GREEN Evidence、GREEN receipt、TODO更新を第3の意味的commitにする。commit前に`git diff --check`、TODO validator、compaction validator、参照整合を実行する。commit後にread-only照合と`python3 tools/development/work_unit_transition.py --work-status completed`を実行する。

## 全作業単位に共通する禁止事項

- cache root、移行inventory、既存直接操作の置換、Git metadata書込み、project成果物書込み、external操作を実装しない。
- push、tag、amend、rebase、reset、force push、履歴書換え、外部送信、hook、watcher、schedulerを行わない。
- Issue recordのstate、Task Contract、policy、config、既存Decision、既存testを変更しない。
- host側tool構文、sandbox／host権限承認、外部tool APIをproject内で解決したと主張しない。
- 実装中の細部で止まらない。ただし、authority、safety、受入条件の矛盾、または承認範囲外の操作が必要になった場合は、継ぎ足さず停止して報告する。

## Claudeの完了報告

完了報告はGit管理外の次へ保存する。

`records/session-handoffs/2026-08-05-claude-to-codex-implement-read-only-argv-executor-slice.md`

各commit SHA、変更file、RED／GREEN結果、全Test結果、TODO validator結果、Decisionと未実施範囲を簡潔に報告する。
