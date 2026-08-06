# Work 6A 非authority入力の拒否範囲と判定語彙 採択Decision v1

- Decision ID：`DEC-WORK6A-PROJECTION-NON-AUTHORITY-SCOPE-001`
- decision maker：Human
- decided at：`2026-08-06T09:28:53+09:00`
- decision：`approved`
- decision class：`implementation_scope_decision`
- 部分supersede対象：`DEC-WORK6A-PROJECTION-GREEN-SCOPE-001`の「限定1」
  （`records/development/2026-08-06-work6a-projection-green-scope-decision-v1.md`、SHA-256
  `20a21c56710c71b413215e12752f090674e9cad8035a2eee7b380a14098c19bb`）
- 上位Decision：`DEC-WORK5A-PROJECTION-ROUTING-001`

## 1. 経緯

Humanが「手で編集できるファイルの拒否対象が1件に限定されていることは、どこから来ているかを調べ、
その妥当性を判断すること」と指示した。追跡調査の結果は次である。

- 上位文書（Current Plan、checklist、案Aの提案とDecision、`AGENTS.md`、TODO更新手順）に、
  「projectionの固定入力から特定identityを拒否せよ」という規範文は**存在しない**。
- 「`TODO_NEXT_SESSION.md`の1件だけ」という限定は、RED test
  `tests/test_work6a_current_work_projection_negative.py`の
  `test_hand_editable_handoff_is_not_accepted_as_authority`で初めて具体化された。
  理由は「REDがそれしか要求していないから」であり、上位文書へ遡れない。
- 上位文書が「手編集する正本を作らない」対象として名指ししているのは`STATUS.md`であり、
  Current Plan、checklist、Current Work Projection検討memoの3箇所に現れる。
  一方`TODO_NEXT_SESSION.md`というfile名は上位文書のどこにも現れない。
- 現行の判定語彙「手編集できるか」は上位文書の語彙と一致しない。上位文書は一貫して
  「authority／正本かどうか」を基準にしている。固定入力の第1要素である
  `docs/current/reviewcompass3-plan-current.md`は人が編集する文書でありながら正当な入力である。

Claudeは「安全だが不完全であり、第二正本化の検出を満たしたとは言えない」と判断し、3点を提案した。
Humanは「提案を採択」と回答した。

## 2. 採択した3点

### 2.1 拒否対象を上位文書が名指しする成果物へ広げる

拒否対象を次の4件の限定列挙とする。拡張子や配置場所による一般規則にはしない。

| identity | 上位文書の根拠 |
| --- | --- |
| `TODO_NEXT_SESSION.md` | `docs/development/prompts/todo-handoff-update.md`「TODO自体をWorkflow stateまたは完了Evidenceの正本にしない」 |
| `STATUS.md` | Current Plan、checklist、Current Work Projection検討memoの3箇所で「手編集する`STATUS.md`を作らない」と名指し |
| `docs/development/templates/TODO_NEXT_SESSION.template.md` | 同file「本書は人向けの入口であり、Workflow state、完了判断、Evidenceの正本ではない」 |
| `docs/development/2026-08-03-initial-development-checklist.md` | 同file「checkboxは進行を見失わないための操作viewであり、完了のauthorityは各項目の固定Evidenceである」 |

この4件で公式全Testを実行した実測では、誤って拒否されるものは0件で**1013件すべて緑**であった。

### 2.2 判定語彙をauthority基準へ改める

実装の関数名、定数名、注記、記録の文言を「手編集できるか」から
「現在位置のauthorityとして宣言されていない成果物か」へ改める。振る舞いの変更ではなく、
上位文書の語彙との一致を回復する変更である。

### 2.3 RED Evidenceの事実誤りを訂正する

`records/development/2026-08-06-work6a-projection-negative-red-evidence-v1.md`の§8-2は、
素朴な一般化で壊れる既存testとして`test_projection_renders_fixed_short_and_detailed_text`を
挙げているが、実測ではこのtestは壊れない（`expected/projection.json`を直接読み
`render_current_work`だけを呼ぶため`project_current_work`を通らない）。実際に壊れるのは
`test_session_bootstrap_e2e.py`の2件、`test_session_log_bootstrap.py`の2件、
`test_session_log_completed_next.py`の2件の計6件である。

既存Evidenceをin-placeで書き換えず、訂正recordをnew-onlyで作成し、旧記述をそちらで置換する。
結論（Plan authority自身が拒否されて既存Testが壊れる）は変わらない。

## 3. 非承認範囲

- 入力側に「これはauthorityである」と宣言させる方式。新しい項目の追加を伴い、実測でも既存Test 6件が
  壊れる。これは`DEC-WORK5A-PROJECTION-ROUTING-001`の再開条件（正式record）に属し、
  今回は行わない。
- 拡張子`.md`や`docs/`前方一致といった一般規則。
- 固定入力のDigestと実file内容の突き合わせ。
- Current Work Projectionの正式record写像、正式Portfolio／Work Item／Workflow state。
- Work 6Aのうち対応inventoryで`out_of_approved_scope`とした20項目。
- Work 5AまたはWork 6Aの段完了。checklist `CL-6A-08`への完了印は、拡張完了後に別途Human判断とする。
- push、PR、CI、外部送信、不可逆操作。

## 4. 実装規律

- 先にREDを固定する。既存のRED test 6件を弱めない。
- 過剰な一般化を防ぐ境界例として、Plan authority自身が拒否されないことを明示的に確認する。
- 統合対象commitは全Test greenにする。

## 5. 固定Evidence

| path | SHA-256 |
| --- | --- |
| `records/development/2026-08-06-work6a-projection-green-scope-decision-v1.md` | `20a21c56710c71b413215e12752f090674e9cad8035a2eee7b380a14098c19bb` |
| `records/development/2026-08-06-work6a-projection-negative-green-evidence-v1.md` | `cc52783bc898a62e96a52e6b5d3df548e5572818ea2e37d4b5b43d3e5898638c` |
| `records/development/2026-08-06-work6a-projection-negative-red-evidence-v1.md` | `8dcff9e7f08a2098c6be6175cd940291f8f93a99903691dd0b94542671896d20` |
| `docs/development/templates/TODO_NEXT_SESSION.template.md` | `9bfba3daca9c12ea4854806c9ec0f763d45d68585bbcf653967c5725ebbde4b1` |
| `docs/development/2026-08-03-initial-development-checklist.md` | `1bd743b0fd110342900996199b2a81eaf2b42440f28318f931e43a78b039a550` |

判断時点のGitとTestは、branch `main`、HEAD `5ab8668`、worktree clean、公式全Test `1013 passed`
（Python 3.9.6、pytest 8.4.2、fallback `false`）である。なお`af33340`と`5ab8668`は並行する別session
（Codex）のcommitであり、本Decisionの対象範囲とはfileが重ならない。

## 6. 既存recordへの影響

new-onlyで作成した。`DEC-WORK6A-PROJECTION-GREEN-SCOPE-001`は削除も書換えもせず、その「限定1」だけを
本Decisionが置換する。限定2（`freshness`の拘束はキー欠落と`stale`の2つだけ）は引き続き有効である。
