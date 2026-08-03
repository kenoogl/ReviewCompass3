---
evidence_id: RC3-SESSION-TRANSCRIPT-EVENTUAL-PRESERVATION-COMPLETION-2026-08-04-V1
recorded_at: 2026-08-04T00:54:45+09:00
status: verified_completed
workflow_state: completed
confidentiality_class: project-internal
---

# Session Transcript Eventual Preservation Completion Evidence V1

## 1. 結果

Humanが選択した`option_1_os_standard_limited_pilot`に従い、OS標準のrepository外private data境界へ、
現在のCodex Desktop taskで保存時点までに利用可能だったrollout 1件を限定保存した。初回は`created`、同じ
入力を同一process内で直ちに再実行した結果は`unchanged`であり、重複保存は発生しなかった。

これによりTask Contract
`TC-SESSION-TRANSCRIPT-EVENTUAL-PRESERVATION-2026-08-03-V1`の実装、fixture検証、Human storage判断、
限定実ログ保存、事後照合を満たした。元のTask Contract recordは固定入力として変更せず、本Evidenceをclosureとする。

## 2. Human Decision

| role | artifact | SHA-256 |
|---|---|---|
| Storage Candidate | `records/development/2026-08-04-session-transcript-eventual-preservation-storage-candidate-v1.json` | `0c712308275cd321870fe2c203b0b53207bc817108a9fba3910da6ee730a5fdc` |
| Human storage Decision | `records/development/2026-08-04-session-transcript-eventual-preservation-storage-decision.json` | `79c9e7aa781d09cb4afe477919889e12583ae1d8e57b15317046cff5c1e74953` |

Human入力は`1`であり、現在のCodex Desktop task 1件、byte-exact raw、private verbatim、durable cursor、
private Provenance、integrity ledgerだけを承認対象とした。過去Codex履歴、Claude、redacted transcript、外部送信、
hook、watcher、scheduler、background service、Git保存は対象外である。

## 3. 限定captureの事後状態

- Receipt：
  `records/development/2026-08-04-session-transcript-eventual-preservation-limited-capture-receipt-v1.json`
- Receipt SHA-256：`ef351d6a7e9754d5206a5a5183d8e2230bd90c156d9763473985331e3cb5f77e`
- source kind：`codex_rollout`
- source identity：`619ff2b0e985199b0006a7166f12ed4b2af26c291ecb1662a9d41d093ac023df`
- 保存時event：2595、parse issue：0
- 保存raw：19,305,386 bytes、parsed：19,305,386 bytes
- 初回action：`created`
- 同一即時再実行：`unchanged`

private transcript本文とabsolute pathはreceiptまたは本Evidenceへ記録していない。会話中もsource本文は表示していない。

## 4. 完全性と境界

機械検証で次を確認した。

- 保存rawは元sourceの保存時点prefixとbyte単位で一致する。
- raw Digestはcursorと一致し、verbatim Digestもcursorと一致する。
- cursorとProvenanceのartifact、parse、raw、source recordが一致する。
- raw、private verbatim、cursor、private Provenance、ledgerの5 fileを作成した。
- redacted transcriptは作成していない。
- private rootはrepository外で、全directoryは`0700`、全fileは`0600`である。
- temporary fileまたはlock fileの残留は0件である。
- private artifactをGitへ追加していない。

capture後もDesktop taskは継続するため、provider sourceは保存prefixより後ろへ追記される。これはdivergenceではなく、
次のmanual reconcileで純粋追記として回収できる設計である。本限定pilotはcapture時点prefixの保存を完了条件とする。

## 5. Test

- Completion Test receipt：
  `records/development/2026-08-04-session-transcript-eventual-preservation-completion-test-receipt-v1.json`
- Receipt SHA-256：`b0d1dcae931c941949d90c477e15d40ef027096d125345b2963c105f0674d76a`
- 公式全Test：`490 passed in 2.54s`
- exit code：0
- fallback：`false`

## 6. 問題、処置、機械化候補

- capture、Digest、permission、prefix照合、Testでは問題は発生しなかった。
- 補助検索commandの検索語に含めたbacktickをshellが解釈し、一部検索だけが1回失敗した。成果物、capture、
  Testへの影響はない。期待executorは引数を構造化して渡す`machine`、実executorはLLMによるshell文字列の
  直接組立てだった。引用を修正して必要な検索を再実行した。機械処理候補はshellを経由しないargv実行または
  composition lint、routeは`manual_operation_candidate / checkpoint`とする。

## 7. 未実施と後続判断

- 自動起動、hook、watcher、scheduler、background service
- 過去Codex履歴またはClaude logの一括capture
- application-layer暗号化、backup、長期retention、削除
- 2026-09-03のretention review
- commit、push、Work 4開始

以上により、本Task Contractを`verified_completed`とし、inter-work correctiveを閉じる。次の開発工程は
初期開発checklistのWork 4である。
