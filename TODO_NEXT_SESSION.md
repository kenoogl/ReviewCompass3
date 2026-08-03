# TODO_NEXT_SESSION

更新日：2026-08-03
用途：session更新・次sessionへの引き継ぎ

> 本書は人向けの入口であり、Workflow state、完了判断、Evidenceの正本ではない。
> 過去sessionを累積せず、固定Plan、checklist、Git、Test、Decision、Provenanceをリンクして使う。

## 現在位置

- 全体：Task Contract中心設計から初期開発へ移る準備段階
- 現在の工程：Work 1「固定入力と開発入口」のEvidence確認前
- activeな製品Task Contract／Work Item：なし
- 製品実装code：未着手
- 当面の進行入口：
  `docs/development/2026-08-03-initial-development-checklist.md`
- checklist SHA-256：
  `42dc7a0d2d1080a2297abeeaa0da79edd902c38f6d3572245b1d0e42026b44c9`
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

### reported_unverified／contradicted

- なし

### 未実施

- checklist Work 1の固定Evidence作成
- 実施報告照合の自動Claim抽出、Provenance対応、完了state結線

### 残余risk

- 統合最新版はHuman承認前の候補であり、製品実装codeは未着手である。

## 次に行う一作業

checklistのWork 1で、固定入力、scope、非目標、未解決事項を既存artifactと固定Evidenceへ接続する。

開始条件：

- 現行Intent、用語集、計画、checklistのpathとDigestが一致している。

完了条件：

- 固定入力、scope、非目標、未解決事項、blocking conflictを一つのEvidenceから確認できる。

後続作業：Work 1AでLayout Baselineを固定する。

## blocker・Human判断待ち

- blocker：なし
- Human判断待ち：なし
- 再開条件：満たしている

## stale・deferred

- stale：確認済みの参照Digestには不一致なし
- deferred：画面UI、As-Built projection、AI判断委譲、shared／distributed deployment、
  改善候補、Issue Resolution、実施報告照合のautomation、汎用Task Registry／plugin system

## Git・Test

- branch：`main`
- handoff base HEAD：`64a6665`。本TODOを含むcommitは
  `git log -1 --format=%H -- TODO_NEXT_SESSION.md`で取得する。
- worktree：本TODO以外はclean。本TODOをhandoff commit対象とし、session終了時に再確認する。
- 直近の全Test：`python3 -m pytest -q`、`412 passed`
- `git diff --check`：通過

## 更新規則

- session終了時に、現在位置、実施報告照合、未実施、次の一作業、blocker、stale、Git／Test、
  参照Digestを更新する。
- 報告だけでClaimを`verified`にせず、Evidenceと観測した事後状態を記録する。
- 現行handoffを短時間で読める量に保ち、過去sessionを本書へ追記し続けない。
- milestone、長期中断、大きな計画改定など独立保持する価値がある場合だけ、
  `records/session-handoffs/`へ不変snapshotを作る。
- 通常の履歴はSession EvidenceとGitへ保存する。
