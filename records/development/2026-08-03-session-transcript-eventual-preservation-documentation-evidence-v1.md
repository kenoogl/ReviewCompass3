---
evidence_id: RC3-SESSION-TRANSCRIPT-EVENTUAL-PRESERVATION-DOCUMENTATION-2026-08-03-V1
recorded_at: 2026-08-03T23:47:06+09:00
status: verified
workflow_state: documentation_completed
confidentiality_class: project-internal
---

# Session Transcript Eventual Preservation Documentation Evidence V1

## 1. 結果

Humanが示した「session終了hookに依存せず、継続回収と事後整合で考える」方向を設計文書へ固定した。
文書は、保証目標、artifact関係、component責務、状態モデル、回収・復旧、failure、LLM／機械境界、
security、Acceptance、現行実装との差分、実装順序、未決事項を分離している。

本変更は文書化だけであり、collector、cursor、reconciler、private verbatim artifact分離を実装していない。
scheduler、hook、watcherを有効化せず、保存場所またはretentionも決定していない。

## 2. Decisionと設計文書

| role | artifact | SHA-256 |
|---|---|---|
| approved design document | `docs/design/2026-08-03-session-transcript-eventual-preservation-design.md` | `b387b9cf913b11a0d39e13cbd5aa6222527fdb4f801e478f1110683c3dd8d1fe` |
| Human design direction Decision | `records/development/2026-08-03-session-transcript-eventual-preservation-decision.json` | `620fde82dc424141f4f5a9e8ce383fd9669506149e764eceebff0ada6addfcba` |

Decisionの`approved_document.sha256`は設計文書の実Digestと一致し、statusは
`approved_and_effective`である。authorityはeventual preservationの設計方向に限定され、実装、activation、
保存場所、retention、Work 4、commit、pushを承認しない。

## 3. 固定した設計境界

- periodic scanとstartup reconciliationをcorrectness pathとする。
- hookとfile watcherをlatency改善用の任意triggerとする。
- session完了判定を保存の必要条件にしない。
- raw commitよりcursorを先へ進めない。
- source短縮、途中置換、並べ替えでは既存rawを上書きしない。
- byte-exact raw、private verbatim transcript、redacted transcriptを別identityにする。
- source探索、offset、重複排除、Digest、保存、再生成、receiptを機械処理にする。
- LLMは保全済み内容の意味分析と説明だけを担当する。

## 4. 現行実装と追加が必要な部分

現行のsource adapter、discovery、prefix preservation、append-only update、atomic storage、regeneration、
scheduler、hookを再利用候補として列挙した。追加が必要な責務はdurable cursor、統一startup reconcile、
private verbatim transcriptとredacted派生物のartifact分離である。

これにより、既存のprovisional機能を「自動保全が完成・有効」と誤認せず、実装済みと未実装を区別した。

## 5. 機械検証

- Decision JSON：`python3 -m json.tool`で再読込成功
- 必須見出し：結論、保証、artifact、component、状態、回収、failure、責務境界、security、Acceptance、
  現行対応、未決事項を`rg`で確認
- 現行実装参照：8 pathすべて存在
- 差分検査：`git diff --check` finding 0
- 公式Test receipt：
  `records/development/2026-08-03-session-transcript-eventual-preservation-documentation-test-receipt-v1.json`
- receipt SHA-256：`e8c1cdcccf3887d55082e82359f2978a9b1ad7e9c0dc55e3185df1f4605a9d49`
- 公式Test：`477 passed in 2.42s`、exit code 0、fallback `false`

## 6. 問題、手戻り、機械化候補

本作業で失敗、手戻り、手入力転記訂正は発生しなかった。path存在、見出し、JSON、Digest、Testは機械処理で
確認した。新しい`manual_rework_candidate`または`manual_operation_candidate`はない。

## 7. 未実施

- collector／cursor／reconcilerのTask ContractとTDD実装
- private verbatim transcriptの独立保存
- 保存root、interval、capture deadline、retention、暗号化、accessのHuman判断
- scheduler、hook、watcher、background serviceのinstallまたはactivation
- current private sessionの取得またはcopy
- Work 4の開始、commit、push

以上により、eventual preservationの文書化を`verified / documentation_completed`とする。
