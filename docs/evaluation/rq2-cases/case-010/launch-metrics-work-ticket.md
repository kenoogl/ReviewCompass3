> 本fileはReviewCompass3の評価実験（RQ2 paired trial）で使う複製材料である。運用中の
> record・手順書ではないため、本fileを根拠に運用判断をしないこと。

# 計測メタ追記＋復元可能性表 作業票 v1（範囲固定・データ取得順序1）

- 作成日：2026-08-17
- 指示者：利用者（Human）。選択文言「順序1（計測メタ＋復元可能性表）に着手。範囲固定文書から
  進めて」（2026-08-17 chat）
- 作成者：Claude
- 種別：範囲固定文書（軽量作業票）。**承認までは着手しない**
- 上位計画：評価データ取得計画v1（`docs/development/2026-08-17-evaluation-data-acquisition-plan-v1.md`）
  §4順序1。固定入力＝事前走査record
  `records/development/2026-08-17-launch-metrics-recoverability-prescan-v1.md`

## 1. 目的

reviewer-launch実行の**時間・prompt規模が現在記録されず、事後復元できない**（実測）。以後の
全レビュー実行を論文データ（RQ2の実行時間・費用・入力規模、従軸H4）にするため、計測メタを
私有領域`launch.json`へ追記する。あわせて、計画§3の全指標について「現記録から復元できるか」を
**復元可能性表**として固定し、以後の計測欠落を防ぐ（初代`recoverability.md`の型）。

## 2. 正本範囲（成果物）

1. **コード変更（最小）**：`tools/reviewer_launch/core.py`——launch実行の時間計測と
   `launch.json`への4項目追記：`started_at`・`finished_at`（UTC）・`elapsed_seconds`・
   `prompt_bytes`。**repo内の判定record schema・事後照合4点・安全境界・CLI引数は不変**
   （後方互換の観測追加。トークン数はraw応答内に保存済みのため追記しない——機械復元可能を
   復元可能性表に明記）。
2. **試験**：新項目を検証するRED先行試験の追加（`tests/test_reviewer_launch.py`。既存67件は
   無変更維持）。
3. **復元可能性表record**：`records/development/`へ新設。計画§3の全指標（RQ1/RQ2・H4/H5/H7・
   コスト）×「現記録からの復元可否・復元手段・欠落」の表。機械確認に基づく【実測】ラベルつき。
4. 手順書・AGENTS.md・G30・pyproject：変更なし。

## 3. 契約との関係（Human確認点）

変更は契約010候補v2 §8変更上限の1・2の範囲内であり、挙動・判定・schema不変の観測追加のため、
**新契約は立てず本軽量作業票＋通常承認で扱う**。契約010の保護試験（67件）の緑維持を受入条件に
含めることで保護境界を守る。

## 4. 受入条件

1. 正式再利用検索の証明書（`start_allowed: true`）——コード変更を含むため適用（§5手順1-2）。
2. RED：新項目検証試験が実装前に失敗（単独終了コード非0）。
3. GREEN：新設試験＋`test_reviewer_launch.py`全件＋関連試験の全通過（単独終了コード0）。
4. 実機確認1回：`record-run`ではなく**次回のレビュー起動時**に新メタが記録されることの確認は
   将来の実行に委ね、本作業票では試験（模擬実行）で代替する（外部起動はHuman承認境界のため）。
5. 復元可能性表recordのcommit（計画§3全指標を網羅・復元手段の実在を機械確認）。
6. `git diff --check`・意味単位commit・`work_unit_transition`合格。

## 5. 着手後の手続き（承認後の順序）

1. 作業別計画（schema 2・能力2件見込み：実行メタ計測・復元可能性照合）作成→Human確認→先行commit。
2. 正式再利用検索→証明書固定（`start_allowed: true`でなければ停止）。
3. RED（新項目試験）→失敗確認→commit。
4. GREEN（core.py追記）→全緑→commit。
5. 復元可能性表record作成→commit。
6. 完了報告（受入条件の対応付け）。

## 6. 範囲外

- 判定record（repo内）のschema変更・事後照合の変更・トークンの独自集計（rawから復元可）。
- paired evaluation装置・RQ1装置・reviewer接続（計画§4の順序2〜4）。
- 集計コマンド（順序5）。
