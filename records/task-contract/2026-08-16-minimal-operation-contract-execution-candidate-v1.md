# 最小運用契約実行 作業契約候補 v1

- 契約ID：`TC-RC3-PRODUCT-MINIMAL-OPERATION-CONTRACT-EXECUTION-006`
- 契約版：1
- 契約種別：製品処理・G30の最初の縦切り
- 状態：`candidate_pending_independent_review_and_human_approval`
- 作成日：2026-08-16
- 直前の製品契約：`TC-RC3-PRODUCT-ONE-REQUIREMENT-FEATURE-SOURCE-005`（受入済み）
- 利用者判断：2026-08-16の運用化目標の指示と、G30契約定義への着手指示
- 実装状態：未開始
- 危険度：高
- 危険の理由：本repositoryで初めてfile書込みを持つ製品処理であり、入力へ機微情報が含まれ得る
- 内容識別値：本候補固定後、独立確認と利用者判断記録から参照する

「作業契約」は、一つの仕事の目的、入力、範囲、許可操作、期待結果、確認方法、停止条件を実装前に固定する約束である。
「運用契約」は、利用者が承認して用意する、部品一件の一回実行を指示する入力JSON一件である。
「実行記録」は、一回の実行の契約・部品結果・入力束縛を結び、人の判断待ちを示す出力JSON一件である。
「正準JSON」は、key昇順、区切り前後の空白なし、UnicodeをUTF-8の文字として保持する固定表現である。

## 1. 現行G30での位置

【記録】上位G30は、承認済みの作業契約一件を検査し、実行計画、確認、判断記録までを小さく接続する候補である。
既存基盤`tools/task_contract/`5 fileは第4段の境界により正式利用を保留中である。

【判断】本契約はG30全体ではない。**承認済み運用契約一件の下で、受入済み部品一件を一回実行し、実行記録一件を
着地させる最初の縦切り**である。

- 既存G30基盤5 fileの正式化・変更・接続は本契約で行わない。
- 実行計画の生成、複数手順の連鎖、状態管理、定期実行は本契約で行わない。
- 本契約の実装受入だけでは候補4を完了にしない。
- この縮小境界を採るかは、独立確認後に利用者が契約採用と同時に判断する。

## 2. 目的

利用者が承認して用意した運用契約JSON一件について、自由文の意味を補わず、次を決定的に行う。

1. 運用契約の形式、機微情報候補、操作名、絶対path、入力束縛宣言を検査する。
2. 固定registryの受入済み部品一件を同一process内で一回実行する。
3. 部品結果が報告する内容識別値と運用契約の入力束縛宣言を照合する。
4. 契約・部品結果・束縛を結んだ実行記録一件を、指定output rootへ新規fileとして着地させ、同じ内容を標準出力へ返す。
5. 結果の採否と後続判断を人の判断として残す。

部品の検査内容そのものは各部品の受入済み契約が定義し、本契約は再定義しない。

## 3. 権威、証拠、上流

| 役割 | path | SHA-256 |
| --- | --- | --- |
| 利用者の運用化目標 | `records/development/2026-08-16-accepted-parts-operationalization-goal-v1.md` | `c5f43f6c3b8eb7bc8b9c6b6dbb57f83039009ffcfe8127a481e04b3f8c7fb42a` |
| 次製品作業の候補一覧 | `records/development/2026-08-15-post-safe-storage-next-product-work-candidates-v1.md` | `bcb4ba2947e32254edc547068728fa580bc6b7919fa0f04d9b9353ab6c7899ba` |
| 現行開発方針 | `docs/development/2026-08-02-development-policy.md` | `e3e6b0d2c7a1265f7cde2c2e00cc888f43d63ce0d1945c300b2b2e5f7730b559` |
| 直前製品の受入判断 | `records/development/2026-08-16-one-requirement-candidate-consistency-check-product-acceptance-decision-v1.md` | `dd9edcfd5895c143f7c83c05dcc2df986d36d066030782a5577d534071866fd8` |
| G30目録 | `records/development/2026-08-14-stage4-product-code-and-task-contract-input-inventory-evidence-v1.md` | `c55367fc6b8f72f7041612cedc11d609b359909156f619fcb72e6d72bd33e72a` |

【判断】`source_requirement_ids`は空とする。運用契約と実行記録を正式要求・正式Workflow stateへ昇格しない。

## 4. 実装方法の3案

| 案 | 内容 | 単純さ・資源 | 頑健さ | 変更範囲・保守 | 判断 |
| --- | --- | --- | --- | --- | --- |
| A 既存機能だけ | 手順書を書き、利用者が各CLIを手で直列実行する | 新規実装0 | 手順飛ばし・転記誤りを機械で防げず、契約・結果・判断が結ばれない | 変更0だが目的未達 | 不採用 |
| B 既存G30基盤の一括正式化 | `tools/task_contract/`5 fileへ実行registryを接続する | 接続は短いが5 file全体の正式化が必要 | 過去に管理基盤の拡大で製品本線が停止した経緯と第4段の保留境界に抵触する | 保留中5 pathへ広く影響 | 不採用 |
| C 狭い専用実行器 | 運用契約一件を検査し、受入済み部品入口を同一processで呼び、実行記録一件だけを新規作成する | 入力件数に比例し上限固定 | 意味推測をせず、上書き・連鎖・状態を持たない | 新規核・入口・試験・実行名だけ | 推奨 |

【提案】案Cを本縦切りの採用候補とする。既存G30基盤の扱いは別の後続契約で扱う。

## 5. 範囲

### 5.1 範囲内

- 一つの運用契約JSON一件（262,144 bytes以下）を安全に読む。
- 操作は§6.1の固定registry 3件だけとする。
- 部品入口を同一process内の関数呼出しで一回実行し、部品の終了コードと結果JSONを受け取る。
- 部品結果が報告する内容識別値を、運用契約の`expected_bindings`と照合する。
- 実行記録一件をoutput rootへ新規fileとして書き、同じbytesを標準出力へ返す。

### 5.2 範囲外

- 運用契約・部品入力の作成または自動修正、雛形生成、意味の妥当性の推測。
- 複数操作の連鎖、実行計画の生成、再試行、並列実行、定期実行、状態管理、進捗表示。
- G02の`organize`操作、G25取り出し、安全保存との統合、暫定pipeline（bootstrap／egress）との接続。
- 既存G30基盤5 fileの利用・変更・正式化。
- 既存fileの上書き・削除・改名、directory作成、出力root外への書込み。
- 通信、外部送信、外部process、subprocess、Git、環境値の解決、認証、時刻取得、乱数。
- 要求権限束への登録、正式昇格、最終採否。

## 6. 固定再利用部品と保護基準

### 6.1 実行registry（受入済み部品の入口）

registryは次の3操作へ固定する。各入口は`main(arguments, *, output)`形式の受入済み関数であり、変更しない。
部品の呼出しは同一process内で行い、subprocessを使わない。

| 操作名 | 入口 | 固定argv形 |
| --- | --- | --- |
| `one_item_review_prepare` | `tools.reviews.one_item_review_entry.main` | `prepare --input-root <root> --material <path> --review-spec <path>` |
| `design_acceptance_check` | `tools.design.one_design_acceptance_entry.main` | `check --input-root <root> --design <path> --acceptance <path>` |
| `requirement_candidate_check` | `tools.requirements.one_requirement_feature_source_entry.main` | `check --input-root <root> --catalog <path> --candidate <path>` |

再利用fileの内容識別値を次へ固定する。実装開始前と完了時に一致を確認する。

| path | SHA-256 |
| --- | --- |
| `tools/reviews/one_item_review.py` | `de658b6e96b804af393d106cbc11c39d7452e9cb54c24c5157853bc5dcd9ad57` |
| `tools/reviews/one_item_review_entry.py` | `92a770583b14728b5f6606a851357efb27a19fdba11d07fecd12d941f633c390` |
| `tools/design/one_design_acceptance.py` | `b3af7fdf254b21e5d368f2a02cf2aba23a86233a67b4120e7c2b39a3fd4a5c14` |
| `tools/design/one_design_acceptance_entry.py` | `7535aa6652514c6ce4dfd31facd2640944a356ddc04802b0df8ae63a9bec9823` |
| `tools/requirements/one_requirement_feature_source.py` | `725c886a97bba63fc6d9d5c0d23a5fdc8e67f86eda2752ae587093c9bcdd14d7` |
| `tools/requirements/one_requirement_feature_source_entry.py` | `db702231fbf179a16c2742e1335d1c7f8198743baae2263ee2b1844e09ca7bd6` |

### 6.2 機微情報候補検査

`tools/session_logs/redaction.py`、SHA-256
`aa49774a447d84422ec885a908bb52c7a3732eb67ddb53dcc1c03fbc149245bd`の公開`default_pattern_rules`と
`find_high_entropy`だけを再利用する。既定patternは5件である。規則の変更は上記file内容識別値の不一致として検出する。

環境依存規則の解決、伏字化、file書込みは呼ばない。このfile、公開関数、既定引数の変更は安全試験をstaleにし、
契約改定まで実装を止める。

### 6.3 保護対象

保護基準commitを`bb55a1fb8d56f45a3c861601ff91b62deab23e26`とする。§6.1・§6.2の再利用fileに加え、
次を変更しない。

| path | SHA-256 |
| --- | --- |
| `tools/task_contract/__init__.py` | `ba556e79e15221f55c4e59d1f90ce6e8fff879da0183f19b8d35bb3f6c4e623d` |
| `tools/task_contract/contract.py` | `68d3a87dcbff34dd18237a9757d768b3d9a3f2a0387b30abeccd84d6f81ed8e9` |
| `tools/task_contract/definition_challenge.py` | `cee75835ea882080f2142a0c1d9eb126b2aa9d9e46924111620c379d0be64594` |
| `tools/task_contract/execution.py` | `32035909a96e6ce28f19792716b5d3e49b7132f6f8e316c1287679c9da291cd0` |
| `tools/task_contract/identity.py` | `fddffe6617c225e9fbedd33ea722316ea41f37c1f76c93cfbce3060ed55b5422` |
| `tests/test_one_item_review.py` | `4af064359a2c1205c6156b1b5295ecaeef5496ae9e59fc82f5d7d44297e4c064` |
| `tests/test_one_design_acceptance.py` | `6adc44ad7c7c9dff37ad3e671abfc0e86d9c5afe53861f2edeafc7acd01e1542` |
| `tests/test_one_requirement_feature_source.py` | `e746f55a7da7c67d8f208cc6a03b7ecaef52e12017c1eca09f0f5acadb17eab6` |

## 7. 安全読取り・書込みと許可能力

正式実行名候補は`reviewcompass3-operation-run`で、入口は次だけとする。

`run --contract <絶対path>`

引数不足、未知・重複引数、相対pathは読取り前に拒否する。

運用契約fileの読取りは、file system起点から全構成要素を非追跡で開き、通常file、size上限262,144 bytes、
読取り前後の同一性（mode・size・機器番号・inode）、実読取りbyte数の一致を確認する。symlink、非通常file、
読取り中変更は停止する。

実行記録の書込みは、運用契約の`output_root`（絶対path・既存directory）直下へ、固定名
`{contract_identifier}--execution-v1.json`の一件だけを、新規作成専用（既存fileがあれば停止し上書きしない）で行う。
directoryを作成しない。書込み後に再読込し、書いたbytesとの完全一致を確認する。

許可する能力は、契約一fileの読取り、UTF-8復号、JSON検査、機微情報候補検査、registry部品の同一process呼出し、
正準JSON、SHA-256、実行記録一件の新規書込みと再読込、標準出力だけである。

上書き、削除、改名、directory作成、通信、外部process、Git、環境値解決、時刻取得、乱数、権限変更、外部送信、
任意コード実行、入力外探索を禁止する。

## 8. 運用契約の形式

### 8.1 共通規則

- rootと全入れ子objectでescape復号後の同名項目を禁止し、通常dictへ変換する前に検出する。
- `schema_version`は`type(value) is int`を満たす整数`1`だけとする。
- 未知項目、浮動小数点数、null、入れ子配列、真偽値（`human_approved`を除く）を禁止する。
- `contract_identifier`はASCII正規表現`[A-Za-z0-9][A-Za-z0-9._-]{0,127}`だけとする。
- SHA-256は`[0-9a-f]{64}`だけとする。
- 絶対pathは`/`始まりで、空・`.`・`..`の構成要素を禁止する。

### 8.2 機微情報候補の検査順

1. JSONのUTF-8、構文、同名項目を検査する。
2. 復号後の全文字列keyと値を、深さ優先で入力順に検査する。
3. 正確な位置`/expected_bindings/{入力名}`にあり、先に`[0-9a-f]{64}`へ合格した値だけを検査対象から外す。
4. それ以外の64桁16進文字列、ID、未知key、絶対path値を除外しない。
5. §6.2の既定patternを宣言順に検査し、その後`find_high_entropy`の既定値で検査する。
6. 最初の一致で値を表示せず停止する。検査の限界（網羅しないこと）は実行記録に固定表示しない代わりに、
   部品結果の`limitations`をそのまま保持する。

### 8.3 運用契約JSON

rootは次の項目だけを持つ。

- `schema_version`：整数`1`。
- `contract_identifier`：一般ID。実行記録のfile名の一部になる。
- `human_approved`：真偽値`true`だけを受理する。`false`・欠落・他型は停止する。
- `operation`：`one_item_review_prepare`、`design_acceptance_check`、`requirement_candidate_check`だけ。
- `input_root`：絶対path。
- `inputs`：操作別の固定keyだけを持つobject。値は絶対path。
  - `one_item_review_prepare`：`material`、`review_spec`。
  - `design_acceptance_check`：`design`、`acceptance`。
  - `requirement_candidate_check`：`catalog`、`candidate`。
- `expected_bindings`：`inputs`と同じkey集合を持つobject。値は各部品の受入済み契約が定義する内容識別値
  （§10.2の照合表が定める部品結果内の値）と一致すべきSHA-256。
- `output_root`：絶対path。`input_root`と同一でもよいが、既存directoryであること。

## 9. 正規化と内容識別値

正準JSON bytesは`json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")`と同じとする。

| 名前 | 計算対象 |
| --- | --- |
| `contract_sha256` | 復号した運用契約root全体 |
| `part_result_sha256` | 部品が標準出力へ返した結果JSON（末尾LFを除くbytesを復号した値） |
| `record_sha256` | `record_sha256`欄だけを除いた§10.1の実行記録root |

## 10. 実行記録（正常結果）

### 10.1 形式

部品が終了コード0を返し束縛照合に合格したとき、次のroot項目だけを持つ正準JSON一件と直後のLF一つを、
実行記録fileと標準出力の両方へ同一bytesで返す。終了コード0、標準エラー空。

- `status: operation_executed`
- `schema_version: 1`
- `contract`：`identifier`、`sha256`（`contract_sha256`）だけ。
- `operation`
- `bindings`：入力名昇順に、各`name`、`expected_sha256`、`reported_sha256`だけ。全件で両値一致。
- `part_exit_code: 0`
- `part_result`：部品結果JSONの全体を無変更で埋め込む。
- `part_result_sha256`
- `decision_status: pending_human_decision`
- `external_send_approved: false`
- `record_sha256`

実行記録へ運用契約の絶対path、入力自由文、例外本文を含めない（`part_result`が部品契約により安全表示である
ことに依拠し、本処理はそこへ何も追加しない）。

### 10.2 束縛照合表

| 操作 | 入力名 | 部品結果内の照合位置 |
| --- | --- | --- |
| `one_item_review_prepare` | `material` | `material.content_sha256` |
| `one_item_review_prepare` | `review_spec` | `review_spec.sha256` |
| `design_acceptance_check` | `design` | `design.sha256` |
| `design_acceptance_check` | `acceptance` | `acceptance.sha256` |
| `requirement_candidate_check` | `catalog` | `catalog.sha256` |
| `requirement_candidate_check` | `candidate` | `candidate.sha256` |

## 11. 停止結果と優先順

停止結果は`status: stopped`、`reason`、`source`、`external_send_approved: false`だけ（`part_stopped`のときだけ
`part_reason`、`part_source`、`part_exit_code`を追加）を持つ正準JSON一件とLF一つを標準出力へ返す。
標準エラーは空とし、入力値、key、path、例外本文を含めない。停止時は実行記録fileを作成しない。

処理順は、引数検査、契約読取り、復号、機微検査、schema検査、出力先事前検査、部品実行、束縛照合、
実行記録書込みである。同じ段階では入力順または§8の項目順で最初の違反を返す。

| 違反 | `reason` | `source` | 終了コード |
| --- | --- | --- | ---: |
| subcommand、引数の不足・未知・重複 | `invalid_arguments` | `arguments` | 2 |
| `--contract`の相対path・不正構成要素 | `invalid_path` | `arguments` | 2 |
| 契約fileのsymlink・非通常file・読取不能・読取り前後不一致 | `unreadable_input` | `contract` | 2 |
| 契約fileのsize上限超過 | `size_limit_exceeded` | `contract` | 2 |
| 契約fileのUTF-8不正 | `invalid_utf8` | `contract` | 2 |
| JSON構文・同名項目・固定schema・型・文字・path形式・`human_approved`不成立 | `invalid_schema` | `contract` | 2 |
| 契約内の機微情報候補 | `sensitive_data_remaining` | `contract` | 3 |
| `output_root`が存在しない・directoryでない・実行記録fileが既存 | `invalid_output_root` | `output` | 2 |
| 部品が非0の終了コードで停止した | `part_stopped` | `part` | 5 |
| 束縛照合の不一致（`expected_sha256`≠`reported_sha256`） | `binding_mismatch` | `contract` | 2 |
| 実行記録の書込み失敗・再読込不一致 | `record_write_failed` | `output` | 4 |
| 上記へ分類できない内部例外 | `internal_failure` | `none` | 4 |

`part_stopped`の`part_reason`・`part_source`は、部品の固定停止形式が返した`reason`・`source`の値だけを転記する。
部品の正常・停止以外の出力形は`internal_failure`とする。

## 12. 変更上限

製品変更は次に限定する。

1. 副作用が書込み一件だけの実行核`tools/operations/operation_contract_run.py`（新規package `tools/operations/`）。
2. 入口`tools/operations/operation_contract_run_entry.py`。
3. `pyproject.toml`への実行名一件。
4. 対象試験`tests/test_operation_contract_run.py`。
5. 作業票、失敗・成功証拠、最終検証、独立確認、受入判断、TODO更新。

§6の再利用・保護対象、既存G30基盤、既存部品、既存試験、要求schema、他製品処理を変更しない。必要なら契約改定へ戻る。

## 13. 受入条件

実装開始後は失敗試験を先に固定し、期待どおり失敗してから最小実装を行う。

1. 3操作それぞれの正例で、部品実行、束縛照合、実行記録の着地、標準出力一致を一度ずつ示す。
2. 実行記録fileと標準出力のbytesが完全一致し、`record_sha256`を独立oracleで再計算できる。
3. `contract_sha256`、`part_result_sha256`を独立oracleで§9の正確な計算対象から再計算する。
4. 部品結果を埋め込んだ`part_result`が部品の標準出力と復号後に完全一致する。
5. object項目順だけの差では実行記録bytesと全内容識別値を変えない。
6. 束縛宣言の一値変更で`binding_mismatch`となり、実行記録fileが作られない。
7. `human_approved`の`false`・欠落・非真偽値を`invalid_schema`で停止する。
8. 未知操作、入力keyの過不足、path形式違反、束縛keyの過不足を`invalid_schema`で停止する。
9. JSON同名項目、escape後同名、未知項目、浮動小数点、null、入れ子配列、単独サロゲート、不正ID・SHA-256を
   未処理例外なしで停止する。
10. AWS鍵形式、email、bearer token、API key代入、秘密鍵block、高乱雑性tokenを契約のkey・値で停止し、
    正しい`expected_bindings`のSHA-256値だけを高乱雑性検査から外す。
11. §6.2のfileの内容識別値、公開関数2名、既定pattern件数5を実行前後に照合し、環境依存規則を解決しない。
12. 契約fileのsymlink、非通常file、size超過、UTF-8不正、読取り中変更を停止する。
13. `output_root`不存在・非directory・実行記録既存を`invalid_output_root`で停止し、上書きが起きない。
14. 部品停止時は`part_stopped`で部品の`reason`・`source`・終了コードだけを転記し、実行記録fileを作らない。
15. §11の全行について`reason`、`source`、終了コード、空stderr、値・path・例外非表示を確認する。
16. 実行記録一件の新規作成以外にfile変更がなく、通信、外部process、Git、環境値解決、時刻取得、入力外探索を行わない。
17. 配布後の正式実行名を別の現在位置から実行しても同じbytesを返す。
18. §6.1の再利用6 fileが固定内容識別値と一致し、次の各単独commandが成功する。
    `.venv/bin/python3 -m pytest -q tests/test_one_item_review.py`、
    `.venv/bin/python3 -m pytest -q tests/test_one_design_acceptance.py`、
    `.venv/bin/python3 -m pytest -q tests/test_one_requirement_feature_source.py`
19. §6.3の保護対象が基準commitから差分0で、`.venv/bin/python3 -m pytest -q tests/test_first_review_task_contract_e2e.py`が成功する。
20. 対象、関連、正規全試験を各単独終了コード0で成功させ、固定commitを別担当が誤合格・未接続・禁止作用・
    上位目的への悪影響0件として確認する。
21. 合成一件で3操作の実行記録、束縛照合、判断待ち、安全表示を示す。
22. 利用者が「G30全体ではなく最初の実行縦切りである」限界、実装結果、後続未完了を確認して製品処理を受け入れる。

## 14. 停止条件

- 実行縦切りだけでは最初の価値がないと利用者が判断する。
- 複数操作の連鎖、実行計画、状態管理、既存G30基盤の変更が本縦切りに必要になる。
- §6の再利用・保護対象の変更が必要になる。
- 通信、外部process、上書き、削除、directory作成、環境値解決、時刻取得が必要になる。
- 入力自由文、機微情報候補、絶対pathを実行記録へ含める必要が生じる。
- 束縛照合を固定規則から一意に判定できない。
- 未承認のschema・既存試験変更、範囲拡大が必要になる。
- 対象、関連、正規全試験または独立確認が不合格になる。

## 15. 影響、未実施、次作業

【判断】受入後は、利用者が承認した運用契約一件を一commandで実行し、部品結果・入力束縛・判断待ちを結んだ
実行記録一件を再現可能に着地できる。受入済み部品の「実行→記録」導線が初めて機械化される。入力の組み立て支援、
部品間の連鎖、保存統合、既存G30基盤の正式化は増えず、候補4は未完了のまま残る。

【未実施】契約採用、縮小境界の利用者判断、実装、既存成果物変更、外部送信は行っていない。

次は本候補と運用化目標recordを固定commitへ記録し、本候補の作成を担当しなかった別担当が定義反証だけを
成果物変更なしで確認する。`開始可`になった後にだけ、利用者へ「最初の実行縦切りの採用」と案Cの実装開始を
一判断として求める。
