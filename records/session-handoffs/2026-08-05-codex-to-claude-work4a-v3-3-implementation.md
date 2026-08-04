# Codex → Claude：Work 4A v3.3 Comparison Discovery実装指示

## 0. 実行者・承認・目的

**実行者はClaudeである。** Claudeは本ファイルを作業指示として読み、以下の実装を行う。
Humanは2026-08-05に、次の二点を承認した。

1. `docs/design/2026-08-05-work-4a-rebuild-design-v3-3-proposal.md`のv3.3設計。
2. 設計中の参照循環を解消する修正：**Comparison DiscoveryだけがRoutine Profileを参照し、
   Routine ProfileはComparison Discoveryを参照しない。** 人が後に採用した組合せだけを
   Attestationが結び付ける。

目的は、v3.2の上限10件で切り捨てられる比較候補を置き換え、機械的根拠ごとに全memberを
保持するComparison Discoveryを作ることである。これは意味的な重複判断や処置決定ではない。

## 1. 固定する一方向の参照

- Routine Profile v3はv2の`semantic_comparison_candidate_ids`と
  `semantic_candidate_selection_reason`を持たない。
- Routine Profile v3は`comparison_discovery_ref`も持たない。
- Comparison Discovery Recordだけが、Routine Profile v3のrun ID、content digest、
  source content IDを固定参照する。
- そのため、Profile v3を先にnew-onlyで確定し、次にDiscoveryをnew-onlyで確定できる。
- ProfileとDiscoveryをプロジェクト内の権威へ結線しない。後続のHuman Decisionと
  Attestationが必要になった時点だけ、その組を結線する。

この方向を、v3.3設計本文、Decision、Policy v4、schema、受入testで同じ意味にする。
循環を回避するためのplaceholder、後書き、既存recordの書換えを作ってはならない。

## 2. 実施範囲とコミット境界

各作業単位をコミットしてから次へ進む。Git historyの書換え、既存のProfile v1/v2、
Observation、Candidate Run、Task Contract、source pinの書換え・削除・移動は禁止する。

### A. 設計確定コミット

次を一つのコミットにする。

- `records/development/2026-08-05-work-4a-rebuild-design-v3-3-approval-decision-v1.md`を
  new-onlyで作成し、上記Human承認と一方向参照を引用する。
- v3.3提案の状態を`approved_for_implementation`へ更新する。
- §3、§7、§8を更新し、Profile v3にDiscovery参照が無いこと、Discovery→Profileだけで
  あること、Attestationが後続の唯一の結線点であることを明記する。
- `TODO_NEXT_SESSION.md`を、v3.3実装中である現在位置へ更新する。参照Digestは実ファイルから
  再計算し、TODO validatorを通す。

### B. REDコミット

- `tests/test_work4a_rebuild_v3_3_e2e.py`を新規作成し、K1〜K12を受入testとして固定する。
- K1〜K12に加えて、次を負例として固定する。
  - Profile→Discovery参照の混入を拒否する。
  - Discoveryが別Profile digestまたは別source content IDを参照した場合を拒否する。
  - memberの切捨て、member_count不一致、代表4件、語彙外basis、語彙外presentation classを拒否する。
  - v2 bounded seedをDiscovery・Decision・Disposition Proposalの根拠に使おうとする場合を拒否する。
- REDは新API未実装またはschema未対応という期待理由で確認し、
  `records/development/2026-08-05-work-4a-v3-3-acceptance-red-evidence-v1.md`へ記録する。
- 既存v3/v3.1/v3.2 testを弱めたり、期待を緩めたりしない。

### C. 実装・GREENコミット

実装と次を同じGREENコミットにする。

- Policy artifact v4をnew-onlyで作成する機能と、生成された
  `.reviewcompass/policies/work4a-freshness-policy-v4.json`。
- Routine Profile v3（`schema_version: 3`、`extraction_rule_version: 4`）と
  Comparison Discovery Record（`schema_version: 1`）のschema、生成、検証、new-only書込み。
- `records/development/2026-08-05-work-4a-v3-3-acceptance-green-evidence-v1.md`。

Policy v4の閉じた`basis_kind`語彙は次の6種だけにする。

1. `structural_exact_match`
2. `interface_shape_match`
3. `shared_direct_callee`
4. `shared_exception_contract`
5. `shared_test_reference`
6. `call_neighborhood`

groupはmemberが2件以上の場合だけを作る。一routineは複数groupに所属できる。
全`member_symbol_ids`を符号順で保持し、`representative_symbol_ids`だけを最大3件とする。
presentation classは`focused`（2〜12）、`broad`（13〜50）、`mass`（51以上）だけにする。

根拠は機械的事実だけに限定する。

- `interface_shape_match`はsymbol kind、parameter kindと個数、型注記、戻り値注記の完全一致。
- `shared_direct_callee`は同じ解決済み直接callee IDを共有するmember群。
- `shared_exception_contract`はraise/catchの役割を混ぜず、同じ役割の同じ例外名を共有するmember群。
- `shared_test_reference`は同じ直接Test参照pathを共有するmember群。
- `call_neighborhood`は、空でない直接caller/calleeの符号順集合が完全一致するmember群。
  部分一致の任意閾値を導入しない。部分的な共通calleeは`shared_direct_callee`で表す。

同一packageや引数個数だけでgroupを作ってはならない。各groupにはbasis evidenceと
「意味的結論ではない」限界を記録する。`merge`、`split`、処置labelを計算または確定してはならない。

Profile v2のbounded seedは歴史recordとして読めても、Discovery生成の唯一の入力、
Decision、Entry、Baseline、Disposition Proposalの根拠に使用してはならない。

K1〜K12と新負例、既存Work 4A test、全testをGREENにする。実装中にtest期待を変える必要が
生じた場合は、設計矛盾として止め、理由を完了報告へ記録する。局所パッチで通してはならない。

### D. 実source生成・Evidenceコミット

実装GREENのコミット後、同一source universeを再観測する。generator自身を含む`tools/`が
変わっているため、v2 ObservationやProfile v2を再利用してはならない。

- 新しいObservation、Profile v3、Comparison Discoveryを外部DATA_ROOTへnew-onlyで生成する。
- Profile v3の後に、そのProfileに一致するDiscoveryだけを生成する。
- 外部recordの配置は
  `<runtime_root>/projects/<project_id>/<profile>/data/work4a/comparison-discoveries/`とする。
- プロジェクト内には、生成したID、Digest、source content ID、件数、basis_kind別group数、
  presentation class別group数、member_count分布、各groupの代表表示だけをEvidenceとして記録する。
  外部recordの全member一覧やsource本文を複製しない。
- `TODO_NEXT_SESSION.md`を「実データ確認待ち」に更新する。LLMのDisposition Proposalは
  別承認待ちと明記する。
- 全testを公式venv runnerで再実行し、結果をEvidenceへ記録する。

## 3. 明確な禁止事項

- LLMの説明生成、意味的比較、Disposition Proposal、処置labelの提案を生成しない。
- Operational Human Decision、Entry、Relation、Baseline、Attestationを作成しない。
- 外部recordの絶対pathをプロジェクト内成果物へ保存しない。
- 全source treeや全group memberのsource本文をLLMへ渡さない。
- 実装の細部で停止・承認要求を繰り返さない。security、authority、不可逆操作、または
  設計を満たせない矛盾が生じた場合だけ停止する。

## 4. ClaudeからCodexへの完了報告

本実装のコミットに完了報告を混ぜない。次の新規ファイルへ短く記録する。

`records/session-handoffs/2026-08-05-claude-to-codex-work4a-v3-3-implementation.md`

報告に含めるのは、A〜Dのcommit SHA、RED/GREEN/全test結果、実Observation/Profile v3/
DiscoveryのIDとDigest、group統計、LLM処理を行っていない事実、設計上の停止があった場合だけの
原因である。Codexがその記録を確認するまで、次のWorkやLLM処理には進まない。
