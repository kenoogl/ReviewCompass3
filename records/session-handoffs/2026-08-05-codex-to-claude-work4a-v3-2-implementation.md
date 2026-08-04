# Codex → Claude：Work 4A v3.2追加特徴の実装指示

## Human承認

Humanは2026-08-05に、`docs/design/2026-08-05-work-4a-rebuild-design-v3-2-proposal.md`を承認した。
本指示は、その承認済み設計の実装範囲を固定する。

## 目的

Routine Profileへ、LLMとHumanが処置labelを判断するための追加特徴を入れる。

- 直接caller/callee
- raise・catch関係
- 構文上の責務分割度
- Testとの直接結び付き
- 公開APIらしさ
- 意味的比較のための機械的候補集合

これらは機械抽出の事実または限定的な構文指標である。意味的な重複判断と処置labelの確定は行わない。

## 実施順序

### 1. 設計確定

- `DEC-WORK4A-REBUILD-DESIGN-005`をnew-onlyで作成し、Human承認を引用する。
- v3.2提案の状態を`approved_for_implementation`へ更新する。
- Policy artifact v3をnew-onlyで作成する。追加featureの閉じた語彙、検出範囲、
  semantic comparison candidateの上限10件を固定する。
- `complexity_signal`は次の決定的閾値をPolicy v3へ記録する。
  - `low`：`branch_count <= 3`、`max_nesting_depth <= 1`、`return_count <= 2`、
    `try_count == 0`、`effect_marker_count <= 1`の全てを満たす。
  - `high`：`branch_count >= 10`、`max_nesting_depth >= 4`、`return_count >= 6`、
    `try_count >= 3`、`effect_marker_count >= 3`のいずれかを満たす。
  - その他は`medium`。
  これは`split`の決定ではなく、確認優先度の指標である。

### 2. TDD

- v3.2のJ1〜J10を受入testとして先に固定し、REDを確認する。
- RED evidenceを記録してコミットする。
- 既存v3／v3.1のtestを弱めたり、期待を緩めたりしない。

### 3. 実装とGREEN

- Routine Profile v2（`schema_version: 2`、`extraction_rule_version: 3`）を実装する。
- 直接呼出は同一source universe内で構文上解決できるものだけを記録する。
  alias import、動的属性、reflection、callback、`eval`、`exec`は解決済みと偽装せず、
  未解決数と検出限界を記録する。
- raise・catchは構文上現れる名前だけを記録する。伝播例外や実行時型を推測しない。
- `tests/**/*.py`は独立したread-only対象とし、直接AST参照だけを関連Testとして記録する。
  文字列参照、fixture経由、動的import、統合testによる間接検証を網羅したと主張しない。
- 公開API指標は`__all__`、cross-package direct caller、CLI構文markerだけから決定的に算出する。
  公開契約の断定をしない。
- semantic comparison candidateは、同一Profile内のsymbol IDだけから決定的に最大10件選ぶ。
  各候補に機械的な選定理由を付ける。`merge`の結論を出さない。
- J1〜J10、既存v3／v3.1、全testをGREENにする。

### 4. 実sourceのProfile v2

- 実sourceからProfile v2を外部DATA_ROOTへnew-onlyで生成する。
- Profile v1、既存Observation、既存Candidate Runを変更・削除・移動しない。
- 実データの件数、各featureのcoverage、未解決数、Test参照数、公開API指標、
  comparison candidate統計をEvidenceへ記録する。
- 実データ生成後に全testを実行し、Profile v2の機械抽出結果を報告して停止する。

## コミット境界

1. Decision record、v3.2状態更新、Policy v3を設計確定コミットにする。
2. J1〜J10のRED testとRED Evidenceを別コミットにする。
3. 実装、GREEN Evidence、実source Profile v2 Evidenceを別コミットにする。

各コミットはGREENでなければならない。ただしRED test commitは、固定したJ1〜J10が
期待理由で失敗することをEvidenceに記録してよい。

## 禁止事項

- LLMによるDisposition Proposal生成を行わない。
- LLMの説明、意味的重複判断、処置labelの提案を生成しない。
- Operational Human Decision、Entry、Relation、Baseline、Attestationを作成しない。
- 既存Routine Profile、Observation、Candidate Run、Task Contract、source pin recordを書き換えない。
- Git historyを書き換えない。

## 完了報告

完了報告は、次の新規ファイルへ書く。報告ファイルは実装コミットに含めない。

`records/session-handoffs/2026-08-05-claude-to-codex-work4a-v3-2-implementation.md`

報告には、3つのcommit SHA、RED／GREEN／全test結果、実Profile v2の統計、
LLM生成を実施していないことだけを書く。
