# Pilot範囲漏れ原因分析 レビュー結果 v1

- レビュー日：2026-08-10
- Reviewer：Codex
- collaboration mode：`role_neutral_pilot_review`
- レビュー段階：completion（Pilot自己申告の原因分析record）
- risk：`medium`（Human指定）
- 対象：
  `records/session-handoffs/2026-08-10-claude-pilot-scope-omission-cause-analysis-v1.md`
  （commit `4c8d7bc6334e0b92b47bf3336b11319a11229cd0`、SHA-256
  `ebc25f88e8655790050d9dc440ba976d021c8f64ef9f94a9858a3a46042ab1f4`）
- 関連Human裁定：
  `records/development/2026-08-10-scope-prescan-rule-decision-v1.md`
  （commit `5a67f5a51f89235d2b38ecef5fc897d7cefc7212`、SHA-256
  `6dac7c6655e12f7d2d0f828baf0b6bae1393083d685ecbeabfccb90d97029cf5`）
- 判定基準：`docs/development/work-review-protocol.md`（SHA-256
  `403491ca1c8f37abeee373ef06401610bc726361f7897611a020d7e3656c6772`、
  特に§4.7・§11）
- model来歴：`~/.codex/config.toml`の実効値 `model = "gpt-5.6-sol"`、
  `model_reasoning_effort = "high"`

## 1. 判定

判定：**要修正（`report_execution_mismatch`）**。`verified`ではない。

【実測】Digest固定32件は再現し、CRLF変換の実処理箇所と、group A・Bの3つの依存先を
5手順で事前検出できることも再現した。一方、次の競合Evidenceがある。

1. §1の「範囲の作り直し8回」は、実際には範囲レビューの指摘8件を数えた値であり、
   4 groupのscope改訂commitは7件だった。「実装中の停止4回」も、実装中と完了レビューを
   混ぜなければ4にならず、件数の単位が実commit列から一意に再現できない。
2. §2.1記載のgrepを独立再実行すると35 test fileが列挙され、16 fileにならない。
   16件へ絞る機械条件もrecordに無いため、16件という実測は再現できない。
3. §3・§4は主因をPilotの手順不足へほぼ単独帰属しているが、上流group C判定のF-C5は
   実処理と異なるmoduleを対象欄へ記し、group B範囲レビューは`conftest.py`を発見しながら
   変更必須ではないと判断していた。上流FindingとReviewer判断の寄与が欠落している。
4. §5の5手順は依存fileの列挙には有効だが、§3.5が挙げる「REDが狙った理由で失敗したか」の
   確認、Human承認、上流authority、完了時の反証成立を検査しない。§1の事象全体を事前検出する
   対策としては不足する。

【判断】上記は報告された実測・原因・対策の十分性とrepositoryの実状態が競合するため、
`work-review-protocol.md` §4.7の`report_execution_mismatch`とする。Humanが5手順を恒久規約に
した裁定そのものは本レビューで変更しない。ただし、同裁定§2が根拠として転記した「16 file」、
「8回・4回」およびPilot単独主因の説明は、本修正が確認されるまで合格根拠に使えない。

## 2. Finding（§11）

### CA-REVIEW-001 blocking／completion／§11.1類型3

【実測】5手順の手順1〜5には、REDの失敗理由を実装前後で照合する操作がない。実際にgroup Aの
完了レビューv1は、反証testがDigest不一致という別理由で失敗したため、狙ったNaN受理欠陥を
検査できていない`F-CG-COMP-001`を記録した。5手順を実行しても、この別理由失敗は判定対象に
ならない。

【記録】group E範囲レビューの`SR-EG-SCOPE-001`〜`004`は、上流authority、Human承認順序、
拒否前副作用を合格させる受入条件、変更可能path・commit境界の4類型だった。5手順は
authorityの正しさとHuman承認順序を検査項目にしていない。group B完了レビューの`F-C1`も、
依存fileの列挙ではなく、Git非表示指定と別repositoryによる完了関門の偽陰性だった。

【判断】依存fileの列挙が合格すれば事象全体を予防できるように見える一方、実際には既知の
誤った合格を残せる。機械反証が記録済みの§11.1類型3に該当し、原因分析と対策の合格を止める
blockingとする。必要な修正は、5手順が検出できる事象と検出できない事象を分け、後者を
「全12件を事前検出できる対策」と扱わないことである。実装方式や将来設計は指定しない。

### CA-REVIEW-002 non-blocking／completion／§11.1閉じた4類型の列挙外

【実測】scope v1後の改訂commitは、group Eが`4b52776`・`8d2f3a4`の2件、group Aが
`35d2fe6`の1件、group Bが`4fda1a6`・`6ce4d03`の2件、group Cが`72b8389`・`c1edf4f`の
2件で、計7件だった。一方、範囲レビューの指摘はgroup E 4件、A 1件、B 0件、C 3件
（blocking 2件とnon-blocking 1件）で計8件だった。

【実測】scope後の停止点は、group A完了レビューv1、group B scope v2、group B完了レビューv1、
group CのRED後の所在判明を含めれば4地点と読める。しかしこれは完了レビューを含み、
「実装中の停止4回」ではない。group B scope v2が列挙した2事項、同完了レビューの2 blocking、
group Cの1事項を事象数として数えれば5件である。さらにgroup Cの停止は対象record以外の
独立した停止recordまたはscope v4がcommit `4c8d7bc`時点に存在しない。

【判断】8と4の数値に対応し得る集合はあるが、§1の名称と表の単位では一意に再現できない。
誤った合格を直接作る指摘ではないためnon-blockingとするが、record上は「scope改訂commit」、
「範囲レビュー指摘」、「scope後の停止地点」、「停止時の指摘件数」を混ぜずに直す必要がある。

### CA-REVIEW-003 non-blocking／completion／§11.1閉じた4類型の列挙外

【実測】§2.1の先頭40 moduleのscriptは終了コード0で`32`を出し、32／40を再現した。
同節記載の次のgrepも終了コード0だったが、出力は16ではなく35 test fileだった。

```text
grep -rln "sha256(.*read_bytes\|_sha256(" tests
```

【判断】35件にはfixture用Digest計算なども含まれるため、35件すべてが固定pin testだとは
判定しない。しかし「assertとpin表を持つもの」を16件へ絞る機械条件、対象一覧、実行出力が
無く、独立再現不能である。16 fileという実測はrecordの誤りとして訂正または再現条件の追加が
必要である。Digest密度32／40の主張は一致する。

### CA-REVIEW-004 non-blocking／completion／§11.1閉じた4類型の列挙外

【実測】上流group C判定のF-C5は対象を`tools/development/todo_update_path.py`と記した。
しかし同moduleは`run_two_phase_update()`から
`todo_record_generation.build_todo_candidate()`を呼ぶだけで、CRLFをLFへ変える実処理は
`tools/development/todo_record_generation.py`の`build_todo_candidate()`にある。

【実測】group B範囲レビューv1は`pytest_summary.py`の実行時結線先として`conftest.py`を
発見したが、「変更を必須にする固定値または指紋pinは見つからなかった」とし、変更が必要なら
実装中に停止する判断をした。その後のscope v2は、収集errorを実運用で数えるには
`conftest.py`へのhook追加が必要だったと記録した。

【判断】PilotがFindingのmodule名を検証せず信じたことは原因である。同時に、F-C5の対象欄の
誤帰属とgroup B範囲レビューの結線判断も、同じ手戻りへ実際に寄与した。group A・Bの上流Findingが
直接欠陥moduleだけを対象欄に置いたことはscope一覧として十分ではなかったが、Finding record自体は
実装scopeを網羅すると宣言した文書ではない。したがって、上流記録だけを主因とも、Pilotだけを
主因とも判定できない。§3・§4はこの共同寄与を欠いている。

## 3. 6観点の逐一照合

### 3.1 §1の件数

【実測】scope commit列は次のとおりで、初版4件と改訂7件を確認した。

| group | scope commit列 | 初版後の改訂 |
| --- | --- | ---: |
| E | `2c970d9` → `4b52776` → `8d2f3a4` | 2 |
| A | `3594172` → `35d2fe6` | 1 |
| B | `c5cd440` → `4fda1a6` → `6ce4d03` | 2 |
| C | `1831450` → `72b8389` → `c1edf4f` | 2 |

【判断】「8」は範囲レビュー指摘数としては再現するが、scope改訂回数としては7である。
「4」はscope後の停止地点としては読み取れるが、実装中だけの回数ではない。観点1は不一致である。

### 3.2 §2.1のDigest実測

【実測】対象record記載scriptの独立再実行は32／40で一致した。各40 moduleのpath、現在Digest、
検索hit数も機械出力で確認した。commit `5a67f5a..4c8d7bc`に`tests/`、`tools/`、`config/`の
変更は無いため、対象時点と同じ入力である。

【実測】test file数は、記載grepの出力35件で不一致だった。16件の選別条件が無いため再現不能。
観点2は一部一致、一部記録誤りである。

### 3.3 §2.2のCRLF処理箇所

【実測】`build_todo_candidate()`は`Path.read_text(encoding="utf-8")`で読み、Pythonの改行変換後の
文字列へ`splitlines(keepends=True)`を行い、最後にUTF-8 bytesへ戻す。CRLF消失の実処理箇所は
`tools/development/todo_record_generation.py`である。`todo_update_path.py`は同関数を呼び、
返された候補bytesを書く統括側である。

【判断】§2.2の所在特定は正しい。上流F-C5の対象欄は実処理の所在としては誤っている。

### 3.4 §3の原因列挙

【判断】Pilotの5原因は、各事象への寄与としては成立する。しかし、group Eの4つの範囲指摘の
原因、上流F-C5の誤った対象欄、group B範囲レビューの結線判断が欠落する。また原因5に対応する
確認が§5の対策に無い。原因列挙は不完全である。

### 3.5 §4の設計要因との切り分け

【記録】共通正本の指紋pinと契約recordによる固定自体は、Human承認境界を守る既存の意図された
設計である。今回のEvidenceから設計欠陥とは判定しない。

【判断】ただし「設計欠陥でない」と「Pilot要因が主因」は別の主張である。後者は上流記録と
Reviewer判断の寄与を除外した比較になっており、現Evidenceでは主因順位を確定できない。
妥当なのは「意図された依存網を事前走査しなかったPilot手順、上流対象欄の誤帰属、範囲レビューの
結線判断が共同で寄与した」までである。観点5は一部妥当、主因の単独帰属は要修正とする。

### 3.6 §5の5手順による事前検出

【実測】各scope初版前のcommit objectを直接読み、次を再現した。

| 対象 | 機械検証 | 結果 |
| --- | --- | --- |
| group A pin file | base `17c2002`の`tools/common/digests.py`と`tools/common/paths.py`のSHA-256を`records tests config`へ`git grep` | 両方とも`tests/test_common_module_pins.py`を検出。手順3で事前検出可能 |
| group B `conftest.py` | base `271826a`で`pytest_summary`のimportとpytest hookを`git grep` | `conftest.py`のimport、`pytest_runtest_logreport`、`pytest_sessionfinish`を検出。手順4で接続点を事前列挙可能 |
| group B契約pin | base `271826a`の`tests/test_declaration_red_map_check.py`のSHA-256を`records tests config`へ`git grep` | Work 5B契約v1・v2の`fixed_tests_checker` pinを検出。手順2で対象testを列挙後、手順3で事前検出可能 |

【判断】指定されたgroup A・Bの3件には5手順が有効である。一方、REDの失敗理由、上流authority、
Human承認順序、完了時の偽陰性は5手順の検査対象外であり、§1の事象すべてを事前検出できない。
観点6は一部合格、対策全体は不足とする。

## 4. 全Test、変更範囲、Human境界

【実測】元repositoryを変更しないようcommit `4c8d7bc`を`/private/tmp`へlocal cloneし、公式runnerを
単独実行した。終了コード1、`1470 passed / 12 failed / total 1482`、receipt SHA-256は
`391ae11ed7f9f9dc9ea7a715cc96957c469db4441a5da1d52ebf412a1dc5b6a4`だった。
12失敗は全件、group CのRED commit `431dd7b`が追加した未実装testであり、今回の対象recordが
code・testを壊した結果ではない。現在地が意図されたREDであることと、本原因分析の判定を分ける。

【実測】対象commit `4c8d7bc`は対象record 1件だけ、関連commit `5a67f5a`はHuman裁定record 1件だけを
追加していた。レビュー開始時の元repositoryはcleanだった。

【判断】本レビューでは対象record、Human裁定、code、test、既存record、TODO、checklistを変更しない。
Humanの恒久規約化裁定、実装方式、将来設計も変更・提案しない。本判定record 1件だけを新規作成し、
単独commitする。

## 5. 次

次：Pilotが、件数の単位、16 test fileの再現条件、上流Finding・Reviewer判断の寄与、5手順の
検出限界を対象原因分析の後継recordで訂正し、Humanが恒久規約の根拠更新要否を判断する。
