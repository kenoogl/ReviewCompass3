# Final Challenge 意図毀損検出 設計提案（CL-6A-10）

状態：`approved`（2026-08-06、Human文言「承認」。§7の3点すべてを承認）

対象：Work 6Aチェックリスト項目`CL-6A-10`「Contract適合でも上位Intent／Requirementを損なう成果を
Final Challengeで検出する」の負例固定と、そのために必要な最小の仕組み。

## 1. 結論（推奨）

2層で作る。

- **テスト層（今回作る・決定的）**：「意図を損なう」という審査所見を固定材料として差し込み、
  最終審査がそれを見逃さず受理を止めることをREDで固定する。所見の中身を機械が意味判定しない。
- **運用層（将来・接続口だけ今固定）**：その所見を実際に生み出す担い手として、複数経路の
  LLMレビュー＋Human裁定を接続する。導入は外部送信承認を伴う別Task Contractとする。

## 2. 固定した現在地（2026-08-06実測）

- `evaluate_final_challenge`（`tools/task_contract/execution.py` 304-330行）の判定は
  `status = "passed" if conformance_verdict["status"] == "passed" else "failed"`である。
  **Conformanceの合否を写すだけで、独自の検出を1つも持たない。** 担当者分離
  （`owner_separation_violated`）だけが実質である。
- したがって「Contract適合（Conformance passed）だが意図を損なう成果」は、現構造では
  **原理的に検出できない**。CL-6A-10の負例が未整備なのは、検出の入口が無いためである。
- findingは`finding_id`／`severity`（error・warning・info）／`target_ref`／`requirement_ref`／
  `rule_id`／`description`を持ち、種別（契約適合性か、意図毀損か）と発生元の区別が無い。
  `finding_set`の`reviewer`は`deterministic_stub`固定、`calls_llm: False`。
- severity `error`はConformanceを落とすため、意図毀損をerrorで表すとConformance段で落ちてしまい、
  「Contract適合**なのに**最終審査で落ちる」という本項目の意味を表現できない。

## 3. 規範宣言（P1〜P7）

### テスト層（今回の範囲）

- **P1**：findingは**種別**（`contract`＝契約適合性／`intent_damage`＝上位意図毀損）と
  **発生元**（`deterministic_stub`／`subagent`／`external_api`／`human`のroute種とidentity）を
  保持できる。種別が無い既存findingは`contract`として扱い、既存Test・既存recordは無変更で
  合格し続ける（後方互換）。
- **P2**：Conformanceは`contract`種別のfindingだけで判定する。`intent_damage`のblocking findingが
  あってもConformanceは落ちない（審査の分離。REQ-CONTRACT-004の「Conformance、Definition
  Challenge、Final Challengeを分離する」に従う）。
- **P3**：Final Challengeは、**Human採否済み**でblockingな`intent_damage` findingが1件でもあれば、
  Conformanceがpassedでも`failed`とする。これが本項目の中核負例である。
- **P4**：Human採否が**未了**の`intent_damage` findingが存在する場合、Final Challengeはverdictを
  出さずfail-closedで停止する（`human_decision_required`の実質化）。LLM所見だけで受理を
  通すことも覆すこともしない。
- **P5**：複数の所見は潰さず保持する。重複・競合・独立所見をそのまま残し、自動多数決で
  裁定しない（REQ-TRIAGE-002）。
- **P6**：Human採否でrejectされた`intent_damage` findingは、Final Challengeの判定に影響しない。
  rejectの事実と理由はProvenanceへ残る。

### 運用層（接続口の宣言のみ。実装は範囲外）

- **P7**：所見の発生経路は形式上等価とする。外部APIのLLM、**サブエージェントのLLM**、人の
  いずれが生成しても、P1の形式で受け取り、経路identityをProvenanceに残す。
  - サブエージェント経路は、外部APIが使えない環境でも動く経路として価値がある。完全な独立には
    劣るため、独立性を可能な限り高める運用要件を残す：別contextで起動し会話履歴を共有しない、
    相互の所見を見せない、可能なら異なるmodelを使う、観点（lens）を分けて割り当てる、
    反証する側の枠組みで指示する。
  - 同系modelの複数レビューを、high riskの唯一の独立oracleにしない（work-review-protocol §5）。
  - **LLMの所見は人が判断する材料であり、裁定ではない**（Human文言、2026-08-06）。
  - LLM呼び出しの実装は外部送信承認を伴う別Task Contractとし、Capability Adapter（Current Plan
    §11.4）として交換可能にする。

## 4. 実装範囲（承認された場合）

- `tools/task_contract/execution.py`のfinding生成・`_severity_counts`・`evaluate_conformance`・
  `evaluate_final_challenge`への最小変更（P1〜P6）。新module・新schema fileは作らない。
  finding fieldの追加は後方互換（省略時は`contract`）とする。
- RED先行。宣言P1〜P7それぞれへREDまたは境界例を結んだ対応表recordを作成し、
  「testの無いP」が0件であることを機械で数えてから実装する（2026-08-06に確立した関門）。
- P7はtestでは「形式を受け取れること」（fixture所見のroute種が保持されること）までを固定し、
  LLM呼び出し・orchestration・prompt設計は固定しない。

## 5. 非対象

- LLMレビューの実装（外部API・サブエージェントとも）、外部送信、prompt設計、reviewer選定。
- 複数round・複数reviewerの完全なharness（REQ-EXEC-004の全体）。
- Findingの意味的な自動裁定、重複の自動統合。
- Work 6Aの他項目、段完了、Work 8前倒し。

## 6. 危険と緩和

| 危険 | 緩和 |
| --- | --- |
| Work 5Aのrecord形（finding）への変更 | 後方互換（省略時`contract`）。既存Test 1032件が無変更で合格することを完了条件にする |
| 「意図毀損」の意味判定を機械が僭称する | 機械は種別・採否・blockingの形式だけを判定する。意味の判定は所見の生成者（将来はLLM＋Human裁定）に属し、テストは固定fixtureで行う |
| 未裁定所見の滞留 | P4のfail-closed停止で、滞留したまま受理へ進むことを禁止する |

## 7. Human判断事項

1. P1〜P7の承認。
2. Work 5Aのfinding・verdict機構への後方互換な変更（§4）の承認。
3. 運用層（LLMレビューの実際の導入）を別Task Contractへ分けることの確認。
