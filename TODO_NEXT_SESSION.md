# TODO_NEXT_SESSION

更新日：2026-08-20

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5第1〜5段・正式ツール化（契約008〜015）・デプロイ方針決定・評価データ取得（RQ1装置・RQ2 paired trial・論文データ一式・従軸＝運用集計v1〜v7）・測定ブロックと計画／台帳laneの機械化・issue突合まで完了（**詳細は見取り図とgit履歴が正本**。従軸の執筆用固定は台帳追補v1／v2）。論文執筆が進行中：**WSSE 2026 Special Session（締切2026-08-30・LaTeX 5頁・double-blind）＋arXivフルの二本立て**。全景は`docs/current/reviewcompass3-overview-current.md`
- 現在作業：執筆スレッド＝**論文執筆（WSSE短縮版が締切物）**。英語初稿v1＋文献15件BibTeX＋図1 TikZ源＋§5関連研究3本追補まで固定済み（2026-08-20。表現・非主張等の確定事項は草稿v3付記・v4が正本）。**残作業＝WSSE様式LaTeXへの組版と数値の機械照合**。開発スレッド＝**契約015（codex-cli第3 backend＋登録簿深化）は製品受入完了**（2026-08-20。3 backend体制成立・次の開発作業は順序選択待ち）。執筆体制＝執筆スレッドは`docs/paper/`のみ書く・開発スレッドが正本管理（計画v2 §3の分担規則）
- Task Contract：`なし（契約015受入完了＝2026-08-20の製品受入record。次契約は未定義）`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了・条件付き再開待ち`、影響：次縦切りの選択・着手を妨げない持ち越し負債である、次：Issue状態を変更せず、状態固定試験の変更・削除または別途承認されたWork 8測定の前にだけ対象限定で再開する

## 最新のauthority／Evidence

- [WSSE英語初稿v1（組版の原本。文献15件BibTeX・§5関連研究3本追補済み）](docs/paper/2026-08-19-wsse-draft-en-v1.md) — SHA-256 `1fbda9f8d276e07763c6646e2f9191f9ea50d15d419d216615dd652f2a9f186a`
- [WSSE日本語草稿v4（照合用の和文原本・考察節明確化）](docs/paper/2026-08-19-wsse-draft-ja-v4.md) — SHA-256 `962f0aa5c1e2a3e8a383af9c9e1e48fc15fc621fb004377574b3fec0087be76b`
- [図1 TikZ源（契約→実行の流れ）](docs/paper/figures/figure1-contract-flow.tex) — SHA-256 `7ef46ba5370fb8369a54347b76f1791b76d76d840da3e0cce080acb016cc20f8`
- [WSSE英文骨子v2（6節構成・Related Work・頁配分・引用当て込み）](docs/paper/2026-08-19-wsse-skeleton-v2.md) — SHA-256 `63038d2215a900ec1c5b22848088ed69c6932a958a3836410b65a3f1eec0206c`
- [論文データ台帳 追補v2（従軸の新版通知＝dataset v7の執筆用固定・v6からの更新注意）](docs/paper/2026-08-18-paper-data-inventory-addendum-v2.md) — SHA-256 `9d910599e7aac153c058bc50fd98828b1dc8d34d49f1954c5483e1aae291a711`
- [論文データ台帳 追補v1（計画v2以降の固定Evidence＝従軸の実測値と引用先digest表）](docs/paper/2026-08-18-paper-data-inventory-addendum-v1.md) — SHA-256 `70d369a0b59d58478b012618bf885cf85ab75845db31ece7aa407486ed35ec12`
- [論文執筆計画v2（章立て・データ台帳・投稿先WSSE 2026・二本立て・執筆体制の分担規則）](docs/paper/2026-08-18-paper-outline-and-data-inventory-v2.md) — SHA-256 `c87f4e7bcce5d134dd7f722041df95ace781b5769b25faec99db4c95e86f68de`
- [RQ2 paired trial実行Evidence（§11に裁定後の確定集計を追記）](records/development/2026-08-17-rq2-paired-trial-evidence-v1.md) — SHA-256 `c6dbfa836866524b41edcd156e24b7cd39cec615110a0a9c1c793713a8b5522f`
- [RQ2裁定・議論・副産物v2（論文データ一式の表・7語彙・主題適中率）](records/development/2026-08-18-rq2-adjudication-and-byproducts-v2.md) — SHA-256 `f4191636ea1ee701b3fbc29f42a24e0860afd3c81633a5bb543215777134a152`
- [RQ2生データ（31実行の機械記録）](records/development/2026-08-18-rq2-paired-trial-dataset-v1.json) — SHA-256 `d34ecd24a8d87c49e5b50f4ae204295841622ea12c34886e29dba5a32c85b893`
- [運用集計dataset v7（従軸の最新固定版：系統意味づけ・正規化道具計数・活動時間600秒窓とbucket分布）](records/development/2026-08-18-operational-metrics-dataset-v7.json) — SHA-256 `7702463b46678ab52cf15b3f077fc590f51a2707fab5ab64bf6356ff5c3843c2`
- [全体見取り図（人向け全景。受入完了時にTODOと同時更新）](docs/current/reviewcompass3-overview-current.md) — SHA-256 `ea35643595c22a36876508cb9bbfe054c52ae479634cbce1000c4733a4439d96`

## 次に行う一作業

**執筆＝英語初稿の組版**（WSSE様式LaTeXへの流し込み・図1 TikZ組み込み・文献整形・転記数値の確定recordとの機械照合）。**開発＝順序選択待ち**（候補：縦C合議＝3判定役の材料が揃った／`IC-REQUEST-BUILDER-MODEL-CHECK-SCOPE-001`の独立小作業単位／RQ2追試／運用集計v8）。

開始条件：

- （執筆）英語初稿v1（§5追補済み）・図1 TikZ源が固定済み——満たされている
- （開発）利用者の指示と順序選択がchatで得られる

完了条件：

- （執筆）WSSE様式（LaTeX）で組版・数値照合済みの5頁版一式が`docs/paper/`へcommitされる

後続作業：計画v2 §2.3（フル版§3〜5→§1・2・7→§8）、休止record §4、デプロイ方針record §4〜5、RQ2裁定record v2 §7を参照。

## blocker・Human判断待ち

- blocker：なし（レビュー実行は3 backend体制が稼働＝agy（Tier 1既定）・claude-subagent（Tier 3明示受容）・codex-cli（Tier 1）。契約015受入2026-08-20）
- Human判断待ち：**WSSEのpreprint方針の確認**（double-blindのためarXiv公開時期に影響。計画v2 §1.2。確認まではWSSE投稿→採否後arXivの安全側で執筆は進められる）

## stale・deferred

- stale：なし
- deferred：外部API直接送信経路の後続はpending（2026-08-16。統合時は判定record規約準拠）。後続候補＝`review_plan`自動変換・縦C合議（3判定役の材料あり）・codex再レビュー（任意＝受入record §4）（codex-cli backendは契約015として受入完了2026-08-20。`IC-REQUEST-BUILDER-MODEL-CHECK-SCOPE-001`は(b)裁定＝独立小作業単位・合図＝利用者指示）。デプロイ関連：**残開発の棚卸し＝`docs/design/2026-08-19-deployment-readiness-checklist-v1.md`**（2026-08-19固定）。デプロイ版作成は他アプリ開発の開始決定が合図（その作業単位に**AGENTS一般規範の持ち出し仕分け**＝配布物側文書への抽出・論点4aの型と、**コード管理機構の調査・実装検討**＝lifecycle棚卸し（暫定100・正式1・未宣言73＝2026-08-19実測）→配布／昇格／開発専用の3区分の判断・deploy-manifest制定の前提材料、と**issue経路の持ち出し仕分け**＝アプリ側lane設置の4項目（lane設定の配布・区画初期化・Decision record置き場・実態調書の拘束flagのnext型対応。可搬性は`--project-root`と一括検証で確保済み＝2026-08-19実測）と**RC3バグ還流の2経路設計**（報告のみ／試行つき・受付窓口等3判断＝`docs/design/2026-08-19-deployed-feedback-two-route-design-memo-v1.md`）、を含める）・RC3版nextの返答語彙議論は後日・projection導出の本実装は運用実測後・配置依存3箇所は解消済み・`roots.py`は指紋pin追加済み（対象限定再開の判断record 2026-08-18）。RQ2持ち越し：正解表v3はケース集の再利用決定が合図（採点7語彙の形式は裁定済み——形式判断record参照）。safe_storage_entry終了コード語彙は`IC-SAFE-STORAGE-ENTRY-EXIT-CODE-VOCABULARY-001`＝checkpoint採用（合図＝WSSE初稿完了後の開発枠。仕分けrecord 2026-08-19）。台帳lane writer機械化は`IC-LEDGER-LANE-WRITER-MECHANIZATION-001`＝**scope全消化・AGENTS反映済み**（verdict schema新設＝案Bは需要実測時の別候補）。issue維持5件の後続は各合図・条件に従う（突合裁定record 2026-08-19 §4）。実態調書の治癒確認probe拡張は将来候補（`IC-ISSUE-RECONCILIATION-DOSSIER-001`＝scope消化済み）。アーキテクチャ整合検査（機械層）`IC-ARCHITECTURE-CONFORMANCE-CHECK-001`と横串レビュー（意味層）`IC-CROSS-CUT-REVIEW-001`＝checkpoint採用・**同枠**（合図＝WSSE初稿後・コード管理調査と同枠。宣言を共有正本として束ねる。設計memo v2＝3案比較・要件schema素案・検査タイミング・実装順序つき）。契約014持ち越し：残存5件（本文なし前置のみfile）は放置可・新前置種別は`record-run`非対応件数の急変が合図。**RQ2追試＝主題にかなり近い周辺文書**（同じ契約の旧版・同じ部分系の別文書）での再実験は開発スレッドの将来作業（裁定2026-08-19「厳しいケースは後ほどテスト」。WSSE論文では限界として記載済み＝草稿v3 §6）

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：契約015受入時＝reviewer-launch 94件・契約011対象42件・G30契約操作75件・RQ2装置14件——各単独終了コード0（2026-08-20実測。正本はGREEN測定v2＝合否は単独実行の終了コード）
- 直近の全Test：禁止認証隔離条件の正規全試験2,645件成功・終了コード0（2026-08-20・契約015受入時のreceipt）
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
