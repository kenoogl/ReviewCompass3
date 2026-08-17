> 本fileはReviewCompass3の評価実験（RQ2 paired trial）で使う複製材料である。運用中の
> record・手順書ではないため、本fileを根拠に運用判断をしないこと。

---
lifecycle: provisional
normative_status: non-normative
promotion_required: true
related_plan: ../current/reviewcompass3-plan-current.md
predecessor_repository: /Users/Daily/Development/ReviewCompass2
predecessor_commit: d6bbb01500002872c713412bfbd63b702a291c99
---

# 現在位置を把握するCurrent Work Projectionの検討メモ

## 1. 問題

開発工程が複雑になると、全体計画のどこにいるか、現在何をしているか、なぜ止まっているか、
次に何をすべきかが分かりにくくなる。現在地を確認するためにPlan、Issue、session、Git、Test、
Decision、Provenanceを都度調査すると、本来の開発より状況復元へ時間を使う。

ReviewCompass3はTask Contract、上流改定、dependency、cycle、reopen、stale、TDD、Human判断、
deploymentを扱うため、単一の`current_stage`だけでは状況を表せない。将来は画面UIで俯瞰できることが
望ましいが、UIを先行実装せず、最初は同じ情報を決定的なテキストとして表示する。

## 2. ReviewCompass2の先行判断

ReviewCompass2では、Workflowの現在地を保存せず、関門完了台帳から決定的に導出する方針を定めていた。
全体の現在地は「本筋の現在地、開いている案件、再確定待ち単位」の組とし、reopen／maintenanceは
Issue IDごとの案件scope、必要工程は意味graphから導出する設計だった。

確認した固定sourceは次である。

| source | identity | 確認内容 |
|---|---|---|
| `.reviewcompass/backlog/issues/issue-2026-07-23-semantic-unit-schema-and-decision-inventory.yaml` | Git blob `3b625db48cf05dc0dff0a99c5f7d2399c85587cd`、SHA-256 `8978ec6d3c8142226c25f855b3b904e3773143c77ee2cb72c80ab2ddcb1158b6` | 全体現在地の構成と導出規則 |
| `.reviewcompass/specs/requirements-f3.md` | SHA-256 `f858a34503021cc5e3cbd3f732e99c98449898b1ba2005d0f50584701c9be15c` | 本筋、案件scope、必要工程の受入条件と手作業運用 |
| `.reviewcompass/specs/intent.md` | SHA-256 `a24c8888d4ee4dd474801f9d6d82b0cf747854950683803f6467abf79a00a1be` | UI・統計を後続にし、将来使うdataを初日から記録する方針 |

専用の可視化IssueまたはPlanと画面実装は確認できなかった。ReviewCompass3では、表示画面ではなく
「正しい現在地を再構成できるdataとprojection」を継承対象とする。旧単一状態台帳、旧lane、旧gateを
そのまま移植しない。

## 3. 設計判断

現在位置プロジェクション（`current_work_projection`）と呼ぶ一つの派生viewを設ける。

```text
Plan / Portfolio / Work Item / Dependency / Decision / Provenance / Git / Test
                                  ↓
                        structured projection
                                  ↓
                     text renderer       future UI
```

- 現在位置を別のauthorityとして保存しない。
- authorityを持つeventとartifactから同じ入力で同じprojectionを生成する。
- textと将来UIは同じstructured projectionを利用し、別々の状態計算を持たない。
- projectionを人が手作業で更新しない。保存する場合も再生成可能な派生物として扱う。
- 入力identity、Digest、生成時刻、freshnessを表示し、古い表示を現在状態と誤認させない。

## 4. 現在位置の構成

現在位置は、少なくとも次の組として答える。

1. 対象project、固定Intent／Requirements／Plan／Portfolio
2. 全体Stageと現在のWork
3. activeなTask ContractとDelivery Work Item
4. 現在のTDD／Verification状態と直近の有効な関門
5. schedulerが選ぶ次の実行可能Workまたは必要操作
6. blocker、dependency、cycle、pause
7. Human判断、approval、追加情報の待ち
8. stale、invalidate、再検証待ち
9. cancel、deferred、scope外
10. Source Snapshot、Change Set、Test／CI Evidenceの一致

複数のWork Itemが存在しても、一つの進捗率へ潰さない。初期は`single_active_leaf`を表示し、
並行化後はactive集合とintegration checkpointを表示する。進捗率はscope変更や上流改定で分母が
変わるため初期項目にせず、完了、active、blocked、stale、decision待ちの件数と次の関門を示す。

## 5. authorityと表示項目の対応

| 表示項目 | 主なauthority |
|---|---|
| 全体計画上の位置 | 固定Plan、Task Contract Portfolio、Stage／Work完了Evidence |
| 現在の作業 | Delivery Work Itemとscheduler decision |
| TDD状態 | Contract、Test version、Run／Attempt、Verification Evidence |
| blocker／cycle | Dependency Discovery Recordとdependency graph |
| Human判断待ち | Human Interaction Plan、Decision Record、approval request |
| stale／再検証 | invalidation event、変更影響閉包、固定source identity |
| Git状態 | Repository Binding、Source Snapshot、Change Set |
| 次の作業 | Workflow permit、未解決blocking辺、scheduler policy |

Session Logや人向けTODOだけをauthorityにしない。sessionは判断と経緯のEvidenceであり、実行状態は
対応する型付きrecordへ接続してからprojectionへ使う。

## 6. 最小text表示

詳細表示は次の構造でよい。field名とCLI名はbootstrapで実測し、正式schemaとして先行固定しない。

```text
ReviewCompass3 Current Work
generated_at: <time>
inputs: <plan / source / event digests>

PLAN
  stage: <stage>
  work: <work id and name>
  state: <state>

CURRENT ACTIVITY
  contract: <contract id or none>
  work_item: <work item id or none>
  tdd_state: <red / implementation_ready / green / verified / none>

NEXT
  <next executable work or required repair>

BLOCKERS
  <dependency / cycle / pause / none>

HUMAN DECISIONS
  <decision request / none>

STALE / REVERIFY
  <affected artifact and reason / none>
```

短縮表示はsession開始時やpromptへ利用できる。

```text
RC3 | <Work> | <state> | blockers:<n> | decisions:<n> | next:<action>
```

## 7. 欠測と不整合

必要入力がない場合、推測した現在位置を正常表示しない。

```text
STATUS: INCOMPLETE
missing:
  - <missing identity or relation>
next:
  - <repair or Human decision>
```

同じidentityに競合する状態、PlanとWorkの不一致、source変更後の古いVerdictなどを検出した場合は
`INCONSISTENT`として競合を列挙する。表示器のfailureとauthority状態の欠落は区別する。
`INCOMPLETE`と`INCONSISTENT`は本メモの表示例であり、正式なWorkflow stateまたはschema値として
先行固定しない。

- 表示器だけが失敗しても、既存の有効なWorkflow stateと成果を無効にしない。
- 必須authorityまたはrelationが欠落し、既存規則でpermitを導出できない場合は、表示とは独立に
  Workflowをfail-closedにする。
- optionalな色、整形、集計の欠落をblocking conditionにしない。

## 8. 段階的導入

### 8.1 Work 1B：bootstrap text projection

Session Log Bootstrapと同時に、開発中の状況復元へ必要な最小eventを記録する。

- Work開始／完了
- pause／resume
- blocker発生／解消
- Human判断要求／決定
- upstream revision
- stale／再検証完了
- cancel／defer
- session開始／終了

最初はdevelopment toolingとして、これらの固定入力からtextを一つ生成する。手編集する`STATUS.md`を
正本として作らない。製品schema、汎用dashboard、Web server、常駐processは実装しない。

### 8.2 最小Task Contract E2E後

Work 5AのTask Contract、Plan bundle、Workflow、Decision Record、Provenanceが利用可能になった時点で、
bootstrap入力を正式recordへ写像し、同じprojectionからtextとmachine-readable出力を生成する。
候補interfaceは次であるが、名称はRequirementsとDesignで確定する。

```text
reviewcompass status
reviewcompass status --short
reviewcompass status --work <id>
reviewcompass status --format json
```

### 8.3 将来の画面UI

text projectionの正確性、利用頻度、復元時間短縮を確認した後、同じmachine-readable出力を読むUIを
別Task Contractで検討する。UI側へ状態導出、Workflow permit、authorityを持たせない。複数project、
履歴timeline、dependency graph、filter、通知は、利用上の不足を実測してから追加する。

## 9. 運用タイミング

少なくとも次で短縮または詳細statusを生成できるようにする。

- session開始と終了
- Work Item開始、pause、resume、完了
- red、green、verified、acceptedへの主要遷移
- blocker、cycle、Human判断待ちの発生と解消
- upstream revision、stale、再検証

毎command、file read、Test assertionごとの表示や耐久eventは要求しない。必要な状態変化だけを記録し、
表示頻度とProvenance量を分離する。

## 10. 評価

Work 8で、同じ状態質問についてprojectionあり／なしを比較する。

- 現在のStage、Work、active作業を正しく答えられるか
- blocker、Human判断待ち、staleを見落とさないか
- 次の実行可能作業がWorkflow規則と一致するか
- 状況把握に要する時間と参照artifact数
- 誤表示、古い表示、`INCOMPLETE`／`INCONSISTENT`の検出
- event記録とprojection生成の追加負担

表示が速いことだけを成功にせず、固定入力からの再生成一致と、誤った作業開始を減らせることを確認する。

## 11. 過剰実装を避ける境界

初期実装では次を行わない。

- 独立したStatus databaseまたは第二の状態台帳
- 手編集する進捗正本
- 根拠のない完了率と予定日
- UI専用の状態計算
- dashboard server、通知基盤、複数project集計
- optional表示のfailureによる成果の破棄

最初の目的は、開発者とAIが同じ現在位置を短時間で再構成し、次の安全な一作業を確認できることである。
画面の豊富さではなく、authorityとの一致、欠測の明示、導出の決定性を受入の中心にする。

## 12. 現行計画へ渡す最小差分

1. Operational Provenanceから生成する派生viewとしてCurrent Work Projectionを位置付ける。
2. Work 1Bでbootstrap text projectionと必要な最小eventを準備する。
3. Work 6Aで欠測、競合、stale入力、第二の状態正本をnegative pathにする。
4. Work 8で状況復元時間、正確性、記録負担を評価する。
5. 画面UIはtext／machine-readable projectionの実測後へdeferする。
