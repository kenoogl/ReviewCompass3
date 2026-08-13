# Work 5B契約試験整理 作業票 v1

- 作成日：2026-08-14
- 状態：`approved / implementation_pending`
- 現在段階：立て直し計画v5 第3段
- 基準commit：`b609d86`
- 対象Issue：`ISSUE-TEST-GROWTH-STATE-PINNING-001`
- 対象種別：試験コード、履歴・監査資料
- 危険度：`high（既存試験の意味的削除）`
- 作業担当：操縦役
- 完了レビュー担当：新規サブエージェント
- Human承認：2026-08-14、利用者が案C、試験file一件・六試験の削除、履歴資料無変更を承認

## 1. 目的

完了済みWork 5Bの履歴内容を現在fileのbytesへ束縛し、正当な後続変更を不合格にしていた
`tests/test_work5b_contract.py`一件・六試験を現役試験集合から外す。現在の検査処理を守る直接試験は維持し、
契約v1・v2と過去Decision・Evidenceは履歴として無変更で残す。

## 2. 入力と根拠

- 役割再評価Evidence：
  `records/development/2026-08-14-work5b-contract-lifecycle-reassessment-evidence-v1.md`
- 独立完了レビュー：
  `records/development/2026-08-14-work5b-contract-lifecycle-reassessment-independent-completion-review-v1.md`
- 利用者が2026-08-14に案Cを承認した。
- 削除前試験file SHA-256：`9630b087d400dd13eb36c519a5d916755626ebcb15ffb6942ad6ce87cb05d9d0`
- 契約v1 SHA-256：`89c92ae260bfb1efd201d414e0235b66ebb270b457942c59ef5fccfc9cfa5387`
- 契約v2 SHA-256：`5123b778cb12b8cf23f353d9725c0598f9214fdcf66d625f9385ef2ebd8a20f0`

## 3. 作業範囲と対象外

変更対象は次の二成果だけとする。

- 削除：`tests/test_work5b_contract.py`一件・六試験
- 追加：本作業の実施Evidence一件

対象外：Work 5B契約v1・v2、固定source Decision・Evidence、初期開発チェックリスト、現在の検査コード、
他の試験、設定、正本、TODO、v2内容識別値、後継契約、新しい検査器・台帳・試験、G06案B、外部送信、
履歴書換え、第3段完了判断。

## 4. 期待する成果

- 契約試験file一件だけが削除される。
- 契約v1・v2と過去の固定source Decision・Evidenceのbytesは基準commitと同一である。
- 現在の宣言対応表検査と再利用検索を直接守る22試験が成功する。
- 正規入口の全試験が成功し、収集数は削除前1,737件から六件減の1,731件になる。
- 削除前fileとcommit `c0acdcd`時点の契約試験六件をGitから回復できる。

## 5. 機械で確認する事実と正規入口

1. Git差分が試験file一件の削除と実施Evidence一件の追加だけであることを確認する。
2. 六試験名と削除fileを読む製品コード、検査コード、設定、他試験の参照が0件であることを確認する。
3. `.venv/bin/python3 -B -m pytest -q tests/test_declaration_red_map_check.py tests/test_reuse_search_externalization.py tests/test_adversarial_remedy_batch1.py`を単独実行する。
4. `.venv/bin/python3 -B -m tools.development.policy_test_runner --suite full --receipt <repository外path>`を単独実行する。
5. 契約v1・v2、固定source Decision・EvidenceのSHA-256を基準commitと比較する。
6. Git物体から削除前fileと`c0acdcd`時点を再読込みし、当時六件成功をリポジトリ外で確認する。
7. `git diff --check`を実行する。

## 6. レビューで判断する事項

新規サブエージェントが一回の独立完了レビューで、変更範囲、現在保証22件、全試験、参照切れ、履歴回復、
契約資料の不変、禁止した新機構がないことを確認する。成果を修正せず、本質から外れた追加案を出さない。

## 7. 停止条件と完了条件

次の場合は停止する。

- 試験file一件以外の削除・変更が必要になる。
- 契約、Decision、Evidence、現在処理、他試験の変更が必要になる。
- 直接試験22件または正規全試験が失敗する。
- 収集数が1,731件にならない。
- 製品コード、検査コード、設定、他試験からの参照が見つかる。
- Gitから履歴を回復できない。

完了条件は、承認範囲の削除、§5の全確認成功、意味的に完結した実施commit、独立完了レビュー`verified`、
作業単位遷移検査の成功である。完了後は承認済みG06案Bへ戻る。
