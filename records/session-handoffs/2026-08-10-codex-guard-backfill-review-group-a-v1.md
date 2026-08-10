# 守り役後追い独立レビュー #6第2単位 group A 判定 v1

- Reviewer model：`gpt-5.6-sol`
- reasoning effort：`high`
- model来歴：`~/.codex/config.toml`の実効値 `model = "gpt-5.6-sol"`、
  `model_reasoning_effort = "high"`
- レビュー日：2026-08-10
- Reviewer：Codex
- collaboration mode：`role_neutral_pilot_review`
- レビュー段階：implementation（既存の守り役codeに対する後追いレビュー）
- risk：`low`（Human確定済み）
- 総合判定：`reported_unverified`
- Finding：blocking 2件、non-blocking 0件、defer 0件

## 1. 固定対象と開始状態

- 範囲固定：
  `records/session-handoffs/2026-08-10-claude-pilot-guard-backfill-high-reviews-scope-v1.md`
  （commit `bedf986408156e661c4a15c6886a4e9558d514ec`、SHA-256
  `6b587a7eedf77380aadf5b41ab90edd148bdcd6f69b850447dc684591737f8e9`）
- 判定基準：`docs/development/work-review-protocol.md`（§3・§4.7・§11、SHA-256
  `403491ca1c8f37abeee373ef06401610bc726361f7897611a020d7e3656c6772`）
- レビュー開始時HEAD：`bedf986408156e661c4a15c6886a4e9558d514ec`
- branch：`main`
- 対象：`tools/common/digests.py`、`tools/common/paths.py`、
  `tools/task_contract/identity.py`
- 許可範囲：対象と既存testの読取り、一時領域での反証、本判定recordの新規作成と単独commit
- 禁止範囲：code、test、既存record、実台帳、実設定、利用者環境の変更、外部操作、
  Findingの修正、TODO・checklist反映
- 期待成果：moduleごとの§4.7判定、§11区分のFinding、反証のcommand・結果・終了コード、
  model来歴を持つ本record 1件と、その単独commit
- 停止条件：固定入力Digest不一致、許可path外の変更が必要な場合

【記録】Humanは2026-08-10に「#6第2単位 risk lowを確定、着手を承認する」と明示した。
`pilot-driven-record-handoff.md` §2.7により、このHumanのchat文言をrisk確定と着手承認の正とした。

【実測】開始時のworktreeとindexはcleanで、HEADは固定commitと一致した。
`git show --name-status bedf986`は範囲固定record 1件だけの追加を示した。
範囲固定§3の固定入力4件は、`shasum -a 256`による再計算で全件一致した。

| 固定入力 | 再計算したSHA-256 |
| --- | --- |
| Human裁定 | `d73f51a17ef20fa6a5abb531c30119384582cec9c299102e518088e3bb51afa7` |
| 対象一覧 | `77b6ba9fc0bfd7ea17e071dc4e4df59e12f84f4a7d23798dedafe58b6ea6571e` |
| 共通レビュー基準 | `403491ca1c8f37abeee373ef06401610bc726361f7897611a020d7e3656c6772` |
| `TODO_NEXT_SESSION.md` | `6de9d6d8b4f0ebc93f59e7fbe1ee6e192f5aba27e7b94e4e5dfe673e65b6205a` |

【実測】確定pathへの`git check-ignore --no-index`は終了コード1で、ignore対象外だった。
作成前の`test -e`も終了コード1で、同名fileが存在しないnew-only状態だった。

## 2. 実装と既存testの読取り

【実測】対象3 moduleと直接・結線・E2Eの既存testを再読込みした。対象bytesのSHA-256は次のとおり。

| 対象 | SHA-256 |
| --- | --- |
| `tools/common/digests.py` | `db6b830592f5d57ef7b42b5ec32fd398f4c36957a978604166525fc54da3396f` |
| `tools/common/paths.py` | `daa325791b5bead80c240eb298c7084f6c26ff2d96ca850cc65449686cc4826d` |
| `tools/task_contract/identity.py` | `bbbce848e3beb50301c2ef4e242a75daf64968a0d5c1f2f733751ac2a75a5c42` |
| `tests/test_common_digests.py` | `a665e1c6c0e4b7ed262c375db8cbfb4de80e5c3b55bdf930feeeb4467bc1d924` |
| `tests/test_common_errors_paths_output.py` | `955dd9922f09d3a9d707889e1d9a77454eaf21d8f6f44637efb64c4ed03c53a8` |
| `tests/test_shared_function_sweep.py` | `b255834a7b7dc6bcc97b884328af6f9c072ff5ce88bd4570e16fa526a03f8260` |
| `tests/test_first_review_task_contract_e2e.py` | `cc99faaa4813aa629c9640431e31d4da635890bc5ec1e1f30c631d06c513661f` |

【記録】`docs/design/2026-08-02-task-contract-design-amendment.md` §3.1は、構造化正本を
「JSON互換の閉じたschema」とし、UTF-8、key順、number・boolean・nullの許可範囲、path・IDの
正規化、Digest algorithmを固定対象にしている。

【実測】既存testは、既知SHA-256、通常のkey順と最上位`content_digest`除外、通常の内外path、
共通関数への結線、Task Contractの正常系と既知改竄を覆う。一方、今回使った非文字列key、tuple、
NaN、大文字小文字alias、NFC/NFD aliasは既存fixtureになかった。

## 3. 既存testの独立再実行

【実測】次の単独commandは終了コード0、`96 passed in 0.49s`だった。

```text
.venv/bin/python3 -m pytest -q tests/test_common_digests.py tests/test_common_errors_paths_output.py tests/test_shared_function_sweep.py tests/test_first_review_task_contract_e2e.py
```

【判断】既存testの合格は確認したが、§4.7の`verified`には反証結果も必要であり、本結果だけを
合格根拠にはしない。

## 4. 既存fixtureにない反証

### 4.1 実行環境と一時領域

【実測】反証はPython 3.9.6、`macOS-26.5.1-arm64-arm-64bit`で実行した。
fileを使う反証はすべて`TemporaryDirectory(dir="/private/tmp")`だけへ作成し、終了時に消去した。
repository内、実台帳、実設定、利用者環境への書込みは行っていない。

### 4.2 実行一覧

`python3 -c`の山括弧内は、同じ行に渡した反証処理の要約である。結果欄へ入力と独立oracleを
再現できる値を記す。

| ID | command | 結果 | 終了コード |
| --- | --- | --- | --- |
| D1 | `.venv/bin/python3 -c '<key順・Unicode NFC/NFD・整数/浮動小数・±0・内外content_digest・非JSON表現衝突をassertしてJSON出力>'` | key順は同一、最上位`content_digest`は除外、nested同名keyは算入、NFC/NFD・`1/1.0`・`-0.0/0.0`は別Digest。`{1:"value"}`と`{"1":"value"}`、tupleとlistはそれぞれ同一Digest | `0` |
| P0 | `.venv/bin/python3 -c '<通常・相対・dotdot・symlink・case・NFC/NFDを一括assert>'` | 通常・相対・dotdot・symlinkのassert通過後、同一実体aliasのassertで`AssertionError` | `1` |
| P1 | `.venv/bin/python3 -c '<case/NFC/NFD aliasをos.path.samefileとwithinで切分け>'` | caseは`same_inode=true / within=false`、Unicodeは`same_inode=true / within=false` | `1` |
| P2 | `.venv/bin/python3 -c '<通常内外・共通prefix・相対脱出・symlink脱出・broken symlink・root symlinkをassert>'` | inside、same root、relative inside、outside→inside symlinkは`true`。sibling、dotdot、relative escape、inside→outside symlink、broken outside symlinkは`false` | `0` |
| P3 | `.venv/bin/python3 -c '<実在private directoryのcase/NFC/NFD aliasをsamefile oracleでassert>'` | case targetとUnicode targetはいずれも`same_inode=true / within=false`となり、安全性assertが失敗 | `1` |
| I1 | `.venv/bin/python3 -c '<正常seal・Digest改竄・safe_relative_path・非JSON recordのseal/validateと衝突をassertしてJSON出力>'` | 正常recordは合格、Digest改竄と6種の不正相対pathは拒否。非文字列key、tuple、NaNは`validate_record`に合格し、key表現とsequence表現の衝突は`true` | `0` |
| I2 | `.venv/bin/python3 -c '<再帰的JSON互換oracleで非文字列key・tuple・NaNを不適合とし、validate_recordの拒否をassert>'` | oracle不適合3件を`seal`と`validate_record`が全件合格。非文字列key対文字列key、tuple対listのDigest衝突も`true`。拒否期待assertが失敗 | `1` |

### 4.3 反証の機械出力

【実測】D1の出力は次だった。

```json
{"integer_float_distinct": true, "key_order_stable": true, "negative_zero_distinct": true, "nested_content_digest_included": true, "non_string_key_collision": true, "top_level_content_digest_excluded": true, "tuple_list_collision": true, "unicode_nfc_nfd_distinct": true}
```

【実測】P3は次を出力してから`AssertionError`となった。

```json
{"case_target_same_inode": true, "case_target_within": false, "unicode_target_same_inode": true, "unicode_target_within": false}
```

【実測】I2は次を出力してから`AssertionError`となった。

```json
{"nan_value": {"accepted": true, "digest": "f385c7fd124b40079176de0c2e9a0c58e94032ff16d4cf2afcf48c2315dbf292"}, "non_string_key": {"accepted": true, "digest": "599fd8ca27a1ac437b555c7c2e41a7579a59b0ddc976277e62a208aa93dd934c"}, "non_string_key_collision": true, "tuple_list_collision": true, "tuple_value": {"accepted": true, "digest": "cc5329f6a306e6776c07d3c2b943aceb34fb85b3c59d0c6b932b6f83ef2b0069"}}
```

## 5. moduleごとの判定（§4.7）

| module | 判定 | Evidenceと理由 |
| --- | --- | --- |
| `tools/common/digests.py` | `reported_unverified` | D1でJSON互換域の指定済み正規化は期待どおりだったが、JSON互換でない異なる入力表現を拒否せず同一Digestへ畳む反証が成立した。F-A1により`verified`にできない |
| `tools/common/paths.py` | `reported_unverified` | P2の通常・相対・symlink境界は期待どおりだったが、P1・P3で同じfilesystem実体をcaseとNFC/NFDの表記差によりroot外と誤判定した。F-A2により`verified`にできない |
| `tools/task_contract/identity.py` | `reported_unverified` | 正常record、Digest改竄、不正相対pathの既知境界は期待どおりだったが、JSON互換でない3表現を`seal`・`validate_record`が合格させ、2種のDigest衝突を同一性として受け入れた。F-A1により`verified`にできない |

【判断】3 moduleすべてにblocking Findingが対応するため、group Aの総合判定は
`reported_unverified`である。§6が定める不足Evidenceではなく、§11.1類型3の機械反証を根拠とする。
固定された完了報告と事後状態の競合はないため`report_execution_mismatch`ではない。
範囲固定§8.3はblocking検出を停止条件にせずrecordへ固定してgroupを完了させるため、`blocked`でもない。

## 6. Finding（§11）

### F-A1 blocking／implementation／§11.1類型3

対象：`tools/common/digests.py`、`tools/task_contract/identity.py`

【実測】非文字列keyを持つmappingと文字列化後のkeyを持つmapping、tupleとlistは、それぞれ
異なるPython値であるにもかかわらず同じcanonical bytesとDigestになった。NaNを含むrecordを含め、
独立の再帰的JSON互換oracleが不適合とした3種を`seal`と`validate_record`は全件合格させた。

【記録】上流設計は構造化正本をJSON互換の閉じたschemaとし、number等の許可範囲と正規化を
固定対象にしている。

【判断】JSON互換でないrecordを拒否せず、異なる入力を同一Digestで合格させるため、identity・Digest
束縛に「誤った合格」を生む検証欠陥である。§11.1類型3のblockingとする。同じ欠陥類型の変種として、
key型、sequence型、非有限数を本周回で一括掃討した。

### F-A2 blocking／implementation／§11.1類型3

対象：`tools/common/paths.py`

【実測】caseだけが違う実在directoryとNFC/NFDだけが違う実在directoryについて、
`os.path.samefile`はそれぞれ同一実体を返したが、`within`は両方`False`を返した。

【判断】実際にはroot内であるpathをroot外と誤分類する境界判定の偽陰性である。
`within`は「内側なら拒否」の否定形guardにも共通利用されており、この偽陰性はroot内pathを
root外として誤って合格させうる。機械反証を伴う§11.1類型3のblockingとする。同じ欠陥類型の
case表現とUnicode表現を本周回で一括掃討した。

### non-blocking／defer

【判断】non-blocking Findingは0件、defer Findingは0件である。F-A1、F-A2の修正は本レビューscope外で
あり、Finding自体をdeferへ格下げしない。

## 7. Human境界、禁止事項、未実施

【実測】本record作成前の`git diff --name-status bedf986 -- tools tests records/session-handoffs`は
出力なし、終了コード0だった。反証は一時領域だけを使い、対象code、test、既存record、実台帳、
実設定、利用者環境を変更していない。外部送信、不可逆操作、push、tag、履歴書換えも行っていない。

未実施：F-A1・F-A2の修正、新規test作成、既存test変更、全Test、TODO・checklist反映、
group B以降のレビュー、Closer作業、外部操作。

【判断】risk `low`は成果物が本レビューrecord 1件だけであることに対するHuman確定であり維持した。
守り役code自体の判定では、依頼どおり既存fixture外の独立反証を追加した。

## 8. 判定と次のHuman判断

判定：`reported_unverified`。

【判断】レビュー作業と本recordは完了したが、対象3 moduleはF-A1またはF-A2により
`verified`ではない。blockingを修正せず、禁止された実装変更を未実施のまま保持した。

次：Humanが本Findingを確認し、現行Plan上で次のいずれかを選ぶ。

1. いま対処：F-A1・F-A2を、守り役code修正の別`high` risk作業単位として範囲固定する。
2. 候補として後回し：Findingを未解消のまま保持し、修正候補へrouteする。
3. 本線へ戻る：本groupの修正には着手せず、固定済み第2単位のgroup Bレビューへ進む。
