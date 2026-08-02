# ReviewCompass2変更規模比例レビュー入力の参照記録

## 1. 目的

ReviewCompass2で明示された、レビュー入力を文書全体の大きさではなく変更から導出した
影響範囲に応じて構成する方針を、Task Contract中心のReviewCompass3へ適合させるための
固定参照として記録する。前身の具体的な文書形式やgraph語彙をそのまま正本にせず、
維持する原則、修正する点、例外時の安全策を区別する。

## 2. 固定source

観測元repository：`/Users/Daily/Development/ReviewCompass2`

| source | SHA-256 | 参照内容 |
|---|---|---|
| `docs/plan/2026-07-23-plan-c-rebuild-minimal-base.md` | `75915b28557b4e83b74e18670b1b80a5f1274cd391faa1ab0974419cb4b97e6b` | 文書サイズ比例から変更規模比例への転換、意味単位graphによる決定的slice、残余リスクとしての全文整合review |
| `docs/design/2026-07-23-semantic-unit-schema-v0.md` | `106dca8a054a6db8153930a92bfef2b58f87a95a6d82745ab410561e50dd7468` | 変更単位から参照の逆向きへ推移的にたどる影響範囲と、到達単位・根拠抜粋によるreview入力 |

## 3. 維持する原則

- review入力を、source universeまたは文書全体の大きさだけを理由に増やさない。
- 固定した変更単位、版付き意味graph、閉包規則から影響候補母集合を決定的に生成する。
- 採用した影響単位と必要なEvidence抜粋をreview入力へ含め、選定理由を追跡可能にする。
- 関係のない文書や意味単位が増えても、変更の影響閉包が同じならreview payloadを増やさない。
- sliceだけでは見つけにくい全体整合上の残余riskを認め、別の検査経路を残す。

## 4. ReviewCompass3向けの修正

「変更規模」は変更行数や変更file数ではなく、変更から意味関係をたどって得た影響閉包、
必須Evidence、Task Contractが要求する固定材料の規模として扱う。小さな変更でも共有Policy、
global invariant、広い依存関係へ影響すれば入力は大きくなり得る。

ReviewCompass3ではSemantic Traceが影響候補母集合を生成し、Review Contextが全候補を
`include | exclude | defer`へ分類して、採用材料、根拠、順序をContext Manifestへ固定する。
全文整合reviewは通常sliceへ暗黙追加せず、独立したreview modeまたは明示的なscope拡大として
実行する。

scope拡大は、少なくとも次のいずれかを満たす場合に限定する。

- 意味graph、閉包規則またはEvidenceが欠落、stale、競合しており安全な閉包を確定できない。
- global invariant、横断Policy、未解決の循環など、局所閉包では検証対象を境界付けられない。
- risk-based Verification Profileまたは明示的なDecision Authorityが全文整合reviewを要求する。
- 定期的な残余risk検査として、通常の変更reviewとは別の固定対象と条件で実施する。

scopeを拡大した場合は、起点、理由、判断主体、追加材料、拡大前後のContext量、機密性、
終了条件をOperational Provenanceへ保存する。入力上限を超えた場合に材料を黙って切り捨てず、
分割、再構成またはHuman escalationへrouteする。

## 5. 検証する性質

- 同じ変更単位、意味graph、閉包規則から同じ候補母集合と同じ採否結果を再生成できる。
- source universeへ無関係な材料を追加しても、freshness再検査後の選択材料とreview payloadは
  増えない。
- 関係辺または必須Contract材料を変更した場合だけ、規則に従って影響閉包とpayloadが変わる。
- 全文または広域scopeへの拡大は、許可条件とProvenanceなしには実行できない。
- `source_universe_bytes`、`changed_unit_count`、`impact_closure_unit_count`、
  `review_input_bytes`、`review_input_tokens`、scope拡大の有無と理由を別々に比較できる。
- 入力削減だけで合格にせず、既知Findingの見逃し、Evidence Coverage、責務外Finding、費用を
  同じtrialで評価できる。

## 6. 制約

この記録は前身sourceと適合判断のEvidenceであり、Requirementsまたは設計の正本ではない。
「変更規模比例」は厳密な線形計算量の保証ではなく、無関係な文書総量をreview入力の支配要因に
しないという構成上の不変条件である。採用事項はIntent、Requirements差分、設計、統合計画、
Evaluation Profileへ反映して現行候補とする。
