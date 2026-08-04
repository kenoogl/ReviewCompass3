# Claude → Codex：Work 4A v3.3 Comparison Discovery実装 完了報告

指示：`records/session-handoffs/2026-08-05-codex-to-claude-work4a-v3-3-implementation.md`

## 1. commit SHA

| 区分 | SHA | 内容 |
| --- | --- | --- |
| A | `7c60d4a45265fd4ba79b46fef744a4987b4463ab` | Approve Work 4A v3.3 comparison discovery（`DEC-WORK4A-REBUILD-DESIGN-006`、v3.3を`approved_for_implementation`、§3／§4／§7／§8更新、TODO更新） |
| A補 | `175814babd0b2774fe9412932189b4bbb5296ed4` | Fix v3.3 design fixation todo digest |
| B | `5fce5518c9ae496666c8aadc39f4457ffa3e1375` | Add Work 4A v3.3 acceptance tests（K1〜K12と負例のRED、RED Evidence） |
| C | `7653db0b110b8f7d1924211051a489f8b6e0fd2c` | Implement Work 4A v3.3 comparison discovery（Policy v4、Profile v3、Discovery、GREEN Evidence） |
| D | `37a91c05699ec10ff840ab0a460d1390d33156a6` | Generate Work 4A v3.3 comparison discovery（実source再観測とEvidence） |

Aの直後に`175814b`を追加した。Aで更新したv3.3提案のDigestをTODOへ反映し忘れ、
TODO参照Digest検査で1件failしたためである。Git historyは書き換えず、後続commitで是正した。
以降のB／C／Dはいずれも全testがGREENである。Bは指示どおりRED test commitで、
期待理由の失敗をRED Evidenceへ記録した。

§4の`call_neighborhood`の記述も更新した。指示Cが「空でない直接caller/calleeの符号順集合の
完全一致、部分一致の任意閾値を導入しない」と固定したのに対し、原文が
「決定的閾値以上重なる」だったためである。

## 2. RED／GREEN／全test結果

- RED：`15 failed in 0.15s`（`AttributeError: ... has no attribute 'build_routine_profile_v3'`）
- GREEN：v3.3 acceptance `15 passed`
- 既存：v3.2 `11 passed`、v3.1 `21 passed`、v3 `22 passed`。いずれも弱めていない
- 全test：venv公式runner `739 passed`、Python 3.9.6、pytest 8.4.2、fallback false
- 実データ生成後の再実行も `739 passed`

testの期待を変える必要は生じなかった。設計矛盾による停止も無い。
実装側の調整を一件行った。`build_decision_card`が固定リストで全fieldを要求していたため、
bounded seedを持たないProfile v3で`KeyError`になった。存在するfieldだけを載せる形へ変更した。
testの期待は変更していない。

## 3. 実データのIDとDigest

| 項目 | 値 |
| --- | --- |
| `source_content_id` | `978da3d1bcc6a2f49cf22e90fa32799daf6f6a1da493397c91f3e0eaa16265a2` |
| `snapshot_id` | `3ecb6a8b629706c990d47a7683d5beef238057274f7105fb916b75e45e308e5f` |
| `profile_run_id`（Profile v3、`content_digest`と同値） | `55fdacd5aec93a857b7c4900eb895488f77b5f57419c25af5309fdafe10ad8c1` |
| `discovery_run_id`（Discovery、`content_digest`と同値） | `4dabb03b820bfbbac01c5d6e38e7e208f19703b617d7cd7376f38a82bea0293d` |

配置は`work4a/observations/`、`work4a/profiles/`、`work4a/comparison-discoveries/`。
DiscoveryはProfileのrun ID、content digest、source content IDを固定参照し、
Profile側はDiscoveryを参照しない。Profile v1／v2、既存Observation、既存Candidate Runは
変更・削除・移動していない。

## 4. group統計

routine 1003件、group 682件、うち994 routineが少なくとも1 groupへ所属。
group memberの延べ数4729（v3.2の上限10件による切り捨ては解消）。

| `basis_kind` | group数 |
| --- | --- |
| `shared_direct_callee` | 286 |
| `shared_test_reference` | 119 |
| `shared_exception_contract` | 87 |
| `call_neighborhood` | 86 |
| `structural_exact_match` | 59 |
| `interface_shape_match` | 45 |

presentation class：`focused` 602、`broad` 72、`mass` 8。
member_count：2が268、3〜5が249、6〜12が85、13〜50が72、51以上が8。中央値3、最大276。

最大は`CG-IFACE-0001`（`interface_shape_match`、276件、`mass`）である。
`mass` 8 groupのうち3件が`interface_shape_match`で、引数の少ない小関数やclass定義が
同じ形に集まったものである。削除せず保持し、LLMへ全member本文を渡さない対象とする。

project内へ記録したのは件数、統計、各groupの代表最大3件だけである。
全member一覧とsource本文は複製していない。外部recordの絶対pathも保存していない。

## 5. LLM処理の不実施

LLMによる説明生成、意味的比較、Disposition Proposal、処置labelの提案は一切行っていない。
Operational Human Decision、Entry、Relation、Baseline、Attestationも作成していない。
Git historyの書換え、既存Profile／Observation／Candidate Run／Task Contract／source pinの
書換え・削除・移動も行っていない。

本報告の確認まで、次のWorkとLLM処理へ進まない。
