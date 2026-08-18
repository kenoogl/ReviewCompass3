# TODO_NEXT_SESSION

更新日：2026-08-18

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5第1〜5段・正式ツール化（契約008〜014）・デプロイ方針決定・評価データ取得（RQ1装置・RQ2 paired trial＝実起動30回・裁定確定・論文データ一式）・RQ2副産物4件の対処・論文執筆開始（WSSE 2026 Special Session・締切**2026-08-30**・LaTeX 5頁・double-blind＋arXivフルの二本立て）までは前回どおり。今回、RQ2持ち越しの**採点7語彙の正式反映を裁定**（案B＝集計側を正本・正解表v3はケース集の再利用決定が合図）、**配置依存3箇所の解消**（デプロイ方針4b-1。`tools/common/roots.py`へ一元化・指紋pin追加済み）、**順序5の運用集計コマンド**（dataset v1固定）を完了——**評価データ取得計画v1の全順序が完了**。続けて**運用集計v2**（H5束縛照合＝一致77.6%・dataset v2固定）、**検索CLIの引数廃止**（保存先・方針版・時刻を自動解決）、**測定ブロックの機械生成tool**（宣言JSON→機械実行→生成file参照。実測の転記を構造的に排除・手順書規律も「転記は例外」へ改定）も完了——方針転換はHuman指示「手作業部分を極力廃してLLMは本来の役割のみ」。加えて**運用規範5件を私的メモリからrepoへ移設**（AGENTS §2・§3＋request-builder手順書）、**LLM／機械分担の精査**（手順書8件・record固定）と**対策1＝既定値化の横展開**、**対策2＝計画JSON writer**（finalize＝検索と同一検証・手書きdigest工程の消滅・committed全22計画のverify一括合格）、**対策3＝review-planのHEAD既定**（64桁SHA手書きの消滅・base-commitは意味情報として残置）を完了——**精査の対策1〜3すべて完了**。締めに**運用集計v3**（書式C＝表cell束縛の照合。採点対象268→1,193組・dataset v3固定・v4＝H4手動記入等は繰り越し）も完了。測定ブロックは観測→根因調査→**二重実行guard＋実行体・環境記録**で強化済み（読み取り専用限定・揺れる出力は宣言側で決定的射影に）。続けて**運用集計v4**（git履歴照合＝不一致313の95.2%が版の前進・真の不一致13件・追跡可能95.9%）、**v5**（H4自動導出率93.9%・保全規模＝8日間で約3.5GB）、**v6**（コスト時系列第一次＝厳密tool_use 28,210回・欠落34の由来確定＝削除8＋履歴なし23＋絶対3）を完了し、**論文データ台帳の追補v1**（計画v2以降の固定Evidence 10件＋従軸実測の要旨表）を`docs/paper/`へ固定。今回、**運用集計v7**（系統意味づけ＝3系統照合一致・道具呼び出しの構造計数＝Codex空白解消・活動時間600秒窓＝経過幅の脆さも実証）を完了、dataset v7固定・台帳追補v2で執筆用に通知（受入・§4確定は2026-08-19裁定record）。続けて**read_only_entry終了コード統合**（部分系3入口の語彙を0／4／5へ同値化・cli.pyとの値一致pin試験・消費側無変更の機械証明）を完了。全景は`docs/current/reviewcompass3-overview-current.md`
- 現在作業：**論文執筆（WSSE短縮版が締切物）**。執筆体制＝**本スレッドが執筆（`docs/paper/`配下のみ書く）・別スレッドが継続開発（TODO・見取り図・records・製品コードの正本管理）**。論文データの更新は開発スレッドが装置で再集計し新版として固定、執筆側は固定版のみ引用（計画v2 §3の分担規則）
- Task Contract：`なし（契約014受入完了・注記追記済み。次契約は未定義）`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了・条件付き再開待ち`、影響：次縦切りの選択・着手を妨げない持ち越し負債である、次：Issue状態を変更せず、状態固定試験の変更・削除または別途承認されたWork 8測定の前にだけ対象限定で再開する

## 最新のauthority／Evidence

（規準：次の一作業の固定入力と判断待ちのauthorityに限る。完了単位の記録は見取り図とgit履歴が正本——todo-handoff-update.md手順4）

- [論文データ台帳 追補v2（従軸の新版通知＝dataset v7の執筆用固定・v6からの更新注意）](docs/paper/2026-08-18-paper-data-inventory-addendum-v2.md) — SHA-256 `9d910599e7aac153c058bc50fd98828b1dc8d34d49f1954c5483e1aae291a711`
- [論文データ台帳 追補v1（計画v2以降の固定Evidence＝従軸の実測値と引用先digest表）](docs/paper/2026-08-18-paper-data-inventory-addendum-v1.md) — SHA-256 `70d369a0b59d58478b012618bf885cf85ab75845db31ece7aa407486ed35ec12`
- [論文執筆計画v2（章立て・データ台帳・投稿先WSSE 2026・二本立て・執筆体制の分担規則）](docs/paper/2026-08-18-paper-outline-and-data-inventory-v2.md) — SHA-256 `c87f4e7bcce5d134dd7f722041df95ace781b5769b25faec99db4c95e86f68de`
- [RQ2 paired trial実行Evidence（§11に裁定後の確定集計を追記）](records/development/2026-08-17-rq2-paired-trial-evidence-v1.md) — SHA-256 `c6dbfa836866524b41edcd156e24b7cd39cec615110a0a9c1c793713a8b5522f`
- [RQ2裁定・議論・副産物v2（論文データ一式の表・7語彙・主題適中率）](records/development/2026-08-18-rq2-adjudication-and-byproducts-v2.md) — SHA-256 `f4191636ea1ee701b3fbc29f42a24e0860afd3c81633a5bb543215777134a152`
- [RQ2生データ（31実行の機械記録）](records/development/2026-08-18-rq2-paired-trial-dataset-v1.json) — SHA-256 `d34ecd24a8d87c49e5b50f4ae204295841622ea12c34886e29dba5a32c85b893`
- [運用集計dataset v7（従軸の最新固定版：系統意味づけ・正規化道具計数・活動時間600秒窓とbucket分布）](records/development/2026-08-18-operational-metrics-dataset-v7.json) — SHA-256 `7702463b46678ab52cf15b3f077fc590f51a2707fab5ab64bf6356ff5c3843c2`
- [全体見取り図（人向け全景。受入完了時にTODOと同時更新）](docs/current/reviewcompass3-overview-current.md) — SHA-256 `6bbec45d7ed3e98f6f68a8ebb2c2762bb81ac8aafbb4bc713fe8c03fdd6d8c89`

## 次に行う一作業

**論文の共通部品（評価の表と図）の作成→WSSE 5頁版の起草**（執筆スレッド。計画v2 §2.3の順序）。数値は確定recordから転記し、転記後に機械照合する。開発スレッド側の選択肢：休止record §3のpending残件（縦C合議等）／運用集計v8（日別展開等＝v7 Evidence §4・候補）／デプロイ版（合図待ち）。

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
- deferred：外部API直接送信経路の後続はpending（2026-08-16。統合時は判定record規約準拠）。後続候補＝`review_plan`自動変換・縦C合議・codex-cli backend（改善候補仕分け2026-08-17の裁定は各candidate recordを参照）。デプロイ関連：デプロイ版作成は他アプリ開発の開始決定が合図（その作業単位に**AGENTS一般規範の持ち出し仕分け**＝配布物側文書への抽出・論点4aの型を含める）・RC3版nextの返答語彙議論は後日・projection導出の本実装は運用実測後・配置依存3箇所は解消済み・`roots.py`は指紋pin追加済み（対象限定再開の判断record 2026-08-18）。RQ2持ち越し：正解表v3はケース集の再利用決定が合図（採点7語彙の形式は裁定済み——形式判断record参照）。safe_storage_entry終了コード語彙は`IC-SAFE-STORAGE-ENTRY-EXIT-CODE-VOCABULARY-001`登録済み・Human仕分け待ち。契約014持ち越し：残存5件（本文なし前置のみfile）は放置可・新前置種別は`record-run`非対応件数の急変が合図

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：review-plan 11件（`tests/test_review_plan.py`）、計画writer6件、測定ブロック10件、正式検索12件、運用集計25件、根解決一元化6件、RQ2装置14件、session系（log・artifact・redaction・bootstrap）53試験file 348件——各単独終了コード0（2026-08-18〜19実測。GREEN固定は機械生成の測定ブロックfileを参照する方式へ移行）
- 直近の全Test：禁止認証隔離条件の正規全試験2,482件成功・終了コード0（2026-08-16・契約013完了時点の実行。以後の作業単位はsession_logs系・評価系の単独緑で受入）
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
