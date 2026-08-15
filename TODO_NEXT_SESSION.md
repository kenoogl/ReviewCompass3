# TODO_NEXT_SESSION

更新日：2026-08-15

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段から第5段と、最初の製品機能G25読取り専用入口は完了した。現在は立て直し後の二つ目の製品機能である安全保存の実装準備を進めている。
- 現在作業：安全保存契約の22受入条件を、利用者から見える状態変化と一つの主要な失敗理由を持つ八つの製品TDD境界へ分け、変更範囲、試験順、停止条件、戻せる地点を実装作業票へ固定した。次は、作業担当と異なる新規実行単位による独立開始前確認である。
- Task Contract：`TC-RC3-PRODUCT-SESSION-ARTIFACT-SAFE-STORAGE-002 / version_3_adopted_implementation_start_approved_reuse_adjudicated_tdd_boundary_prechecked_start_review_pending`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了・条件付き再開待ち`、影響：安全保存の実装境界確認を妨げず、立て直し計画を未完了へ戻さない持ち越し負債である、次：Issue状態を変更せず、状態固定試験の変更・削除または別途承認されたWork 8測定の前にだけ対象限定で再開する

## 最新のauthority／Evidence

- [採用済みの安全保存Task Contract v3](records/task-contract/2026-08-15-session-artifact-safe-storage-candidate-v3.md) — SHA-256 `38de71b1d8910f7cf05ae76a8f881235400d7522f81314f844d8cf1e0e52cfac`
- [案Cの実装開始判断](records/development/2026-08-15-session-artifact-safe-storage-option-c-implementation-start-decision-v1.md) — SHA-256 `f8c55611de59cd25946aa27bb4330ca66bbf1cf751baba6c5fe5c19a3ec1d45f`
- [現行開発方針](docs/development/2026-08-02-development-policy.md) — SHA-256 `e3e6b0d2c7a1265f7cde2c2e00cc888f43d63ce0d1945c300b2b2e5f7730b559`
- [立て直し完了後の現在位置訂正判断](records/development/2026-08-15-post-recovery-product-development-position-correction-decision-v1.md) — SHA-256 `5c753f8a155b018452d86ce29d5f37f4ef164e046feac3089f9936295436ef6a`
- [八つの働き正式検索Evidence](records/development/2026-08-15-safe-storage-capability-search-formal-execution-evidence-v1.md) — SHA-256 `d433fcdae6fea26f2fb8f3de703f54db9d7b2905dd4cbd6f2552739d5c645dbc`
- [再利用方法とHuman裁定負荷の承認判断](records/development/2026-08-15-safe-storage-capability-reuse-human-adjudication-decision-v1.md) — SHA-256 `68e9807328b8af3a8443534ab20b8da6d45afd42b03226a2b3964891ca9e1ceb`
- [Python仮想環境入口の不一致訂正Evidence](records/development/2026-08-15-python-venv-entry-correction-evidence-v1.md) — SHA-256 `17cc86a8ebde21a89cbf284b4f09dbbb18f7d261da9cf6b888bdb3f3398f9733`
- [製品TDD実装境界の事前確認方針](records/development/2026-08-15-tdd-implementation-boundary-precheck-policy-decision-v1.md) — SHA-256 `5c844a835b272283eb7ac485e2f5e4be792b7ded6dcf4d600054934a1007edfd`
- [安全保存の製品TDD実装作業票v1](docs/development/2026-08-15-session-artifact-safe-storage-implementation-work-ticket-v1.md) — SHA-256 `08465265b0881a63f4b209897072e7dcc2623e47c86ebffb7d19d1356eb9d326`

## 次に行う一作業

コミット済みの安全保存実装作業票v1を、作業担当と異なる新規実行単位が読み取り専用で反証し、契約22条件、八境界、再利用判断、変更範囲、安全条件、停止条件について開始可または修正要を返す。

開始条件：

- 作業票v1と固定入力のSHA-256がcommitへ固定され、worktreeがcleanである
- レビュー担当が作業担当と異なる新規実行単位で、成果物を変更しない
- 製品コード、製品試験、製品設定、配布入口が未変更である
- レビューは上位契約との矛盾、承認欠落、誤った合否、安全境界、範囲違反に限定する

完了条件：

- 契約受入条件1から22までの未接続が0件である
- 各境界の主要な失敗理由、最小実装、先取りしない責務、依存順、戻せる地点に止める指摘がない
- 参考だけの暫定処理が製品実行時依存へ入らず、固定file、権限、状態、削除確認値が契約と一致する
- 判定が開始可で、止める指摘0件または承認範囲内の一回の修正後確認で0件になる

後続作業：開始可の場合だけ境界1の失敗試験へ進む。修正要の場合は製品コードへ進まず、同じ原因をまとめた一回の限定修正後確認を行う。契約変更が必要なら、目的、根拠、判断基準、推奨案、影響へ圧縮して利用者へ戻す。

## blocker・Human判断待ち

- blocker：独立開始前確認には作業担当と異なる新規実行単位が必要である。現在の主担当だけでは独立確認済みと表示できない
- Human判断待ち：内部の新規Codexサブエージェント一名を、読み取り専用の独立開始前レビュー担当として使う明示許可が必要である。外部送信は行わない

## stale・deferred

- stale：固定20 pathによる旧検索、過大な平坦候補を作った能力検索v1からv3、および対応する旧証明書は履歴観測として保持するが、現在の実装開始根拠に使わない
- deferred：独立開始前レビューが開始可となるまで、失敗試験、製品コード、製品設定、配布入口を変更しない。中央一覧、自動commit、push、外部送信も開始しない

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：実装境界は文書作業であり製品試験は未実施。八境界の存在、受入条件1から22の欠落0、参照Digest、TODO単一入口を機械確認する
- 直近の全Test：直近の正規全試験は1,762件成功、失敗・error・skip 0、終了コード0。今回の変更では製品コード、試験、設定を変更していない
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
