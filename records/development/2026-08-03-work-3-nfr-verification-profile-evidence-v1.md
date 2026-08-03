# Work 3 NFR Verification Profile Evidence V1

## Identity

- Evidence ID：`RC3-WORK3-NFR-VERIFICATION-PROFILE-EVIDENCE-2026-08-03-V1`
- recorded at：`2026-08-03T20:56:18+09:00`
- stage／work：`initial-development / Work 3`
- status：`verified / human_decision_pending`

## Candidate

- path：`records/development/2026-08-03-work-3-nfr-verification-profile-candidate-v1.json`
- file SHA-256：`08d5159a483d16507c5652857e5245993b42559ed3bcc24c9434e70b0d5c2381`
- candidate digest：`c93f9336790fc8641f3f89687f94fcff3baa23254936545ed9cb85c15c25d3a6`
- authority：`proposed_only`
- approved effect：Profile接続、3分類、authority境界、`not_compilable`規則の固定候補。Requirement、
  Architecture Policy、数値閾値、runtime実装は変更しない。

## Fixed Sources

- 50 Requirement authority bundle：
  `records/requirements/authority/rc3-requirements-authority-2026-08-03--v1.json`
  - file SHA-256：`fc6d945a6bef1ebea0c4ef22705d70fac6177a8c561be0f992ca94474a8a7509`
  - bundle digest：`497bcc4374e3224acbfbb08e38c7d9f3d4e5373f59df505179b6a19bc035a02c`
  - authority status：`effective`
- current Plan：`docs/current/reviewcompass3-plan-current.md`
  - SHA-256：`0ae6bef979192b008a8a71fc090f709279c4bd1f0db159f9faadf947e929156f`
  - authority status：`provisional_plan`
- NFR memo：`docs/design/2026-08-03-non-functional-requirements-verification-profile-memo.md`
  - SHA-256：`5fb46a8b54e0cec2b3de7a5b4ad8debae0a4e05828e33454b8d654c3f811122c`
  - authority status：`non_normative_design_input`

固定sourceのfile Digestは再読込時に全件一致した。

## Authority Boundary

承認済みの版付きArchitecture Policy recordは現時点で存在しない。Planにある次の6横断ruleは
`policy_rule_candidate`としてProfileへ結線したが、`proposed_policy_rule_not_authoritative`のままWork 4へ渡す。

- component state ownership
- ID、Digest、Schema
- security、permission、external send
- Decision Authority、Human decision、Delegation Authorization
- storage、deployment、cross-contract interface
- Implementation Reuse Policy

初期必須ProfileはeffectiveなRequirementだけをauthorityに持つ。Planまたはmemoだけを根拠にPolicy authorityを
偽造していない。将来shared／distributed scopeを有効化する場合は、上流RequirementまたはArchitecture Policyと
新Profileが揃うまで`not_compilable`とする。

## Audit Results

### Requirement screening

- effective Requirement：50
- NFR invariantまたは観測義務へ接続：29
- functional／control only：21
- 重複：0
- 欠落：0

一Requirementに非機能invariantまたは観測義務が一つでもあればmappedへ分類し、残りだけを
`functional_or_control_only`へ置いた。

### Profile shape

- Profile総数：19
- `initial_required`：8
- `threshold_after_measurement`：6
- `deferred_to_deployment_profile`：5
- 必須field：18
- Profile ID重複：0
- 未知Requirement参照：0

全Profileにauthority、適用条件、workload／fixture、environment、measurement、threshold／invariant、sampling、
failure verdict、必要Evidence、stale、recovery、activation／completion条件がある。性能、規模、信頼性、費用、
互換性、security・privacy、maintainabilityの7属性を一件以上で被覆した。

### Compilation boundary

- 初期必須Profileのauthorityまたは必須field欠落：`not_compilable`
- 必須ProfileをContract、Plan、Test、Evidenceへ結線できない：`not_compilable`
- 実測後閾値Profile：観測完全性だけを現時点の判定対象とし、Human承認前の数値を品質合否に使わない
- deployment defer：`local_integrated`では明示的`not_applicable`でありrelease blockerにしない
- shared／distributed scope activation後の上流authorityまたはProfile欠落：`not_compilable`
- Requirement、Policy、Profile、workload、environment、tool変更：依存EvidenceとVerdictをstaleにする

### Negative audit

次の既知違反をin-memory copyへ一件ずつ注入し、全6件が期待分類で拒否された。

- 必須field欠落
- Requirement screeningの重複
- 初期Profileのsource authority欠落
- deferred Profileの初期scope混入
- 未承認Policy candidateの`effective`化
- 根拠のない`30秒`閾値

結果：`NEGATIVE_AUDIT_OK mutations=6 baseline=passed`

## Problems and Treatment

1. 初回監査はdeferred Profileの空`source_requirement_ids`を一律欠落として誤停止した。deferredは現行Requirementを
   持たず、scope activation時に上流authorityを要求することが正しいため、監査条件を3分類別に修正した。候補変更は
   行っていない。
2. 再監査で同時Work Item測定Profileの判定文に観測完全性の明記がないことを検出した。直列既定と上限非発明は維持し、
   待機時間、競合、fallbackの観測完全性を判定する文へ訂正した。訂正後candidate digestへ更新して全監査を再実行した。

## Test

- Candidate digest：passed
- fixed source Digest：passed
- Requirement screening：`total=50 mapped=29 non_nfr=21 duplicate=0`
- Profile shape：`profiles=19 initial=8 measurement=6 deferred=5 fields=18`
- quality attribute coverage：`attributes=7`
- Policy authority boundary：`effective_policy_records=0 candidates=6`
- negative audit：`mutations=6 baseline=passed`
- full Test：`448 passed in 1.84s`
- diff check：Evidence、checklist、TODO更新後に再実行する

## Result

候補は`verified / human_decision_pending`である。Requirement由来の初期必須義務、実測後にHumanが閾値を決める
観測Profile、deployment選択時まで初期scopeへ入れないProfileを分離し、未被覆時の停止規則を固定した。
Human承認前はWork 3の「必須非機能義務をVerification Profileへ接続した」checkboxを未完了のまま維持する。
