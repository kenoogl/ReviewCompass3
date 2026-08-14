# TODO_NEXT_SESSION

更新日：2026-08-14

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段と第2段、および第3段の前提接続は完了した。第3段は、現在の設計に適合する実装を古い試験が誤って不合格にしないことの確認へ限定した。
- 現在作業：参照文字列による不完全な候補抽出を停止し、正しい実装例で現役の全試験を実行する方法を現役文書へ反映した。独立完了レビューは未実施である。
- Task Contract：`none（ブートストラップ立て直し中のため未導入）`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 中心問題は維持 / 確認方法を直接実証へ変更`、影響：状態固定試験が正当な変更を妨げた実害は残るが、全試験の詳細確認、参照一覧の全面分類、試験数削減は行わない、次：方針変更の独立完了レビューで、正しい実装例による方法、三種類の分離、六件限定を確認する

## 最新のauthority／Evidence

- [採用済み立て直し計画v5](docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md) — SHA-256 `8c814067511797e445d66779ad144f42ea0b139501ff6002a7d6c46e6706055c`
- [現行開発方針](docs/development/2026-08-02-development-policy.md) — SHA-256 `422d234a0503670e61936edfe98cd13451f4e7af6bfc1506a07824f2904f0fac`
- [重要度別確認メモ](docs/development/2026-08-13-risk-proportional-verification-method-note-v1.md) — SHA-256 `05336194017fed4ad7011a1631dc2f2ff0faec0b404b2060071499c963181594`
- [正しい実装例による方法への修正判断](records/development/2026-08-14-stage3-correct-behavior-witness-method-amendment-decision-v1.md) — SHA-256 `76aa813046a07176650e0bc5db5d5308f569a8e51011f15cd2c21341852e0d2f`
- [方針修正作業票v2](docs/development/2026-08-14-stage3-correct-behavior-witness-method-amendment-bootstrap-work-ticket-v2.md) — SHA-256 `22220624e145877712e064911bf99ffa893b816b318d8e803842c0b822bd982a`
- [作業票v2の変更点確認](records/development/2026-08-14-stage3-correct-behavior-witness-method-amendment-scope-one-time-review-v1.md) — SHA-256 `f1352e6c39684e68f1ecd2191c019286205ae21c85571ff11de4532675cbc6c1`
- [不完全な候補抽出の独立完了レビュー](records/development/2026-08-14-stage3-test-authority-contradiction-candidate-extraction-independent-completion-review-v1.md) — SHA-256 `66779dae0326304f297c58b0465215d83cb7d07bee9d6914379b06802183405d`

## 次に行う一作業

方針変更の六件だけを対象に独立完了レビューを行い、現役文書の意味、参照値、変更範囲、旧17件の使用停止を確認する。コード、試験、設定は変更しない。

開始条件：

- 作業票v2の一回限り変更点確認が開始可である
- 立て直し計画、開発方針、確認メモ、チェックリスト、Decision、TODOの六件だけが変更対象である
- 各文書の変更後SHA-256と参照値が実fileから再計算できる

完了条件：

- 第3段が正しい実装の誤拒否確認だけに限定され、残る三種類が別作業へ分離されている
- 参照文字列抽出、495参照、不完全な17件を現役の候補または完了根拠にしていない
- 独立完了レビューがverifiedで、現役参照とTODO共通検証が合格している

後続作業：正しい実装例を作る対象となる、現在設計の変更・廃止・緩和点を限定する次の軽量作業票を作成する。

## blocker・Human判断待ち

- blocker：なし。方針変更の独立完了レビュー前であり、正しい実装例の選定と一時実装にはまだ進まない。
- Human判断待ち：なし。第3段を正しい実装の誤拒否確認だけに限定する判断は利用者が承認済みである。

## stale・deferred

- stale：参照文字列を逆引きして17件へ絞ったEvidenceはreported_unverifiedであり、作業票v1・v2とともに現役手順へ使用しない。
- deferred：誤った実装の受理、守れない保証の表示、安全方針に反する副作用の見逃しは、必要時のWork 8または通常開発へ分離する。ISSUE-AUTHORITY-REFERENCE-DIGEST-CHECK-001はregistered、issue_resolution_v4.pyは暫定・使用停止のまま維持する。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：文書だけの変更のため、差分、再読込み、参照解決、内容識別値を確認する。全試験と変異検査は実行しない。
- 直近の全Test：直近の正規全試験は1,728件成功である。本方針変更ではコード、試験、設定を変更していないため再実行しない。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
