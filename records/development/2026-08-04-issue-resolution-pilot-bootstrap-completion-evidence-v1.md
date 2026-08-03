---
evidence_id: RC3-ISSUE-RESOLUTION-PILOT-BOOTSTRAP-COMPLETION-2026-08-04-V1
recorded_at: 2026-08-04T08:18:05+09:00
status: verified_completed_pending_commit
confidentiality_class: project-internal
---

# Issue Resolution Pilot Bootstrap Completion Evidence V1

## 完了範囲

Issue Resolution早期Pilot全体ではなく、Task Contractで定めた最初の作業単位
`bootstrap Candidate and Triage Decision shape with RED and GREEN validation`を完了した。

- Humanの限定再開Decisionを固定した。
- TODO肥大化の観測値を、CandidateでもIssueでもない不変Observationとして固定した。
- 一つのPilot subject、固定source 9件、scope、non-scope、Acceptance、停止条件をTask Contractへ固定した。
- provisionalなImprovement CandidateとHuman Triage Decisionの配置、field、ID、version、命名、Digest、参照規則を
  設定とvalidatorへ固定した。
- Human以外のIssue昇格、stale Candidate参照、誤配置、Digest不一致、TODOへの詳細複製を負例で拒否した。
- 初期record directoryは`.gitkeep`だけであり、Candidate、Decision、Issueはまだ作成していない。

正式な製品schema、state machine、Workflow permit、自動Issue昇格、Work 8正式評価は開始していない。

## 固定成果物

- Resume Decision：
  `records/development/2026-08-04-issue-resolution-pilot-bootstrap-resume-decision.json`、SHA-256
  `d633c3b319cd46bf98a2b90cb5251370cd495511421a485ba41184e1b3e962b6`
- Observation：`records/development/2026-08-04-todo-growth-pilot-observation-v1.json`、SHA-256
  `7d3e472f84d20e19d28a1c0e5c1c3d894b10e851fe3e7164cc2b7302fc00f67b`
- Task Contract：`records/task-contract/issue-resolution-early-pilot-v1.json`、SHA-256
  `69e2c73167f930cab48abdcf3bd4d1eafa938aa9b3abaa714d6c3ad5e41c4ed7`
- RED Evidence：
  `records/development/2026-08-04-issue-resolution-pilot-bootstrap-red-evidence-v1.md`、SHA-256
  `a4ffda7ff5654b7be9d2630ed688abc4926347ae4a8fe386e7837b89898db9e5`
- Pilot設定：`config/development-issue-resolution-pilot.json`、SHA-256
  `b12700f68b3de9e690ad11f8b97a9ee8baed9a3f60ff6580a3dc4c27c0b0967a`
- 固定Test：`tests/test_issue_resolution_pilot.py`、SHA-256
  `007b85a63f93b6ffeb12139717bc9abc2c19ad5c13424ce27ebdbeff698d13f6`
- validator：`tools/development/issue_resolution_pilot.py`、SHA-256
  `73538405e5275c3feb364199060a4fe8bdf74ab156e07a4f1a6cbcedd2b35d63`
- Layout互換Test：`tests/test_layout_baseline.py`、SHA-256
  `baec18533e2f8486d8b4c797e5cb69341673636367e68c54b2386b3216980928`

## 検証

- RED：`python3 -m pytest -q tests/test_issue_resolution_pilot.py`は、validator未実装だけを理由に
  `15 failed in 0.11s`となった。
- GREEN：同じTestを変更せず再実行し、`15 passed in 0.03s`となった。
- bootstrap CLI：`python3 tools/development/issue_resolution_pilot.py bootstrap`は
  `{"status": "passed"}`を返した。
- Task Contract CLI：
  `python3 tools/development/issue_resolution_pilot.py task-contract records/task-contract/issue-resolution-early-pilot-v1.json`は
  `{"fixed_source_count": 9}`を返した。
- 初回公式全Testは`1 failed, 520 passed in 2.69s`となった。既存Layout TestがProject Manifest作成時の
  workflow snapshot一件を永続不変と解釈し、承認済みroot内の二つの空directory追加を拒否したためである。
  旧Evidenceは当時のsnapshotとして変更せず、既存Testの期待値へ今回の二つの空directoryを追加した。
- Layout互換TestとPilot Testの再実行は`27 passed in 0.08s`だった。
- 公式全Test結果は
  `records/development/2026-08-04-issue-resolution-pilot-bootstrap-green-test-receipt-v3.json`を正本とする。初回失敗receipt
  v1とpost-write変更前の成功receipt v2は問題発生／検証履歴として保持し、完了根拠には使わない。

## 手戻りと機械処理候補

bootstrap検証時に、実装済みCLIが`bootstrap`と`task-contract`を受け付けるのに、LLMが確認せず
`validate-bootstrap`を手入力し、引数エラーを一回発生させた。成果物、Test結果、固定sourceへの影響はない。

- 期待executor：共有されたcommand定義からsubcommandを選ぶ機械処理
- 実executor：LLMによるshell command文字列の手組み
- 対処：`--help`を読み、定義済みsubcommandで再実行して合格を確認した。
- 恒久対策候補：完了検証を公式runnerまたは固定verification scriptへ集約し、LLMがsubcommand名を再入力しない。
- route：`manual_operation_candidate / checkpoint`

この観測は現Pilot subjectと別のIssueへ昇格させず、本Evidenceへ保持する。分類と昇格は別のHuman判断があるまで
行わない。

公式全Testでは、機械Testが旧snapshot期待と今回の意図した配置拡張の不一致を一件検出した。実executorと
期待executorはともに`machine`で、手作業因果はない。旧Evidenceを上書きせず、現在の互換Testだけを変更して閉じた。
routeは`expected_contract_evolution / closed_by_updated_test`とする。

成功receipt v2作成後、LLMがTODOの作業単位状態を`verified_completed_pending_commit`からcommit後にも安定する
`verified_completed`へ手修正し、receiptの`source_state_digest`と事後状態を不一致にした。内容訂正自体は必要だが、
最終receiptより後に行った検証順序が誤りだった。全成果物を先に確定してから公式全Testをv3へ再実行する。

- 期待executor：最終成果物確定を検査してからreceiptを発行する機械finalizer
- 実executor：LLMによるreceipt実行とTODO状態確定の順序選択
- 恒久対策候補：公式receipt発行をpost-write finalizerの最後の書込みに固定し、その後はread-only照合だけを許可する。
- route：`manual_rework_candidate / checkpoint`

## 次作業

固定した暫定形状を使い、TODO肥大化という単一subjectの最初のImprovement Candidateを作成し、Human Triage
Decisionを得る。Human判断なしにはIssue Recordを作らない。
