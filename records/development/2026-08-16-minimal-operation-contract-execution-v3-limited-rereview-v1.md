# 最小運用契約実行 契約候補v3 限定再確認 v1

- Reviewer model：`gpt-5.6-sol`
- reasoning effort：`high`
- 実施日：2026-08-16
- 依頼record：`records/session-handoffs/2026-08-16-g30-operation-contract-v3-limited-rereview-codex-request-v1.md`
- 先行レビュー：`records/development/2026-08-16-minimal-operation-contract-execution-v2-limited-rereview-v1.md`
- 対象commit：`8351622efb8c66b018fe1ccd7e3e69f905c50a3b`
- 対象契約：`records/task-contract/2026-08-16-minimal-operation-contract-execution-candidate-v3.md`
- 対象契約SHA-256：`d97a742bd2c67946f4336a06167767c4060a38157073e13cb42e5ecbf2117f85`
- 方法：依頼record §3の鮮度検査と§4の限定再確認だけ
- プロトコル状態：`verified`
- 判定：`開始可`

## 1. 結論

【判断】固定commit `8351622`の契約候補v3から実装を開始できる。v2の停止原因だった、hard linkによる公開確定後の
一時名削除失敗は、公開の確定点、停止状態、終了コード、残留状態、回復境界まで一意に定義され、閉じた。
今回の限定再確認でblocking Findingは0件、未接続条件は0件である。

【判断】v2で開始可とされたregistryの2操作への縮小、目的縮小の固定、§8.2の機微情報候補検査、§10.2の
束縛照合位置4件、固定内容識別値、基準commitには、v3差分による退行を確認しなかった。

## 2. 開始時の鮮度検査

【実測】開始時のbranchは`main`だった。`git status --short`は出力なし、終了コード0だった。

【実測】`git log -10 --format=%H%x09%P%x09%s -- records/session-handoffs`は終了コード0で、最新のsession handoffを
次のとおり特定した。

- commit：`9d21472a1ebf2b2955182b3fb5bd709dd598e488`
- 親commit：`8351622efb8c66b018fe1ccd7e3e69f905c50a3b`
- path：`records/session-handoffs/2026-08-16-g30-operation-contract-v3-limited-rereview-codex-request-v1.md`
- 件名：`Request limited re-review of operation contract v3`

【実測】依頼先はCodexであり、本依頼recordが自分宛の最新依頼recordだった。レビュー開始時のHEADも
`9d21472a1ebf2b2955182b3fb5bd709dd598e488`だった。

【実測】`.venv/bin/python3`で個別に再計算した依頼record §2の3 fileのSHA-256は、記載値と全件一致した。
各commandの終了コードは0だった。

| 固定入力 | 再計算値 |
| --- | --- |
| 対象契約候補v3 | `d97a742bd2c67946f4336a06167767c4060a38157073e13cb42e5ecbf2117f85` |
| v2限定再確認 | `1926cfa2f4ebbb45d500813348e61cebc9f25018eae22194d28afaaa5aec005d` |
| 直前版契約v2 | `927965f9502c0762c0ba289968d37d16237ae0ef433f15c2ac53cc8dacd94090` |

【実測】`git merge-base --is-ancestor 8351622 HEAD`と、対象契約についての
`git diff --exit-code 8351622 HEAD -- <対象契約>`は、ともに終了コード0だった。対象契約は固定commitの内容から
変わっていない。鮮度停止には該当しなかった。

## 3. v2停止原因が閉じたこと

【実測】契約§7手順3はhard link成功を公開の確定点とし、確定点以降の最終名を有効な実行記録の正本と定義する。
手順5は、その後の一時名削除失敗を`partial_cleanup_failed`で停止し、最終名と一時名が同一inode・同一bytesで
残ること、一時名は正本でないことを定義する。回復は利用者による一時名削除に限定され、同じ契約の再実行は
最終名既存の`invalid_output_root`で停止する。

【実測】§11の停止表は、`partial_cleanup_failed`をsource `output`、終了コード6へ接続する。停止結果の共通規則により
標準エラーは空である。§13.16・16b・16cは、正常完了、公開前失敗、公開後削除失敗の残留と反証をそれぞれ分け、
§14は手順4・5の自作一時成果だけを削除禁止の例外へ固定する。

【判断】書込み経路の失敗位置は次のとおり一意に閉じている。

| 失敗位置 | 結果と残留 |
| --- | --- |
| 一時成果の作成 | `record_write_failed`、終了コード4。最終名は未作成 |
| 書込み・再読込照合・hard link作成 | `record_write_failed`、終了コード4。自作一時成果を回収し、最終名は未作成 |
| 公開前回収 | `record_write_failed`、終了コード4。回収失敗時だけ一時名が残り、最終名は未作成 |
| 公開後の一時名削除 | `partial_cleanup_failed`、終了コード6。公開済みの最終名と同一inodeの一時名が残る |

【判断】確定点後の削除失敗を正常、公開前停止、内部失敗のどれへ分類するか、残る2名をどう扱うか、誰が回復するかを
実装者が後決めする余地は残っていない。v2の停止原因は閉じた。

## 4. 退行確認

【実測】`git diff --no-index --numstat <v2> <v3>`は、34行追加・22行削除を示した。差分が存在するため終了コードは
期待どおり1だった。`--unified=0`で再読込みした全文差分は、次だけだった。

- 見出しの版、契約版、supersedes、訂正根拠、訂正範囲の更新
- §7の公開確定点、公開前回収、公開後清掃と許可する削除の更新
- §11の確定点前後の停止規則、処理順、`record_write_failed`の範囲、`partial_cleanup_failed`の追加
- §13.16・16b・16c、§14、§15を同じ定義へ合わせる更新

【実測】registryはG08とG24の2操作のままで、目的と範囲、§8.2の機微情報候補検査、§10.2の束縛照合位置4件、
§6の固定内容識別値、保護基準commit `bb55a1fb8d56f45a3c861601ff91b62deab23e26`に差分はなかった。

【実測】§6.1の再利用4 file、§6.2の1 file、§6.3の保護10 pathは、記載SHA-256と全件一致した。15 pathについて
`git diff --exit-code bb55a1f HEAD -- <15 path>`も差分なし、終了コード0だった。

【判断】v2からv3への変更は依頼record §2の訂正範囲に限定され、指定された既存境界に退行はない。

## 5. 必須の機械確認

【実測】内容識別値は各組を`.venv/bin/python3`で別々に照合し、試験はpipeやcommand連結を使わず個別に実行した。

| command／確認 | 件数 | 結果 | 終了コード |
| --- | ---: | --- | ---: |
| §6.1 再利用fileのSHA-256 | 4 | 全件一致 | 0 |
| §6.2 機微情報候補検査fileのSHA-256 | 1 | 一致 | 0 |
| §6.3 保護pathのSHA-256 | 10 | 全件一致 | 0 |
| §6.1〜§6.3の15 pathと基準commit `bb55a1f`の差分 | 15 | 差分0 | 0 |
| `.venv/bin/python3 -m pytest -q tests/test_one_design_acceptance.py` | 107 | 全件合格 | 0 |
| `.venv/bin/python3 -m pytest -q tests/test_one_requirement_feature_source.py` | 111 | 全件合格 | 0 |
| `.venv/bin/python3 -m pytest -q tests/test_one_item_review.py` | 158 | 全件合格 | 0 |
| `.venv/bin/python3 -m pytest -q tests/test_first_review_task_contract_e2e.py` | 38 | 全件合格 | 0 |

## 6. 範囲、Human境界、未実施、次

【実測】製品code、対象契約、既存試験、固定部品、外部systemは変更していない。レビューは依頼record §3の鮮度検査と
§4の限定再確認だけであり、全面再走査は行っていない。

【実測】契約採用、実装開始、縮小境界の採否、最終受入、外部送信は実施していない。

【判断】Human境界は維持した。本recordの`開始可`は限定再確認の完了根拠であり、契約採用や最終受入のHuman判断を
代替しない。

【提案】次の一作業は、Claudeが本判定recordのcommit、変更path、判定内容を事後照合することである。
