# Work 4B最小試行 範囲提案 v1

- 状態：`human_decision_pending`（Human承認まで実装・REDを開始しない）
- 作成日：2026-08-07
- 位置づけ：Current Plan §17 初期実装順12の前半
  「Work 4Bの最小Pilotで対象routineの再利用検索と記録方法を確認し、Work 5Bの内部
  Implementation Task Contract Pilotでそのgateを実証する」

## 1. 固定入力と承認済み境界の照合

| 固定入力 | path | SHA-256 |
| --- | --- | --- |
| Current Plan（§12 Work 4B、§17実装順12） | `docs/current/reviewcompass3-plan-current.md` | `1a73597605eafb65a2259ccf19431e3aba041564d03fdb279150042a9bd0962f` |
| Work 4A早期完了Decision | `records/development/2026-08-05-work-4a-early-completion-and-4b-decision-v1.md` | `68899660b1162b0fb00e5e2b604b3c3c4831c7cc0a32eebfe9541fd0d441a29e` |
| Work 4A v3.3実データEvidence | `records/development/2026-08-05-work-4a-v3-3-actual-comparison-discovery-evidence-v1.md` | `2cbefe548462d5c05a4cdba263decc074739d0933e4fe8fa688b219e92fd5d02` |
| 作業レビュー手順書 | `docs/development/work-review-protocol.md` | `22856c9836de2fd1a5d3a8a79d9437ea82150c8e167fb9ddc40ac6b82bb0a923` |

承認済み境界との照合結果（本提案が収まっていること）：

- 全1003 routineの一括分類・一括台帳化を前提にしない（`DEC-WORK4A-EARLY-EXIT-001`）。本提案の対象は
  1作業単位・1探索範囲だけである。
- LLMの説明・Disposition Proposalは別承認後のみ（同Decision）。本提案はLLM処理を含まない。
- Discovery groupだけで統合を確定しない（Plan §12）。本提案は統合判断そのものを扱わない。
- 検索の固定sourceはWork 4A v3.3の実データidentityとする：
  `profile_run_id` `55fdacd5aec93a857b7c4900eb895488f77b5f57419c25af5309fdafe10ad8c1`
  （routine 1003件、schema 3／抽出規則4）、
  `discovery_run_id` `4dabb03b820bfbbac01c5d6e38e7e208f19703b617d7cd7376f38a82bea0293d`
  （group 682件、schema 1／grouping規則1）、
  `source_content_id` `978da3d1bcc6a2f49cf22e90fa32799daf6f6a1da493397c91f3e0eaa16265a2`。

## 2. 対象routineの選定基準（固定）

**採用する系統**：Plan §12の第1系統「新規・変更実装の対象範囲」を採る。理由：最小試行の目的は
「実装前に検索し記録してから開始する」という関門の型を確認することであり、次に実際へ新設される
routineを対象にしなければ関門の意味を実証できない。第2系統（価値・riskの高いcandidate group）は
リファクタリング判断を伴い最小試行を超える。

**最小試行の具体対象**：本試行で新設する**再利用検索記録helper（仮称`reuse_search_record`、
`tools/development/`配下の1 module）自身**を最初の被験対象とする。すなわち、helperを実装する前に、
そのhelperが担う機能（symbol検索、group照合、record生成）と同種の既存routineを検索し、結果を
記録してから実装を開始する。自己適用により、追加の題材選定なしで関門の型を一周できる。

**選定基準の一般形（宣言）**：Implementation作業単位が宣言する「変更対象path集合と新設・変更symbol
集合」に対し、検索範囲は次の4種とする。

1. 同一`relative_path`配下（同一module・同一package）の既存routine
2. 名前・`signature`・`structure_digest`の一致または近接（`structural_exact_match`、
   `interface_shape_match`）
3. 該当routineが属するDiscovery groupの**全member**（上限切り捨てなし、Work 4A境界の継承）
4. 該当routineの`direct_caller_symbol_ids`／`direct_callee_symbol_ids`の直接近傍

## 3. 記録方法（固定）

- **record kind**：`reuse_search_record`（JSON、new-only。既存fileの書き換え・削除を拒否する）
- **置き場**：`records/development/`（Git管理下）。file名は
  `<日付>-<subject>-reuse-search-v<n>.json`。理由：この記録は実装関門のEvidenceであり、RED Evidence・
  将来のTask Contractからdigestで参照されるため、repository内に置く。Work 4Aの実データ（外部
  DATA_ROOT）は移動せず、identity（run ID＝内容digest）で結線する。
- **必須field**：
  - `subject`：作業単位名、宣言した変更対象path集合・symbol集合
  - `source_identity`：`profile_run_id`、`discovery_run_id`、`source_content_id`、schema／規則version
  - `query`：適用した検索範囲（§2の4種のどれをどのkeyで実行したか）
  - `hits`：該当routineの`symbol_id`、`code_reference`、所属group ID、`basis_kind`。0件は0件として
    正常に記録し、検索未実施と区別する
  - `content_digest`：正規化JSONのSHA-256（既存recordと同じ方式）
- **含めないfield**：処置label（`reuse | extend | merge | split | as_is`）、統合可否、削除可否。
  これらはHuman判断であり、検索recordが先取りしない。

## 4. 規範宣言（承認後の宣言→RED対応表の対象）

- **R1**：検索recordは§1のWork 4A identityへdigestで結線され、結線が欠けるか一致しないrecordを
  validatorが拒否する。
- **R2**：検索recordはnew-onlyであり、既存fileへの上書き書き込みを拒否する。
- **R3**：同一の宣言（対象path・symbol集合）と同一のProfile／Discoveryからは、同一の検索結果
  （content digest一致）が決定的に再生成される。
- **R4**：hit 0件は正常なrecordとして保存でき、record不存在（検索未実施）と機械的に区別される。
- **R5**：処置labelを含むrecordはvalidatorが拒否する（Human判断の先取り禁止）。
- **R6**：Discovery groupの参照はmemberを上限で切り捨てない。
- **R7**：gate判定（Work 5Bで実証する開始条件の判定）は、検索recordの不存在、identity結線の不一致の
  いずれでもfail-closedで「開始不可」を返す。

## 5. 実施手順（承認後）

1. 宣言→RED対応表を作成し、R1〜R7それぞれへREDまたは境界例を結び、「テストの無い宣言0件」を
   機械で数える（2026-08-06確立の関門）。**この時点で、対応表照合の恒久tool化の要否をHumanへ
   提示する**（TODO登録済みリマインド）。
2. REDを固定してcommitする。
3. helperを実装する前に、§2の基準でhelper自身の再利用検索を実行し、最初の`reuse_search_record`を
   生成する（この一回は既存の機械操作で行い、生成後にhelperで再生成一致を確認する）。
4. 固定テストを変更せずGREENにする。
5. gate判定helperを含めてWork 5Bへ引き継ぐ。

## 6. 非対象

- Entry・Relation・Baselineの台帳形式の確定と記録（Work 4B本体の後続作業単位）
- 共通部品への移行、旧実装の削除、既存codeの変更（helper新設以外の変更を行わない）
- LLMによる説明・Disposition Proposal（別承認）
- 全routineの一括検索・一括分類
- 対応表照合の恒久tool化（§5-1でHumanが判断するまで着手しない）

## 7. risk（work-review-protocol §3）

本helperは実装関門の合否を決める**守り役のcode**に該当するため、既定`high`である。実装後のレビューでは
§4.4（fixtureに無い反証の新作。例：結線digestを改竄したrecord、処置labelを紛れ込ませたrecord）と
§5（上流＝本提案とPlan §12からの期待挙動の独立導出）を適用する。

## 8. Human判断点

1. 本範囲提案の承認・修正・却下（承認まで宣言→RED対応表とREDへ進まない）
2. 対象を「helper自身の自己適用」とすることの採否（代替案：Work 5Bのhelper選定を先に行い、
   それを対象にする。ただし順序が実装順12の前後半と逆転する）
3. 記録の置き場を`records/development/`とすることの採否
