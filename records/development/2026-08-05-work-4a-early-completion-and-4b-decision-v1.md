# DEC-WORK4A-EARLY-EXIT-001

## Decision

Humanは2026-08-05に「計画を修正して、4Aを早く終わらせる」と指示した。
これを、Work 4Aの完了境界を全routineの意味的分類・台帳化から切り離し、実装済みの
Reuse Discovery baselineで早期完了とする決定として記録する。

## Work 4Aの完了境界

Work 4Aは、既存routineを機械的に発見・比較できる再利用探索基盤を作る工程とする。
完了Evidenceは次である。

- source universeを再観測し、Routine Profile v3をnew-onlyで生成した。
- Comparison Discoveryをnew-onlyで生成し、比較候補を上限で切り捨てずgroupとして保持した。
- 実データはroutine 1003件、group 682件であり、根拠・member・表示classを記録した。
- v3.3 acceptance 15件と全test 739件が通過した。

根拠は`records/development/2026-08-05-work-4a-v3-3-actual-comparison-discovery-evidence-v1.md`である。

## Work 4Bへ移す範囲

次はWork 4Aの未完了ではなく、**Work 4B：再利用・統合の運用Pilot**として扱う。

- LLMによる限定的な説明・Disposition Proposal（別承認後のみ）
- Humanによる`reuse | extend | merge | split | as_is`の確定
- Entry、Relation、Baselineの台帳記録
- 新規routineまたは変更routineに対する、実装前の既存部品検索と実装後の台帳更新
- 共通候補ごとの安全なリファクタリング、段階移行、旧実装の削除判断

Work 4Bは全1003 routineの一括分類を前提にしない。実際に変更する範囲と、価値・riskの高い
candidate groupから小さな作業単位で実施する。一つのDiscovery groupだけで統合を確定せず、
各リファクタリングは振る舞いTest、移行、Human判断を持つ独立Work Itemとする。

## 実装順への効果

Work 4Aの完了は、Work 4へ戻り、最初のReview Task ContractのDesignを進めることを許す。
ただしroutineを新設・変更するImplementation Task Contractへ進む前には、Work 4Bの最小Pilotとして
対象範囲の既存routine検索と、その結果の記録方法を確認する。全routineの台帳化は開始条件にしない。

このDecisionはv3.1／v3.2／v3.3の機械抽出Evidenceを無効化せず、Humanの意味判断、LLMの助言、
Entry、Relation、Baselineを自動化または完了済みにもしない。
