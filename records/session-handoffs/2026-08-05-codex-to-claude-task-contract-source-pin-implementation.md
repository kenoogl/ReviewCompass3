# Codex → Claude：Task Contract固定入力の恒久対応

## 承認済みの方針

Humanは次を承認した。

- lifecycle statusが`active`のTask Contractは、fixed sourceを現在のworking treeで検証する。
  fixed sourceの内容が変われば、契約は`stale`として停止する。
- lifecycle statusが`completed`、`completed_carried_forward`、`superseded`、`historical`の
  Task Contractだけは、受理時点のGit blob（commit、repository-relative path、SHA-256）で
  fixed sourceを検証できる。
- `issue-resolution-early-pilot-v1`は後続Task Contractの
  `completed_carried_forward`記録を根拠に歴史記録として扱う。
- `session-transcript-eventual-preservation-v1`は`active`のまま`stale`として扱い、
  Work 4Aとは別作業に分離する。

## 目的

更新可能なCurrent Planを更新しても、完了・引継ぎ済みのTask Contractの受理時点の来歴を
失わず検証できるようにする。同時に、activeなTask Contractが古いPlanまたはPolicyで
継続しないようにする。

## 実施すること

### 1. lifecycle status record

new-onlyのlifecycle status recordを作る。少なくとも次を記録する。

- `issue-resolution-early-pilot-v1`：`completed_carried_forward`
  - 根拠は後続の`issue-resolution-todo-compaction-implementation-v2`にある
    `status_at_creation: completed_carried_forward`である。
- `session-transcript-eventual-preservation-v1`：`active_stale`
  - fixed Development PolicyのDigest不一致を根拠として記録する。

status recordは、対象Task Contractのpath、Task Contract file SHA-256、status、根拠sourceの
pathとSHA-256、record自身のcontent digestを持つ。既存Task Contract fileは変更しない。

### 2. historical source-pin record

`issue-resolution-early-pilot-v1`だけに対するnew-only source-pin recordを作る。

- Task Contract IDとTask Contract file SHA-256を記録する。
- `docs/current/reviewcompass3-plan-current.md`について、fixed sourceとして記録済みの
  SHA-256 `0ab828f4d940ab8a6a4d285479afbb1fdbc086afbb72fb993b885599f9bf2694`と、
  それに一致するGit commit `c475becb3ebf3f3cb9e362d64bab79606ed3719d`を記録する。
- repository-relative path、commit、blobのSHA-256、pinの理由、content digestを持つ。
- source pinは歴史状態のTask Contractにしか使用できない。

`session-transcript-eventual-preservation-v1`にはsource pinを作らない。

### 3. validatorとCLI

`tools/development/issue_resolution_pilot.py`を変更する。

- active statusのcontractは従来どおりworking treeのfixed sourceを検証する。
- historical statusのcontractは、対応するsource-pin recordがある場合だけ
  `git cat-file blob <commit>:<path>`のSHA-256を検証する。
- pinが無い、commitまたはblobが解決できない、blob digestが不一致、pinのTask Contract digestが
  対象contractと不一致、同一fixed sourceへ競合するpinがある場合は停止する。
  エラーcodeは`pin_unresolvable`または`source_pin_mismatch`として固定する。
- historical statusなのにpinが無い場合、working treeへ黙ってfallbackしてはならない。
- `active_stale`のcontractはsource pinで有効化してはならず、`stale_fixed_source`で停止する。
- CLIにはpin解決件数を追加してよいが、既存の出力keyを削除・改名しない。

### 4. TDDと検証

先にtestを作り、失敗を確認する。少なくとも次を固定する。

1. historicalなearly-pilot契約は、Current Planが変わっていても、pinのGit blobが一致すれば通る。
2. activeなcontractはCurrent PlanまたはPolicyが変われば停止する。
3. `active_stale`なsession-transcript契約は、source pinで通せない。
4. pinのcommit不存在、blob不一致、対象contract不一致、重複pinを停止する。
5. source pinの無いhistorical contractを停止する。
6. 既存のissue-resolution Pilot Testと全testを通す。

### 5. 既存の未コミットPlan更新

現在未コミットの次の変更は保持する。

- `docs/current/reviewcompass3-plan-current.md`
- `docs/development/2026-08-03-initial-development-checklist.md`
- `TODO_NEXT_SESSION.md`

Task Contract対応のGREEN確認後、Plan・Checklist・TODOを別コミットで確定する。
その際、現在の`work-4a-v3-1-plan-alignment-green-test-receipt-v1.json`は実際にはfailed receiptなので、
正しい`failure`名で保存する。誤った`green`名のfileをコミットしてはならない。

## コミット境界

1. lifecycle status record、source-pin record、TDD test、validator実装、GREEN Evidenceを
   **Task Contract固定入力対応**として一つのGREEN commitにする。Plan・Checklist・TODOは含めない。
2. 全testが通ったことを確認してから、Plan・Checklist・TODOとfailed receiptを
   **Work 4A v3.1 Plan alignment**として別commitにする。

## 禁止事項

- Git historyの書換え、既存Task Contract fileの書換え、Task Contract v2の作成を禁止する。
- Work 4Aの追加実装、Routine Profile再生成、Disposition Proposal生成、LLM分析、外部DATA_ROOTへの
  追加書込みを禁止する。
- `session-transcript-eventual-preservation-v1`をsource pinで有効化してはならない。

## Claudeの完了報告

結果は次の新規ファイルへ書き、commitしない。

`records/session-handoffs/2026-08-05-claude-to-codex-task-contract-source-pin-implementation.md`

報告には、作成したrecord、RED／GREEN結果、全test結果、2つのcommit SHA、
active_staleのsession-transcript契約を別作業へ残したことだけを書く。
