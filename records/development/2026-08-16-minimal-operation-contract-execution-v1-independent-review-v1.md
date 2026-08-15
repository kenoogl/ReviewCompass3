# 最小運用契約実行 契約候補v1 独立確認 v1

- Reviewer model：`gpt-5.6-sol`
- reasoning effort：`high`
- 実施日：2026-08-16
- 依頼record：`records/session-handoffs/2026-08-16-g30-operation-contract-v1-review-codex-request-v1.md`
- 先行レビュー：`records/development/2026-08-15-one-requirement-feature-source-contract-v1-independent-review-v1.md`
- 対象commit：`93fa28dee6850d71279f599735b69108ea91f200`
- 対象契約：`records/task-contract/2026-08-16-minimal-operation-contract-execution-candidate-v1.md`
- 対象契約SHA-256：`1ed92a89a96550fe1ea5df74fc40fd74102694e8bfefa07b5ec0c9d09df1bb6d`
- 方法：依頼record §3の鮮度検査と§4の読取り専用定義反証
- 判定：`修正要`

## 1. 結論

【判断】固定commit `93fa28d`からの実装開始を止める。停止原因は、同じ原因の変種をまとめて2系統である。

1. 固定registryのうち`one_item_review_prepare`について、契約が前提にする呼出し形式、正常結果の安全表示、
   停止結果の形が、保護して変更しない現物と一致しない。
2. 新規fileを作成した後の書込み失敗または再読込失敗ではfileが残り得るが、契約は復旧または公開前検証の経路を
   許可能力へ含めず「停止時は実行記録fileを作成しない」と定めており、書込み境界が両立しない。

【判断】目的縮小、契約入力の機微情報候補検査の定義、6個の束縛照合位置、固定内容識別値、基準commit、必須試験は、
今回確認した範囲では停止原因にならなかった。

## 2. 開始時の鮮度検査

【実測】開始時のbranchは`main`、`git status --short`は出力なし、終了コード0だった。

【実測】`git log -1 --format=%H%n%P%n%s --name-only -- records/session-handoffs`は終了コード0で、最新の
session handoffを次のとおり特定した。

- commit：`81556e8a2ca63deb0d2ba0a29e0c2e01ba88273c`
- 親commit：`93fa28dee6850d71279f599735b69108ea91f200`
- path：`records/session-handoffs/2026-08-16-g30-operation-contract-v1-review-codex-request-v1.md`
- 件名：`Request independent review of operation contract candidate`

【実測】上記依頼recordの依頼先はCodexであり、本recordが自分宛の最新依頼recordだった。

【実測】`.venv/bin/python3`で再計算した固定入力のSHA-256は、依頼record記載値と一致した。各commandの終了コードは0だった。

| 固定入力 | 再計算値 |
| --- | --- |
| 対象契約候補 | `1ed92a89a96550fe1ea5df74fc40fd74102694e8bfefa07b5ec0c9d09df1bb6d` |
| 利用者の運用化目標 | `c5f43f6c3b8eb7bc8b9c6b6dbb57f83039009ffcfe8127a481e04b3f8c7fb42a` |

【実測】`git diff --exit-code 93fa28d HEAD -- <上記2 file>`は差分なし、終了コード0だった。開始条件は鮮度停止に
該当しなかった。

## 3. 停止原因

### 3.1 固定registryと保護対象の現物契約が一致しない

- Finding：`blocking`
- 確認段階：`scope`
- blocking類型：3「誤った合格を実証できる受入条件・検証の欠陥」および4「scope境界の破り」

【実測】新作fixtureとして、通常の非機微文字列`Novel ordinary material text that is not a secret.\n`と、
`Ordinary goal text for a new reviewer counterexample.`を実際の
`tools.reviews.one_item_review.prepare_material`へ渡した。commandは`.venv/bin/python3 -c <現物形式の照合>`、
終了コード0で、次を再現した。

- 正常結果の`material.content`に入力資料の全文がそのまま入った。
- 正常結果の`review_spec.goal`に入力した自由文がそのまま入った。
- `material.content_sha256`と`review_spec.sha256`は存在し、§10.2の正常時の束縛照合位置自体は一致した。
- `tools.reviews.one_item_review_entry.main`の実際の署名は`(argv=None)`であり、契約§6.1が全入口に固定する
  `main(arguments, *, output)`ではなかった。
- 同入口を未知操作で停止させると、終了コード2、root keyは`external_send_approved`、`reason`、`status`の3件で、
  `source`はなかった。

【実測】同じ機械照合で、残る4個の照合位置
`design.sha256`、`acceptance.sha256`、`catalog.sha256`、`candidate.sha256`は現物の正常結果に存在した。

【実測】契約§10.1は部品結果全体を`part_result`へ無変更で埋め込む一方、同節は入力自由文を実行記録へ含めないと
定める。上記の通常文字列は部品側の機微情報検査に合格して正常結果へ入り、契約どおり無変更で埋め込むと実行記録にも入る。

【実測】契約§11は`part_stopped`で部品結果の`part_reason`と`part_source`を転記すると定めるが、
`one_item_review_prepare`の停止結果には`source`がない。契約§6.1はこの入口を保護し、変更しないと定める。

【判断】一件レビュー部品を含む正例だけを通しても、入力自由文非記録、共通呼出し形式、停止結果の一意な構成を満たせない。
これは実装詳細の未決ではなく、固定した現物と契約の矛盾である。現物を契約へ合わせる修正は、保護対象を変更しないscopeを破る。

【提案】最小修正は、契約候補v2のregistryから`one_item_review_prepare`を外し、G08とG24の2操作だけで最初の縦切りを
定義することである。一件レビュー部品は、自由文を実行記録へ入れない安全な投影、`stdout`捕捉方法、停止元の固定変換を
別の後続契約で定義してから追加する。

### 3.2 停止時無作成と書込み後失敗が両立しない

- Finding：`blocking`
- 確認段階：`scope`
- blocking類型：3「誤った合格を実証できる受入条件・検証の欠陥」

【実測】契約§7は実行記録を新規作成専用で書いた後に再読込照合すると定める。§11は書込み失敗または再読込不一致を
`record_write_failed`で停止すると同時に、停止時は実行記録fileを作成しないと定める。§5.1と§7の許可能力はfile書込みを
最終名の実行記録一件に限定し、§5.2と§7は改名・削除を禁止する。§12の変更上限にも公開前検証または復旧の経路はない。

【実測】新作のOS境界反証を`.venv/bin/python3 -c <新規作成後失敗の照合>`で実行した。`O_CREAT | O_EXCL`で一時領域に
新規fileを作成してcloseした後に後段失敗を発生させると、`file_exists_after_exclusive_create=True`だった。commandの
終了コード0は、この反証を再現できたことを示す。

【判断】file作成後のwrite、close、再読込のいずれかが失敗した場合、新規作成専用だけでは作成済みfileを未作成へ戻せない。
正常例、既存file、書込み開始前の失敗だけを試験して合格しても、「停止時無作成」を誤って合格にできる。

【提案】最小修正は、最終名を公開する前にbytesを検証する一時成果と、既存fileを上書きしない原子的な公開方法を契約へ
明記し、その一時成果の作成・回収に必要な能力を変更上限と禁止事項の例外へ狭く追加することである。これを採らない場合は、
停止時無作成の保証を撤回し、作成後失敗で残り得る状態と復旧手順を明記する必要がある。

## 4. 問題がなかった定義境界

【記録】利用者の運用化目標は、最初の縦切りを「承認済み運用契約一件の下で受入済み部品一件を実行し、入力束縛を
照合し、実行記録一件を着地させる最小の導線」とする。

【実測】【判断】契約§1、§5、§12、§13.22、§15は、G30全体ではないこと、既存G30基盤5 fileを利用・変更・正式化
しないこと、候補4を完了にしないこと、縮小採用と最終受入を利用者判断に残すことを明記する。目的縮小は誤解なく固定されている。

【実測】契約§8.2は、復号後の全文字列keyと値を深さ優先・入力順で検査し、正確な
`/expected_bindings/{入力名}`にある正規SHA-256値だけを除外する。その他の64桁16進文字列、ID、未知key、絶対pathを
除外しない。§6.2の現物は既定pattern 5件を持ち、新作の5種のpattern例と高乱雑性例は全件検出された。commandの終了コードは0だった。

【判断】運用契約自体の機微情報候補検査順には、今回の停止原因と同じ類型の追加変種を確認しなかった。ただし§3.1のとおり、
機微検査を通る通常の入力自由文が、一件レビュー部品の正常結果経由で実行記録へ入る別境界は不合格である。

【実測】【判断】正準JSONの文字表現、3個の内容識別値の計算対象、正常結果の全root項目、停止理由・停止元・終了コード表は
文面上で一意に固定されている。§10.2の6個の正常時束縛照合位置は現物に存在する。停止形式は§3.1の一件レビュー部品だけが
現物と一致しない。

## 5. 固定fileと必須試験の機械確認

【実測】各組を`.venv/bin/python3`で機械照合した。

| 確認 | 件数 | 結果 | 終了コード |
| --- | ---: | --- | ---: |
| §6.1 再利用fileのSHA-256 | 6 | 全件一致 | 0 |
| §6.2 機微情報候補検査fileのSHA-256 | 1 | 一致 | 0 |
| §6.3 保護pathのSHA-256 | 8 | 全件一致 | 0 |
| §6.1〜§6.3の15 pathと基準commit `bb55a1f`の差分 | 15 | 差分0 | 0 |

【実測】依頼record §4の必須試験を、pipeやcommand連結を使わず個別に実行した。

| command | 成功件数 | 終了コード |
| --- | ---: | ---: |
| `.venv/bin/python3 -m pytest -q tests/test_one_item_review.py` | 158 | 0 |
| `.venv/bin/python3 -m pytest -q tests/test_one_design_acceptance.py` | 107 | 0 |
| `.venv/bin/python3 -m pytest -q tests/test_one_requirement_feature_source.py` | 111 | 0 |
| `.venv/bin/python3 -m pytest -q tests/test_first_review_task_contract_e2e.py` | 38 | 0 |

【判断】既存試験の合格は固定部品自体の退行がないことを示すが、新しい実行契約がその現物形式へ正しく接続できることや、
新しい書込み境界の成立は示さない。§3の反証を打ち消すEvidenceにはならない。

## 6. レビュー照合と停止

【実測】許可範囲は本判定record一件の作成と単独commitだけである。製品コード、対象契約、既存試験、G30基盤、再利用部品、
外部systemは変更していない。外部送信、実装開始、契約採用、縮小採用のHuman判断は実施していない。

【判断】Human境界は維持した。`修正要`は実装開始または候補4完了の根拠に使えない。

【提案】次の一作業は、Claudeが上記2原因だけを契約候補v2へ限定訂正し、同じ範囲の独立確認へ戻すことである。
