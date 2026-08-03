---
candidate_id: RC3-WORK2-INTENT-GLOSSARY-2026-08-03-V1
generated_at: 2026-08-03T14:56:34+09:00
stage: initial-development
work: Work 2
status: human_decision_pending
decision_authority: human
confidentiality_class: project-internal
metadata_correction:
  corrected_at: 2026-08-03T15:44:34+09:00
  decision_id: DEC-WORK2-CANDIDATE-TIMESTAMP-2026-08-03-V1
  previous_generated_at: 2026-08-03T14:35:03+09:00
  previous_sha256: 2666511bcf95a2fdc5237257b5c5e38fbc7dc1c80fd829064b02e34b759e6ab9
  reason: replace reused Work 1 approval time with verified Work 2 session boundary
---

# Work 2 Intent・統合用語集 Human判断候補 V1

## 1. 判断対象

次の現行候補を、ReviewCompass3のIntentと統合用語集として承認するか判断する。

| role | path | SHA-256 |
|---|---|---|
| Intent候補 | `docs/current/reviewcompass3-intent-current.md` | `1950f5a37fb5d0d0554f56343b39bbca7fc635523409f10ee761d8cef68f9ec6` |
| 統合用語集候補 | `docs/current/reviewcompass3-glossary-current.md` | `f1e7e9a9c57292fe911217d9b4f5d5b8ed99a881d6f113f9b60db1f0d01b19fa` |
| 現行Plan候補 | `docs/current/reviewcompass3-plan-current.md` | `0ae6bef979192b008a8a71fc090f709279c4bd1f0db159f9faadf947e929156f` |

固定入力はWork 1 corrective snapshotのcommit
`ee60e3b4baf74c60da949a9d04d793fb83a61e69`から再構築できる。Planの`intent_ref`と`glossary_ref`、
corrective snapshotの3 artifact Digestは上表と一致した。

## 2. Intent照合結果

### 目的

AIを利用した開発について、資料、作業、review、Human判断、Testを結び、判断根拠、判断主体、権限を
後から確認できる状態を作る。記録量そのものを目的にせず、必要な材料と重要な判断を失わず、安全に
開発を継続できることを目的とする。

### 主な利用者

AIの支援を受けながら一人でsoftwareを開発・保守し、自分で判断するか、能力を確認した範囲だけAIへ
明示的に委譲する開発者である。利用者は内部実装を知らなくても、現在地、確認済み・未確認、Human判断
地点、委譲範囲、復旧入口、完了根拠を理解できることを求める。

### 非目標

- AIへ目的、最終判断、完了判断を無条件または無制限に委ねない。
- 会話履歴や全資料を暗黙入力にせず、不足を推測で補わない。
- ReviewCompass3を汎用自律AI基盤にしない。
- 特定AI、開発app、OS、保存場所へ製品全体を固定しない。
- 文書数、Test数、記録数の多さだけを品質としない。
- 実装から生成した説明を上位Requirementの正本へ自動昇格しない。

### authority境界

| actor | 有効な責務 | 越えてはならない境界 |
|---|---|---|
| Human | 製品の存在理由とPolicy、委譲の設定・変更・停止・取消し、外部送信・不可逆判断を確定する | 明示DecisionなしにAIまたは機械が代行しない |
| AI | 理解、案作成、review、別視点を提示し、有効なDelegation Authorization内だけ限定判断する | 自分への委譲を発行・拡張・延長・再有効化せず、範囲外判断を確定しない |
| 機械処理 | 列挙、照合、欠落検査、state管理、保存、再開、安全確認、委譲scope・期間を検査する | 未定義の意味裁量で不足を補完せず、Human／AIの意味判断を置換しない |

初期開発ではDelegation Authorizationを発行せず、全decision classをHuman modeで扱うというPlanの
境界と一致している。

## 3. 統合用語集照合結果

機械照合でcanonical token 109個を抽出した。重複tokenは0、Work 2で必要な次の13語の欠落は0だった。

```text
intent
terminology_control
task_contract
decision_authority
decision_record
delegation_authorization
machine_process
human_only
improvement_candidate
session_log_bootstrap
current_work_projection
execution_claim_verification
completion
```

旧語の読み替えは、旧6段SDD、Task記述、単一状態台帳、代理判定、曖昧なTask／Plan／完了／AI・LLMを
含む8境界を確認した。Work 2のIntentとauthority境界を表すために必要な未登録domain用語はなく、
用語集本文への追加差分は不要である。

## 4. Provenance上の既知事項

Intentと用語集の`generated_from`には、同じpathの過去内容Digestが2件残る。これらは現行authority参照
ではなく、Work 1で既にv16の未達forward snapshotとして`digest-only`履歴へ分類された。Work 1は
corrective snapshotとpost-commit verificationにより、現行3文書をcommit `ee60e3b`へ固定済みである。

したがって、本判断は再構成可能な現行Digestを対象とする。過去`generated_from`を現行内容へ単純置換せず、
既知履歴を消さない。この残余riskを越えて旧生成途中内容を根拠にした主張は行わない。

## 5. 機械照合結果

```text
audit: passed
Intent required sections: 8 / 8
authority boundaries: 3 / 3
registered canonical tokens: 109
required tokens: 13 / 13
missing tokens: 0
duplicate tokens: 0
legacy mappings: 8 / 8
```

文書・調査工程のため形式的RED／GREENは適用していない。現行Intent、用語集、Plan本文は変更していない。

## 6. Human判断候補

### 選択肢1（提案）

上表のIntent候補と統合用語集候補を内容Digestに束縛して承認する。承認後、別Decision Recordで対象、
Digest、範囲を固定し、promotion metadataの扱いとWork 3への進行を更新する。

### 選択肢2

承認せず、変更が必要な節、用語またはauthority境界を具体的に指定する。指定内容は現行候補をin-placeで
確定扱いにせず、後継候補と影響閉包として扱う。

## 7. 現在の判定

Intent、利用者、非目標、Human／AI／機械のauthority境界はHuman判断可能な粒度で固定された。Work 2で
必要なdomain用語は統合用語集へ登録済みである。技術的なblocking conflictはなく、残る関門はHumanによる
選択肢1または2の判断である。本候補だけではIntentまたは用語集を承認済みへ昇格しない。
