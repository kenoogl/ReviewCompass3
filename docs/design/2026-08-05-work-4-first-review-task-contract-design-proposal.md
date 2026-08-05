# Work 4：最初のReview Task Contract設計提案

状態：`approved_for_implementation`
対象：Current Plan §13の「最初のTask Contract」
基準文書：`docs/current/reviewcompass3-plan-current.md`（Work 4、4A、4B、5A、6A、§13、§17）、
`docs/design/2026-08-02-task-contract-design-amendment.md`、
`docs/development/2026-08-02-development-policy.md`、
`records/development/2026-08-05-work-4a-early-completion-and-4b-decision-v1.md`
Requirement正本：`records/requirements/authority/rc3-requirements-authority-2026-08-03--v2.json`（50件）

**これはDecision Recordではない。**承認記録は`DEC-WORK4-FIRST-REVIEW-CONTRACT-DESIGN-001`である。
Humanは2026-08-05に本提案を承認し、§9の五点を固定した。Work 5Aの実装範囲はこの提案に限る。
§11のE2〜E7は`deferred`であり、E2、E4、E5の開始にはそれぞれ別途Human判断が必要である。

## 1. 対象scenario、利用者、入力、出力、非目標

### 1.1 対象

| 項目 | 内容 |
| --- | --- |
| scenario | `new_development / fresh`だけ（`REQ-WORKFLOW-005`の二軸のうち一組合せ） |
| Contract type | Review Task Contract一種類のみ |
| review対象 | ReviewCompass3自身の小さな**文書変更**一件。code、schema、policyを対象にしない |
| 利用者 | ReviewCompass3の開発者（Human）。判断はHuman modeで行い、委譲しない |
| reviewer | deterministic stub reviewer。LLMを呼ばない |
| scheduler policy | `single_active_leaf`固定 |
| Git | read-only local Gitのみ。write、push、PR、CI起動を行わない |

### 1.2 入力

1. 固定Requirement（本提案§7の対応表で指定する既存Requirementだけ）
2. 対象文書の変更（base commitとHEADから得たChange Set、Source Snapshot）
3. Review Task Contract（版付き、identity固定）
4. 版付きCompilerとPolicy

### 1.3 出力

1. Plan bundleと6 typed view
2. Context Manifest（Digest固定）
3. deterministic Finding集合
4. Contract Conformance verdict
5. Final Contract Challenge verdict
6. Human decision record
7. Provenance verdict
8. accepted artifact（reviewが通った文書変更）

### 1.4 非目標

次は本Contractのscopeに入れない。

- 汎用framework、複数Contract type、任意task orchestration、DSL、plugin
- LLMによる実レビュー、外部送信、CI起動、UI、delegated AI
- Implementation Task Contract、As-Built projector、文書renderer、
  Documentation Conformance gate、legacy reconstruction
- Work 4Bの台帳（Entry、Relation、Baseline）作成と統合リファクタリング
- `maintenance`、`reopen`、`bounded_parallel`、複数Work Itemの同時開始

## 2. 最小Review Task Contractの構造

`REQ-CONTRACT-001`が要求する項目を、文書変更reviewの最小形へ具体化する。
以下はschemaの形であり、**Task Contractの発行ではない**。

### 2.1 Identity

| field | 内容 |
| --- | --- |
| `task_contract_id` | `TC-RC3-REVIEW-DOC-CHANGE-<date>-V<n>`の形 |
| `task_contract_version` | 整数。意味変更ごとに新versionを作り、既存を上書きしない |
| `contract_type` | `review_task_contract`固定 |
| `origin` | `new_development` |
| `continuation` | `fresh` |
| `scheduler_policy` | `single_active_leaf` |

### 2.2 Responsibility（責務）

固定した一件の文書変更が、束縛された固定Requirement集合に適合しているかを判定し、
不適合を構造化Findingとして返す。文書を書き換えない。Requirementを改訂しない。

### 2.3 Boundary（境界）

- 対象は`docs/`配下の指定した一文書と、その変更に伴う参照Digestだけとする。
- source universeは固定したSource Snapshotに限る。実行中にfileを追加読込しない。
- 出力はFindingとverdictだけで、成果物への書込みはHuman decision後の別操作とする。

### 2.4 Precondition（前提）

1. Requirement authority bundleが解決でき、束縛したRequirement IDが全て存在する。
2. Source SnapshotとChange Setが確定し、workspaceがcleanである。
3. Contractが`compiled`である（`not_compilable`では開始しない）。
4. Workflowが開始を許可した実行仕様である（`REQ-EXEC-001`）。
5. active leafが他に無い（`single_active_leaf`）。

### 2.5 Context Obligation（文脈義務）

`REQ-CONTEXT-001`〜`005`から次を必須とする。

- Goal、Target、Constraints、Expected Output、Context Requirements、Validation Policy、
  Provenance Requirementを明示する。
- Targetとsource materialを、役割・内容・出所・Digestを持つ一つの材料束にする。
- 母集合、対象範囲、除外条件、分類結果をScope contractとして固定する。
- Context内容をDigestで固定し、入力変更後に旧結果を再利用せず`stale`で停止する。
- 呼出側が指定した材料だけを構成し、暗黙の資料を追加しない。

### 2.6 Allowed Capability（許可能力）

| 能力 | 可否 |
| --- | --- |
| 固定Snapshotからのfile読取り | 可 |
| Digest計算、schema検査、集合演算 | 可 |
| deterministic stub reviewerの実行 | 可 |
| LLM呼出 | 不可 |
| 外部送信 | 不可 |
| file書込み（成果物） | 不可。Human decision後の別操作 |
| Git write、CI起動 | 不可 |

### 2.7 Expected Output（期待出力）

閉じたschemaを持つFinding集合と、各verdict record。
Findingは`finding_id`、`severity`、`target_ref`（path＋Digest）、`requirement_ref`、
`rule_id`、`description`を持つ。severityは`error`／`warning`／`info`の閉じた語彙とする。

### 2.8 Acceptance（受入）

- 束縛した全Requirementに、対応するruleかHumanの明示的な非採用がある（`REQ-TRACE-002`）。
- Conformance verdictとFinal Challenge verdictがともに`passed`である。
- Human decisionが対象Digestへ束縛されている（`REQ-TRIAGE-003`）。
- Provenance verdictが`verified`である（`REQ-TRACE-005`、`REQ-CONTRACT-005`）。

### 2.9 Provenance Obligation（来歴義務）

実行前にCapture Planを生成し、Contract、Plan、Context、Execution、Result、Evidence、
Decisionをidentity・version・Digestで一続きに結ぶ。
将来の委譲評価に必要な`decision_class`、判断主体、入力Evidence、理由、Outcomeを記録する。

### 2.10 Escalation（エスカレーション）

| 事象 | 扱い |
| --- | --- |
| Requirement欠落 | 停止。`not_compilable` |
| Context不足・stale | 停止。再構築が必要 |
| Conformance不合格 | 停止。Findingを添えてHumanへ |
| Final Challenge不合格 | 停止。Contract版の見直しへ |
| Human不承認 | 停止。accepted artifactを作らない |
| 実行中のsource変更 | 停止。`stale`とし旧結果を再利用しない |

## 3. record、owner、順序、許可と停止

### 3.1 経路

```text
Requirement（固定）
  → Review Task Contract（版付き）
  → compile
  → Plan bundle（6 typed view）
  → Context Manifest（Digest固定）
  → deterministic stub reviewer
  → Contract Conformance
  → Final Contract Challenge
  → Human decision
  → Provenance verdict
  → accepted artifact
```

### 3.2 各段のrecordとowner

| # | record | owner | 許可条件 | 停止条件 |
| --- | --- | --- | --- | --- |
| 1 | Requirement binding | Requirements authority | bundleが解決でき、全IDが存在 | ID不明、bundle digest不一致 |
| 2 | Review Task Contract | Contract owner | §2の全項目が埋まる | 項目欠落、identity重複 |
| 3 | Compile verdict | Compiler | Contract、Policy、Catalogが固定版 | obligation未充足で`not_compilable` |
| 4 | Plan bundle | Compiler | compile成功 | view欠落、bundle digest不一致 |
| 5 | Context Manifest | Context owner | 材料束とScope contractが固定 | 暗黙資料の混入、Digest不一致 |
| 6 | Review Run | Workflow | permitあり、active leafが空 | permit無し、二重実行 |
| 7 | Finding set | stub reviewer | Contextだけを根拠 | schema違反、範囲外参照 |
| 8 | Conformance verdict | Conformance owner | Findingが揃う | 未対応obligation |
| 9 | Final Challenge verdict | Challenge owner | Conformance通過 | Contract適合だが上位Intentを損なう |
| 10 | Human decision | Human | 対象Digestへ束縛 | 未承認、Digest不一致 |
| 11 | Provenance verdict | Trace owner | 1〜10の辺が揃う | 辺欠落、Digest断絶 |
| 12 | accepted artifact | Workflow | Provenance `verified` | 上流いずれかの不成立 |

各段は前段のIDとDigestを参照する。順序を飛ばす経路を作らない。
ConformanceとFinal Challengeは分離し、同一ownerが兼ねない（`REQ-CONTRACT-004`）。

## 4. 正常経路と負例・復旧

### 4.1 正常経路（`new_development / fresh`）

1. 対象文書の変更を確定し、Source SnapshotとChange Setを固定する。
2. Requirementを束縛し、Contractを版付きで固定する。
3. compileしてPlan bundleと6 viewを作る。
4. Context Manifestを作り、Digestで固定する。
5. permitを得てReview Runを開始する。
6. stub reviewerがFindingを返す（`error` 0件が正常）。
7. Conformance `passed`。
8. Final Challenge `passed`。
9. HumanがDigest束縛付きで承認する。
10. Provenance verdict `verified`。
11. accepted artifactを確定する。

### 4.2 負例と復旧

| # | 負例 | 検出点 | verdict | 復旧経路 |
| --- | --- | --- | --- | --- |
| N1 | 束縛Requirementが存在しない | compile | `not_compilable` | Requirement bundleを確認し、Contract版を作り直す |
| N2 | 必須obligationに受け先がない | compile | `not_compilable` | ruleを追加するか、Humanが非採用を明示する |
| N3 | Context材料が不足 | Context構築 | `context_incomplete` | 材料束を再構成する。暗黙補完はしない |
| N4 | 暗黙の資料が混入 | Context検査 | `implicit_material_rejected` | 呼出側指定だけで再構成する |
| N5 | Context Digest不一致 | Run開始前 | `stale` | Contextを再構築し、旧Findingを破棄する |
| N6 | Conformance不合格 | Conformance | `failed` | Findingを添えてHumanへ。文書を直して再実行 |
| N7 | Final Challenge不合格 | Challenge | `failed` | Contract版の見直し。成果を通さない |
| N8 | Human不承認 | Human decision | `rejected` | accepted artifactを作らない。理由を記録 |
| N9 | 実行中にsourceが変わった | Provenance | `stale` | Snapshotを取り直し、全段をやり直す |
| N10 | 二重実行・permit無し | Workflow | `not_permitted` | active leafを確認してから開始する |

N1〜N10はWork 6Aのred fixtureへ引き継ぐ。本提案では検出点とverdictだけを固定する。

## 5. Work 5Aで実装するcomponentと、defer するcomponent

### 5.1 Work 5Aで初めて実装する最小component

| component | 最小範囲 |
| --- | --- |
| Contract schema + validator | 一Contract type、§2の項目のみ |
| Compiler | 一version。1 bundle + 6 typed view |
| Context builder | 材料束、Scope contract、Digest固定 |
| Workflow permit | `single_active_leaf`のpermitと状態遷移のみ |
| deterministic stub reviewer | 固定ruleでFindingを返す。LLM無し |
| Conformance | obligation対応の機械照合 |
| Final Challenge | Conformanceと別ownerの判定 |
| Human decision record | 対象Digest束縛 |
| Provenance verdict | 型付き辺とDigestの連鎖検証 |
| Source Snapshot / Change Set | read-only local Gitのみ |

### 5.2 Work 6A以降へdeferするcomponent

Work 6Aへ：§4の負例のred fixture化。
Work 4B・5Bへ：再利用検索gate、台帳更新、Implementation Task Contract。
Work 7A以降へ：deployment、update、rollback。
Work 8以降へ：evaluation、Issue Resolution automation、bounded parallel、AI委譲。
Deferred Workへ：As-Built projection、文書renderer、Documentation Conformance gate。

### 5.3 既存実装との重複回避

`tools/bootstrap/`にreview契約、材料束、閉鎖payload、triage、pipeline、assuranceの
bootstrap実装がある。これらは`normative_status: non-normative`のbootstrapであり、
Work 5AのRuntime componentとして昇格させない。
同じschema・validator・runtimeを二重設計せず、**Work 5Aは新しいContract schemaとCompilerを
正本とし、bootstrap実装は参照のみ**とする。昇格の可否は別のHuman判断とする。

## 6. Work 4Aの参照境界とWork 4Bへ送る範囲

- 本Contractの対象は文書変更だけであり、routineを新設・変更しない。
  したがって**Entry、Relation、Baselineを作らず、台帳を実装しない**。
- Work 4AのReuse Discovery（Routine Profile v3、Comparison Discovery）は、
  本Contractの入力にも出力にもしない。参照するのは「既に完了したbaselineが存在する」という
  事実だけである（`DEC-WORK4A-EARLY-EXIT-001`）。
- routineを新設・変更するImplementation Task Contractへ進む場合に限り、実装前の既存部品検索と
  結果記録を行う。これは**Work 4Bの範囲**であり、本提案のscopeに入れない。
- LLMによる説明、Disposition Proposal、処置labelの確定も本提案のscope外とする。

## 7. Requirement → Contract obligation → 受入testの対応

根拠のない新Requirementを作らない。既存50件のうち、本Contractが直接束縛するのは次の16件とする。

| Requirement | Contract obligation | 受入test（Work 5A） |
| --- | --- | --- |
| `REQ-CONTRACT-001` | §2のidentity〜escalationを全て持つ | A1 Contract schema検査 |
| `REQ-CONTRACT-002` | compileが1 bundle + 6 typed viewを生成 | A2 compile出力検査 |
| `REQ-CONTRACT-003` | Requirementとの順逆被覆を検査 | A3 被覆検査／B2 未被覆で停止 |
| `REQ-CONTRACT-004` | ConformanceとFinal Challengeを分離 | A6 分離実行／B5 兼務を拒否 |
| `REQ-CONTRACT-005` | Capture Planを実行前に生成 | A8 Capture Plan生成 |
| `REQ-CONTEXT-001` | 7項目の事前明示 | A4 Context項目検査／B3 欠落で停止 |
| `REQ-CONTEXT-002` | 材料束にDigestと出所 | A4 材料束検査 |
| `REQ-CONTEXT-003` | Scope contractの固定 | A4 Scope検査 |
| `REQ-CONTEXT-004` | Context Digestでstale停止 | B4 入力変更でstale |
| `REQ-CONTEXT-005` | 暗黙資料の追加禁止 | B6 暗黙混入を拒否 |
| `REQ-EXEC-001` | permitされた実行だけ開始 | A5 permit経路／B7 permit無しで停止 |
| `REQ-TRACE-002` | 義務の受け先が無ければ拒否 | B2 未被覆で停止 |
| `REQ-TRACE-005` | Provenanceを型付き辺で連結しverdict生成 | A9 verdict `verified`／B8 辺欠落で停止 |
| `REQ-TRIAGE-003` | Human決定を対象Digestへ束縛 | A7 Digest束縛／B9 不一致を拒否 |
| `REQ-WORKFLOW-005` | `new_development / fresh`を独立に固定 | A10 二軸の記録 |
| `REQ-WORKFLOW-004` | ReviewCompass3自身の文書を、通常のContract、Context、Harness、Triage、Trace、Workflow関門でreviewする。自己対象の特例や関門迂回を許さない | A11 自己対象でも通常経路・関門を迂回しない |

残る34件は本Contractで束縛せず、`deferred`としてowner・着手条件を保つ。
新しい義務を発明せず、既存Requirementの範囲内に収める。

## 8. Work 5A用の受入条件案

実装前にREDで固定できる形にする。正常例、負例、境界例を分ける。

### 8.1 正常例

- A1：Contract schemaが§2の全項目を要求し、欠落を拒否する。
- A2：compileが1 bundleと6 typed viewを決定的に生成する。
- A3：Requirementとの順逆被覆が成立する。
- A4：Context Manifestが7項目、材料束、Scope contractを持ち、Digestで固定される。
- A5：permitされたRun一件だけが開始する。
- A6：ConformanceとFinal Challengeが別ownerで順に`passed`になる。
- A7：Human decisionが対象Digestへ束縛される。
- A8：Capture Planが実行前に生成される。
- A9：Provenance verdictが`verified`になり、accepted artifactが確定する。
- A10：`origin`と`continuation`が独立に記録される。
- A11：自己対象のreviewでも通常経路と関門を迂回せず、自己対象の特例を作らない。

### 8.2 負例

- B1：Contract項目欠落で`not_compilable`。
- B2：義務の受け先欠落で停止。
- B3：Context項目欠落で停止。
- B4：入力変更後に旧結果を再利用せず`stale`で停止。
- B5：ConformanceとFinal Challengeの兼務を拒否。
- B6：暗黙資料の追加を拒否。
- B7：permit無しの開始を拒否。
- B8：Provenanceの辺欠落で`verified`にしない。
- B9：Human決定のDigest不一致を拒否。
- B10：実行中のsource変更で`stale`。

### 8.3 境界例

- C1：Finding 0件（`error`なし）でも正常経路が完結する。
- C2：`warning`のみの場合にHuman判断を必須にするか、規則どおり通すかを明示的に検査する。
- C3：対象文書が1 fileだけ、変更行が1行だけの最小Change Setで全段が通る。
- C4：同時開始候補が存在してもactive leafは1件に保たれる。

## 9. Human判断が必要な論点

実装の細部ではなく、意味・authority・scopeに絞る。

1. **対象文書の指定範囲。**最初のReview対象を`docs/`配下の一文書に限ってよいか。
   複数文書や`records/`を含めるかは意味上のscope判断である。
2. **束縛するRequirementを14件とすること。**残り35件を`deferred`のままにしてよいか。
   増減はRequirement authorityの解釈に関わる。
3. **`warning`だけの場合の扱い**（C2）。Human判断を必須にするか、`error`のみを停止条件とするか。
   これはFindingの裁定権限の設計であり、`REQ-TRIAGE-003`の解釈に関わる。
4. **bootstrap実装の位置づけ。**`tools/bootstrap/`のreview系実装を参照のみとし、
   Work 5AでRuntime componentを新規に作る方針でよいか。昇格させる場合はauthority変更になる。
5. **Final Challengeのowner分離の実現形。**同一sessionのHumanが両方を担ってよいか、
   別Runとして時間的に分離するか。`REQ-CONTRACT-004`の「分離」の意味の確定である。

## 10. 本提案で確認した既存正本との整合

矛盾は検出しなかった。確認した対応は次である。

- Current Plan §13の「最初のContract」の列挙項目を、§2と§3へ全て割り当てた。
- Work 5Aの経路図（Plan §Work 5A）と§3.1の経路が一致する。
- Work 6Aの負例catalogのうち、初期slice内のものを§4.2のN1〜N10へ対応させた。
  それ以外はWork 6Aのcatalogへ残し、本Contractの完了をblockしない。
- `DEC-WORK4A-EARLY-EXIT-001`のとおり、Work 4Aの完了を前提にWork 4へ戻る位置づけとした。
- 開発方針の「LLMと機械処理の責務分離」に従い、reviewerをdeterministic stubとした。

## 11. 後続評価シリーズ（本Contractのscope外）

最初の一件は「枠が動くこと」と「来歴が繋がること」しか示さない。検出力、対象種別の違い、
LLMを使う場合の妥当性は別の評価が要る。以下は**本Contractのscopeに入れず**、
承認後に一件ずつ別作業として実施する提案である。順序には理由がある。

| # | 評価 | 新たに分かること | 前提 |
| --- | --- | --- | --- |
| E1 | 本Contract（文書1件、指摘0件想定、deterministic reviewer） | 枠が動くか、来歴が繋がるか、止まるべき所で止まるか | なし |
| E2 | 対象文書を変える（指摘が1件出る変更、`warning`だけの変更、複数文書、`records/`配下） | **検出力**。本来止めるべきものを止められるか。`warning`の扱いの妥当性。対象範囲を広げたときのContext構築コスト | E1完了 |
| E3 | 対象種別を変える（code変更、schema変更） | 文書特有でない難しさ。Change Setの粒度、影響閉包、Testとの結び付き | E2完了、Work 4Bの再利用検索gate |
| E4 | LLMレビューのshadow評価 | deterministic reviewerと同じ入力でLLMが何を返すか。**判断には一切使わず観測だけ**する。件数差、見落とし、過検出、根拠の妥当性 | E2完了。外部送信のHuman承認 |
| E5 | LLMを非権威の助言として組み込む | 説明の有用性、根拠参照（`evidence_refs`相当）の成立、実在しない参照の検出率。Humanの判断時間の増減 | E4の観測結果をHumanが確認 |
| E6 | `maintenance / reopen`シナリオ | 同じContractで継続方法だけを変えられるか。identity保持と再開地点 | E1〜E3完了 |
| E7 | 規模（連続実行、複数Work Item候補） | `single_active_leaf`の運用コスト、待ち時間、直列fallbackの妥当性 | E6完了 |

### 11.1 順序の理由

E2とE3を先に置くのは、**信頼できる決定的なbaselineを作ってからLLMと比較する**ためである。
baselineが不確かなまま比較すると、差分がLLMの問題か枠組みの問題か切り分けられない。

E4をshadow（判断に影響させない観測）としたのは、開発方針の「LLMと機械処理の責務分離」と、
Human判断を必須とする操作（外部送信、意味的裁定）に従うためである。

### 11.2 LLMを使う評価で維持する規律

E4以降で採る規律は、Work 4A v3.1で確立したものをそのまま使う。新しい規律を発明しない。

- LLM由来の記述は**非権威**とし、生成元（提供者、モデル、テンプレート版とDigest、対象入力のDigest、
  生成日時、生成物Digest）を記録する。
- 各所見に根拠参照を必須とし、参照先は固定した入力の範囲内に限る。範囲外・実在しない参照は拒否する。
- 根拠が足りない場合はlabelを強制せず、Humanの確認対象として残す。
- deterministic reviewerとLLMの不一致は**停止ではなく、Humanが確認すべき不確実性**として記録する。
- LLMの所見からaccepted artifact、Decision、Findingの確定を自動生成しない。
- 全source treeを一括で渡さない。対象と限定した周辺だけを渡す。

### 11.3 Human判断が要る点（後続評価）

1. E2で「指摘が1件出る変更」を意図的に作ってよいか。作る場合、その変更自体をどう扱うか。
2. E4の外部送信を承認するか。承認する場合の送信先、内容、保存範囲。
3. E5でLLMの助言をHumanへ提示する形（提示する／しないの選択を含む）。

## 12. 本提案で行っていないこと

- 製品code、test、schema、policy、Requirement、Decision Record、Task Contractの作成・変更
- 外部`DATA_ROOT`への書込み
- LLM呼出、レビュー実行、Human判断の代行
- Current Plan、checklistの変更（承認前のため）
