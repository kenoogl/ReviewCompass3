# DEC-WORK4A-REBUILD-DESIGN-004

## Decision

Humanは`docs/design/2026-08-04-work-4a-rebuild-design-v3-1-amendment.md`を承認した。
v3は置き換えず、v3.1を差分として実装正本に加える。

## 承認範囲

- 三層の役割分担（機械はRoutine Profile、LLMは非権威のDisposition Proposal、Humanだけがdispositionを確定）
- 分類三軸の分離（`candidate_classification`／`responsibility_class`／`disposition`）
- 抽出対象と除外対象の固定、`__qualname__`規約のsymbol_id、`extraction_rule_version` 2
- `symbol_id_collision`による重複停止
- Routine Profile（機械事実のみ）と`syntactic_effect_markers`
- Disposition Proposal（非権威）、参照範囲の限定、`evidence_refs`必須、生成元の必須field
- `structural_match_group_id`（構造一致の手掛かりであり統合の結論ではない）
- group条件式による判断支援と取りこぼし禁止
- Attestation schema 2
- 受入条件I1〜I21

## 未決事項の決定

| # | 論点 | 決定 |
| --- | --- | --- |
| 1 | lambdaの扱い | 除外し、件数と位置を`excluded_constructs`へ記録する |
| 2 | group条件式の記法 | 三つ組の連言（AND）のみ。正規表現とORを許さない |
| 3 | 例外classの機械初期値 | `ownership_unclear`とする |
| 4 | Disposition Proposalの生成単位 | 922件全件をbatch生成する |
| 5 | nested functionの機械初期値 | `implementation_detail`とする |

決定3は設計案の推奨（`implementation_detail`）と異なる。例外classは責務の帰属が
codeからは決まらないため、`ownership_unclear`としてHumanの確定を要求する扱いとする。

`responsibility_class`の機械規則は、上から順に最初に一致したものを採る。

1. 例外class（基底が例外型） → `ownership_unclear`
2. nested function → `implementation_detail`
3. symbol名が`_`で始まり、source universe内の他moduleから参照されない → `implementation_detail`
4. source universe内のどこからも参照されない → `ownership_unclear`
5. それ以外 → `public_responsibility`

いずれも提案であり、Humanが確定するまでEntryを作らない。

## 自律実行の範囲

承認範囲では、実装途中の細かな判断で停止せず自律実行する。

1. 本Decisionの記録
2. Policy artifactの`policy_version` 2固定
3. 受入testI1〜I21のRED固定
4. 実装とGREEN、全test
5. 実sourceでのRoutine Profile生成と機械抽出結果の提示

**段階5の提示時点で停止する。**

## 停止して別承認を要する操作

- LLMによるDisposition Proposalの生成。Routine Profileの実データ確認後の別承認とする。
- Operational Human Decision、Entry、Relation、Baselineの作成。
- 破棄、revert。
- 設計レベルの矛盾、security、authority、不可逆操作に影響する問題を見つけた場合は、
  局所patchを行わず停止して報告する。

## 根拠

- Human approval：2026-08-04の会話における次の承認。

  > v3.1設計改訂と、Work 4Aに限定したconformance-evaluation利用範囲の緩和を承認する。
  >
  > 未決事項は次のとおり決定する。
  > - lambda：除外し、件数と位置を記録する
  > - group条件式：三つ組の連言（AND）のみ
  > - 例外クラス：機械初期値は ownership_unclear
  > - Disposition Proposal：922件全件をバッチ生成する
  > - nested function：機械初期値は implementation_detail
  >
  > この承認をDecision recordへ記録し、Policy v2固定、I1〜I21のREDテスト、
  > 実装、GREENまでを自律実行せよ。
  > 実ソースでRoutine Profileを生成して機械抽出結果を提示した時点で停止すること。
  > LLMによるDisposition Proposal生成は、Routine Profileの実データ確認後の別承認とすること。

- 対象設計：`docs/design/2026-08-04-work-4a-rebuild-design-v3-1-amendment.md`
- 先行Decision：`records/development/2026-08-04-work-4a-rebuild-design-v3-approval-decision-v1.md`
- 関連Decision：`records/development/2026-08-04-conformance-evaluation-scope-relaxation-decision-v1.md`
