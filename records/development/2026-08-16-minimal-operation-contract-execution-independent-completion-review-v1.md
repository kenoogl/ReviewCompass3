# 最小運用契約実行 独立完了レビュー v1

- Reviewer model：`gpt-5.6-sol`
- reasoning effort：`high`
- 実施日：2026-08-16
- 依頼record：`records/session-handoffs/2026-08-16-g30-operation-run-completion-review-codex-request-v1.md`
- 先行レビュー：`records/development/2026-08-16-minimal-operation-contract-execution-v4-limited-rereview-v1.md`
- 対象実装commit：`b1ad31ad497d8b47877cbaccc1b2878d6e88b3df`
- 対象契約：`TC-RC3-PRODUCT-MINIMAL-OPERATION-CONTRACT-EXECUTION-006 / v4`
- review risk：`high`
- 方法：依頼record §3の鮮度検査と§4の独立完了レビューだけ
- 判定：`correction_required`
- Finding：blocking 3件、non-blocking 0件

## 1. 結論

【判断】受入条件20は成立しない。通常の対象・関連・正規全試験はすべて成功したが、独立反証で受入条件12、
15の実装違反2件と、受入条件10の誤合格を許す試験欠陥1件を確認した。3件はいずれも完了段階のblocking
Findingであり、`docs/development/work-review-protocol.md` §11.1類型3「誤った合格を実証できる受入条件・
検証の欠陥」に該当する。

【判断】対象実装の通信・外部process・Git・環境値解決・時刻取得・乱数・入力外探索、保護15 pathの変更、
既存G30基盤の正式化、Human境界の違反は確認しなかった。しかしblocking 3件が残るため、受入条件20の
「誤合格0件」および完了判定には使えない。

## 2. 開始時の鮮度検査

【実測】開始時のbranchは`main`、HEADは`e5778d4cd46f1a9ad44527eea75ac9a4a2d3bcc5`だった。
`git status --short`は出力なし、終了コード0だった。

【実測】`git log -12 --format=%H%x09%P%x09%s -- records/session-handoffs`は終了コード0だった。最新handoffは
HEADの本依頼recordで、依頼先はCodex、親commitは対象実装commit `b1ad31a`だった。
`git merge-base --is-ancestor b1ad31a HEAD`も終了コード0だった。

【実測】依頼record §2の固定7 fileについてSHA-256を`.venv/bin/python3`で再計算し、全件が記載値と一致した。

| 固定入力 | 再計算したSHA-256 |
| --- | --- |
| 契約v4 | `d7b1861ccc73cb8f1c305294bf7c7e2a5fddd6ddb3fb46eab74e3204e8a2a7a1` |
| 採用judgment | `5f8c9fab3e3512376359f4b58ca528b87adcb74d0d488e1e86af1af06f2b6614` |
| 実装成功Evidence | `145f4938b7358acf301195901dfcacdf633b712927e60539c2db8e956c088336` |
| 実行核 | `b09a41e1396263a6be48c5e062c18983f8d343034aa25946af8d387d0aa000f4` |
| 入口 | `a7521c5a2ed314c248b91738d390e1b4144287a1b840b51235971f2b2a6a0a21` |
| 対象試験 | `1b03ab702e9347b5dd31784f99cdf6001a3b3ef7d70c5326fe2f486584586c65` |
| `pyproject.toml` | `bea8151c9c055d9fe696672013b64e566579d9a7365f3c753b9eedae7885d5ef` |

【判断】固定入力、宛先、開始状態に不一致はなく、鮮度停止には該当しなかった。

## 3. Claim、変更範囲、Provenanceの照合

【実測】RED commit `fd24453`は対象試験1 fileだけを追加した。commit列は`fd24453`（RED）→`918e838`
（契約v4）→`f7513dd`（限定再確認依頼）→`a5377a1`（限定再確認判定）→`b1ad31a`（GREEN）で、
実装成功Evidence記載の順序と一致した。

【実測】対象実装commit `b1ad31a`の変更は、`TODO_NEXT_SESSION.md`、`pyproject.toml`、成功Evidence、対象試験、
`tools/operations/`の3 fileの計7 pathだった。製品変更は契約§12の実行核、入口、実行名、対象試験と、許可された
作業票・Evidenceに限定されていた。対象実装commit以後、HEADまでの追加は本レビュー依頼record 1件だけだった。

【実測】契約§6.1〜§6.3の再利用・保護15 pathは、記載SHA-256と全件一致した。
`git diff --exit-code bb55a1f HEAD -- <15 path>`は差分なし、終了コード0だった。既存G30基盤5 fileを含む
保護対象に変更はなかった。

【実測】製品2 fileを抽象構文木で確認した。importは標準module、固定部品入口、固定機微検査だけであり、`os`呼出しは
`open`、`read`、`write`、`fstat`、`lstat`、`link`、`unlink`、`close`だけだった。通信、外部process、
subprocess、Git、環境値解決、時刻取得、乱数、directory作成、権限変更を行う呼出しはなかった。

【記録】成功Evidence §4は、正式実行名をrepository外から実行した合成E2Eについて、終了コード0、標準エラー0 bytes、
G24部品実行、2入力の束縛一致、標準出力と実行記録fileの完全一致、判断待ち、安全表示、一時名残留なしを記録している。
これは依頼recordが受入条件21へ指定したEvidenceである。

## 4. blocking Finding

### B-01：同一inode・同一sizeの読取り中変更を受理する

- 区分：`blocking`
- 確認段階：`completion`
- 根拠類型：3（誤った合格を実証できる受入条件・検証の欠陥）
- 対応受入条件：12、15

【実測】一時領域の契約fileを読み始めた後、最初の`os.read`直後に、同じ8 bytesの別内容を同一fileへ書き戻す
新作反証を実行した。期待は`unreadable_input / contract`だったが、`read_contract_file`は変更前の8 bytesを正常値として
返し、commandは反証不成立を示す終了コード1になった。実fileは変更後の別内容だった。

【実測】実装は読取り前後の`st_mode`、`st_size`、`st_dev`、`st_ino`と実読取りbyte数だけを比較する。
同じinode・同じsizeの書換えでは全比較値が不変なため、読取り中変更を検出できない。対象61件には読取り中変更の
失敗注入がなく、通常試験はこの違反を検出せず成功した。

【判断】契約§11と受入条件12が要求する「読取り中変更を停止する」を満たさず、変更中の入力を誤って受理するため
blockingである。

### B-02：不正な引数path 2変種の停止形式が契約と異なる

- 区分：`blocking`
- 確認段階：`completion`
- 根拠類型：3（誤った合格を実証できる受入条件・検証の欠陥）
- 対応受入条件：15

【実測】`--contract`へ絶対path形式の文字列としてNUL文字を含む値と、単独サロゲートを含む値を個別に渡す新作反証を
実行した。両方とも期待値は`invalid_path / arguments`・終了コード2だが、実結果は
`internal_failure / none`・終了コード4だった。2変種を一括したcommandは終了コード1だった。

【実測】入口のpath検査は、先頭`/`と空・`.`・`..`の構成要素だけを確認し、NUL文字と単独サロゲートを読取り前に
拒否しない。後段のfile openで一般例外となり、包括例外処理が`internal_failure`へ変換する。対象61件は相対pathだけを
反証し、この2変種を検出せず成功した。

【判断】処理自体は停止するが、契約§7・§11が固定する読取り前の`invalid_path / arguments`・終了コード2を満たさず、
受入条件15を満たしたという試験判定を誤って合格させるためblockingである。

### B-03：機微情報候補3類型を外しても対象61件が成功する

- 区分：`blocking`
- 確認段階：`completion`
- 根拠類型：3（誤った合格を実証できる受入条件・検証の欠陥）
- 対応受入条件：10、20

【実測】実行核が使う既定patternを実行時にemailとAWS鍵形式の2件だけへ変異させ、bearer token、API key代入、
秘密鍵blockの3規則を外した状態で対象試験を再実行した。61件すべてが成功し、終了コード0だった。固定fileの
内容識別値と既定pattern件数5の試験は、再利用module側だけを見ているためこの変異を検出しなかった。

【実測】無変異の実装へbearer token、API key代入、秘密鍵blockを各1件与えた独立oracleでは、3件とも
`sensitive_data_remaining / contract`で停止し、commandは終了コード0だった。正しい束縛SHA-256と固定registry操作名だけを
除外し、別位置の高乱雑性hex64を3位置で停止する独立oracleも終了コード0だった。

【判断】現実装の3規則は動作するが、対象61件はその欠落を検出できない。成功Evidence §3の「機微6種を含む」と§5の
「受入条件1〜17は対象試験61件が覆う」は、この変異に対して誤合格する。高riskの受入条件10・20を支える試験として
不足するためblockingである。

## 5. 書込み境界の独立反証

【実測】対象試験には、再読込不一致、hard link失敗、公開後の一時名削除失敗の反証があり、61件の通常実行で成功した。

【実測】対象fixtureにない反証として`os.write`を失敗させた。一時成果と最終名はいずれも残らず、
`record_write_failed / output`となり、commandは終了コード0だった。

【実測】出力先事前検査後、hard link直前に最終名を作る競合を注入した。既存bytesは上書きされず、一時成果は回収され、
`record_write_failed / output`となり、commandは終了コード0だった。

【判断】受入条件16b・16cの実装について、上の独立反証では新たな欠陥を確認しなかった。

## 6. 必須の機械確認

【実測】次を各単独commandとして実行し、各終了コードで判定した。

| command | 件数 | 結果 | 終了コード |
| --- | ---: | --- | ---: |
| `.venv/bin/python3 -m pytest -q tests/test_operation_contract_run.py` | 61 | 成功 | 0 |
| `.venv/bin/python3 -m pytest -q tests/test_one_design_acceptance.py` | 107 | 成功 | 0 |
| `.venv/bin/python3 -m pytest -q tests/test_one_requirement_feature_source.py` | 111 | 成功 | 0 |
| `.venv/bin/python3 -m pytest -q tests/test_one_item_review.py` | 158 | 成功 | 0 |
| `.venv/bin/python3 -m pytest -q tests/test_first_review_task_contract_e2e.py` | 38 | 成功 | 0 |
| 依頼record §4.5の認証環境値を外した`.venv/bin/python3 -m pytest -q` | 2,299 | 成功 | 0 |
| 読取り中の同一inode・同一size変更反証 | 1 | 期待停止せず受理 | 1 |
| 不正な引数pathのNUL・単独サロゲート反証 | 2 | 期待と異なる停止形式 | 1 |
| 機微pattern 3件除去の変異下で対象試験 | 61 | 誤って全件成功 | 0 |
| 無変異での機微pattern 3件の独立oracle | 3 | 全件期待停止 | 0 |
| 限定除外の位置・値境界oracle | 4 | 全件期待どおり | 0 |
| 書込み失敗時の回収反証 | 1 | 期待どおり | 0 |
| 公開直前の最終名競合反証 | 1 | 非上書き・回収 | 0 |

## 7. Human境界、未実施、次

【実測】レビュー中に対象契約、製品code、試験、既存record、再利用部品、外部systemを変更していない。外部送信、
push、製品受入、G30全体の完了、後続縦切り、blocking Findingの修正は実施していない。

【判断】Human境界は維持した。本判定は受入条件22の利用者による製品受入を代替せず、`verified`の完了根拠を作らない。

【提案】次の一作業は、ClaudeがB-01〜B-03を一つの最小修正単位で直し、対象・関連・正規全試験と本反証を再実行した後、
独立完了再レビューを依頼することである。
