# Work 4A Rebuild Design v3.3 Proposal

状態：`awaiting_human_approval`
対象：Work 4A Reusable Routine Ledger
基準文書：`docs/design/2026-08-05-work-4a-rebuild-design-v3-2-proposal.md`
関連メモ：`docs/design/2026-08-05-work-4a-llm-analysis-context-memo.md`
承認記録（予定）：`DEC-WORK4A-REBUILD-DESIGN-006`

これはv3.2を置換しない差分提案である。目的は、LLMの意味分析に渡す比較対象を上位件数で
切り捨てず、比較の根拠ごとにgroupとして保持・提示することである。

承認されるまで、実装、test、Routine Profileの再生成、Comparison Discoveryの生成、
外部DATA_ROOTへの追加書込み、LLMによるDisposition Proposal生成を行わない。

## 1. 背景

v3.2の`semantic_comparison_candidate_ids`は、機械的な比較候補を最大10件だけ記録する。
実Profile v2では989件中952件が上限10件に達した。この値は候補がちょうど10件であることを
示さず、11件目以降が失われている可能性を示す。

また、現行候補は同一packageや同じ引数個数といった広い条件でも選ばれるため、名称に反して
意味的な近さの結論ではない。このfieldをLLMへの最終入力や`merge`の根拠として用いてはならない。

## 2. 設計原則

### 2.1 発見と表示を分ける

- **候補発見**：比較の可能性を持つroutineを、根拠とともに失わずgroupへ収録する。
- **初期表示**：LLMとHumanへ、groupの要約と少数の代表を渡す。
- **深掘り**：必要なgroupだけ、全memberと限定した周辺code・Testへ展開する。

「最初に3件だけ表示する」は候補の保存上限ではない。表示上限であり、groupの全memberを失わない。

### 2.2 機械根拠と意味判断を分ける

機械は「同じ構造」「同じ例外名」「同じcaller」「同じTest参照」などの観測事実だけをgroup化する。
LLMは、それらが同じ責務か、統合すべきかを説明する。Humanだけが処置labelを確定する。

## 3. Comparison Discovery Record

Routine Profile v2を入力に、外部DATA_ROOTへnew-onlyで`Comparison Discovery Record`を作る。
Routine Profileそのものへ候補を追記しない。

配置：

`<runtime_root>/projects/<project_id>/<profile>/data/work4a/comparison-discoveries/<discovery_run_id>.json`

recordは、Routine ProfileのDigestとsource content IDを固定参照する。Profileとsourceが異なる
Discoveryを読込・参照してはならない。

```json
{
  "record_kind": "work4a_comparison_discovery",
  "schema_version": 1,
  "discovery_run_id": "<content digest>",
  "routine_profile_run_id": "<profile run ID>",
  "routine_profile_content_digest": "<profile digest>",
  "source_content_id": "<source content ID>",
  "grouping_rule_version": 1,
  "groups": [
    {
      "group_id": "CG-STRUCT-0001",
      "basis_kind": "structural_exact_match",
      "basis_evidence": {"structure_digest": "<digest>"},
      "member_symbol_ids": ["..."],
      "member_count": 8,
      "presentation_class": "focused",
      "representative_symbol_ids": ["...", "...", "..."],
      "is_semantic_conclusion": false
    }
  ],
  "content_digest": "<digest>"
}
```

`member_symbol_ids`は同一Routine Profile内の全memberを符号順で持つ。上限で切り捨てない。
`representative_symbol_ids`だけを最大3件にする。

## 4. groupの根拠

一つのroutineは複数groupに所属してよい。groupの種類は閉じた語彙とする。

| `basis_kind` | 機械的根拠 | 意味上の限界 |
| --- | --- | --- |
| `structural_exact_match` | 正規化ASTが完全一致 | 同じ責務・統合可能性を示さない |
| `interface_shape_match` | kind、引数kind・個数、型注記、戻り値注記が一致 | 同じ業務概念を示さない |
| `shared_direct_callee` | 同一の直接calleeを1件以上共有 | 依存が同じだけで、責務は異なり得る |
| `shared_exception_contract` | raiseまたはcatchの例外名を共有 | 例外名が同じだけでは契約は同じでない |
| `shared_test_reference` | 同一Test fileから直接参照される | Testの意図や間接検証を示さない |
| `call_neighborhood` | callerまたはcalleeの集合が決定的閾値以上重なる | 動的呼出や未解決呼出を含まない |

同一package、同じ引数個数だけではgroupを作らない。これらはgroupの補助的な
`basis_evidence`としてだけ用いる。

## 5. groupの大きさと表示

groupを削除せず、`member_count`によって表示方法を分ける。

| `presentation_class` | 条件 | 初期表示 |
| --- | --- | --- |
| `focused` | 2〜12 member | 全member IDと最大3件の代表 |
| `broad` | 13〜50 member | 件数、根拠、代表3件、全member IDへの展開参照 |
| `mass` | 51 member以上 | 件数、根拠、分布、代表3件。LLMへ全member本文を渡さない |

`broad`と`mass`は無価値ではない。広すぎる機械的共通性を表す観測として保持し、
LLMの比較対象を自動拡大しないための情報である。

## 6. LLMへの段階的提示

LLMが最初に受け取るのは、対象routineの判断カードと、そのroutineが所属するgroup一覧である。

各groupについて提示するもの：

- `basis_kind`と`basis_evidence`
- member数
- `presentation_class`
- 代表最大3件
- 全member IDを取得できるrecord reference
- 機械的根拠の限界

LLMが全memberまたは周辺codeを読むことが許されるのは、次のいずれかの場合だけとする。

1. `focused` groupを比較する必要がある。
2. `broad`または`mass` groupで、代表間の責務差を解消する必要がある。
3. `merge`または`split`を提案する根拠が不足している。
4. `human_review_required`にする理由を説明するために必要である。

追加範囲、理由、対象symbol IDはDisposition Proposalのprovenanceへ記録する。
プロジェクト全体のsourceを一括してLLMへ渡してはならない。

## 7. 旧fieldの扱い

Profile v2の`semantic_comparison_candidate_ids`と`semantic_candidate_selection_reason`は
**bounded comparison seed**として歴史recordに残す。

- 意味的な比較結果ではない。
- Comparison Discovery生成の唯一の入力にしない。
- Decision、Entry、Baseline、Disposition Proposalの根拠にしない。
- Profile v3ではこのfieldを廃止し、`comparison_discovery_ref`だけを持つ。

Profile v2と既存Observationは書き換えない。v3.3実装はProfile v3とComparison Discovery Recordを
new-onlyで作る。

## 8. source再観測の境界

Comparison Discoveryの実装自体が`tools/`配下へroutineを追加・変更する場合、Profile v2の
`source_content_id`は実装前sourceを表す。実装後には、同一source universeを再観測し、
Profile v3をnew-onlyで生成してからComparison Discoveryを作る。

実装後sourceを含まない旧Profile v2へ、後からDiscoveryを結び付けない。これにより
generator自身を含むsource treeの一貫性を保つ。

## 9. 受入条件

- K1：groupは同一Profile内のmemberだけを持ち、全memberを切り捨てず記録する。
- K2：代表は最大3件だが、member全件とmember_countを保持する。
- K3：一routineが複数の根拠groupに所属できる。
- K4：同一package・同じ引数個数だけではgroupを作らない。
- K5：各`basis_kind`の根拠と限界をrecordに保持する。
- K6：`focused`、`broad`、`mass`の表示classを決定的に付ける。
- K7：構造一致groupやDiscovery groupだけから`merge`を確定できない。
- K8：ProfileとDiscoveryのroutine profile digest・source content ID不一致を拒否する。
- K9：Profile v2のbounded seedをDecisionまたはDisposition Proposalの根拠に使おうとすると拒否する。
- K10：LLMの初期入力は判断カードとgroup要約だけであり、全source treeを含まない。
- K11：LLMの追加読込は対象group、理由、symbol IDをprovenanceへ残さなければならない。
- K12：Profile v2、Profile v3、Comparison Discoveryを併存させ、いずれも書き換えない。

## 10. 実装順序

1. 本提案をHumanが承認する。
2. Policy artifact v4にgrouping ruleと表示classを固定する。
3. K1〜K12をREDで固定する。
4. Profile v3とComparison Discoveryを実装しGREENにする。
5. 実sourceを再観測し、Profile v3とComparison Discoveryをnew-onlyで生成する。
6. group統計と代表表示をHumanへ提示する。
7. Humanが確認した後、LLMによるDisposition Proposal生成を別承認で実施する。

## 11. Human判断が必要な点

1. group根拠の6種類を採用するか。
2. `focused` 2〜12、`broad` 13〜50、`mass` 51以上の境界を採用するか。
3. groupの全member IDを外部recordへ保存することを採用するか。
4. LLMの初期表示は各group最大3代表とし、全memberは必要時に展開する方針を採用するか。
