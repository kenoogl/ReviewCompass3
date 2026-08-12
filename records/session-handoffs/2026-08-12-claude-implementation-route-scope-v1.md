# Claude実装委譲経路 第1縦切り 範囲固定 v1

- 状態：`proposed_scope`
- 日付：2026-08-12
- 危険度：`high`
- 用途名：`claude_implementation_executor`
- 先行裁定：`2026-08-12-claude-implementation-route-selection-human-decision-v1.md`

## 1. 目的

`pilot: codex`で、品質確認済みの実装依頼だけをClaudeへ渡し、Claudeの変更を主作業ツリーから隔離して
保存し、機械検証後に反対側のCodexモデルがレビューできる最小経路を作る。

この経路を作る実装作業は、まだClaudeへ委譲できないため、Codex実装用サブエージェントが担当する。
経路の確認運転では、Claudeが合成fixture repositoryの小さな実装だけを行う。ReviewCompass3本体の内容を
Claudeへ読ませる実運用は本縦切りに含めない。

## 2. 既存方式との関係

- `docs/development/pilot-specific-claude-codex-collaboration.md`の`pilot: codex`を使う。
- Codex主担当は`gpt-5.6-sol`、実装用Codexサブエージェントも`gpt-5.6-sol`、指示文監査、判定、
  完了レビューは相互に別の`gpt-5.6-terra`サブエージェントとする。
- 無工具疎通の`claude_session_bootstrap`は能力設定、承認、用途を流用しない。
- 既存のHuman裁定・再監査を扱う「第2縦切り」は変更しない。
- 内容の正本はGitへコミットした指示書と結果記録とし、CLIは発見力を維持する。

## 3. 開始時の固定値

```text
collaboration_method: pilot_specific_claude_codex
pilot: codex
implementer_for_route: codex_implementation_subagent
implementer_for_proof: claude
review_requester: codex_main
review_executor: codex_review_subagent
pilot_model: gpt-5.6-sol
reviewer_model: gpt-5.6-terra
instruction_quality_model: gpt-5.6-terra
closer: codex_main
material_mode: discovery
fixed_input_origin: judgment_selected
instruction_quality_round_limit: 2
implementation_review_round_limit: 2
reimplementation_context: new
mechanical_assurance_status: specified_only
```

基準コミット、指示書、固定資料、要求集合、結果形式、能力設定、許可する試験command、変更可能path、
一回限り承認は、作業開始設定でSHA-256へ束縛する。

## 4. 能力設定

確認運転のClaude Codeは、実測済みの版と実行file指紋、`claude.ai`／`firstParty`認証、Humanが指定した
モデルを要求する。API key由来の認証は拒否する。

Claudeは主作業ツリーでなく、固定基準commitから作るrepository外の一時worktreeで起動する。worktree全体の
読取は許可して発見性を維持するが、編集は作業開始設定の変更可能pathだけに限定する。

道具の可用集合は`Read`、`Glob`、`Grep`、`Edit`、`Write`、`Bash`だけとする。権限方式は`dontAsk`とし、
読取、変更可能pathの編集、固定した完全一致の試験commandだけを事前許可する。未列挙の道具とcommandは
自動拒否する。`bypassPermissions`と`auto`は使わない。

BashはOSの隔離機能を必須にし、利用不能なら起動前停止する。作業worktree以外への書込、隔離外実行、
ネットワーク、Unix socketを許可しない。MCPは空設定に固定し、plugin、hook、skill、Chrome、Web、別agent、
背景agentを無効にする。

## 5. 実行順序

1. 既存の指示文品質入口を一般のコミット済み実装依頼へ適用できるようにする。
2. 機械検査、指示文監査、指示文判定が合格し、必要なHuman裁定が完了した依頼だけを
   `ready_for_executor`にする。
3. 一回限り承認と能力設定を再確認し、一時worktreeを固定基準commitから作る。
4. 同じClaude sessionの第1ターンでは受入試験だけを変更可能にし、機械処理が対象試験の不合格を確認する。
5. 第1ターン後の試験file指紋を固定する。第2ターンではproductionの変更可能pathだけを編集可能にし、
   試験fileの変更を拒否する。
6. 機械処理が対象試験、既存関連試験、変更path、秘密情報、未追跡file、禁止操作を検査する。
7. 合格した場合だけ固定pathを明示stageし、意味単位commitを機械作成する。
8. 基準commitと実装commitから変更一覧を機械生成し、レビュー依頼へ束縛する。
9. `gpt-5.6-terra`の別サブエージェントが独立レビューし、技術的合格後もHuman段完了承認で停止する。

## 6. 受入条件

- `AC-CD-001` コミット済み指示書、固定資料、要求集合、能力設定、Human承認の全指紋が一致する場合だけ
  Claude実装入口を利用できる。
- `AC-CD-002` `ready_for_executor`以外、古い入力、未裁定所見、期限切れまたは使用済み承認は、Claudeの
  process作成前に停止する。
- `AC-CD-003` Claudeの読取発見性を一時worktree内で維持し、主作業ツリーと管理者配置へ書き込ませない。
- `AC-CD-004` 同一sessionの試験作成ターンと実装ターンを分け、RED確認後の試験指紋を固定し、実装ターンの
  試験変更を拒否する。
- `AC-CD-005` 許可した道具、編集path、完全一致commandだけを使え、OS隔離とネットワーク拒否を強制する。
- `AC-CD-006` 未加工結果、起動記録、道具使用記録、変更一覧、検証結果を上書きせず保存し、入力、試行、
  session、commitへ結び付ける。
- `AC-CD-007` 合格した変更だけを機械commitし、反対側モデルの独立レビューとHuman段完了承認を分離する。

## 7. 禁止事項

- `NG-CD-001` 無工具疎通用の承認、payload、全道具無効設定を実装委譲へ流用しない。
- `NG-CD-002` `bypassPermissions`、`auto`、任意Bash、隔離外実行、外部ネットワークを許可しない。
- `NG-CD-003` MCP、plugin、hook、skill、Chrome、Web、別agent、背景agentを有効にしない。
- `NG-CD-004` ClaudeへGit commit、merge、push、tag、履歴書換え、主作業ツリーの変更をさせない。
- `NG-CD-005` 別モデル、別認証、別経路、別送信先への自動切替と、失敗した外部送信の自動再試行をしない。
- `NG-CD-006` Claudeの報告だけで変更範囲、試験合格、レビュー合格、段完了を確定しない。
- `NG-CD-007` ReviewCompass3本体のrepository内容、秘密情報、利用者情報を確認運転で送信しない。

## 8. 停止条件

- `ST-CD-001` 指示文品質、要求被覆、Human裁定、能力設定、承認、固定入力のいずれかが不一致である。
- `ST-CD-002` Claude Codeの版、実行file指紋、認証、要求モデルまたは許容応答モデルが一致しない。
- `ST-CD-003` OS隔離が利用不能、隔離外実行が要求された、または禁止道具・禁止commandが試行された。
- `ST-CD-004` 第1ターンが期待したREDにならない、または第2ターンで試験fileが変わった。
- `ST-CD-005` 許可外path、秘密情報、未解析結果、改竄、余剰・欠落成果物、入力変更を検出した。
- `ST-CD-006` 対象試験、関連試験、独立レビューが不合格、またはHuman段完了承認がない。

## 9. 出力要件

- `OUT-CD-001` 能力設定、開始設定、指示書、固定資料、要求集合のSHA-256と機械検査結果。
- `OUT-CD-002` 試験ターンと実装ターンごとの一回限り起動記録、未加工結果、道具使用記録、receipt。
- `OUT-CD-003` RED結果、固定した試験指紋、GREEN結果、関連試験、秘密情報検査のcommandと終了コード。
- `OUT-CD-004` 基準commit、実装commit、全変更path、変更前後のSHA-256、未追跡fileを持つ変更一覧。
- `OUT-CD-005` `gpt-5.6-terra`の独立レビュー結果、反証、要求別結果、Human段完了承認待ち状態。

## 10. 変更可能範囲案

- `tools/development/`のClaude実装委譲専用moduleとCLI。
- `tools/deployment/installed/`の信頼済み入口のClaude実装用途。
- `tools/deployment/trusted_claude_transport.py`の固定配置検査。
- `docs/development/prompts/`の共通入口。
- `tests/test_claude_implementation*.py`と必要最小限の合成fixture。
- `pyproject.toml`、`AGENTS.md`、`CLAUDE.md`の入口だけ。

既存の`tools/egress/`、Workflow台帳schema、無工具疎通payload、既存承認、既存保存済み応答は変更しない。
既存の共通不変保存処理を再利用し、同形の保存処理を新規作成しない。

## 11. 確認運転

確認運転はReviewCompass3本体でなく、機密を含まない合成Git repositoryを使う。固定した小さな要求に対し、
Claudeが受入試験を先に作り、その後に純粋関数を実装する。Codex主担当は変更せず、機械検証後のcommitを
`gpt-5.6-terra`サブエージェントへレビュー依頼する。

確認運転のClaude起動、固定文、合成repository内容、モデル、道具、command、期限、一回限り承認は、
実装完了レビュー後に別のHuman承認へ束縛する。本範囲固定の承認を実送信承認として扱わない。
