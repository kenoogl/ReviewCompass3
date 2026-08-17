# TODO_NEXT_SESSION

更新日：2026-08-18

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5第1〜5段・正式ツール化（契約008〜014）・デプロイ方針決定・全体見取り図までは前回どおり。今回、**評価データ取得（計測メタ・RQ1装置・reviewer接続・RQ2 paired trial）が完了**——実起動30回・裁定確定・論文データ一式をrecord化（論文構想：Task Contracts for Evidence-Bounded LLM Code Review、8/30目標）。RQ2の副産物4件（手順書と実装の食い違い・作業票表題・終了コード語彙・契約014注記）も改善候補経路で対処完了。全景は`docs/current/reviewcompass3-overview-current.md`
- 現在作業：なし。レビュー基盤moduleは休止中（2026-08-17休止record）。本回完了：RQ2実験全工程（B/C全10ケース・A1/A2/D副実験・主題適中率の採用）・副産物4件対処・セッションログ終了コード是正（partialは非対応4を返す）
- Task Contract：`なし（契約014受入完了・注記追記済み。次契約は未定義）`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了・条件付き再開待ち`、影響：次縦切りの選択・着手を妨げない持ち越し負債である、次：Issue状態を変更せず、状態固定試験の変更・削除または別途承認されたWork 8測定の前にだけ対象限定で再開する

## 最新のauthority／Evidence

- [RQ2 paired trial実行Evidence（§11に裁定後の確定集計を追記）](records/development/2026-08-17-rq2-paired-trial-evidence-v1.md) — SHA-256 `c6dbfa836866524b41edcd156e24b7cd39cec615110a0a9c1c793713a8b5522f`
- [RQ2裁定・議論・副産物v2（論文データ一式の表・7語彙・主題適中率）](records/development/2026-08-18-rq2-adjudication-and-byproducts-v2.md) — SHA-256 `f4191636ea1ee701b3fbc29f42a24e0860afd3c81633a5bb543215777134a152`
- [RQ2生データ（31実行の機械記録）](records/development/2026-08-18-rq2-paired-trial-dataset-v1.json) — SHA-256 `d34ecd24a8d87c49e5b50f4ae204295841622ea12c34886e29dba5a32c85b893`
- [副産物4件の仕分け判断record（委任実施・全4件対処済み）](records/development/2026-08-18-rq2-byproduct-candidates-triage-decision-v1.md) — SHA-256 `86ec0e3a5aa064d4f929970a1e576bffc31c387c02e221a555e733d39280cbcf`
- [評価データ取得計画v1（順序1〜4完了・順序5未着手）](docs/development/2026-08-17-evaluation-data-acquisition-plan-v1.md) — SHA-256 `c666bdd7d0b5c44a8fbb876238a19c1d05ee245e693a2b104ceee514cdad55cb`
- [全体見取り図（人向け全景。受入完了時にTODOと同時更新）](docs/current/reviewcompass3-overview-current.md) — SHA-256 `f53b12562a1cc5b8a6d296a7e7e3470e5b130210b2371a1303939f4c9b39500b`
- [デプロイ方針Decision（論点1〜4の裁定・next型起点・訂正版P3）](records/development/2026-08-17-deployment-policy-decision-v1.md) — SHA-256 `ad3bbf84931f55d27c62e5243fede3fbfe2cc4c4d97cc87404ccab969e597671`
- [レビュー基盤module開発の一時終了record（pending残件と再開の入口）](records/development/2026-08-17-review-tooling-module-pause-decision-v1.md) — SHA-256 `9b4d184f378d5dc8dad203caba5daf6b6e58b2471dd387187d5c5ede971cfd6c`
- [文字列理解の失敗類型と対策原則（参照record・事前走査の必読入力）](records/development/2026-08-17-text-interpretation-failure-principles-reference-v1.md) — SHA-256 `ea482a3c7653b0966316012f43cc87ae426cdd5e429348a7f96c4e7f05ecd7b6`
- [現行50要求を解決する要求権限束v2](records/requirements/authority/rc3-requirements-authority-2026-08-03--v2.json) — SHA-256 `760e33ea2ecf6937f56d7bf8d2bd703b18b47dbd2bd6b2bd5919e0dd556d9dae`

## 次に行う一作業

なし（module休止中・次契約未定義）。再開の選択肢：(1) 論文執筆（8/30目標。RQ1初回計測とRQ2確定集計・生データ一式が揃った）、(2) 評価の運用集計コマンド（データ取得計画§4順序5）、(3) 休止record §3のpending残件（縦C合議／codex-cli第3 backend＝疎通回復が合図／外部API後続）、(4) デプロイ版の作成（合図＝他アプリ開発の開始決定）。いずれも利用者の指示で選択し、事前走査（6手順・必読原則record）で着手する。

開始条件：

- 利用者の再開指示と順序選択がchatで得られる

完了条件：

- 選択された作業単位の事前走査record固定（または新規作業単位の範囲固定文書）

後続作業：休止record §4、デプロイ方針record §4〜5、RQ2裁定record v2 §7（正解表7語彙の正式反映の形式判断ほか）を参照。

## blocker・Human判断待ち

- blocker：codexCLIのトークン枯渇は継続（第3 backend候補として疎通回復待ち）。レビュー実行はagy headless正式経路とclaude-subagent（Tier 3・明示受容つき）の2経路が稼働
- Human判断待ち：なし（module休止中。再開の時機・順序は利用者判断）

## stale・deferred

- stale：なし
- deferred：外部API直接送信経路の後続はpending（2026-08-16。統合時は判定record規約準拠）。後続候補＝`review_plan`自動変換・縦C合議・codex-cli backend（改善候補仕分け2026-08-17の裁定は各candidate recordを参照）。デプロイ関連：デプロイ版作成は他アプリ開発の開始決定が合図・RC3版nextの返答語彙議論は後日・projection導出の本実装は運用実測後。RQ2持ち越し（裁定record v2 §7）：正解表7語彙の正式反映の形式判断・`read_only_entry`独自語彙の統合は別作業単位。契約014持ち越し：残存5件（本文なし前置のみfile）は放置可・新前置種別は`record-run`非対応件数の急変が合図

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：RQ2装置14件（`tests/test_rq2_paired_trial.py`）、前置解釈20件（`tests/test_session_log_prefix_interpretation.py`・注記の挙動固定2本を含む）、session_logs系全域361件——各単独終了コード0（2026-08-18実測）
- 直近の全Test：禁止認証隔離条件の正規全試験2,482件成功・終了コード0（2026-08-16・契約013完了時点の実行。以後の作業単位はsession_logs系・評価系の単独緑で受入）
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
