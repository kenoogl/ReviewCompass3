# Codex → Claude：V4 Issue永続化と会話記録方針候補のtriage実装指示

## 誰が何をするか

- **Human**は、会話記録の保存・暗号化・自動化に関する4候補のtriageを承認した。
- **Human**は、`HTC-BEB5E0BD`を「高影響だが、現在のWorkを止めない非blockingの正式Issue」として
  登録することを承認した。
- **Codex**は、V4が正式Issueを永続保存するschemaとdirectoryを持たない不足を確認し、その根本対応を
  指示する。
- **Claude**は、V4 Issue永続化をTDDで実装し、承認済みの4候補を記録する。

## 解く問題

現行V4の`promote_candidate_from_decision()`はメモリ上のissue dictを返せるが、V4 Issueのfile path、
content digest、candidate／decision参照の再検証、repository集合検証を持たない。

旧PilotのIssue directory `.reviewcompass/workflow/issues/`には「旧Pilot subjectは1件だけ」という
検査がある。V4 Issueをそこへ置かず、旧Pilotを変更しない。

## 固定入力

- V4 config：`config/development-issue-resolution-pilot-v4.json`
- V4実装：`tools/development/issue_intake_v4.py`
- V4受入test：`tests/test_issue_intake_v4.py`
- 候補bundle：`records/development/2026-08-05-historical-todo-intake-candidates-v1.json`
  - SHA-256：`e01c0feb082712f8ef0f77bfa4f031fbdc4530ed51f331f7dafbfd133d479a3e`
- 既存V4 triage decision：`.reviewcompass/workflow/triage-decisions-v4/`
- 旧Pilot config、V1 decision、V1 Issue、旧test：変更しない。

## 実装要件

### 1. V4専用Issue directoryと永続schema

V4 configに、旧`issue_record`とは別のV4 Issue directoryを追加する。

- 推奨path：`.reviewcompass/workflow/issues-v4/`
- V4 Issue directoryと旧Issue directoryが同一なら、config validationはfail-closedで拒否する。
- V4 Issue recordは`schema_version: 2`とし、ID、version、path、content digestを検証する。
- file名は`issue_id`とversionから決定的に導出する。
- `candidate_ref`と`triage_decision_ref`は、bundle path／digest、candidate digest、decision path／digestを
  含めて再検証する。
- 未知field、path escape、digest不一致、参照decision不一致、同一candidateの有効Issue重複を拒否する。
- V4 Issue repository validatorを作る。V4 directoryだけを検証し、旧IssueをV4語彙で再判定しない。

V4 Issueの作成関数は、検証済みHuman triage decisionから決定的にrecordを作り、candidate bundleは
書き換えない。`in_progress`へは進めず、初期stateは`registered`とする。

### 2. TDD受入条件

実装前にtestを追加し、失敗を確認する。少なくとも次を固定する。

1. Human decisionから作ったV4 Issueを、決定的pathとcontent digestで保存・再読込・検証できる。
2. V4 Issue directoryと旧Issue directoryの混同を拒否する。
3. candidate bundle SHA、candidate digest、decision path、decision digestの改竄を拒否する。
4. Human decisionなし、`promote_to_issue: false`、`disposition`不一致、issue ID／path不一致、
   同candidateの有効Issue重複を拒否する。
5. 旧PilotのIssue directoryが1件のままで、旧testが通る。
6. V4 Issue repository集合検証と、全testが通る。

RED evidenceを作る。実装中にtestを緩めない。

### 3. 承認済み4候補のHuman triage

候補bundleを変更せず、V4 Human triage decisionを各一件作る。

| candidate ID | Human判断 |
| --- | --- |
| `HTC-045A8FB5` | 限定captureの保存場所を決めた完了記録。`unresolved: false`、`recurrence: false`、`impact: not_applicable`、`priority: not_applicable`、`promote_to_issue: false`、`disposition: historical_completed`、`blocking: false`。 |
| `HTC-4ED2C5B1` | 手動収集・照合は完了し、自動化は保存方針の決定まで実施しない。`unresolved: true`、`recurrence: true`、`impact: medium`、`priority: low`、`promote_to_issue: false`、`disposition: dependency`、`blocking: false`。next actionは下記正式Issueの方針決定後に再判定。 |
| `HTC-BEB5E0BD` | 生会話記録の保存期間・削除・暗号化・backup方針は未決定。`unresolved: true`、`recurrence: true`、`impact: high`、`priority: high`、`promote_to_issue: true`、`disposition: issue_resolution`、`blocking: false`。 |
| `HTC-CD984CD0` | 2026-09-03の保存期間見直し・暗号化・自動化有効化は、上記正式Issueのdecision inputとして扱う。`unresolved: true`、`recurrence: true`、`impact: high`、`priority: low`、`promote_to_issue: false`、`disposition: dependency`、`blocking: false`。next actionは2026-09-03または上記正式IssueのPlan作成時に再確認。 |

この値はHuman承認済みの「保存方針は未決定」「自動化は方針決定まで保留」「高影響だが現行Workは
nonblocking」という判断を構造化したもの。Claudeは他の候補の判断をしない。

### 4. 正式Issueの作成

`HTC-BEB5E0BD`の有効decisionだけから、V4 Issueを一件作る。

- issue ID：`ISSUE-HTC-BEB5E0BD`
- initial state：`registered`
- nonblocking：trueではなく、issue recordの状態・triage decisionの`blocking: false`で表す。
- 問題文：生会話記録の保存期間、削除、application-layer暗号化、backupの方針が未決定であること。
- 作るのはIssue recordだけ。Plan、Work、scheduler、hook、暗号化、backup、retention変更、実会話の追加captureは
  作らない。

### 5. TODOとEvidence

decisionとIssue recordの作成後、TODOは現在位置を次に置き換える。

- active Issueはなし。`ISSUE-HTC-BEB5E0BD`は`registered`であり、まだ作業開始していない。
- 次の一作業は、このIssueをPlan化するかどうかのHuman判断である。
- 他の候補は詳細をTODOへ再累積させない。
- V4 Issue／decision Evidenceと全test receiptへのlink／digestを更新する。

## コミット境界

1. RED testとEvidenceを作成し、REDを確認する。red-only commitは任意。
2. V4 Issue永続化のschema／config／validator／testを実装し、GREEN Evidenceと全test receiptを作る。
   **実装だけ**を一つのcommitにする。
3. 四decision、V4 Issue一件、TODO更新、作成後の全test receiptを作る。
   **Human承認recordとIssue recordだけ**を別commitにする。

次の作業単位へ進む前に、追跡fileのworktreeがcleanであることを確認する。

## 禁止事項

- 他の33候補の判断、Issue、Plan、Workを作成・変更しない。
- 旧Pilotのconfig、V1 decision、V1 Issue、旧testを変更しない。
- `HTC-BEB5E0BD`を`in_progress`へ移さない。
- push、PR、外部送信、scheduler／hook有効化、暗号化・backup・retentionの実装、実会話の追加capture、
  Work 4B、Work 6A、E2以降を開始しない。

## 完了報告

完了報告はcommitに混ぜず、次へ保存する。

`records/session-handoffs/2026-08-05-claude-to-codex-v4-issue-persistence-and-session-policy-triage.md`

報告には、commit SHA、RED／GREEN結果、四decision ID、V4 Issue path／digest、旧Issue不変確認、
候補bundle不変確認、全test結果、未実施事項を記す。
