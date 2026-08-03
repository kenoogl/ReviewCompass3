# TODO_NEXT_SESSION

更新日：2026-08-03
用途：session更新・次sessionへの引き継ぎ

> 本書は人向けの入口であり、Workflow state、完了判断、Evidenceの正本ではない。
> 過去sessionを累積せず、固定Plan、checklist、Git、Test、Decision、Provenanceをリンクして使う。

## 現在位置

- 全体：初期開発Work 1AのLayout Baselineを完了
- 現在の工程：Work 1A `verified / completed`、次はWork 1B「Session Log Bootstrapと現在位置text表示」
- activeなTask Contract／Work Item：なし
- 製品実装code：未着手。Work 1A bootstrap validatorだけを追加
- 当面の進行入口：`docs/development/2026-08-03-initial-development-checklist.md`
- 進行入口SHA-256：`bb998fe67d78ce578aae23e3cd305ad749ba0e9aa3279182156fbd8f61f0f73c`
- 現行計画：`docs/current/reviewcompass3-plan-current.md`
- 現行計画SHA-256：`0ae6bef979192b008a8a71fc090f709279c4bd1f0db159f9faadf947e929156f`
- 現行開発方針：`docs/development/2026-08-02-development-policy.md`
- 現行開発方針SHA-256：`a094926a5c9f981cdb1997b4a8e205da9a333fda51f2876b47e76d53fcf7dc1c`
- 直近のDecision／Evidence：`records/development/2026-08-03-work-1a-layout-evidence-v1.md`
- Decision／Evidence SHA-256：`5d54c7de759388ae81c1fefebcc50c817c0b38ae2bcdc65444f47aa48cc8e899`

## 実施報告照合

### verified

- Claim `EC-015`：9 logical root、Git境界、Manifest／Binding、stable／development分離、migration規則を
  Layout Baseline Recordとbootstrap validatorへ実装した。
  - Evidence：commit `d3add9f2e6bc812bf512a36a24877e29879e9842`、
    `records/development/2026-08-03-layout-baseline-v1.json`、SHA-256
    `c18ee7a14a5720e578ea24b71e0cc120524fcfc2bca9df87a81de795cfc36cc2`
  - 観測した事後状態：commitからRecord、validator、Test、fixtureを再読込し、記録Digestと一致した。
- Claim `EC-016`：空配置fixtureのproject移動、相対link、Manifest／Binding、端末固有path、isolation、
  migration負例をtest-firstで検証した。
  - Evidence：`records/development/2026-08-03-work-1a-layout-evidence-v1.md`、SHA-256
    `5d54c7de759388ae81c1fefebcc50c817c0b38ae2bcdc65444f47aa48cc8e899`
  - 観測した事後状態：最初のred `7 failed`、Binding追加red `1 failed, 6 passed`、targeted
    `7 passed`、全`419 passed`、managed absolute path finding 0件を確認した。
- Claim `EC-017`：checklistのWork 1A全項目と完了関門をEvidenceへ接続した。
  - Evidence：`docs/development/2026-08-03-initial-development-checklist.md`、SHA-256
    `bb998fe67d78ce578aae23e3cd305ad749ba0e9aa3279182156fbd8f61f0f73c`
  - 観測した事後状態：Work 1Aのcheckbox、Evidence path／Digest、commit、Test件数、
    `verified / completed`を再読込した。
- Claim `EC-018`：Layout実装とWork 1A完了Evidenceをgreenな意味単位で分割commitした。
  - Evidence：commit `d3add9f2e6bc812bf512a36a24877e29879e9842`
    （`Implement portable layout baseline`）、commit `bc9b6f149672fe5de3dcf55807f4163a2fef4d1e`
    （`Verify Work 1A layout baseline`）
  - 観測した事後状態：`git show --stat`で実装commit 11 file、検証commit 3 fileを確認した。

### reported_unverified／contradicted

- なし

### 未実施

- Work 1B Session Log Bootstrapと現在位置text表示
- platform別OS標準rootの具体解決とProject Bindingのdurable保存
- 実施報告照合の自動Claim抽出、Provenance対応、完了state結線

### 残余risk

- Layout validatorはWork 1A固定規則のbootstrap oracleであり、正式製品Runtimeではない。
- documentation revision v16は`digest-only`の履歴として残るが、現行固定入力とWork 1A Evidenceは
  Gitから再構築可能である。

## 次に行う一作業

Work 1Bで、Layout Baselineを使うSession Log Bootstrapの固定fixtureとred Testを作る。

開始条件：

- Work 1A Evidence、Layout Baseline Record、commit `d3add9f`のidentityとDigestが一致している。

完了条件：

- raw／派生物のroot分離、source availability、restore、主要状態event、短縮／詳細text表示の固定fixtureが、
  bootstrap mapping未実装を期待理由として失敗する。

後続作業：固定したWork 1B Testを変更せず、最小Session Log Bootstrapとtext projectionをgreenにする。

## blocker・Human判断待ち

- blocker：なし
- Human判断待ち：なし
- 再開条件：満たしている

## stale・deferred

- stale：なし。Layout Baseline、validator、fixture、oracle変更時はWork 1A Evidenceをstaleにして再検証する。
- deferred：画面UI、As-Built projection、AI判断委譲、shared／distributed deployment、改善候補・
  Issue Resolution・実施報告照合のautomation、汎用Task Registry／plugin system

## Git・Test

- branch：`main`
- Layout implementation commit：`d3add9f2e6bc812bf512a36a24877e29879e9842`
- Work 1A verification commit：`bc9b6f149672fe5de3dcf55807f4163a2fef4d1e`
- HEAD：`bc9b6f149672fe5de3dcf55807f4163a2fef4d1e`
- worktree：本TODOだけをhandoff commit対象とし、commit後にcleanを再確認する
- 直近の関連Test：`python3 -m pytest -q tests/test_layout_baseline.py`、`7 passed`
- 直近の全Test：`python3 -m pytest -q`、`419 passed`
- 差分検査：`git diff --check`、通過

## 更新規則

- session終了時に、現在位置、実施報告照合、未実施、次の一作業、blocker、stale、Git／Test、
  参照Digestを更新する。
- 報告だけでClaimを`verified`にせず、Evidenceと観測した事後状態を記録する。
- TODOは現行handoffだけを保持し、過去sessionの時系列logにしない。
- Stage変更、長期中断、大きな計画改定など、独立保持する価値がある場合だけ
  `records/session-handoffs/`へ日付付きの不変snapshotを作る。
- 通常のsession履歴と完了EvidenceはSession Evidence、Decision、Provenance、Gitへ保存する。
