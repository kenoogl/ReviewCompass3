# DEC-WORK4A-REBUILD-DESIGN-005

## Decision

Humanは2026-08-05に`docs/design/2026-08-05-work-4a-rebuild-design-v3-2-proposal.md`を承認した。
v3.1を置換せず、Routine Profileへ追加特徴を入れる差分としてv3.2を実装正本に加える。

## 承認範囲

- Routine Profile v2（`schema_version` 2、`extraction_rule_version` 3）
- 直接caller／calleeの記録と未解決呼出数
- raise・catch関係とbare exceptの構文抽出
- 責務分割度の構文指標と`complexity_signal`
- `tests/**/*.py`の直接AST参照だけを対象とする関連Test
- `__all__`、cross-package direct caller、CLI構文markerからの公開API指標
- 同一Profile内から決定的に選ぶ意味的比較候補（上限10件）
- 受入条件J1〜J10

## Human判断の確定

v3.2提案§8の四点は次で確定した。

| # | 論点 | 確定 |
| --- | --- | --- |
| 1 | 意味的比較候補の上限 | 10件 |
| 2 | `complexity_signal`の閾値 | 下表のとおりPolicy v3へ固定する |
| 3 | Test参照の範囲 | 直接AST参照だけに限定する |
| 4 | `public_api_signal`の段階 | `low`／`medium`／`high`の3段階 |

`complexity_signal`の閾値は次を決定的に適用する。これは`split`の決定ではなく、
LLMとHumanが周辺codeを読む確認優先度の指標である。

- `low`：`branch_count <= 3`、`max_nesting_depth <= 1`、`return_count <= 2`、
  `try_count == 0`、`effect_marker_count <= 1`の全てを満たす。
- `high`：`branch_count >= 10`、`max_nesting_depth >= 4`、`return_count >= 6`、
  `try_count >= 3`、`effect_marker_count >= 3`のいずれかを満たす。
- その他は`medium`。

`public_api_signal`の閾値は提案§3.5が段階数だけを定めていたため、Policy v3で次を固定した。
公開契約の証明ではなく、確認優先度の指標である。

- `high`：`is_exported_by_all`が真、`cli_entrypoint_marker`が真、または
  `cross_package_caller_count >= 2`のいずれか。
- `low`：`is_private_name`が真、かつ`is_exported_by_all`が偽、かつ`cli_entrypoint_marker`が偽、
  かつ`cross_package_caller_count == 0`。
- その他は`medium`。

## 検出限界の明示

追加特徴は機械抽出の事実または限定的な構文指標であり、意味的な重複判断と処置labelの確定を行わない。
次をrecordへ明記し、未検出を「存在しない」の証明として扱わない。

- 直接呼出：alias import、動的属性、reflection、callback、`eval`／`exec`を解決済みと偽装せず、
  未解決数を記録する。
- 例外：構文上現れる名前だけを記録し、伝播例外や実行時型を推測しない。
- Test参照：`tests/**/*.py`の直接AST参照だけを記録し、文字列参照、fixture経由、動的import、
  統合testによる間接検証を網羅したと主張しない。
- 公開API：`__all__`、cross-package direct caller、CLI構文markerだけから算出し、公開契約を断定しない。
- 意味的比較候補：読む対象を絞るためだけに使い、`merge`の根拠または結論にしない。

## 禁止事項

- LLMによるDisposition Proposalの生成、LLMの説明・意味的重複判断・処置label提案の生成。
- Operational Human Decision、Entry、Relation、Baseline、Attestationの作成。
- 既存Routine Profile、Observation、Candidate Run、Task Contract、source pin recordの書換え。
- Git historyの書換え。

## 根拠

- Human approval：2026-08-05。対象は`docs/design/2026-08-05-work-4a-rebuild-design-v3-2-proposal.md`。
  引継ぎ指示`records/session-handoffs/2026-08-05-codex-to-claude-work4a-v3-2-implementation.md`は
  この承認を受けて実装範囲を固定したものである。
- 先行Decision：`DEC-WORK4A-REBUILD-DESIGN-004`、`DEC-CONFORMANCE-SCOPE-RELAXATION-001`
