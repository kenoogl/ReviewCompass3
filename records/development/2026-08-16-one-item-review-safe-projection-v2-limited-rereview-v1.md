# 一件レビュー安全投影 契約候補v2 限定再確認 v1

- Reviewer model：`gpt-5.6-sol`
- reasoning effort：`high`
- 実施日：2026-08-16
- 依頼record：`records/session-handoffs/2026-08-16-g02-safe-projection-v2-limited-rereview-codex-request-v1.md`
- 先行レビュー：`records/development/2026-08-16-one-item-review-safe-projection-v1-independent-review-v1.md`
- 対象commit：`14a74a5a00ac4e38412e1b27bb9ae7ee2b915952`
- 対象契約：`records/task-contract/2026-08-16-one-item-review-safe-projection-candidate-v2.md`
- 対象契約SHA-256：`9a35a25fc6481a62e8978574f8f1e73dc123eda2f96e9acb213851686d10f603`
- 方法：依頼record §3の鮮度検査と§4の限定再確認だけ
- 共通プロトコル上の状態：`verified`
- 判定：`開始可`

## 1. 結論

【判断】v1独立確認の停止原因だった「8種の記載と9理由の列挙の競合」は閉じた。契約候補v2は、prepare経路の
2関数が到達し得る8理由だけを閉じた転記集合とし、集合外の理由を`internal_failure`へ固定している。実装開始の
前提となる契約採用と縮小境界の判断を利用者へ求めてよい。

【判断】v1からv2への変更は依頼record §2の訂正範囲に限定されている。v1で問題なしとされた安全投影の許可項目、
束縛照合位置、変更対象・保護基準、基底契約006 v4との整合に退行はない。blocking、non-blockingともFindingは0件である。

## 2. 開始時の鮮度検査

【実測】開始時のbranchは`main`、HEADは`49f34701deac2bb2f36c7920af20cd9353ad078e`だった。
`git status --short`は出力なし、終了コード0だった。

【実測】`git log -1 --format=%H%n%P%n%s --name-only -- records/session-handoffs`は終了コード0で、最新の
session handoffを次のとおり特定した。

- commit：`49f34701deac2bb2f36c7920af20cd9353ad078e`
- 親commit：`14a74a5a00ac4e38412e1b27bb9ae7ee2b915952`
- path：`records/session-handoffs/2026-08-16-g02-safe-projection-v2-limited-rereview-codex-request-v1.md`
- 件名：`Request limited re-review of safe projection contract v2`

【実測】依頼先の記載とsession handoffの履歴を再読込みし、本依頼recordがCodex宛ての最新依頼recordだった。

【実測】`.venv/bin/python3`で個別に再計算した固定入力3件のSHA-256は依頼record記載値と一致した。各commandの
終了コードは0だった。

| 固定入力 | 再計算値 |
| --- | --- |
| 対象契約候補v2 | `9a35a25fc6481a62e8978574f8f1e73dc123eda2f96e9acb213851686d10f603` |
| v1独立確認 | `b211626ba83409e9a892c202c0903e1363b535dc93b6f390627d42361ba3d33f` |
| 直前版契約v1 | `b42232fd0f6a559a680c5447845502a0947b0d96caaaddae208c8bf0c94a2f9b` |

【実測】`git diff --exit-code 14a74a5a HEAD -- <対象契約候補v2>`は差分なし、終了コード0だった。開始条件は
鮮度停止に該当しなかった。

## 3. 訂正1点の閉鎖

【実測】契約候補v2 §7.1は、転記理由を`invalid_arguments`、`invalid_path`、`invalid_schema`、
`invalid_utf8`、`sensitive_data_remaining`、`size_limit_exceeded`、`unreadable_input`、
`absolute_path_remaining`の閉じた8種として列挙し、8種以外は`internal_failure`とする。organize経路専用の
`stale_material`も集合外の例として明記する。

【記録】先行レビュー§3.1は、現物の`read_input_files`と`prepare_material`および補助関数から到達できる理由が
上記8種であり、`stale_material`は範囲外の`validate_results`だけに存在すると、実行fixtureと構文木抽出の両方で
確認している。

【実測】§6.2のG02核`tools/reviews/one_item_review.py`のSHA-256は
`de658b6e96b804af393d106cbc11c39d7452e9cb54c24c5157853bc5dcd9ad57`で先行レビュー時の固定値と一致した。
保護基準commitからHEADまで同fileに差分がないため、先行レビューの現物到達可能集合を今回も適用できる。

【実測】`.venv/bin/python3`の補助検査で、§7.1の列挙が期待する8理由と順序を含め完全一致し、集合外理由の
`internal_failure`固定と、受入条件5の`stale_material`相当の反証が存在することを確認した。訂正版commandの
終了コードは0だった。

【実測】補助検査の初回だけは、抽出用正規表現が数字を許さず`invalid_utf8`を抽出できなかったため終了コード1だった。
対象記載の欠落ではなく検査式の誤りであり、正規表現を`[a-z0-9_]+`へ訂正した同一確認で上記の終了コード0を得た。
対象成果物は変更していない。

【判断】転記対象の8理由と集合外変換は一意である。先行レビューが示した二通りの実装解釈は残っておらず、停止原因は閉じた。

## 4. v1からの退行確認

【実測】`git diff --no-index --unified=12 <契約候補v1> <契約候補v2>`は差分があるため終了コード1となり、全文差分は
次の箇所だけだった。

1. 見出し、契約版、状態、`supersedes`、訂正根拠、訂正範囲
2. §6.2のprepare経路8理由と`stale_material`の到達範囲の注記
3. §7.1の閉じた8理由と集合外の`internal_failure`固定
4. 受入条件5の集合外理由の反証
5. §11の次作業を限定再確認へ更新する文

【実測】安全投影の許可項目を定める§7.2、二つの束縛照合位置を定める§7.3、変更上限を定める§8、停止条件を
定める§10に差分はなかった。

【実測】保護基準commit `a052312645328d7272f65aededdb74152e157c41`からHEADまで、§6.3が保護する18 pathを
`git diff --exit-code`で照合し、差分なし、終了コード0だった。内容識別値が記載されていない
`tests/test_first_review_task_contract_e2e.py`も18 pathに含めた。

【判断】訂正は停止理由集合の一意化とその確認可能性に限られ、先行レビューで問題なしとされた4境界へ意味変更を
持ち込んでいない。

## 5. 必須の機械確認

【実測】契約候補v2 §6.1〜§6.3に値が記載された19 fileのSHA-256を`.venv/bin/python3`で再計算し、19件一致、
不一致0件、終了コード0だった。

| 確認 | 件数 | 結果 | 終了コード |
| --- | ---: | --- | ---: |
| §6.1〜§6.3の内容識別値 | 19 | 全件一致 | 0 |
| §6.3の保護対象 | 18 path | 保護基準commitから差分なし | 0 |

【判断】依頼record §4が必須とした機械確認は合格した。限定再確認の依頼で指定されていない試験群の再実行と、
先行レビュー済みの全面的な定義反証は行っていない。

## 6. 範囲、Human境界、次

【実測】許可範囲は本判定record一件の作成と単独commitだけである。製品code、対象契約、既存試験、基底実行器、
再利用部品、外部systemは変更していない。外部送信、実装開始、契約採用、縮小境界のHuman判断は実施していない。

【判断】Human境界は維持した。`開始可`は実装の自動開始ではなく、利用者へ契約採用と縮小境界の判断を求められる
ことを意味する。

【提案】次の一作業は、Claudeが依頼record §6の事後照合を行い、その結果を踏まえて契約採用と実装開始の一判断を
利用者へ求めることである。
