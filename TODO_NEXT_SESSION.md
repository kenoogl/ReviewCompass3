# TODO_NEXT_SESSION

更新日：2026-08-18

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5第1〜5段・正式ツール化（契約008〜014）・デプロイ方針決定・評価データ取得（RQ1装置・RQ2 paired trial＝実起動30回・裁定確定・論文データ一式）・RQ2副産物4件の対処・論文執筆開始（WSSE 2026 Special Session・締切**2026-08-30**・LaTeX 5頁・double-blind＋arXivフルの二本立て）までは前回どおり。今回、RQ2持ち越しの**採点7語彙の正式反映を裁定**（案B＝集計側を正本・正解表v3はケース集の再利用決定が合図）、**配置依存3箇所の解消**（デプロイ方針4b-1。`tools/common/roots.py`へ一元化・指紋pin追加済み）、**順序5の運用集計コマンド**（dataset v1固定）を完了——**評価データ取得計画v1の全順序が完了**。続けて**運用集計v2**（H5束縛照合＝一致77.6%・dataset v2固定）、**検索CLIの引数廃止**（保存先・方針版・時刻を自動解決）、**測定ブロックの機械生成tool**（宣言JSON→機械実行→生成file参照。実測の転記を構造的に排除・手順書規律も「転記は例外」へ改定）も完了——方針転換はHuman指示「手作業部分を極力廃してLLMは本来の役割のみ」。全景は`docs/current/reviewcompass3-overview-current.md`
- 現在作業：**論文執筆（WSSE短縮版が締切物）**。執筆体制＝**本スレッドが執筆（`docs/paper/`配下のみ書く）・別スレッドが継続開発（TODO・見取り図・records・製品コードの正本管理）**。論文データの更新は開発スレッドが装置で再集計し新版として固定、執筆側は固定版のみ引用（計画v2 §3の分担規則）
- Task Contract：`なし（契約014受入完了・注記追記済み。次契約は未定義）`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了・条件付き再開待ち`、影響：次縦切りの選択・着手を妨げない持ち越し負債である、次：Issue状態を変更せず、状態固定試験の変更・削除または別途承認されたWork 8測定の前にだけ対象限定で再開する

## 最新のauthority／Evidence

- [測定ブロックtool Evidence（転記排除・dogfooding・fence耐性・手順書改定）](records/development/2026-08-18-measurement-block-evidence-v1.md) — SHA-256 `58a553c9480f59aa72aa816146320908707779b5fd98a946e087d5ccf3f4ade6`
- [検索CLI引数廃止Evidence（既定値・数値最大版解決・手順書縮小・効果）](records/development/2026-08-18-reuse-search-cli-defaults-evidence-v1.md) — SHA-256 `fa5a153121beca9020d1fdbf76e008b1ee287c86348361bb19d30f42797438df`
- [運用集計v2 Evidence（H5束縛照合・承認点欄形式・自己言及の記録・v3繰り越し）](records/development/2026-08-18-operational-metrics-v2-evidence-v1.md) — SHA-256 `34a62366f14d1d9651e1abf361da8898d051156cde0d06c34437ca896fedddde`
- [運用集計dataset v2（束縛268組：一致208・不一致59・欠落1／承認点49・欄形式35）](records/development/2026-08-18-operational-metrics-dataset-v2.json) — SHA-256 `d39fbf1f641ae426a63736856cb99d7c3e02620894aae517c6c7e13ee476c0fd`
- [運用集計Evidence（装置新設・実測の要旨・母数訂正の手戻り記録・v2繰り越し）](records/development/2026-08-18-operational-metrics-evidence-v1.md) — SHA-256 `e7a46f56ee3fcfc573e0947ac1845e5f2a9e916399976800b6c132225fc4d4de`
- [運用集計dataset v1（H4 launch実測30件・H7承認点47件の機械集計）](records/development/2026-08-18-operational-metrics-dataset-v1.json) — SHA-256 `6a85d7d87239bdc17afbad3459c9bdca52d1402cbfc0137039388fb3619cdd25`
- [roots.py指紋pin追加の判断record（状態固定試験の対象限定再開・復帰まで）](records/development/2026-08-18-roots-module-pin-addition-decision-v1.md) — SHA-256 `9765b6d52f317c0b6105ca19eeee1fb9e88e1146bb6a868b7665e40e89286461`
- [配置依存3箇所の解消Evidence（roots.py一元化・RED/GREEN・証明書・作業票と事前走査への入口）](records/development/2026-08-18-placement-root-resolution-evidence-v1.md) — SHA-256 `28f734cfa1579b91e93de75e95af13d8dce91f6a77441b1229051a1badcd19e7`
- [RQ2採点7語彙の形式判断record（案B確定・正本の所在表・v3の合図）](records/development/2026-08-18-rq2-answer-key-vocabulary-format-decision-v1.md) — SHA-256 `63f74966614251c1ad6a268cb021099df783a591e7149bf2b32086cd228825a9`
- [論文執筆計画v2（章立て・データ台帳・投稿先WSSE 2026・二本立て・執筆体制の分担規則）](docs/paper/2026-08-18-paper-outline-and-data-inventory-v2.md) — SHA-256 `c87f4e7bcce5d134dd7f722041df95ace781b5769b25faec99db4c95e86f68de`
- [RQ2 paired trial実行Evidence（§11に裁定後の確定集計を追記）](records/development/2026-08-17-rq2-paired-trial-evidence-v1.md) — SHA-256 `c6dbfa836866524b41edcd156e24b7cd39cec615110a0a9c1c793713a8b5522f`
- [RQ2裁定・議論・副産物v2（論文データ一式の表・7語彙・主題適中率）](records/development/2026-08-18-rq2-adjudication-and-byproducts-v2.md) — SHA-256 `f4191636ea1ee701b3fbc29f42a24e0860afd3c81633a5bb543215777134a152`
- [RQ2生データ（31実行の機械記録）](records/development/2026-08-18-rq2-paired-trial-dataset-v1.json) — SHA-256 `d34ecd24a8d87c49e5b50f4ae204295841622ea12c34886e29dba5a32c85b893`
- [副産物4件の仕分け判断record（委任実施・全4件対処済み）](records/development/2026-08-18-rq2-byproduct-candidates-triage-decision-v1.md) — SHA-256 `86ec0e3a5aa064d4f929970a1e576bffc31c387c02e221a555e733d39280cbcf`
- [評価データ取得計画v1（全順序完了）](docs/development/2026-08-17-evaluation-data-acquisition-plan-v1.md) — SHA-256 `c666bdd7d0b5c44a8fbb876238a19c1d05ee245e693a2b104ceee514cdad55cb`
- [全体見取り図（人向け全景。受入完了時にTODOと同時更新）](docs/current/reviewcompass3-overview-current.md) — SHA-256 `f53b12562a1cc5b8a6d296a7e7e3470e5b130210b2371a1303939f4c9b39500b`
- [デプロイ方針Decision（論点1〜4の裁定・next型起点・訂正版P3）](records/development/2026-08-17-deployment-policy-decision-v1.md) — SHA-256 `ad3bbf84931f55d27c62e5243fede3fbfe2cc4c4d97cc87404ccab969e597671`
- [レビュー基盤module開発の一時終了record（pending残件と再開の入口）](records/development/2026-08-17-review-tooling-module-pause-decision-v1.md) — SHA-256 `9b4d184f378d5dc8dad203caba5daf6b6e58b2471dd387187d5c5ede971cfd6c`
- [文字列理解の失敗類型と対策原則（参照record・事前走査の必読入力）](records/development/2026-08-17-text-interpretation-failure-principles-reference-v1.md) — SHA-256 `ea482a3c7653b0966316012f43cc87ae426cdd5e429348a7f96c4e7f05ecd7b6`
- [現行50要求を解決する要求権限束v2](records/requirements/authority/rc3-requirements-authority-2026-08-03--v2.json) — SHA-256 `760e33ea2ecf6937f56d7bf8d2bd703b18b47dbd2bd6b2bd5919e0dd556d9dae`

## 次に行う一作業

**論文の共通部品（評価の表と図）の作成→WSSE 5頁版の起草**（執筆スレッド。計画v2 §2.3の順序）。数値は確定recordから転記し、転記後に機械照合する。開発スレッド側の選択肢：休止record §3のpending残件（縦C合議等）／運用集計v3（書式C表cell等＝v2 Evidence §6）／デプロイ版（合図＝他アプリ開発の開始決定）。機械化の単位1・2は完了済み。

開始条件：

- （執筆）計画v2が固定済み——満たされている
- （開発）利用者の指示と順序選択がchatで得られる

完了条件：

- （執筆）WSSE 5頁版の初稿が`docs/paper/`へcommitされる

後続作業：計画v2 §2.3（フル版§3〜5→§1・2・7→§8）、休止record §4、デプロイ方針record §4〜5、RQ2裁定record v2 §7を参照。

## blocker・Human判断待ち

- blocker：codexCLIのトークン枯渇は継続（第3 backend候補として疎通回復待ち）。レビュー実行はagy headless正式経路とclaude-subagent（Tier 3・明示受容つき）の2経路が稼働
- Human判断待ち：**WSSEのpreprint方針の確認**（double-blindのためarXiv公開時期に影響。計画v2 §1.2。確認まではWSSE投稿→採否後arXivの安全側で執筆は進められる）

## stale・deferred

- stale：なし
- deferred：外部API直接送信経路の後続はpending（2026-08-16。統合時は判定record規約準拠）。後続候補＝`review_plan`自動変換・縦C合議・codex-cli backend（改善候補仕分け2026-08-17の裁定は各candidate recordを参照）。デプロイ関連：デプロイ版作成は他アプリ開発の開始決定が合図・RC3版nextの返答語彙議論は後日・projection導出の本実装は運用実測後・配置依存3箇所は解消済み・`roots.py`は指紋pin追加済み（対象限定再開の判断record 2026-08-18）。RQ2持ち越し：`read_only_entry`独自語彙の統合は別作業単位（採点7語彙の形式は裁定済み——形式判断record参照。正解表v3はケース集の再利用決定が合図）。契約014持ち越し：残存5件（本文なし前置のみfile）は放置可・新前置種別は`record-run`非対応件数の急変が合図

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：測定ブロック7件（`tests/test_measurement_block.py`）、正式検索12件、運用集計9件、根解決一元化6件、RQ2装置14件、session_logs言及の全59試験file 793件——各単独終了コード0（2026-08-18実測。GREEN固定は機械生成の測定ブロックfileを参照する方式へ移行）
- 直近の全Test：禁止認証隔離条件の正規全試験2,482件成功・終了コード0（2026-08-16・契約013完了時点の実行。以後の作業単位はsession_logs系・評価系の単独緑で受入）
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
