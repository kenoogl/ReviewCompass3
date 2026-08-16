# Claude → Codex：正本・履歴・検証手順9候補のHuman triage記録 完了報告

指示：`records/session-handoffs/2026-08-05-codex-to-claude-triage-authority-history-and-procedure.md`

指示の実施範囲をすべて完了した。作成したのは9件のdecision record、test receipt、TODO更新だけである。
新しい正式Issue、Plan、Workは作成していない。この作業により、過去TODO候補41件のHuman triageが完了した。

## commit

- commit SHA：`7af4cd58513f018e491a564790003f61c895ea53`
- 内容：decision record 9件、TODO更新、作成後の全test receipt 1件（計11file、314行追加・7行削除）
- `git diff --check`：stage前後とも合格
- commit後の追跡fileのworktree：clean（未追跡のまま残るのは、commitへ混ぜないsession-handoffsの
  完了報告12件のみ。本報告を含む）

## 9 decision ID

保存先：`.reviewcompass/workflow/triage-decisions-v4/`、schema version 2、`decision_version: 1`、
`decided_at: 2026-08-05T14:25:12+09:00`（9件共通）。

9件とも指示どおり次の値である（機械確認済み）。

- `unresolved: false`、`recurrence: false`、`impact: not_applicable`、`priority: not_applicable`、
  `promote_to_issue: false`
- `disposition: reject`、`blocking: false`
- `issue_promotion: {"approved": false, "issue_id": null}`
- `supersedes: null`

### 現行の正本と履歴保持（7件）

| decision ID | candidate ID | file SHA-256 | content digest |
| --- | --- | --- | --- |
| `DEC-HTC-C05BE65C` | `HTC-C05BE65C` | `0aa55a118cbc2aaed1257ac545c869690525fbe44692ee200c56805666707ebf` | `11399cae191e5f4c0fb5211ed4cb9db32d07cbab5fdacfa352b5941e804bfa8a` |
| `DEC-HTC-C3193ABF` | `HTC-C3193ABF` | `a4d23319b4d2820fad76bcea3844f6b36c74526c802efa1cefc7061af90c19d5` | `23a169f0e2396580ab30d93185128b7b522f4f075acd95e65e9054e8265f8810` |
| `DEC-HTC-ECE89CA2` | `HTC-ECE89CA2` | `65407685f051bd9a8544be62d5c7aff4689fe9fbfac6abdb9b1d29e04ba1acf6` | `cb81b8c8b3d657eb2bba04d1030527fffb04afdc35b93e7be8a4e4709a809de7` |
| `DEC-HTC-49795CC0` | `HTC-49795CC0` | `54464f901b101e75f69f31107a756cabb21792106bdebf229f3c6f72ca23cd61` | `ca27a74546724bf58be71d956a86e4ce584d7da3457a073d643f3524b873b0b4` |
| `DEC-HTC-094589CA` | `HTC-094589CA` | `a2cb341e0aec3ac92d51d7e62bda70fb9ddd506be2bc8f0bdcf9442704065881` | `c3929a5ea35fe7a58b84b26e690ff4574fc4c4cda21151c1fa3e8363285c5efb` |
| `DEC-HTC-876989C2` | `HTC-876989C2` | `5cbb32ff1567134d5248822ce50f3271cf3de9ad200aee6c420bf19c958a8dc4` | `ee49d46fedae9b7d427afe83ebf62eeca43bb13beb2b6acb767aa25e3d97c08c` |
| `DEC-HTC-ABE70CFC` | `HTC-ABE70CFC` | `68d2ba601462332da8a82e2373d695445bb5dff18fd808fff525a79070d1ba1b` | `b45e48bfa40b1abdf6b255aba2e2dc6178c63338427608435be6db887d15bacc` |

### 検証と報告の現行手順（2件）

| decision ID | candidate ID | file SHA-256 | content digest |
| --- | --- | --- | --- |
| `DEC-HTC-7071DD99` | `HTC-7071DD99` | `d2dfcede969732f35b25b700a4cb82344d26a45e7cbf034a2e124d2a16294587` | `e45cbfba59a0cc4707fc5d03a18bd7f74d4b16efc6fd5d9fe25ee6fa7c846c4e` |
| `DEC-HTC-62719E1C` | `HTC-62719E1C` | `5b4f09f9a85d67795839860347fecdc65380f8ff043f19782b34735ddf35479b` | `bf177ed327cb8d12b89c1b8a92ebd255fa01fd88f02412787c6efc5d63957889` |

`rationale`には、候補ごとに何が現行の取り決めなのかを平易に記した。digest-only履歴の保持とGitからの
再構築、候補fileを第二正本にしないこと、旧sessionと旧候補のDigestを証拠として保持しつつ判断関門には
使わないこと、coverage matrixとidentity／配置規則の正本が外部Decisionと承認対象Digestであること、
CI adapter・Build Artifact実装・provider操作が対象外であること、現行の権威が50 definitionで旧版を
superseded履歴として保持すること、公式Testはpolicy runnerが起動しreceiptを機械生成すること、
作業後報告に因果・期待／実executor・Evidence・機械処理候補・routeを含めることである。

あわせて9件とも、次の趣旨を明記した。

> ここでの`reject`は、正本の規則、履歴、検証手順を捨てるという意味ではない。これは現在も守られている
> 取り決めの説明であり、この候補を独立したIssueとしては追跡しない、という意味である。
> 元のPlan、Decision、Evidence、code、test、configは変更しない。

## 候補bundle不変確認

- SHA-256は`e01c0feb082712f8ef0f77bfa4f031fbdc4530ed51f331f7dafbfd133d479a3e`のまま変わらない。
  bundleのpathとschema version（1）も既存V4 decisionと同じ値を使っている。
- 候補41件すべての`human_fields`は`null`のままである。
- Git履歴上、bundle fileを変更したcommitは生成時の`3ef8759`だけである。

## V4 Issue数とactive Issue数

- V4 Issueは3件：`ISSUE-HTC-BEB5E0BD`、`ISSUE-HTC-C9F6C917`、`ISSUE-HTC-66C3E6CA`。
  いずれも`state: registered`、参照decisionは`blocking: false`。
- active Issue数は0。
- 既存3 Issueは変更していない。file SHA-256は`a4a1511e60900519…`、`66cfe50ce79136bc…`、
  `56e0911d6f565915…`で前回と同一であり、`.reviewcompass/workflow/issues-v4/`の最新commitは
  `c6edcad`のままである。新しい正式Issueは作っていない。
- decision集合検証は有効decision 41件で競合なし。V4 decision directoryのfile数も41件で一致する。
  候補bundleの41候補のうち、判断recordが無いものは0件である。

## 全test結果

公式Test runner（`tools/development/policy_test_runner.py`、suite `full`。実コマンドは
`.venv/bin/python3 -m pytest -q`、Python 3.9.6、pytest 8.4.2、fallback false）で実行した。

- receipt：`records/development/2026-08-05-triage-authority-history-and-procedure-test-receipt-v1.json`
  （SHA-256 `b817a25ceab21bfc4987d8aec42d2e18fff014225fbb291e9a12805f4307af34`）
- status：`passed`、exit code：`0`、結果：`815 passed`

TODOの最終更新後にも全testを再実行し、`815 passed`を確認した（このrunはreceiptを上書きしないため、
receiptは上記1件のままである）。TODOの参照digest28件はすべて一致し、commit安定Git節も合格。
9,216 bytesで上限内。active ID projectionは`ISSUE-PILOT-TODO-GROWTH-001`の1件のままである。

## TODO更新

現在位置だけを更新した。過去TODO候補41件のHuman triageは完了し未判断0件であること、正式Issue3件、
active Issue 0件、3 Issueはいずれも`registered`かつnonblockingであることを記載した。
次の一作業は「3正式IssueのPlan化順序、またはIssue Intake V4 Pilotを閉じるかのHuman判断」とした。
全test receiptへのlinkとdigestも今回のものへ差し替えた。詳細は再累積していない。

## 未実施事項（指示どおり行っていないこと）

- IssueのPlan化、Issue Intake V4 Pilotの閉鎖、実装、既存文書の一括書換え：行っていない。
- 既存32 decision、既存3 Issue、候補bundle、Plan、Decision、Evidence、code、test、configの変更：
  行っていない。今回のcommitに含まれるのはdecision record 9件、TODO、receiptだけである。
- push、PR、外部送信、Work 4B、Work 6A、E2以降：開始していない。
- 本完了報告はcommitに混ぜていない。
