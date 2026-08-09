# 役割中立Pilot／Review方式 試行計測 v1（Work 7A第2項 前駆slice）

- 記録日：2026-08-09
- 対象試行：`role_neutral_pilot_review` mode 初回1件
  （Pilot=Claude、Reviewer=Codex、Closer=Codex、risk `high`）
- 根拠：`docs/development/role-neutral-pilot-review-collaboration.md` §10
  「方式の採否は印象で決めず、試行Evidenceへ記録する」
- 対象作業：Work 7A第2項 前駆slice（read-only Git捕捉とcheckout移動後照合）。
  SCOPE `47217cb`（v1）／`4990ba6`（v2）→RED `a7e58eb`→GREEN `86f0f63`→
  修正2周（`2b27b4d`／`af8e005`、`0e19521`／`2c834b4`）→`verified`
  （review result v3、`bb9723b`）→完了projection（`c5e8332`）

## 1. 実測値

計数はsession記録とGit履歴から再構成した（時刻の自動計測は未導入）。計数規則：
Humanのchat message 1通を1 eventとし、承認と受け渡しを兼ねるmessageは両方の分類へ
各1件として計上する。内訳は§1.1に列挙する。

| §10計測項目 | 実測 | 備考 |
| --- | --- | --- |
| 着手指示から範囲固定までの時間 | 同一session内（2026-08-09） | mode宣言→SCOPE v1 commitまで途中停止なし |
| Humanによる受け渡し回数 | 13回 | §1.1のH1〜H13。scope関連5回、完了レビュー関連6回、Closer関連2回 |
| Humanによる承認・裁定回数 | 6回 | §1.1のA1〜A6 |
| 実装前の範囲修正件数 | 1回（scope v1→v2） | 範囲レビューv1のFinding 4件（P1×2、P2×2）と分割裁定を反映 |
| 範囲レビューの周回 | 2周＋再評価record 1件 | v1・v2とも判定は`reported_unverified`。v2は再評価record（Reviewer自身による過剰判定の訂正、blocking→0、条件2件）で`verified`へ訂正 |
| 完了レビューのFinding件数とseverity | 計4件（P1×3、P2×1）、全て機械反証つき | v1：3件、v2：1件、v3：0件 |
| 修正commit数 | 4（修正RED×2、修正GREEN×2） | Testを弱めた修正は0 |
| 全Test再実行回数 | Pilot 3回（1334→1337→1338）、Reviewer 3回 | すべてreceipt付き、failed 0 |
| 停止系判定の発生回数 | 範囲2回（scope review v1・v2の`reported_unverified`。うちv2は再評価で`verified`へ訂正）、完了2回（review result v1・v2の`report_execution_mismatch`）→最終`verified` | いずれも根拠（Finding）の列挙を伴う |
| 完了までの総経過 | 2026-08-09の1日内 | scope固定〜完了projectionまで |
| 未実施範囲の保持 | 維持 | Work 7A第2項checkbox開のまま、耐久Binding・Verification Run未実施、TODOは後続sliceへprojection |

### 1.1 Human event内訳

承認・裁定（A1〜A6。いずれもHumanのchat文言による）：

- A1：mode宣言（pilot／reviewer／work_item指定とrisk `high`確定）
- A2：Closer確定（`closer: codex`）
- A3：分割案1裁定（前駆slice化・後続分離・checkbox未完了維持、scope v2作成指示）
- A4：RED再開承認（「再評価record追加を確認した。RED開始を承認する。」）
- A5：RR-P1-001〜003の修正承認
- A6：RR-P1-004の修正承認（「RR-P1-004の修正を承認する」）

受け渡し（H1〜H13。Human↔Claude↔Codex間のchat中継。関連record併記）：

- H1：scope v1のレビュー依頼をCodexへ（→scope review v1）
- H2：scope review v1結果をClaudeへ（A3と同一message。→scope v2）
- H3：scope v2の再レビュー依頼をCodexへ（→scope review v2）
- H4：scope review v2結果と再評価方針をClaudeへ
- H5：再評価record化の依頼をCodexへ（→scope reevaluation v1）
- H6：完了レビュー依頼v1をCodexへ（→review result v1）
- H7：review result v1をClaudeへ（A5と同一message）
- H8：再レビュー依頼v2をCodexへ（→review result v2）
- H9：review result v2の要旨をClaudeへ（A6の前段）
- H10：再レビュー依頼v3をCodexへ（→review result v3）
- H11：review result v3の判定（`verified`）をClaudeへ
- H12：Closerの完了projection依頼をCodexへ（→completion projection）
- H13：「Codex作業終了」をClaudeへ（→Claudeの独立確認）

## 2. 観察（判断材料。裁定はしない）

- **検出力**：完了レビューのFinding 4件は全て「誤った合格」の機械反証つきで、
  Pilot（実装者）のTestに無い盲点だった。役割中立化後もReviewerの独立反証が
  防波堤として機能した。
- **周回コスト**：完了レビューが3周になった一因は、同一欠陥類型（変更検出の偽陰性）の
  変種（通常file→symlink）が2周に分かれて指摘されたこと。この反省は
  `work-review-protocol.md` §11.3「類型一括掃討」として規約化済み。
- **範囲段階の過剰判定**：範囲レビューv1で実装詳細（option位置・区切り・閾値）が
  blocking扱いになり、Reviewer自身の再評価で訂正された。§11.2「altitude規則」と
  §11.5「軽量な再評価」として規約化済み。
- **統制**：範囲の事後拡張・禁止操作・Testの弱化は、全周回の独立レビューで0件だった。
  handoffのcommit化とignore検査は運用どおり機能した。
- **未測定**：`low`／`medium` riskでの適用実績なし。従来方式との同条件比較なし。
  時間の自動計測なし。

## 3. 次

§10のとおり、一件の結果だけで恒久方式へ昇格しない。`low`／`medium`の適用結果を
分けて集め、継続・改定・廃止はHumanが判断する。
