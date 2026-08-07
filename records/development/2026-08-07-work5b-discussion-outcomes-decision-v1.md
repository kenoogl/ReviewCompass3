# Work 5B前の設計議論 経緯と結論 Decision v1

- decision ID：`DEC-WORK5B-DISCUSSION-OUTCOMES-001`
- decision maker：Human
- decided at：2026-08-07
- 指示：本sessionのHuman文言「以上の議論の経緯と結論を証跡化して実装へ」（2026-08-07）

## 1. 経緯

Work 5BのContract・RED固定後、`implementation_ready`判断の前にHumanが議論を要請した。
Claudeが論点5件を提示し、Humanが各論点へ判断を与え、派生論点（絞り込み観点、RC2先行資産、
機密境界、Work 5B後の順序）まで議論した。Humanは「まだ議論が残っているので、それが終了したら
implementation_readyと判断してよい」と条件付き承認を先行して与え、本記録の指示で議論を終了した。

## 2. 結論（論点別）

### 論点1：再利用検索sourceの鮮度

**合意**：当面は現状（2026-08-05観測のProfile v3）で運用し、限界を記録に残す。検索のたびの
再観測（検索への組み込み）はWork 4B本体の設計課題として扱う。

### 論点2：検索の質と意味判断

**Human判断**：「LLMの意味判断を採用する。候補をどのような観点で絞り込むかも検討」。
再利用検索は三段構えとする——(1)実装前は名前・場所、(2)実装後は構造の指紋（structure_digest）
による事後照合、(3)内容（意味）はLLMの非権威説明＋HumanのDisposition確定（既承認境界どおり
別承認後のみ）。

絞り込み観点は5つで合意した：(1)構造一致の強さ（basis_kind順）、(2)現に変更する範囲との交差、
(3)守り役の重複の危険度優先、(4)重複の実害の大きさと乖離の兆候、(5)**除外規則の先行**——
版固定・凍結・履歴保持は統合してはいけない。除外対象の機械可読宣言の作成自体がHuman承認事項。
**Human判断**：「絞り込み観点の運用形は、すぐ対処がよい」——順位表生成と除外宣言の対処を
早期（Work 5B完了後の最初の作業群）に置く。

### 論点3：検索記録の置き場

**Human判断**：「先を見越して仕組みを整える」。Work 4Aの先例（大きな記録は外部DATA_ROOT、
project内はidentityとDigestの証明書）を検索recordへ適用する設計を先回りで用意する。

### 論点4：外部LLMによる独立レビューとRC2先行資産

**Human判断**：「承認。既にReviewCompass2で外部APIに送信するコンテキストの作り方、プロトコルは
試して、一定の結果を得ている」「（RC2先行資産は）固定sourceとして結線する前に、そのソース自体を
あたかもこのプロジェクトの実装済ソースとして考えてみたらどうか。必要に応じて修正もいれる」
「RC2先行資産の扱いはその通り（Claudeの形式化案を承認）」。

形式化された扱い：RC2該当module（文脈組み立て・送信手順）は、RC2のcommit・Digestを固定した
Provenance付きでRC3へ取り込み、**取り込み＝routine新設としてRC3の全関門**（再利用検索gate、
宣言→RED対応表、外部送信は既定high、反証レビュー）を適用する。**実装済み扱いはするが
検証済み扱いはしない**。適合修正（Layout v3・new-only・venv基盤）は前提とし、保守・継承
（adapt）の型で扱う。

機密境界の原則は**基本OK**：送るのは判定に必要な候補コード断片と機械的特徴量のみ。生の
session記録とSENSITIVE_ROOTの内容は送らない。送信前に機械検査（既存の伏字化・秘匿検出系の
再利用候補）を通す。具体のallowlistは外部APIレビューTask Contract提案でHuman承認する。

### 論点5：規律の費用対効果

**合意**：「費用は起こりうる重大な穴（黙って壊れる型）を埋めるためのものであり許容する」。
歯止め2件を維持する——(1)費用を掛ける対象を守り役と不可逆に限る（work-review-protocol §3）、
(2)儀式が実際に何を捕まえたかをWork 8で測り、捕まえない儀式は削る出口を持つ。

### Work 5B後の順序

**Human判断**：「提案で」——次の折衷案を採用する。

1. Work 5Bを閉じる（検査器の第一実運用まで）
2. Work 4B本体の設計束を一枚の提案にまとめる（再観測の組み込み、記録の外部化、順位表と
   除外宣言、台帳Entry・Relation・Baseline）。論点2の「すぐ対処」はこの束の先頭に置く
3. レビューbacklogは上位2系統だけ先行（operation_routing系、Issue・候補の合否を決める検証器群）
4. 残りのbacklogとRC2取り込み・外部APIレビューは台帳整備後

## 3. この決定が承認していないこと

- LLM意味判断・外部APIレビューの実行開始（それぞれ別承認・別Task Contract）
- 除外宣言・順位表・外部化・台帳の実装（設計束の提案とHuman承認が先）
- RC2 sourceの取り込み実行（Task Contract提案とHuman承認が先)
- レビューbacklog Issueの`in_progress`化

## 4. 参照

| 種別 | path | SHA-256 |
| --- | --- | --- |
| Work 5B開始Decision | `records/development/2026-08-07-work5b-start-decision-v1.md` | `b99da9e4f3eb2913731ebf2701eb6abcf7787548feb5c152118c7aa98d916bfe` |
| Work 5B Contract | `records/development/2026-08-07-work5b-implementation-task-contract-v1.json` | `89c92ae260bfb1efd201d414e0235b66ebb270b457942c59ef5fccfc9cfa5387` |
| 下流影響の参考情報 | `records/development/2026-08-07-unreviewed-work-review-downstream-impact-note-v1.md` | 順序判断の根拠 |
| ReviewCompass2前身Evidence | Work 1固定入力に束縛済み | RC2取り込み時に再結線する |
