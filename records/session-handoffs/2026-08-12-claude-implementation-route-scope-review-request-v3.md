# Claude実装委譲経路 第1縦切り 独立範囲レビュー依頼 v3

- 状態：`fixed_request`
- 対象commit：`ecadd9b7cccb178e46265141c7983c2c7218927d`
- レビュー担当：新しい会話状態の`gpt-5.6-terra`
- レビュー段階：`scope`
- 危険度：`high`
- 変更権限：なし
- 外部送信権限：なし

## 1. 固定対象

- 範囲固定：`records/session-handoffs/2026-08-12-claude-implementation-route-scope-v3.md`
- 範囲固定SHA-256：`063d4299e78c11c2060b012ff7f09d7feaa2eca318e879e35bd418a7015e689f`
- 権限裁定：`records/session-handoffs/2026-08-12-claude-implementation-route-permission-finding-human-decision-v1.md`
- 権限裁定SHA-256：`49c705b5ddab15adc8b8dde2a2f402e6b4528301c8961f8e0cac26829490c106`
- RED開始裁定：`records/session-handoffs/2026-08-12-claude-implementation-route-red-start-human-decision-v1.md`
- 上流文書：`docs/development/pilot-specific-claude-codex-collaboration.md`
- レビュー規則：`docs/development/work-review-protocol.md`

## 2. 判定対象

v2の合格は対象変更により古い。v3について、Human裁定との一致、危険度、Human承認境界、合成repository限定、
読取・限定編集とcommand禁止、機械試験、25要求と目的・順序・変更範囲・出力の接続だけを確認する。

command option、fixture構成、保存形式の細部はblockingにしない。blockingはレビュー規則§11.1の4類型だけ
とする。独立反証は1件までとし、Claudeがcommandを使わずに禁止pathへ変更するか、Human承認なしに
後続へ進む例が範囲上合格し得るかを確認する。

## 3. 出力

最終応答は説明文なしの単一JSON objectとし、
`records/session-handoffs/2026-08-12-claude-implementation-route-scope-review-raw-v2.json`と同じ構造を使う。
`round`の代わりに`revalidation_cycle: 1`を持つ。`target_sha256`はv3のSHA-256、`reviewer_model`は
`gpt-5.6-terra`とする。要求結果は25件を固定順で一度ずつ列挙する。fileを変更せず、Claude、外部CLI、
外部送信を起動しない。
