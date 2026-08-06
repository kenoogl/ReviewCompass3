# Work 6A 非authority入力の拒否範囲拡大 GREEN Evidence v1

- 承認Decision：`DEC-WORK6A-PROJECTION-NON-AUTHORITY-SCOPE-001`
  （`records/development/2026-08-06-work6a-non-authority-input-scope-decision-v1.md`）
- 部分supersede対象：`DEC-WORK6A-PROJECTION-GREEN-SCOPE-001`の「限定1」
  （`records/development/2026-08-06-work6a-projection-green-scope-decision-v1.md`）
- 上位Decision：`DEC-WORK5A-PROJECTION-ROUTING-001`
  （`records/development/2026-08-06-work5a-current-work-projection-routing-decision-v1.md`）
- 先行Evidence：RED
  `records/development/2026-08-06-work6a-projection-negative-red-evidence-v1.md`、
  GREEN v1
  `records/development/2026-08-06-work6a-projection-negative-green-evidence-v1.md`
- 実行環境：Python 3.9.6、pytest 8.4.2、公式venv runner、fallback `false`
- 実行時刻：2026-08-06T09:37:53+09:00（公式全Test receiptの`recorded_at`）
- RED基準commit：`a2a90a7`（`Fix non-authority input rejection as red tests`）

## 0. 何を行ったのか（範囲の明示）

**同じTestを弱めずGREENにした。** RED commit `a2a90a7`が固定したtest 3件と境界例1件は
1文字も変更しておらず、実装側だけを直して対象file 10件すべてを通した。
先行GREEN v1で通した既存6件も無変更のまま通っている。

**振る舞いの拡大は、拒否対象identityを1件から4件の限定列挙へ広げたことだけ**である。
判定は完全一致のみで、拡張子や配置場所による一般規則へは広げていない。

**行っていないこと**は次である。

- 新schema、新state、新authority、新module、新設定fileの追加。追加したのは既存module
  `tools/development/session_log_bootstrap.py`内のprivate定数の要素3件だけで、
  公開APIの形も返り値のキー構成も変えていない。関数は改名しただけで新設していない。
- 入力側に「これはauthorityである」と宣言させる方式。承認Decision §3の非承認範囲である。
- Current Work Projectionの正式record写像、正式Portfolio／Work Item／Workflow state。
- checklist `CL-6A-08`への完了印。承認Decision §3により別途Human判断とする。

変更fileは`tools/development/session_log_bootstrap.py`の1件だけである
（`git diff --stat`：`1 file changed, 22 insertions(+), 7 deletions(-)`）。
`git diff --check`は合格した。`git status --porcelain`は当該実装1件の変更のみを示す。

## 1. 固定入力（機械計算したSHA-256）

`shasum -a 256`で計算した。実装fileは**変更後**の値である。

| path | SHA-256 |
| --- | --- |
| `records/development/2026-08-06-work6a-non-authority-input-scope-decision-v1.md` | `2991aed38dd7e6f294774baa0ff98d664168bd8f2fffdc3337e7228938109af8` |
| `records/development/2026-08-06-work6a-projection-green-scope-decision-v1.md` | `20a21c56710c71b413215e12752f090674e9cad8035a2eee7b380a14098c19bb` |
| `records/development/2026-08-06-work5a-current-work-projection-routing-decision-v1.md` | `f084b471d3fe4ba40a9c6a7a5e3882fa78090da54c7e9b19b04547dde5307eda` |
| `records/development/2026-08-06-work6a-projection-negative-red-evidence-v1.md` | `8dcff9e7f08a2098c6be6175cd940291f8f93a99903691dd0b94542671896d20` |
| `records/development/2026-08-06-work6a-projection-negative-green-evidence-v1.md` | `cc52783bc898a62e96a52e6b5d3df548e5572818ea2e37d4b5b43d3e5898638c` |
| `records/development/2026-08-06-work6a-negative-path-test-inventory-v1.json` | `51674c143858b37608c7914c5bc2a8973be8221e2d5bde9707d89d082f995a16` |
| `tests/test_work6a_current_work_projection_negative.py`（`a2a90a7`時点、以後未変更） | `a7b6d53ee4d6e6af38061613241bfb10417b5dec870cbd33cf498a38f265a8dd` |
| `tools/development/session_log_bootstrap.py`（変更後） | `b97bd5eec6f6ae4fedd7a719089a8af0f642ddfb59e6ee4e29f851993db02a97` |
| `docs/development/prompts/todo-handoff-update.md` | `eff64878479ce82a48f8e5b4160dd7913364268c9e94d1a6f0a63087e7fb0f4d` |
| `docs/development/templates/TODO_NEXT_SESSION.template.md` | `9bfba3daca9c12ea4854806c9ec0f763d45d68585bbcf653967c5725ebbde4b1` |
| `docs/development/2026-08-03-initial-development-checklist.md` | `1bd743b0fd110342900996199b2a81eaf2b42440f28318f931e43a78b039a550` |
| `docs/current/reviewcompass3-plan-current.md` | `1a73597605eafb65a2259ccf19431e3aba041564d03fdb279150042a9bd0962f` |

実装digestはGREEN v1時点の`125b4e18…`から`b97bd5ee…`へ変わっている。
Test fileはRED Evidence §1記載の`25a76b7b…`から`a7b6d53e…`へ変わっているが、これは
RED commit `a2a90a7`でtestを**追加**したためであり、既存6件の本文は変更していない
（§5参照）。承認Decision §5記載の固定Evidence 5件はすべて記載値と一致した。

## 2. 旧名→新名の対応と診断文言

行番号は変更後の`tools/development/session_log_bootstrap.py`のものである。

| 種別 | 旧（GREEN v1） | 新（本Evidence） | 位置 |
| --- | --- | --- | --- |
| 定数 | `_HAND_EDITABLE_HANDOFF_IDENTITIES`（1件） | `_NON_AUTHORITY_FIXED_INPUT_IDENTITIES`（4件） | 529-534行 |
| 関数 | `_hand_editable_authority_inputs` | `_non_authority_declared_inputs` | 598-614行 |
| 呼び出し | `missing.extend(_hand_editable_authority_inputs(fixed_inputs))` | `missing.extend(_non_authority_declared_inputs(fixed_inputs))` | 759行（1箇所） |

診断文言は次へ変えた。

- 旧：`hand-editable handoff is not a current work authority: <identity>`
- 新：`fixed input is declared not a current work authority: <identity>`

docstringも「手編集できる引き継ぎメモを…受け付けない」から
「上位文書がauthorityではないと宣言した成果物を、現在位置のauthorityにしない」へ改め、
判定基準が手編集可能性ではなくauthority宣言であることを明記した。
定数の直上には各identityの非authority宣言の出所をcommentで残している。

`status`の優先順位（競合→`inconsistent`、欠落→`incomplete`、どちらも無ければ`complete`）と、
`project_current_work()`（662-799行）内での合流位置は既存のままである。

## 3. 拡大した4件の非authority宣言（該当文書を開いて確認済み）

承認Decision §2.1の表を根拠に、4件すべて該当fileを実際に開き、引用が正しいことを
確認した。行番号は上表のdigest時点のものである。

| identity | 宣言している文書 | 該当箇所 |
| --- | --- | --- |
| `TODO_NEXT_SESSION.md` | `docs/development/prompts/todo-handoff-update.md` 6行目 | 「TODO自体をWorkflow stateまたは完了Evidenceの正本にしない。」 |
| `STATUS.md` | `docs/current/reviewcompass3-plan-current.md` 993行目 | 「手編集する`STATUS.md`、製品schema、WebUI、常駐serviceを作らず」 |
| `STATUS.md` | `docs/development/2026-08-03-initial-development-checklist.md` 201行目 | 「手編集する`STATUS.md`、第二の状態台帳、WebUI、常駐serviceを作っていない。」 |
| `STATUS.md` | `docs/design/2026-08-03-current-work-projection-memo.md` 168行目 | 「手編集する`STATUS.md`を正本として作らない。」 |
| `docs/development/templates/TODO_NEXT_SESSION.template.md` | 同file 6行目（自己宣言） | 「本書は人向けの入口であり、Workflow state、完了判断、Evidenceの正本ではない。」 |
| `docs/development/2026-08-03-initial-development-checklist.md` | 同file 37行目（自己宣言） | 「checkboxは進行を見失わないための操作viewであり、完了のauthorityは各項目の固定Evidenceである。」 |

`STATUS.md`は承認Decisionが述べるとおり3箇所で名指しされており、3箇所すべてを確認した。
templateとchecklistは自file内の宣言であり、いずれも冒頭の位置づけ節にある。

なお`TODO_NEXT_SESSION.md`というfile名は、承認Decision §1が指摘するとおり
Current Planやchecklist本文には現れない。その非authority宣言は運用手順文書
`docs/development/prompts/todo-handoff-update.md`にある。

## 4. 過剰な一般化を防いだ根拠

### 実装側

`_non_authority_declared_inputs()`（598-614行）は`identity not in
_NON_AUTHORITY_FIXED_INPUT_IDENTITIES`の完全一致だけを見る。拡張子判定も
`docs/`前方一致も存在しない。定数の実測値は次である。

```python
('TODO_NEXT_SESSION.md',
 'STATUS.md',
 'docs/development/templates/TODO_NEXT_SESSION.template.md',
 'docs/development/2026-08-03-initial-development-checklist.md')
```

### 境界例testの実測

`test_plan_authority_markdown_is_still_accepted`（test file 155-176行）は、
`projection-inputs.json`の固定入力に`docs/current/reviewcompass3-plan-current.md`が
含まれていることを確認したうえで、`status == "complete"`かつ当該identityが`missing`に
現れないことを要求する。現行実装での実測は次のとおりで、testは通る。

- `diagnostics["status"]` = `complete`
- `diagnostics["missing"]` = `[]`

拡張子`.md`と`docs/`前方一致の両方を含む識別子でありながら拒否されていない。

### 素朴な一般化が実際に何を壊すかの実測

一般規則へ広げた場合に何が壊れるかを、repository内のfileを変更せずに実測した。
確認方法は次である。scratchpad配下にpytest pluginを1つ置き、`pytest_configure`で
`_non_authority_declared_inputs`を「`identity`が`.md`で終わる、または`docs/`で始まれば
拒否する」素朴版へ実行時だけ差し替え、`.venv/bin/python3 -m pytest -q -p <plugin> tests/`
を実行した（`PYTHONPATH`にscratchpadを追加。repository内のfileは無変更で、
実行後の`git status --porcelain`も変化しなかった）。

結果は`7 failed, 1010 passed`で、内訳は既存test 6件と境界例test 1件である。

| 壊れたtest | 種別 |
| --- | --- |
| `tests/test_session_bootstrap_e2e.py::test_captures_session_lifecycle_and_renders_current_work_e2e` | 既存 |
| `tests/test_session_bootstrap_e2e.py::test_display_failure_does_not_discard_valid_capture_or_authority` | 既存 |
| `tests/test_session_log_bootstrap.py::test_projection_reduces_major_state_events_deterministically` | 既存 |
| `tests/test_session_log_bootstrap.py::test_projection_reports_conflicting_active_work_as_inconsistent` | 既存 |
| `tests/test_session_log_completed_next.py::test_work_completed_replaces_started_next_with_completion_next` | 既存 |
| `tests/test_session_log_completed_next.py::test_work_completed_without_next_is_incomplete` | 既存 |
| `tests/test_work6a_current_work_projection_negative.py::test_plan_authority_markdown_is_still_accepted` | 今回の境界例 |

境界例testが7件目として確実に落ちることから、この境界例が回帰防止として機能している
ことを確認した。既存6件の内訳はRED Evidenceの誤りの訂正でもあり、詳細は
`records/development/2026-08-06-work6a-evidence-correction-v1.md`にある。

## 5. RED→GREENの対比

RED commit `a2a90a7`時点の失敗を、同じ手法（scratchpad pluginで
`_non_authority_declared_inputs`を改名前の1件版へ実行時だけ戻す）で再現して実測した。
結果は`3 failed, 7 passed`である。

| # | test関数（行） | RED時の失敗 | GREEN後の`missing`（実測） |
| --- | --- | --- | --- |
| 1 | `test_status_document_is_not_accepted_as_authority`（105-118行、assertは115行） | `AssertionError: assert 'complete' != 'complete'` | `['fixed input is declared not a current work authority: STATUS.md']` |
| 2 | `test_todo_handoff_template_is_not_accepted_as_authority`（121-135行、assertは132行） | `AssertionError: assert 'complete' != 'complete'` | `['fixed input is declared not a current work authority: docs/development/templates/TODO_NEXT_SESSION.template.md']` |
| 3 | `test_initial_development_checklist_is_not_accepted_as_authority`（138-152行、assertは149行） | `AssertionError: assert 'complete' != 'complete'` | `['fixed input is declared not a current work authority: docs/development/2026-08-03-initial-development-checklist.md']` |

3件とも`status`は`incomplete`、`next`は`Repair missing projection inputs`になる。
既存の`test_hand_editable_handoff_is_not_accepted_as_authority`が扱う
`TODO_NEXT_SESSION.md`も、文言だけが新しくなり
`['fixed input is declared not a current work authority: TODO_NEXT_SESSION.md']`で
`incomplete`になる。同testは`"TODO_NEXT_SESSION.md" in item`という部分一致で判定するため、
文言変更後も通る。

境界例`test_plan_authority_markdown_is_still_accepted`はRED時点でも成功する
回帰防止testであり、RED再現でも7 passedの側に含まれていた。

## 6. Testの実測

いずれも自分で実行して確認した。

| 対象 | command | 結果 |
| --- | --- | --- |
| 対象Test | `.venv/bin/python3 -m pytest -q tests/test_work6a_current_work_projection_negative.py` | **`10 passed in 0.02s`** |
| 隣接する既存Test | `.venv/bin/python3 -m pytest -q tests/test_session_log_bootstrap.py tests/test_session_bootstrap_e2e.py tests/test_session_log_completed_next.py` | **`13 passed in 0.04s`** |
| 公式全Test | `.venv/bin/python3 -m tools.development.policy_test_runner --suite full --receipt <scratchpad>` | **`1017 passed`** |

公式全Test receiptの内訳は次である。receiptはscratchpad配下だけに置き、
repositoryへは保存していない。

| 項目 | 実測値 |
| --- | --- |
| status | `passed`（exit code 0） |
| passed | 1017 |
| failed | 0 |
| errors | 0 |
| skipped | 0 |
| xfailed / xpassed | 0 / 0 |
| total | 1017 |
| command | `.venv/bin/python3 -m pytest -q` |
| python_version | 3.9.6 |
| pytest_version | 8.4.2 |
| fallback_used | `false` |
| config_digest | `890380460e063e508145450cf6e80865409d20035dfc2265b99c364f03b8b6ea` |
| source_state_digest | `9277a132308e19dfbc6e2254f9240c13e4f89142db4a9b64a10e07627e052e31` |
| recorded_at | `2026-08-06T09:37:53+09:00` |

GREEN v1時点の`1013 passed`（total 1013）に対し、RED commitでtestが4件増えてtotalが
1017になり、そのすべてがpassedである。`config_digest`は一連の作業を通じて同一で、
`source_state_digest`はGREEN v1の`df04ef63…`から`9277a132…`へ変わっている。

### 既存Testを弱めていないこと

| 検証 | 結果 |
| --- | --- |
| 変更fileの数 | `tools/development/session_log_bootstrap.py` 1件のみ |
| RED commit `a2a90a7`のtest差分 | 92 insertions、**0 deletions**（既存6件の本文は無変更） |
| GREEN実装時の`tests/`変更 | 0件（`git status --porcelain`に`tests/`配下は現れない） |
| fixture変更 | 0件 |
| skip／xfail／assertion緩和 | 0件 |

## 7. 変更していない範囲

- `tests/`配下すべて。今回のGREEN実装では1 byteも触っていない。
- `tests/fixtures/`配下すべて。
- `tools/`配下のうち`tools/development/session_log_bootstrap.py`以外すべて。
- 既存記録（`records/`配下の既存file）。上書き、削除、無効化、stale化はしていない。
  RED Evidenceの誤りは別記録`records/development/2026-08-06-work6a-evidence-correction-v1.md`
  で訂正し、旧記録はそのまま残している。
- Contract、Requirement、Plan、Policy、checklist、TODO、設定file。
- commit、push、tag、PR、CI、外部送信、LLM呼び出しは行っていない。

## 8. 残っている限界

1. **拒否対象は4件の限定列挙である。** 上位文書が名指ししていない他の手編集経路
   （別名のhandoff、session handoff record、任意の作業memo等）は、固定入力として
   渡されても拒否されない。拡大には上位文書の宣言を根拠にした別途Human判断が要る。
2. **判定は`identity`の完全一致であって、内容や宣言そのものを読んでいない。**
   当該fileを開いて「これは正本ではない」という宣言文を検出しているわけではないため、
   file名が変われば拒否は外れ、宣言が撤回されても拒否は残る。
   pathの表記ゆれ（先頭`./`、絶対path、大文字小文字差）も一致しない。
3. **入力側にauthorityを宣言させる方式は未実施である。** 承認Decision §3の非承認範囲で、
   新しい項目の追加を伴い、実測でも既存Test 6件が壊れる。
   `DEC-WORK5A-PROJECTION-ROUTING-001`の再開条件（正式record）に属する。
4. **Work 6Aの残り20項目は未着手である。** 対応inventory
   `records/development/2026-08-06-work6a-negative-path-test-inventory-v1.json`で
   `out_of_approved_scope`とした20項目には手を付けていない。
5. **Current Work Projectionの正式record写像は未着手である。**
   `DEC-WORK5A-PROJECTION-ROUTING-001`の再開条件が満たされるまでdeferredのままで、
   今回の診断は派生viewの健全性checkにとどまる。
6. GREEN v1 §7で挙げた限界のうち、`freshness`の`unknown`を拘束しないこと、
   固定入力のDigestと実file内容を突き合わせないこと、Digest競合時の`next`が
   `work_started`競合と同じ文言であることは、今回も解決していない。
