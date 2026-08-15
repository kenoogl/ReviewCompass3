# 一件レビュー安全投影 独立完了レビュー v1

- Reviewer model：`gpt-5.6-sol`
- reasoning effort：`high`
- 実施日：2026-08-16
- 依頼record：`records/session-handoffs/2026-08-16-g02-safe-projection-completion-review-codex-request-v1.md`
- 先行レビュー：`records/development/2026-08-16-one-item-review-safe-projection-v2-limited-rereview-v1.md`
- 対象GREEN commit：`9e7bd97fa7c8df1252ceb91eeebcbab9eb54dd6b`
- 対象RED commit：`23be5e0d38e4f1d154a6756169525a3d6fb946fa`
- 危険度：`high`
- 方法：依頼record §3の鮮度検査と§4の独立完了レビューだけ
- 共通プロトコル上の状態：`verified`
- 判定：`verified`
- Finding：blocking 0件、non-blocking 0件

## 1. 結論

【判断】契約`TC-RC3-PRODUCT-ONE-ITEM-REVIEW-SAFE-PROJECTION-007 / v2`の受入条件1〜11は、
固定成果物、対象75試験、関連試験、正規全試験、静的検査、新作反証、別の現在位置からの正式実行を相互照合した結果、
成立した。誤合格、未接続、禁止作用、上位目的への悪影響は0件である。

【判断】blocking、non-blockingともFindingは0件であり、判定を`verified`とする。本判定は受入条件12の
利用者による製品受入を代替しない。

## 2. 開始時の鮮度検査

【実測】開始時のbranchは`main`、HEADは`5c8a999c7f3afda1cb8b26e6f7573af258ee8d95`だった。
`git status --short`は出力なし、終了コード0だった。

【実測】`git log -1 --format=%H%n%P%n%s --name-only -- records/session-handoffs`は終了コード0で、
自分宛の最新依頼recordを次のとおり特定した。

- commit：`5c8a999c7f3afda1cb8b26e6f7573af258ee8d95`
- 親commit：`9e7bd97fa7c8df1252ceb91eeebcbab9eb54dd6b`
- path：`records/session-handoffs/2026-08-16-g02-safe-projection-completion-review-codex-request-v1.md`
- 件名：`Request completion review of safe projection operation`

【実測】`.venv/bin/python3`で再計算した依頼record §2の対象5件のSHA-256は、記載値と全件一致した。
照合commandの終了コードは0だった。

| 固定対象 | 再計算値 |
| --- | --- |
| 採用済み契約v2 | `9a35a25fc6481a62e8978574f8f1e73dc123eda2f96e9acb213851686d10f603` |
| 採用判断 | `17b4f4f522810db3a851b1bc8dd1ab65bb90fb9ce5df2276ae60a42fcb19ec99` |
| 実装成功Evidence | `6b9e6dbd7c43f1d34dc456f3fff6bc5e17c82103a8aa5db623f0b841be84fb63` |
| 実行核 | `7ce02906cf5be3c6976ed602488516bdd9c4331fbe6193d16a2eb60bcc170a08` |
| 対象試験 | `2d2bd889b24af8e1e57cba86a779b83121bc86e8045685bf5ba0205214ee73e6` |

【判断】依頼record §3の鮮度停止条件には該当せず、固定対象を変更せず完了レビューへ進める状態だった。

## 3. commit列と変更範囲

【実測】RED commitは対象試験1 fileだけへ8試験を追加している。GREEN commitの直接の親はRED commitで、
GREEN commitは実行核、実装成功Evidence、`TODO_NEXT_SESSION.md`の3 pathだけを変更している。
採用判断commitからGREEN commitまでの全変更は、対象試験、実行核、Evidence、TODOの4 pathであり、契約§8の変更上限内だった。

【記録】実装成功Evidence §1はRED固定時の単独実行を`7 failed, 68 passed`、§3はGREEN後の対象試験を
75件成功、終了コード0としている。commit列と変更pathはこの記録と一致した。

【実測】保護基準commit `a052312645328d7272f65aededdb74152e157c41`からGREEN commitまで、契約§6.3の
保護対象18 pathを明示した`git diff --exit-code`は差分なし、終了コード0だった。G02本体・入口、実行器入口、
`pyproject.toml`、機微情報規則、G08・G24再利用4 file、既存G30基盤5 file、関連試験4 fileに変更はなかった。

## 4. 誤合格と未接続の独立反証

### 4.1 自由文遮断、固定投影、内容変異

【実測】実装担当のfixtureにない新作反証として、G02結果へ9個の異なる漏えい標識を注入した。対象は
`material.content`、material追加項目、`review_spec.goal`・`criteria`・`constraints`・追加項目、
`result_schema`追加項目、root追加項目、読取り結果の追加項目である。投影から実行記録まで機械処理し、標識の出現は0件だった。

【実測】同じ反証で、投影root 7項目、`material` 3項目、`result_schema` 3項目、`review_spec` 1項目が
契約§7.2の許可集合と完全一致した。`part_result_sha256`と`record_sha256`も投影と実行記録から独立再計算して一致した。
反証commandの終了コードは0だった。

### 4.2 閉じた8理由と呼出し順

【実測】`invalid_arguments`、`invalid_path`、`invalid_schema`、`invalid_utf8`、
`sensitive_data_remaining`、`size_limit_exceeded`、`unreadable_input`、`absolute_path_remaining`を一件ずつ
注入した新作反証で、8件すべてが`part_stopped`、`part_source: none`へ転記された。部品終了コードは
`sensitive_data_remaining`だけ3、ほか7件は2だった。集合外の`stale_material`は`internal_failure`となった。
反証commandの終了コードは0だった。

【実測】同じ反証と構文木検査の双方で、`read_input_files`、`prepare_material`がこの順で各1回だけ呼ばれることを
確認した。G02から追加された名前はこの2関数と例外型`ReviewStop`だけであり、例外型は呼び出されていない。

### 4.3 受入条件との接続

【実測】対象75試験の収集結果と試験本文を契約§9へ照合した。正例・着地・標準出力一致・束縛2件は
`test_prepare_positive_run_lands_projected_record`、自由文遮断と許可集合完全一致は
`test_prepare_record_excludes_free_text`、束縛不一致は`test_prepare_binding_mismatch_stops_without_files`、
停止変換と集合外理由は4試験、入力key違反は1試験へ接続されていた。既存67試験は基底契約006の停止表、
既存2操作、内容識別値、書込み境界、正式実行名を維持していた。

【実測】対象試験だけではG02について直接固定していない8理由全件、2関数の回数・順序、正式実行名による別の現在位置からの
G02実行、3種の内容識別値再計算は、本レビューの新作反証と実装成功Evidence §4へ接続して補完した。

【判断】契約§9.1〜§9.11に試験、Evidence、または本レビューの独立反証へ接続されていない受入条件はなかった。
§9.12は独立完了レビュー後のHuman境界として未実施のまま維持されている。

## 5. 禁止作用と上位目的への悪影響

【実測】RED commitからGREEN commitまでの実行核差分と構文木を機械検査した。通信、外部process、環境値解決、
時刻取得、乱数、入力外探索に当たる新規importと呼出しは0件だった。G02の許可2関数以外のG02関数呼出しも0件だった。
静的反証commandの終了コードは0だった。

【実測】別の現在位置`/private/tmp/g02-rv1/outside`から正式実行名`reviewcompass3-operation-run`で新作のG02契約を実行した。
終了コード0、標準エラー0 bytes、標準出力と着地fileは完全一致した。契約、投影、実行記録の3種のSHA-256を
独立再計算して一致し、4種の自由文の漏えいは0件だった。実行記録SHA-256は
`7f5ae22b7acc1b98745101674a40370443acb0b68a5127c705415385a2928f77`だった。一時fixtureは実行後に回収した。

【実測】既存2操作を含む対象75試験、G02 158試験、G08 107試験、G24 111試験、G30基盤38試験、
正規全試験2,313試験はすべて成功した。保護対象18 pathの差分0と合わせ、既存2操作の実行記録形式、G02本体、入口、
既存G30基盤、保護対象への退行は確認されなかった。

## 6. 必須の機械確認

【実測】依頼record §4の必須試験を、pipeやcommand連結を使わず個別に実行した。

| command | 成功件数 | 終了コード |
| --- | ---: | ---: |
| `.venv/bin/python3 -m pytest -q tests/test_operation_contract_run.py` | 75 | 0 |
| `.venv/bin/python3 -m pytest -q tests/test_one_item_review.py` | 158 | 0 |
| `.venv/bin/python3 -m pytest -q tests/test_one_design_acceptance.py` | 107 | 0 |
| `.venv/bin/python3 -m pytest -q tests/test_one_requirement_feature_source.py` | 111 | 0 |
| `.venv/bin/python3 -m pytest -q tests/test_first_review_task_contract_e2e.py` | 38 | 0 |
| 隔離条件の正規全試験 | 2,313 | 0 |

【実測】対象試験の収集は75件、実装担当fixtureにない動的反証2組と静的反証1組はすべて終了コード0だった。

## 7. 反証fixtureの手戻り

【実測】対象操作は、正式実行名を別の現在位置から動かす独立E2Eだった。期待executorと実executorはともに、
Reviewerの`.venv/bin/python3`から正式実行名を起動する機械処理だった。

【実測】初回は既定一時領域の`/var`経路が非追跡読取りで`unreadable_input`、次は乱数付きまたは長い
`/private/tmp`名が機微情報候補検査で`sensitive_data_remaining`となった。これは対象実装の不合格ではなく、
反証fixtureのpathが契約入力検査に適合しなかった事象である。

【実測】既存成果物の変更や手作業実行は行わず、短い固定一時path`/private/tmp/g02-rv1`が未存在であることを
機械確認してから同じ反証を再実行し、§5の合格を得た。fixtureは機械回収した。今後の同種反証は、固定された短い
安全な一時pathを事前検査して使う経路が機械処理候補である。

## 8. 判定、Human境界、未実施、次

【判断】blocking 0件、non-blocking 0件であり、停止判定の根拠はない。共通プロトコルの状態と依頼recordの判定を
ともに`verified`とする。

【実測】製品code、対象契約、既存試験、基底実行器、再利用部品、外部systemは変更していない。外部送信、push、
製品受入、G02のorganize操作、連鎖、保存統合は実施していない。

【判断】Human境界は維持した。本レビューが完了根拠にできるのは受入条件11までであり、受入条件12の製品受入は
利用者の判断として残る。

【提案】次の一作業は、Claudeが依頼record §6の事後照合を行い、縮小境界と実装結果を利用者へ提示して、
製品受入を一判断として求めることである。
