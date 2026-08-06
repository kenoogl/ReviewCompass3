# Work 6A `CL-6A-08` 項目完了 承認Decision v1

- Decision ID：`DEC-WORK6A-CL-6A-08-COMPLETION-001`
- decision maker：Human
- decided at：`2026-08-06T09:55:45+09:00`
- decision：`approved`
- decision class：`item_completion_decision`
- 上位Decision：`DEC-WORK6A-PROJECTION-NON-AUTHORITY-SCOPE-001`、
  `DEC-WORK6A-PROJECTION-GREEN-SCOPE-001`、`DEC-WORK5A-PROJECTION-ROUTING-001`

## 1. 承認対象

初期開発チェックリスト9節「Work 6A：初期sliceのnegative path」の項目
`CL-6A-08`にHumanが完了を承認した。

> Current Work Projectionの第二正本化、欠測推測、stale／競合の正常表示を検出する。

Claudeが完了可否を提示し、Humanは「1は終了でよい」と回答した。

## 2. 完了根拠

同項目が要求する4つの検出は、いずれも実装とTestで固定されている。

| 要求 | 実装 | Test |
| --- | --- | --- |
| 第二正本化の検出 | `_non_authority_declared_inputs()`。上位文書が非authorityと宣言する4 identityの限定列挙 | `test_hand_editable_handoff_is_not_accepted_as_authority`、`test_status_document_is_not_accepted_as_authority`、`test_todo_handoff_template_is_not_accepted_as_authority`、`test_initial_development_checklist_is_not_accepted_as_authority` |
| 欠測推測の検出 | `_freshness_missing()`のキー欠落判定、`_incomplete_fixed_inputs()` | `test_missing_freshness_is_not_guessed_as_current`、`test_fixed_input_without_valid_digest_is_not_ignored` |
| staleの正常表示の検出 | `_freshness_missing()`の`stale`判定と診断表示への切替 | `test_stale_freshness_is_not_displayed_as_complete`、`test_stale_input_text_does_not_assert_a_normal_next_action` |
| 競合の正常表示の検出 | `_fixed_input_digest_conflicts()` | `test_conflicting_digests_for_one_identity_are_inconsistent` |

過剰な一般化を防ぐ境界例として`test_plan_authority_markdown_is_still_accepted`を固定し、
Plan authority自身が拒否されないことを保証している。実測でも、一般規則へ広げると
既存6件とこの境界例が落ちることを確認済みである。

公式全Testは`1017 passed`（failed 0、errors 0、Python 3.9.6、pytest 8.4.2、fallback `false`）。

## 3. 完了に含まれない範囲

**この承認はWork 6Aの段完了ではない。** 承認したのは`CL-6A-08`の1項目だけである。

- Work 6Aの他10項目は未完了のまま残る。対応inventoryで`out_of_approved_scope`とした
  20項目（計画側の分類）にも着手していない。
- Current Work Projectionの正式record写像は`DEC-WORK5A-PROJECTION-ROUTING-001`の
  再開条件が満たされるまでdeferredである。
- 拒否対象は4 identityの完全一致であり、上位文書が名指ししていない手編集経路、
  path表記のゆれ、file名変更後の追随は扱わない。
- `freshness`の`unknown`など他の値、固定入力のDigestと実file内容の突き合わせは扱わない。
- 入力側にauthorityを宣言させる方式は非承認範囲のままである。

## 4. 固定Evidence

| path | SHA-256 |
| --- | --- |
| `records/development/2026-08-06-work6a-non-authority-input-green-evidence-v1.md` | `79c5783c6f759c631aeabc41916fcc93f914984e2278ab1acb29589e1119a5ac` |
| `records/development/2026-08-06-work6a-projection-negative-green-evidence-v1.md` | `cc52783bc898a62e96a52e6b5d3df548e5572818ea2e37d4b5b43d3e5898638c` |
| `records/development/2026-08-06-work6a-projection-negative-red-evidence-v1.md` | `8dcff9e7f08a2098c6be6175cd940291f8f93a99903691dd0b94542671896d20` |
| `records/development/2026-08-06-work6a-evidence-correction-v1.md` | `219eefc14dcda02d4ea72e70682bcaf0fe9ea98d752cb25aacc79dcee64871b7` |
| `records/development/2026-08-06-work6a-non-authority-input-scope-decision-v1.md` | `2991aed38dd7e6f294774baa0ff98d664168bd8f2fffdc3337e7228938109af8` |
| `records/development/2026-08-06-work6a-negative-path-test-inventory-v1.json` | `51674c143858b37608c7914c5bc2a8973be8221e2d5bde9707d89d082f995a16` |

判断時点のGitとTestは、branch `main`、HEAD `7055ed9`、worktree clean、公式全Test
`1017 passed`である。

## 5. 既存recordへの影響

new-onlyで作成した。既存record、Contract、accepted artifact、Provenanceの上書き、削除、
無効化、stale化は行っていない。checklistは当該checkboxとEvidence節だけを更新する。
