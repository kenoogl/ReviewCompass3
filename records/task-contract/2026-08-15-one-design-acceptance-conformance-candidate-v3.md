# 一件の設計・受入条件照合 作業契約候補 v3

- 契約ID：`TC-RC3-PRODUCT-ONE-DESIGN-ACCEPTANCE-CONFORMANCE-004`
- 契約版：3
- 契約種別：製品処理
- 状態：`candidate_corrected_pending_limited_independent_review_and_human_approval`
- 作成日：2026-08-15
- 直前の製品契約：`TC-RC3-PRODUCT-ONE-ITEM-REVIEW-003`
- supersedes：`records/task-contract/2026-08-15-one-design-acceptance-conformance-candidate-v2.md`、SHA-256 `d34c96e44a716555f61d666e35ad1c1eed5d79cdecfd43be9a95dce4e5812e15`
- 訂正根拠：`records/development/2026-08-15-one-design-acceptance-contract-v2-independent-review-v1.md`、SHA-256 `41548a326e1e8ea362605a015f43a5e2beeeab858c57b7d4ce3a3d05b21bb85e`
- 訂正範囲：JSON同名項目拒否、4比較の不成立例、入力root全要素のsymlink非追跡、危険度だけ
- 利用者判断：2026-08-15の「次へ」、残る7候補の自律実行指示、別担当AIによる独立確認の許可
- 実装状態：未開始
- 危険度：高
- 危険の理由：設計適合と受入真偽へ影響する検査であり、入力に機微情報が含まれ得る
- 内容識別値：本候補固定後、独立定義確認と利用者判断記録から参照する

「作業契約」は、一つの仕事の目的、入力、範囲、許可操作、期待結果、確認方法、停止条件を実装前に固定する約束である。
「内容識別値」は、検査・正規化後の正準JSONからSHA-256で計算する改変検出用の値である。

## 1. 目的

利用者が明示した設計一件と受入条件一式を、自由文の意味を推測せず、明示された項目と比較規則だけで照合する。

1. 設計に同じ項目があり、比較が成立する場合は`満たす`。
2. 設計に同じ項目がない場合は`欠落`。
3. 設計に同じ項目があるが、比較が成立しない場合は`矛盾`。
4. 受入条件から参照されない設計項目は`未参照`として残す。
5. 全結果を入力の内容識別値へ結び、最終受入は人の判断として残す。

【判断】入力作成者が同じ意味へ同じ`subject`を割り当てる。製品処理は同義語、類似表現、設計または条件の
正しさを推測しない。各`subject`を設計と受入条件でそれぞれ一意にし、条件同士の競合を設計側の矛盾へ混ぜない。

## 2. 権威と証拠

### 2.1 現在の権威

| 役割 | path | SHA-256 |
| --- | --- | --- |
| 現行開発方針 | `docs/development/2026-08-02-development-policy.md` | `e3e6b0d2c7a1265f7cde2c2e00cc888f43d63ce0d1945c300b2b2e5f7730b559` |
| 直前製品の受入判断 | `records/development/2026-08-15-one-item-review-product-acceptance-decision-v1.md` | `8401ff7bd145755af2d5893db2da1fd5d00ee62c224d1602c3080c380f454441` |
| 次製品作業の候補一覧 | `records/development/2026-08-15-post-safe-storage-next-product-work-candidates-v1.md` | `bcb4ba2947e32254edc547068728fa580bc6b7919fa0f04d9b9353ab6c7899ba` |

### 2.2 固定証拠

| 役割 | path | SHA-256 |
| --- | --- | --- |
| G08を2 path・関連試験2 fileとして分けた目録 | `records/development/2026-08-14-stage4-product-code-and-task-contract-input-inventory-evidence-v1.md` | `c55367fc6b8f72f7041612cedc11d609b359909156f619fcb72e6d72bd33e72a` |
| 契約定義Evidence | `records/development/2026-08-15-one-design-acceptance-contract-definition-evidence-v1.md` | `9bad2d80fcddb6f97f9db71fa05a4811ce59404353aa07fb55c3070784d5f6b5` |
| 製品目的の候補 | `docs/current/reviewcompass3-intent-current.md` | `1950f5a37fb5d0d0554f56343b39bbca7fc635523409f10ee761d8cef68f9ec6` |
| 統合製品計画候補 | `docs/current/reviewcompass3-plan-current.md` | `1a73597605eafb65a2259ccf19431e3aba041564d03fdb279150042a9bd0962f` |
| 既存の設計契約検査 | `tools/design/design_contract.py` | `4678b9e16a5e4b02b3e065ab69c94ffacc10a975986c2d0c238039ea02ad3792` |
| 既存の証拠付き適合検査 | `tools/design/bootstrap_conformance.py` | `100d46a4013c3cea3981d6a665d8cfda5f372d2a6e70ccc5fd3fde346bb58fcb` |

【実測】既存G08は2,471行、関連試験2 file 31件で、単独試験は終了コード0だった。既存処理は旧第5段の
設計構造、境界、接続面、状態遷移、通信手順、証拠、固定commitを広く検査し、一件用の製品入口は持たない。
`bootstrap_conformance.py`は固定commit内容の確認で外部processを起動する経路も持つ。

【判断】製品目的と統合製品計画は暫定候補のままとし、正式要求へ昇格しない。本契約の正式責務は候補一覧、
直前製品受入判断、利用者指示から狭く導く。

## 3. 実装方法の3案

| 案 | 内容 | 単純さ・資源 | 頑健さ | 変更範囲・保守 | 判断 |
| --- | --- | --- | --- | --- | --- |
| A 既存機能だけ | `validate_design_contract`へ既存形式を渡す | 新規実装0、資源小 | 対応被覆だけで、値の矛盾、安全表示、正式入口がない | 変更0だが目的未達 | 不採用 |
| B 既存2 pathを包む | 旧第5段の広い検査へ製品入口を足す | 接続は短いが不要な検査が多い | 外部processと旧構造を製品責務へ持ち込む | 既存2 pathへ影響し戻しにくい | 不採用 |
| C 狭い専用処理 | 明示した設計事実と受入条件だけを比較する | 入力件数に比例し上限固定 | 意味推測をせず、欠落と矛盾を決定的に分ける | 新規核・入口・試験だけで既存G08を変えず戻しやすい | 推奨 |

【提案】案Cを採用候補とする。案Aは目的を満たさず、案Bは一件照合に不要な広い責務を持ち込む。

## 4. 識別と範囲

| 項目 | 値 |
| --- | --- |
| `task_contract_id` | `TC-RC3-PRODUCT-ONE-DESIGN-ACCEPTANCE-CONFORMANCE-004` |
| `contract_type` | `product_delivery` |
| `version` | 3 |
| 正式な責務の出所 | 直前製品受入判断、次製品作業の候補一覧、利用者指示 |
| `source_requirement_ids` | なし。正式採用済みRequirementが存在しないため空 |
| 対応候補 | `REQ-EVAL-001`。正式要求への昇格はしない |
| 直前契約ID | `TC-RC3-PRODUCT-ONE-ITEM-REVIEW-003` |
| 記録形式 | Markdown候補。未完成の汎用作業契約schemaと状態管理を使わない |

### 4.1 範囲内

- 利用者が絶対pathで明示した一つの入力root、設計JSON一件、受入条件JSON一件を読む。
- 各入力は262,144 bytes以下とする。
- 設計事実と受入条件は各1件以上256件以下とする。
- JSON復号時の同名項目、固定schema、識別子、値型、重複、件数、root内束縛を検査する。
- 設計事実と受入条件を一意な`subject`で対応させ、固定した4比較だけを実行する。
- 結果、件数、内容識別値、人の判断一覧を正準JSON一件で表示する。

### 4.2 範囲外

- Markdown、Word、PDF、画像、自由文の設計書の解析。
- 表現の類似、同義語、設計の妥当性、受入条件の正しさの推測。
- 複数設計、directory探索、glob、再帰走査、暗黙資料、会話履歴全体。
- 外部AI、通信、外部送信、外部process、Git、環境値解決、認証、再試行。
- 入力・結果の保存、file作成・書換え、権限変更、削除。
- 設計・条件の自動修正、条件追加、最終採否、完了の自動決定。
- 既存G08の2 path、関連試験2 file、旧第5段検査の変更または正式化。
- G30の汎用作業契約、状態管理、台帳の追加。

## 5. 前提と許可能力

### 5.1 前提

- 独立定義確認後に、利用者が契約採用と案Cの実装開始を明示する。
- `input_root`、設計JSON、受入条件JSONは絶対pathで明示される。
- 二入力は字句上もopen後もroot内にあり、互いに異なる通常fileである。
- file system起点`/`から二入力までの全構成要素にsymlinkがない。
- 入力位置を探索・推測せず、所有者、mode、ACLを変更しない。
- 入力中の自由値は画面へ表示しない。表示識別子は安全な識別子規則に合格している。
- 入力作成者が同じ意味へ同じ`subject`を割り当てる。製品処理は意味の一致を再判定しない。

### 5.2 許可する能力と安全読取り

- UTF-8復号、同名項目を保持できるJSON復号、固定schema、件数、型、識別子の検査。
- 正準JSON、SHA-256、型付き完全一致、集合の包含・非交差、件数、並べ替えの決定的計算。
- 入力値を含まない正常結果または停止結果のJSON一件の標準出力。

絶対`input_root`を`/`から一要素ずつdirectory file descriptorで相対的に開く。空要素、`.`、`..`を拒否し、
各要素へ`O_DIRECTORY`と`O_NOFOLLOW`相当を使う。入力file pathは字句上の構成要素がrootと一致することを確認し、
rootから先の全directoryと最後のfileもdirectory file descriptorから一要素ずつ`O_NOFOLLOW`相当で開く。
最後のfileは通常fileであることをopen後に確認する。

各fileはopen後にsize、機器番号、inodeを確認し、上限より1 byte多く読める処理で上限超過を検出する。
読取り後に再度種類、size、機器番号、inodeを確認し、open後の値または実読取りbyte数と一致しなければ
`unreadable_input`で停止する。この方法を使えない環境では停止する。`resolve()`後の文字列比較、root自身だけへの
一回の`O_NOFOLLOW`、file最後の要素だけへの`O_NOFOLLOW`で安全とみなさない。

禁止する能力は、file書込み、directory作成、通信、外部process、Git、環境値解決、権限変更、削除、外部送信、
任意コード実行、指定file以外の探索である。

## 6. 入力形式

正式実行名候補は`reviewcompass3-design-acceptance-check`とし、入口は次の一つだけとする。

`check --input-root <絶対path> --design <絶対path> --acceptance <絶対path>`

引数不足、未知・重複引数、相対pathは読取り前に拒否する。入力pathを標準出力・標準エラーへ表示しない。

### 6.1 JSON同名項目

設計と受入条件は、rootと全ての入れ子objectで同名項目を禁止する。JSON escapeを復号した後の文字列を比較し、
`"a"`と`"\u0061"`も同名として拒否する。通常のdictへ変換して先の値を失う前に、全項目対を保持する
`object_pairs_hook`相当で検出する。同名項目を含む入力は`invalid_schema`で停止し、正規化またはSHA-256計算へ進めない。

### 6.2 安全な識別子

`design_identifier`、`acceptance_identifier`、`fact_id`、`condition_id`、`subject`は、英数字で始まり、以後を
英数字、ピリオド、下線、ハイフンに限る1文字以上128文字以下とする。

### 6.3 比較値

比較値は次だけとし、浮動小数点数、null、object、入れ子配列を禁止する。

- 真偽値。
- `-9007199254740991`以上`9007199254740991`以下の整数。真偽値を整数として扱わない。
- NULを含まない1文字以上2,000文字以下の文字列。
- 1件以上32件以下の重複しない文字列配列。各文字列はNULなし、1文字以上256文字以下。

文字列は大文字小文字を区別する。文字列配列は入力順を意味にせず文字列昇順へ正規化する。
異なるJSON型の値を等しいと扱わない。

### 6.4 設計JSON

rootは`schema_version: 1`、`design_identifier`、`facts`だけを持つ。各事実は`fact_id`、`subject`、`value`だけを持つ。
`fact_id`と`subject`は設計内でそれぞれ一意とする。未知項目、空配列、上限超過を拒否する。
設計事実は`subject`、`fact_id`順へ正規化する。

### 6.5 受入条件JSON

rootは`schema_version: 1`、`acceptance_identifier`、`conditions`だけを持つ。各条件は`condition_id`、`subject`、
`operator`、`expected`だけを持つ。`condition_id`と`subject`は受入条件内でそれぞれ一意とし、重複を
`invalid_schema`で停止する。未知項目、空配列、上限超過を拒否する。

| `operator` | 成立条件 | 不成立条件 |
| --- | --- | --- |
| `equals` | 設計値と期待値のJSON型と値が同じ | 型または値が異なる |
| `not_equals` | 設計値と期待値のJSON型または値が異なる | 型と値が同じ |
| `contains_all` | 両値が文字列配列で、期待値の全要素が設計値に含まれる | 設計値が配列でない、または不足要素がある |
| `contains_none` | 両値が文字列配列で、共通要素がない | 設計値が配列でない、または共通要素がある |

集合比較の期待値が文字列配列でなければschema不正とする。同じ`subject`の設計値が文字列配列でない場合は
入力不正ではなく当該条件の`contradicted`とする。条件は`condition_id`順へ正規化する。

## 7. 判定と期待成果

### 7.1 条件ごとの判定

1. 同じ`subject`の設計事実がなければ`missing`。
2. 設計事実があり、§6.5の比較が成立すれば`satisfied`。
3. 設計事実があるが比較が成立しなければ`contradicted`。
4. 条件から参照された設計事実を使用済みとし、それ以外を未参照とする。

`missing`は項目不在だけ、`contradicted`は明示比較の不成立だけを表し、設計全体の誤りへ広げない。

### 7.2 正常結果

終了コード0で、入力自由値と絶対pathを含まず、次の項目だけを持つ正準JSON一件を返す。

- `status: comparison_completed`
- `schema_version: 1`
- `decision_status: pending_human_decision`
- `verdict`：欠落または矛盾があれば`review_required`、両方0件なら`conditions_met_pending_human_decision`
- `design`：`identifier`、`sha256`、`fact_count`
- `acceptance`：`identifier`、`sha256`、`condition_count`
- `comparison_sha256`
- `counts`：`satisfied`、`missing`、`contradicted`、`unreferenced_fact`
- `results`
- `unreferenced_fact_ids`
- `human_decision_queue`
- `external_send_approved: false`

各`results`は`condition_id`、`subject`、`disposition`、`fact_id`、`operator`、`expected_value_sha256`、
`actual_value_sha256`だけを持つ。`missing`の`fact_id`と`actual_value_sha256`はnullとする。値のSHA-256は
値単体の正準JSONから計算し、自由値自体は出力しない。

`results`は条件ID順、`unreferenced_fact_ids`は事実ID順とする。`human_decision_queue`は`contradicted`、`missing`、
`satisfied`、`unreferenced_fact`の順で、各項目は`kind`と昇順の`identifiers`だけを持つ。0件区分は省く。
満たした条件も人の判断一覧から外さない。

設計と受入条件のSHA-256は検査・正規化後の入力全体から計算する。`comparison_sha256`は、その欄だけを除く正常結果の
正準JSONから計算する。object項目順、事実順、条件順、文字列配列順だけの入力差では結果と内容識別値を変えない。

### 7.3 停止結果

成功成果を返さず非0終了コードとし、`status: stopped`、`reason`、`source`、`external_send_approved: false`だけを持つ
正準JSON一件を返す。

`source`は`arguments`、`design`、`acceptance`、`none`だけとする。引数・path不正は`arguments`、設計fileだけに
確定した読取り・size・UTF-8・schema不正は`design`、受入条件fileだけなら`acceptance`、入力fileを特定できない
読取り失敗と内部失敗は`none`とする。値、項目名、path、例外本文は返さない。

固定理由は`invalid_arguments`、`invalid_path`、`unreadable_input`、`size_limit_exceeded`、`invalid_utf8`、
`invalid_schema`、`internal_failure`だけとする。引数・path・読取り・size・UTF-8・schemaは終了コード2、内部失敗は4。

全JSONはUTF-8、BOMなし、項目名昇順、区切り前後の空白なし、直後に改行一つとする。標準エラーは常に空とし、
入力path、自由値、例外本文、入力抜粋を正常・停止出力へ含めない。

## 8. 実装候補の変更上限

案Cの製品変更は次に限定する。

1. 副作用のない照合核`tools/design/one_design_acceptance.py`。
2. 安全読取りと正式入口`tools/design/one_design_acceptance_entry.py`。
3. `pyproject.toml`への実行名一件。
4. 対象試験`tests/test_one_design_acceptance.py`。
5. 作業票、失敗・成功証拠、最終検証、独立確認、受入判断、TODO更新。

既存G08の2 path、関連試験2 file、既存schema、他製品処理を変更しない。必要になれば停止して契約改定を求める。

## 9. 受入条件

実装開始後は失敗試験を先に固定し、期待どおり失敗してから最小実装を行う。

1. 4比較それぞれに次の成立・不成立を固定する：`equals`の同値・値違い・型違い、`not_equals`の値違い・同値、
   `contains_all`の包含・不足・設計値非配列、`contains_none`の非交差・交差・設計値非配列。
2. 項目不在を`missing`、値違いを`contradicted`として区別する。
3. 受入条件の重複`subject`を入力不正とし、条件側競合を設計側矛盾へ混ぜない。
4. 未参照の全設計事実を一度ずつ残す。
5. 全条件成立時も自動受入せず、全条件を人の判断一覧へ残す。
6. 真偽値と整数など異なる型を同値にしない。
7. 項目順、事実順、条件順、文字列配列順だけでは結果と内容識別値を変えない。
8. 一つの値変更で対応する値、入力、照合結果の内容識別値が変わる。
9. rootと全入れ子のJSON同名項目、escape復号後同名、未知項目、重複ID・subject、不正識別子、禁止値型、
   空配列、件数超過を成功にせず、同名項目を正規化・SHA-256計算前に拒否する。
10. file system起点から入力rootと二fileまでの各途中要素・最後の要素のsymlink、root外、通常file以外、同じ二入力、
    読取不能、size超過、UTF-8不正を成功にしない。root自身だけの`O_NOFOLLOW`で途中要素を許す欠陥を検出する。
11. 事前検査後のpath差替えと読取り中のsize・identity変更を成功にせず、文字列path確認だけで安全としない。
12. 停止元を閉じた`source`で正しく示し、値、項目名、path、例外本文を出さない。
13. 正常・停止の標準出力へ自由値、絶対path、例外本文を含めず、標準エラーを空にする。
14. file変更、通信、外部process、Git、環境値解決、入力外探索を行わない。
15. 配布後の正式実行名を別の現在位置から実行しても同じbytesを返す。
16. 既存G08の2 pathと関連試験2 fileは基準commitから差分0で、関連31件が成功する。
17. 対象、関連、安全表示、正規全試験が各単独終了コード0で成功する。
18. 固定commitを別実行単位が読取り専用で確認し、誤合格、未接続条件、禁止作用、上位目的への悪影響が0件である。
19. 合成一件で内容識別値、件数、満たす・欠落・矛盾・未参照、人の判断一覧、安全表示を示す。
20. 利用者が実装結果と限界を確認後、製品処理として受け入れる。

## 10. 停止条件

- 自由文の意味推測がないと利用者価値が成立しない。
- 既存G08の2 path、関連試験、既存schemaの変更が必要になる。
- 通信、外部process、保存、Git、環境値解決、入力外探索が必要になる。
- 入力自由値または絶対pathを製品出力へ含める必要が生じる。
- `missing`と`contradicted`を固定規則から一意に区別できない。
- 未承認の設計・schema・既存試験変更、範囲拡大が必要になる。
- 対象、関連、安全表示、正規全試験または独立確認が不合格になる。

## 11. 影響と未実施

【判断】受入後は、構造化した設計一件と受入条件一式について、条件ごとの満たす・欠落・矛盾・未参照を
再現可能に確認できる。満たした条件も人の判断一覧へ残る。通信、保存、外部処理、既存G08の正式化は増えない。

【未実施】契約採用、実装、コード・試験・配布設定変更、既存G08変更、実利用者設計、外部送信、保存、
自由文解析、意味による同義判定、自動受入は行っていない。

## 12. 次の一作業

本候補を固定commitへ記録し、同じ独立担当が4訂正点と退行の有無だけを成果物変更なしで再確認する。
`開始可`となった後にだけ、利用者へ契約採用と案Cの実装開始を一判断として求める。
