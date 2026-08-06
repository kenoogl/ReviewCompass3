# 作業レビュープロトコルへの高risk観点追記 Decision v1

- decision ID：`DEC-WORK-REVIEW-PROTOCOL-HIGH-RISK-001`
- decision maker：Human
- decided at：2026-08-07
- 指示：本sessionのHuman文言「追記を承認する。」および「未実施項目に対応」（2026-08-07）

## 1. 背景

実装codeのチェックの要否に関する検討で、次の事実を確認した。

- これまでの独立レビュー（独立監査、Challenge、独立検証）の対象は文書・候補・計画に限られ、
  実装codeのレビュー記録はどのWorkにもない。
- テストを書く実行者と実装を書く実行者が同じ場合、盲点が共有される。実例として、機械操作routing v2は
  TDDのGREEN後に「execution receiptの改竄を拒否できない」欠陥が後から発見され、訂正を要した
  （`DEC-MACHINE-OPERATION-ROUTING-RECEIPT-INTEGRITY-001`）。
- 当該欠陥は、追記前の`docs/development/work-review-protocol.md`の全手順（報告と事後状態の一致、
  RED根拠、対象Test・全Testの合格）を通過して`verified`になる。すなわち追記前の手順書では検出できない。

## 2. Humanの決定

Humanは、`docs/development/work-review-protocol.md`への次の追記を承認した。

1. **§3**：既定で`high`とするriskの判定基準を追加した。守り役のcode（validator、Digest照合、
   承認関門の判定、改竄拒否など、他の成果物の合否を決めるcode。失敗が「誤った合格」として黙って
   現れるため）と、不可逆操作を行うcode（移行、削除、上書き、外部送信）である。
2. **§4.4**：`high`では、実行者のfixtureに存在しない反証を最低1件、reviewerが新たに作って機械で試す
   手順を追加した。守り役のcodeでは誤って合格させる方向（改竄、偽装、迂回、境界値）を優先し、
   反証が成立した場合は検証結果として分離して、承認なしに実装修正へ移らない。
3. **§5**：`high`のcodeでは、期待挙動を実行者のTestからではなく上流（承認Decision、設計、Contract、
   Requirement）から独立に導出して照合し、実行者が書いたTestの再実行だけを独立oracleに数えない
   規定を追加した。
4. **§10**：レビュー完了チェックへ「`high`では、実行者のfixtureに無い反証を新作して機械で試した」を
   追加した（Human文言「未実施項目に対応」による）。

## 3. 対象と実Digest

| 対象 | 値 |
| --- | --- |
| 追記対象 | `docs/development/work-review-protocol.md` |
| 追記前SHA-256（commit `56dbfeb`の親時点） | `1a4f8ce267793f1d80585f6a01ea6f2fd622f7185b7d6a527da7502acf5f2d00` |
| 追記1〜3反映後SHA-256（commit `56dbfeb`） | `a55edfcdfc7fc3690e10eccf667014c3ab6ef295762186bb5c69ed55484e5ec1` |
| 追記4反映後SHA-256（本Decisionと同じ作業単位） | `22856c9836de2fd1a5d3a8a79d9437ea82150c8e167fb9ddc40ac6b82bb0a923` |
| 追記1〜3のcommit | `56dbfeb438324ebd926b42594478b50e10c54b7a` |

## 4. この決定が承認していないこと

- 実装codeレビューの一斉実施、過去の完了済み作業単位の再レビュー、レビュー漏れ一覧の遡及処置。
- 変異検査（mutation testing）の系統的測定の前倒し。これはWork 8への割当てを維持する
  （`records/development/2026-08-06-work6a-inventory-correction-v1.md`）。
- AGENTS.md、Development Policy、チェックリスト、validator、test、configの変更。
- 所見を生成するLLMレビュー経路（外部API・サブエージェント）の実装。これは別Task Contractのままとする。
- 本手順書の適用発動条件の変更。独立レビューを高risk境界へ適用する方針はAGENTS.mdの既存記述の
  とおりであり、本Decisionは手順書側の観点を具体化しただけである。
