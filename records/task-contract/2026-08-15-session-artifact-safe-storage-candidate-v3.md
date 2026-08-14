# Session記録と伏字化結果の安全保存・再読込み Task Contract候補 v3

- 契約ID：`TC-RC3-PRODUCT-SESSION-ARTIFACT-SAFE-STORAGE-002`
- 契約版：3
- 契約種別：製品処理
- 状態：`candidate_corrected_pending_one_point_review_and_human_approval`
- 作成日：2026-08-15
- prior contract：`TC-RC3-PRODUCT-G25-SESSION-ARTIFACT-PREPARATION-001`
- supersedes：`records/task-contract/2026-08-15-session-artifact-safe-storage-candidate-v2.md`、SHA-256 `c42c36a1ec389409892cf990116055bee301a29008c44f4e9fed9d03d4811163`
- 訂正根拠：`records/development/2026-08-15-session-artifact-safe-storage-task-contract-definition-correction-review-v1.md`、SHA-256 `6408d28e92fed3ebb62a2d8ea716d2b4af5d273a362b6d6437c15bd290f8cbb7`
- 利用者判断：2026-08-15の選択「1」。契約候補v3の一点訂正だけを承認し、契約採用と実装開始は承認していない
- 実装状態：未開始
- 危険度：高
- 内容識別値：本候補を固定した後、独立した定義挑戦と利用者判断記録から参照する

## 1. 権威、証拠、暫定候補を分ける

### 1.1 現在の権威

| 役割 | path | SHA-256 |
| --- | --- | --- |
| 立て直し計画v5と第5段の完了 | `records/development/2026-08-14-recovery-plan-v5-stage5-completion-decision-v1.md` | `4c50bdf643c12e3c4fb02c78d3fe47de20885efab4b8b9b34dbd946c763da3b0` |
| 現行開発方針 | `docs/development/2026-08-02-development-policy.md` | `422d234a0503670e61936edfe98cd13451f4e7af6bfc1506a07824f2904f0fac` |
| 最初の承認済み契約 | `records/task-contract/2026-08-14-g25-session-artifact-preparation-candidate-v1.md` | `20e4e0551c5b1357ba3e66d6ba849f19566da27c58c54ef98e8fa1db110fb72b` |

【判断】本候補は、第5段完了判断が次作業候補として明示した「利用者が許可したSession記録一件と、正式入口が
作る伏字化結果を、安全な別領域へ保存して再読込みできる範囲」から責務を導く。下記の製品計画、要求、既存G26を、
未承認のまま正式な正本または実装依存へ昇格しない。

### 1.2 固定証拠

| 役割 | path | SHA-256 |
| --- | --- | --- |
| G25、G26、G30を分けたコード在庫 | `records/development/2026-08-14-stage4-product-code-and-task-contract-input-inventory-evidence-v1.md` | `c55367fc6b8f72f7041612cedc11d609b359909156f619fcb72e6d72bd33e72a` |
| 正式な読取り専用入口 | `tools/session_logs/read_only_entry.py` | `dd95f087833d4ff30fbb761193a3a2e7da5a2536954a766624aa9d7e77530d72` |
| 製品入口の登録正本 | `pyproject.toml` | `ec771cd06e063d2f4b252ecfc9962d7f221effbf072169edbabfb7c8f71d3229` |

【実測】G26は設定、探索、保存、保全、復旧を9 pathで扱うが、`repository_root`を省略すると保存境界検査を
行わない反例が固定され、全体は`provisional / non-normative / promotion_required: true`のまま保留である。

### 1.3 暫定の上流候補

| 役割 | path | SHA-256 | 本契約での扱い |
| --- | --- | --- | --- |
| 統合製品計画候補 | `docs/current/reviewcompass3-plan-current.md` | `1a73597605eafb65a2259ccf19431e3aba041564d03fdb279150042a9bd0962f` | rawと派生物を別領域に置く候補入力だけを確認する |
| 残機能要求候補 | `docs/requirements/remaining-feature-requirements.md` | `ec31ce53ce097a8ff8a59a4649d97e4af8d8dd0cbdb8a1a8c7d4e8d2a1f8bcf6` | 対応候補IDの所在だけを確認する |

【記録】対応候補は`REQ-SESSION-001`、`REQ-SESSION-002`、`REQ-PORTABLE-002`、`REQ-PORTABLE-004`である。
本契約を承認しても、これらの要求候補全体または上流文書を正式採用したことにはしない。

## 2. Identity（識別）

| 項目 | 値 |
| --- | --- |
| `task_contract_id` | `TC-RC3-PRODUCT-SESSION-ARTIFACT-SAFE-STORAGE-002` |
| `contract_type` | `product_delivery` |
| `version` | 3 |
| 正式な責務の出所 | `DEC-RECOVERY-PLAN-V5-STAGE5-COMPLETION-2026-08-14-V1` |
| `source_requirement_ids` | なし。正式採用済みRequirementが存在しないため空とする |
| 対応候補 | `REQ-SESSION-001`、`002`、`REQ-PORTABLE-002`、`004` |
| `prior_contract_id` | `TC-RC3-PRODUCT-G25-SESSION-ARTIFACT-PREPARATION-001` |
| `supersedes` | 候補v2、SHA-256 `c42c36a1...1163` |
| 訂正根拠 | v2変更点限定レビュー、SHA-256 `6408d28e...cbb7` |
| 内容識別 | 本候補fileのSHA-256を変更点レビューと承認Decisionから参照する |
| 記録形式 | Markdown候補。G30の未完成schema、生成器、状態機械を使わない |

## 3. Responsibility（責務）

利用者が明示的に指定した一件のSession記録について、次を一つの永続記録単位として行う。

1. 元記録を機微情報用領域へ保存する。
2. 正式入口が同じ記録から作る正常結果から、下記の保存許可項目だけを抜き出した保存用派生物を、別の通常データ領域へ保存する。
3. 二領域の固定fileを記録IDで結び、`incomplete`、`committed`、`deleting`、`deleted`の状態を当該記録内だけで判定できるようにする。
4. 二領域の書込みと再読込み照合が完了した後にだけ、確定済みの伏字化結果として見える状態にする。
5. 確定済みの保存用派生物を、記録IDから再読込みし、保存時の内容識別値と一致する場合だけ返す。元記録本文は返さない。
6. 保持期限を過ぎた記録は通常の再読込みを拒否し、削除待ちと表示する。
7. 未確定または確定済みの一記録を削除するときは、削除前に利用者へ固定fileの種類と件数を示し、確認値を得る。削除途中では確認値を失わず、完了まで同じ記録IDで再試行できるようにする。

### 3.1 保存用派生物

正式入口の正常結果全体をそのまま保存しない。保存・再出力を許す項目は次に限定する。

- `external_send_approved: false`、`parse_issues: []`、`source_kind`、`status: ok`。
- `transcript`、`summary`、`redaction_findings`、`summary_redaction_findings`。
- `provenance`のうち、`start_line`、`end_line`、`source_sha256`、`transcript_sha256`、`summary_sha256`、`redaction_rules_sha256`、`summary_changed_files`、`summary_commits`、`tool_version`。

正式入口の`provenance.source_path`は保存用派生物、manifest、削除後監査情報、`load-derived`の出力へ含めない。
元記録との対応は`record_id`、内容識別値、行範囲で保ち、Session入力pathを通常データ領域へ移さない。

【判断】本契約は、保存した結果を検索・索引化したり、複数記録を自動探索したり、外部送信したりしない。
一件の保存、再読込み、明示削除という小さい一連の処理だけを扱う。

## 4. Boundary（境界）

### 4.1 範囲内

- 一つの`raw_root`内にある、利用者が許可した一つの`raw_log`。
- 正式入口が返す`status: ok`の構造化結果一件と、§3.1の保存用派生物。
- 必須の`repository_root`、機微情報用の`sensitive_root`、通常データ用の`data_root`。
- 一つの`record_id`、保持期限、保存時刻、内容識別値、固定file、記録単位の状態。
- `store`、`load-derived`、`plan-delete`、`delete`の四操作。
- 同じ入力での保存再試行と、同じ記録ID・削除確認値での中止・削除再試行。

### 4.2 範囲外

- Session記録の探索、複数file一括処理、継続回収、追記・改変判定、移行、backup一覧、scheduler、hook。
- 保存済み元記録の本文、`provenance.source_path`、保存rootを標準出力へ返す操作。
- 内容検索、索引、全文検索、意味検索、共有、同期、外部送信、network、外部process、Git操作。
- 環境変数、home、利用者名、host名から保存先を推測すること。
- G26、G27、G28、G30全体の正式採用または暗黙の依存。
- 保持期限を自動監視する常駐処理と元記録・派生物の自動削除。
- repository内への元記録、派生物、端末固有絶対pathの保存。
- 全対応OSで同じ権限制御を保証すること。初期候補は現在のmacOSに限定し、他OSは後続契約へ分ける。

【判断】保持期限は保存時に必須とし、期限後の通常読込みを拒否する。元記録と派生物の自動削除は導入しない。
削除は利用者が`plan-delete`の結果を確認した後の明示操作に限定し、期限切れを理由に勝手に消さない。

## 5. Preconditions（前提）

- 本契約候補と実装開始が、変更点レビュー後に利用者へ別々に承認されている。
- `repository_root`、`raw_root`、`raw_log`、`sensitive_root`、`data_root`はすべて絶対pathである。
- `repository_root`はGit repositoryとして実在し、省略できない。
- `sensitive_root`と`data_root`は事前に作成され、repository外にあり、互いに同一でも包含関係でもない。
- 初期対応OSはmacOSである。各保存rootと記録directoryは実効利用者が所有しmode 0700相当、通常fileは同じ利用者が所有しmode 0600相当でなければならない。group・otherまたは追加ACLに所有者以外への権限があれば停止する。
- 各rootから固定fileまでの全構成要素をdirectory file descriptorから相対的に開き、symlinkを追わない。`resolve()`後の文字列比較だけで安全とみなさず、`O_NOFOLLOW`相当とopen後の所有者・種類・mode再確認を使えない場合は書込み前に停止する。
- `raw_log`は解決後の`raw_root`内にある通常fileで、正式入口の処理を利用者が許可している。
- 正式入口から値で受ける結果は`status: ok`、終了コード0、`external_send_approved: false`で、絶対pathと未伏字値を含まない。
- 保存用派生物は§3.1の項目集合と完全一致し、`provenance.source_path`を含まない。
- 結果の`source_sha256`が、保存直前に読んだ`raw_log`のSHA-256と一致する。
- 保持期限は現在より後で、時刻帯を含む固定形式で指定される。

## 6. Context Obligations（必要材料）

| 材料 | 必須性 | 充足条件 |
| --- | --- | --- |
| 第5段完了判断 | 必須 | §1.1のSHA-256一致 |
| 最初の承認済み契約 | 必須 | §1.1のSHA-256一致 |
| 正式な読取り専用入口 | 必須 | §1.2のSHA-256一致、正式・安定表示 |
| 保存対象の元記録 | 実行時必須 | 利用者許可、root内、通常file、内容識別値一致 |
| 保存用派生物 | 実行時必須 | 正式入口の正常結果から§3.1だけを選択し、内容識別値一致、`source_path`不在、安全出力検査合格 |
| 三つのroot | 実行時必須 | 明示入力、解決後の境界と分離、権限検査合格 |
| G26 | 参考 | 保留表示と既知反例を維持。個別関数を使うなら別途再評価 |
| 上流候補 | 参考 | 暫定表示を維持し、正式正本にしない |
| 実Session記録 | 定義時不要 | 定義挑戦と通常試験では合成fixtureだけを使う |

## 7. Allowed Capabilities（許可能力）

- 指定された元記録一件と、正式入口の正常結果一件の読取り。
- 正常結果から§3.1の保存用派生物だけを決定的に選ぶ処理。
- 三つの明示rootと、その境界・所有者・mode・symlink非追跡の検査。
- SHA-256、記録ID、保持期限、操作識別値、確定印、削除確認値の計算。
- `sensitive_root/<record_id>/`の固定file `operation.json`、`raw.bin`と、一時file `operation.json.tmp`、`raw.bin.tmp`への書込み・再読込み。
- `data_root/<record_id>/`の固定file `operation.json`、`derived.json`、`manifest.json`、`commit.json`、`deleted.json`と、一時file `operation.json.tmp`、`derived.json.tmp`、`manifest.json.tmp`、`commit.json.tmp`、`deleted.json.tmp`への書込み・再読込み。
- 一時file名は対応する最終file名から決定的に導出し、乱数名、時刻名、任意suffixを使わない。同一root内の名前変更と必要な同期だけを行う。
- 同じ入力または同じ記録ID・確認値による、当該記録の保存再試行、中止、削除再試行。
- 確定済み保存用派生物の読取りと標準出力。
- 明示確認された当該記録だけの削除。

禁止する能力は、rootの推測、広い探索、globまたは再帰的な対象決定、root自体の削除、元記録本文または
`provenance.source_path`の標準出力、外部送信、network、外部process、Git、環境値解決、権限拡張、常駐処理である。

## 8. Expected Outputs（期待成果）

### 8.1 正式入口との値受渡し

実装時は`tools.session_logs.read_only_entry`へ、標準出力を行わずに`(終了コード, JSON化可能な結果)`を返す
小さい公開関数`prepare_safe_result(raw_root, raw_log)`を追加する。現在の`run()`は引数解決後にこの関数を呼び、
返された結果を従来どおり一回だけJSON表示して同じ終了コードを返す。保存入口は同じ関数を直接呼び、終了コード0かつ
`status: ok`だけを受け付ける。標準出力の捕捉・再解析、人の転記、外部process、G25からの別組立ては使わない。

この変更では現在の正式実行名、正常・停止時の出力bytes、終了区分、安全検査、正式・安定表示を変えない。

### 8.2 保存用の固定fileと状態判定

一記録の許可fileは、§7に列挙した最終fileと、その最終名へ`.tmp`を一つだけ付けた一時fileだけとする。
両rootの`operation.json`は同じ操作識別値、記録ID、全ての最終fileと一時fileの名前、対応する最終名、期待する
内容識別値、保持期限、状態を持ち、本文とpathを持たない。ただし`operation.json.tmp`は自分自身のSHA-256を
`operation.json`へ書かず、同じ記録ID・操作識別値・schema版・変更前後の状態を持つ完全な正準JSONの場合だけ
有効な一時fileとみなす。状態は次の優先順位で判定する。

1. `deleting`：どちらかの有効な`operation.json`または`operation.json.tmp`が`deleting`である。通常読込みを必ず拒否する。
2. `deleted`：本文file、本文の一時file、`commit.json`、`commit.json.tmp`がなく、有効な`deleted.json`がある。
3. `committed`：`commit.json`が最後に作成され、両rootの操作識別値と全内容識別値が一致し、一時fileが一つもなく、`deleting`でない。
4. `incomplete`：当該記録の最終fileまたは一時fileが一つ以上あるが、上記三状態を満たさない。

異なる状態が二rootに見える場合は、成功側へ推測せず`deleting`、次に`incomplete`を優先する。一時fileは最終fileと
同じ保持期限を持つ。root全体を走査せず、明示された`record_id`と§7の決定的一覧だけを読む。有効な
`operation.json`がなく一時fileだけが存在する場合は、その内容を推測して再開または削除せず停止する。

### 8.3 保存成功

保存は、両rootへ同じ有効な`incomplete`の`operation.json`を置いて再読込みした後にだけ、`raw.bin.tmp`、
`derived.json.tmp`、`manifest.json.tmp`を書き始める。各一時fileを期待する内容識別値と照合して最終名へ移し、
全fileを再読込み照合した後、`commit.json.tmp`を照合して最後に`commit.json`へ移す。二rootを同時確定できるとは主張しない。
`commit.json`が有効になる前は成功も通常読込みも許さない。

終了コード0では、秘密値とpathを含まない次の最小情報だけを返す。

- `status: stored`、`record_id`、`raw_sha256`、`derived_sha256`、`manifest_sha256`。
- `retention_until`、`committed: true`、`external_send_approved: false`。

`record_id`は入力pathではなく、raw、保存用派生物、規則、tool版、保持期限の内容識別値から決定的に導出する。
同じ入力で同じIDを得る。異なるbytesを同じIDへ上書きしない。

### 8.4 再読込み成功

`load-derived`は状態が`committed`で、両rootの操作情報、確定印、manifest、元記録、保存用派生物の内容識別値が
全て一致し、保持期限内の場合だけ、§3.1の保存用派生物と最小状態を返す。元記録本文、`source_path`、保存root、
絶対pathは返さない。

### 8.5 途中失敗、保存再試行、中止

途中失敗では成功を返さず、`status: incomplete`、`record_id`、操作識別値のSHA-256、秘密を含まない固定理由を返す。
同じ入力による`store`再試行は、有効な`operation.json`が存在し、存在する最終fileと一時fileが記録済みの名前、
操作識別値、対応する最終名、期待する内容識別値に一致する場合だけ再開する。不一致、一覧外file、または
有効な操作情報がない一時fileがあれば何も変更せず停止する。

保存を取りやめる場合は、`plan-delete`が`incomplete`状態にも対応する。一方または両方に存在する有効な
`operation.json`と、記録済みの最終fileおよび一時fileを記録IDから直接確認し、それらへ結び付く削除確認値を作る。確定印や片方の
`operation.json`がなくても、残る操作情報の記録ID・操作識別値・期待する内容識別値が一致すれば、当該途中記録だけを
`delete`で処理できる。有効な操作情報が一つもなければ推測で削除しない。一時fileも最終fileと同じ保持期限の対象で、期限後も
自動削除せず通常利用を拒否する。

### 8.6 期限切れ

保持期限を過ぎた記録は`status: expired_pending_deletion`として保存用派生物を返さない。自動削除は行わない。

### 8.7 削除と削除再試行

`plan-delete`は`incomplete`、`committed`または`deleted`について、記録ID、現在状態、存在する操作識別値、
manifest識別値があればその値、削除対象の最終fileと一時fileの種類・対応・件数、削除後監査の扱いを返す。pathは返さない。
削除確認値は、この計画全体の正準JSONへ結び付ける。`deleted`では、保持期限以後の`deleted.json`と残った
`operation.json`または`operation.json.tmp`だけを対象にでき、本文fileを新たに対象へ加えない。

`delete`は確認値を再照合してから、両rootの`operation.json`へ同じ`deleting`状態と確認値を先に書く。片方への
書込みが失敗した場合は本文fileを削除せず、書けた`deleting`状態を次回の再試行根拠として残す。`deleting`が一つでも
あれば通常読込みを拒否する。

両方が`deleting`になった後に、記録済みの一時file、raw、保存用派生物、manifest、`commit.json`を削除する。削除確認値と操作情報は
本文fileの削除が完了するまで残す。全対象の不存在を再確認後、data側へ`deleted.json`を書いて再読込みし、最後に
両rootの`operation.json`を除く。途中失敗は成功とせず`deletion_incomplete`を返し、残った`deleting`情報と同じ
確認値で再試行できる。

`deleted.json`は記録ID、削除時刻、削除済み内容のSHA-256、元の保持期限、`deleted: true`だけを持ち、本文、path、
秘密値、削除確認値を持たない。削除が保持期限前なら元の保持期限まで保持する。保持期限以後の明示`delete`は、
対象本文が存在しないことを確認したうえで当該`deleted.json`だけを除ける。保持期限後も常駐処理による自動削除はしない。

## 9. Acceptance Criteria（受入条件）

1. 明示した一件の元記録と§3.1の保存用派生物を、分離した二rootへ保存できる。
2. `repository_root`、`sensitive_root`、`data_root`のいずれかを省略した場合は、保存前に停止する。
3. 各保存rootがrepository内、互いに同一または包含関係、所有者不一致、mode不適合、追加権限ありの場合は書込み前に停止する。
4. rootから固定fileまでの構成要素がsymlinkである場合、またはsymlink非追跡のopen後検査ができない場合は書込み前に停止する。
5. 正式入口の停止・部分結果、`external_send_approved: true`、絶対path残存、raw識別値不一致を保存しない。
6. 保存用派生物、manifest、再読込み出力に`provenance.source_path`を含めない。
7. 保存名と出力へSession入力path、home、利用者名、host名、秘密値を含めない。
8. 現在の正式入口は値受渡し境界の追加前後で出力bytes、終了区分、安全検査が同一である。
9. 同じ入力の再保存は同じ記録IDで`unchanged`となり、異なる内容を上書きしない。
10. 保存用派生物または元記録を一文字変えた場合、再読込みは成功せず、本文を返さない。
11. 元記録書込み後、派生物書込み後、確定印作成前の各失敗で成功を返さず、同じ入力から復旧できる。
12. 確定印のない途中状態と一時fileを通常読込みへ出さず、同じ記録IDの`plan-delete`と確認済み`delete`で中止できる。
13. 二rootの状態が不一致なら成功側へ推測せず、`deleting`または`incomplete`として停止する。
14. 保持期限後は通常読込みを拒否し、元記録と派生物を自動削除しない。
15. 削除確認値が欠落・古い・別記録用の場合は何も削除しない。
16. 削除途中で片方の操作情報書込み、raw削除、派生物削除、確定印削除の各段階が失敗しても、同じ確認値で再試行できる。
17. 削除対象は`operation.json`に記録された当該記録の最終fileと一時fileだけで、root、他記録、一覧外fileを削除しない。
18. `raw.bin.tmp`書込み中の停止後でも、同じ入力から再開するか、確認済み削除で一時fileを片付けられる。有効な操作情報がない一時fileは推測削除しない。
19. 成功、失敗、再読込み、削除の標準出力に元記録本文、Session入力path、絶対path、例外本文、秘密値を含めない。
20. 保存・再読込み・削除でnetwork、外部process、Git、環境値解決を行わない。
21. 対象試験、正式入口とG25の関連試験、影響するG26試験、正規全試験が単独commandで成功する。
22. 利用者が合成例の保存、再読込み、途中状態の中止、削除計画、削除再試行を確認し、製品処理として受け入れる。

【判断】保存、削除、機微情報、復旧を扱うため危険度は高い。実装時の高危険度確認は、root境界、権限、内容改変、
途中失敗、誤削除、秘密値出力へ限定する。全製品機能や全試験へ一律の変異検査を課さない。

## 10. Provenance Obligations（来歴義務）

- 本契約、定義挑戦、利用者承認、失敗確認、実装、受領記録、利用者受入、実装後レビューをcommitとSHA-256で結ぶ。
- 保存manifestはprior contract ID・版、正式入口版、raw・保存用派生物・規則のSHA-256、保持期限、書込み版を持ち、`source_path`を持たない。
- repository内の証拠へ実Session本文、未伏字転写、保存rootの絶対path、削除確認値を残さない。
- 代表入力は合成fixtureとし、実Session記録を定義挑戦や通常試験へ使わない。
- 契約、正式入口、安全出力規則、保存形式、root検査、削除順のいずれかが変われば、影響する受領記録をstaleとする。
- 削除後の監査記録は本文、path、削除確認値を持たず、削除済み内容を復元できる材料にしない。元の保持期限までを保持期間とする。

## 11. Escalation Policy（利用者へ戻す条件）

次の場合は定義、実装または実行を停止し、契約を暗黙に広げず利用者へ戻す。

- 元記録本文を出力または通常データ領域へ置く必要が生じた。
- rootを省略、推測、環境値から取得しなければ動かせない。
- 二root間の完全な同時書込みを保証済みと表示する必要が生じた。
- 常駐処理、自動削除、自動探索、複数記録、移行、外部送信が必要になった。
- G26、G27、G28、G30または暫定上流候補の正式採用が必要になった。
- 現在の正式入口の出力bytes、終了区分または保証範囲を変更する必要が生じた。
- 初期対象OSで安全な所有・権限検査を実装できない。
- 途中状態の復旧、誤削除防止、改変検出を、追加の大域台帳なしに満たせない。
- 実装案、変更範囲、許可能力、保持・削除の意味を変える必要が生じた。

## 12. 版付きdependency

| dependency | 固定値 | 変更時の扱い |
| --- | --- | --- |
| prior contract | `TC-RC3-PRODUCT-G25-SESSION-ARTIFACT-PREPARATION-001`、SHA `20e4e055...fb72b` | 本候補をstaleにして再挑戦 |
| superseded candidate | 候補v2、SHA `c42c36a1...1163` | 履歴として保持し、現在の採用根拠にしない |
| correction review | v2変更点限定レビュー、SHA `6408d28e...cbb7` | 一時file一点の確認まで有効 |
| 正式入口 | `tools/session_logs/read_only_entry.py`、SHA `dd95f087...30d72` | 出力bytesと安全境界を再確認 |
| 製品入口登録 | `pyproject.toml`、SHA `ec771cd0...3229` | 導入後入口を再確認 |
| G26在庫 | 9 path、tree SHA `a2768896...1197`、保留 | 個別再利用前に必要部分だけ再評価 |
| 現行開発方針 | SHA `422d234a...0fac` | 実装前に現行版を再固定 |
| 初期対応OS候補 | macOS、観測kernel `Darwin 25.5.0` | 変更点レビュー後に利用者が採否を判断。他OSへ自動拡張しない |
| Python・pytest | Python 3.13.14、pytest 8.4.2 | 実装受領記録で再固定 |

## 13. 実装方法の三案比較

| 観点 | 案A：既存機能と手動保存 | 案B：G26全体を利用 | 案C：狭い専用保存境界 |
| --- | --- | --- | --- |
| 内容 | 正式入口の画面出力を利用者がfileへ保存し、元記録を手動複製する | G26の設定、探索、保全、保存、復旧CLIを使う | 正式入口へ`prepare_safe_result`を加え、一件だけを明示rootへ保存・再読込み・削除する専用入口を作る |
| 単純さ | 新実装0で最も単純 | 新実装は少ないが9 pathと広い操作を使う | 小さい値受渡し境界、保存核、入口が必要 |
| 処理時間 | 最小 | 探索と複数成果物処理が増える | 一件処理でAとの差は小さい |
| メモリ | 最小 | 探索対象に応じて増える | 一件のrawと保存用派生物に限定 |
| 頑健さ | root分離、原子的書込み、改変検出、復旧、削除確認を保証できない | 既存機能は多いが、root省略反例、広いCLI、暫定状態を持つ | 必須root、固定file、内容照合、途中状態、削除再試行、明示削除へ閉じられる |
| 変更範囲 | repository変更0 | G26の修正・正式化と広い再確認が必要になり得る | 正式入口の値受渡し、保存核、新入口、登録、対象試験に限定できる |
| 保守負担 | 手順と利用者判断へ分散し、再現しにくい | G26全体の保守へ結合する | 小さい製品入口一件として保守できる |
| 戻しやすさ | repository変更なし | G26の他用途と結合し戻しにくい | 新入口と専用保存部を使用停止し、正式読取り入口を維持できる |
| 現在目的への適合 | 保存・再読込みの安全保証を満たさない | 一件処理より広く、未承認範囲を含む | 一件、二領域、明示root、保存用派生物、再読込み、明示削除へ限定できる |

【提案】訂正後も案Cを採用候補とする。案Aは最小だが、利用者の手作業を完成経路にし、安全境界と復旧を保証できない。
案Bは既存機能を使えるが、G26全体の既知問題と広い責務を取り込む。案Cは新実装を要するが、必要な保証を満たす
最も単純な意味的完結単位である。

【判断】案Cの実装候補は、正式入口の`prepare_safe_result`、一件用の保存核、新しい保存入口、`pyproject.toml`の
実行名、対象試験である。既存G26の個別関数を再利用する場合も、G26全体を採用せず、対象関数だけを別途再評価する。

## 14. 実装順序の候補

1. 本v3を一時fileの接続だけの一回限り確認へ掛ける。
2. 利用者が契約の採否、案C、初期対応OS、実装開始を別々に判断する。
3. 実装開始が承認された場合だけ、値受渡し、root省略、権限、symlink、二root不一致、途中失敗、改変、誤削除の失敗確認を作る。
4. 現在の正式入口の出力bytesと終了区分を変えず、安全結果を値で保存入口へ接続する。
5. 合成入力で保存、再読込み、保存中止、期限切れ、削除計画、削除途中失敗、削除再試行を確認する。
6. 対象試験、影響する既存試験、正規全試験を実行する。
7. 高危険度境界だけを故障注入と独立判定で確認し、独立完了レビューを行う。

## 15. 成果物の役割と終了時の扱い

| 成果物 | 完成時の役割 | 役割終了時 |
| --- | --- | --- |
| 承認済みの本契約 | 現在の動作保証と履歴・監査の両方 | 後継版から参照して履歴保存 |
| 保存核と製品入口 | 現在の動作保証 | 保存済み記録の移行・削除境界を確認後に削除または使用停止 |
| 対象試験 | 現在の動作保証 | 入口と保存形式の役割終了時に判断 |
| 定義挑戦、承認、実装Evidence、完了レビュー | 履歴・監査資料 | Git履歴で保存 |
| 合成fixture、一時保存root、一時受領記録 | 実施中の確認材料 | repository外で破棄し、必要な識別値だけEvidenceへ残す |

## 16. 利用者が判断する点

本v3の一点確認後、利用者が次を別々に判断する。

1. v2の残る止める指摘一点が解消した本v3をTask Contractとして採用するか。
2. 元記録を機微情報用領域、保存用派生物を通常データ領域へ分ける責務を承認するか。
3. 固定fileによる途中状態、期限後の読込み拒否、確認値を失わない明示削除という境界を承認するか。
4. macOSの所有者限定権限、mode、symlink非追跡の範囲を承認するか。
5. 案Cと実装開始範囲を承認するか。
6. G26と上流候補を保留・暫定のまま、必要な個別関数だけを再評価可能とするか。

【判断】本v3の作成承認は、上記の契約採用、実装開始、G26の正式化を承認したことにはしない。

## 17. 未実施

【未実施】本v3の一点確認、契約採用、実装開始、コード・試験・設定・`pyproject.toml`の変更、
G26の修正・正式化、保存rootの作成、実Session記録の読取りまたは保存、削除、外部送信、network、外部process、
Task Contract実行基盤、push、tag、amend、rebase、reset、履歴書換えは行っていない。
