# 一件のレビュー材料作成と結果整理 作業契約候補 v3

- 契約ID：`TC-RC3-PRODUCT-ONE-ITEM-REVIEW-003`
- 契約版：3
- 契約種別：製品処理
- 状態：`candidate_corrected_pending_limited_independent_review_and_human_approval`
- 作成日：2026-08-15
- 直前の製品契約：`TC-RC3-PRODUCT-SESSION-ARTIFACT-SAFE-STORAGE-002`
- supersedes：`records/task-contract/2026-08-15-one-item-review-material-and-result-organization-candidate-v2.md`、SHA-256 `60b8703e5a361eb7f509ecdb7532c1b928450bf55aea5c2eb9814020046d3e37`
- 利用者判断：2026-08-15の「では、一件のレビュー材料作成と結果整理に取りかかる」
- 訂正理由：候補v2で残った、必須path引数と内容検査の衝突、配列順・指摘署名・絶対path境界の未固定
- 訂正根拠：`records/development/2026-08-15-one-item-review-task-contract-definition-correction-review-v1.md`、SHA-256 `8544484e25c7af07743002793c63a591aa3ad63c2dd09ce74f512fead4899a1f`
- 実装状態：未開始
- 危険度：高
- 危険の理由：資料とレビュー結果に機微情報が含まれ得る。外部送信は行わないが、誤った画面出力でも情報を露出し得る
- 内容識別値：本候補を固定した後、定義挑戦と利用者判断記録から参照する

## 1. 権威、証拠、暫定候補を分ける

### 1.1 現在の権威

| 役割 | path | SHA-256 |
| --- | --- | --- |
| 立て直し計画v5と第5段の完了 | `records/development/2026-08-14-recovery-plan-v5-stage5-completion-decision-v1.md` | `4c50bdf643c12e3c4fb02c78d3fe47de20885efab4b8b9b34dbd946c763da3b0` |
| 現行開発方針 | `docs/development/2026-08-02-development-policy.md` | `e3e6b0d2c7a1265f7cde2c2e00cc888f43d63ce0d1945c300b2b2e5f7730b559` |
| 安全保存の製品受入判断 | `records/development/2026-08-15-session-artifact-safe-storage-product-acceptance-decision-v1.md` | `7145f57a59efb965f64a5401f6e109685ba1920b5039fe65a4edd644af7573dc` |
| 次製品作業の候補一覧 | `records/development/2026-08-15-post-safe-storage-next-product-work-candidates-v1.md` | `bcb4ba2947e32254edc547068728fa580bc6b7919fa0f04d9b9353ab6c7899ba` |

【記録】候補一覧は、G02全体ではなく「固定資料一件のレビュー材料作成と、外部送信なしの結果整理」だけを
次の第一候補とした。利用者は本候補の作成開始を指示したが、契約採用、実装開始、外部送信、外部処理を承認していない。

### 1.2 固定証拠

| 役割 | path | SHA-256 |
| --- | --- | --- |
| G02を14 path・関連試験18 fileとして分けた目録 | `records/development/2026-08-14-stage4-product-code-and-task-contract-input-inventory-evidence-v1.md` | `c55367fc6b8f72f7041612cedc11d609b359909156f619fcb72e6d72bd33e72a` |
| 製品目的の候補 | `docs/current/reviewcompass3-intent-current.md` | `1950f5a37fb5d0d0554f56343b39bbca7fc635523409f10ee761d8cef68f9ec6` |
| 統合製品計画候補 | `docs/current/reviewcompass3-plan-current.md` | `1a73597605eafb65a2259ccf19431e3aba041564d03fdb279150042a9bd0962f` |
| Review Context要求候補 | `docs/requirements/review-context-requirements.md` | `0622d8b1cc80e0c23119b78bd137c90e8e1c621bc0fde2e99f8a82e71e76ac23` |
| 所見整理要求候補 | `docs/requirements/remaining-feature-requirements.md` | `ec31ce53ce097a8ff8a59a4649d97e4af8d8dd0cbdb8a1a8c7d4e8d2a1f8bcf6` |

【実測】G02の既存14 pathは、目録が観測したcommit
`66d608e5b5d605ddaf387bbd75a507ac934800c6`から現在まで差分0である。材料固定、応答解析、所見整理の
部品を持つ一方、全fileが`provisional / non-normative / promotion_required: true`であり、外部実行、raw結果保存、
二担当経路を前提にした一括処理へ結び付いている。

【判断】上表の製品目的、製品計画、要求は暫定候補であり、本契約の正式な要求正本へ昇格しない。現在の正式責務は、
立て直し計画、第5段完了後の製品受入履歴、次候補一覧、今回の利用者指示から狭く導く。

## 2. 識別

| 項目 | 値 |
| --- | --- |
| `task_contract_id` | `TC-RC3-PRODUCT-ONE-ITEM-REVIEW-003` |
| `contract_type` | `product_delivery` |
| `version` | 3 |
| 正式な責務の出所 | 第5段完了判断、安全保存受入後の候補一覧、2026-08-15の利用者指示 |
| `source_requirement_ids` | なし。正式採用済みRequirementが存在しないため空とする |
| 対応候補 | `REQ-CONTEXT-001`、`002`、`004`、`005`、`REQ-TRIAGE-001`、`002` |
| 直前契約ID | `TC-RC3-PRODUCT-SESSION-ARTIFACT-SAFE-STORAGE-002` |
| supersedes | 候補v2、SHA-256 `60b8703e...e37` |
| 訂正根拠 | v2変更点確認、SHA-256 `8544484e...a1f` |
| 記録形式 | Markdown候補。G30の未完成schema、生成器、状態機械を使わない |

## 3. 責務

利用者が明示した安全な資料一件について、次を読取り専用の二操作で行う。

1. `prepare`は、資料本文、利用者が指定した表示用識別子、目的、確認基準、制約を一つのレビュー材料へ組み立てる。
2. レビュー材料は本文と各入力のSHA-256を含み、自己の内容識別値欄を除く正準JSON全体のSHA-256へ固定する。
3. `organize`は、同じレビュー材料の内容識別値に結ばれた、別途与えられた一件以上のレビュー結果を検査する。
4. 担当別の結論、要約、指摘件数を失わず、指摘を一致、競合、単独報告、重複の可能性、証拠不足へ整理する。
5. 整理結果は入力結果の内容識別値へ逆引きでき、同じ入力から同じbytesを再生成できる。
6. 最終採否は自動決定せず、整理結果を`pending_human_decision`として利用者へ返す。

ここでいう「内容識別値」は、入力の正準JSONまたは本文bytesからSHA-256で計算する改変検出用の値である。
ここでいう「正準JSON」は、key順、区切り、文字表現を一つに固定したJSONである。

【判断】本契約はレビューそのものを実行しない。レビュー材料を外部へ送らず、既に手元へある結果だけを整理する。
結果が一件だけの場合も受け付けるが、その指摘は他結果との一致が確認されていない`single_report`として残す。

## 4. 境界

### 4.1 範囲内

- 一つの明示された`input_root`内にある、空でないUTF-8の通常file一件を対象資料として読む。NULを含む本文は拒否する。
- 同じroot内にあるレビュー条件JSON一件を読む。
- `organize`では、同じroot内にある結果集合JSON一件を追加で読む。
- 資料は最大262,144 bytes、条件JSONは最大65,536 bytes、結果集合JSONは最大1,048,576 bytesとする。
- レビュー条件は、表示用識別子、目的、1件以上16件以下の確認基準、0件以上16件以下の制約を持つ。
- 結果集合は1件以上8件以下の担当別結果、全体で100件以下の指摘を持つ。
- 結果の厳格検査、内容識別値計算、決定的な並べ替え、標準出力へのJSON一件の表示。

### 4.2 範囲外

- 複数資料、directory探索、glob、再帰走査、会話履歴全体、暗黙の参考資料。
- レビューの実行、外部AI、外部送信、network、外部process、provider選択、認証、再試行。
- raw応答の取得・保存、結果fileの作成・書換え、材料または整理結果の永続保存。
- 意味が似ているだけの別表現を、自動で同じ指摘と確定すること。
- 指摘の採用・不採用、修正方針、完了、受入を自動決定すること。
- G02の既存一括処理、G04の旧不変保存、G20の外部送信、G30の状態管理の正式採用。
- 安全保存をレビュー結果の保存へ転用すること。承認済み安全保存はSession記録専用である。
- 設定探索、環境変数、home、利用者名、host名、Git情報から入力を推測すること。

## 5. 前提

- 本契約候補の定義挑戦、契約採用、実装開始を利用者が順に承認している。
- `input_root`、資料file、条件JSON、結果集合JSONは全て絶対pathで明示される。
- 各入力fileは解決後に`input_root`内にあり、rootからfileまでの構成要素にsymlinkがなく、通常fileである。
- 資料file、条件JSON、結果集合JSONは互いに異なるfileである。
- 入力rootとfileは読取り可能である。製品処理は所有者、mode、ACLを変更しない。
- 利用者は資料一件をこの端末画面へ表示してよいと確認済みである。
- schemaで形式を確認したSHA-256欄を除き、資料本文と、条件JSON・結果集合JSONを復号した後の全ての文字列key・値に
  機微情報候補または絶対pathがあれば、処理は伏字化して続行せず停止する。
- `input_root`、資料file、条件JSON、結果集合JSONの位置指定引数は、root内束縛と安全なfile読取りにだけ使う。
  内容検査の対象、内容識別値、成功・停止出力へ含めない。
- 本検査は全ての機微情報を発見できるとは主張しない。既定pattern、高い乱雑性を持つ長いtoken、POSIXとWindowsの
  絶対pathを検査し、検査限界を出力形式の版と結ぶ。
- schemaで位置と形式が固定されたSHA-256欄だけは、64桁の小文字16進数であることと参照値への一致を先に検査し、
  高い乱雑性を持つtokenの検査対象からだけ外す。自由記述中の64桁文字列は除外しない。
- 結果作成者は共通の`issue_key`を付ける。同じ問題を同じkeyへ対応させる意味判断は、結果作成側の責務である。

## 6. 必要材料

| 材料 | 必須性 | 充足条件 |
| --- | --- | --- |
| 第5段完了判断 | 必須 | §1.1のSHA-256一致 |
| 次製品作業の候補一覧 | 必須 | §1.1のSHA-256一致、候補1の狭域境界を維持 |
| G02の目録 | 必須 | §1.2のSHA-256一致、既存14 pathを暫定のまま扱う |
| 対象資料 | 実行時必須 | 一件、UTF-8、size上限内、利用者の画面表示許可、機微情報検査合格 |
| レビュー条件 | 実行時必須 | 固定schema、必須項目、基準件数、機微情報検査合格 |
| 結果集合 | `organize`時必須 | 固定schema、材料の内容識別値一致、1〜8結果、全指摘100件以下 |
| 実利用者資料 | 定義・通常試験では不要 | 合成fixtureだけを使う |
| 暫定の製品目的・要求 | 参考 | 暫定表示を維持し、正式要求へ昇格しない |

## 7. 許可する能力

- 明示されたroot、資料file、条件JSON、結果集合JSONの検査と読取り。
- file descriptorを用いたsymlink非追跡の読取りと、読取り後の種類・sizeの再確認。
- UTF-8 decode、固定schema検査、SHA-256欄以外の資料本文と復号済みJSONの全文字列key・値に対する
  機微情報候補と絶対pathの検査。位置指定引数は対象外とする。
- SHA-256、正準JSON、行数、件数、一致、競合、単独報告、重複可能性の決定的計算。
- 成功または停止を示すJSON一件の標準出力と、固定した終了区分の返却。

禁止する能力は、file書込み、directory作成、network、外部process、Git、環境値解決、権限変更、削除、外部送信、
任意コード実行、入力file以外の探索である。

## 8. 入力と期待成果

正式実行名の候補は`reviewcompass3-one-item-review`とし、次の二入口だけを持つ。

- `prepare --input-root <絶対path> --material <絶対path> --review-spec <絶対path>`
- `organize --input-root <絶対path> --material <絶対path> --review-spec <絶対path> --results <絶対path>`

引数の不足、未知引数、相対pathは処理前に拒否する。利用者が与えたpathを標準出力または標準エラーへ表示しない。

### 8.1 レビュー条件

レビュー条件JSONは次の項目だけを持つ。

- `schema_version: 1`
- `material_identifier`：pathではない安全な表示名。1〜128文字。
- `goal`：何を確認するかを示す1〜2,000文字の文。
- `criteria`：`id`と`text`を持つ1〜16件。IDは重複不可。
- `constraints`：0〜16件の文。

`material_identifier`、基準ID、`reviewer_id`、`finding_id`、`issue_key`は、英数字で始まり、以後を英数字、
`.`、`_`、`-`に限る1〜128文字の識別子とする。未知key、空文字、NUL、改行を含む識別子、重複した基準ID、
上限超過を拒否する。

### 8.2 `prepare`の正常結果

終了コード0で、rootに次のkeyだけを持つ正準JSON一件を返す。

- `status: material_prepared`
- `schema_version: 1`
- `material`：`identifier`、`content`、`content_sha256`、`line_count`だけを持つ。
- `review_spec`：`goal`、ID順の`criteria`、指定順の`constraints`、`sha256`だけを持つ。
  各criterionは`id`と`text`だけを持つ。
- `result_schema`：`schema_version: 1`、`grouping_basis: supplied_issue_key`、
  `semantic_deduplication_performed: false`だけを持つ。
- `material_package_sha256`。
- `external_send_approved: false`。

入力の絶対path、root、file名の自動抽出値、機微情報検査の一致箇所、環境値を返さない。
この出力は外部送信の承認ではなく、利用者の手元で確認する固定材料である。
未知keyと追加keyをrootと全ての入れ子で禁止する。`material_package_sha256`は、その欄だけを除いた正常結果の
正準JSON bytesから計算する。基準はID順に並べる。
制約は利用者が指定した順序を意味のある入力として保つ。条件JSONの内容識別値は、検査後の条件を正準JSONへ変換して
計算する。資料の行数は、空でない本文へ`splitlines()`相当を適用した件数とする。

### 8.3 結果集合

結果集合JSONのrootは次だけを持つ。

- `schema_version: 1`
- `material_package_sha256`
- `reviews`

各reviewは次だけを持つ。

- `reviewer_id`：結果集合内で一意な安全な識別子。
- `verdict`：`findings_present`、`no_findings`、`insufficient_evidence`のいずれか。
- `summary`：結論を失わずに示す文。
- `findings`：指摘の配列。

各findingは次だけを持つ。

- `finding_id`：同じreview内で一意な識別子。
- `issue_key`：複数結果で同じ問題を対応させる共通key。同じreview内で一意。
- `severity`：`error`、`warning`、`info`のいずれか。
- `title`、`description`。
- `criterion_ids`：レビュー条件に存在する基準IDを1件以上。
- `start_line`、`end_line`：資料の実在する行範囲。

`no_findings`と`insufficient_evidence`は指摘0件、`findings_present`は指摘1件以上とする。
未知key、別材料の内容識別値、未知の基準、同じfinding内の重複した基準ID、範囲外の行、重複ID、空の結果集合を拒否する。

### 8.4 `organize`の正常結果

終了コード0で、資料本文を含まず、rootに次のkeyだけを持つ正準JSON一件を返す。

- `status: results_organized`
- `schema_version: 1`
- `decision_status: pending_human_decision`
- `material`：`identifier`、`content_sha256`、`material_package_sha256`だけを持つ。
- `result_set_sha256`。
- `reviews`：担当別に`reviewer_id`、`review_sha256`、`review_content_sha256`、`verdict`、`summary`、
  `finding_count`だけを持つ。`review_content_sha256`は`reviewer_id`だけを除くreviewの正準JSONから計算する。
- `counts`：`review_count`、`finding_count`、`issue_count`だけを持つ。
- `issue_groups`：各群は`issue_key`、`disposition`、`reporters`、`findings`だけを持つ。各findingは
  `reviewer_id`、`finding_id`、`severity`、`title`、`description`、`criterion_ids`、`start_line`、`end_line`だけを持つ。
- `possible_duplicate_reviews`：同じ`review_content_sha256`を持つ二件以上の`reviewer_ids`と当該SHA-256だけを持つ。
- `possible_duplicate_keys`：完全一致した指摘署名のSHA-256と、異なる`issue_keys`だけを持つ。
- `insufficient_evidence_reviewers`、`unresolved_issue_keys`。
- `human_decision_queue`：各項目は`kind`、`identifiers`、`reason`だけを持つ。
- `grouping_basis: supplied_issue_key`、`semantic_deduplication_performed: false`。
- `external_send_approved: false`。

未知keyと追加keyをrootと全ての入れ子で禁止する。各入力reviewの`review_sha256`は`reviewer_id`を含む正準JSON、
`review_content_sha256`は`reviewer_id`だけを除く正準JSONから計算する。

同じ`issue_key`が一件だけなら`single_report`とする。同じkeyが複数結果にあり、severity、title、description、
基準ID集合、開始行、終了行の全てが同じなら`matching_reports`とする。いずれかが異なれば`conflict`とする。
finding IDとreporter IDは指摘内容の一致対象に含めない。`matching_reports`は報告が一致した事実だけを表し、
担当の独立性も指摘の正しさも表さない。

同じ`review_content_sha256`を持つ結果は`possible_duplicate_reviews`へ必ず出し、複数の独立した根拠として数えない。
異なる`issue_key`で指摘内容が完全一致する組は`possible_duplicate_keys`へ出す。
`unresolved_issue_keys`には`single_report`と`conflict`を全て含める。

`human_decision_queue`には、`insufficient_evidence`、`conflict`、`possible_duplicate_review`、
`possible_duplicate_key`、`single_report`、`matching_reports`の順で全対象を一度ずつ入れる。
一致した指摘も人の最終採否から外さない。元資料やレビュー本文は再掲せず、対象IDと固定理由だけを示す。

担当別結果は`reviewer_id`順、各担当の指摘は`issue_key`、`finding_id`順、指摘群は`issue_key`順へ並べる。
結果集合と各reviewのSHA-256は、検査後の値を上記の順へ正規化した正準JSONから計算する。
JSON objectのkey順と結果集合内のreview配列順は整理結果へ影響させない。

全配列の順は次で固定する。

- 各findingの`criterion_ids`は基準ID順。入力時の順を意味として扱わない。
- `issue_groups`は`issue_key`順。各群の`reporters`は担当ID順、`findings`は担当ID、指摘ID順。
- `possible_duplicate_reviews`は`review_content_sha256`順、各`reviewer_ids`は担当ID順。
- `possible_duplicate_keys`は指摘署名SHA-256順、各`issue_keys`は問題key順。
- `insufficient_evidence_reviewers`は担当ID順、`unresolved_issue_keys`は問題key順。
- `human_decision_queue`は§8.4の区分順、同一区分内は昇順に並べた`identifiers`の配列を文字列として比較した昇順。
  各`identifiers`自体もID順とする。

指摘署名SHA-256は、次のkeyだけを持つ正準JSONから計算する。`criterion_ids`は基準ID順とする。

```json
{
  "criterion_ids": ["<criterion_id>"],
  "description": "<description>",
  "end_line": 1,
  "severity": "<severity>",
  "start_line": 1,
  "title": "<title>"
}
```

`review_sha256`と`review_content_sha256`の計算前にも、reviewを担当ID順、findingsを問題key・指摘ID順、
各`criterion_ids`を基準ID順へ正規化する。この順序以外の入力差だけで内容識別値を変えない。

【判断】`matching_reports`は複数の結果が同じ指摘を返した事実であり、指摘が正しいという合格判定ではない。
`possible_duplicate_keys`も重複確定ではない。いずれも利用者の意味判断を置き換えない。

### 8.5 停止結果

入力不正、root逸脱、symlink、読取不能、size超過、UTF-8不正、schema不正、内容識別値不一致、機微情報候補、
絶対path残存では、成功成果を返さず非0終了コードにする。

標準出力へ返すのは`status: stopped`、固定理由、`external_send_approved: false`だけとし、入力本文、レビュー本文、
一致箇所、例外本文、絶対pathを含めない。失敗時も標準エラーへ入力値や例外本文を出さない。

固定理由は`invalid_arguments`、`invalid_path`、`unreadable_input`、`size_limit_exceeded`、`invalid_utf8`、
`invalid_schema`、`stale_material`、`sensitive_data_remaining`、`absolute_path_remaining`、`internal_failure`だけとする。
正常結果は終了コード0、引数・path・読取り・size・UTF-8・schema・改変の停止は2、機微情報または絶対pathの停止は3、
入力値を含まない内部失敗は4とする。

### 8.6 JSON表示と絶対pathの固定規則

成功・停止の全JSONは、UTF-8、BOMなし、`ensure_ascii: false`、key昇順、区切り`,`と`:`の前後空白なしで作り、
JSON一件の直後にLF一つだけを付ける。標準エラーは常に空とする。

schemaで固定したSHA-256欄以外の資料本文と、復号済みJSONの全文字列key・値へ、Pythonの`re.search`相当で
次の4 patternを適用する。一つでも一致すれば絶対pathとして停止する。

```text
POSIX:       (?<![A-Za-z0-9._~/-])/(?:[^/\s"'<>]+/)*[^/\s"'<>]+
DRIVE_OR_UNC:(?<![A-Za-z0-9])(?:[A-Za-z]:[\\/]|\\\\)[^\s"'<>]+
FORWARD_UNC: (?<![A-Za-z0-9:])//[^/\\\s"'<>]+[/\\][^\s"'<>]+
FILE_URI:    (?i)\bfile://[^\s"'<>]+
```

位置指定用の実行引数にはこの4 patternを適用しない。`work=/Users/example/project`、`path:/Users/example/project`、
`path=C:\Users\example`、`\\server\share\item`、`//server/share/item`、`file:///tmp/item`は停止例とする。
`https://example.test/item`、`relative/path`、単独の`/`は、この規則だけを理由に停止しない。
規則版は本契約版3に固定し、実装者がpattern、検索方法、停止例、非停止例を追加または削除してはならない。

## 9. 受入条件

1. `prepare`が一つの資料だけを読み、目的、確認基準、制約、本文、各内容識別値を持つ材料一件を返す。
2. 同じ入力内容から同じ`prepare`結果を得る。時刻、環境値、現在位置、JSON objectのkey順で結果が変わらない。
3. 資料本文の一byteまたは条件・結果の意味を持つ一項目を変えると、旧内容識別値を再利用せず停止するか、
   新しい内容識別値を返す。
4. root外の通常path、symlink、通常file以外、複数資料、size超過を読取り前または成功前に拒否する。
5. 既定の秘密pattern、高い乱雑性を持つ長いtoken、§8.6の各絶対pathを、資料本文と復号済みJSONの
   自由記述、表示名、ID、keyへ一つずつ入れると、値や一致箇所を出さず停止する。形式・参照一致を確認済みの
   SHA-256欄だけは除く。位置指定引数は内容検査せず、出力にも含めない。
6. `organize`は結果1件から8件までを受け、担当別の結論、要約、指摘件数、元結果の内容識別値を失わない。
7. 空の結果集合、別材料へ結ばれた結果、未知key、未知基準、範囲外行、矛盾した`verdict`と指摘件数を拒否する。
8. 同じ`issue_key`の同一報告を`matching_reports`、相違を`conflict`、一件だけを`single_report`へ決定的に分ける。
9. 異なるkeyの完全一致だけを`possible_duplicate_keys`とし、意味が似るだけの指摘を自動統合しない。
10. 担当IDだけが異なる同一reviewを`possible_duplicate_reviews`へ出し、独立した一致根拠として数えない。
11. `single_report`、`conflict`、`insufficient_evidence`、重複可能性、`matching_reports`を人の判断一覧から外さず、
    採否を自動確定しない。
12. `organize`の正常出力に資料本文、入力path、root、秘密候補、入力にない判断が含まれない。
13. §8.4で順を固定した集合扱いの配列を逆順にした入力から、同じ内容識別値と同じ整理結果を得る。
    指定順を意味として保つ`constraints`は除く。指摘署名は§8.4の正準JSONを独立再計算した値と一致する。
14. 成功・停止のJSON bytes、追加key禁止、配列順、末尾LF、空の標準エラーが§8と一致する。
15. 成功・失敗の全経路で、file書込み、network、外部process、Git、環境値解決、権限変更、外部送信が0回である。
16. 正式入口を導入後の場所から実行でき、現在位置に依存しない。
17. 新入口の対象試験、影響する既存G02試験、安全出力に関係する試験、正規全試験が単独commandで成功する。
18. 実装後の独立完了レビューが契約適合と上位目的への影響を確認し、利用者が製品処理として受け入れる。

## 10. 来歴義務

- 本契約候補、独立定義挑戦、利用者の契約採用と実装開始、失敗確認、実装、試験結果、利用者向け合成例、
  独立完了レビュー、製品受入をcommitとSHA-256で結ぶ。
- 試験記録にはPython版、pytest版、正式入口版、終了コード、対象・関連・全試験、代替実行の有無を含める。
- 定義挑戦と通常試験は合成fixtureだけを使い、実利用者資料、秘密候補、絶対pathをrepositoryへ保存しない。
- 一時fixtureと一時実行出力はrepository外へ置き、必要な内容識別値と件数だけを証拠へ残す。
- 契約、入力schema、機微情報検査規則、正式入口のいずれかが変われば、影響する試験結果をstaleとする。

## 11. 利用者へ戻す条件

次の場合は実装または実行を止め、契約を暗黙に広げず利用者へ戻す。

- 二件以上の資料、資料探索、外部送信、外部処理、結果取得、永続保存が必要になった。
- 入力資料を自動伏字化しなければ目的を満たせない。初期処理は資料内容を黙って変えない。
- 共通`issue_key`なしに、文章の意味だけで重複または競合を確定する必要が生じた。
- 指摘の採否、修正、完了、受入を自動決定する必要が生じた。
- 既存G02、G04、G20、G30全体の正式化または変更が必要になった。
- 暫定上流候補の採否が責務、出力、受入条件を変える。
- 成功出力または失敗出力へ秘密候補、入力本文、絶対path、例外本文が漏れる。
- 実装範囲、危険度、許可能力、出力schema、受入条件の意味を変える必要がある。

入力fileの訂正、schemaに沿う結果の作り直し、同じ材料に結んだ結果の追加は、同じ契約内で再試行できる。
秘密候補をallowlistで迂回して成功へ変えることは、初期範囲では認めない。

## 12. 版付き依存

| 依存 | 固定値 | 変更時の扱い |
| --- | --- | --- |
| 現行開発方針 | SHA-256 `e3e6b0d2...73d0b559` | 実装開始前に差分を確認 |
| G02目録 | SHA-256 `c55367fc...e72a` | 14 pathの境界変更なら再挑戦 |
| G02既存コード | 観測commit `66d608e...c6`から現在まで14 path差分0 | 再利用判断を再確認 |
| 材料schema | 版1 | 変更後は旧材料と結果をstaleにする |
| 結果schema | 版1 | 変更後は旧結果をstaleにする |
| G25の既定patternと高乱雑性検査 | `tools/session_logs/redaction.py`、SHA-256 `aa49774a447d84422ec885a908bb52c7a3732eb67ddb53dcc1c03fbc149245bd`の公開`default_pattern_rules`と`find_high_entropy` | 対象file変更後は契約と安全出力試験をstaleにする |
| 絶対path検査 | 本契約v3 §8.6の4 pattern | 変更後は契約版を上げ、安全出力試験を再実行 |
| Python | 3.13系 | 実装受領記録で実版を固定 |
| pytest | 8.4系 | 実装受領記録で実版を固定 |

## 13. 実装方法の三案比較

| 観点 | 案A：既存入口のdry-runと人手整理 | 案B：既存G02一括処理を改造 | 案C：一件用の読取り専用入口 |
| --- | --- | --- | --- |
| 内容 | 現行`reviewcompass3-bootstrap-review --dry-run`と人の転記だけを使う | 材料束、raw保存、応答解析、二担当triageを直接変更する | 一件の材料作成と手元結果整理だけを新しい小さい核と入口へ分ける |
| 単純さ | 新実装0 | 既存14 pathの責務分離が必要 | 新しい核と入口だけで閉じる |
| 処理時間 | 機械処理をしないため比較不能 | 外部実行・保存前提の処理が残る | 一件の読取りとJSON計算だけ |
| メモリ | 最小だが製品結果を作らない | 材料・raw結果・解析結果を重ねて持つ | size上限内の資料と結果だけ |
| 頑健さ | 転記誤り、改変、結果混在を検出できない | 外部runner、私有保存、二経路の前提が今回と衝突する | 一件、通信なし、書込みなしを入口で固定できる |
| 変更範囲 | 0 | 既存の暫定6 path以上と試験群 | 新しい製品核1、入口1、対象試験1、実行名1 |
| 保守負担 | 人の手順として残る | 暫定一括処理全体を正式保守する | 小さいschema二つと入口を保守する |
| 戻しやすさ | 変更なし | 既存暫定処理への影響分離が難しい | 新規入口と実行名を外せば戻る |
| 目的への適合 | 材料作成も結果整理も未達 | 広すぎ、外部実行なし一件へ狭めにくい | 現在の目的と禁止事項に一致 |

【提案】案Cを採用候補とする。案Aは既存機能だけで済む最小案だが、現在のdry-runは配置確認だけで、材料も整理結果も
作らない。案Bは既存部品を再利用できる一方、外部実行、raw保存、二担当経路という未承認責務を同時に変更する。
案Cは新規実装を要するが、外部送信も保存も増やさず、一件処理を説明できる最小の意味単位である。

【判断】既存G02と似る決定的処理は、正準JSON、SHA-256、厳格schema、`issue_key`による群分けである。しかし既存関数は
暫定型、raw保存record、二経路条件へ結合している。初期実装は別の狭い製品入口とし、既存G02が正式化され、直接入力と
一件結果を同じ責務で扱える版になった時だけ統合を再検討する。これは`split_with_rationale`、すなわち理由を固定した分離である。

【判断】機微情報候補の既定patternと高い乱雑性の検出は、正式受入済みG25の公開関数を責務変更なしで再利用する。
環境値解決、伏字化、報告file書込みは呼ばない。絶対path検査はG25と安全保存に非公開関数しかないため、既存fileを
変更して共通化せず、一件用の核へ閉じる。共通の公開方針が後で採用された場合だけ統合を再検討する。

実装開始を承認した場合の変更上限は次とする。

- 新規：`tools/reviews/one_item_review.py`
- 新規：`tools/reviews/one_item_review_entry.py`
- 変更：`pyproject.toml`の`[project.scripts]`へ正式実行名一件を追加
- 新規：`tests/test_one_item_review.py`
- 実装選択と試験結果を残す短い証拠record

既存G02の14 path、既存試験、安全保存、G20、G30は変更しない。変更が必要と判明した時点で停止する。

## 14. 実装順序の候補

1. 本候補を固定し、作業担当と異なる実行単位で独立定義挑戦を行う。
2. 指摘があれば原因をまとめ、契約候補だけを訂正して変更点確認へ渡す。
3. 利用者が契約採用、案C、実装開始を判断する。
4. 承認後、root逸脱、symlink、資料複数、改変、schema不正、秘密候補、絶対path、結果混在、競合整理の失敗試験を先に作る。
5. 変更がなければ失敗することを確認し、試験の境界を固定する。
6. §13の変更上限内で実装し、対象試験を成功させる。
7. 対象試験、関連試験、正規全試験、利用者向け合成例を単独commandで実行する。
8. 機微情報と結果混在の境界へ反例を試し、独立完了レビューを行う。
9. 利用者が製品処理の受入を判断する。

## 15. 成果物の役割と終了時の扱い

| 成果物 | 完成時の役割 | 役割終了時 |
| --- | --- | --- |
| 承認済みの本契約 | 現在の動作保証と履歴・監査の両方 | 後継版から参照して履歴保存 |
| 一件用の製品核と入口 | 現在の動作保証 | 後継入口へ移行後に削除または使用停止 |
| 対象試験 | 現在の動作保証 | 入口とschemaの役割終了時に判断 |
| 定義挑戦、承認、実装証拠、完了レビュー | 履歴・監査資料 | Git履歴で保存 |
| 合成fixture、一時入力root、一時出力 | 実施中の確認材料 | repository外で破棄し、識別値と件数だけ残す |

## 16. 利用者が判断する点

独立定義挑戦後、利用者が次を判断する。

1. 固定資料一件と結果集合一件を読む責務を採用するか。
2. 結果は一件から受け付け、共通`issue_key`だけで一致・競合を整理する限界を採用するか。
3. 材料も整理結果も自動保存せず、外部送信なし・書込みなしとする初期境界を採用するか。
4. 機微情報候補を自動伏字化せず、値を出さず停止する境界を採用するか。
5. 案Cと§13の実装開始範囲を承認するか。

【判断】本候補の作成開始は、上記の契約採用、実装開始、既存G02の正式化、外部送信を承認したことにはしない。

## 17. 未実施

【未実施】独立定義挑戦、契約採用、実装開始、コード・試験・設定・`pyproject.toml`の変更、入力root作成、
実利用者資料の読取り、レビュー実行、結果file作成、保存、削除、外部送信、network、外部process、既存G02・G04・G20・
G30の変更または正式化、正規全試験、push、tag、amend、rebase、reset、履歴書換えは行っていない。
