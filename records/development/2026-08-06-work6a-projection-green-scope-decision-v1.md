# Work 6A Current Work Projection negative path GREEN実装範囲 承認Decision v1

- Decision ID：`DEC-WORK6A-PROJECTION-GREEN-SCOPE-001`
- decision maker：Human
- decided at：`2026-08-06T08:59:32+09:00`
- decision：`approved`
- decision class：`implementation_scope_decision`
- authority mode：`human`
- 上位Decision：`DEC-WORK5A-PROJECTION-ROUTING-001`
  （`records/development/2026-08-06-work5a-current-work-projection-routing-decision-v1.md`）

## 経緯

`DEC-WORK5A-PROJECTION-ROUTING-001`（案A）はRED固定までを承認し、GREEN実装範囲は
別途Human判断で確定すると定めていた。RED固定の完了後、実測から判明した制約を添えて
GREEN実装範囲をHumanへ提示し、Humanは「提案を受け入れる」と回答した。

## 承認した実装範囲

変更対象は`tools/development/session_log_bootstrap.py`の診断判定と表示に限る。
次の5規則を追加する。

1. `fixed_inputs`の各要素に`identity`と64桁の`digest`が揃わないものを、無視せず
   `diagnostics["missing"]`へ挙げる。文言に当該`identity`を含める。
2. 手編集できる引き継ぎメモを現在位置のauthorityとして受け付けない。対象は
   **`TODO_NEXT_SESSION.md`の限定列挙1件だけ**とする。
3. `freshness`がキー欠落または`stale`のとき`diagnostics["status"]`を`complete`にしない。
4. `fixed_inputs`に同一`identity`で異なる`digest`があるとき`conflicts`へ挙げ、
   `status`を`inconsistent`にする。
5. 上記に該当するとき、`render_current_work`は通常の現在位置表示ではなく診断表示を返し、
   次作業を断定せず修復指示にする。

`status`の優先順位は既存どおり（競合→`inconsistent`、欠落→`incomplete`、
どちらも無ければ`complete`）を維持する。

## Humanが個別に承認した2つの限定

RED Evidence §8の既知制約に基づき、次の限定をHumanが明示的に承認した。

1. **手編集sourceの拒否対象は`TODO_NEXT_SESSION.md`の1件だけに限定する。**
   拡張子`.md`や`docs/`配下といった一般規則にすると、Plan authority自身の
   `docs/current/reviewcompass3-plan-current.md`が拒否され、既存Testが壊れる。
2. **`freshness`の拘束はキー欠落と`stale`の2つだけに限定する。**
   `unknown`など他の値へ一般化すると、既存fixture
   `tests/fixtures/development/session-log-bootstrap/projection-incomplete-inputs.json`
   の`freshness: unknown`が既存Testの完全一致assertionを壊す。

## 非承認範囲

- 新しいschema、state、authority、module、設定fileの追加。
- Current Work Projectionの正式record写像。これは`DEC-WORK5A-PROJECTION-ROUTING-001`の
  再開条件が満たされるまでdeferredのままである。
- 正式Portfolio／Work Item／Workflow stateの実装。
- Work 6Aのうち、対応inventoryで`out_of_approved_scope`とした20項目。
- Work 4B、Work 5B、Work 7、Work 8、UI、automation、外部送信、push、PR、CI。
- Work 5AまたはWork 6Aの段完了。

## 実装規律

- 既存のRED testを弱めない。実装が通らない場合はTestではなく実装を直す。
- Testの期待が誤っていると判明した場合は、実装を進めず停止してHuman判断を得る。
- 統合対象commitは全Test greenにする。

## 固定Evidence

| path | SHA-256 |
| --- | --- |
| `records/development/2026-08-06-work5a-current-work-projection-routing-decision-v1.md` | `f084b471d3fe4ba40a9c6a7a5e3882fa78090da54c7e9b19b04547dde5307eda` |
| `records/development/2026-08-06-work6a-projection-negative-red-evidence-v1.md` | `8dcff9e7f08a2098c6be6175cd940291f8f93a99903691dd0b94542671896d20` |
| `records/development/2026-08-06-work6a-negative-path-test-inventory-v1.json` | `51674c143858b37608c7914c5bc2a8973be8221e2d5bde9707d89d082f995a16` |
| `tests/test_work6a_current_work_projection_negative.py` | `25a76b7ba39dc032c3e30204cf9d83377129d9b530ab4eeb90dd0f5a199ade0f` |

判断時点のGitとTestは、branch `main`、HEAD `9a39365`、worktree clean、公式全Test
`1007 passed / 6 failed`（失敗は新規RED 6件のみ、total 1013、Python 3.9.6、pytest 8.4.2、
fallback `false`）である。

## 別件のHuman指示

同じ回答でHumanは「恒久的な検査器の追加を検討」も指示した。これは調査と提案までの指示であり、
**検査器実装の承認ではない**。提案はHuman判断候補として別文書へ固定し、承認を得るまで
実装しない。

## 既存recordへの影響

new-onlyで作成した。既存record、Contract、accepted artifact、Provenanceの上書き、削除、
無効化、stale化は行っていない。
