# TODO_NEXT_SESSION

更新日：2026-08-03
用途：session更新・次sessionへの引き継ぎ

> 本書は人向けの入口であり、Workflow state、完了判断、Evidenceの正本ではない。
> 過去sessionを累積せず、固定Plan、checklist、Git、Test、Decision、Provenanceをリンクして使う。

## 現在位置

- 全体：初期開発Work 1のProvenance修復をHuman承認に基づいて実施中
- 現在の工程：Work 1 corrective snapshotのcommit前検証
- activeな製品Task Contract／Work Item：なし
- 製品実装code：未着手
- 当面の進行入口：
  `docs/development/2026-08-03-initial-development-checklist.md`
- checklist SHA-256：
  `ea833b027d61b5fc200ef289dffa5cde41be5e8d7fbe36b97bfeae3ab94e2db3`
- Work 1固定入力Evidence：
  `records/development/2026-08-03-work-1-fixed-input-evidence.md`
- Work 1固定入力Evidence SHA-256：
  `d07c5abdce7bc4b3322e7c6f973feb0e00d7218151dafe7013aff5d08148b879`
- blocking改善候補：
  `records/development/2026-08-03-work-1-reconstructability-candidate.md`
- blocking改善候補 SHA-256：
  `4206805e3066335c5a84a56baa839e4b074da4b5af1f8cd17b20bcbe22860404`
- 修復Decision：
  `records/development/2026-08-03-work-1-reconstructability-repair-decision.json`
- 修復Decision SHA-256：
  `d8da18034eabaa38dcd80f2648a7484ed516ce0dfadce91f819ba436956e7576`
- corrective snapshot：
  `records/development/2026-08-03-work-1-corrective-snapshot-v1.json`
- corrective snapshot SHA-256：
  `08365d976f020b428c46d1f83b14d7b0861beb335103493cf81823a144cc25c4`
- 現行計画：`docs/current/reviewcompass3-plan-current.md`
- 現行計画 SHA-256：
  `0ae6bef979192b008a8a71fc090f709279c4bd1f0db159f9faadf947e929156f`
- 現行開発方針：`docs/development/2026-08-02-development-policy.md`
- 現行開発方針 SHA-256：
  `a094926a5c9f981cdb1997b4a8e205da9a333fda51f2876b47e76d53fcf7dc1c`
- 改定判断記録：`records/development/development-policy-v4.json`
- 改定判断記録 SHA-256：
  `87bd0460bce3ae471a598ae5ab2964d05e6ceb97701870f25b5cc9110133f24a`
- TODO template：`docs/development/templates/TODO_NEXT_SESSION.template.md`
- TODO template SHA-256：
  `9e76436a2de0a3a7ce7d5764247e2d8b17bad18b62c190c9e2fd3721fb848870`

## 実施報告照合

### verified

- Claim `EC-001`：現在位置表示、改善候補route、初期開発checklist、TODO縮約とsnapshot分離を文書へ反映した。
  - Evidence：`docs/design/2026-08-03-current-work-projection-memo.md`、
    `docs/design/2026-08-03-self-application-improvement-routing-memo.md`、
    `docs/development/2026-08-03-initial-development-checklist.md`、`records/session-handoffs/`
  - 観測した事後状態：対象fileの存在、参照、Digestを再確認した。
- Claim `EC-002`：TODOの新規作成・構造復元用templateを作成し、開発入口から参照した。
  - Evidence：`docs/development/templates/TODO_NEXT_SESSION.template.md`、SHA-256
    `9e76436a2de0a3a7ce7d5764247e2d8b17bad18b62c190c9e2fd3721fb848870`
  - 観測した事後状態：fileの再読込、`AGENTS.md`、checklist、文書索引からの参照を確認した。
- Claim `EC-003`：実施報告を固定Evidenceと事後状態へ照合する規律を文書へ反映した。
  - Evidence：`docs/design/2026-08-03-execution-claim-verification-memo.md`、現行開発方針、用語集、
    現行計画、checklist、TODO template、`records/development/development-policy-v4.json`
  - 観測した事後状態：対象内容、参照Digest、JSON構文、全Test、差分形式を再確認した。
- Claim `EC-004`：開発規律、現行計画、設計メモ、checklist、template、改定Evidenceを分割commitした。
  - Evidence：commit `1968eee`（`Add operational development guidance`）
  - 観測した事後状態：`git show --stat 1968eee`で11 file、1481 insertions、6 deletionsを確認した。
- Claim `EC-005`：文書索引を更新し、旧TODOを不変snapshotへ分離してcommitした。
  - Evidence：commit `64a6665`（`Index guidance and archive prior handoff`）
  - 観測した事後状態：`git show --stat 64a6665`で索引とsnapshotの2 fileを確認した。
- Claim `EC-006`：Work 1の固定入力、scope、非目標、未解決事項、Extraction Contract、
  Consumption Closure、stale／再開規則を一つのEvidenceへ固定した。
  - Evidence：`records/development/2026-08-03-work-1-fixed-input-evidence.md`、SHA-256
    `d07c5abdce7bc4b3322e7c6f973feb0e00d7218151dafe7013aff5d08148b879`
  - 観測した事後状態：authority 3文書、source catalog 10 entry、前身inventory 2件、Git開始状態を
    再照合した。Work 1結果は`blocked`であり、Work 1Aの開始根拠には使用しない。
- Claim `EC-007`：documentation revision v16の同一commit再構築でmanifest 18件中5件のDigest不一致を
  検出し、blocking改善候補へ記録した。
  - Evidence：`records/development/2026-08-03-work-1-reconstructability-candidate.md`、SHA-256
    `4206805e3066335c5a84a56baa839e4b074da4b5af1f8cd17b20bcbe22860404`
  - 観測した事後状態：commit `e603804d4853f29c1ebeb97ef82774447211ff05`からv16 manifestを
    再読込し、`README.md`、`docs/README.md`、現行Intent、現行Plan、design amendmentの不一致を確認した。
- Claim `EC-008`：checklist Work 1へ固定Evidenceと停止結果を接続した。
  - Evidence：`docs/development/2026-08-03-initial-development-checklist.md`、SHA-256
    `ea833b027d61b5fc200ef289dffa5cde41be5e8d7fbe36b97bfeae3ab94e2db3`
  - 観測した事後状態：Work 1の開始条件、確認項目、完了関門、Evidence path／Digest、
    `blocked / pause_and_triage`表示を再読込した。
- Claim `EC-009`：Humanがv16を上書きしないcorrective snapshot修復の開始を承認した。
  - Evidence：`records/development/2026-08-03-work-1-reconstructability-repair-decision.json`、
    Decision `WORK1-RECONSTRUCTABILITY-REPAIR-DEC-001`、SHA-256
    `d8da18034eabaa38dcd80f2648a7484ed516ce0dfadce91f819ba436956e7576`
  - 観測した事後状態：修復scope、Intent／Plan意味変更・v16上書き・risk受容を含まない境界、
    `approved_for_execution`をJSON再読込で確認した。
- Claim `EC-010`：v16の未達forward fixを訂正し、Work 1固定入力13件を同一commitへ固定する
  corrective snapshot manifestを作成した。
  - Evidence：`records/development/2026-08-03-work-1-corrective-snapshot-v1.json`、SHA-256
    `08365d976f020b428c46d1f83b14d7b0861beb335103493cf81823a144cc25c4`
  - 観測した事後状態：JSON構文とworktree上のmanifest 13件全Digest一致を確認した。
    状態は`pending_post_commit_verification`であり、まだreconstructableとは扱わない。

### reported_unverified／contradicted

- なし

### 未実施

- corrective recordを含むcommitとpost-commit manifest全件照合
- Human判断後のWork 1再開Evidence v2
- Work 1A Layout Baseline
- 実施報告照合の自動Claim抽出、Provenance対応、完了state結線

### 残余risk

- 統合最新版はHuman承認前の候補であり、製品実装codeは未着手である。
- documentation revision v16はforward immutable-snapshot ruleを満たしたcommitを再構築できず、
  現行候補への過去revision Provenanceを完全と扱えない。

## 次に行う一作業

corrective snapshot、固定入力13件、Work 1 blocked Evidence、修復Decisionを第一commitへ固定する。

開始条件：

- corrective snapshotのworktree manifest 13件が全件一致している。

完了条件：

- corrective snapshotを含むcommit SHAを取得できる。

後続作業：固定commitからmanifest全件を照合し、post-commit EvidenceとWork 1 Evidence v2を作る。

## blocker・Human判断待ち

- blocker：v16不一致はcorrective snapshotへ記録したが、まだ固定commitとpost-commit Evidenceがない。
- Human判断待ち：なし。修復開始Decisionを固定済み。
- 再開条件：corrective snapshotを含むcommitからmanifest 13件が全件一致し、Work 1 Evidence v2が
  fixed-input completenessをpassする。

## stale・deferred

- stale：Work 1 Evidence v1は`blocked`結果として固定し、Work 1Aのpermitには使わない。
  authority 3文書の現在内容とchecklist記載Digestには不一致なし。
- deferred：画面UI、As-Built projection、AI判断委譲、shared／distributed deployment、
  改善候補、Issue Resolution、実施報告照合のautomation、汎用Task Registry／plugin system

## Git・Test

- branch：`main`
- session base HEAD：`13347232f2f0c1b891d761840c4ae9d9382b354f`（`Refresh session handoff`）
- worktree：checklist、TODO、Work 1 Evidence、blocking改善候補、修復Decision、corrective snapshotが未commit。
- 本sessionの全Test：`python3 -m pytest -q`、`412 passed`
- `git diff --check`：通過
- commit：未実施。利用者から本sessionのcommit指示は受けていない。

## 更新規則

- session終了時に、現在位置、実施報告照合、未実施、次の一作業、blocker、stale、Git／Test、
  参照Digestを更新する。
- 報告だけでClaimを`verified`にせず、Evidenceと観測した事後状態を記録する。
- 現行handoffを短時間で読める量に保ち、過去sessionを本書へ追記し続けない。
- milestone、長期中断、大きな計画改定など独立保持する価値がある場合だけ、
  `records/session-handoffs/`へ不変snapshotを作る。
- 通常の履歴はSession EvidenceとGitへ保存する。
