# TODO_NEXT_SESSION

更新日：2026-08-14

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段と第2段、および第3段の前提接続は完了した。第3段の正しい実装に対する誤拒否確認はverifiedで閉じ、段完了前に残る成果物ライフサイクル整理へ戻る。
- 現在作業：承認済みの現在設計から二つの確認点を固定し、観測commitの全1,728試験が正しい現在状態を拒否しないことを独立再実行まで含めて確認した。次は第3段開始以後に追加・変更したコードと文書の整理範囲を固定する。
- Task Contract：`none（ブートストラップ立て直し中のため未導入）`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 誤拒否確認verified・成果物整理継続`、影響：既知の正しい現在状態を全試験が拒否しないことは確認済みだが、第3段中に追加・変更したコードと文書の段完了前整理が未完了である、次：第3段開始commitと成果物列挙の対象・除外・分類方法を軽量作業票へ固定する

## 最新のauthority／Evidence

- [採用済み立て直し計画v5](docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md) — SHA-256 `8c814067511797e445d66779ad144f42ea0b139501ff6002a7d6c46e6706055c`
- [現行開発方針](docs/development/2026-08-02-development-policy.md) — SHA-256 `422d234a0503670e61936edfe98cd13451f4e7af6bfc1506a07824f2904f0fac`
- [第3段成果物整理の追補判断](records/development/2026-08-14-recovery-plan-v5-stage3-created-artifact-completion-condition-amendment-decision-v1.md) — SHA-256 `181c74b9b325df9544ce195e3344aee60d0090cce61ab4f136f5d8c1f9da00db`
- [正しい実装例による方法への修正判断](records/development/2026-08-14-stage3-correct-behavior-witness-method-amendment-decision-v1.md) — SHA-256 `76aa813046a07176650e0bc5db5d5308f569a8e51011f15cd2c21341852e0d2f`
- [既知の正しい現在状態による実施Evidence](records/development/2026-08-14-stage3-known-correct-state-witness-execution-evidence-v1.md) — SHA-256 `5d65e67b6239f9f267eaac8fce749b28267e81618ca7ea01c26614eb2ac0ebc4`
- [既知の正しい現在状態による独立完了レビュー](records/development/2026-08-14-stage3-known-correct-state-witness-independent-completion-review-v1.md) — SHA-256 `623095ce50005400977749fa323e6bea00213db46b9487651ea42e01337afd97`

## 次に行う一作業

第3段開始時点から段完了候補までに追加・変更したコードと文書をGit差分から機械列挙するため、第3段開始commit、観測commit、対象種別、除外範囲、意味群、四分類、確認の深さを軽量作業票へ固定する。まだ成果物の削除、統合、使用停止、コード・試験・設定の変更は行わない。

開始条件：

- 誤拒否確認の実施Evidenceと独立完了レビューがverifiedとして固定されている
- 立て直し計画v5と第3段成果物整理の追補判断の内容識別値が実fileと一致する
- 第3段開始commitを件数や日付から推測せず、既存Decision、Evidence、Git履歴から確定する

完了条件：

- 第3段開始commit、観測commit、対象種別、除外範囲、列挙方法、意味群、四分類、停止条件を作業票へ固定する
- コードと文書で確認方法を分け、重要度に応じて深さを変え、全成果物へ一律の詳細確認を課さない
- 新しい台帳、検査器、試験、関門を追加せず、コード、試験、設定、Issueを変更しない
- 作業担当とは異なる新規サブエージェントの独立開始前レビューを行う

後続作業：開始可の確認後、Git差分から対象成果物を機械列挙し、意味群ごとの利用先・守る性質・重複・再利用・四分類を確認する。

## blocker・Human判断待ち

- blocker：なし。誤拒否確認はverifiedで閉じており、第3段成果物整理の範囲固定へ進める。
- Human判断待ち：なし。次のHuman判断は、列挙・分類結果から役割終了や整理候補が実証された場合、または第3段完了候補を提示する時点で行う。

## stale・deferred

- stale：参照文字列を逆引きした17件候補と495参照は現役入力にしない。全試験の詳細確認、試験数削減、実行時間短縮を第3段完了条件とする見方も失効している。
- deferred：誤った実装の受理、守れない保証の表示、安全方針に反する副作用の見逃しは必要時のWork 8または通常開発へ分離する。ISSUE-AUTHORITY-REFERENCE-DIGEST-CHECK-001はregistered、issue_resolution_v4.pyは暫定・使用停止のまま維持する。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：既知の正しい現在状態で正規収集1,728件・重複0・一覧SHA一致を確認し、構造化記録の二つの現在状態を再計算した。独立完了レビューはverified、止める指摘0件、報告不一致0件である。
- 直近の全Test：観測commitの履歴付き一時複製で正規全試験1,728件成功、失敗・error・skip 0、終了コード0。独立レビューも同じ状態識別値で1,728件成功を再現した。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
