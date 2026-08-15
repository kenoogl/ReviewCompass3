# 最小運用契約実行 契約候補v4 限定再確認 v1

- Reviewer model：`gpt-5.6-sol`
- reasoning effort：`high`
- 実施日：2026-08-16
- 依頼record：`records/session-handoffs/2026-08-16-g30-operation-contract-v4-limited-rereview-codex-request-v1.md`
- 先行レビュー：`records/development/2026-08-16-minimal-operation-contract-execution-v3-limited-rereview-v1.md`
- 対象commit：`918e838fd9d7bc4d102030274158fbcacdeb1f81`
- 対象契約：`records/task-contract/2026-08-16-minimal-operation-contract-execution-candidate-v4.md`
- 対象契約SHA-256：`d7b1861ccc73cb8f1c305294bf7c7e2a5fddd6ddb3fb46eab74e3204e8a2a7a1`
- 方法：依頼record §3の鮮度検査と§4の限定再確認だけ
- プロトコル状態：`verified`
- 判定：`開始可`

## 1. 結論

【判断】固定commit `918e838`の契約候補v4から実装を再開できる。手順3bにより、正確な位置`/operation`にある
固定registry操作名との完全一致だけが機微情報候補の検査対象から外れ、2操作の正例は固定操作名を理由とする
機微停止をしない。完全一致しない値と他の位置は除外されないため、利用者の識別子、自由文、path、未知keyへ
除外が拡大する後決め要素はない。今回の限定再確認でblocking Findingは0件、non-blocking Findingは0件である。

【判断】v3で開始可とされた書込み境界の確定点、registryの2操作への縮小、目的縮小、束縛照合位置4件、
固定内容識別値には、v4差分による退行を確認しなかった。

## 2. 開始時の鮮度検査

【実測】開始時のbranchは`main`、HEADは`f7513dd53db13496ce20639cc48596720cec1124`だった。
`git status --short`は出力なし、終了コード0だった。

【実測】`git log -12 --format=%H%x09%P%x09%s -- records/session-handoffs`は終了コード0で、最新の
session handoffを次のとおり特定した。

- commit：`f7513dd53db13496ce20639cc48596720cec1124`
- 親commit：`918e838fd9d7bc4d102030274158fbcacdeb1f81`
- path：`records/session-handoffs/2026-08-16-g30-operation-contract-v4-limited-rereview-codex-request-v1.md`
- 件名：`Request limited re-review of operation contract v4`

【実測】依頼先はCodexであり、本依頼recordが自分宛の最新依頼recordだった。

【実測】`.venv/bin/python3`で個別に再計算した依頼record §2の3 fileのSHA-256は、記載値と全件一致した。
各commandの終了コードは0だった。

| 固定入力 | 再計算値 |
| --- | --- |
| 対象契約候補v4 | `d7b1861ccc73cb8f1c305294bf7c7e2a5fddd6ddb3fb46eab74e3204e8a2a7a1` |
| 直前版契約v3 | `d97a742bd2c67946f4336a06167767c4060a38157073e13cb42e5ecbf2117f85` |
| v3限定再確認 | `daa414658c2d6fc8ef712ceb47ae9b188cd787c1214be1ab826209795e97689e` |

【実測】`git merge-base --is-ancestor 918e838 HEAD`と、対象契約についての
`git diff --exit-code 918e838 HEAD -- <対象契約>`は、ともに終了コード0だった。対象契約は固定commitの内容から
変わっていない。鮮度停止には該当しなかった。

## 3. 訂正1点が閉じたこと

【実測】`tools.session_logs.redaction.find_high_entropy`を既定引数で各操作名へ個別実行した結果は次のとおりだった。
各commandの終了コードは0だった。

| 操作名 | 文字数 | 一致件数 | 実測した乱雑さ |
| --- | ---: | ---: | ---: |
| `requirement_candidate_check` | 27 | 1 | 3.630275354882 |
| `design_acceptance_check` | 23 | 0 | 長さの既定下限24未満のため非算出 |

【実測】契約§8.2手順3bは、除外を「正確な位置`/operation`」かつ「§6.1の固定registry操作名との完全一致」へ
限定する。完全一致しない値は除外しないことを明記し、手順4はそれ以外のID、未知key、絶対path値を除外しない。
§6.1のregistryは`design_acceptance_check`と`requirement_candidate_check`の2操作だけである。

【実測】受入条件10は同じ境界を、2操作の正例が機微停止しないことと、registry操作名に一致しない
`/operation`値が除外されないことへ接続している。

【判断】27文字側で実際に生じる高乱雑性一致は、固定公開語だけを対象とする手順3bで回避される。23文字側も
正例として同じ固定規則に含まれる。除外条件の位置、値集合、照合方法、受入反証が固定されており、実装者が
除外範囲を後決めする余地はない。v3実装中に判明した停止原因は閉じた。

## 4. 退行確認

【実測】`git diff --no-index --numstat <v3> <v4>`は16行追加・10行削除を示し、差分があるため終了コードは
期待どおり1だった。`--unified=0`で再読込みした全文差分は次だけだった。

- 見出し、契約版、supersedes、訂正根拠、訂正範囲のv4更新
- §8.2手順3bの追加
- 受入条件10を手順3bと同じ境界へ合わせる更新
- §15の次作業文の更新

【実測】v3で開始可とされた§7の書込み境界の確定点、§6.1のregistry 2操作、§2の目的縮小、§10.2の
束縛照合位置4件、§6の固定内容識別値には全文差分がなかった。

【実測】§6.1の再利用4 file、§6.2の1 file、§6.3の保護10 pathは、記載SHA-256と全件一致した。
15 pathについて`git diff --exit-code bb55a1f HEAD -- <15 path>`も差分なし、終了コード0だった。

【判断】v3からv4への変更は依頼record §2の訂正範囲に限定され、指定された既存境界に退行はない。

## 5. 必須の機械確認

【実測】内容識別値は各組を`.venv/bin/python3`で別々に照合し、すべて単独commandの終了コードで判定した。

| command／確認 | 件数 | 結果 | 終了コード |
| --- | ---: | --- | ---: |
| `find_high_entropy`：`requirement_candidate_check` | 1 | 一致、乱雑さ3.630275354882 | 0 |
| `find_high_entropy`：`design_acceptance_check` | 1 | 非一致 | 0 |
| §6.1 再利用fileのSHA-256 | 4 | 全件一致 | 0 |
| §6.2 機微情報候補検査fileのSHA-256 | 1 | 一致 | 0 |
| §6.3 保護pathのSHA-256 | 10 | 全件一致 | 0 |
| §6.1〜§6.3の15 pathと基準commit `bb55a1f`の差分 | 15 | 差分0 | 0 |

【実測】対象試験、関連試験、正規全試験は実行していない。本レビューは成果物変更を伴わない契約候補の限定再確認で、
依頼record §4が指定した必須の機械確認だけを実行した。

## 6. 範囲、Human境界、未実施、次

【実測】対象契約、製品code、既存試験、固定部品、外部systemは変更していない。レビューは依頼record §3の
鮮度検査と§4の限定再確認だけであり、全面再走査は行っていない。

【実測】契約採用、実装再開、縮小境界の採否、最終受入、外部送信は実施していない。

【判断】Human境界は維持した。本recordの`開始可`は限定再確認の完了根拠であり、契約採用や最終受入の
Human判断を代替しない。

【提案】次の一作業は、Claudeが本判定recordのcommit、変更path、判定内容を事後照合することである。
