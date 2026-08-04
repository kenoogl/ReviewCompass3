# TODO_NEXT_SESSION

更新日：2026-08-04

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：Work 1B、Work 2、Work 3、Issue Resolution早期Pilot、開発venv baseline、Project-first Runtime Layout v3が完了。Work 4Aの旧patch群はrevert済みで、再設計から再開する。
- 現在の工程：Work 4A rebuild／E2E acceptance RED。
- activeなTask Contract／Work Item：なし。
- 製品実装code：未着手。
- 当面の進行入口：[Work 4A Rebuild Design](/docs/design/2026-08-04-work-4a-rebuild-design-proposal.md)
- 進行入口SHA-256：`233ac821e6f55b34ab31219e55bf9f23b19f2e97d2884e34be6fa191b87dda2a`
- 現行計画：[Current Plan](/docs/current/reviewcompass3-plan-current.md)
- 現行計画SHA-256：`0ab828f4d940ab8a6a4d285479afbb1fdbc086afbb72fb993b885599f9bf2694`
- 現行開発方針：[Development Policy](/docs/development/2026-08-02-development-policy.md)
- 現行開発方針SHA-256：`9078276d7ba1f540495a9679a75f12f9dac0c7717fcfd637e883f41b6bf739a0`
- 直近のDecision／Evidence：[DEC-WORK4A-REBUILD-DESIGN-001](/records/development/2026-08-04-work-4a-rebuild-design-approval-decision-v1.md)
- Decision／Evidence SHA-256：`dfa69cabf35cf5e1c40b26eab6044250b270fcdc9fc8e45b9c9b5e71ffdcdf59`

## 実施報告照合

### verified

- Claim `EC-WORK4A-REBUILD-DESIGN-001`：再設計と、局所patchを禁じる方針をHumanが承認した。
  - Evidence：`15bf012`、`DEC-WORK4A-REBUILD-DESIGN-001`。
  - 観測した事後状態：承認済み設計文書がGitに存在する。
- Claim `EC-WORK4A-REVERT-001`：台帳、候補抽出、局所policy対応の旧patchをrevertし、Layout v3を保持した。
  - Evidence：revert commit群。
  - 観測した事後状態：旧Work 4Aのsource index、candidate、ledger実装とrecordが存在しない。

### 手戻り・機械化候補

- 対象操作：関数追加時の台帳更新。期待executor：versioned ledger writer。旧実executor：既存Entryを複製する局所実装。手戻り事象：追加一件で既存recordを複製する設計になった。機械処理候補：E2E acceptanceでnew-only書込みと既存Digest再利用を強制する。route：Work 4A rebuild。

### 未実施

- 七項目のE2E RED acceptance、rebuild実装、actual artifactは未実施。

## 次に行う一作業

Work 4A再設計の七項目を一つのE2E acceptance test群としてREDで固定する。

開始条件：

- `DEC-WORK4A-REBUILD-DESIGN-001`によるHuman承認。
- reversion commit後のclean transition。

完了条件：

- new-only Entry／Relation／Baseline、content-based freshness、Historical Contract Status、負例を含む受入testが意図どおりREDになる。
- production implementation、actual artifact、既存patchの部分復元を含めない。

後続作業：RED testを変更せず、最小のidentity chain実装をGREENにする。

## blocker・Human判断待ち

- blocker：なし。
- Human判断待ち：なし。設計承認済み。
- 再開条件：RED acceptance containing commit後のclean transition。

## stale・deferred

- stale：旧Work 4AのSource Snapshot、Index、Candidate、Ledger、Policy状態を根拠にしたEvidence。rebuild E2EがGREENになるまで再利用しない。
- deferred：正式Issue Resolution schema、UI、automation、Work 8正式評価。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点。
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する。
- worktree：本revert完了・commit時点でcleanにする。
- 直近の関連Test：revert後に実行する。
- 直近の全Test：revert後に実行する。
- 差分検査：revert後に実行する。

## 更新規則

- 現在位置、実施報告照合、未実施、次の一作業、blocker、stale、Git／Test、参照Digestだけを置き換える。
- TODOへ過去sessionを累積しない。完了Evidence、Decision、Gitへ詳細を残す。
- 完了した作業単位が未コミットなら、次作業へ進まない。
