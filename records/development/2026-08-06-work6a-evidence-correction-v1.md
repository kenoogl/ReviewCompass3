# Work 6A Evidence 訂正記録 v1

- 訂正の根拠：`DEC-WORK6A-PROJECTION-NON-AUTHORITY-SCOPE-001` §2.3
  （`records/development/2026-08-06-work6a-non-authority-input-scope-decision-v1.md`、
  SHA-256 `2991aed38dd7e6f294774baa0ff98d664168bd8f2fffdc3337e7228938109af8`）
- 訂正対象1：`records/development/2026-08-06-work6a-projection-negative-red-evidence-v1.md`
  （SHA-256 `8dcff9e7f08a2098c6be6175cd940291f8f93a99903691dd0b94542671896d20`）の §8-2
- 訂正対象2：`records/development/2026-08-06-work6a-projection-negative-green-evidence-v1.md`
  （SHA-256 `cc52783bc898a62e96a52e6b5d3df548e5572818ea2e37d4b5b43d3e5898638c`）の
  定数名・関数名・診断文言・行番号
- 実行環境：Python 3.9.6、pytest 8.4.2、fallback `false`

## 0. この記録の位置づけ

**旧記録をin-placeで書き換えていない。** 訂正内容を本記録にnew-onlyで固定し、
旧記録は当時の状態の記録として履歴に残す。承認Decision §2.3が定めた扱いである。

訂正は2件で、どちらも**結論を変えない**。訂正1は根拠として挙げたtest名の誤りであり、
訂正2は改名による記述の陳腐化である。

## 1. 訂正1：RED Evidence §8-2 が挙げたtest名の誤り

### 1.1 旧記述

RED Evidence §8-2（当該fileの196-201行）は次のように書いている。

> 2. 「手編集可能なsource」の判定を拡張子（`.md`）や`docs/`配下といった一般規則にすると、
>    Plan authority自身の`docs/current/reviewcompass3-plan-current.md`が拒否される。
>    これは`projection-inputs.json`の`fixed_inputs`第1要素であり、
>    `test_projection_renders_fixed_short_and_detailed_text`をはじめ複数の既存Testを壊す。

### 1.2 誤り

`test_projection_renders_fixed_short_and_detailed_text`は**壊れない**。
このtestは`project_current_work()`を呼ばないため、`project_current_work()`内の判定を
どう変えても影響を受けない。

### 1.3 自分で確認した方法と結果

**確認A：当該testのコードを読んだ。**
`tests/test_session_log_bootstrap.py`の206-221行にある同testの本体は次の形である。

```python
def test_projection_renders_fixed_short_and_detailed_text():
    bootstrap = _bootstrap()
    projection = _json(FIXTURE_ROOT / "expected" / "projection.json")

    short = bootstrap.render_current_work(projection, mode="short")
    detailed = bootstrap.render_current_work(projection, mode="detailed", ...)
```

`projection`は固定fixture`expected/projection.json`をそのまま読み込んだ値であり、
`project_current_work()`は一度も呼ばれていない。呼ばれるのは`render_current_work()`だけである。

**確認B：`grep`で呼び出しを機械的に確認した。**
`grep -n "project_current_work\|render_current_work" tests/test_session_log_bootstrap.py`
の結果、`project_current_work`の呼び出しは183行、184行、229行、255行にあり、
同testの本体（206-221行）には1件も無い。

**確認C：素朴な一般化を実行時にだけ差し込んで実測した。**
scratchpad配下にpytest pluginを1つ置き、`pytest_configure`で
`tools.development.session_log_bootstrap._non_authority_declared_inputs`を
「`identity`が`.md`で終わる、または`docs/`で始まれば拒否する」素朴版へ差し替え、
`PYTHONPATH`にscratchpadを追加して
`.venv/bin/python3 -m pytest -q -p <plugin> tests/`を実行した。
repository内のfileは1件も変更しておらず、実行後の`git status --porcelain`も変化しなかった。

結果は`7 failed, 1010 passed`で、
`test_projection_renders_fixed_short_and_detailed_text`は**passedの側**にあった。

### 1.4 実際に壊れる既存test 6件（確認Cの実測）

| # | test |
| --- | --- |
| 1 | `tests/test_session_bootstrap_e2e.py::test_captures_session_lifecycle_and_renders_current_work_e2e` |
| 2 | `tests/test_session_bootstrap_e2e.py::test_display_failure_does_not_discard_valid_capture_or_authority` |
| 3 | `tests/test_session_log_bootstrap.py::test_projection_reduces_major_state_events_deterministically` |
| 4 | `tests/test_session_log_bootstrap.py::test_projection_reports_conflicting_active_work_as_inconsistent` |
| 5 | `tests/test_session_log_completed_next.py::test_work_completed_replaces_started_next_with_completion_next` |
| 6 | `tests/test_session_log_completed_next.py::test_work_completed_without_next_is_incomplete` |

7件目の失敗は
`tests/test_work6a_current_work_projection_negative.py::test_plan_authority_markdown_is_still_accepted`
で、これは既存testではなくRED commit `a2a90a7`で追加した境界例である。
境界例が意図どおり一般化を捕まえることの確認にもなっている。

6件に共通するのは、`project_current_work()`を通し、かつ固定入力に
`docs/current/reviewcompass3-plan-current.md`を含むことである。1と2は
`run_session_bootstrap()`経由で`projection-inputs.json`を渡す。3と4は
`project_current_work()`を直接呼ぶ。5と6は`tests/test_session_log_completed_next.py`の
`_inputs()`が同じPlan pathを固定入力に持つ。いずれも`diagnostics`の完全一致または
`status == "complete"`を要求するため、`missing`が1件増えると落ちる。

実測した失敗内容の一例（6番）は次である。

```text
{'missing': ['fixed input is declared not a current work authority:
  docs/current/reviewcompass3-plan-current.md', 'work_completed.payload.next']}
!= {'missing': ['work_completed.payload.next']}
```

一方、`tests/test_session_log_bootstrap.py::test_projection_reports_missing_authority_without_guessing`
は`project_current_work()`を通るが、使うfixture`projection-incomplete-inputs.json`の
`fixed_inputs`が空のため`.md` identityを含まず、壊れない。実測でもpassedであった。

### 1.5 結論は変わらない

「Plan authority自身が拒否されると既存Testが壊れるので、拒否対象はidentityの限定列挙に
しなければならない」というRED Evidence §8-2の結論は**そのまま有効**である。
誤っていたのは、その根拠として挙げた具体的なtest名だけである。

## 2. 訂正2：GREEN Evidence v1 の名前と行番号の陳腐化

`DEC-WORK6A-PROJECTION-NON-AUTHORITY-SCOPE-001` §2.2による改名の結果、
GREEN Evidence v1が記述する次の項目は現行実装と一致しなくなった。

| 種別 | GREEN Evidence v1 の記述 | 現行実装 |
| --- | --- | --- |
| 定数名 | `_HAND_EDITABLE_HANDOFF_IDENTITIES`（523行、1件） | `_NON_AUTHORITY_FIXED_INPUT_IDENTITIES`（529-534行、4件） |
| 関数名 | `_hand_editable_authority_inputs`（587-599行） | `_non_authority_declared_inputs`（598-614行） |
| 診断文言 | `hand-editable handoff is not a current work authority: <identity>` | `fixed input is declared not a current work authority: <identity>` |
| 呼び出し行 | 744行 | 759行 |
| `project_current_work` | 647-784行 | 662-799行 |
| 合流位置 | 742-748行 | 757-763行 |
| `_render_diagnostic` / `render_current_work` | 787-801行 / 804-859行 | 802-816行 / 819-874行 |
| 実装digest | `125b4e18145b5fa2f41ecb8208a018b9bdb706dacb8278dda2d2fc23c58abbe1` | `b97bd5eec6f6ae4fedd7a719089a8af0f642ddfb59e6ee4e29f851993db02a97` |

**GREEN Evidence v1は、改名前の状態を記録した文書として引き続き有効である。**
当時の実装digest`125b4e18…`に対する記録であり、そのdigestの実装においては記述は正しい。

現行の名前、文言、行番号を参照する場合は、本訂正記録と
`records/development/2026-08-06-work6a-non-authority-input-green-evidence-v1.md`
（拡大分のGREEN Evidence）を見ること。

なおGREEN Evidence v1が記述する規則1、規則3、規則4、規則5の内容と、
§3の限定2（`freshness`の拘束はキー欠落と`stale`の2つだけ）は、今回の改名の影響を
受けておらず、そのまま有効である。§3の限定1（拒否対象1件）だけが
`DEC-WORK6A-PROJECTION-NON-AUTHORITY-SCOPE-001`により置換された。

## 3. 誤りが下流に与えた影響の評価

### 3.1 `DEC-WORK6A-PROJECTION-GREEN-SCOPE-001` への影響：**文言上なし**

同Decision（`records/development/2026-08-06-work6a-projection-green-scope-decision-v1.md`）は
「RED Evidence §8の既知制約に基づき」（38行目）として§8-2を根拠に引用しているが、
その「限定1」の本文は次であり、**test名を1件も挙げていない**。

> 拡張子`.md`や`docs/`配下といった一般規則にすると、Plan authority自身の
> `docs/current/reviewcompass3-plan-current.md`が拒否され、既存Testが壊れる。

「既存Testが壊れる」という記述は実測（既存6件が壊れる）と一致しており、
訂正1による文言の変更を要しない。したがって同Decisionの再発行や訂正は不要である。

### 3.2 判断への影響：**なし**

誤っていたのは根拠として例示したtest名であり、「Plan authorityを拒否すると既存Testが
壊れる」という事実そのものは実測で確認されている。壊れるtestは1件ではなく6件であり、
影響はむしろ大きい方向であった。したがって「拒否対象をidentityの限定列挙にする」という
Humanの承認判断（`DEC-WORK6A-PROJECTION-GREEN-SCOPE-001`の限定1、および
`DEC-WORK6A-PROJECTION-NON-AUTHORITY-SCOPE-001` §2.1の4件限定列挙）は、
訂正後も同じ結論になる。

### 3.3 実装への影響：**なし**

実装は当初から拡張子や配置場所による一般規則を採らず、identityの完全一致だけで
判定していた。誤ったtest名が実装の形を変えたことはない。

### 3.4 その他の記録への影響

- `records/development/2026-08-06-work6a-negative-path-test-inventory-v1.json`：
  §8-2を参照していないため影響なし。
- `records/development/2026-08-06-work6a-projection-negative-green-evidence-v1.md`：
  §2の規則5でRED Evidence §8-3を、§3でRED Evidence §8-1を参照しているが、
  いずれも訂正1の対象（§8-2）ではない。§8-1と§8-3の記述に誤りは見つかっていない。

## 4. 旧記録を削除・書換えしていないこと

| 検証 | 結果 |
| --- | --- |
| `records/development/2026-08-06-work6a-projection-negative-red-evidence-v1.md` のSHA-256 | `8dcff9e7f08a2098c6be6175cd940291f8f93a99903691dd0b94542671896d20`。作成時の値と一致（未変更） |
| `records/development/2026-08-06-work6a-projection-negative-green-evidence-v1.md` のSHA-256 | `cc52783bc898a62e96a52e6b5d3df548e5572818ea2e37d4b5b43d3e5898638c`。作成時の値と一致（未変更） |
| `records/development/2026-08-06-work6a-negative-path-test-inventory-v1.json` のSHA-256 | `51674c143858b37608c7914c5bc2a8973be8221e2d5bde9707d89d082f995a16`。未変更 |
| `git status --porcelain` の`records/`配下 | 変更（`M`）は0件。未追跡は今回new-onlyで作成した記録のみ |

削除、書換え、無効化、stale化のいずれも行っていない。旧記録は当時の状態の記録として
そのまま残り、本記録がその上に訂正を重ねる形である。commit、push、外部送信は
行っていない。
