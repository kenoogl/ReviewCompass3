# 一件の要求候補整合検査 作業契約候補 v2

- 契約ID：`TC-RC3-PRODUCT-ONE-REQUIREMENT-FEATURE-SOURCE-005`
- 契約版：2
- 契約種別：製品処理・G24の最初の縦切り
- 状態：`candidate_corrected_pending_limited_independent_review_and_human_approval`
- 作成日：2026-08-15
- 直前の製品契約：`TC-RC3-PRODUCT-ONE-DESIGN-ACCEPTANCE-CONFORMANCE-004`
- supersedes：`records/task-contract/2026-08-15-one-requirement-feature-source-candidate-v1.md`、SHA-256 `19702df3b5414b4e271ba30e6fb84ec285c887a98e189ed9bfd88e8ad2df6a25`
- 訂正根拠：`records/development/2026-08-15-one-requirement-feature-source-contract-v1-independent-review-v1.md`、SHA-256 `31d8227de940dc1aca264222cd25aad9870a0e6fb4fe16c954c109d11a6d7705`
- 訂正範囲：目的縮小の明示、全入力文字列の機微検査、正常・停止形式と内容識別値、再利用・保護基準
- 利用者判断：2026-08-15のG08正式受入、残る候補の自律実行、別担当AIによる独立確認の許可
- 実装状態：未開始
- 危険度：高
- 危険の理由：要求の由来と昇格判断に影響し、入力へ機微情報が含まれ得る
- 内容識別値：本候補固定後、独立再確認と利用者判断記録から参照する

「作業契約」は、一つの仕事の目的、入力、範囲、許可操作、期待結果、確認方法、停止条件を実装前に固定する約束である。
「原子義務」は、要求本文または要求内の一覧一項目として、出典対応を個別に確認する最小単位である。
「正準JSON」は、key昇順、区切り前後の空白なし、UnicodeをUTF-8の文字として保持する固定表現である。

## 1. 現行G24での位置

【記録】上位G24は、固定した要求資料から要求、機能区分、由来対応を一件分作る候補である。

【判断】本契約はG24全体ではない。構造化済みの要求候補、機能区分、出典採否、原子義務対応を利用者または別の文章作成処理が
用意した後に、その一件の整合だけを検査する最初の縦切りである。

- 要求文、機能区分、採否理由、出典対応の作成は本契約の入力前に行われ、製品処理は作成しない。
- G24の「固定資料から作成する」責務は未完了の後続として残す。
- 本契約の実装受入だけでは候補3を完了にしない。
- この縮小境界を採るかは、独立再確認後に利用者が契約採用と同時に判断する。

## 2. 目的

利用者が明示した出典一覧一件と構造化要求候補一件について、自由文の意味を補わず、次を決定的に確認する。

1. 出典一覧の全件に、採用または理由付き不採用がちょうど一つある。
2. 一つの要求が一つの機能IDへ属し、要求内の全原子義務が採用出典へ戻れる。
3. 採用出典は少なくとも一つの原子義務に使われ、不採用出典はどの義務にも使われない。
4. 機微情報候補を正常表示せず、結果を各構成物の内容識別値へ結ぶ。
5. 要求昇格と最終採否を人の判断として残す。

要求文、機能名、責務、採否理由の正しさは推測しない。出典の申告状態が`effective`でも、新しい要求候補を正式要求へ昇格しない。

## 3. 権威、証拠、上流不一致

| 役割 | path | SHA-256 |
| --- | --- | --- |
| 現行開発方針 | `docs/development/2026-08-02-development-policy.md` | `e3e6b0d2c7a1265f7cde2c2e00cc888f43d63ce0d1945c300b2b2e5f7730b559` |
| 直前製品の受入判断 | `records/development/2026-08-15-one-design-acceptance-product-acceptance-decision-v1.md` | `7e3eb626474f72ebcd3a3d5ec2646cf004ba192606f03684a50ae6f0b251ce86` |
| 次製品作業の候補一覧 | `records/development/2026-08-15-post-safe-storage-next-product-work-candidates-v1.md` | `bcb4ba2947e32254edc547068728fa580bc6b7919fa0f04d9b9353ab6c7899ba` |
| G24目録 | `records/development/2026-08-14-stage4-product-code-and-task-contract-input-inventory-evidence-v1.md` | `c55367fc6b8f72f7041612cedc11d609b359909156f619fcb72e6d72bd33e72a` |
| 契約定義証拠 | `records/development/2026-08-15-one-requirement-feature-source-contract-definition-evidence-v1.md` | `9d35dc70f5d96eb497bd8530ced4a1b32d5d838a6c0503f24668d8be719987c6` |
| 現行要求権限束v2 | `records/requirements/authority/rc3-requirements-authority-2026-08-03--v2.json` | `760e33ea2ecf6937f56d7bf8d2bd703b18b47dbd2bd6b2bd5919e0dd556d9dae` |
| 50要求の格納形式昇格判断 | `records/requirements/decisions/dec-requirements-unified-50-2026-08-03-v1.json` | `dd8b5dd15197da0a3463b3981d607da6edcb8318e17d91038786de7edc9eff27` |

【実測】要求権限束v2は既存解決処理で50要求を`effective`として返すが、人の判断は要求本文と受入真偽を承認範囲外とする。

【判断】`source_requirement_ids`は空とする。`REQ-CONTEXT-002`と`REQ-TRACE-002`は対応候補にとどめる。旧37要求、
旧機能分割、旧出典対応、旧完了記録も暫定資料のままとし、本製品から正式要求へ昇格しない。

## 4. 実装方法の3案

| 案 | 内容 | 単純さ・資源 | 頑健さ | 変更範囲・保守 | 判断 |
| --- | --- | --- | --- | --- | --- |
| A 既存機能だけ | 呼出し側がPython値を作り既存5検査を順に呼ぶ | 新規実装0、資源小 | 正式入口、安全読取り、全採否、未昇格表示が一組にならない | 変更0だが目的未達 | 不採用 |
| B 既存5 fileを正式化 | 旧固定入力照合を入口にし4検査を接続する | 接続は短いが全面修正が必要 | シンボリックリンク、型混同、未処理例外、暫定権限を持ち込む | 既存10 pathへ広く影響 | 不採用 |
| C 狭い専用検査 | 出典一覧と構造化済み候補だけを安全に読み、全採否・全義務対応・機能一致を検査する | 入力件数に比例し上限固定 | 意味推測をせず、未定義・未被覆・自動昇格を閉じる | 新規核・入口・試験・実行名だけ | 推奨 |

【提案】案Cを本縦切りの採用候補とする。G24の作成責務は別の後続契約で扱う。

## 5. 範囲

### 5.1 範囲内

- 一つの絶対入力root、出典一覧JSON一件、構造化済み要求候補JSON一件を読む。
- 各入力262,144 bytes以下、出典1〜256件、機能一件、要求一件、原子義務8〜225件とする。
- JSON同名項目、固定schema、識別子、文字、型、重複、件数、root内束縛、機微情報候補を検査する。
- 全出典の採否、全原子義務の出典対応、採用出典の消費、機能ID一致を検査する。
- 入力自由文を含めない正準JSON一件を表示する。

### 5.2 範囲外

- 要求文、機能区分、採否理由、出典対応の作成または自動修正。
- 自由文資料の読解、同義語、類似表現、意味の妥当性、申告状態の真実性の推測。
- 複数要求・複数機能の分割、重複、境界、依存の検査。
- 出典本文fileの読取り、directory探索、glob、再帰走査、暗黙資料、会話履歴全体。
- 外部AI、通信、外部送信、外部process、Git、環境値解決、認証、再試行。
- 入力・結果の保存、file作成・書換え、権限変更、削除。
- 要求権限束への登録、正式昇格、最終採否。
- 既存G24、旧第4段成果物、現行50要求、G08、G30の変更または正式化。

## 6. 固定再利用部品と保護基準

### 6.1 G08安全読取り

受入済みG08製品commitは`1fec2475dfd50898edd22cb28f866952b764d2e0`である。実装開始前と完了時に次の一致を確認する。

| path | SHA-256 |
| --- | --- |
| `tools/design/one_design_acceptance.py` | `b3af7fdf254b21e5d368f2a02cf2aba23a86233a67b4120e7c2b39a3fd4a5c14` |
| `tools/design/one_design_acceptance_entry.py` | `7535aa6652514c6ce4dfd31facd2640944a356ddc04802b0df8ae63a9bec9823` |
| `tests/test_one_design_acceptance.py` | `6adc44ad7c7c9dff37ad3e671abfc0e86d9c5afe53861f2edeafc7acd01e1542` |

新しい入口は`tools.design.one_design_acceptance.read_input_pair`だけを再利用し、G08を変更しない。内部停止元`design`を
`catalog`、`acceptance`を`candidate`へ閉じて変換する。G08の他の比較処理と正式入口は呼ばない。

### 6.2 機微情報候補検査

`tools/session_logs/redaction.py`、SHA-256
`aa49774a447d84422ec885a908bb52c7a3732eb67ddb53dcc1c03fbc149245bd`の公開`default_pattern_rules`と
`find_high_entropy`だけを再利用する。既定patternは5件、規則内容識別値は
`3c736257fc01740dbd8e5b3eba53c810b401640cae7c31201cbc0b85840bd328`である。

環境依存規則の解決、伏字化、file書込みは呼ばない。このfile、公開関数、既定引数、規則内容識別値の変更は安全試験をstaleにし、
契約改定まで実装を止める。

### 6.3 G24保護対象

保護基準commitを`0583863e4612f7f14b5db131beb627677b99017a`とする。

| path | SHA-256 |
| --- | --- |
| `tools/requirements/boundary_relations.py` | `31ae6b8edfde022300a817ec3d9d553ddb3f64d71a92a3d95c35e01a8e40e869` |
| `tools/requirements/feature_partition.py` | `0796d436b7f6c3e075b998f1d80451ea59d3cb3cc6b77e6ef3084f9ffbecec2a` |
| `tools/requirements/fixed_inputs.py` | `60cfdef9e5d506fcb9519a00a02e83ed379f87a290aa34a50051d716c0354c9b` |
| `tools/requirements/requirement_batch.py` | `2e91889620ae18e2b49b856939d07102429b9d07d24b707fcd9d4b1ecb6f3986` |
| `tools/requirements/source_trace.py` | `7919f0baac5eabac3bb937fbb9264193c4ad31735a78cba4b07207f52fd282b3` |
| `tests/test_requirements_feature_partition.py` | `ec7908934b15de8a65878a9172fddfe6684db0fd66b00b87f2930fb8c95854d5` |
| `tests/test_requirements_fixed_inputs.py` | `529b4ad7b985173845d2e0404dbd991542397a10617e6fe79dfd4feb809d3111` |
| `tests/test_requirement_boundary_relations.py` | `00cbd919baf8c98d295e45007b136b48dda13596d78daeace262b638c30fb50d` |
| `tests/test_requirements_source_trace.py` | `9f04b748882ade1626e125cc78700850d0f1eeeb92c6202e0234de06e0f978c5` |
| `tests/test_requirements_batch.py` | `43e6ba7815a7c839b611e0d9f49d317b82c60fd7d3eb588545cc2810f663934b` |

## 7. 安全読取りと許可能力

正式実行名候補は`reviewcompass3-requirement-candidate-check`で、入口は次だけとする。

`check --input-root <絶対path> --catalog <絶対path> --candidate <絶対path>`

引数不足、未知・重複引数、相対pathは読取り前に拒否する。位置指定引数はroot内束縛にだけ使い、内容検査、内容識別値、
正常・停止表示へ含めない。

安全読取りは§6.1の関数をそのまま使う。file system起点から全構成要素を非追跡で開き、通常file、size、機器番号、inode、
読取り前後一致、実読取りbyte数、二入力が異なるfileであることを確認する。

許可する能力は、指定二fileの読取り、UTF-8復号、JSON検査、機微情報候補検査、正準JSON、SHA-256、集合、件数、並べ替え、
正常または停止JSON一件の標準出力だけである。

file書込み、directory作成、通信、外部process、Git、環境値解決、権限変更、削除、外部送信、任意コード実行、入力外探索を禁止する。

## 8. 入力形式

### 8.1 共通規則

- rootと全入れ子objectでescape復号後の同名項目を禁止し、通常dictへ変換する前に検出する。
- `schema_version`は`type(value) is int`を満たす整数`1`だけとする。
- 未知項目、浮動小数点数、null、自由なobject追加、入れ子配列を禁止する。
- 一般IDはASCII正規表現`[A-Za-z0-9][A-Za-z0-9._-]{0,127}`だけとする。
- 機能IDは`FEAT-[A-Z0-9]+(?:-[A-Z0-9]+)*`、要求IDは`REQ-[A-Z0-9]+(?:-[A-Z0-9]+)*-[0-9]{3,}`とする。
- SHA-256は`[0-9a-f]{64}`だけとする。
- 自由文はUnicode scalar valueを1文字として数え、1〜2,000文字、NULなしとする。
- 一覧自由文は各1〜500文字、復号後完全一致の重複なし、各一覧1〜32件とする。

### 8.2 機微情報候補の検査順

1. JSONのUTF-8、構文、同名項目を検査する。
2. 復号後の全利用者入力文字列keyと値を、深さ優先で入力順に検査する。
3. 出典一覧の正確な位置`/sources/{0-based-index}/sha256`にあり、先に`[0-9a-f]{64}`へ合格した値だけを検査対象から外す。
4. それ以外の64桁16進文字列、ID、未知key、自由文、採否理由を除外しない。
5. §6.2の既定patternを宣言順に検査し、その後`find_high_entropy`の既定値、最低24文字・entropy 3.5で検査する。
6. catalogをcandidateより先に検査する。最初の一致で値を表示せず停止する。

検査は全ての秘密を発見できるとは主張しない。既定patternと高乱雑性検査の限界を正常結果に固定表示する。

### 8.3 出典一覧JSON

rootは`schema_version`、`catalog_identifier`、`sources`だけを持つ。`sources`は1〜256件で、各項目は
`source_id`、`sha256`、`declared_status`だけを持つ。出典IDは一意とする。

`declared_status`は`effective`、`approved_context`、`candidate`、`historical`だけとする。これは入力作成者の申告であり、
外部権限記録を探索して確認した値ではない。出典は`source_id`順へ正規化する。

### 8.4 要求候補JSON

rootは`schema_version`、`candidate_identifier`、`feature`、`requirement`、`source_dispositions`、
`obligation_sources`だけを持つ。

`feature`は`feature_id`、`name`、`responsibility`、`non_goals`だけを持つ。`non_goals`は1〜32件で入力順を保持する。

`requirement`は`requirement_id`、`feature_id`、`statement`、`inputs`、`outputs`、`stop_conditions`、
`recovery_conditions`、`preserved_artifacts`、`acceptance_criteria`、`non_goals`だけを持つ。七一覧は各1〜32件で入力順を保持する。
要求の`feature_id`は`feature.feature_id`と一致する。

`source_dispositions`は各`source_id`、`disposition`、`rationale`だけを持つ。`disposition`は`selected`または
`not_selected`だけである。出典一覧の全IDがちょうど一度現れ、未知ID、欠落、重複を禁止する。出典ID順へ正規化する。

`obligation_sources`は各`obligation_id`、`source_ids`だけを持つ。原子義務IDは本文を
`{requirement_id}#statement`、七一覧を`{requirement_id}#{field}.{1-based-index:03d}`とする。
全原子義務がちょうど一度現れる。各`source_ids`は1〜256件、重複なし、採用出典だけを参照する。
全採用出典は少なくとも一つの原子義務から参照される。義務ID順、各出典ID順へ正規化する。

## 9. 正規化と内容識別値

正準JSON bytesは`json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")`と同じとする。
BOMを付けず、内容識別値計算へ改行を含めない。

| 名前 | 計算対象 |
| --- | --- |
| `catalog.sha256` | `schema_version`、`catalog_identifier`、出典ID順の全`sources`を持つ正規化済み出典一覧root |
| `candidate.sha256` | §8.4の全項目を持ち、採否と対応だけを正規化した要求候補root |
| `feature.sha256` | `feature_id`、`name`、`responsibility`、入力順の`non_goals`を持つfeature object |
| `requirement.sha256` | §8.4の全requirement項目を持ち、七一覧を入力順で保持するrequirement object |
| `trace_sha256` | `schema_version: 1`、理由を含む正規化済み`source_dispositions`、正規化済み`obligation_sources`だけを持つobject |
| `result_sha256` | `result_sha256`欄だけを除いた§10の正常結果root |

object項目順、出典順、採否順、対応順、対応内出典順だけの差では各内容識別値を変えない。featureの`non_goals`と
requirementの七一覧の順序変更は原子義務の意味を変えるため内容識別値を変える。

## 10. 正常結果

終了コード0で、次のroot項目だけを持つ正準JSON一件と直後のLF一つを標準出力へ返す。標準エラーは空とする。

- `status: requirement_candidate_checked`
- `schema_version: 1`
- `decision_status: pending_human_decision`
- `promotion_status: not_promoted`
- `verdict`
- `catalog`
- `candidate`
- `feature`
- `requirement`
- `counts`
- `source_dispositions`
- `obligation_sources`
- `trace_sha256`
- `result_sha256`
- `human_decision_queue`
- `limitations`
- `external_send_approved: false`

各objectの完全な形は次である。

- `catalog`：`identifier`、`sha256`、`source_count`だけ。
- `candidate`：`identifier`、`sha256`だけ。
- `feature`：`identifier`、`sha256`だけ。
- `requirement`：`identifier`、`sha256`、`obligation_count`だけ。
- `counts`：`approved_context_sources`、`candidate_sources`、`effective_sources`、`historical_sources`、
  `not_selected_sources`、`selected_sources`、`traced_obligations`だけ。申告状態別件数は採否と無関係に全出典を数える。
- `source_dispositions`：出典ID順に、各`source_id`、`declared_status`、`disposition`だけ。
- `obligation_sources`：義務ID順に、各`obligation_id`、昇順の`source_ids`だけ。

`human_decision_queue`の各項目は`kind`と非空の昇順`identifiers`だけを持ち、次の順とする。

1. 常に`kind: requirement_candidate`、`identifiers: [candidate_identifier]`。
2. 採用した候補出典があれば`kind: candidate_source_selection`とその出典ID。
3. 採用した履歴出典があれば`kind: historical_source_selection`とその出典ID。

存在しない2または3は省く。`verdict`は2または3があれば`review_required_pending_human_decision`、なければ
`trace_complete_pending_human_decision`とする。

`limitations`は`source_status_not_verified`、`semantic_correctness_not_verified`、
`multi_requirement_partition_not_verified`、`authority_not_changed`、`sensitive_detection_not_exhaustive`の順に固定する。

正常結果へ入力自由文、採否理由、出典SHA-256、絶対path、例外本文、機微検査の一致値を含めない。

## 11. 停止結果と優先順

停止結果は`status: stopped`、`reason`、`source`、`external_send_approved: false`だけを持つ正準JSON一件とLF一つである。
標準エラーは空とし、入力値、key、path、例外本文を含めない。

処理順は、引数検査、二file安全読取り、catalog復号、candidate復号、catalog機微検査、candidate機微検査、catalog schema、
candidate schema、相互参照、被覆、正常結果作成である。同じ段階では入力順または§8の項目順で最初の違反を返す。

| 違反 | `reason` | `source` | 終了コード |
| --- | --- | --- | ---: |
| subcommand、引数の不足・未知・重複 | `invalid_arguments` | `arguments` | 2 |
| 相対path、root外、空・`.`・`..`要素、同一pathまたは同一file | `invalid_path` | `arguments` | 2 |
| root自体の非追跡open不能 | `unreadable_input` | `none` | 2 |
| catalogのsymlink、非通常file、読取不能、読取り前後不一致 | `unreadable_input` | `catalog` | 2 |
| candidateの同じ違反 | `unreadable_input` | `candidate` | 2 |
| catalogのsize上限超過 | `size_limit_exceeded` | `catalog` | 2 |
| candidateのsize上限超過 | `size_limit_exceeded` | `candidate` | 2 |
| catalogのUTF-8不正 | `invalid_utf8` | `catalog` | 2 |
| candidateのUTF-8不正 | `invalid_utf8` | `candidate` | 2 |
| catalogのJSON構文・同名項目・固定schema・型・文字・件数違反 | `invalid_schema` | `catalog` | 2 |
| candidateの同じ違反 | `invalid_schema` | `candidate` | 2 |
| catalogの機微情報候補 | `sensitive_data_remaining` | `catalog` | 3 |
| candidateの機微情報候補 | `sensitive_data_remaining` | `candidate` | 3 |
| 機能ID不一致、未知出典・義務、不採用出典参照 | `unresolved_reference` | `candidate` | 2 |
| 採否または義務対応の欠落、重複、未消費採用出典 | `incomplete_coverage` | `candidate` | 2 |
| 上記へ分類できない内部例外 | `internal_failure` | `none` | 4 |

機微検査はschema検査より先なので、未知keyに機微情報候補がある場合も`sensitive_data_remaining`を返す。構文・同名項目で
復号できない場合だけ`invalid_schema`を先に返す。SHA-256除外位置の形を判断できない場合は除外せず機微検査する。

## 12. 変更上限

製品変更は次に限定する。

1. 副作用のない検査核`tools/requirements/one_requirement_feature_source.py`。
2. G08安全読取りを再利用する入口`tools/requirements/one_requirement_feature_source_entry.py`。
3. `pyproject.toml`への実行名一件。
4. 対象試験`tests/test_one_requirement_feature_source.py`。
5. 作業票、失敗・成功証拠、最終検証、独立確認、受入判断、TODO更新。

§6の固定部品・保護10 path、旧第4段成果物、要求schema、現行50要求、他製品処理を変更しない。必要なら契約改定へ戻る。

## 13. 受入条件

実装開始後は失敗試験を先に固定し、期待どおり失敗してから最小実装を行う。

1. 一機能・一要求・出典三件の正例で、全出典の採否、全原子義務対応、採用出典の消費を一度ずつ示す。
2. 採否欠落・重複・未知出典・空理由、義務対応欠落・重複・未知義務・空出典を契約表どおり停止する。
3. 未定義出典、不採用出典参照、未消費採用出典、機能ID不一致を契約表どおり停止する。
4. 七一覧の欠落・空・重複、各件数境界と総義務上限を確認する。
5. 全義務が対応しても自動昇格せず、人の判断待ちと固定限界5件を返す。
6. 候補・履歴出典の採用を固定順の人の判断一覧へ残し、申告状態から権限を推測しない。
7. §10の全root・入れ子項目、配列順、件数、verdictを完全一致で確認する。
8. object項目順、出典順、採否順、対応順、対応内出典順だけでは正常bytesと全内容識別値を変えない。
9. 要求本文、一覧一項目、採否理由、出典SHA-256の一変更で§9どおり対応する内容識別値が変わる。
10. 各内容識別値を独立oracleで§9の正確な計算対象から再計算する。
11. JSON同名項目、escape後同名、未知項目、真偽値の版、浮動小数点、単独サロゲート、不正ID・SHA-256、
    禁止型、件数・文字長超過を未処理例外なしで停止する。
12. AWS鍵形式、email、bearer token、API key代入、秘密鍵block、高乱雑性tokenをcatalogとcandidateのkey・値・IDで停止し、
    正しいSHA-256欄だけを高乱雑性検査から外す。
13. §6.2のfile、公開関数、規則内容識別値を実行前後に照合し、環境依存規則を解決しない。
14. rootから二fileまでの全symlink、root外、非通常file、同一file、読取不能、size超過、UTF-8不正、読取り中変更を停止する。
15. §11の全行について`reason`、`source`、終了コード、空stderr、値・path・例外非表示を確認する。
16. file変更、通信、外部process、Git、環境値解決、入力外探索を行わない。
17. 配布後の正式実行名を別の現在位置から実行しても同じbytesを返す。
18. G08固定3 fileが§6.1と一致し、`.venv/bin/python3 -m pytest -q tests/test_one_design_acceptance.py`が成功する。
19. G24保護10 pathが§6.3と一致し、次の単独commandが59件成功する。

`.venv/bin/python3 -m pytest -q tests/test_requirements_feature_partition.py tests/test_requirements_fixed_inputs.py tests/test_requirement_boundary_relations.py tests/test_requirements_source_trace.py tests/test_requirements_batch.py`

20. 次の単独commandが21件成功し、現行要求権限束v2が50要求を`effective`として返す。

`.venv/bin/python3 -m pytest -q tests/test_requirements_artifact_layout.py tests/test_requirements_unified_migration.py`

21. 対象、安全表示、関連、正規全試験を各単独終了コード0で成功させ、固定commitを別担当が誤合格・未接続・禁止作用・
    上位目的への悪影響0件として確認する。
22. 合成一件で全内容識別値、件数、全採否、全義務対応、未昇格、人の判断一覧、安全表示を示す。
23. 利用者が「G24全体ではなく最初の整合検査縦切りである」限界、実装結果、後続未完了を確認して製品処理を受け入れる。

## 14. 停止条件

- 整合検査だけでは最初の縦切りとして価値がないと利用者が判断する。
- 自由文の意味推測、要求作成、複数要求間の分割が本縦切りに必要になる。
- §6の固定部品または保護対象の変更が必要になる。
- 通信、外部process、保存、Git、環境値解決、入力外探索が必要になる。
- 入力自由文、機微情報候補、絶対pathを製品出力へ含める必要が生じる。
- 出典の採否、義務対応、採用出典の消費を固定規則から一意に確認できない。
- 未承認のschema・既存試験変更、範囲拡大が必要になる。
- 対象、関連、安全表示、正規全試験または独立確認が不合格になる。

## 15. 影響、未実施、次作業

【判断】受入後は、構造化済み要求候補一件について、全出典の採否、各原子義務から固定出典への対応、一機能への所属を
再現可能に検査できる。要求作成、意味判断、要求昇格、通信、保存、既存G24の正式化は増えず、G24全体は未完了のまま残る。

【未実施】契約採用、縮小境界の利用者判断、実装、既存成果物変更、現行要求変更、実利用者資料、外部送信、保存は行っていない。

次は本候補と独立確認記録を固定commitへ記録し、同じ別担当が4訂正点と退行だけを成果物変更なしで再確認する。
`開始可`になった後にだけ、利用者へ「最初の整合検査縦切りの採用」と案Cの実装開始を一判断として求める。
