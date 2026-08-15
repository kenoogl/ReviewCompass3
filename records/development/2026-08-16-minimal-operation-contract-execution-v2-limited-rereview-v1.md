# 最小運用契約実行 契約候補v2 限定再確認 v1

- Reviewer model：`gpt-5.6-sol`
- reasoning effort：`high`
- 実施日：2026-08-16
- 依頼record：`records/session-handoffs/2026-08-16-g30-operation-contract-v2-limited-rereview-codex-request-v1.md`
- 先行レビュー：`records/development/2026-08-16-minimal-operation-contract-execution-v1-independent-review-v1.md`
- 対象commit：`dd5375ab52eb787252d6c814a8a18378d8e3cabb`
- 対象契約：`records/task-contract/2026-08-16-minimal-operation-contract-execution-candidate-v2.md`
- 対象契約SHA-256：`927965f9502c0762c0ba289968d37d16237ae0ef433f15c2ac53cc8dacd94090`
- 方法：依頼record §3の鮮度検査と§4の限定再確認だけ
- 判定：`修正要`

## 1. 結論

【判断】固定commit `dd5375a`からの実装開始を止める。v1停止原因1のregistry縮小は閉じたが、停止原因2の
書込み境界には、hard linkで最終名を公開した後の一時名削除失敗が未定義のまま残る。停止原因はこの1件だけである。

【判断】v1で問題なしとされた目的縮小の固定、§8.2機微情報候補検査、§10.2の束縛照合位置4件、固定内容識別値、
基準commit、必須試験には、v2差分による退行を確認しなかった。

## 2. 開始時の鮮度検査

【実測】開始時のbranchは`main`、`git status --short`は出力なし、終了コード0だった。

【実測】`git log -5 --format='%H %P %s' -- records/session-handoffs`は終了コード0で、最新のsession handoffを
次のとおり特定した。

- commit：`493c524d5680870aa50348fdcc52f4b5d6e60fdd`
- 親commit：`dd5375ab52eb787252d6c814a8a18378d8e3cabb`
- path：`records/session-handoffs/2026-08-16-g30-operation-contract-v2-limited-rereview-codex-request-v1.md`
- 件名：`Request limited re-review of operation contract v2`

【実測】依頼先はCodexであり、本依頼recordが自分宛の最新依頼recordだった。

【実測】`.venv/bin/python3`で再計算した依頼record §2の3 fileのSHA-256は、記載値と全件一致した。各commandの
終了コードは0だった。

| 固定入力 | 再計算値 |
| --- | --- |
| 対象契約候補v2 | `927965f9502c0762c0ba289968d37d16237ae0ef433f15c2ac53cc8dacd94090` |
| v1独立確認 | `3eb9eba738171ac0f66572de1da5454377684f5ab4d4c110e85397c86657e5ca` |
| 直前版契約v1 | `1ed92a89a96550fe1ea5df74fc40fd74102694e8bfefa07b5ec0c9d09df1bb6d` |

【実測】`git merge-base --is-ancestor dd5375a HEAD`と、対象契約についての
`git diff --exit-code dd5375a HEAD -- <対象契約>`は、ともに終了コード0だった。対象契約は固定commitの内容から
変わっていない。鮮度停止には該当しなかった。

## 3. 訂正1：registry縮小

【実測】v2のregistry、運用契約の`operation`、入力key、束縛照合表、受入条件1・18・19・21はG08とG24の
2操作へ縮小されている。G02の2 fileは§6.3の保護対象へ移り、§5.2は安全な投影、標準出力の捕捉、停止元の
固定変換を後続契約で定義してから追加すると明記する。

【実測】`.venv/bin/python3 -c <2入口の現物照合>`は終了コード0で、次の全件が一致した。

- 2入口の署名はともに`(arguments=None, *, output=None)`だった。
- 正常結果2件は終了コード0で、入力fileの絶対pathを含まなかった。必須試験では両部品の入力自由文が
  正常結果へ含まれないことも合格した。
- 停止結果2件は終了コード2で、`reason`、`source`を持つ固定形だった。
- 内部例外注入2件は終了コード4で、例外本文を含まず`internal_failure`となった。

【判断】一件レビュー部品の呼出し形式、自由文埋め込み、停止形式の現物不一致は、registryからの除外と後続条件の
明記により閉じた。残る2入口は契約§6.1の共通形と一致する。

## 4. 訂正2：書込み境界に残る停止原因

### 4.1 公開後の一時名削除失敗が定義されていない

- Finding：`blocking`
- 確認段階：`scope`
- blocking類型：3「誤った合格を実証できる受入条件・検証の欠陥」

【実測】契約§7手順3は、一時名から最終名へのhard link作成後に一時名を削除する。§7手順4が定義する回収は、
書込み・照合・公開のいずれかが失敗した場合だけであり、hard link成功後の一時名削除失敗を含まない。§11の
`record_write_failed`行も「回収の失敗」までしか一意に接続せず、公開後削除の失敗時に返す結果と残留状態を定めない。

【実測】新作のOS境界反証を`.venv/bin/python3 -c <公開後削除失敗の照合>`で実行した。検証済みbytesを持つ一時名から
最終名へhard linkを作成し、その直後の`unlink`へ失敗を注入すると、次を全件再現した。commandの終了コードは0だった。

- `unlink_failed=True`
- `final_exists=True`
- `partial_exists=True`
- 両名のinodeとbytesは同一

【判断】この状態では、§13.16の「公開後は最終名一件だけ」を満たさない。停止として扱うと、§11の「停止時は最終名を
作成しない」を満たさない。正常として扱うか停止として扱うか、残る2名をどう報告・回復するかは実装者の後決めになる。
作成・書込み・照合・hard link公開前失敗の回収定義だけを試験しても、この境界を誤って合格にできる。

【判断】同じ類型の書込み後失敗を、作成、書込み、照合、公開、公開前回収、公開後削除の位置で確認した。v2は公開前の
失敗と回収失敗を一時名だけの残留へ限定したが、公開後削除だけが残った追加変種である。

【提案】最小修正は、hard link成功を公開の確定点としたうえで、その後の一時名削除失敗について、返す状態・終了コード、
最終名と一時名の残留、再開または回復境界を§7と§11へ一意に追加し、§13.16・16bと§14を同じ定義へ合わせることである。
「停止時は最終名未作成」または「公開後は最終名一件だけ」のどちらかを例外なしで残す場合は、現在のhard link後削除の
二操作では両立しないため、公開方式を契約改定する必要がある。

## 5. 退行確認

【実測】v1とv2の全文差分は、見出しの版・状態・supersedes・訂正根拠・訂正範囲・利用者判断、registryの2操作への
縮小、G02の後続条件と保護対象への移動、§7の二段書込み、これらに対応する§8.3、§10.2、§11、§13、§14、§15の
更新に限定されていた。依頼record §2が宣言する訂正範囲外の本文変更はなかった。

【実測】§6.1の再利用4 file、§6.2の1 file、§6.3の保護10 pathは、記載SHA-256と全件一致した。15 pathについて
`git diff --exit-code bb55a1f HEAD -- <15 path>`も差分なし、終了コード0だった。

【判断】目的縮小の固定、§8.2機微情報候補検査、§10.2の4照合位置、固定内容識別値、基準commit、必須試験には、
今回の限定再確認で退行を確認しなかった。訂正2の停止原因は§4.1だけである。

## 6. 必須の機械確認

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

【実測】追加の2入口照合は、最初の2回が一時directoryの`/var` symlink表現を未解決のまま入力したため、入口が
非追跡pathとして正しく拒否し、確認commandは終了コード1になった。製品不具合ではなく確認入力の誤りだった。pathを
`/private/var`へ解決して再実行すると、署名2件、正常2件、停止2件、内部例外注入2件の全件一致、終了コード0だった。

## 7. 範囲、Human境界、次

【実測】製品code、対象契約、既存試験、固定部品、外部systemは変更していない。外部送信、実装開始、契約採用、
縮小採用、最終受入のHuman判断は実施していない。

【判断】Human境界は維持した。`修正要`は実装開始または候補4完了の根拠に使えない。

【提案】次の一作業は、Claudeが§4.1の公開後削除失敗だけを契約候補v3へ限定訂正し、同じ範囲の限定再確認へ戻す
ことである。
