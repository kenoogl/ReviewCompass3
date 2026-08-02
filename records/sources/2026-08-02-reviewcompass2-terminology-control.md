# ReviewCompass2用語統制の参照記録

## 1. 目的

ReviewCompass2で運用された用語集、用語統制方針、用語追加時の失敗記録、レビュー方式の
語彙改定を、ReviewCompass3用語集へ適合させるための固定参照として記録する。前身文書を
ReviewCompass3の正本として直接利用せず、採用、修正採用、置換、非継承を明示する。

## 2. 固定source

観測元repository：`/Users/Daily/Development/ReviewCompass2`

| source | blob | SHA-256 |
|---|---|---|
| `.reviewcompass/specs/glossary.md` | `ee88e97a1630a67cc9433cd6321f3ea36f0c4d84` | `55f2a159378f0d690aabb996b888830fc172f8a543ac94a479f1859d96774485` |
| `.reviewcompass/backlog/issues/issue-2026-07-23-reopen-intent-terminology-and-code-consolidation-amendment.md` | `4519ea781c4d4bde74a356565e8ee85d02a3c036` | `053ae984d0652af03d0d3a4bc998558f109581b3f2e768efa0f5f2985a40512f` |
| `docs/design/2026-07-26-glossary-additions-for-intent-v2.md` | `e22ccd77297f4f10ff2e713a976de7cc9c0cec5d` | `b385c43261d4456ed3ffd775d667ab7c048b16dd9c4059fd99782a4633dd5bc5` |
| `.reviewcompass/backlog/issues/issue-2026-07-25-f2-review-method-vocabulary-alignment-amendment.md` | `3a9dd06ce691f33b1e764e77a77f8c2609a299ea` | `c5820ba3536da5bd2a1043fc852def1995c2be4102efbdf4767952765f59e722` |

ReviewCompass3内のtree Evidenceは
`records/reference-baselines/2026-07-27/reviewcompass2-d6bbb015.git-tree.txt`に保持されている。

## 3. 前身から維持する原則

- domain固有語は使用前に定義し、未定義の造語を増やさない。
- 一つの概念には一つのcanonical termを割り当て、表示名と機械名を対応付ける。
- 定義の意味変更、alias、retirementを履歴として残す。
- 文書、schema、設定の閉じた語彙を混同せず、正の登録先を明示する。
- 利用者向け表示には平易な語を使い、内部command名を操作語として要求しない。
- 同じ「独立」など、複数の意味を持つ語は属性を分けて定義する。
- 過去文書を新語へ合わせてin-place変更せず、読み替えと適用範囲を残す。

## 4. ReviewCompass3向けに修正する原則

- 全単語を登録対象にせず、domain概念、成果物名、役割、状態、関係、schema値を対象とする。
- 散文用語集は人が意味を理解する正本とし、機械が許可するenum値の正本は対応schemaまたは
  Policyに置く。用語集だけから実行時allowlistを生成しない。
- 日本語の表示名と英語のcanonical tokenを対にし、散文で不要な日英混在を減らす。
- Task Contract、Work Item、二つのwork origin、fresh／reopen continuation、component所有state、
  Decision Authorityを現在のworkflowとして定義する。
- 用語検査は、登録対象を識別できる構造化参照から始める。自由文の全語を完全照合できるとは
  仮定しない。

## 5. 置換する旧定義

| ReviewCompass2 | ReviewCompass3での扱い |
|---|---|
| 6段SDD | IntentからRelease Evaluationまでの7 stageへ置換 |
| SDD本筋／reopen／maintenanceの3 lane | `work_origin`と`continuation_mode`の直交分類へ置換 |
| Task記述 | 版付きTask Contractへ置換 |
| 案件 | Delivery Work ItemまたはIssue Recordへ責務を分離 |
| 単一状態台帳 | component所有stateと追記型Operational Provenanceへ置換 |
| 承認停止点 | Decision Authority、Decision Record、Workflow permitへ分解 |
| 代理判定 | 能力EvidenceとDelegation Authorizationに基づく段階的AI判断委譲へ置換 |
| 共通ルーチン台帳だけでの探索 | Source Symbol Index、Reusable Routine Ledger、実codeの三者照合へ拡張 |
| deploy-manifest | Deployment Manifest、Project Manifest、Binding、論理rootへ分解 |

## 6. 非継承または保留

- 旧gateの固定5値、review-wave、旧単一台帳のpathは現行workflowへ継承しない。
- 原理A〜Cという略号は、その内容が現在のIntentと計画へ個別に解決されているため現行用語に
  しない。
- 単位ファイル、主従逆転、旧レビュー方式の要素／組み立ての全語彙は、現行Requirementsで
  必要になるまで登録しない。
- 前身の具体的なpath、ID例、model数、送信sizeなどは定義へ持ち込まない。

## 7. 制約

この記録は前身sourceの存在と適合判断を保持するEvidenceであり、ReviewCompass3の用語正本
ではない。ReviewCompass3で使用する定義は統合用語集の現行versionを参照する。
