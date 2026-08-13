# TODO_NEXT_SESSION

更新日：2026-08-13

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段と第2段、および第3段の前提である対象分類・工程分離の機械接続は完了した。第3段は未開始である。
- 現在作業：対象分類・工程分離の機械接続は、限定修正後にCodexと利用者が手動で受け渡したClaudeの完了レビューがともにverifiedとなった。次は試験を変更せず、1,338件時点から現在までに増えた候補を機械列挙する。
- Task Contract：`none（ブートストラップ立て直し中のため未導入）`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 現在有効性を再判定済み / 第3段の列挙待ち`、影響：状態固定と試験増加の中心問題は現存する。件数だけで削除せず、現在の401件の差分候補を履歴と試験識別子から先に固定する必要がある、次：1,338件時点の固定commitと現在状態を機械照合し、当初398件と今回追加した3件を区別して401件の差分候補を列挙する

## 最新のauthority／Evidence

- [採用済み立て直し計画v5](docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md) — SHA-256 `c57336dd2df961e6fe65b8f7c46665db6bce8e0df66111fc90796398a48dd812`
- [試験増加・状態固定Issue現在有効性の再判定v1](records/development/2026-08-13-test-growth-state-pinning-current-validity-decision-v1.md) — SHA-256 `1609dfdd76b25c86b38bd105f4199cbbc1636614c5f68256fdee61879c3bddac`
- [対象分類・工程分離の機械接続完了判断v1](records/development/2026-08-13-review-target-process-connection-completion-decision-v1.md) — SHA-256 `26de9fb10c4f5d6b30918496d8bed892f84ad7378196719091b1a4e45b23b096`
- [Claude最終完了レビュー結果v1](records/session-handoffs/2026-08-13-claude-review-target-process-connection-completion-review-result-v1.md) — SHA-256 `c818877875017d9214e0f9b2af0f8046a4539c0430de6d1d1edb241a82c3fd49`
- [現行開発方針](docs/development/2026-08-02-development-policy.md) — SHA-256 `df0fb4e5e960cbbb0b8c5c671c2596292638f26e20b3d81f3f6ae95ec7a3f703`

## 次に行う一作業

第3段の最初の文書・読み取り調査として、公式全試験が1,338件だった固定状態と現在の1,739件を機械比較し、増加した401件の試験候補をGit履歴と試験識別子で列挙する。内容分類、削除、統合、実装はまだ行わない。

開始条件：

- 対象分類・工程分離の機械接続完了判断と二つの独立完了レビューが固定済みで、作業ツリーがcleanである
- 1,338件の根拠となる受領証と観測commitを既存Evidenceから先に確定し、件数からcommitを推測しない
- 文書・読み取り調査として扱い、コード、試験、設定、台帳を変更しない

完了条件：

- 基準commit、現在commit、両試験集合の取得方法、件数、識別値を再現可能な形で固定する
- 現在の差401件を機械集計し、当初398件と今回の対象分類・工程分離作業で追加した3件を区別する
- 名称変更、移動、パラメータ展開による見かけの増減を未確認のまま新規試験と断定せず、照合不能を明示する
- 試験を変更せず、列挙結果だけを独立した読み取り確認へ渡す

後続作業：列挙結果から最初の小さな低危険度の分類単位を一つだけ選び、利用者判断へ渡す。

## blocker・Human判断待ち

- blocker：なし。401件は整理対象の現在候補数であり、品質指標や削除数として使わない。
- Human判断待ち：列挙後に、最初に内容分類する小さな一単位を選ぶ。列挙開始前の追加判断はない。

## stale・deferred

- stale：対象分類・工程分離の機械接続が未完了という状態は解消した。現在対象を398件とする表示は、今回追加した3件を含まない過去時点の値であり、現在値としては失効した。
- deferred：401件の内容分類と試験削減、状態固定を宣言fileと共通検査へ置き換える作業、Work 8の全体的な変異検査、外部実装経路の再開と保証範囲再裁定、重大な欠陥12件のうち選択入口が依存しないもの。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：対象試験と既存方針試験は34件成功、終了コード0。五つの欠陥投入はすべて対象試験が終了コード1で検出。Codexと利用者が手動で受け渡したClaudeの最終レビューはともにverified、止める指摘0件、報告不一致0件。
- 直近の全Test：限定修正後の公式入口で1,739件成功、失敗・エラー・除外0、Python 3.13.14、代替実行なし、終了コード0。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
