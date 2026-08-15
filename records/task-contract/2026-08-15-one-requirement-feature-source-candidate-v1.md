# 一件の要求・機能区分・出典対応 作業契約候補 v1

- 契約ID：`TC-RC3-PRODUCT-ONE-REQUIREMENT-FEATURE-SOURCE-005`
- 契約版：1
- 契約種別：製品処理
- 状態：`candidate_pending_independent_review_and_human_approval`
- 作成日：2026-08-15
- 直前の製品契約：`TC-RC3-PRODUCT-ONE-DESIGN-ACCEPTANCE-CONFORMANCE-004`
- 利用者判断：2026-08-15のG08正式受入、残る候補の自律実行、別担当AIによる独立確認の許可
- 実装状態：未開始
- 危険度：高
- 危険の理由：要求の由来と昇格判断に影響し、入力へ機微情報が含まれ得る
- 内容識別値：本候補固定後、独立定義確認と利用者判断記録から参照する

「作業契約」は、一つの仕事の目的、入力、範囲、許可操作、期待結果、確認方法、停止条件を実装前に固定する約束である。
「内容識別値」は、検査・正規化後の正準JSONからSHA-256で計算する改変検出用の値である。
「原子義務」は、要求本文または要求内の一覧一項目として、出典対応を個別に確認する最小単位である。

## 1. 目的

利用者が明示した出典一覧一件と構造化要求候補一件について、自由文の意味を補わず、次を決定的に確認する。

1. 出典一覧の全件に、採用または理由付き不採用がちょうど一つある。
2. 一つの要求が一つの機能IDへ属し、要求内の全原子義務が採用出典へ戻れる。
3. 採用出典は少なくとも一つの原子義務に使われ、不採用出典はどの義務にも使われない。
4. 結果を入力と各構成物の内容識別値へ結び、要求昇格と最終採否は人の判断として残す。

【判断】要求文、機能名、責務、採否理由の正しさは推測しない。製品処理は構造、被覆、参照整合、決定性だけを確認する。
出典の申告状態が`effective`であっても、本処理は新しい要求候補を正式要求へ昇格しない。

## 2. 権威と証拠

### 2.1 現在の権威

| 役割 | path | SHA-256 |
| --- | --- | --- |
| 現行開発方針 | `docs/development/2026-08-02-development-policy.md` | `e3e6b0d2c7a1265f7cde2c2e00cc888f43d63ce0d1945c300b2b2e5f7730b559` |
| 直前製品の受入判断 | `records/development/2026-08-15-one-design-acceptance-product-acceptance-decision-v1.md` | `7e3eb626474f72ebcd3a3d5ec2646cf004ba192606f03684a50ae6f0b251ce86` |
| 次製品作業の候補一覧 | `records/development/2026-08-15-post-safe-storage-next-product-work-candidates-v1.md` | `bcb4ba2947e32254edc547068728fa580bc6b7919fa0f04d9b9353ab6c7899ba` |

### 2.2 固定証拠

| 役割 | path | SHA-256 |
| --- | --- | --- |
| G24を5実装・5試験として分けた目録 | `records/development/2026-08-14-stage4-product-code-and-task-contract-input-inventory-evidence-v1.md` | `c55367fc6b8f72f7041612cedc11d609b359909156f619fcb72e6d72bd33e72a` |
| 契約定義証拠 | `records/development/2026-08-15-one-requirement-feature-source-contract-definition-evidence-v1.md` | `9d35dc70f5d96eb497bd8530ced4a1b32d5d838a6c0503f24668d8be719987c6` |
| 現行要求権限束v2 | `records/requirements/authority/rc3-requirements-authority-2026-08-03--v2.json` | `760e33ea2ecf6937f56d7bf8d2bd703b18b47dbd2bd6b2bd5919e0dd556d9dae` |
| 50要求の格納形式昇格判断 | `records/requirements/decisions/dec-requirements-unified-50-2026-08-03-v1.json` | `dd8b5dd15197da0a3463b3981d607da6edcb8318e17d91038786de7edc9eff27` |

【実測】現行要求権限束v2は既存解決処理で50要求を`effective`として返す。一方、対応する人の判断は、要求本文、
受入真偽、現行計画、製品実装、非機能要求と先送り判断を承認範囲外と明記する。

【判断】本契約の正式責務は候補一覧、直前製品受入判断、利用者指示から狭く導く。`REQ-CONTEXT-002`と
`REQ-TRACE-002`は対応候補として記録するが、上流不一致が解消されていないため`source_requirement_ids`へ固定しない。
旧第4段の37要求、機能分割、出典対応、完了記録も暫定資料のままとし、正式要求へ昇格しない。

## 3. 実装方法の3案

| 案 | 内容 | 単純さ・資源 | 頑健さ | 変更範囲・保守 | 判断 |
| --- | --- | --- | --- | --- | --- |
| A 既存機能だけ | 呼出し側がPython値を作り既存5検査を順に呼ぶ | 新規実装0、資源小 | 正式入口、安全読取り、全出典採否、未昇格表示が一組にならない | 変更0だが目的未達 | 不採用 |
| B 既存5 fileを正式化 | 旧固定入力照合を入口にし4検査を接続する | 接続は短いが全面修正が必要 | シンボリックリンク、型混同、未処理例外、暫定権限を持ち込む | 既存5 fileと5試験へ広く影響 | 不採用 |
| C 狭い専用処理 | 出典一覧と要求候補だけを安全に読み、全採否・全義務対応・機能一致を検査する | 入力件数に比例し上限固定 | 意味推測をせず、未定義・未被覆・自動昇格を閉じる | 新規核・入口・試験・実行名だけで戻しやすい | 推奨 |

【提案】案Cを採用候補とする。二fileの安全読取りは受入済みG08の`read_input_pair`を再利用し、G08自体は変更しない。
G08の内部停止元`design`と`acceptance`はG24入口で`catalog`と`candidate`へ読み替える。

## 4. 識別と範囲

| 項目 | 値 |
| --- | --- |
| `task_contract_id` | `TC-RC3-PRODUCT-ONE-REQUIREMENT-FEATURE-SOURCE-005` |
| `contract_type` | `product_delivery` |
| `version` | 1 |
| 正式な責務の出所 | 直前製品受入判断、次製品作業の候補一覧、利用者指示 |
| `source_requirement_ids` | なし。要求本文と受入真偽の権限不一致が未解消のため空 |
| 対応候補 | `REQ-CONTEXT-002`、`REQ-TRACE-002`。正式要求への再昇格はしない |
| 直前契約ID | `TC-RC3-PRODUCT-ONE-DESIGN-ACCEPTANCE-CONFORMANCE-004` |
| 記録形式 | Markdown候補。未完成の汎用作業契約schemaと状態管理を使わない |

### 4.1 範囲内

- 利用者が絶対pathで明示した一つの入力root、出典一覧JSON一件、要求候補JSON一件を読む。
- 各入力は262,144 bytes以下とする。
- 出典は1件以上256件以下、要求は一件、機能は一件、要求の原子義務は8件以上225件以下とする。
- JSON復号時の同名項目、固定schema、識別子、文字、型、重複、件数、root内束縛を検査する。
- 全出典の採否、全原子義務の出典対応、採用出典の消費、機能ID一致を検査する。
- 結果、件数、内容識別値、人の判断一覧を正準JSON一件で表示する。

### 4.2 範囲外

- Markdown、Word、PDF、画像、自由文資料の読解、要求文または機能区分の起草。
- 同義語、類似表現、要求の正しさ、採否理由、出典の申告状態の真実性の推測。
- 複数要求間または複数機能間の分割、重複、境界関係、依存関係の検査。
- 出典本文fileの読取り、directory探索、glob、再帰走査、暗黙資料、会話履歴全体。
- 外部AI、通信、外部送信、外部process、Git、環境値解決、認証、再試行。
- 入力・結果の保存、file作成・書換え、権限変更、削除。
- 要求候補、機能、出典対応の自動修正、要求権限束への登録、正式昇格、最終採否。
- 既存G24の5実装、関連5試験、旧第4段成果物、現行50要求、G08の変更または正式化。
- G30の汎用作業契約、状態管理、台帳の追加。

## 5. 前提と許可能力

### 5.1 前提

- 独立定義確認後に、利用者が契約採用と案Cの実装開始を明示する。
- `input_root`、出典一覧JSON、要求候補JSONは絶対pathで明示される。
- 二入力は字句上もopen後もroot内にあり、互いに異なる通常fileである。
- file system起点`/`から二入力までの全構成要素にシンボリックリンクがない。
- 入力位置を探索・推測せず、所有者、mode、アクセス制御を変更しない。
- 入力中の自由文は画面へ表示しない。表示するIDは安全な識別子規則に合格している。
- 入力作成者が要求候補、機能区分、採否理由、出典対応を用意する。製品処理は意味を再判定しない。

### 5.2 許可する能力と安全読取り

- UTF-8復号、同名項目を保持できるJSON復号、固定schema、件数、型、識別子の検査。
- 正準JSON、SHA-256、型付き完全一致、集合の包含・非交差、件数、並べ替えの決定的計算。
- 入力値を含まない正常結果または停止結果のJSON一件の標準出力。

安全読取りは受入済みG08の`tools.design.one_design_acceptance.read_input_pair`をそのまま使う。絶対rootを
file system起点から各要素ずつ非追跡で開き、rootから二入力までの各directoryと最後のfileも非追跡で開く。
通常file、size、機器番号、inode、読取り前後の一致、実読取りbyte数を確認する。二pathが同じfileを指す場合は拒否する。

禁止する能力は、file書込み、directory作成、通信、外部process、Git、環境値解決、権限変更、削除、外部送信、
任意コード実行、指定二file以外の探索である。

## 6. 入力形式

正式実行名候補は`reviewcompass3-requirement-candidate-check`とし、入口は次の一つだけとする。

`check --input-root <絶対path> --catalog <絶対path> --candidate <絶対path>`

引数不足、未知・重複引数、相対pathは読取り前に拒否する。入力pathを標準出力・標準エラーへ表示しない。

### 6.1 共通JSON規則

- rootと全ての入れ子objectで、escape復号後の同名項目を禁止する。通常のdictへ変換する前に検出する。
- `schema_version`は真偽値ではない整数`1`だけとする。
- 未知項目、浮動小数点数、null、objectの自由な追加、入れ子配列を禁止する。
- 識別子は英数字で始まり、以後を英数字、ピリオド、下線、ハイフンに限る1文字以上128文字以下とする。
- `feature_id`は`FEAT-`、`requirement_id`は`REQ-`で始まり、同じ安全な文字規則に従う。
- SHA-256は小文字16進64文字とする。
- 自由文はUnicode scalar valueだけを含む1文字以上2,000文字以下とし、NULを禁止する。
- 一覧内自由文は各1文字以上500文字以下、重複なし、各一覧1件以上32件以下とする。

### 6.2 出典一覧JSON

rootは`schema_version`、`catalog_identifier`、`sources`だけを持つ。`sources`は1件以上256件以下で、各項目は
`source_id`、`sha256`、`declared_status`だけを持つ。出典IDは一覧内で一意とする。

`declared_status`は`effective`、`approved_context`、`candidate`、`historical`だけとする。これは入力作成者の申告であり、
製品処理が外部権限記録を探索して真実性を保証した値ではない。出典は`source_id`順へ正規化する。

### 6.3 要求候補JSON

rootは`schema_version`、`candidate_identifier`、`feature`、`requirement`、`source_dispositions`、
`obligation_sources`だけを持つ。

`feature`は`feature_id`、`name`、`responsibility`、`non_goals`だけを持つ。`non_goals`は1件以上32件以下とする。

`requirement`は次だけを持つ。

- `requirement_id`
- `feature_id`
- `statement`
- `inputs`
- `outputs`
- `stop_conditions`
- `recovery_conditions`
- `preserved_artifacts`
- `acceptance_criteria`
- `non_goals`

要求の`feature_id`は`feature.feature_id`と一致しなければならない。七つの一覧項目は入力順を意味の一部として保持する。
object項目順、出典順、採否順、対応順、各対応内の出典順だけは意味を持たず正規化する。

`source_dispositions`の各項目は`source_id`、`disposition`、`rationale`だけを持つ。`disposition`は`selected`または
`not_selected`だけとする。出典一覧の全IDがちょうど一度現れ、未知ID、欠落、重複を禁止する。

`obligation_sources`の各項目は`obligation_id`と`source_ids`だけを持つ。原子義務IDは次のように作る。

- 本文：`{requirement_id}#statement`
- 一覧項目：`{requirement_id}#{field}.{1から始まる3桁位置}`

全原子義務がちょうど一度現れなければならない。各`source_ids`は1件以上256件以下で、重複せず、採用出典だけを参照する。
全採用出典は少なくとも一つの原子義務から参照されなければならない。

## 7. 判定と期待成果

### 7.1 正常結果

終了コード0で、入力自由文と絶対pathを含まず、次の項目だけを持つ正準JSON一件を返す。

- `status: requirement_candidate_checked`
- `schema_version: 1`
- `decision_status: pending_human_decision`
- `promotion_status: not_promoted`
- `verdict`：候補または履歴出典を採用していれば`review_required_pending_human_decision`、それ以外は`trace_complete_pending_human_decision`
- `catalog`：`identifier`、`sha256`、`source_count`
- `candidate`：`identifier`、`sha256`
- `feature`：`identifier`、`sha256`
- `requirement`：`identifier`、`sha256`、`obligation_count`
- `counts`：申告状態別、`selected`、`not_selected`、`traced_obligation`
- `source_dispositions`：`source_id`、`declared_status`、`disposition`
- `obligation_sources`：`obligation_id`、昇順の`source_ids`
- `trace_sha256`
- `result_sha256`
- `human_decision_queue`
- `limitations`
- `external_send_approved: false`

`source_dispositions`は出典ID順、`obligation_sources`は義務ID順とする。`human_decision_queue`は常に
`requirement_candidate`を一件持ち、採用した`candidate`または`historical`出典があれば状態別に安全な出典IDを加える。
`limitations`は固定語彙`source_status_not_verified`、`semantic_correctness_not_verified`、
`multi_requirement_partition_not_verified`、`authority_not_changed`の4件をこの順で持つ。

出典一覧、候補、機能、要求、出典対応の各SHA-256は検査・正規化後の対象全体から計算する。`result_sha256`は、
その欄だけを除く正常結果の正準JSONから計算する。object項目順、出典順、採否順、対応順、対応内出典順だけの差では
結果と内容識別値を変えない。要求内七一覧の順序変更は原子義務IDの意味を変えるため内容識別値を変える。

### 7.2 停止結果

成功成果を返さず非0終了コードとし、`status: stopped`、`reason`、`source`、`external_send_approved: false`だけを持つ
正準JSON一件を返す。

`source`は`arguments`、`catalog`、`candidate`、`none`だけとする。引数・path不正は`arguments`、出典一覧だけに
確定した読取り・size・UTF-8・schema不正は`catalog`、要求候補だけなら`candidate`、入力fileを特定できない読取り失敗と
内部失敗は`none`とする。値、項目名、path、例外本文は返さない。

固定理由は`invalid_arguments`、`invalid_path`、`unreadable_input`、`size_limit_exceeded`、`invalid_utf8`、
`invalid_schema`、`unresolved_reference`、`incomplete_coverage`、`internal_failure`だけとする。引数、入力、参照、被覆の停止は
終了コード2、内部失敗は4とする。

全JSONはUTF-8、BOMなし、項目名昇順、区切り前後の空白なし、直後に改行一つとする。標準エラーは常に空とし、
入力path、自由文、例外本文、入力抜粋を正常・停止出力へ含めない。

## 8. 実装候補の変更上限

案Cの製品変更は次に限定する。

1. 副作用のない検査核`tools/requirements/one_requirement_feature_source.py`。
2. G08安全読取りを再利用する正式入口`tools/requirements/one_requirement_feature_source_entry.py`。
3. `pyproject.toml`への実行名一件。
4. 対象試験`tests/test_one_requirement_feature_source.py`。
5. 作業票、失敗・成功証拠、最終検証、独立確認、受入判断、TODO更新。

既存G24の5実装・5試験、旧第4段成果物、要求artifact schema、現行50要求、G08、他製品処理を変更しない。
必要になれば停止して契約改定を求める。

## 9. 受入条件

実装開始後は失敗試験を先に固定し、期待どおり失敗してから最小実装を行う。

1. 一機能・一要求・出典三件の正例で、全出典の採否、全原子義務の対応、採用出典の消費を一度ずつ示す。
2. 出典の採否欠落、重複、未知出典、空理由を成功にしない。
3. 原子義務の対応欠落、重複、未知義務、空出典、未定義出典、不採用出典参照を成功にしない。
4. 採用したがどの義務にも使わない出典を成功にしない。
5. 要求の機能IDと機能のID不一致、七一覧の欠落・空・重複を成功にしない。
6. 全義務が対応しても自動昇格せず、`not_promoted`、`pending_human_decision`、固定限界4件を返す。
7. 候補・履歴出典の採用を人の判断一覧へ残し、申告状態から権限を推測しない。
8. object項目順、出典順、採否順、対応順、対応内出典順だけでは結果と内容識別値を変えない。
9. 要求本文、一覧一項目、採否理由、出典SHA-256の一変更で対応する内容識別値が変わる。
10. rootと全入れ子のJSON同名項目、escape復号後同名、未知項目、真偽値の版、浮動小数点、単独サロゲート、
    不正識別子、不正SHA-256、禁止値型、件数・文字長超過を成功にせず未処理例外を表示しない。
11. file system起点から入力rootと二fileまでの各途中要素・最後の要素のシンボリックリンク、root外、通常file以外、
    同じ二入力、読取不能、size超過、UTF-8不正を成功にしない。
12. 事前検査後のpath差替えと読取り中のsize・identity変更を成功にしない。
13. 停止元を閉じた`source`で正しく示し、自由文、項目名、path、例外本文を出さない。
14. file変更、通信、外部process、Git、環境値解決、入力外探索を行わない。
15. 配布後の正式実行名を別の現在位置から実行しても同じbytesを返す。
16. 既存G24の5実装・5試験は基準commitから差分0で、関連59件が成功する。
17. 現行要求権限束v2は既存解決処理で引き続き50要求を`effective`として返し、既存要求artifact関連21件が成功する。
18. 対象、関連、安全表示、正規全試験が各単独終了コード0で成功する。
19. 固定commitを別実行単位が読取り専用で確認し、誤合格、未接続条件、禁止作用、上位目的への悪影響が0件である。
20. 合成一件で内容識別値、件数、全採否、全義務対応、未昇格、人の判断一覧、安全表示を示す。
21. 利用者が実装結果と限界を確認後、製品処理として受け入れる。

## 10. 停止条件

- 自由文の意味推測または要求文の自動生成がないと利用者価値が成立しない。
- 複数要求間の機能分割または境界関係がないと一件処理を完了できない。
- 既存G24、旧第4段成果物、現行50要求、要求schema、G08の変更が必要になる。
- 通信、外部process、保存、Git、環境値解決、入力外探索が必要になる。
- 入力自由文または絶対pathを製品出力へ含める必要が生じる。
- 出典の採否、原子義務の対応、採用出典の消費を固定規則から一意に確認できない。
- 未承認の設計・schema・既存試験変更、範囲拡大が必要になる。
- 対象、関連、安全表示、正規全試験または独立確認が不合格になる。

## 11. 影響と未実施

【判断】受入後は、構造化した要求候補一件について、全出典の採否、各原子義務から固定出典への対応、一機能への所属を
再現可能に確認できる。候補または履歴資料の利用も人の判断一覧へ残る。要求昇格、意味判断、通信、保存、既存G24の
正式化は増えない。

【未実施】契約採用、実装、コード・試験・配布設定変更、既存G24・G08変更、現行要求変更、実利用者資料、
外部送信、保存、自由文解析、自動昇格は行っていない。

## 12. 次の一作業

本候補を固定commitへ記録し、別担当が成果物変更なしで目的、上流不一致、入力、全採否、全義務対応、未昇格、
安全読取り、安全表示、変更上限、受入条件の誤合格余地を反証する。`開始可`となった後にだけ、利用者へ契約採用と
案Cの実装開始を一判断として求める。
