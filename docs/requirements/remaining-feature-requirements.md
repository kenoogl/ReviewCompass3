---
lifecycle: provisional
normative_status: non-normative
promotion_required: true
---

# ReviewCompass3 残機能 requirements

本書は`FEAT-REVIEW-CONTEXT`以外の8機能を対象とする。各要件の入力、出力、
停止条件、復旧条件、失敗時保存、受け入れ条件、対象外および由来は
`records/requirements/remaining-batches-0002-0009.json`へ固定する。

## Harnessed review execution

- `REQ-EXEC-001`：固定実行仕様と許可状態順序に従うReview Runだけを開始する。
- `REQ-EXEC-002`：外部送信の内容、能力、論理送信先、Human承認を同じ
  実行identityへ束縛する。
- `REQ-EXEC-003`：provider raw応答と解析試行を分離し、送信条件から追跡する。
- `REQ-EXEC-004`：複数担当の実行トポロジとround結果を欠落なく記録する。
- `REQ-EXEC-005`：出力検証と形式復旧を版付きで管理し、意味を変える復旧を拒否する。
- `REQ-EXEC-006`：実行条件と観測値を不変記録し、再試行・再利用根拠を監査可能にする。

Harnessは観測値、条件、raw結果の取得と不変記録を所有する。観測の意味的評価は
Evidence Evaluationへ渡す。

## 所見統合とHuman判断

- `REQ-TRIAGE-001`：担当別結果を件数と結論を失わず要約する。
- `REQ-TRIAGE-002`：複数modelの所見を重複と競合を保って統合する。
- `REQ-TRIAGE-003`：Findingの最終採否をHuman判断として対象と内容へ束縛する。

## 意味単位と来歴追跡

- `REQ-TRACE-001`：意味単位と関係を閉じた語彙とID参照で固定する。
- `REQ-TRACE-002`：上流義務と下流成果物を順逆追跡し、受け先なしを拒否する。
- `REQ-TRACE-003`：共有データ境界を決定的validatorでfail-closedに検査する。

## セッション記録ライフサイクル

- `REQ-SESSION-001`：利用者が明示した範囲からセッション取込を安全に起動する。
- `REQ-SESSION-002`：生ログを保全し、伏字化転写・要約・来歴へ結ぶ。
- `REQ-SESSION-003`：追記と改変を区別し、転写変異を検出する。

## Workflowと作業単位の制御

- `REQ-WORKFLOW-001`：現在対象、作業単位、backlog、進行段階を一意IDで結線する。
- `REQ-WORKFLOW-002`：作業状態、許可遷移、関門を状態機械で管理する。
- `REQ-WORKFLOW-003`：成果物書込みを進行中作業単位と承認actionへ束縛する。

## ポータブルな配置と運用

- `REQ-PORTABLE-001`：設定、データ、成果物の配置を主要OSで移植可能に解決する。
- `REQ-PORTABLE-002`：構造化成果物を安全に読書きし、部分失敗から復旧する。
- `REQ-PORTABLE-003`：配布、導入、運用、解除を所有境界と利用者データ保護の下で行う。

## 証拠付き評価と分析

- `REQ-EVAL-001`：固定対象へ明示基準を適用し、適合性を証拠付きで評価する。
- `REQ-EVAL-002`：Harnessの観測値へ基準を適用し、結果と解釈限界を分離する。
- `REQ-EVAL-003`：評価と分析を再現可能なpackageへ固定し、限界を保持する。

Evidence Evaluationは基準適用、結果および解釈限界を所有し、観測値そのものを
変更しない。

## 実測に基づく自己改善

- `REQ-IMPROVE-001`：成功と失敗の実測を条件付き学習材料として蓄積する。
- `REQ-IMPROVE-002`：改善候補を検証し、Human承認後だけ次周期へ反映する。
