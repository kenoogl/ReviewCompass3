# authority参照Digest検査器 完了レビュー結果 v1

- Reviewer model：`gpt-5.6-sol`
- reasoning effort：`high`
- レビュー日：2026-08-10
- Reviewer：Codex
- collaboration mode：`role_neutral_pilot_review`
- レビュー段階：completion（完了レビュー）
- risk：`high`（Human確定済み）
- 判定：`report_execution_mismatch`
- Finding：blocking 1件、non-blocking 0件

【実測】起動時に表示されたmodel名とreasoning effortは
`gpt-5.6-sol`／`high`だった。

## 1. 固定対象と開始状態

- review request：
  `records/session-handoffs/2026-08-10-claude-pilot-reference-digest-checker-review-request-v1.md`
- review request SHA-256：`99569c2e7f786b4624f3aa4ba1f81e3fb93a1aa4b7100cfa24d3cb396dc1f308`
- review request commit：`929e6628e55db04ac1856987758d0321c87ef3e2`
- 有効scope：
  `records/session-handoffs/2026-08-10-claude-pilot-reference-digest-checker-scope-v2.md`
- scope SHA-256：`c37b7742a05592f514fac85f5bed606c8e396410a9df7deeac22a7afe46f9172`
- base：`c7579fffcb3bf407df80084c7190b68098dc202e`
- branch：`main`
- 許可範囲：本判定recordの作成と単独commit
- 禁止範囲：実装、Test、既存record、TODO、checklist、Issue stateの変更、外部操作、Closer作業

【実測】review requestは対象pathのGit履歴上の最新recordで、レビュー開始時のHEADだった。
worktreeとindexはcleanだった。本record予定pathの`git check-ignore --no-index`は終了コード1で、
ignore対象ではなかった。

## 2. commit列、変更範囲、Digest

【実測】`git rev-list --ancestry-path --reverse c7579ff..929e662`で次の直列を確認した。

1. `34f44da`：SCOPE v2 record 1件
2. `40ccd3b`：再範囲レビューv2 record 1件
3. `c3bcb0f`：RED Test 1件
4. `6706cff`：訂正RED Test 1件
5. `f61eeca`：検査器、許可一覧、GREEN Evidence、receiptの4件
6. `929e662`：review request 1件

【実測】`git diff --name-status c7579ff 929e662`の8 pathは、scopeとReviewer recordを含む予定範囲に
一致した。`git diff --check c7579ff 929e662`は終了コード0だった。RED commitにはTestだけがあり、
同commitのtreeに`tools/development/authority_reference_checker.py`は存在しなかった。
`c3bcb0f..6706cff`のTest差分は、期待参照数`10→11`、file内参照数`9→10`の2箇所だけで、
拒否条件の緩和はなかった。

【実測】固定入力13件はscope記載SHA-256と13／13一致した。次の成果物もreview requestの値と一致した。

| file | SHA-256 |
| --- | --- |
| `tools/development/authority_reference_checker.py` | `8641ceb7fb615c217ff9d67fd15229409d6a30dd1fb3a443ce556a1425cb707f` |
| `tools/development/authority_reference_keys.json` | `560a835103765149f7e02b52876b6d2cec2e4817e7ec94c8ab1cfea85cd744b2` |
| `tests/test_authority_reference_checker.py` | `b6edd8ce4f9c598a8240eb7562fccdeb267404ba961fcd341f8813c6241e398c` |
| GREEN Evidence | `0a4211136354e51f7b293f843046c32f8a699d4ece9d2365da5c068ee3859724` |
| 公式receipt | `5de14a42510d26721327db1b610b2b0c9c66cff4ea2ed5c67a09cbb497a0f518` |

【実測】許可一覧はHuman承認済みの7 keyと過不足なく一致し、`generated_from`を含まない。
各keyの期待形もscopeどおり、`authority_order`と`related_design`が`mapping_list`、残り5 keyが
`mapping`だった。

## 3. 独立再実行

【実測】次をそれぞれ単独commandとして実行した。

| 区分 | command | 結果 | exit code |
| --- | --- | --- | --- |
| targeted | `.venv/bin/python3 -m pytest tests/test_authority_reference_checker.py` | 15 passed | `0` |
| 関連回帰 | `.venv/bin/python3 -m pytest tests/test_todo_snapshot.py tests/test_layout_baseline.py` | 21 passed | `0` |
| 公式全Test | `.venv/bin/python3 -m tools.development.policy_test_runner --project-root . --suite full --receipt /private/tmp/2026-08-10-codex-authority-reference-review-full-receipt-v1.json` | 1353 passed、failed 0、fallback false | `0` |
| 実docs確認 | `.venv/bin/python3 -m tools.development.authority_reference_checker docs/development/2026-08-03-initial-development-checklist.md docs/current/reviewcompass3-plan-current.md` | 11 checked、11 matched | `0` |

【実測】Reviewerの公式全Test receiptを再読込みし、status `passed`、total 1353、failed 0、
source state digest `767bed9c6c4fb104f7c076cf5ba12772140b1678290b78fb76b8d24499670ab5`を確認した。
receiptのSHA-256は`52f0f3d3de0531665b166d2739a602c8a4fbc77cf014d2feac14f8bb94cdfa9e`だった。
一時receiptと反証fixtureは確認後に削除し、repository内へ残していない。

【実測】実docs確認ではチェックリスト8件、現行Plan 3件が一致した。現行Planの許可一覧外
`generated_from`にあるDevelopment Policyの記載Digestは`d37a60ab...3903ed46`、現行bytesは
`08bea1f9...a22ad1c`で不一致だが、合否に影響しなかった。正しい時点固定pinを誤拒否していない。

【実測】Pilot fixtureにない反証として、現行Planの実front matterを一時領域へ複製し、許可対象
`intent_ref`のDigestを`1950...`から`0950...`へ1文字だけ変更した。検査器は3件中2件をmatched、
1件を`intent_ref`・line 11のmismatchedとして報告し、終了コード5で拒否した。repository外を指す
symlinkへ同keyのpathを変更した別反証も、1 checked、1 invalid、終了コード5で拒否した。

## 4. Finding

### AR-P1-001：許可key行の不正な値を無視して合格させる

- 分類：`blocking`
- 確認段階：`completion`
- §11.1類型：3「誤った合格」を実証できる受入条件・検証の欠陥

【記録】scope v2 §7は、宣言された期待形だけを受け付ける専用解析とし、許可key配下の
解釈不能な形をfail-closed、すなわち安全側で不合格にするよう要求する。review request §3と
GREEN Evidence §3も、不正形をfail-closedにしたという完了Claimを置いている。

【実測】`tools/development/authority_reference_checker.py`の`_TOP_KEY`はkey行のコロン後を
正規表現で取得するが、`_extract_references`はその値を確認せず、下位行の`path`と`sha256`だけを
解析する。このため、許可keyに不正な値が同居しても、下位の参照対が正しければ合格する。

【実測】§11.3の類型一括掃討として、Pilotの合成fixtureにない実docs形式から次の4変種を作り、
それぞれ単独で機械実行した。いずれも本来は宣言形と異なるが、`invalid` 0、全参照matched、
終了コード0になった。

| 宣言形 | 反証したkey行 | 結果 |
| --- | --- | --- |
| `mapping` | `intent_ref: unexpected` | 3 checked、3 matched、exit `0` |
| `mapping` | `intent_ref: []` | 3 checked、3 matched、exit `0` |
| `mapping_list` | `authority_order: unexpected` | 8 checked、8 matched、exit `0` |
| `mapping_list` | `authority_order: {}` | 8 checked、8 matched、exit `0` |

【判断】これは将来設計の提案ではなく、明示された現在の受入条件に対する誤った合格である。
targeted Testと公式全Testの合格は既存fixture集合について有効だが、この反証を覆わない。
GREEN Evidenceとreview requestの「不正形をfail-closedにした」という完了Claimは実状態と競合する。

必要な修復は、許可key行のコロン後に空白以外の値がある場合を不正形として終了コード5で拒否し、
少なくとも`mapping`と`mapping_list`の上記変種をRED Testへ追加することである。Reviewerは実装修正を
行っていない。

## 5. Human境界、未実施、判定

【実測】Humanによるrisk `high`確定、7 key許可一覧承認、RED開始承認、訂正RED承認はreview requestへ
固定されている。許可一覧の追加・削除、実docsの修復、Issue state更新、TODO・checklist反映は行われて
いない。Reviewerが行った実docs確認は固定実例2件への読み取り専用実行だけで、書換えや広域適用はしていない。
レビュー開始時のlocal tracking表示は`main...origin/main [ahead 312]`で、本作業commitはlocalのままだった。

判定：`report_execution_mismatch`

競合Evidence：scope、GREEN Evidence、review requestは許可key配下の不正形をfail-closedにしたと報告するが、
AR-P1-001の4反証は同じ不正形を終了コード0で合格させた。

影響：GREEN Evidenceとreview requestのfail-closed完了Claim、および本sliceの完了判定はstaleである。
既存Testと公式receiptの実行結果自体は有効だが、`verified`またはCloser projectionの根拠にしない。

未実施：実装修正、Test変更、既存record変更、Issue resolve、TODO・checklist反映、外部操作、Closer作業。

次：HumanがAR-P1-001の修正をPilotへ戻すことを承認する。
