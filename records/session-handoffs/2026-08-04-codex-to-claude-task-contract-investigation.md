# Codex → Claude：Task Contract 固定入力の調査指示

## このファイルの役割

Codexが次の作業をClaudeへ渡すための指示書である。Humanへの伝言は要求しない。
Claudeはこのファイルを最新の作業指示として読み、完了報告は指定の返答ファイルへ書く。

## 現在の停止理由

`docs/current/reviewcompass3-plan-current.md`をWork 4Aの承認済み方針へ更新したところ、
`records/task-contract/issue-resolution-early-pilot-v1.json`が固定していた旧Digestと一致しなくなり、
全testが1件停止した。

これはWork 4A実装の不良ではない。更新可能なCurrent Planを、active扱いのTask Contractが
固定入力として直接参照している、authority境界の問題である。

## Claudeが行うこと

読み取り専用で、恒久対応の設計案を調査する。

- `issue-resolution-early-pilot-v1`の後続Task Contract、状態記録、参照関係を確認する。
- Current Planを固定sourceに持つTask Contractを列挙する。
- Task Contractが固定sourceを `Git commit + repository-relative path + SHA-256` で参照する方式を検討する。
- 既存Task Contractを変更せずに、historic検証とCurrent Plan更新を両立する最小migrationを示す。
- validatorとtestの変更が必要な範囲を示す。

## 行ってはならないこと

- Work 4Aの実装、test、外部DATA_ROOT、LLM生成、候補再抽出を変更しない。
- `records/task-contract/issue-resolution-early-pilot-v1.json`を変更しない。
- 現在未コミットのPlan、Checklist、TODOを変更・破棄・コミットしない。
- Task Contract v2、Decision、Issue、改善候補を作成しない。
- 既存testを変更・実行して結果を固定しない。

## 返答ファイル

調査結果だけを次の新規ファイルへ書く。コミットしない。

`records/session-handoffs/2026-08-04-claude-to-codex-task-contract-investigation.md`

返答は次の5節だけにする。

1. 確認した事実
2. 根本原因
3. 最小の恒久対応案
4. migration対象とvalidator／testへの影響
5. Human判断が必要な一点

設計案を複数並べてHumanへ判断を委ねない。推奨案を一つに絞り、必要なHuman判断も一つに絞る。
