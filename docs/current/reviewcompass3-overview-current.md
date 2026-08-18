# ReviewCompass3 全体見取り図

- 役割：**人が全景と進捗を一目で見通すための資料**。Workflow stateや完了Evidenceの正本では
  ない（正本は各行の参照record）。現在位置の詳細は`TODO_NEXT_SESSION.md`を見る。
- 更新規則：**作業単位の受入完了時（TODO更新と同時）にのみ**状態欄を更新し、**同じ行の時点も
  更新する**。詳細・履歴・件数を書かない（古びる情報はリンク先の正本に置く）。将来、現在位置の
  機械導出（計画正本§10.1.1）が実装されたら、本資料はその人向け描画に置き換わる。
- 時点の意味：その状態が確定した日（根拠recordの日付）。「〜日付」は複数作業の完了範囲、
  「日付〜」はその日から継続中、を表す。
- 骨格の出自：`docs/design/2026-08-17-rc3-overall-plan-memo-import-v1.md`のA〜F構造
- 状態語彙：完了／進行中／休止／未着手／凍結
- 最終更新：2026-08-18

## A. 製品本体（Work 1〜8）

| 項目 | 状態 | 時点 | 主な根拠 |
| --- | --- | --- | --- |
| Work 1〜5B（固定入力・配置基盤・セッションログ経路・目的/要求統合・最初の縦切り・異常系・内部実装試行） | 完了 | 〜2026-08-15 | 立て直し計画v5 §11第1〜5段の完了record群（`records/development/`） |
| Work 7A（4種root分離・checkout移動照合） | 一部完了 | 2026-08-09 | `tools/deployment/local_integrated_roots.py`ほか（残りは未着手） |
| Work 7B（更新・移行・解除・巻き戻し） | 未着手 | — | — |
| Work 8／8A（新旧方式の比較評価・限定並行） | 未着手 | — | Work 8測定の前提に`ISSUE-TEST-GROWTH-STATE-PINNING-001`の限定再開（D欄） |
| 評価データ取得（計測メタ・RQ1装置・reviewer接続・RQ2 paired trial実験＝実起動30回・裁定確定） | 完了 | 2026-08-17〜2026-08-18 | `records/development/2026-08-17-rq2-paired-trial-evidence-v1.md`（§11確定集計）・`records/development/2026-08-18-rq2-adjudication-and-byproducts-v2.md`（論文データ一式の表） |
| 評価の運用集計コマンド（データ取得計画の順序5・v7＝系統意味づけ・道具正規化・活動時間まで） | 一部完了（v8＝日別展開等が候補） | 2026-08-18 | `records/development/2026-08-18-operational-metrics-dataset-v7.json`と同Evidence v1〜v7 |
| 最終公開評価 | 未着手 | — | — |

## B. レビューの仕組み

| 項目 | 状態 | 時点 | 主な根拠 |
| --- | --- | --- | --- |
| 外部送信の安全経路（契約008・009） | 完了 | 2026-08-16 | 各製品受入判断record |
| Reviewer起動アダプタ／依頼組み立て器／第2 backend／自由文類型（契約010〜013） | 完了 | 2026-08-17 | 各製品受入判断record。起動2 backend体制（agy＝Tier 1既定・claude-subagent＝Tier 3明示受容） |
| レビュー基盤moduleの続き（縦C合議・codex-cli第3 backend・外部API後続） | **休止** | 2026-08-17 | `records/development/2026-08-17-review-tooling-module-pause-decision-v1.md`（再開は利用者判断） |

## C. 開発コードの管理

| 項目 | 状態 | 時点 | 主な根拠 |
| --- | --- | --- | --- |
| 正式再利用検索（実装前の機械検索・証明書） | 完了（稼働中・`--plan`のみへ引数廃止） | 2026-08-15〜 | `docs/development/prompts/scope-prescan-run.md`手順5 |
| 実測・引数の機械化（測定ブロック＋二重実行guard・CLI既定値化・計画writer・review-plan既定） | 完了（稼働中） | 2026-08-18 | `records/development/2026-08-18-llm-machine-split-audit-v1.md`（対策1〜3の台帳）と同日Evidence群 |
| 高危険検証コードの再レビュー | 一部完了 | 2026-08-07 | E/A/B群は修正済み。残（旧C/D群）は立て直し計画v5 §10の枠組みで扱う |

## D. テストコードの整理

| 項目 | 状態 | 時点 | 主な根拠 |
| --- | --- | --- | --- |
| 試験準備の共通化・要求対応の機械照合 | 完了 | 〜2026-08-10 | 立て直し前の整理record群 |
| 状態固定試験の扱い | 持ち越し | 2026-08-06登録 | `ISSUE-TEST-GROWTH-STATE-PINNING-001`（条件付き再開待ち。全試験自体は安定） |

## E. 作業状態の管理

| 項目 | 状態 | 時点 | 主な根拠 |
| --- | --- | --- | --- |
| セッションログ保全（3系統一括`record-run`・現セッション既定除外。終了コード語彙は2026-08-18是正） | 完了（稼働中） | 2026-08-17〜 | `docs/development/prompts/session-log-record-run.md`・`records/development/2026-08-18-session-log-exit-code-vocabulary-evidence-v1.md` |
| 前置record解釈（実会話の取りこぼし解消・遡及。契約014） | 完了 | 2026-08-17 | `records/development/2026-08-17-session-log-prefix-interpretation-product-acceptance-decision-v1.md` |
| TODO handoff（現在位置の人向け入口） | 稼働（暫定） | 2026-08-04〜 | `docs/development/prompts/todo-handoff-update.md`。**現在位置の機械導出（projection）は未実装**——方針は横断欄のデプロイ方針record §4c |
| 改善候補・Issueの経路 | 稼働 | 2026-08-06〜 | AGENTS.md §4の既存経路 |
| 初期開発checklist | **凍結** | 2026-08-17 | `docs/development/2026-08-03-initial-development-checklist.md`（時点記録。詳細参照は可） |

## F. LLM協業

| 項目 | 状態 | 時点 | 主な根拠 |
| --- | --- | --- | --- |
| 操縦Claude＋独立レビューの体制 | 完了（Bへ正式化） | 2026-08-17 | pilot方式→契約010〜013の正式経路へ発展 |
| codex-cli（第3 backend候補） | 待機 | 2026-08-16〜 | トークン枯渇の疎通回復が合図 |
| 運用規範のrepo正本化（私的メモリ→AGENTS §2・§3＋手順書） | 完了 | 2026-08-18 | `records/development/2026-08-18-agents-norm-transfer-decision-v1.md` |

## 横断（配置・デプロイ）

| 項目 | 状態 | 時点 | 主な根拠 |
| --- | --- | --- | --- |
| デプロイ方針（当面ローカル・配置同型性・next型起点・訂正版P3） | 決定 | 2026-08-17 | `records/development/2026-08-17-deployment-policy-decision-v1.md` |
| デプロイ版の作成（配置規約・パス一元化・lint・入口文書・next最小形） | 一部完了（パス一元化＝配置依存3箇所解消のみ先行） | 2026-08-18 | `records/development/2026-08-18-placement-root-resolution-evidence-v1.md`。残りの合図＝**他アプリ開発の開始決定**（利用者。AGENTS規範の持ち出し仕分けを含める） |
