# Codex → Claude：Issue Intake V4 Human triage永続化の実装指示

## 誰が何をするか

- **Human**は、候補`HTC-14D810C7`、`HTC-1AB699F7`、`HTC-21C3CE46`、`HTC-6ABDDC35`を、
  当時の完了済み手順の記録として保持し、正式Issueへ昇格しないと承認した。
- **Codex**は、この承認を候補一覧へ手書きで戻さず、検証可能なHuman triage記録として保存する
  根本対応を指示する。
- **Claude**は、V4のHuman triage記録のschema・validator・Issue昇格との結線を、TDDで実装し、
  承認済みの4判断を記録する。

## 解く問題

現在の候補41件は一つのbundle JSONの中にあり、既存V1の`human_triage_decision`は
「候補一件が独立JSON fileである」ことを前提にしている。そのため、既存形式では候補bundle内の
`HTC-...`を正しく参照・検証できない。

候補bundleを人が書き換える方式にはしない。候補は機械抽出時のimmutableな観測であり、Humanの
判断正本は別recordとする。

## 固定入力

- V4 config：`config/development-issue-resolution-pilot-v4.json`
- 候補bundle：`records/development/2026-08-05-historical-todo-intake-candidates-v1.json`
  - file SHA-256：`e01c0feb082712f8ef0f77bfa4f031fbdc4530ed51f331f7dafbfd133d479a3e`
- Human triage資料：`records/development/2026-08-05-historical-todo-intake-triage-material-v1.md`
- V4実装：`tools/development/issue_intake_v4.py`
- V4受入test：`tests/test_issue_intake_v4.py`
- 旧Pilotのconfig／record／validator：履歴として変更しない。

## 設計と実装の要件

### 1. 一候補につき一つのV4 Human triage decision

新しい集約recordを発明せず、既存の「一候補につき一判断record」という粒度を維持する。
V4用の`human_triage_decision` schema version 2を定義する。

各decisionは、少なくとも次を持つ。

- `decision_id`、`decision_version`、`decided_at`、`decision_maker: human`
- `candidate_ref`：
  - candidate bundleの相対pathとfile SHA-256
  - bundle内の`candidate_id`
  - candidate自身の`content_digest`
  - bundle schema version
- Human判断：`unresolved`、`recurrence`、`impact`、`priority`、`promote_to_issue`
- `disposition`、`blocking`、`rationale`、`next_action`
- `content_digest`

decision ID・path・content digestの規則を固定する。未知field、bundle path脱出、bundle SHA不一致、
candidate ID不存在、candidate digest不一致、schema version不一致をfail-closedで拒否する。

### 2. 判断の競合と改訂

- 同じcandidateに対する有効なdecisionは一つだけとする。
- 判断を変える場合は、旧decisionを上書きせず、`decision_version`を上げ、旧decisionへの
  `supersedes`参照を持つ改訂recordとして保存する。
- 異なるdecisionが同じcandidateを参照し、適切な改訂関係を持たない場合は拒否する。
- repository検証は、decision record単体だけでなく、decision集合の競合も確認する。
- V1の旧decisionをV4規則で再判定・変更しない。

### 3. Issue昇格の権限をdecisionへ移す

`historical_todo_intake_candidate.human_fields`は、生成時の未記入観測として保持し続ける。
Issue昇格は、candidate JSONを変更せず、検証済みV4 decisionが次をすべて満たす場合だけ可能にする。

- `decision_maker`が`human`
- `promote_to_issue`が`true`
- `disposition`が`issue_resolution`
- decisionのcandidate参照が、入力candidateとbundle digestを含め完全一致する
- 同candidateに競合する有効decisionが無い

それ以外は`human_triage_decision_required`または具体的な検証codeで停止する。
既存V1の昇格規則を壊さない。

### 4. 今回承認済みの四判断

次の四candidateについて、V4 decisionを各一件ずつ作成する。候補bundle自体は変更しない。

| candidate ID | Human判断 |
| --- | --- |
| `HTC-14D810C7` | `unresolved: false`、`recurrence: false`、`impact: not_applicable`、`priority: not_applicable`、`promote_to_issue: false` |
| `HTC-1AB699F7` | 同上 |
| `HTC-21C3CE46` | 同上 |
| `HTC-6ABDDC35` | 同上 |

`disposition`は「歴史的な完了済み手順であり、現在解くIssueではない」意味を失わない既存語彙または
V4の明示語彙にする。語彙を追加する場合はconfigで固定し、なぜ`reject`だけでは不十分かを
Evidenceに記す。四recordの`rationale`には、次の根拠を平易に記す。

- `6b68c25`でWI-006が実装済み
- `b10cd09`でWI-007のsnapshotが保存済み
- `416e4e1`でTODO compactionが完了済み

`blocking: false`、`issue_promotion.approved: false`とし、Issue IDを持たせない。
決定recordのpathはV4のdirectory規則とID規則に一致させる。

### 5. TDD受入条件

実装前に、既存V4受入testへ追加し、失敗を確認する。少なくとも次を固定する。

1. bundle内candidateを指紋付きで参照するV4 decisionが検証できる。
2. bundle fileのSHA不一致、candidate ID不存在、candidate digest不一致、未知field、path traversalを拒否する。
3. 同candidateへの競合decisionを拒否し、適切な`supersedes`を持つ改訂だけを許す。
4. decisionなし、`promote_to_issue: false`、`disposition`不一致、candidate参照不一致ではIssue化できない。
5. 承認済み四decisionが検証を通り、candidate bundleのbytesが不変である。
6. 旧V1 decisionと旧Pilot検証が通り続ける。
7. repository全体のdecision集合に競合が無い。

テストを実装中に緩めない。設計の矛盾や既存V1／V4の互換性破壊が判明したら、局所patchをせず停止して
報告する。

## 作業単位とコミット

1. RED testを追加して失敗を確認する。RED evidenceを作る。red-only commitは任意。
2. schema／config／validator／昇格結線を実装し、追加testと全testをGREENにする。GREEN evidenceを作り、
   **実装だけ**を一つのコミットにする。
3. 承認済み四decision recordと必要なTODO更新を作成し、全test、参照整合、digest、repository集合検証を
   行う。**判断recordだけ**を別のコミットにする。

各コミット後、次の作業単位へ進む前にworktreeがcleanであることを確認する。

## 禁止事項

- 他の37候補の`human_fields`、triage decision、Issue、Plan、Workを作成・変更しない。
- 四candidateを正式Issueへ昇格しない。
- 既存candidate bundle、旧Pilot config／record、V1 decision、TODOの過去履歴を上書きしない。
- 外部送信、push、PR、CI、Work 4B、Work 6A、E2以降を開始しない。

## 完了報告

完了報告はcommitに混ぜず、次へ保存する。

`records/session-handoffs/2026-08-05-claude-to-codex-v4-human-triage-persistence.md`

報告には、commit SHA、RED／GREEN結果、四decision IDとcandidate ID、bundle不変確認、
全test結果、未実施事項を記す。
