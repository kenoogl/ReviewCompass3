# group A 共通正本修正 範囲レビュー結果 v1

- レビュー日：2026-08-10
- Reviewer：Codex
- collaboration mode：`role_neutral_pilot_review`
- レビュー段階：scope（実装前の範囲レビュー）
- risk：`high`（Human確定済み）
- 判定：**要修正**
- 実行状態：`correctly_stopped_before_RED`
- Finding：blocking 1件、non-blocking 0件、defer 0件
- model来歴：`~/.codex/config.toml`の実効値 `model = "gpt-5.6-sol"`、
  `model_reasoning_effort = "high"`

## 1. 固定対象と開始状態

- 対象：
  `records/session-handoffs/2026-08-10-claude-pilot-common-guard-fix-scope-v1.md`
- 対象SHA-256：`b9a7f49ad5897525e2f572c6da86d2f09b083d8dc108ab798fd5c00fb631d163`
- 対象commit：`35941724c8e0cc99c6974c52ccb39218199d993b`
- base：`17c2002491bf004b741077676845de56da845fbe`
- branch：`main`
- 対象Finding：group A判定record（commit `17613d2`）のF-A1・F-A2
- 修正順序：Human裁定record（commit `4bb1c9b`）のE → A → B → C → D
- 許可範囲：本判定record 1件の新規作成と単独commit、読取り、決定的な照合
- 禁止範囲：対象scope、code、test、既存record、config、schema、上流設計、TODO、
  checklistの変更、RED・GREEN開始、push、履歴書換え

【実測】対象commitの親は申告baseと一致し、変更pathは対象scope 1件の追加だけだった。
レビュー開始時のworktreeとindexはcleanで、`git diff --check 3594172^ 3594172`は終了コード0だった。

【実測】scope §3に固定された8入力のSHA-256を内容から再計算し、8／8で記載値と一致した。

| 固定入力 | 再計算したSHA-256 |
| --- | --- |
| group A判定record | `34a53581751a5b23864933b3ab23e08a875170ab5cdbe08e00e112c803da5139` |
| 修正順序のHuman裁定 | `f69f8a969e732072514a44f684c7b216687e9d63cf2d4af9d280d2ea16f15997` |
| Task Contract設計改定 | `55115696a3a33612fa52d7fab59dddccb2045ef6baba982a4b5fe17437b25eda` |
| 共通レビュー基準 | `403491ca1c8f37abeee373ef06401610bc726361f7897611a020d7e3656c6772` |
| `TODO_NEXT_SESSION.md` | `bcab80e9f52fcaa1a594567ca79d03be6f3777ecebb83cc8eb4ca7b987d78164` |
| `tools/common/digests.py` | `db6b830592f5d57ef7b42b5ec32fd398f4c36957a978604166525fc54da3396f` |
| `tools/common/paths.py` | `daa325791b5bead80c240eb298c7084f6c26ff2d96ca850cc65449686cc4826d` |
| `tools/task_contract/identity.py` | `bbbce848e3beb50301c2ef4e242a75daf64968a0d5c1f2f733751ac2a75a5c42` |

【実測】本recordの確定pathに対する`git check-ignore --no-index`は終了コード1、作成前の
`test -e`も終了コード1で、ignore対象外かつnew-onlyだった。

## 2. 上流authorityと修正範囲

【記録】Task Contract設計改定 §3.1は、構造化正本をJSON互換の閉じたschemaとし、UTF-8、
key順序、number・boolean・nullの許可範囲、path・IDの正規化、Digest algorithmを固定対象にする。

【判断】F-A1で非文字列key、tuple等の非JSON型、NaN・正負Infinityを拒否し、既存のkey順、
UTF-8、`content_digest`除外、SHA-256を維持する方向は、既存authorityへの適合に収まる。
新しいschemaまたはDigest algorithmの導入ではない。

【判断】F-A2で、case差またはUnicodeのNFC／NFD差だけがある同一filesystem実体を
`within`で同じ境界として扱う方向は、F-A2の成立反証を閉じるものである。存在しないpathの
従来判定とfail-closedを維持し、新しいpath種別または呼び出し契約を導入していない。

【記録】`DEC-SHARED-FUNCTION-POLICY-001`は、Digestとpath境界を`tools/common/`の共通正本へ
一元化し、意図的な複製を禁止し、正本の変更をHuman承認事項とする。

【実測】`tools/task_contract/identity.py`の`content_digest`は
`tools.common.digests.canonical_content_digest`へ直接結線され、`seal`と`validate_record`は
その共通正本を使う。`canonical_bytes`は同file内の正規化関数であり、repository内の呼び出しは0件だった。

【判断】`identity.py`をF-A1の許可pathに含めることは、元Findingが同moduleの`seal`・
`validate_record`を対象とし、scopeが`canonical_bytes`を含むJSON互換境界を固定しているため、
はみ出しではない。共通Digest正本との結線を維持するという境界もscopeの「正本」宣言と一致する。

【実測】`within`の利用側は共通関数へ結線されており、通常の内外判定と結線は既存testで固定されている。

【判断】F-A2は共通正本の挙動修正だけで各利用側へ届くため、`within`の呼び出し側を変更しない判断は妥当である。
group B〜Dの先取りもない。

## 3. Human境界と停止条件

【記録】Humanはgroup A修正のrisk `high`を確定し、着手を承認済みである。修正順序の裁定は、
group Aを1つの`high`修正単位とし、範囲固定、範囲レビュー、Human裁定、RED、GREEN、完了レビュー、
Closerの順を要求する。

【判断】risk確定と着手承認の欠落はない。scope §8は、固定入力不一致、許可path外の必要、
上流矛盾に加え、既存の実台帳recordがJSON互換検査で拒否される場合と既存recordのDigest値が
変わる場合を明示的な停止条件にしている。移行要否やDigest変更を実装側で裁定せずHumanへ返すため、
指定されたHuman境界は維持されている。

## 4. F-A1・F-A2と受入条件

【実測】scopeはF-A1の非文字列key、tuple／list、非有限数と、F-A2のcase差、NFC／NFD差を
修正対象へ取り込み、元Finding 2件以外のgroupを含めていない。

【判断】危険側では、異なるPython値が同一Digestとして合格しないことをDigest計算、`seal`、
`validate_record`の3入口で照合する。path側では同一実体に対する`within`と`os.path.samefile`の
一致を照合する。正例側では既存のJSON互換recordの修正前後Digest一致を代表実台帳recordで
機械確認し、値変化時は停止する。危険側と正例側の方向は、範囲レビューの受入条件として妥当である。

【判断】既存testの削除・検査性質の緩和を禁止し、RED後のtest変更をHuman承認へ戻す規則は、
group E scope v3でHuman承認され、完了レビュー `6ece925`でverifiedとなった運用と一致する。

【実測】ただし、`tests/test_common_module_pins.py`は
`tools/common/digests.py`と`tools/common/paths.py`の現在のfile SHA-256を固定し、正本変更時に
承認記録とともにpinを更新することを要求する。現行状態の単独実行は`5 passed`、終了コード0だった。
一方、`digests.py`のbytesへ改行1 byteだけを仮に加えてメモリ上で再計算したSHA-256は
`e7a2332022f4ae48fe3347397617ab5c332d1e39ae1451b7eec842bb62bcbc43`となり、固定値と不一致だった。

【判断】F-A1・F-A2の実装修正は両共通moduleのbytes変更を伴うため、既存pinを変更しない限り
公式全Testは不合格になる。しかしscope §6・§7は`tests/test_common_module_pins.py`をRED、GREEN、
変更可能pathのどこにも含めていない。このままでは「§7以外を変更しない」と「公式全Test合格」を
同時に満たせない。これは実装方式の問題ではなく、変更可能pathとcommit境界の不足である。

## 5. Finding（§11）

### SR-A-SCOPE-001 blocking／scope／§11.1類型4

【判断】共通正本2 fileの変更を検知する既存pin testが、変更可能pathとcommit境界から漏れている。
許可範囲を守ると公式全Testが不合格になり、公式全Testを合格させるとscope §7・§8の禁止境界を破る。
共通正本変更のHuman決定とpin testを固定入力へ結び、当該testの扱いを変更可能pathおよび意味単位commitへ
一意に位置付ける必要がある。禁止事項またはscope境界の破りに当たる§11.1類型4のblockingとする。

### non-blocking／defer

【判断】0件。command option、検査関数の配置、inode照合の具体形、fixture構成などの実装細部には
立ち入っていない。後続groupの論点も持ち込んでいない。

## 6. 判定と次

判定：**要修正**

【判断】対象scope commitは1 fileだけで、申告base、固定入力Digest、risk、Human停止条件、
F-A1・F-A2の方向、既存recordの正例、group Eに沿うRED定義は妥当である。しかし、
SR-A-SCOPE-001により、現scopeをRED開始の根拠にはできない。

Human境界：維持。risk `high`と着手承認は受領済みであり、既存実台帳recordの拒否、既存Digest値の
変化、上流矛盾、許可path外変更の必要が判明した場合は停止してHumanへ戻す。

未実施：対象scope、code、test、既存record、config、schema、上流設計、TODO、checklistの変更、
RED、GREEN、完了レビュー、Closer作業、push、履歴書換え。

次：PilotがSR-A-SCOPE-001を反映した新しいscopeを単独commitして停止し、Codexが再範囲レビューする。
