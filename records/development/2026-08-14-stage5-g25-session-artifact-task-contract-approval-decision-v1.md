# 第5段 G25 Session記録成果物 Task Contract承認判断 v1

- Decision ID：`DEC-STAGE5-G25-SESSION-ARTIFACT-TASK-CONTRACT-APPROVAL-2026-08-14-V1`
- 判断日：2026-08-14
- 判断主体：利用者
- 対象契約：`TC-RC3-PRODUCT-G25-SESSION-ARTIFACT-PREPARATION-001` version 1
- 対象path：`records/task-contract/2026-08-14-g25-session-artifact-preparation-candidate-v1.md`
- 対象SHA-256：`20e4e0551c5b1357ba3e66d6ba849f19566da27c58c54ef98e8fa1db110fb72b`
- 対象commit：`4edac47151c0d0fc9ace5d8bb7a7fca08a913e86`
- 訂正後独立レビュー：`records/development/2026-08-14-stage5-g25-session-artifact-task-contract-definition-correction-review-v1.md`
- レビューSHA-256：`8f07d74cb03e4ab6134a1774af8b775e1d01c57d836f32720ad6296dd1099e91`
- 判断：`approved_for_implementation`

## 1. 利用者の判断

【記録】利用者は、案Cが何であるか、何のために使う機能か、契約の責務、入力、処理、出力、範囲外、
安全性の限界、実装範囲、完成条件について平易な説明を受けた。その後、次のとおり明示した。

> 承認

【判断】この承認を、対象SHA-256で固定したTask Contract version 1の意味と、その契約に従う実装開始の
承認として採用する。

## 2. 承認した内容

1. 利用者が許可したローカルSession記録一件を読み取り、三形式の識別、伏字化した転写・要約・来歴の
   生成、安全な項目だけの構造化出力を行う責務を承認する。
2. 読取り専用とし、file書込み、探索、複数file処理、network、外部送信、外部process、Git操作、
   権限変更、利用者判断の自動推測を行わない境界を承認する。
3. 既定規則、高い乱雑性の検査、絶対pathの最終検査で確認できる範囲を保証するが、その他の低い乱雑性の
   機微情報をすべて検出する保証はなく、出力を外部送信許可済みと扱わない限界を承認する。
4. 案Cを採用し、実装範囲を次の三pathだけに限定する。
   - 新規：`tools/session_logs/read_only_entry.py`
   - 変更：`pyproject.toml`の`[project.scripts]`へ専用実行名一件を追加
   - 新規：`tests/test_session_log_read_only_entry.py`
5. G25の既存10 path、G26、G30、他142 pathを変更範囲へ加えず、上流候補を暫定のまま正式化しない。
6. 契約§13の順序に従い、入口固有の失敗試験、最小実装、関連試験、通常の全試験、利用者向け出力例、
   独立完了レビューの順で進める。

## 3. 実装時の停止条件

次の場合は承認を拡張せず停止し、利用者へ戻す。

- G25の既存10 path、G26、G30、他142 pathの変更が必要になった。
- 保存、探索、外部送信、環境値解決その他の範囲外能力が必要になった。
- 三pathでは契約の安全な出力境界または正規入口を完成できない。
- 契約の責務、限界、出力、受入条件を変える必要が生じた。
- 既存試験を書き換えなければ実装できない。

## 4. 未実施

【未実施】本Decisionは実装完了または第5段完了の判断ではない。新入口、試験、`pyproject.toml`、G25既存コード、
G26、G30、他142 path、上流候補、Issue、TODOは本Decision作成時点では変更していない。外部送信、push、tag、
amend、rebase、reset、履歴書換えも行っていない。
