# 参照Digest正式Issueの解決状態反映・独立開始前レビュー v1

- レビュー日：2026-08-14
- 対象commit：`0686d0e009259d4799651b5ccc1c70e9e25cdb68`
- 対象作業票：`docs/development/2026-08-14-authority-reference-issue-resolution-bootstrap-work-ticket-v1.md`
- 対象Issue：`ISSUE-AUTHORITY-REFERENCE-DIGEST-CHECK-001`
- レビュー範囲：固定値、三案比較、状態反映経路、変更境界、停止条件、対象commitへの別作業混入
- 実施範囲：読み取り、Digest計算、Git照合、既存validatorと対象試験。本記録以外を変更しない。

## 1. 判定

【判断】`correction_required / 開始不可`。

【判断】止める指摘は1件である。状態反映に使う既存処理は動作と独立レビューを確認できるが、ソース自身が
`lifecycle: provisional`、`normative_status: non-normative`、`promotion_required: true`と明示している。
ReviewCompass3自身のIssue台帳へこの処理を適用することは自己適用であり、現行開発方針の「`stable`と明示された
機能だけを自己適用に使う」という条件を満たさない。Humanの今回の承認は対象Issueを`resolved`へ反映する判断であり、
この不一致を提示したうえで処理を現役化する判断ではないため、現役化を承認したものとは扱わない。

【判断】commit `0686d0e`への別作業混入は、意味単位commitの規則には反するが、本状態反映を止める直接原因ではない。
対象Issue、設定、G01 Evidenceは混入commitで変わっておらず、作業ツリーもcleanである。履歴書換えは行わず、混入を
本記録に残し、以後のcommitを明示pathだけで行えば安全に続行できる。ただし上記の成熟度不一致が解消するまで、
Issue状態反映そのものは開始しない。

## 2. 固定材料

【実測】対象commitは実在し、レビュー開始時のHEADと一致した。固定対象のSHA-256は次のとおりである。

| 対象 | SHA-256／状態 |
| --- | --- |
| 作業票v1 | `554f38ca40474ce56900e102bfd7f5246150e5c393b0805b0cc89e5bcb87b9f5` |
| Issue | `d260ed570598f56ada2cd6b4e54f15543bba0e792db65c14403a038f8100afbe` |
| 正規設定 | `ed274e487318d44baed701ffbc8a1130df3e9d81cadca96515848a2bea228a8e` |
| G01実施Evidence | `52022b04a72b1c5df458f949f80bde1383ef4238f8d6b6b024977eac6ad398cd` |
| G01独立完了レビュー | `c441ef796f34959cadf5a111826af50fa02e46a3e367f896768a417940f78515` |
| Issueの現状態 | version `1`、state `registered`、正規record検証合格 |

【記録】G01独立完了レビューは`verified`、止める指摘0件、報告不一致0件である。作業票は、利用者の直前発言
「承認」を、`ISSUE-AUTHORITY-REFERENCE-DIGEST-CHECK-001`の`resolved`反映に対するHuman判断として固定している。

## 3. 三案比較と変更境界

【実測】作業票は、A「状態を変えずHuman判断記録だけ」、B「既存処理で状態反映」、C「Issueと解決記録を手編集」の
異なる3案を、単純さ、処理時間、メモリ使用量、頑健さ、変更範囲、保守負担、戻しやすさの7観点で比較している。
既存機能だけを使う案Bが最小実装案であり、新しいコード、設定、schema、検査器、関門を要しない。

【判断】三案比較自体と案Bの処理内容は妥当である。Aは実態と台帳の不一致を残し、Cは正規処理を迂回する。
ただし案Bを自己適用できるという開始前提だけが、処理の成熟度宣言と一致していない。

【実測】計画された変更は、Human判断記録1件、対象Issueの`state`と`content_digest`、新規解決記録1件、
独立完了レビュー1件、完了後のTODOに限定される。コード、試験、設定、他Issue、G01成果物、第3段完了判断は対象外である。
既存処理は、遷移元`registered`、遷移先の終端状態、Human判断の6項目、判断記録とEvidenceのSHA-256、解決記録の
新規pathを検証し、事後の台帳検証に失敗すればIssueを元のbytesへ戻す。

## 4. 止める指摘

### AR-RES-START-001：暫定処理を自己適用する計画になっている

【実測】`tools/development/issue_resolution_v4.py`の冒頭は次を明示する。

- `lifecycle: provisional`
- `normative_status: non-normative`
- `promotion_required: true`

【実測】`docs/development/2026-08-02-development-policy.md`の「段階的自己適用」は、現行契約と試験を満たし、
`stable`と明示された機能だけをReviewCompass3自身へ適用できると定める。`AGENTS.md`も自己適用にはstable機能だけを
使うと定める。

【記録】この処理には2026-08-10の高risk独立完了再レビューがあり、24件の対象試験、67件の関連試験、当時の
全試験1,381件に成功し、判定は`verified`だった。後追いレビュー対象一覧も同処理を「現基準済」としている。

【判断】独立レビューは動作の信頼性を支持するが、成熟度を現役へ変更するHuman判断ではない。ソースの明示宣言を
無視して「正規だから自己適用可能」とは判定できない。これはauthorityと自己適用境界に関わるため停止条件に該当する。

【判断】最小回復は、新しい処理を作ることではない。既存の`issue_resolution_v4`について、現在の実装・対象試験・
独立レビューを材料に、現役化するかを別の小さい判断単位で確認し、Humanが現役化を承認した場合だけ状態反映へ戻る。
現役化しない場合はIssueを`registered`のまま維持する。処理の修正、schema変更、追加試験、履歴書換えは現時点で不要である。

## 5. commit `0686d0e`への別作業混入

【実測】commit `0686d0e`には、対象作業票に加えて次の3 pathが含まれる。

- `TODO_NEXT_SESSION.md`
- `docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md`
- `records/development/2026-08-14-recovery-plan-v5-stage4-formal-product-code-identification-amendment-decision-v1.md`

【判断】作業票だけを意味単位commitにする意図と実commitが一致せず、意味単位commit不一致である。作業票§8も、
開始時に存在した第4段差分のstageとcommitを本作業の対象外としているため、commit結果との不一致を隠してはならない。

【実測】一方、commit `7246526`から`0686d0e`までで、対象Issue、正規設定、G01実施Evidence、G01独立完了レビューの
差分は0件である。混入後のTODOは第4段追補の新しいSHA-256とDecision参照を反映しただけで、Issue状態反映の開始条件、
対象Issue、完了条件を変更していない。レビュー開始時のworktreeとindexはcleanだった。

【判断】混入は履歴上の一回の境界違反として保存し、これを直すためのrebase、reset、amendを行わない。内容を再編集せず、
今後のHuman判断記録、状態反映、解決記録、レビュー記録、TODOをそれぞれ合意した意味単位と明示pathだけでcommitすればよい。
混入自体を直す新しい機構・試験・関門も提案しない。

## 6. 反証と機械確認

1. 【実測】混入commitが対象Issueまたは固定Evidenceを変えた可能性を`git diff`で調べた。対象4件と設定の差分は0件で、
   反証は不成立だった。
2. 【実測】対象Issueを現行configでrecord単体とrepository全体の両方へ検証し、version `1`、state `registered`で
   合格した。
3. 【実測】`.venv/bin/python3 -m pytest tests/test_issue_resolution_v4.py -q`は終了コード0、24件成功だった。
4. 【実測】暫定宣言が過去の文言だけで、別の現役化判断により上書き済みではないかを検索した。高risk独立レビューと
   現基準済の分類は見つかったが、`lifecycle`、`normative_status`、`promotion_required`を変更するHuman判断または
   ソース変更は見つからず、反証は成立した。開始不可の判断を維持する。

## 7. 手戻り

【実測】Issue単体とrepository全体を検証する最初の読み取り用commandで、存在しない内部関数`_read_json`を呼び、
製品検証へ到達する前に`AttributeError`、終了コード1となった。

- 対象操作：現行Issueの正規検証
- 期待executor／実executor：Reviewerの読み取り用Python command／同command
- 手作業理由：なし
- 事象とEvidence：内部関数名の事前確認不足。JSON標準読込みと公開validatorを使う再実行は終了コード0
- 機械処理候補・route：一回のレビューprobe訂正であり、製品欠陥ではないため候補化せず本記録へ固定

## 8. 開始再判定の条件

次のどちらかをHumanが判断した後に再判定する。

1. 既存処理を現役化する：現在の実装・対象試験・独立レビューを確認材料とし、`stable`として自己適用へ使う判断を
   記録する。その後、作業票の処理成熟度前提だけを限定修正する。
2. 現役化しない：Issueを`registered`のまま維持し、本状態反映作業を終了する。

【判断】1を選んでも、状態反映の対象、Human判断、Evidence、変更key、停止条件を広げない。追加実装や全体設計の
見直しを前提にしない。

## 9. 未実施

【未実施】Human判断記録の作成、Issue状態反映、解決記録作成、TODO更新、コード・試験・設定・既存記録の変更、
新しい機構・試験・関門の提案、履歴書換え、外部送信、第3段完了判断は行っていない。リポジトリ内の変更は本記録1件だけである。
