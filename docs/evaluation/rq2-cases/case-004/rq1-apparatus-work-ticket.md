> 本fileはReviewCompass3の評価実験（RQ2 paired trial）で使う複製材料である。運用中の
> record・手順書ではないため、本fileを根拠に運用判断をしないこと。

# RQ1装置（Contract completeness計測） 作業票 v1（範囲固定・データ取得順序2）

- 作成日：2026-08-17
- 指示者：利用者（Human）。選択文言「続けて順序2（RQ1装置）に着手。範囲固定文書から進めて」
  （2026-08-17 chat）
- 作成者：Claude
- 種別：範囲固定文書（軽量作業票）。**承認までは着手しない**
- 上位計画：評価データ取得計画v1 §3優先1a・§4順序2。固定入力＝事前走査record
  `records/development/2026-08-17-rq1-apparatus-prescan-v1.md`

## 1. 目的

論文RQ1（Contract completeness——Task ContractからのPlan compilationが実行前に欠落・競合を
検出できるか）の5指標を、**機械生成の指標JSON**として計測できる装置を作る。照合・検出の中核は
既存部品（`check_requirement_coverage`・`compile_contract`・`definition_challenge`）を呼ぶだけ
とし、**新しい検証ロジックは書かない**（検証器の重複実装の禁止）。

## 2. 正本範囲（成果物）

1. **装置の新設**：`tools/evaluation/rq1_contract_completeness.py`（新パッケージ
   `tools/evaluation/`）＋entry（単体CLI）。入力＝Contract fixture集合、出力＝**正準JSON一行**
   の指標（coverage 2種・再生成一致・negative検出率・誤停止率・数値の来歴欄）。
2. **fixture群の新設**：`tools/evaluation/fixtures/rq1/`——正常・欠落・競合・stale の4群
   （初版各3〜5件・後から追加できる登録形）。正常系は既存E2E fixtureの形を流用。
3. **試験の新設**：RED先行（装置の指標計算・fixture判定の固定）。既存task_contract系試験は
   無変更維持。
4. 指標の定義（本票で固定・§4）。

## 3. 実装方法（3案比較）

- **案A（採用）**：集計器1本＋fixture登録形。既存部品を読み取り専用で呼ぶ。新検証ロジックなし。
- 案B：既存E2E試験を拡張して指標も出す——試験と計測装置の責務が混ざり、試験の意図変質risk。
  不採用。
- 案C：汎用評価framework（複数RQ対応の抽象層）を先に設計——早すぎる一般化。RQ2装置（順序4）
  の実測後に共通化を判断。不採用。

## 4. 指標の定義（固定）

| 指標 | 定義 |
| --- | --- |
| Requirement-to-obligation coverage | `REQUIREMENT_OBLIGATIONS`の16要求のうち、Contractの義務欄へ束縛が解決したもの÷16（既存照合器`check_requirement_coverage`の結果を数える） |
| obligation-to-plan coverage | Contractの義務のうち、6 Plan viewのいずれかへ写像されたもの÷全義務（compile出力から機械照合） |
| 再生成一致率 | 同一入力で`compile_contract`をN回（既定3回）実行し、**sealed record単位のbyte一致**が成立した割合 |
| negative case検出率 | 欠落・競合・stale fixtureのうち、compile前検査（definition_challenge・compile gate）が**blocking検出または停止**したもの÷negative総数 |
| 誤停止率 | 正常fixtureのうち、不当にblocking／停止となったもの÷正常総数 |

## 5. 受入条件

1. 正式再利用検索の証明書（`start_allowed: true`）——着手後手続き§6の1-2。
2. RED：装置試験が実装前に失敗（単独終了コード非0）。
3. GREEN：新設試験＋task_contract系既存試験の全通過（単独終了コード0）。
4. `git diff --check`・意味単位commit・`work_unit_transition`合格。

## 6. 着手後の手続き（承認後の順序）

1. 作業別計画（schema 2・能力2件：指標集計・fixture判定駆動）→先行commit（計画内容は
   完了報告で明示）。
2. 正式再利用検索→証明書固定。
3. RED（装置試験＋fixture初版）→失敗確認→commit。
4. GREEN（装置実装）→全緑→commit。
5. 初回計測→Evidence転記→完了報告。

## 7. 範囲外

- `tools/task_contract/`本体・既存試験の変更（読み取り専用利用）。
- RQ2装置（paired evaluation・順序4）・reviewer接続（順序3）・運用集計（順序5）。
- 指標recordの定常生成（計測はコマンド実行ごと。record化はHuman指示時）。
- 汎用評価frameworkの先行設計（RQ2実測後に共通化判断）。
