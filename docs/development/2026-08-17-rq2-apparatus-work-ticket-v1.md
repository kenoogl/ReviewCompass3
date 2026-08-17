# RQ2 paired evaluation装置 作業票 v1（範囲固定・後続作業単位2）

- 作成日：2026-08-17
- 指示者：利用者（Human）。選択文言「正解表v1を確定。論点2も事前登録形で確定。後続(2)から
  実起動まで一気に進めて」（2026-08-17 chat）
- 作成者：Claude
- 種別：範囲固定文書（軽量作業票）。**実験計画v1の承認と上記文言が着手指示を兼ねる**
- 固定入力：事前走査record`records/development/2026-08-17-rq2-apparatus-prescan-v1.md`

## 1. 目的

RQ2 paired trialの4条件を機械実行し、材料選択・入力規模・Finding品質を集計する装置を作る。
実起動（後続3）とその集計（後続4）を同じ装置で行えるところまで固める。

## 2. 正本範囲（成果物）

1. **材料の移設**：`tools/evaluation/fixtures/rq2/`→`docs/evaluation/rq2-cases/`。file内容は
   変えない（digest不変）。契約が`docs/`配下のpathしか受け付けないため（事前走査§0-1）。
2. **正解表v2**：v1のpath表記だけを移設後の値へ差し替える。答・採点基準・限界の記述は不変。
   v2が事前登録の対象になる。
3. **装置の新設**：`tools/evaluation/rq2_paired_trial.py`——
   - ケース定義（10ケース・材料path・条件別の対象path集合）
   - 条件A／B／C／Dごとの契約chain組み立て（既存部品の読み取り専用呼び出し）
   - bridge経由の依頼record組み立て（assemble→機械記入→check）
   - launcherの注入口（試験ではfake、実起動では`reviewer_launch.launch_review`）
   - 正解表との採点（検出・誤検出・責務外の分類）
   - RQ2指標の集計（材料選択の不変性・入力トークン数・検出率・誤検出率）
   - 中断条件4種の機械判定（計画§5-4）
4. **試験**：RED先行。既存試験は無変更維持。**本作業の試験は外部起動を一切行わない**
   （fakeのみ。起動ゼロを機械確認する）。

## 3. 範囲外

- `tools/task_contract/`・`tools/request_builder/`・`tools/reviewer_launch/`・
  `tools/evaluation/reviewer_bridge.py`の変更（すべて読み取り専用利用）。
- 独立プールの選定・事前登録・実起動バッチ・集計の実行（後続3〜4。装置はここまでで作る）。
- 実験計画v1の条件定義・ケース数・起動上限の変更。

## 4. 受入条件

1. 正式再利用検索の証明書（`start_allowed: true`）。
2. 移設後の材料digestが移設前と**全件一致**する（`shasum -c`の終了コード0）。
3. RED：装置試験が実装前に失敗（単独終了コード非0）。
4. GREEN：新設試験＋保護対象（`test_rq1_contract_completeness.py`・`test_reviewer_bridge.py`・
   task_contract系・reviewer_launch系・request_builder系）の全通過（単独終了コード0）。
5. 条件A／B／C／Dの対象path集合が事前走査§3の表どおりになることを試験で固定する。
6. **外部起動ゼロ**の機械確認（試験内でlauncherを禁止fakeへ差し替える）。
7. `git diff --check`・意味単位commit・`work_unit_transition`合格。

## 5. 着手後の手続き

1. 作業別計画（schema 2）作成→先行commit。
2. 正式再利用検索→証明書固定（`start_allowed: true`でなければ停止）。
3. 材料移設＋正解表v2→commit。
4. RED→失敗確認→commit。
5. GREEN→全緑→commit。
6. 完了報告（後続3の実起動へ続く）。
