---
source_id: SRC-RC2-CROSS-CUTTING-LESSONS-001
captured_at: 2026-08-02
source_kind: predecessor-project-intent-plan-issue-implementation-and-failure-evidence
normative_status: predecessor-evidence
confidentiality_class: project-internal
raw_snapshot_retained: false
---

# ReviewCompass2横断知見と凍結原因の継承記録

## 1. 位置付け

ReviewCompass2のIntent、Issue、Plan、review、実装、test Evidence、限界記録、凍結判断から、
ReviewCompass3のTask Contract中心設計へ継承する横断原則を固定する。ReviewCompass2は計画の
骨子に問題があるとして凍結されており、未承認のIntent第2版や旧workflowを正本として移植
しない。採用対象は、固定sourceから再構成できる失敗事実、実測、実装Evidence、Human判断、
およびReviewCompass3へ適合させた教訓である。

## 2. 固定source

- repository：`/Users/Daily/Development/ReviewCompass2`
- fixed commit：`d6bbb01500002872c713412bfbd63b702a291c99`
- commit日時：`2026-07-26T20:27:38+09:00`

| artifact | Git blob | SHA-256 | 参照内容 |
|---|---|---|---|
| `FREEZE.md` | `9dfd3eee649d26d5f68ef54b445c2a2d13bcb983` | `be13353fe02224430f48da2467cf76dc33711474fc37d9f8b2c892eff2a48e4f` | 凍結理由、エッセンス抽出と材料構成の欠陥、再開順序 |
| `.reviewcompass/specs/intent-v2-draft.md` | `976a480236e89907716cdb2391a19dfba7370d22` | `17c7a178dc007d1cef5f24d25aa1527523ef56545571e7aaae88492095246a49` | 宣言と強制、停止と復旧、唯一の置き場、失効、棚卸し、対の規定、validator保証 |
| `docs/design/2026-07-25-current-advantages-inventory.md` | `009b14bfb64f737664e5d79b7bc8f00e4d3b9335` | `9166504b79c02cb01af80189082d0c32ad027e3221a5a678ac292d4a767c353d` | 前身より良い設計、訂正4件、係争、境界と非採用の明示 |
| `docs/design/2026-07-25-reference-impl-guarantees.md` | `61a23f7a21566f786557624bf44b2964a5d3e33f` | `72a1e389011ac1b5b15f33cfec92d75ff4e6f01e8402608612acfba1642d9b58` | 1,416実質規則、抽出漏れ、保証主題、post-write工程 |
| `docs/design/2026-07-25-user-decisions-inventory.md` | `1dcc01d296dda479e0a9fd0d5c2ee37003875ceb` | `8ef25d5584ee8033136d2848ea8c84ab8cbec8b2af14246fdec0f99504ee5e64` | Human判断93件、既知陽性42件による抽出規則検証、収束、Intent方針 |
| `docs/design/2026-07-25-review-instruction-guidelines.md` | `503452a8e7cecaefeeaf59e0fbbd571650250994` | `f5508cbefef9283690a995d1cd82f136ad6a75bf60a46ed16d442ae218f203ae` | 材料品質、判定語彙、severity、実データ、根拠不足、段水準、review計測 |
| `docs/design/2026-07-25-red-test-as-acceptance-criteria.md` | `aee9c2088922f43fb7f871c64d10be6385ed4c0c` | `f086bca80f194fca1053a45fb31624e3b2cc1d802f433e455195070d64652e66` | red Test、manual acceptance 7類型、mutation、実装可能性の実測 |
| `docs/design/2026-07-26-session-capture-limitations.md` | `cae6ce923ee956f586774042ec373623385e5a14` | `8d0c56c0464750054619a4ea632d4946a83104b9483741efb4194da2a5bcf567` | 実装済みSession取込みの限界、source消失、共有誤り、mutation実績 |
| `.reviewcompass/backlog/plans/plan-2026-07-25-session-log-capture-tool.yaml` | `ebbd88f3170ce6b9e94bfc93ef492790a4552cd7` | `eaf5dfad6199ad17828c2cb128fdfc6bef0cb37f192f2f2b096788a62a4497c9` | 完了した15 Work、red／green／mutation／manual Evidence |
| `.reviewcompass/backlog/issues/issue-2026-07-26-raw-session-log-preservation.yaml` | `bde92b520268fa4ca42dd22c58435bb7bc3b9e6f` | `0a68f2cbc0e8f3259bb709ed4ed582fa466efd79e4f7e0046b175b1404c5d9bb` | source lifetime、既発生の消失、保全・復旧の未決事項 |

観測時、選択sourceに未コミット変更はなかった。repositoryには別のsession文書一件の変更が
あったため、fixed commitと上表のblob／Digestだけを本記録のsource identityとする。

## 3. 最重要の失敗事実

ReviewCompass2は「前身の保証一覧を作れば移植漏れを防げる」という因果で再構築したが、一覧を
入力へ含めても移植漏れが再発した。材料準備を担う10部品中9部品が一覧へ現れず、規則抽出は
手続き、順序、data flow、入口、閉包を対象にできていなかった。

同じ欠陥は、強制表現5系統のうち1系統だけを抽出した欠落、調査対象25本の欠落、調査主題を
規則だけに限定した欠落として3回発生した。問題を文書へ記録しても、次作業の必須入力として
消費・処置しなかったため再発した。

ReviewCompass3では「一覧の存在」を完了条件にせず、次を満たす必要がある。

- 調査入口とsource universeが列挙されている。
- 関係を展開する規則と停止条件が版付きである。
- 原則、手続き、状態所有、data flow、失敗経路、禁止、非採用、実装保証を別々に探索する。
- 候補全件を`adopt | adapt | reject | defer`へ分類し、未分類を残さない。
- reviewで得た不足とFindingを、次のTask入力または明示的な非採用判断へ結ぶ。
- 要約だけで完了せず、判断を元source、raw Finding、実装またはtestへ戻せる。

この一連を`Evidence Extraction Contract`と`Evidence Consumption Closure`として扱う。

## 4. 採用する横断原則

### 4.1 Assuranceの対と強制被覆

- 宣言した義務または制約を、実行時のvalidator、failure verdict、Workflow permitへ結ぶ。
- 入力を検査するなら、生成・保存した出力も固定対象から再読込して検査する。
- Digestまたは照合値を記録するなら、不一致時に停止する規則を対で置く。
- fail-closedの停止には、停止理由、必要操作、再開条件を持つ復旧入口を対で置く。
- 許可、承認、委譲にはscope、消費、失効、取消し、対象変更時のstale化を対で置く。
- 方法を狭める場合は、Evidenceを失わない代替経路またはHuman escalationを置く。
- 機能を捨てる場合も、その機能が持っていた保証、failure verdict、保存順序、出口を棚卸しする。

Task Contractの各obligationについて、宣言、強制、failure verdict、permit効果、復旧、Evidenceを
`Assurance Obligation Matrix`で検査する。強制できないものは未実装を隠さず、Human判断、
manual acceptance、観測または明示的非採用へ割り当てる。

### 4.2 Validator Assurance

- validator、抽出器、分類器、lint、metric projection自体を検証対象にする。
- 既知陽性、既知陰性、境界fixtureと件数を固定し、未確認領域を明示する。
- validatorの代表的な欠陥を注入し、期待するfalse negativeまたはfalse positiveを検出する。
- mutationが実際に対象挙動を壊したことを先に確かめ、単なるcode変更をmutation成功としない。
- producerとvalidatorが同じhelperまたは同じ誤った仮定を共有する場合、独立oracleまたは実データ
  照合を追加する。
- validator version、fixture、source universeが変われば旧verdictをstaleにする。

### 4.3 Review Quality Contract

- review verdict、severity、出力schemaを品質確認済みtemplateへ固定する。
- severityは対象自体の重要さではなく、欠落または矛盾が与える影響へ付ける。
- `insufficient_evidence`を正規の結果とし、推測で埋めない。
- 対象Stageの水準を越える所見を`out_of_level`として保持し、捨てずに適切な上流・下流へrouteする。
- 参照実装を正解と仮定せず、現行が別の強い保証を持つ場合を分類できるようにする。
- riskと目的に応じ、代表実データまたはfixtureをreview材料へ含める。
- 材料の適格性、閉包、独立性が未保証なら、成立していない層をEvidenceへ明記する。
- 全文、差分、impact sliceの費用を事前仮定せず、対象／材料比、token、時間、Finding品質で測る。

### 4.4 Convergenceとpost-write verification

- 初回Findingゼロだけを合格根拠にせず、Context adequacy、Prompt／template、validator Evidenceを
  確認する。
- roundごとに新規意味Finding、表現Finding、反映起因Finding、残余Findingを区別する。
- round上限到達時は残余Findingを削除せず、継続、accept-with-known-risk、改定、中止をDecision
  Authorityへ返す。
- 書込みを伴うTaskは、固定Expected Outputに対して保存後の実体を再読込するpost-write
  verificationをriskに応じてVerification Planへ含める。
- post-write verdictが必須の場合、合格前に`verified`または`accepted`へ進めない。

## 5. 実装Evidenceから採用するもの

Session取込みPlanは15 Workが完了し、red／green Evidence、11項目のmutation、実データ353本の
取込み、364件の再生成照合を持つ。この結果から次を採用する。

- raw source、機械可読転写、人向け要約を別identity、保存境界、retentionで扱う。
- 追記されるsourceは取り込んだ範囲を固定し、追記、非追記変更、消失を区別する。
- sourceの実効retentionと消失条件を取得・観測し、capture deadlineと`source_missing |
  source_expired | non_reconstructable`を区別する。
- 保存したことだけで完了せず、保全先からのrestoreとDigest照合を検証する。
- capture triggerは忘却を減らすが保全の代替ではない。trigger失敗は作業を不必要に妨げず、
  失敗を観測可能にする。
- 実データで次工程が前工程の欠陥を見つけることを前提に、局所testだけで完了としない。

## 6. 修正して採用するもの

- Intentは人が理解しやすい目的、利用者、作るもの、作らないもの、前提、衝突基準を保つ。
  ReviewCompass3ではAI支援や限定委譲を一律禁止せず、Humanが委譲範囲を決める現方針を維持する。
- 「現在地を保存せずeventから導出する」は、component state ownershipとdurable recoveryに適合
  させる。authoritative event projectionとmaterialized stateのどちらを正本にするかはDesign
  Decisionで決め、不整合を検出不能な二重正本を作らない。
- red Testを実行可能Evidenceとして重視するが、Task ContractとPlanから期待、境界、禁止、
  oracleを消さない。Testで表現できない事項には型付きmanual acceptanceとownerを置く。
- multi-reviewer数、round上限、timeout、retryは固定値を継承せず、risk、能力、費用の実測から
  Verification ProfileとPolicyで選ぶ。

## 7. 採用しないもの

- 未承認のIntent第2版をReviewCompass3の規範正本として扱うこと。
- 凍結された再構築Planを成功済みの開発計画として扱うこと。
- `sdd | maintenance | reopen`の旧3 lane、単一状態台帳、旧gate名を復活させること。
- Human以外の意味判断を一律禁止する旧境界。
- Acceptance Test参照だけをPlanの意味正本にすること。
- reviewer数3、round数2、45KB、30日などの環境・製品固有値を固定Requirementにすること。
- Claude固有path、hook名、log formatを製品共通設計へ持ち込むこと。

## 8. Evidenceの限界

ReviewCompass2のIntent第2版、優位点一覧、保証一覧の一部はHuman未承認であり、凍結理由からも
網羅性を主張できない。review Evidenceには同一model・subagent経路のものがあり、model独立性を
一般化できない。Session取込みは実装済みだが単一provider dataであり、二つ目のprovider adapterで
境界の妥当性を検証していない。

したがって本記録も前身のエッセンス全体を網羅した一覧ではない。選択source、抽出観点、既知の
未確認領域を明示したReviewCompass3側の一回の入力であり、今後の調査Findingは本記録を上書き
せず新versionまたは後継recordへ追加する。
