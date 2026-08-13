# 第3段 G07赤試験宣言契約の限定修正 独立完了レビュー v1

- 記録日：2026-08-13
- 判定：`verified`
- 対象Issue：`ISSUE-TEST-GROWTH-STATE-PINNING-001`
- 基準commit：`8608df20245f6d51e3557f0d00644f244631a202`
- 作業票commit：`5ee4a79e71032cf048f9da3913b7a45948c3de9e`
- 結果commit：`793d2e836621e2395eb770ffe4809e8bd1120a29`
- 実行環境：Python 3.13.14、pytest 8.4.2

## 1. 固定対象と変更範囲

【実測】作業票
`docs/development/2026-08-13-stage3-g07-declaration-red-contract-correction-bootstrap-work-ticket-v1.md`
のSHA-256は`f08d004b8a782cf1da7583f9511bc52f21f516f1feece4fddfba38a9ffee0800`、実施Evidence
`records/development/2026-08-13-stage3-g07-declaration-red-contract-correction-evidence-v1.md`
は`a0bec84823f86b9d46da05bd792d7499e9417f99d70b4b602b02785f3187fc46`、修正後の現行レビュー手順
`docs/development/work-review-protocol.md`は`e768d32ed0a2b95fced5a744dd9b98734a2bc3b0c644f415af9dd508c5223d29`、
修正後試験`tests/test_declaration_red_map_check.py`は
`6ed4d7dd37a792c545f246d98accfd64e4c0e4ad1c08a9f107059e66cae8e09d`で、固定値と全件一致した。
基準、作業票、結果の三commitもGit物体として実在した。

【実測】基準commitから結果commitまでの変更は、作業票一件、現行レビュー手順、既存試験一件、実施Evidence一件の
計四pathだけだった。作業票commitから結果commitまで、および結果commit自体の変更は、現行レビュー手順、既存試験、
実施Evidenceの三pathだけだった。レビュー開始時の作業ツリーはcleanで、結果commitから現在まで差分はなかった。

## 2. 現行レビュー手順の確認

【実測】現行レビュー手順の「宣言から赤試験への対応表を作る作業」の一つの規定内に、次の条件がすべて入っていた。

- `red_verification_contract.version`を2にする。
- `red_now: true`の各試験へ`expected_failure_reason`、すなわち予定した失敗理由を持たせる。
- `verify_red=True`と`minimum_red_contract_version=2`を同時に指定する。
- 結果全体の`status`が`passed`であることを要求する。
- `execution_errors`、`reason_mismatched`、`mismatched`、`unknown`がすべて0件でなければcommitしない。

【実測】この規定部分に必要な十個の語句があることを機械照合し、欠落は0件だった。文書全体に
`minimum_red_contract_version=1`は0件で、旧方式を現行の完成経路として選べる別の指示はなかった。後段の確認表は
実行照合を行ったかを尋ねる短い確認欄であり、上記の必須条件を置き換える記述ではない。

【判断】現行レビュー手順は、版2、予定失敗理由、実行照合、最低版2、成功状態、四種類の所見0件を一体で要求している。
曖昧な旧方式へ戻る読み方は確認できなかった。

## 3. 試験識別子と関連試験

【実測】基準commitと結果commitから`tests/test_declaration_red_map_check.py`を別々に収集した。試験識別子は双方9件で、
集合も完全一致した。構文木による照合でも試験関数名の集合は同一9件で、新しい試験関数は増えていなかった。

【実測】結果commitと同じ状態で、次をそれぞれ単独の試験commandとして実行した。

- G07追加8件：8件成功、終了コード0。
- 専用四file：22件成功、終了コード0。
- 混在二fileの関連7件：7件成功、終了コード0。
- 現行レビュー手順への導線試験一件：1件成功、終了コード0。

【実測】混在二fileの関連7件について、最初に実在しない試験名を指定したため収集前に終了コード4となった。
これはreviewerの入力誤りである。直後に`--collect-only`で実在する試験識別子を機械収集し、検査処理を直接呼ぶ
2件と5件を選び直して単独実行し、上記の7件成功、終了コード0を得た。製品、試験、Evidenceは変更していない。

## 4. 二つの空条件への独立した変異確認

【実測】実施時の複製を使わず、結果commitからリポジトリ外へ二つの別複製を作った。一方では完全範囲の空宣言を
拒否する分岐だけを無効にし、もう一方では空の試験file一覧を拒否する分岐だけを無効にした。同じ既存試験
`test_complete_scope_with_no_declarations_is_rejected`を各複製で単独実行した結果は、どちらも1件失敗、終了コード1だった。

【実測】各失敗は、他方の条件による単なる`status: failed`ではなく、無効にした側に固有の所見が存在しないことを
既存試験が検出した結果だった。

【判断】変更前のように別条件の不合格だけで成功する経路は閉じている。試験数を増やさず、同じ一試験が二つの
拒否条件を個別に守るという作業票の目的を満たす。

## 5. 別入力による準備失敗の反証

【実測】実施Evidenceの入力を転記せず、`tests/test_alternate_probe.py::test_signal_contract`という別名、
`ALT-RED-777`という別宣言、`deliberate semantic gap sentinel`という別の予定失敗理由を持つ対応表を、
リポジトリ外に作った。模擬実行器は`ModuleNotFoundError: independent_missing_module`という準備失敗を返した。

【実測】版を持たない旧方式を`verify_red=True`だけで照合すると、`status: passed`、`verified: 1`、
`execution_errors: 0`となり、準備失敗を予定した赤試験として誤合格した。同じ意味の入力を版2にし、予定失敗理由、
`verify_red=True`、`minimum_red_contract_version=2`を与えると、`status: failed`、`verified: 0`、
`execution_errors: 1`となった。照合script自身の終了コードは0だった。

【実測】検査処理`tools/development/declaration_red_map_check.py`のGit物体識別値は基準commitと結果commitの双方で
`20bcb25092803401f5a97fed8f662c2f74bf70f0`で同一だった。

【判断】旧方式の互換動作は変えていない。既存の版2処理は別入力でも準備失敗を拒否し、現行レビュー手順がその版2を
必須にしたため、通常の完成経路で旧方式の誤合格へ戻らない。

## 6. 変更しなかった範囲

【実測】`records/`配下のJSONを結果commitから独立列挙すると、宣言対応表は21件、内訳は版1が19件、版2が2件だった。
全21件の内容は基準commitと結果commitでバイト単位に同一だった。

【実測】構文木で、専用四fileの22件と混在二fileの関連7件、計29件を固定した。変更対象一件を除く28件は、
基準commitと結果commitで構文木が全件同一だった。検査処理、`config/`、`.reviewcompass/workflow/`、`AGENTS.md`、
立て直し計画v5、`TODO_NEXT_SESSION.md`も基準commitと結果commitで差分0だった。

## 7. 試した反証

1. 【実測】空宣言と空試験file一覧の拒否分岐を別々に無効化し、既存一試験が別条件の不合格だけで成功しないかを試した。
   各変異で固有所見の欠落を検出して1件失敗したため、反証は不成立だった。
2. 【実測】実施Evidenceと異なる名前、宣言、予定理由、準備失敗を使い、版2も誤合格しないかを試した。
   旧方式だけが誤合格し、版2は準備失敗1件として拒否したため、反証は不成立だった。
3. 【実測】現行レビュー手順の同じ節または別節に、版2の必須条件を弱める指示がないかを検索した。
   最低版1の指定と旧方式を完成経路にする記述は0件で、反証は不成立だった。

## 8. 判定、止める指摘、報告不一致、利用者承認境界

【判断】判定は`verified`。承認済み案Aの二file限定修正は、旧方式の互換性を変えず、現行レビュー手順を既存版2へ
接続し、既存一試験の入力を分離した。申告された変更範囲、件数、試験結果、変異結果、不変範囲は独立照合と一致した。

【判断】止める指摘は0件。

【判断】報告不一致は0件。レビュー中の実在しない試験名指定はreviewerの入力誤りとして上記3節へ分離し、
正しい識別子の再収集と単独再実行で結果を確認した。実施Evidenceの報告不一致ではない。

【判断】利用者が2026-08-13に承認した案Aの境界を維持した。G07追加8件を削除せず、新しい試験、検査器、台帳、
入口を追加せず、検査処理の既定、過去の対応表、他試験を変更していない。本レビューは意味変更の再承認、
第3段完了、次群開始を代行しない。

## 9. 未実施

【未実施】レビュー記録以外のリポジトリ内fileの作成・変更、製品コード、検査処理、設定、対応表、台帳、AGENTS、
計画、TODOの変更、全試験、外部送信、Claude実行、全401件または別群への拡張、新しい検査器・台帳・強制関門の提案、
意味変更の再承認、第3段完了判断、次群開始は行っていない。一時複製、変異、別入力、照合scriptはすべて
リポジトリ外へ置いた。
