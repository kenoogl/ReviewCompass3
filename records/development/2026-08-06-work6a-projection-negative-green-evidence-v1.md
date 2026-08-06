# Work 6A Current Work Projection negative path GREEN Evidence v1

- 承認Decision：`DEC-WORK6A-PROJECTION-GREEN-SCOPE-001`
  （`records/development/2026-08-06-work6a-projection-green-scope-decision-v1.md`）
- 上位Decision：`DEC-WORK5A-PROJECTION-ROUTING-001`
  （`records/development/2026-08-06-work5a-current-work-projection-routing-decision-v1.md`）
- 対応RED Evidence：`records/development/2026-08-06-work6a-projection-negative-red-evidence-v1.md`
- 対応inventory：`records/development/2026-08-06-work6a-negative-path-test-inventory-v1.json`
- 実行環境：Python 3.9.6、pytest 8.4.2、公式venv runner、fallback `false`
- 実行時刻：2026-08-06T09:03:54+09:00（公式全Test receiptの`recorded_at`）
- 基準commit：`9a39365`（`Fix Work 6A projection negative paths as red tests`）

## 0. 何を行ったのか（範囲の明示）

**同じTestを弱めずGREENにした。** RED Evidenceが固定した6 testは1文字も変更しておらず、
実装側だけを直して6件すべてを通した。RED Evidence記載のtest file digest
`25a76b7ba39dc032c3e30204cf9d83377129d9b530ab4eeb90dd0f5a199ade0f`は現在も一致する。

**行っていないこと**は次である。

- Current Work Projectionの正式record写像。`DEC-WORK5A-PROJECTION-ROUTING-001`の
  再開条件が満たされるまでdeferredのままである。
- 新schema、新state、新authority、新module、新設定fileの追加。追加したのは
  既存module`tools/development/session_log_bootstrap.py`内のprivate helper 6個と
  private定数2個だけで、公開APIの形も返り値のキー構成も変えていない。
- 正式Portfolio／Work Item／Workflow stateの実装。
- Work 5AまたはWork 6Aの段完了。

変更ファイルは`tools/development/session_log_bootstrap.py`の1件だけである
（`git diff --stat`：`1 file changed, 95 insertions(+), 5 deletions(-)`）。
`git diff --stat HEAD -- tests/`は空で、`tests/`と`tests/fixtures/`は1文字も変更していない。
`git diff --check`は合格した。

## 1. 固定入力（機械計算したSHA-256）

`shasum -a 256`で計算した。実装fileは**変更後**の値である。

| path | SHA-256 |
| --- | --- |
| `records/development/2026-08-06-work6a-projection-green-scope-decision-v1.md` | `20a21c56710c71b413215e12752f090674e9cad8035a2eee7b380a14098c19bb` |
| `records/development/2026-08-06-work5a-current-work-projection-routing-decision-v1.md` | `f084b471d3fe4ba40a9c6a7a5e3882fa78090da54c7e9b19b04547dde5307eda` |
| `docs/design/2026-08-06-work5a-current-work-projection-routing-proposal.md` | `c061be7d5abd1f428497f59d2b4ccc352b699d657d038d11f1d359a76e587809` |
| `records/development/2026-08-06-work6a-projection-negative-red-evidence-v1.md` | `8dcff9e7f08a2098c6be6175cd940291f8f93a99903691dd0b94542671896d20` |
| `records/development/2026-08-06-work6a-negative-path-test-inventory-v1.json` | `51674c143858b37608c7914c5bc2a8973be8221e2d5bde9707d89d082f995a16` |
| `tools/development/session_log_bootstrap.py`（変更後） | `125b4e18145b5fa2f41ecb8208a018b9bdb706dacb8278dda2d2fc23c58abbe1` |
| `tests/test_work6a_current_work_projection_negative.py`（未変更） | `25a76b7ba39dc032c3e30204cf9d83377129d9b530ab4eeb90dd0f5a199ade0f` |
| `tests/fixtures/development/session-log-bootstrap/projection-inputs.json`（未変更） | `08d36c9db08ce8fd64c5810de45d71dedb3350e54aab35d14772d44f9666f936` |
| `tests/fixtures/development/session-log-bootstrap/projection-incomplete-inputs.json`（未変更） | `b0291bf318ae611a4ffbf360b737e43666a4cda17edc56acbb73b10336058eb5` |

RED Evidence §1の実装digest`55a7c38b…`から`125b4e18…`へ変わっている。
それ以外の8件はRED Evidence／GREEN範囲Decision記載値と一致する。

## 2. 規則1〜5の実装箇所と、固定した負例

行番号は変更後の`tools/development/session_log_bootstrap.py`のものである。

共通ヘルパとして`_is_fixed_digest()`（526-533行、64桁かつ16進を判定）と
`_fixed_input_identity()`（536-544行）を新設した。既存`_projection_missing_inputs()`
（547-568行）の長さ判定2箇所を`_is_fixed_digest()`へ置換したのが削除5行の主たる内訳で、
判定の意味は「64桁」から「64桁かつ16進」へ厳格化する方向にのみ変わっている。

### 規則1：正式入力欠落

- 実装：`_incomplete_fixed_inputs()`（571-584行）。`identity`と64桁16進`digest`が揃わない
  固定入力を`missing`へ挙げる。文言は`fixed input lacks identity and Digest: <identity>`、
  identityが取れない要素は`(identity absent)`。
- 対象test：`test_fixed_input_without_valid_digest_is_not_ignored`
- RED時：`assert diagnostics["status"] != "complete"` が
  `AssertionError: assert 'complete' != 'complete'`
- GREEN後（実測）：`status` = `incomplete`、
  `missing` = `['fixed input lacks identity and Digest: records/task-contract/first-review-task-contract.json']`
  （末尾の文字列はtestが合成した`identity`の値であって、実在するfileへの参照ではない）

### 規則2：第二正本化

- 実装：`_hand_editable_authority_inputs()`（587-599行）と定数
  `_HAND_EDITABLE_HANDOFF_IDENTITIES = ("TODO_NEXT_SESSION.md",)`（523行）。
  完全一致の限定列挙1件のみ。文言は
  `hand-editable handoff is not a current work authority: <identity>`。
- 対象test：`test_hand_editable_handoff_is_not_accepted_as_authority`
- RED時：`AssertionError: assert 'complete' != 'complete'`
- GREEN後（実測）：`status` = `incomplete`、
  `missing` = `['hand-editable handoff is not a current work authority: TODO_NEXT_SESSION.md']`

### 規則3：欠測推測とstale

- 実装：`_freshness_missing()`（602-609行）。キー欠落と値`stale`のみ拘束する。
  文言は`freshness is absent and must not be guessed as current`と
  `freshness is stale and must be refreshed`。
- 対象test：`test_missing_freshness_is_not_guessed_as_current`、
  `test_stale_freshness_is_not_displayed_as_complete`
- RED時：どちらも`AssertionError: assert 'complete' != 'complete'`
- GREEN後（実測）：キー欠落は`status` = `incomplete`、
  `missing` = `['freshness is absent and must not be guessed as current']`、
  `projection["freshness"]` = `None`。
  `stale`は`status` = `incomplete`、
  `missing` = `['freshness is stale and must be refreshed']`、
  `projection["freshness"]` = `stale`（値は素通しのまま保存される）。

### 規則4：Digest競合

- 実装：`_fixed_input_digest_conflicts()`（612-630行）。同一`identity`に異なる`digest`が
  あれば`conflicts`へ`fixed input has conflicting Digests: <identity>`を挙げる。
- 対象test：`test_conflicting_digests_for_one_identity_are_inconsistent`
- RED時：`assert diagnostics["status"] == "inconsistent"` が
  `AssertionError: assert 'complete' == 'inconsistent'`
- GREEN後（実測）：`status` = `inconsistent`、
  `conflicts` = `['fixed input has conflicting Digests: docs/current/reviewcompass3-plan-current.md']`

### 規則5：表示の切替

- 実装：**`render_current_work()`（804-859行）と`_render_diagnostic()`（787-801行）は
  無変更である。** 既存の「`status`が`complete`でなければ診断表示へ切替える」分岐
  （現在の812行）をそのまま使い、`next`も既存ロジック（754-764行、うち762行が
  `next_action = "Repair missing projection inputs"`）で修復指示になる。
  RED Evidence §8-3が「診断表示へ切替えるだけでは足りず、`next`自体を差し替える実装が要る」
  と記録していた点は、規則3が`missing`を増やした結果`next_action`が
  `Repair missing projection inputs`へ変わることで満たされ、表示器の変更は不要だった。
- 対象test：`test_stale_input_text_does_not_assert_a_normal_next_action`
- RED時：`assert "STATUS:" in detailed`が失敗し、`freshness: stale`を添えたまま
  PLAN／CURRENT ACTIVITY／NEXTを断定表示していた。
- GREEN後（実測）：`detailed`と`short`はともに次を返す。

```text
ReviewCompass3 Current Work
STATUS: INCOMPLETE
missing:
  - freshness is stale and must be refreshed
next:
  - Repair missing projection inputs
```

`Implement Session Log Bootstrap mapping`はdetailedからもshortからも消えている。

### 統合点と優先順位

`project_current_work()`（647-784行）の合流は次（742-748行）で、`status`の優先順位
（競合→`inconsistent`、欠落→`incomplete`、どちらも無ければ`complete`）は既存のままである。

```python
missing = _projection_missing_inputs(fixed_inputs)
missing.extend(_incomplete_fixed_inputs(fixed_inputs))
missing.extend(_hand_editable_authority_inputs(fixed_inputs))
missing.extend(_freshness_missing(input_record))
if completion_next_missing:
    missing.append("work_completed.payload.next")
conflicts = _fixed_input_digest_conflicts(fixed_inputs)
```

## 3. Humanが個別に承認した2つの限定を守っていること

### 限定1：拒否対象は`TODO_NEXT_SESSION.md`の1件だけ

- 実装は523行の定数`_HAND_EDITABLE_HANDOFF_IDENTITIES = ("TODO_NEXT_SESSION.md",)`に対する
  完全一致（`identity not in ...`）だけを見る。拡張子判定も`docs/`前方一致も無い。
- 根拠（実測）：`tests/fixtures/development/session-log-bootstrap/projection-inputs.json`の
  `fixed_inputs`第1要素の`identity`は`docs/current/reviewcompass3-plan-current.md`である。
  この固定入力をそのまま与えたときの`diagnostics["status"]`は`complete`、`missing`は`[]`で、
  Plan authority自身は拒否されていない。

### 限定2：`freshness`の拘束はキー欠落と`stale`の2つだけ

- 実装は602-609行で`"freshness" not in input_record`と`== "stale"`のみを見る。
  それ以外の値は空listを返す。
- 根拠（実測）：`tests/fixtures/development/session-log-bootstrap/projection-incomplete-inputs.json`
  の`freshness`は`unknown`である。この固定入力を与えたときの`diagnostics`は

  ```python
  {'conflicts': [], 'missing': ['fixed Plan identity and Digest',
   'workflow event stream identity and Digest'], 'status': 'incomplete'}
  ```

  で、RED Evidence §8-1が壊れると指摘した
  `test_projection_reports_missing_authority_without_guessing`の完全一致assertionと
  同じ2要素のままである。`unknown`によるmissingは1件も増えていない。

## 4. 既存Testを弱めていないことの根拠

| 検証 | 結果 |
| --- | --- |
| `git diff --stat HEAD -- tests/` | 空（`tests/`と`tests/fixtures/`に変更0件） |
| `git status --porcelain` の`tests/`配下 | 変更・未追跡ともに0件 |
| `tests/test_work6a_current_work_projection_negative.py` のSHA-256 | `25a76b7ba39dc032c3e30204cf9d83377129d9b530ab4eeb90dd0f5a199ade0f`。RED Evidence §1記載値と一致 |
| 既存fixture 2件のSHA-256 | RED Evidence §1記載値と一致 |
| 変更ファイル数 | `tools/development/session_log_bootstrap.py` 1件のみ |

RED testのassertionを緩めた、skipした、xfailにした、fixtureを書き換えた、という操作は
一切していない。

## 5. Testの実測

いずれも自分で実行して確認した。

| 対象 | command | 結果 |
| --- | --- | --- |
| 今回のRED test | `.venv/bin/python3 -m pytest -q tests/test_work6a_current_work_projection_negative.py` | **`6 passed in 0.01s`** |
| 隣接する既存Test | `.venv/bin/python3 -m pytest -q tests/test_session_log_bootstrap.py tests/test_session_bootstrap_e2e.py tests/test_session_log_completed_next.py` | **`13 passed in 0.04s`** |
| 公式全Test | `.venv/bin/python3 -m tools.development.policy_test_runner --suite full --receipt <scratchpad>` | **`1013 passed`** |

公式全Test receiptの内訳は次である。receiptはscratchpad配下だけに置き、
repositoryへは保存していない。

| 項目 | 実測値 |
| --- | --- |
| status | `passed`（exit code 0） |
| passed | 1013 |
| failed | 0 |
| errors | 0 |
| skipped | 0 |
| xfailed / xpassed | 0 / 0 |
| total | 1013 |
| command | `.venv/bin/python3 -m pytest -q` |
| python_version | 3.9.6 |
| pytest_version | 8.4.2 |
| fallback_used | `false` |
| config_digest | `890380460e063e508145450cf6e80865409d20035dfc2265b99c364f03b8b6ea` |
| source_state_digest | `df04ef6357f7c42c412d2292f929777840adc67eac1d4899291657aa58656d60` |
| recorded_at | `2026-08-06T09:03:54+09:00` |

RED時点の`1007 passed / 6 failed`（total 1013）から、totalを変えずに6件が
failedからpassedへ移った。`config_digest`はRED時点と同一で、
`source_state_digest`は`bedd2cb0…`から`df04ef63…`へ変わっている。

## 6. 変更していない範囲

- `tests/`配下すべて（既存Test、今回のRED test、fixture）。
- `tools/`配下のうち`tools/development/session_log_bootstrap.py`以外すべて。
- 既存記録（`records/`配下の既存file）。上書き、削除、無効化、stale化はしていない。
- Contract、Requirement、Plan、Policy、checklist、TODO、設定file。
- commit、push、tag、PR、CI、外部送信、LLM呼び出しは行っていない。

## 7. 残っている限界（今回のGREENが解決していないこと）

1. 対応inventoryで`out_of_approved_scope`とした**Work 6Aの20項目は未着手**である。
   今回のGREENが対応するのは`CL-6A-08`と`PL-6A-09`の1対象だけで、Work 6Aの段は完了しない。
2. **Current Work Projectionの正式record写像はdeferredのまま**である。
   `DEC-WORK5A-PROJECTION-ROUTING-001`の再開条件（Stage／Work／Work Item identityと
   state owner、型付きrelation、dependency・cycle・termination等の正式record、
   Workflow規則）が満たされるまで再開しない。今回の診断はあくまで派生viewの健全性checkであり、
   状態正本ではない。
3. **手編集sourceの拒否は`TODO_NEXT_SESSION.md`の1件だけ**である。他の手編集経路
   （別名のhandoff、`docs/`配下の手書き文書、session handoff record等）はauthorityとして
   渡されても拒否されない。Human承認済みの限定であり、拡張には別途Human判断が要る。
4. **`freshness`の`unknown`など他の値は拘束していない**。拘束するのはキー欠落と`stale`の
   2つだけで、`unknown`を与えても`complete`になりうる。
5. **固定入力のDigestと実file内容の突き合わせは行っていない**。見ているのは記録された
   値どうしの整合（identityの有無、64桁16進の形、同一identity間の一致）だけで、
   `digest`が実際にそのfileのSHA-256かどうかは検証していない。したがって、
   形式が正しく内部矛盾もない偽のDigestは`complete`を通す。
6. **Digest競合時の`next`は`Resolve conflicting active work`**で、これは
   event側の`work_started`競合と同じ文言である。競合の種類（固定入力のDigest競合か、
   並行work_startedか）を`next`では区別していない。区別は`diagnostics["conflicts"]`の
   文言を読む必要がある。
