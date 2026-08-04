# conformance-evaluation利用範囲の緩和提案

状態：`awaiting_human_approval`
対象：旧ReviewCompassの`conformance-evaluation`をWork 4Aで利用する範囲
承認記録（予定）：`DEC-CONFORMANCE-SCOPE-RELAXATION-001`

**これは提案であり、Human承認前である。**承認されるまで、本提案を根拠に逆推定を実行しない。
承認された場合にだけDecision recordを作成する。

## 1. 現行の制限

前身ReviewCompassに、実装codeからrequirementsとdesignを推定する`conformance-evaluation`がある。
継承記録は`records/sources/2026-08-02-reviewcompass-conformance-evaluation.md`
（前身固定commit `cab302d4b32af790628b811b3566f39d55781fa5`）。

現在このrepositoryには二つの制限がある。

| 出所 | 制限 |
| --- | --- |
| 継承記録§5 | 管理下で開発したcodeでは、requirementsとdesignのLLM逆推定を通常経路にしない |
| 継承記録§6、`docs/plan/2026-08-02-task-contract-centered-replan.md` Deferred Work 9 | 本Workは初期開発へ入れない |

## 2. 緩和を提案する理由

Work 4Aの実source観測で候補が922件になった。内訳はmodule直下の関数648、class 274、
うち非公開`_`始まり393、docstringあり124のみである。

Humanは「台帳には全て載せ、処置labelを付ける。人がcodeを1件ずつ読むのは現実的でないため、
全codeを調べて一覧表を作り、それを元に分類する」方針を示した。

この作業は、実装から責務を読み取って構造化するという点で`conformance-evaluation`の責務と重なる。
既存の制限を保ったままでは、この方針を実行できない。

## 3. 緩和を提案する範囲

| # | 現行 | 提案 |
| --- | --- | --- |
| 1 | LLM逆推定を通常経路にしない | Work 4Aの範囲で、routineの責務分析と処置label提案に限り通常経路として使う |
| 2 | 初期開発へ入れない | Work 4Aの範囲で先行して使う |

適用範囲はWork 4A Reusable Routine Ledgerに限る。
Deferred Work 9のAs-Built projector、Markdown renderer、Documentation Conformance gateの
実装着手を含めない。

## 4. 緩和しないもの

緩和するのは「使ってよいか」だけである。次の規律は前身から継承し、維持する。
これらは逆推定の信頼性を担保する条件である。

- 文書生成と適合判定を分離する。
- 推定時に既存仕様を遮断し、後段で比較する。
- 推定根拠としてcode referenceを保持する。
- 生成物は`draft_only`とし、派生文書から規範正本を直接更新しない。
- 意味変更候補はHuman判断へ渡す。

あわせてv3設計の次も維持する。

- 機械がHuman dispositionを先取りしない。
- LLM由来の記述は非権威（advisory）とし、生成元を記録する。
- 派生物からDecision、Entry、Baselineを自動生成しない。

## 5. 前身codeの扱い

前身repositoryのcodeは複製しない。継承するのは責務と語彙である。
継承元は継承記録の固定commitとDigestで示す。
前身codeを読む必要が生じた場合は、対象と目的を提示してから読む。

## 6. 影響

- Work 4AがDeferred Work 9に属する能力の一部を先行して使う。
- Work 4Aの完了条件がWork 9の完了条件を吸収しないよう、v3.1設計改訂§9で境界を明記する。
- 継承記録は固定source recordであり、本文をin-place変更しない。位置づけの更新は、承認された場合の
  Decision recordを正本とする。

## 7. Humanへの確認事項

1. 上記§3の二点を、Work 4Aの範囲に限って緩和してよいか。
2. §4の規律を維持することでよいか。緩和すべきものがあれば指示を求める。
3. 承認する場合、`DEC-CONFORMANCE-SCOPE-RELAXATION-001`として記録してよいか。

## 8. 経緯

2026-08-04の会話で、Humanは「要件と設計を言語モデルで逆推定することを通常経路にしない。
作業自体を初期開発に入れないを緩めればいいだけのこと」と述べた。
本提案はその指摘を設計文書へ落としたものであり、承認そのものではない。
