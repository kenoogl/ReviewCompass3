# TODO_NEXT_SESSION

更新日：`{{YYYY-MM-DD}}`
用途：session更新・次sessionへの引き継ぎ

> 本書は人向けの入口であり、Workflow state、完了判断、Evidenceの正本ではない。
> 過去sessionを累積せず、固定Plan、checklist、Git、Test、Decision、Provenanceをリンクして使う。

## 使用方法

- このtemplateの内容をルートの`TODO_NEXT_SESSION.md`へ適用する。
- 既存TODOを更新する場合はsession履歴を追記せず、各欄を現在のhandoffで置き換える。
- `{{...}}`を実値または`なし`へ置き換え、不要な説明とplaceholderを残さない。
- pathだけでなく、内容同一性が必要なauthorityとEvidenceにはDigestを記録する。
- 次作業は、開始条件と完了条件を説明できる一作業に限定する。
- 最終stage前に`python3 tools/development/todo_handoff.py TODO_NEXT_SESSION.md`を実行する。
- Git欄へ自己SHA、固定ahead／behind、push済否、未コミットsnapshotを記録しない。

## 現在位置

- 全体：`{{全体状況}}`
- 現在の工程：`{{Stage／Work／関門}}`
- activeなTask Contract／Work Item：`{{IDまたはなし}}`
- 製品実装code：`{{未着手／進行中／存在}}`
- 当面の進行入口：`{{path}}`
- 進行入口SHA-256：`{{sha256}}`
- 現行計画：`{{path}}`
- 現行計画SHA-256：`{{sha256}}`
- 現行開発方針：`{{path}}`
- 現行開発方針SHA-256：`{{sha256}}`
- 直近のDecision／Evidence：`{{pathまたはなし}}`
- Decision／Evidence SHA-256：`{{sha256またはなし}}`

## 実施報告照合

### verified

- Claim `{{EC-ID}}`：`{{実施、結果または判断}}`
  - Evidence：`{{path、Digest、command結果、commit SHA、receiptまたはDecision}}`
  - 観測した事後状態：`{{再読込または独立照合の結果}}`

### reported_unverified／contradicted

- `{{EC-ID、報告、欠けているEvidence、不一致、影響またはなし}}`

### 手戻り・機械化候補

- `{{対象操作、期待executor、実executor、手作業理由、手戻り事象、Evidence、機械処理候補、routeまたはなし}}`

### 未実施

- `{{提案、予定、deferred、未実施作業またはなし}}`

### 残余risk

- `{{riskまたはなし}}`

## 次に行う一作業

`{{次に実行可能な一作業}}`

開始条件：

- `{{開始に必要な状態または判断}}`

完了条件：

- `{{固定Evidenceで確認できる完了状態}}`

後続作業：`{{次作業完了後の候補。一件またはなし}}`

## blocker・Human判断待ち

- blocker：`{{事象、原因、解除条件、ownerまたはなし}}`
- Human判断待ち：`{{判断対象またはなし}}`
- 再開条件：`{{再開に必要な状態またはなし}}`

## stale・deferred

- stale：`{{対象、理由、再確認条件またはなし}}`
- deferred：`{{初期範囲へ入れない能力またはなし}}`

## Git・Test

- branch：`{{branch}}`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：`{{command、結果または未実施理由}}`
- 直近の全Test：`{{command、結果または未実施理由}}`
- 差分検査：`{{command、結果}}`

## 更新規則

- session終了時に、現在位置、実施報告照合、未実施、次の一作業、blocker、stale、Git／Test、
  参照Digestを更新する。
- 報告だけでClaimを`verified`にせず、Evidenceと観測した事後状態を記録する。
- 手戻り時は手作業との因果を確認し、原因または原因候補なら機械処理候補とrouteを記録する。
- Git欄はcommit安定形式を維持し、mutableなGit状態はGitから機械取得する。
- TODOは現行handoffだけを保持し、過去sessionの時系列logにしない。
- Stage変更、長期中断、大きな計画改定など、独立保持する価値がある場合だけ
  `records/session-handoffs/`へ日付付きの不変snapshotを作る。
- 通常のsession履歴と完了EvidenceはSession Evidence、Decision、Provenance、Gitへ保存する。
