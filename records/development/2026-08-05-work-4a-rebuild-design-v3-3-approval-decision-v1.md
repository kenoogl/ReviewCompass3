# DEC-WORK4A-REBUILD-DESIGN-006

## Decision

Humanは2026-08-05に次の二点を承認した。

1. `docs/design/2026-08-05-work-4a-rebuild-design-v3-3-proposal.md`のv3.3設計。
2. 設計中の参照循環を解消する修正。**Comparison DiscoveryだけがRoutine Profileを参照し、
   Routine ProfileはComparison Discoveryを参照しない。**人が後に採用した組合せだけを
   Attestationが結び付ける。

## 固定する一方向の参照

- Routine Profile v3は、v2の`semantic_comparison_candidate_ids`と
  `semantic_candidate_selection_reason`を持たない。
- Routine Profile v3は`comparison_discovery_ref`も持たない。
- Comparison Discovery Recordだけが、Routine Profile v3のrun ID、content digest、
  source content IDを固定参照する。
- したがってProfile v3を先にnew-onlyで確定し、次にDiscoveryをnew-onlyで確定できる。
- ProfileとDiscoveryをproject内の権威へ結線しない。後続のHuman DecisionとAttestationが
  必要になった時点だけ、その組を結線する。

循環を回避するためのplaceholder、後書き、既存recordの書換えを作らない。
この方向はv3.3設計本文、本Decision、Policy v4、schema、受入testで同じ意味とする。

## 承認範囲

- Comparison Discovery Record（`schema_version` 1）と`grouping_rule_version` 1
- Routine Profile v3（`schema_version` 3、`extraction_rule_version` 4）
- 閉じた`basis_kind`語彙6種
- groupはmember 2件以上のみ。一routineは複数groupへ所属できる
- 全`member_symbol_ids`を符号順で保持し、`representative_symbol_ids`だけを最大3件とする
- presentation classは`focused`（2〜12）、`broad`（13〜50）、`mass`（51以上）
- 受入条件K1〜K12

## 根拠の定義

| `basis_kind` | 機械的根拠 |
| --- | --- |
| `structural_exact_match` | 正規化ASTのDigestが完全一致 |
| `interface_shape_match` | symbol kind、parameter kindと個数、型注記、戻り値注記の完全一致 |
| `shared_direct_callee` | 同じ解決済み直接callee IDを共有する |
| `shared_exception_contract` | raiseとcatchの役割を混ぜず、同じ役割の同じ例外名を共有する |
| `shared_test_reference` | 同じ直接Test参照pathを共有する |
| `call_neighborhood` | 空でない直接caller/calleeの符号順集合が完全一致する |

`call_neighborhood`は部分一致の任意閾値を導入しない。部分的な共通calleeは
`shared_direct_callee`で表す。同一packageや引数個数だけでgroupを作らない。
これらは補助的な`basis_evidence`としてだけ用いる。

各groupには`basis_evidence`と「意味的結論ではない」限界を記録する。
`merge`、`split`、処置labelを計算または確定しない。

## bounded seedの扱い

Profile v2の`semantic_comparison_candidate_ids`と`semantic_candidate_selection_reason`は
歴史recordとして読めるが、次に使用してはならない。

- Comparison Discovery生成の唯一の入力
- Operational Human Decision、Entry、Baseline、Disposition Proposalの根拠

## 禁止事項

- LLMの説明生成、意味的比較、Disposition Proposal、処置labelの提案。
- Operational Human Decision、Entry、Relation、Baseline、Attestationの作成。
- 外部recordの絶対pathをproject内成果物へ保存すること。
- 全source treeまたは全group memberのsource本文をLLMへ渡すこと。
- Git historyの書換え、既存Profile v1／v2、Observation、Candidate Run、Task Contract、
  source pin recordの書換え・削除・移動。

## 根拠

- Human approval：2026-08-05。対象は
  `docs/design/2026-08-05-work-4a-rebuild-design-v3-3-proposal.md`と上記の一方向参照修正。
  引継ぎ指示`records/session-handoffs/2026-08-05-codex-to-claude-work4a-v3-3-implementation.md`は
  この承認を受けて実装範囲を固定したものである。
- 先行Decision：`DEC-WORK4A-REBUILD-DESIGN-005`、`DEC-WORK4A-REBUILD-DESIGN-004`
