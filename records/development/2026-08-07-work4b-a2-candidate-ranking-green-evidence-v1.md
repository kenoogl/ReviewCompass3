# 構成A-2 絞り込み順位表 GREEN Evidence v1

- 作成日：2026-08-07
- 承認：`DEC-WORK4B-MAIN-DESIGN-BUNDLE-001` §2 A-2
- RED Evidence：`records/development/2026-08-07-work4b-a2-candidate-ranking-red-evidence-v1.md`

## 1. 実装

`tools/development/candidate_ranking.py`を新設した。承認済み辞書式順（basis_kind強度→守り役含有→
member数→変更範囲交差→group_id）の決定的な順位付け、統合除外宣言の機械参照と落とした件数・
group・entry IDの表示、staleなProfileからの生成のfail-closed拒否（構成Bの締め）、new-only保存を
含む。除外判定は`integration_exclusions.excluded_entry_ids`、鮮度計測は`reuse_search_record`の
計測routineを再利用した（車輪の再発明なし）。

- targeted：`tests/test_candidate_ranking.py` `5 passed`、exit `0`。固定testは変更していない。
- 公式全Test：`1080 passed`、exit `0`。

## 2. 鮮度gateの初回発火（記録）

最初の実生成は`profile_stale: tools/development/candidate_ranking.py`で**正しく拒否された**。
順位表module自身が観測後の新設fileだったためであり、設計どおりの停止である。GREEN commit
（`3fae166`）後に再観測してから生成した。

## 3. 再観測（2回目）と実順位表

| 項目 | 値 |
| --- | --- |
| snapshot_id | `5cea442a82a5662c3a8fa0db49f1c741842489f8965223b7c2ae981bc3c6d4d0` |
| profile_run_id | `b4ba016eaac8bc07326ef24e8c730d235dcf97b01ed7c4312107bc96fff1b66d`（routine 1245件、file 119） |
| discovery_run_id | `a66a4f5b28468fedcc6e9b94df75786bc6336a969fb56178fdeb1e049b7080b3`（group 809件） |
| head / captured_at | `3fae166f6510680a3a6e80bf19ee33b058b392e1` / `2026-08-07T13:38:57+0900` |

実順位表は`records/development/2026-08-07-candidate-ranking-v1.json`（content digest
`d270903ab16ca89625212c9fd5c0cb7d71503862c07445bf52480daa197275f7`、185KB）：

- **順位付け：741 group、除外脱落：68 group**（全group IDと該当entry IDを列挙。silent capなし）
- 上位は`structural_exact_match`×守り役含有の大型cluster（member最大28件）。LLM意味判断
  （別承認）へ渡す候補の最初の実材料である。
- guard一覧はトリアージメモ§6と本設計束で新設した守り役3 module、changed_pathsは
  `tools/development/`を入力とし、順位表record内に固定した。

## 4. 残余と限界

- 順位表の消費（LLMへの提示、Human処置確定、台帳記録）は未実施。LLM起動は別承認のまま。
- guard一覧は順位表への入力paramであり、宣言recordではない。恒久化はトリアージメモの
  後継整備（レビューbacklog着手時）に合流する。
- 本moduleは候補脱落を決める守り役codeであり既定`high`。反証レビュー対象に含める。
- 構成D（台帳）とC（外部化）が設計束の残余である。
