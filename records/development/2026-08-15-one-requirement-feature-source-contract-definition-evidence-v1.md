# 一件の要求・機能区分・出典対応 契約定義証拠 v1

- 実施日：2026-08-15
- 対象：候補3「G24の要求固定・機能分割・由来追跡」
- 作業範囲：作業契約候補の根拠作成だけ。契約採用、実装、既存試験変更、要求昇格は行わない
- 観測開始commit：`25bed5c`

「内容識別値」は、内容の変化を機械検出するためSHA-256で計算した値である。

## 1. 目的と判断基準

【記録】次製品候補は、固定した要求資料から要求、機能区分、出典との対応を一件分作り、全入力の採否を示し、
要求から出典へ戻れ、暫定文書を正式要求へ自動昇格しないことを完了条件としている。

【判断】自由文から正しい要求を機械的に発明することは本候補の決定的処理へ含めない。利用者または別の文章作成処理が
用意した構造化候補について、次の三点だけを製品責務とする。

1. 固定した出典一覧の全件を、採用または理由付き不採用へ割り当てる。
2. 要求の本文と各一覧項目を一つずつ義務として識別し、採用出典へ結ぶ。
3. 要求が明示した一つの機能IDと一致することを確認し、結果を未昇格・人の判断待ちとして返す。

判断基準は、欠落・重複・未定義参照を成功にしないこと、意味を補わないこと、入力内容や絶対pathを表示しないこと、
暫定資料または既存コードの存在だけで要求権限を与えないことである。

## 2. 既存G24の機械抽出

目録がG24へ割り当てた実装5 fileは次のとおりである。

| path | 行数 | SHA-256 | 公開処理 | 作用 |
| --- | ---: | --- | --- | --- |
| `tools/requirements/boundary_relations.py` | 143 | `31ae6b8edfde022300a817ec3d9d553ddb3f64d71a92a3d95c35e01a8e40e869` | `validate_boundary_relations` | 渡された値の検査と内容識別値計算 |
| `tools/requirements/feature_partition.py` | 239 | `0796d436b7f6c3e075b998f1d80451ea59d3cb3cc6b77e6ef3084f9ffbecec2a` | `validate_feature_partition` | 渡された値の検査と内容識別値計算 |
| `tools/requirements/fixed_inputs.py` | 249 | `60cfdef9e5d506fcb9519a00a02e83ed379f87a290aa34a50051d716c0354c9b` | `verify_fixed_inputs` | file読取り、JSON復号、内容識別値計算 |
| `tools/requirements/requirement_batch.py` | 216 | `2e91889620ae18e2b49b856939d07102429b9d07d24b707fcd9d4b1ecb6f3986` | `validate_requirement_batch` | 渡された値の検査と内容識別値計算 |
| `tools/requirements/source_trace.py` | 587 | `7919f0baac5eabac3bb937fbb9264193c4ad31735a78cba4b07207f52fd282b3` | `validate_requirement_sources`、`validate_obligation_sources`、`validate_atomic_obligation_sources` | 渡された値の検査と内容識別値計算 |

【実測】5 fileの合計は1,434行である。正式な命令入口はなく、repository内の呼出しは関連試験だけだった。
成果物JSONから関数名を説明用文字列として参照する箇所はあるが、製品実行経路ではない。

関連試験は次の5 file、合計863行だった。

1. `tests/test_requirements_feature_partition.py`
2. `tests/test_requirements_fixed_inputs.py`
3. `tests/test_requirement_boundary_relations.py`
4. `tests/test_requirements_source_trace.py`
5. `tests/test_requirements_batch.py`

単独command：

`.venv/bin/python3 -m pytest -q tests/test_requirements_feature_partition.py tests/test_requirements_fixed_inputs.py tests/test_requirement_boundary_relations.py tests/test_requirements_source_trace.py tests/test_requirements_batch.py`

- 終了コード：0
- 結果：59件成功
- 失敗：0件

【実測】5実装のうち4 file、関連5試験のうち4 fileは先頭で`provisional`、`non-normative`、
`promotion_required`を宣言する。境界関係の実装と試験は同じ宣言を持たないが、現行実行入口も権限接続もない。

## 3. 上流資料の一致と不一致

### 3.1 旧第4段の固定入力と成果物

【実測】`records/requirements/fixed-input-verification.json`は13入力を列挙する。現行fileへ既存
`verify_fixed_inputs`を再実行すると`ready`、13件、相違0件、検証内容識別値
`0a3eeba8c43ac80a700ffb7fee902f7428e7ee817eccae917b5f6866437c55a0`だった。

【実測】旧第4段の完了記録は37要求、9機能、47エッセンス、464原子義務を記録する。一方、作業計画、固定入力、
機能分割、要求束、出典対応、利用者承認、完了記録はいずれも`provisional`、`non-normative`、
`promotion_required`のままである。

### 3.2 現行の要求権限

【記録】2026-08-03の人の判断は、統一候補内の50 Requirement definitionを現行の単一格納形式として昇格した。
同じ判断は、要求本文、受入真偽、現行計画、製品実装、非機能要求と先送り判断を承認範囲外と明記する。

【実測】`tools/requirements/artifact_layout.py`の現行解決処理へ権限束v2を渡すと、終了コード0相当で
`effective`、要求ID 50件、束の内部内容識別値
`79a69d921bb00eb2b321e3d1adb073b88a527eb938398d1813567009255bd688`を返した。
権限束v2は個別定義50件、判断1件、証拠1件を参照し、旧形式への結び付けは0件である。

【判断】旧37件の成果物は履歴と検査候補として保持するが、G24製品が正式要求として自動採用してはならない。
現行50件の権限束は「どの格納物が現行か」を決める入力にはなるが、要求本文の妥当性または新しい要求候補の採用を
自動決定する根拠にはならない。

## 4. 反証

### 4.1 シンボリックリンク追跡

【実測】一時root内に通常fileと、それを指す別名のシンボリックリンクを作り、別名のpathと通常fileの正しい
SHA-256を`verify_fixed_inputs`へ渡した。結果は`ready`、相違0件だった。

【判断】既存処理は`Path.resolve()`の後に読み、入力rootから各要素を非追跡で開かない。事前確認後のpath差替えも
閉じないため、製品の安全読取りとして再利用しない。

### 4.2 真偽値と整数の混同

【実測】JSONの`approved`を整数`1`とし、期待値を真偽値`true`とした固定入力表明を実行すると、結果は
`ready`、相違0件だった。

【判断】Pythonの値比較で`true`と`1`を同値とするため、権限または承認の表明検査へ再利用しない。

### 4.3 未処理文字例外

【実測】`requirement_batch.validate_requirement_batch`へ単独サロゲート文字を要求本文として渡すと、
契約固有の停止ではなく`UnicodeEncodeError`が発生した。

【判断】既存4検査は入力件数、文字長、Unicode scalar value、JSON同名項目、安全表示、正式命令入口を一組で
閉じていない。既存試験59件の成功だけでは製品境界を満たさない。

## 5. 実装方法の3案

| 案 | 内容 | 単純さ・時間・資源 | 頑健さ | 変更範囲・保守・戻しやすさ | 判断 |
| --- | --- | --- | --- | --- | --- |
| A 既存機能だけ | 呼出し側がPython値を用意し、既存5検査を順に呼ぶ | 新規実装0、処理時間と記憶量は入力件数に比例 | 正式入口、安全読取り、全出典の採否、未昇格表示が一組にならない | 変更0だが製品目的未達 | 不採用 |
| B 既存5 fileを正式化 | `fixed_inputs`を入口にして他4検査を接続する | 接続は短いが、反証3件と上限・表示を全面修正する | 旧37件の暫定構造と危険な読取りを製品へ持ち込む | 既存5 file・5試験・旧成果物へ広く影響し戻しにくい | 不採用 |
| C 一件用の専用処理 | 出典一覧JSON一件と要求候補JSON一件だけを安全に読み、全採否・全義務対応・機能一致を検査する | 二入力各256 KiB、出典・義務各256件以下で上限固定 | 意味推測をせず、未定義・未被覆・自動昇格を閉じて停止できる | 新規核・入口・試験・実行名だけ。既存G24と現行要求権限を変えず戻しやすい | 推奨 |

【提案】案Cを作業契約候補にする。既存G08で受け入れ済みの二file安全読取りを再利用し、G08自体は変更しない。
G08の停止元`design`と`acceptance`はG24入口で`catalog`と`candidate`へ閉じて読み替え、例外本文は表示しない。

## 6. 最小製品境界

【提案】入力は同じ明示root内の異なる通常JSON file二件に限定する。

1. 出典一覧：安全な出典ID、内容SHA-256、申告状態`effective | approved_context | candidate | historical`。
2. 要求候補：安全な候補ID、一つの機能、一つの要求、全出典の採否と理由、要求内の全原子義務から採用出典への対応。

要求の原子義務は本文一件と、`inputs`、`outputs`、`stop_conditions`、`recovery_conditions`、
`preserved_artifacts`、`acceptance_criteria`、`non_goals`の各項目である。全出典はちょうど一度採否を持ち、
採用出典は少なくとも一義務に使われ、不採用出典は義務へ結ばない。

【提案】正常出力は入力自由文を表示せず、候補・機能・要求・出典の安全なID、件数、内容識別値、採否、
出典対応の被覆、人の判断一覧だけを返す。申告状態が何であっても`not_promoted`と
`pending_human_decision`を固定し、入力file、既存権限束、directory名、既存コードの存在から承認を推測しない。

【判断】実際の出典本文の意味確認、要求文の起草、要求本文の妥当性、出典一覧に記載した申告状態の真実性確認、
複数要求間の機能分割と境界関係、要求権限束への登録は範囲外である。この限界を出力と作業契約へ残す。

## 7. 影響と未実施

【判断】この境界なら、一件の構造化要求候補について「何を採用し、各義務がどの固定出典へ戻り、どの機能に属するか」を
機械確認できる。自由文から要求を発明せず、旧37件または暫定資料の自動昇格も起こさない。

【未実施】作業契約候補の採用、実装、コード・試験・配布設定変更、既存G24変更、現行50要求変更、要求昇格、
実利用者資料の読込み、外部送信、保存は行っていない。
