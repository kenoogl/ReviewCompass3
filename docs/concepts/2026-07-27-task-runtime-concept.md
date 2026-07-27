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
- **source universe**：Review Taskが材料を探索・検査する、根拠を固定した母集合。
- **Scope contract**：source universeから対象範囲を決める規則、閉包、
  除外理由、未確定時の扱いを示す契約。
- **Execution Context**：特定のReview Taskを実行するために確定した入力単位。
- **Harnessed Execution**：実行主体、Prompt、Tool、Validation、Retry、Loggingを
  Task固有の契約に従って制御する実行。
- **Review Run**：固定したExecution ContextとHarness contractに対する、
  一つのReview Taskの実行と判断の記録単位。
- **Attempt**：一つのReview Run内で、同じ固定条件に対して行う個別の実行試行。
- **Retry**：失敗したAttemptと同じ固定条件で、新しいAttemptを追加すること。
- **Finding**：証拠単位への参照を持つレビュー上の主張。Review Runの最終結果は、
  採用、却下、未解決を含むFinding集合として扱い、空集合も明示する。
- **Operational Provenance**：Task入力から最終Findingまでの実行上の来歴。
- **外部provenance reference**：Task Runtime外にあるセッション、変更、
  成果物などの証跡へ接続する参照。対象identity、内容Digest、解決規則、
  信頼境界、検証結果を持つ。

## 原理Aとの関係

Task Runtimeは原理Aの役割分離を実装する境界である。

- LLMは、文章読解、意味判断、Findingや対応案の起草を担う。
- 機械処理は、材料の列挙・実体化、Digest、Scope・Schema・被覆検査、
  状態遷移、保存、再実行条件、権限制御を担う。
- Humanは、目的、承認、裁定、Findingの最終的な採否を担う。

外部Toolは最終判断を持たない。実行単位ごとに、機械処理を行うToolか、
LLMを含む意味処理を呼び出すToolかを明示し、それぞれの責務に従わせる。
決定性は責務とは別の属性として扱う。検索APIや時変データ取得などの
非決定的なToolも、入力、版・環境、出力、Validation、Retry条件を
Harness contractと来歴へ記録する。

LLMは材料候補やRetry案を提示できるが、材料の採用、完全性の宣言、
Validationの通過、Retryの開始、Review Runの完了を決定しない。
Task契約に基づく機械判定で決まらない事項はHumanが承認または裁定し、
その対象と理由を記録する。材料選択、実行経路、完了条件をLLMの推論だけに
埋め込まない。

## Review Task

Review Taskは単なる処理名ではなく、少なくとも次の意味を持つ必要がある。
具体的な必須フィールドとSchemaはrequirements以降で確定する。

- Goal
- Target
- Constraints
- Expected Output
- Context Requirements
- Validation Policy
- Upstream Provenance References

WorkflowはReview Taskの目的と境界を示し、Task Runtimeはその内部実行を担う。
Upstream Provenance ReferencesはReview Taskへ与えられた外部証跡であり、
実行後に生成されるOperational Provenanceとは区別する。

## Execution Context

Execution Contextは会話履歴全体やプロジェクト内の全資料ではない。
特定のReview Taskについて、次を一つの検証可能な入力単位として確定したものを指す。

- Target
- source materials
- Task criteria
- source universe identity
- Scope contract
- 完全性判定結果
- 出力要件

Execution ContextはPromptから分離して保持する。これにより、材料の変更と
Prompt表現の変更を区別する。

source universeの固定manifestまたはDigest、Scope contract、完全性判定結果を含む
Execution Contextの内容を固定した識別を**Execution Context identity**とする。
Prompt、Harness contract、Validation、モデル条件まで含め、実行に有効な条件を
固定した識別を**effective execution identity**とする。同じレビュー材料の比較は
前者を、同じ実行条件の比較は後者を使う。

Digestが直接保証するのは、規定した直列化規則に基づく内容の同一性と
改変検知である。材料の完全性、出所の真実性、実際の送信、モデルによる
因果的利用までは保証しない。これらはScope検査、出所記録、送信境界で
確定したpayload、関係辺の検査など、別の証拠によって示す。

## Context Composition

Context Compositionは、Task固有の入力構成を明示化し、Execution Contextとして
確定する処理である。

完全自律的な材料探索・採用を前提としない。当面は、WorkflowまたはHumanが
Task契約に基づいてTargetと材料候補を提示し、Task Runtimeが実体化、
完全性検査、Scope検査、Schema検査、Digest固定を行う。機械判定で採用を
確定できない材料はHumanへ戻す。将来、候補探索を支援する場合も、
候補の提示と採用決定を区別し、採用理由を記録する。

完全性は、固定したsource universeとScope contractに対してだけ判定する。
Scope contractは、母集合の根拠、範囲を閉じる規則、除外理由を保持する。
母集合または範囲を確定できない場合は完全とせず、停止またはHuman判断へ戻す。
未提示の関連材料をDigestだけで検出できるとは扱わない。

## Harnessed Execution

Harnessed Executionは、Task、Target、実行目的に応じて次を管理する。

- 実行主体と実行トポロジ
- Prompt manifest
- モデルまたはToolへの入力と出力
- Validation
- Retry
- Logging
- Humanの承認停止点と最終判定

Harness contractでは、Runtimeとコードの版、Providerとモデルの識別、
推論条件、Tool、Prompt、Policy、Schema、実行者、時刻の記録方法など、
出力に影響する条件を固定する。単独LLM、複数LLMの独立レビュー、
Toolによる検査、Humanによる裁定などを、Review Runの明示的な構成として扱う。

外部API送信前には、実際に送信する直列化payloadを先に確定し、Digestを付与する。
機械的な機微情報検査とHuman承認を独立した関門として置き、両方を同じpayload
Digestへ束縛する。Human承認はExecution Context、Prompt、Harness contractの
各Digestにも束縛する。payload、検査結果、承認判断、送信Attempt、
実送信結果をOperational Provenanceへ記録する。

## Review RunとOperational Provenance

一つのReview Runは、一つのExecution Context identityとeffective execution
identityを固定し、その下へAttemptを追記する。失敗した担当を同じ固定条件で
再試行する場合は同じRun内のRetryとする。source universe、材料、Prompt、
Harness contract、Validationまたはモデル条件を変更した場合は新しい
Review Runを開始し、変更理由と前Runへの関係を記録する。

各Review Runでは、少なくとも次の記録候補を関連づける。

- source universeとScope contract
- Task criteria
- Target
- source materials
- 外部provenance reference
- Execution Context
- Prompt manifest
- 実行主体と実行トポロジ
- Harness contractとeffective execution identity
- 直列化した送信payload、機微情報検査、Human承認
- モデルまたはToolへの入力と出力
- Validation結果
- Retryと変更理由
- Triage
- Humanの最終判断
- 最終Finding集合

各記録は、一意ID、内容Digest、限定された平文の関係種別を分けて持つ。
Digestは記録内容の同一性を、関係種別は辺の意味を表す。次の鎖について、
参照先の存在、内容、関係の種類を機械検証できるようにする。
外部provenance referenceを解決できない場合、内容Digestが一致しない場合、
または信頼境界を検証できない場合は、鎖を検証済みにせず停止または
Human判断へ戻す。

```text
session / change / artifact evidence
  → external provenance reference
  → Review Task
  → Execution Context
  → Harness contract
  → serialized outbound payload
  → sensitive-information inspection for payload digest
  → Human approval for the same payload digest
  → Attempt
  → delivery result / raw output
  → Validation
  → Triage
  → Human decision
  → final Finding set
```

各Findingの主張とHuman decisionは、Execution Context内の安定した証拠単位への
参照と採否理由を持つ。参照先がExecution Context内に存在し、内容が一致することを
検査する。採用されなかったFinding、空の最終Finding集合、失敗したAttemptも
消さずに残す。

新しいReview Runでは、source universe、材料、Prompt、Harness contract、
Validationまたはモデル条件の何を、なぜ変更したかを前回Runへ結線する。
同じRun内のRetryでは、固定条件を変えず、失敗Attemptとの関係を記録する。

## 現行実装との対応

第1段のブートストラップreview基盤には、レビューTask向けの縦切りとして
次が実装されている。根拠は固定commit、実装箇所、テストを結んだ
`records/intent/task-runtime-current-implementation-evidence.json`へ分離する。

- source universeと材料役割の明示
- 本文を含む材料束とDigest
- 材料被覆、原文一致、stale検査
- Targetと材料を含み、承認フラグと対象Digestが一致する閉鎖payload
- Prompt・出力Schema・入力payloadの分離とDigest
- main・independentへの同一入力配布
- write-once APIによるraw応答と失敗診断の保存、およびDigest付与
- 厳格な出力Schema解析
- Triage
- 成功済み成果を保持した失敗担当の再実行

現行の閉鎖payloadが検証する承認フラグは、Humanの識別、承認操作、理由を
証明する承認証跡ではない。

ただし、現行実装は固定されたブートストラップレビュー用pipelineであり、
汎用的なTask Runtimeではない。主な不足は次である。

- 第一級のReview Task定義
- 成果物種別と実行目的に応じたContext Composition
- 可変の実行トポロジとHuman判定主体
- Task固有のValidation PolicyとRetry Policy
- Findingが参照する材料のExecution Context内存在検査
- HumanによるFinding採否と最終Findingの記録
- Run全体を束ねるroot digestと再実行間の来歴
- raw応答と失敗診断の作成後改変を検出する再照合
- 送信直前payloadと事前検査・Human承認・実送信結果の結線
- WorkflowからTask内部処理を分離する共通Runtime境界

## 後続段への送り

requirementsでは、外部から観測できるTask Runtimeの振る舞い、入出力、
停止・復旧条件、保存する証跡、受け入れ条件を定める。

designでは、Review Task、Execution Context、Review Run、各PolicyのSchema、
Runtime境界、保存配置、Digest連結方法を定める。

ブートストラップ実装の現状にrequirementsやdesignを合わせず、確定したintentから
必要な契約を導き、既存実装を`conformant / adapt / replace / defer`へ分類する。
