# TODO_NEXT_SESSION

更新日：2026-08-13

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段と第2段、および第3段の前提接続は完了した。第3段では401件を16意味群へ分け、現在保証と履歴固定を区別して群単位で整理している。
- 現在作業：G07の案Aを実施し、現行レビュー手順を安全な版2へ接続した。既存試験一件は試験数を増やさず二つの空条件を個別に検出し、独立完了レビューはverifiedだった。次はG06の共通内容識別値・経路・出力を意味群として再評価する。
- Task Contract：`none（ブートストラップ立て直し中のため未導入）`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 最初の整理単位完了 / G07限定修正verified / G06再評価待ち`、影響：増加した試験を一件単位で処分せず、共有処理の現在保証と過去資料の固定を分離して保守負債を減らす、次：G06の24件、共通処理、その現在利用者、固定値を持つ文書・台帳試験を一群として読み取り、重複と役割を裁定前まで整理する

## 最新のauthority／Evidence

- [採用済み立て直し計画v5](docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md) — SHA-256 `c57336dd2df961e6fe65b8f7c46665db6bce8e0df66111fc90796398a48dd812`
- [現行開発方針](docs/development/2026-08-02-development-policy.md) — SHA-256 `20c4c00a69677af9b4dc51b59b5718889c27fe6cfbbe2adc57cfcc2f601a7a42`
- [G07限定修正 作業票](docs/development/2026-08-13-stage3-g07-declaration-red-contract-correction-bootstrap-work-ticket-v1.md) — SHA-256 `f08d004b8a782cf1da7583f9511bc52f21f516f1feece4fddfba38a9ffee0800`
- [G07限定修正Evidence](records/development/2026-08-13-stage3-g07-declaration-red-contract-correction-evidence-v1.md) — SHA-256 `a0bec84823f86b9d46da05bd792d7499e9417f99d70b4b602b02785f3187fc46`
- [G07限定修正 独立完了レビュー](records/development/2026-08-13-stage3-g07-declaration-red-contract-correction-independent-completion-review-v1.md) — SHA-256 `e88520fb116b826aa8f17013767bff354bb9a70b669ddd3d3d1556e4677ad356`
- [修正後の現行レビュー手順](docs/development/work-review-protocol.md) — SHA-256 `e768d32ed0a2b95fced5a744dd9b98734a2bc3b0c644f415af9dd508c5223d29`
- [処理目録安全問題の後回し判断](.reviewcompass/workflow/triage-decisions-v4/dec-ic-process-inventory-safety-claim-001--v1.json) — SHA-256 `19c730b299cb0eb2d3bd9098427fbc0b138d5cbe8ac1ad80dffd39f87a081f01`

## 次に行う一作業

G06「共通内容識別値・経路・出力」を意味的に完結する一群として読み取り再評価する。401件中の24試験だけでなく、共通処理、現在の取り込み元、実在文書・台帳の固定値、異常入力試験を照合する。コード、試験、設定、正本は変更しない。

開始条件：

- G07案Aの実施Evidenceと独立完了レビューがcommit済みで判定verifiedである
- G06の24 node IDと対応する試験file、共通処理を機械列挙する
- 固定値があることだけで履歴専用とせず、現在の利用者と互換性を先に確認する

完了条件：

- 試験、共通処理、現在利用者、文書・台帳を対象種別ごとに確認する
- 現在保証、履歴・監査資料、両方、役割終了へ意味単位で分類する
- 正常例、異常例、境界例と固有保証または重複を機械で確認する
- 削除・維持・修正の意味判断は実施せず利用者へ返し、新しい試験・検査器・台帳を作らない

後続作業：一回の独立完了レビュー後、意味変更候補がある場合だけ三案比較と利用者判断点を示す。Claude手動確認は追加せず、第3段完了前の一回を残す。

## blocker・Human判断待ち

- blocker：なし。G06は読み取り再評価から開始できる。
- Human判断待ち：G06の再評価後に意味変更候補が生じた場合だけ求める。現時点ではなし。

## stale・deferred

- stale：G07追加8件を削除する案、旧方式だけで赤試験を安全に照合できるという見方、空宣言試験が修正前から二条件を個別保証していたという見方は採用しない。
- deferred：IC-PROCESS-INVENTORY-SAFETY-CLAIM-001（外部送信入口の再利用前にHuman裁定）、G11三試験と専用補助処理、他の未評価意味群、状態固定を宣言fileと共通検査へ置き換える作業、Work 8の全体変異検査。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：G07追加8件、関連29件、手順書導線1件は成功。独立変異二件は同じ既存試験が各一件失敗で個別検出し、試験識別子は9件のまま。
- 直近の全Test：限定二file修正で製品コードと検査処理は不変のため再実行しない。直前の試験整理単位では正規入口から1,737件成功、失敗・エラー・除外0、終了コード0。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
