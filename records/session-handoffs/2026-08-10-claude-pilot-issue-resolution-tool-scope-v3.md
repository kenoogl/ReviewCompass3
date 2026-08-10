# 範囲固定 v3：V4 Issue resolve tool（deferred #1）— 完了レビューv1修復とfixture境界改定

- 作成日：2026-08-10
- 作成者：Claude（Pilot）
- 先行版：`scope-v2`（SHA-256 `ddc4b312ca529f58c38f2ad90127e0ec5ef065b03ffb1af17c1b10076eff2ee7`、
  変更せず保持。本v3で明記した改定点以外はv2の全条項が引き続き有効）
- 契機：完了レビューv1（`records/session-handoffs/2026-08-10-codex-review-result-issue-resolution-v4-v1.md`、
  SHA-256 `94f3230526add0f20ad4166aafdee5d0c14c405a73dbff6ec0fd49707829b926`、
  判定`report_execution_mismatch`、IR-COMP-001〜003 blocking）

## 1. Human裁定の固定（2026-08-10）

「IR-COMP-001と002の修正を承認する。IR-COMP-003は(a)scope改定とする」

- IR-COMP-001（非Human入力の受理）・IR-COMP-002（部分書込みの残留）：修正を承認。
- IR-COMP-003：**(a) scope改定**——Test fixtureにおけるconfigは、repository committedの
  実config（`config/development-issue-resolution-pilot-v4.json`）を**読み取り専用**で
  使用してよい。合成config複製による正本構造の重複を避けるための裁定である。
  台帳・裁定record・Evidenceは引き続き`tmp_path`内の合成のみとする。

なお、裁定record契約の変更（下記§2）に伴い、既存Testの裁定fixtureを構造化形式へ
更新する。これは承認済みFinding修復の一部であり、検査の緩和ではない。

## 2. IR-COMP-001の修復契約：裁定recordの構造化束縛

裁定record（`--ruling`）は、任意fileではなく次の**厳密形JSON**を要求する。

- 必須fieldちょうど：`decision_maker`・`human_id`・`decided_at`・`issue_id`・
  `target_state`・`wording`
- `decision_maker`は`"human"`のみ許可（AIへの判断委譲はchecklist §16どおり前倒ししない。
  将来の委譲は上流方針の改定とtool改定＝`high`レビューを経る）
- `human_id`・`decided_at`はCLI入力と**一致**し、`decided_at`はtimestamp形式
  （`YYYY-MM-DDTHH:MM:SS+HH:MM`）であること
- `issue_id`は対象issueと、`target_state`は`--to`と**一致**すること（裁定の対象束縛。
  無関係fileや別Issue向け裁定の流用を拒否）
- `wording`は空でない文字列（Humanの裁定文言の転記）
- 従来どおりpath＋SHA-256の一致も必須

違反はすべて`human_ruling_invalid`でfail-closed。

## 3. IR-COMP-002の修復契約：無残留の原子的書込み

- issue更新・解決record作成の両方を、一時file＋原子的置換で行う。
- **書込み途中の失敗（部分書込み）を注入しても**：issue fileは元bytesのまま、解決record
  は存在せず、一時fileの残骸も残らないこと。issue更新成功後にrecord書込みが失敗した
  場合は、issueを元bytesへ復元し、部分recordを残さないこと。
- 受入条件はこの**無残留性**であり、一時file名や置換手順の詳細は実装手段とする。

## 4. 受入条件の追加（v2 §6へ追加）

負例（追加）：

12. 裁定recordの束縛違反6態様——`decision_maker`が`"human"`以外／`issue_id`不一致／
    `target_state`不一致／`human_id`不一致／`decided_at`形式不正／必須field欠落——を
    すべて`human_ruling_invalid`で拒否し、無変更を保つ。
13. issue書込みへの部分書込み障害注入で、issue bytes不変・解決record非存在・
    一時file残骸なし。
14. 解決record書込みへの部分書込み障害注入で、issueが元bytesへ復元され・部分record
    非存在・一時file残骸なし。

既存の正例・負例はv2のまま（裁定fixtureの形式のみ§2の厳密形へ更新）。

## 5. その他

- 変更可能path・停止条件・関連回帰・公式全Test・commit境界はv2のとおり。
- 修正commit境界：**SCOPE v3**（本commit）→**修正RED**（Test変更のみ：裁定fixture更新
  ＋追加負例。単独実行で追加負例だけが現実装の欠陥どおり失敗することを確認）→
  **修正GREEN**（実装のみ＋Evidence追記＋receipt更新）→**review request v2**。
- risk `high`・案B・遷移元`registered`限定・実Issue非適用はv2のまま不変。
