# G25 Session記録解析 最初のTask Contract候補 v1

- 契約ID：`TC-RC3-PRODUCT-G25-SESSION-ARTIFACT-PREPARATION-001`
- 契約版：1
- 契約種別：製品処理
- 状態：`candidate_pending_definition_challenge_and_human_approval`
- 作成日：2026-08-14
- prior contract：なし
- 実装状態：未開始
- 危険度：高
- 内容識別値：本候補を固定した後、独立した定義挑戦と利用者判断記録から外部参照する

## 1. 権威、証拠、候補を分ける

### 1.1 現在の権威

| 役割 | path | SHA-256 |
| --- | --- | --- |
| 第5段の進め方 | `docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md` | `8c814067511797e445d66779ad144f42ea0b139501ff6002a7d6c46e6706055c` |
| G25採用と第4段完了 | `records/development/2026-08-14-recovery-plan-v5-stage4-completion-decision-v1.md` | `147217192ea1d4d491005bd4cb7879f292f8739364e6b912a46d3dda8b8295b7` |
| 現行開発方針 | `docs/development/2026-08-02-development-policy.md` | `422d234a0503670e61936edfe98cd13451f4e7af6bfc1506a07824f2904f0fac` |

【判断】本候補の製品責務は、利用者が承認した第4段完了判断から導く。下記の要求・設計候補を、未承認のまま
正式要求または正式設計へ昇格しない。

### 1.2 固定証拠

| 役割 | path | SHA-256 |
| --- | --- | --- |
| 152件の分類、G25境界、最小入力 | `records/development/2026-08-14-stage4-product-code-and-task-contract-input-inventory-evidence-v1.md` | `c55367fc6b8f72f7041612cedc11d609b359909156f619fcb72e6d72bd33e72a` |
| 限定訂正後の独立確認 | `records/development/2026-08-14-stage4-product-code-and-task-contract-input-inventory-correction-review-v1.md` | `2c5abce8085642ff02d81fef3552e154917145f581b63b64f1df81a9f4f92137` |

### 1.3 暫定の上流候補

| 役割 | path | SHA-256 | 本契約での扱い |
| --- | --- | --- | --- |
| Task Contract構想 | `docs/concepts/2026-08-02-task-contract-centered-engineering.md` | `80f388b9308450f1758f623346e25fa6623c8d5d59cb32979436ee3831af1d91` | 11項目の選定元。正式正本にはしない |
| 製品Intent候補 | `docs/intent/2026-08-02-task-contract-centered-intent-amendment.md` | `85aa1fb5cc57255b57b14e4af0eaa2a8c498fba400bea2db3cc9e307d2bc5a44` | 機微情報保護とSession派生物の候補入力 |
| 既存要求一覧 | `docs/requirements/remaining-feature-requirements.md` | `ec31ce53ce097a8ff8a59a4649d97e4af8d8dd0cbdb8a1a8c7d4e8d2a1f8bcf6` | 要求IDの所在確認だけに使う |
| 要求差分候補 | `docs/requirements/2026-08-02-task-contract-requirements-delta.md` | `9c69f54aae6b03549844db73aab24aac0d448f856f2b3faf81f2b0549ece9ccd` | G25との部分対応と対象外を調べる |
| 第5段設計の継承候補 | `docs/design/2026-08-02-stage-five-to-task-contract-inheritance.md` | `b75450300fc6a254843d5353be17d66838553376393d68a0da8f529ab26cdd5e` | rawと派生物の分離境界だけを確認する |
| Task Contract設計候補 | `docs/design/2026-08-02-task-contract-design-amendment.md` | `55115696a3a33612fa52d7fab59dddccb2045ef6baba982a4b5fe17437b25eda` | Session Evidence Source全体を本契約へ取り込まないための境界入力 |

【記録】対応候補IDは`REQ-SESSION-001`〜`003`、`REQ-PORTABLE-002`、`REQ-PORTABLE-004`である。
本契約は、取込範囲の管理、raw保存、追記・改変判定、保存時の原子性、保持・削除を実装しないため、これらの
要求全体を満たすとは主張しない。G25に対応する「一つの既知形式を解析し、伏字化した派生候補と来歴を値として
作る」部分だけを扱う。

【記録】上流候補には、source catalog、開発方針、統合Intentへの直接参照不一致が計3件ある。
本契約の責務は上記の利用者Decisionから固定し、3件を成功条件へ使わない。関連が生じた場合は競合入力として
利用者へ戻す。

### 1.4 Identity（識別）

| 項目 | 値 |
| --- | --- |
| `task_contract_id` | `TC-RC3-PRODUCT-G25-SESSION-ARTIFACT-PREPARATION-001` |
| `contract_type` | `product_delivery` |
| `version` | 1 |
| 正式な責務の出所 | `DEC-RECOVERY-PLAN-V5-STAGE4-COMPLETION-2026-08-14-V1` |
| `source_requirement_ids` | なし。正式採用済みRequirementが存在しないため空とする |
| 対応候補 | `REQ-SESSION-001`〜`003`、`REQ-PORTABLE-002`、`REQ-PORTABLE-004` |
| `prior_contract_id` | なし |
| 内容識別 | 本候補fileのSHA-256を定義挑戦と承認Decisionから参照する |
| 記録形式 | 第5段最初の候補用Markdown。G30の未完成schema・生成器・状態機械を使わない |

【判断】正式なRequirementが無いことを推測で埋めない。利用者が本契約を承認しても、対応候補5件の全体を
自動的に正式採用したことにはしない。

## 2. Responsibility（責務）

利用者が許可した一つのローカルSession記録について、次を一回の読み取り専用処理で行う。

1. Claude JSONL、Codex公開JSON stream、Codex rolloutの三形式のいずれかを識別する。
2. 共通eventへ解析する。未知または不完全なrecordを既知形式として推測しない。
3. 承認済み規則に一致する文字列を伏字化し、高い乱雑性を持つ未登録値が残れば停止する。
4. 伏字化転写、要約、元記録と派生候補を結ぶ来歴を生成する。
5. 許可した項目だけから出力候補を組み立て、低い乱雑性であっても絶対pathが残れば停止する。
6. 利用者が確認できる構造化結果を標準出力へ一回だけ返す。

【判断】「機微情報をすべて検出する」とは約束しない。既定規則、高い乱雑性の検査、絶対pathの最終検査で
確認できる範囲を保証し、結果は外部送信許可済みとは扱わない。

## 3. Boundary（境界）

### 3.1 範囲内

- 一つの`raw_log`と、その親範囲を示す`raw_root`。
- G25の固定10 pathと、公開関数`tools.session_logs.pipeline.prepare_artifact`から到達する処理。
- 実装時に追加する薄い読み取り専用入口、同入口の試験、`pyproject.toml`の実行名一件。
- 成功、警告付き部分結果、停止結果を示す一つの構造化出力。

### 3.2 範囲外

- Session記録の探索、複数file一括処理、raw保存、派生物保存、backup、復旧、追記・改変判定。
- 設定file、G26、G27、G28、G30、既存の広いSession CLIへの依存。
- 外部送信、network、外部process、Git、権限変更、scheduler、hook、Issue状態変更。
- home、利用者名、host名その他の環境値の自動取得。
- Contextへの採否、Task実行状態、retention、削除、access policyの決定。
- 利用者の判断、決定、意図を要約から自動推測すること。

【実測】G25に含まれる`redaction.py`には、今回の入口から到達しない`resolve_environment_rules`、
`redact_with_environment`、`write_sensitive_report`が同居する。これらは本契約の許可能力に含めない。
file単位の在庫分類と、契約実行時の到達境界を混同しない。

## 4. Preconditions（前提）

- 本契約案と実装開始が利用者に承認されている。
- `raw_root`と`raw_log`は絶対pathであり、解決後の`raw_log`が解決後の`raw_root`内にある。
- `raw_log`は利用者が処理を許可した通常fileであり、読取り可能である。
- 入力の先頭recordが三つの対応形式のいずれかを一意に示す。
- 伏字化にはG25の既定pattern規則を使う。環境値解決と個別allowlistは使わない。
- 薄い入口はG25の返却値を汎用的に辞書化せず、§7で許可した項目だけを選ぶ。
- tool版はインストール済み製品版から導出し、利用者入力で上書きしない。
- G25の固定tree SHA-256が
  `f476cbf6df63bc2accfb188764b2b8216aefdb7c446572b40b56b2cbcab861e4`と一致する。
- 固定10 pathに変更があれば本契約候補をstaleとし、実装開始前に再挑戦する。

## 5. Context Obligations（必要材料）

| 材料 | 必須性 | 充足条件 |
| --- | --- | --- |
| 第4段完了Decision | 必須 | §1.1のSHA-256一致 |
| G25固定コード | 必須 | commit `66d608e5b5d605ddaf387bbd75a507ac934800c6`、10 path、tree SHA一致 |
| G25直接関連試験 | 必須 | 14 fileのtree SHA-256 `7892fc7ab6424a5624abebfe90a136802312e577278c8b5b455c42caa3623d32` |
| 第4段Evidenceと訂正レビュー | 必須 | §1.2のSHA-256一致 |
| 上流候補 | 参考 | 暫定表示と3不一致を保持し、権威として自動採用しない |
| 受入fixture | 実装時必須 | 三形式の合成例、種別不明、root逸脱、機微情報残存、解析警告の各一例 |
| 実Session記録 | 不要 | 定義挑戦と通常試験ではrepositoryへ置かない |

## 6. Allowed Capabilities（許可能力）

- 指定された`raw_log`一件の読取り。
- 引数と読取りbytesを使ったメモリ上の解析、伏字化、要約、内容識別値計算。
- インストール済み製品版の読取り。
- 許可した項目だけから成る構造化結果一件の標準出力と、秘密値を含まない終了区分の返却。

禁止する能力は、file書込み、network、外部process、Git、環境値解決、権限変更、永続化、外部送信である。
標準出力は利用者が明示実行した一回の結果に限り、別fileへ自動保存しない。

## 7. Expected Outputs（期待成果）

### 7.1 正常結果

標準出力へ正準化したJSON一件を返し、終了コード0とする。最低限、次を含む。

- `status: ok`
- `source_kind`
- 伏字化済み`transcript`
- 伏字化済み`summary`
- raw相対path、行範囲、raw・転写・要約・規則のSHA-256、tool版を持つ`provenance`
- 伏字化規則のlabelと件数
- `external_send_approved: false`

未伏字の共通event、raw bytes、規則pattern、秘密候補、絶対pathを出力しない。`PreparedArtifact`の
汎用的な全項目変換は禁止し、`events`は出力候補へ含めない。

### 7.2 解析警告がある結果

既知形式の途中に未知、不完全、または不正なrecordがある場合は、推測せず`kind`、行番号、block番号だけを
`parse_issues`へ入れる。入力由来の`detail`は出力しない。`status: partial`と非0終了コードを返し、完全な成功として扱わない。
解析できた部分の伏字化結果を返してよいが、raw断片や未伏字eventは返さない。

### 7.3 停止結果

種別不明、root逸脱、読取不能、規則不正、高い乱雑性を持つ未登録値の残存、低い乱雑性を含む絶対pathの残存、
内部失敗では、成功成果を返さず非0終了コードにする。
出力する失敗区分は固定語彙だけとし、秘密値、raw断片、例外本文、絶対pathを含めない。

## 8. Acceptance Criteria（受入条件）

1. 利用者がインストール済み入口を一回実行し、三形式それぞれから§7の構造化結果を得られる。
2. 同じraw bytes、root、規則、tool版から同じ結果を得る。
3. 解決後のraw pathがroot外へ出る通常pathとsymlinkを、読取り前に拒否する。
4. 種別不明を既知形式へ推測しない。
5. 高い乱雑性を持つ未登録値、または低い乱雑性を含む絶対pathが出力候補に残る場合、転写・要約・秘密値を
   出力せず停止する。
6. 正常出力に未伏字event、raw bytes、規則pattern、絶対pathが含まれず、汎用的な全項目変換を使わない。
7. parse issueがある結果を完全成功にせず、未知recordの内容を出力しない。
8. raw、転写、要約、規則の内容識別値を独立再計算し、来歴と一致する。
9. 実行前後でrepositoryとraw fileのbytesが不変であり、file書込み、network、外部processが0回である。
10. 新入口の対象試験、G25直接関連55件、正規全試験が単独commandで成功する。
11. 新入口を使わない既存処理の既定動作を変えない。
12. 利用者が出力例を確認し、製品処理として受け入れる。

【判断】危険度が高い理由は、Session記録が機微情報を含み得るためである。実装時の高危険度確認は、
root逸脱、種別不明、秘密値残存、未伏字event出力、禁止した外部作用に限定する。全機能への一律の高価な検査は行わない。

## 9. Provenance Obligations（来歴義務）

- 本契約案、定義挑戦、利用者承認、失敗確認、実装、試験受領記録、利用者向け受入結果、実装後レビューを
  commitとSHA-256で結ぶ。
- 受領記録にはPython版、pytest版、入口版、終了コード、対象試験、全試験、代替実行の有無を含める。
- 代表入力は合成または機微情報を除いたfixtureとし、実Session raw、未伏字転写、秘密値をrepository内の証拠へ
  保存しない。
- 実行結果の証拠には出力schemaと内容識別値だけを残し、利用者データ本文を残さない。
- 契約、G25固定コード、伏字化規則、入口のいずれかが変われば、影響する受領記録をstaleとする。

## 10. Escalation Policy（利用者へ戻す条件）

次の場合は実装または実行を停止し、契約を暗黙に広げず利用者へ戻す。

- G26、G30、他142 path、保存、探索、外部送信、環境値解決が必要になった。
- 暫定上流候補または既知不一致3件の採否が、責務や受入条件を変える。
- G25固定コードを変更しなければ新入口を実装できない。
- 既定規則だけでは利用者が必要とする機微情報境界を満たせない。
- 同じ入力で結果が変わる、秘密値が結果または例外へ出る、禁止した外部作用が起きる。
- 安全な項目選択または最終出力検査では、契約の出力境界を満たせない。
- 実装範囲、risk、出力、許可能力、受入条件を変える必要がある。

retryは、入力path、対応形式、または一時的な読取失敗を利用者が訂正した場合だけ許す。秘密値残存をallowlistで
迂回して成功へ変えない。

## 11. 版付きdependency

| dependency | 固定値 | 変更時の扱い |
| --- | --- | --- |
| G25コード | commit `66d608e5b5d605ddaf387bbd75a507ac934800c6`、tree SHA `f476cbf6...61e4` | 契約候補をstaleにして再挑戦 |
| G25関連試験 | 14 file、tree SHA `7892fc7a...d32`、55件成功 | 変更理由と影響範囲を確認 |
| 製品入口の登録正本 | `pyproject.toml`の`[project.scripts]` | 実行名変更時は導入後の入口を確認 |
| Task Contract構想 | SHA `80f388b9...1d91` | 自動追随せず差分を利用者へ提示 |
| 現行開発方針 | SHA `422d234a...fac` | 実装前に現行版を再固定 |
| Python | 3.13系 | 実装受領記録で実版を固定 |
| pytest | 8.4系 | 実装受領記録で実版を固定 |

## 12. 実装方法の三案比較

| 観点 | 案A：既存公開関数だけ | 案B：既存の広いCLIのdry-run | 案C：薄い読取り専用入口 |
| --- | --- | --- | --- |
| 内容 | `prepare_artifact`をPythonから直接呼ぶ | `tools.session_logs.cli --dry-run`を使う | G25だけを呼ぶ専用入口を追加する |
| 単純さ | 新実装0で最も単純 | 既存だが設定・探索・保存群を通る | 小さい引数処理と出力変換だけを追加 |
| 処理時間 | 最小 | 探索と設定読込みが増える | Aとの差は小さい |
| メモリ | 最小 | 複数対象探索で増え得る | 一件だけでAと同程度 |
| 頑健さ | API利用者が入力と出力変換を毎回正しく行う必要 | G26の未解決保存境界と広い例外経路を持つ | path、出力、失敗語彙を一入口で固定できる |
| 変更範囲 | 0 | 0だが保留中のG26等へ依存 | 新入口1件、`pyproject.toml`の実行名1件、対象試験1件 |
| 保守負担 | 利用者ごとの手製接続が増える | 広いCLI全体の保守へ結合する | 小さい入口一件を保守する |
| 戻しやすさ | 変更なし | 変更なしだが依存境界を戻せない | 新入口、実行名、対象試験を外せば戻る |
| 現在目的への適合 | 利用者向け正規入口がなく未達 | 一件処理より広く、承認済み除外範囲へ入る | 一件、読取り専用、構造化結果に限定できる |

【提案】案Cを採用する。案Aは最小だが、人がPython呼出しと安全な出力変換を毎回つなぐため、正規の製品入口に
ならない。案Bは実装0だが、保留中のG26、探索、設定、保存境界へ依存し、承認済み範囲を越える。案Cは新実装を
要するが、必要な保証を満たす最も単純な意味的完結単位である。

実装を承認した場合の変更候補は次の三つだけとする。

- 新規：`tools/session_logs/read_only_entry.py`
- 変更：`pyproject.toml`の`[project.scripts]`へ専用実行名一件を追加
- 新規：`tests/test_session_log_read_only_entry.py`

G25の既存10 pathは変更しない。変更が必要と判明した場合は§10に従って停止する。

## 13. 実装順序とTDD境界

1. 新入口が存在しない状態で、§8の入口固有条件が失敗する試験を用意する。
2. 試験内容と、既存G25が担う条件・新入口が担う条件の分担を確認する。
3. 利用者の実装開始承認後、案Cの三pathだけを変更して成功させる。
4. 対象試験、G25関連55件、正規全試験を実行する。
5. root逸脱、高乱雑性値の残存、低乱雑性の絶対path残存、未伏字event出力、入力由来の`detail`出力、
   禁止外部作用の六境界だけを故障注入または独立oracleで確認する。
6. 利用者向け合成例を正規入口から実行し、結果を利用者へ提示する。
7. 契約適合確認と最終挑戦を一回の独立完了レビューで行う。

## 14. 成果物の役割と終了時の扱い

| 成果物 | 完成時の役割 | 役割終了時 |
| --- | --- | --- |
| 承認済みTask Contract | 現在の動作保証と履歴・監査の両方 | 後継版から参照して履歴保存 |
| 読取り専用入口 | 現在の動作保証 | 後継入口へ移行後、参照と利用先を確認して削除または使用停止 |
| 入口の試験 | 現在の動作保証 | 入口の役割終了と同時に判断 |
| 定義挑戦・承認・実装Evidence・完了レビュー | 履歴・監査資料 | Git履歴で保存 |
| 一時fixture・一時受領記録 | 実施中の確認材料 | repository外で破棄。必要な識別値だけEvidenceへ残す |

## 15. Human判断点

独立した定義挑戦後、利用者が次を判断する。

1. 本契約の責務、境界、前提、能力、出力、受入条件を承認するか。
2. 「既定規則、高乱雑性検査、絶対path検査で確認できる範囲であり、その他の低乱雑性の機微情報をすべて
   検出する保証も外部送信許可もない」という限界を承認するか。
3. 案Cと三pathの変更範囲で実装開始を承認するか。
4. 上流候補を暫定のまま、部分対応だけを記録して進めるか。

## 16. 未実施

【未実施】本契約の利用者承認、実装開始、コード・試験・設定・`pyproject.toml`の変更、失敗試験の作成、
Task Contract実行基盤の使用、G25 lifecycle表示の変更、G26・G30の使用、上流候補の正式化、外部送信、
実Session記録の読取り、push、tag、amend、rebase、reset、履歴書換えは行っていない。
