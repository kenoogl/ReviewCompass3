# 一件レビュー安全投影 契約候補v1 独立確認 v1

- Reviewer model：`gpt-5.6-sol`
- reasoning effort：`high`
- 実施日：2026-08-16
- 依頼record：`records/session-handoffs/2026-08-16-g02-safe-projection-v1-review-codex-request-v1.md`
- 先行レビュー：`records/development/2026-08-16-minimal-operation-contract-execution-v1-independent-review-v1.md`
- 対象commit：`b82ccf30ada56f0cb763b0741a56bcb945f10481`
- 対象契約：`records/task-contract/2026-08-16-one-item-review-safe-projection-candidate-v1.md`
- 対象契約SHA-256：`b42232fd0f6a559a680c5447845502a0947b0d96caaaddae208c8bf0c94a2f9b`
- 方法：依頼record §3の鮮度検査と§4の読取り専用定義反証だけ
- 判定：`修正要`

## 1. 結論

【判断】固定commit `b82ccf3`からの実装開始を止める。停止原因は一件だけである。契約候補§7.1は
G02 prepare経路の停止理由を「8種」と記す一方、現物で到達できる8理由に、organize経路だけで使う
`stale_material`を加えた9理由を固定集合として列挙している。実装時に8理由と9理由のどちらを採るかを
一意に決められない。

【判断】安全投影の列挙項目、自由文遮断、二つの束縛位置、固定内容識別値、保護基準、基底契約006 v4の
書込み境界と機微情報候補検査は、今回指定された範囲では停止原因にならなかった。

## 2. 開始時の鮮度検査

【実測】開始時のbranchは`main`、HEADは
`e44d2abde32085a253c76a2b7a41a1682ab104a5`、`git status --short`は出力なし、終了コード0だった。

【実測】`git log -1 --format=%H%n%P%n%s --name-only -- records/session-handoffs`は終了コード0で、
最新のsession handoffを次のとおり特定した。

- commit：`e44d2abde32085a253c76a2b7a41a1682ab104a5`
- 親commit：`b82ccf30ada56f0cb763b0741a56bcb945f10481`
- path：`records/session-handoffs/2026-08-16-g02-safe-projection-v1-review-codex-request-v1.md`
- 件名：`Request independent review of safe projection candidate`

【実測】上記依頼recordの依頼先はCodexであり、本recordが自分宛の最新依頼recordだった。

【実測】`.venv/bin/python3`で再計算した固定入力3件のSHA-256は依頼record記載値と一致した。
各commandの終了コードは0だった。

| 固定入力 | 再計算値 |
| --- | --- |
| 対象契約候補 | `b42232fd0f6a559a680c5447845502a0947b0d96caaaddae208c8bf0c94a2f9b` |
| 基底契約006 v4 | `d7b1861ccc73cb8f1c305294bf7c7e2a5fddd6ddb3fb46eab74e3204e8a2a7a1` |
| 006 v1独立確認 | `3eb9eba738171ac0f66572de1da5454377684f5ab4d4c110e85397c86657e5ca` |

【実測】`git diff --exit-code b82ccf30 HEAD -- <対象契約候補>`は差分なし、終了コード0だった。
開始条件は鮮度停止に該当しなかった。

## 3. 停止原因

### 3.1 prepare経路の停止理由集合が8理由と9理由で競合する

- Finding：`blocking`
- 確認段階：`scope`
- blocking類型：3「誤った合格を実証できる受入条件・検証の欠陥」および4「scope境界の破り」

【実測】契約候補§7.1は「理由は§6.2の8種」と記した後、
`invalid_arguments`、`invalid_path`、`invalid_schema`、`invalid_utf8`、
`sensitive_data_remaining`、`size_limit_exceeded`、`unreadable_input`、
`absolute_path_remaining`、`stale_material`の9理由を固定集合として列挙する。

【実測】新作の一時領域fixtureを実際の`read_input_files`と`prepare_material`へ渡し、前者から
`invalid_arguments`、`invalid_path`、`unreadable_input`、`size_limit_exceeded`、後者から
`invalid_schema`、`invalid_utf8`、`sensitive_data_remaining`、`absolute_path_remaining`を
それぞれ再現した。`ReviewStop`には`reason`があり、`source`はなかった。commandの終了コードは0だった。

【実測】`.venv/bin/python3`による構文木抽出では、上記8理由はprepare経路の二関数とその補助関数に存在した。
`stale_material`は`validate_results`だけに存在し、本契約が直接呼ぶ二関数には存在しなかった。
`validate_results`を使うG02の`organize`操作は契約候補§1・§5.2で範囲外である。同じ類型を全
`ReviewStop`理由へ広げて照合し、prepare範囲へ混入した他のorganize専用理由は0件だった。

【判断】8理由を正として`stale_material`を`internal_failure`へ変換する実装と、列挙した9理由を正として
`part_stopped`へ変換する実装の両方が文面の一部へ合致する。契約候補§9.5の受入例は
`sensitive_data_remaining`、`absolute_path_remaining`、`invalid_schema`の3理由であり、この二実装を
区別しないため、誤った合格が可能である。これは契約候補§10の「停止変換を固定規則から一意に決められない」
停止条件にも該当する。

【提案】最小修正は、§7.1の固定集合からprepare経路で到達しない`stale_material`だけを削除し、上記8理由を
正確な閉じた集合として記すことである。ほかの契約定義を変える必要はない。

## 4. 停止原因にならなかった定義境界

### 4.1 安全投影と束縛位置

【実測】既存fixtureにない短い通常文を材料本文、goal、criteria 2件、constraintsへ入れ、G02現物で材料を
作った後、契約候補§7.2どおりに投影した。投影のrootは7項目、`material`は3項目、`result_schema`は3項目、
`review_spec`は1項目の完全一致となり、列挙した全項目は現物に存在した。5個の自由文の出現は0件だった。
commandの終了コードは0だった。

【実測】同じ新作fixtureで、`material.content_sha256`は入力material fileの生bytesから独立計算したSHA-256と
一致し、`review_spec.sha256`はcriteriaをID順へ正規化したreview仕様の正準JSON bytesから独立計算した
SHA-256と一致した。`material_package_sha256`も、同欄を加える前のG02結果全体から再計算して一致した。

【判断】§7.2の固定allowlist投影と§7.3の二つの束縛位置は、今回の現物と一意に接続できる。

### 4.2 固定基準、基底契約006 v4との整合

【実測】§6.1〜§6.3で値が記載された19 fileのSHA-256を`.venv/bin/python3`で再計算し、19件全て一致、
不一致0件、終了コード0だった。

【実測】保護基準commit `a052312645328d7272f65aededdb74152e157c41`からHEADまで、§6.3が保護する
18 pathを`git diff --exit-code`で照合し、差分0、終了コード0だった。内容識別値が記載されていない
`tests/test_first_review_task_contract_e2e.py`もこの18 pathへ含めた。

【実測】操作名`one_item_review_prepare`は23文字だった。現行の既定pattern 5件と高乱雑性検査には一致せず、
契約006 v4 §8.2手順3bは追加後の固定registry操作名を`/operation`位置だけで除外するため、候補§9.6と矛盾しない。

【判断】変更対象を実行核と対象試験の2 fileに限定し、G02核を直接呼ぶ定義は、006 v4の停止表、二段書込み境界、
保護対象を変更しない境界と両立する。§3.1の一箇所を直せば、理由転記、`part_source: none`、
`sensitive_data_remaining`だけ部品終了コード3、他は2、実行器終了コード5という変換に後決め要素は残らない。

## 5. 必須試験

【実測】依頼record §4の必須試験を、pipeやcommand連結を使わず個別に実行した。

| command | 成功件数 | 終了コード |
| --- | ---: | ---: |
| `.venv/bin/python3 -m pytest -q tests/test_operation_contract_run.py` | 67 | 0 |
| `.venv/bin/python3 -m pytest -q tests/test_one_item_review.py` | 158 | 0 |

【判断】既存試験の合格は基底実行器とG02現物の退行がないことを示すが、§3.1の契約文面の競合を解消する
Evidenceにはならない。

## 6. レビュー照合と停止

【実測】許可範囲は本判定record一件の作成と単独commitだけである。製品コード、対象契約、既存試験、基底実行器、
再利用部品、外部systemは変更していない。外部送信、実装開始、契約採用、縮小境界のHuman判断は実施していない。

【判断】Human境界は維持した。`修正要`は実装開始の根拠に使えない。

【提案】次の一作業は、Claudeが§7.1から`stale_material`だけを除く最小訂正を行い、同じ範囲の独立確認へ戻す
ことである。
