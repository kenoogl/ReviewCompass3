# TODO_NEXT_SESSION

更新日：2026-08-13

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段と第2段、および第3段の前提接続は完了した。第3段は401件の候補列挙まで完了し、内容分類は未開始である。
- 現在作業：1,338件から現在までの正味増加401件を固定し、Codexと利用者が手動で受け渡したClaudeの独立レビューがともにverifiedとなった。次は最初に調べる小さな一単位を一つだけ選ぶ。
- Task Contract：`none（ブートストラップ立て直し中のため未導入）`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 現在有効性を再判定済み / 401件列挙完了 / 整理単位選定待ち`、影響：状態固定と試験増加の中心問題は現存するが、401件は未分類の母集団であり削除数ではない、次：31のtest file群から、履歴と現在の保証を確認して最初の小さな低危険度候補を一つだけ提示する

## 最新のauthority／Evidence

- [採用済み立て直し計画v5](docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md) — SHA-256 `c57336dd2df961e6fe65b8f7c46665db6bce8e0df66111fc90796398a48dd812`
- [試験増加・状態固定Issue現在有効性の再判定v1](records/development/2026-08-13-test-growth-state-pinning-current-validity-decision-v1.md) — SHA-256 `1609dfdd76b25c86b38bd105f4199cbbc1636614c5f68256fdee61879c3bddac`
- [試験増加候補の機械列挙Evidence v1](records/development/2026-08-13-test-growth-nodeid-enumeration-evidence-v1.md) — SHA-256 `dfa2ebb73a940daa527d3ceac8c502876bf13152bff940a24308411ab2a64f3f`
- [Codex独立完了レビューv1](records/development/2026-08-13-test-growth-nodeid-enumeration-completion-review-v1.md) — SHA-256 `a4300dfe938fc6b98bca6fe34441d566bee928a088d504bb01e7188315753d6c`
- [Claude独立完了レビュー結果v1](records/session-handoffs/2026-08-13-claude-test-growth-nodeid-enumeration-review-result-v1.md) — SHA-256 `b23527d925e9dcc4d0d14120c6bb6df5c99c2dec33a29eef67436874272f9392`
- [試験増加候補列挙の完了判断v1](records/development/2026-08-13-test-growth-nodeid-enumeration-completion-decision-v1.md) — SHA-256 `18dab950d7d35720f9a0d36ae9c4cb50019b31dc2b31a9f9cb122bb042d3a92f`
- [現行開発方針](docs/development/2026-08-02-development-policy.md) — SHA-256 `df0fb4e5e960cbbb0b8c5c671c2596292638f26e20b3d81f3f6ae95ec7a3f703`

## 次に行う一作業

第3段の読み取り調査として、401件を一括分類せず、31のtest file群から最初に扱う小さな一単位を一つだけ選び、利用者判断へ提示する。試験は変更しない。

開始条件：

- 401件の個別一覧、完了判断、CodexとClaudeの独立レビューが固定済みで、作業ツリーがcleanである
- 候補数や名前だけで必要性を推測せず、追加commit、現在要求または実害、参照先、共有境界を実測する
- 外部送信、機密情報、承認、不可逆操作、守り役コードに関係する群を低危険度とみなさない

完了条件：

- 一つの候補単位について、含む試験識別子、追加理由の履歴、現在守る保証、参照先、後継保証の有無を示す
- 低危険度とする根拠、または低危険度候補を選べなかった理由を、反証一件とともに示す
- 削除・統合・使用停止を実施せず、候補単位と危険度案だけを利用者判断へ渡す

後続作業：利用者が選定候補と危険度を判断した後、その一単位だけの軽量作業票と開始確認へ進む。

## blocker・Human判断待ち

- blocker：なし。401件全体を先に分類する必要はない。
- Human判断待ち：候補提示後に、その一単位を最初の整理対象とするか、提示した危険度で進めるかを判断する。

## stale・deferred

- stale：第3段の列挙が未完了という状態と、現在候補を398件とする表示は失効した。
- deferred：401件の残りの内容分類と試験削減、状態固定を宣言fileと共通検査へ置き換える作業、Work 8の全体的な変異検査、外部実装経路の再開と保証範囲再裁定。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：三commitの独立収集は1,338件、1,736件、1,739件で各重複0件。二つの独立レビューはverified、止める指摘0件、報告不一致0件。
- 直近の全Test：直近の公式入口は1,739件成功、失敗・エラー・除外0、Python 3.13.14、代替実行なし、終了コード0。本読み取り調査では再実行していない。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
