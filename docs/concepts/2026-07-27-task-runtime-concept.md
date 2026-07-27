---
lifecycle: provisional
normative_status: non-normative
promotion_required: true
---

# Task Runtime概念整理

## 位置付け

本文書は、ReviewCompass3で検討するTask Runtimeの概念、現行実装との対応、
後続段で決める必要がある事項を整理した非規範の検討資料である。
フィールド、Schema、処理順序、採用技術を確定するものではない。

## 背景

LLMを検索、外部Tool、記憶、人との対話に組み合わせると、複数段階の知的作業を
実行できる。一方、必要な材料や実行経路をPromptやLLMの推論へ暗黙に埋め込むと、
結果がどの入力と条件から生まれたかを再現・監査しにくい。

同じ「成果物間の整合性をレビューする」という目的でも、レビュー対象によって
必要な材料は異なる。

- 要求のレビューでは、上位の意図、関連Feature、他の要求が主要な根拠になる。
- 実装のレビューでは、設計、Task記述、変更差分、テスト結果が主要な根拠になる。
- 修正後の再レビューでは、前回Finding、修正差分、未解決事項との対応が主要な
  根拠になる。

材料準備、複数モデルへの分配、人の判定、出力検証、再試行を対象ごとに
上位Workflowへ展開すると、業務上のTaskとTask内部の実行処理が混在する。
Task Runtimeは、このTask内部の実行処理を明示的に管理する境界として扱う。

## 対象範囲

Task Runtimeは、ReviewCompass3が扱うレビュー支援へ適用する。
要求、設計、Task記述、実装などの成果物間の整合性を、Human、複数のLLM、
外部Toolが協調して確認するReview Taskを対象とする。

汎用エージェント基盤や、LLMによる完全自律的な作業計画を目的としない。

## 用語

- **Review Task**：レビューの目的を持つ意味的な実行単位。
- **Task記述**：SDDで実装作業を記述する成果物。Review Taskとは区別する。
- **Execution Context**：特定のReview Taskを実行するために確定した入力単位。
- **Harnessed Execution**：実行主体、Prompt、Tool、Validation、Retry、Loggingを
  Task固有の契約に従って制御する実行。
- **Review Run**：一つのReview Taskについて実施した実行と判断の記録単位。
- **Operational Provenance**：Task入力から最終Findingまでの実行上の来歴。

## 原理Aとの関係

Task Runtimeは原理Aの役割分離を実装する境界である。

- LLMは、文章読解、意味判断、Findingや対応案の起草を担う。
- 機械処理は、材料の列挙・実体化、Digest、Scope・Schema・被覆検査、
  状態遷移、保存、再実行条件、権限制御を担う。
- Humanは、目的、承認、裁定、Findingの最終的な採否を担う。

材料選択、実行経路、完了条件をLLMの推論だけに埋め込まない。

## Review Task

Review Taskは単なる処理名ではなく、少なくとも次の意味を持つ必要がある。
具体的な必須フィールドとSchemaはrequirements以降で確定する。

- Goal
- Target
- Constraints
- Expected Output
- Context Requirements
- Validation Policy
- Provenance

WorkflowはReview Taskの目的と境界を示し、Task Runtimeはその内部実行を担う。

## Execution Context

Execution Contextは会話履歴全体やプロジェクト内の全資料ではない。
特定のReview Taskについて、次を一つの検証可能な入力単位として確定したものを指す。

- Target
- source materials
- Task criteria
- Scope contract
- 出力要件

Execution ContextはPromptから分離して保持する。これにより、材料の変更と
Prompt表現の変更を区別する。入力内容をDigestで固定し、複数のレビュー主体へ
同じ入力が渡されたことを機械検証できるようにする。

## Context Composition

Context Compositionは、Task固有の入力構成を明示化し、Execution Contextとして
確定する処理である。

完全自律的な材料探索・採用を前提としない。当面は、呼出側がTargetと材料候補の
多くを明示し、Task Runtimeが実体化、完全性検査、Scope検査、Schema検査、
Digest固定を行う。将来、候補探索を支援する場合も、候補の提示と採用決定を区別し、
採用理由を記録する。

## Harnessed Execution

Harnessed Executionは、Task、Target、実行目的に応じて次を管理する。

- 実行主体と実行トポロジ
- Prompt manifest
- モデルまたはToolへの入力と出力
- Validation
- Retry
- Logging
- Humanの承認停止点と最終判定

単独LLM、複数LLMの独立レビュー、Toolによる検査、Humanによる裁定などを、
Task Runの明示的な構成として扱う。

## Review RunとOperational Provenance

各Review Runでは、少なくとも次の記録候補を関連づける。

- Task criteria
- Target
- source materials
- Execution Context
- Prompt manifest
- 実行主体と実行トポロジ
- モデルまたはToolへの入力と出力
- Validation結果
- Retryと変更理由
- Triage
- Humanの最終判断
- 最終Finding

各記録をDigestで結び、次の鎖を検証できるようにする。

```text
Review Task
  → Execution Context
  → Harness contract
  → Attempt
  → raw output
  → Validation
  → Triage
  → Human decision
  → final Finding
```

再実行時には、材料、Prompt、実行契約、Validationの何を、なぜ変更したかを
前回Runへ結線する。採用されなかったFindingや失敗したAttemptも消さずに残す。

## 現行実装との対応

第1段のブートストラップreview基盤には、レビューTask向けの縦切りとして
次が実装されている。

- source universeと材料役割の明示
- 本文を含む材料束とDigest
- 材料被覆、原文一致、stale検査
- Targetと材料を含む承認済み閉鎖payload
- Prompt・出力Schema・入力payloadの分離とDigest
- main・independentへの同一入力配布
- raw応答と失敗診断の不変保存
- 厳格な出力Schema解析
- Triage
- 成功済み成果を保持した失敗担当の再実行

ただし、現行実装は固定されたブートストラップレビュー用pipelineであり、
汎用的なTask Runtimeではない。主な不足は次である。

- 第一級のReview Task定義
- 成果物種別と実行目的に応じたContext Composition
- 可変の実行トポロジとHuman判定主体
- Task固有のValidation PolicyとRetry Policy
- Findingが参照する材料のExecution Context内存在検査
- HumanによるFinding採否と最終Findingの記録
- Run全体を束ねるroot digestと再実行間の来歴
- WorkflowからTask内部処理を分離する共通Runtime境界

## 後続段への送り

requirementsでは、外部から観測できるTask Runtimeの振る舞い、入出力、
停止・復旧条件、保存する証跡、受け入れ条件を定める。

designでは、Review Task、Execution Context、Review Run、各PolicyのSchema、
Runtime境界、保存配置、Digest連結方法を定める。

ブートストラップ実装の現状にrequirementsやdesignを合わせず、確定したintentから
必要な契約を導き、既存実装を`conformant / adapt / replace / defer`へ分類する。
