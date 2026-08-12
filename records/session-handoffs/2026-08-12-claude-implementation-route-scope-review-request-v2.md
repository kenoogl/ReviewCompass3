# Claude実装委譲経路 第1縦切り 独立範囲レビュー依頼 v2

- 状態：`fixed_request`
- 対象commit：`67e37f0d72bbb36cc8d9d01ce419aff71530c5ca`
- レビュー担当：新しい会話状態の`gpt-5.6-terra`
- レビュー段階：`scope`
- 危険度：`high`
- 変更権限：なし
- 外部送信権限：なし

## 1. 固定対象

- 範囲固定：`records/session-handoffs/2026-08-12-claude-implementation-route-scope-v2.md`
- 範囲固定SHA-256：`9881f7df526c3aef8c21e665f75927329608d1b0518e343db0ac5c89f954a024`
- Human裁定：`records/session-handoffs/2026-08-12-claude-implementation-route-scope-finding-human-decision-v1.md`
- Human裁定SHA-256：`0565a68c8c9c363d3998f50225e78ff7b97aaff6b9e0e57662b8d48f05a71b37`
- 前周所見：`PA-CD-001`
- 前周レビュー：`records/session-handoffs/2026-08-12-claude-implementation-route-scope-review-result-v1.md`
- 選択裁定：`records/session-handoffs/2026-08-12-claude-implementation-route-selection-human-decision-v1.md`
- 上流文書：`docs/development/pilot-specific-claude-codex-collaboration.md`
- レビュー規則：`docs/development/work-review-protocol.md`

## 2. 判定対象

v1レビューは対象変更により古い状態なので、v2を独立に確認する。選択裁定、Human所見裁定、上流文書との
一致、Human承認境界、確認運転の送信範囲、読取・書込・Bash・ネットワークの境界、25要求と目的・順序・
変更範囲・出力の接続だけを確認する。

command option、fixture構成、保存形式の細部はblockingにしない。blockingはレビュー規則§11.1の4類型だけ
とする。独立反証は1件までとし、禁止操作またはHuman境界の迂回が範囲上合格し得るかを確認する。

## 3. 出力

最終応答は説明文なしの単一JSON objectとし、v1独立範囲レビュー依頼§3の構造に`round: 2`を加える。
`target_sha256`はv2のSHA-256、`reviewer_model`は`gpt-5.6-terra`とする。要求結果は25件を固定順で一度ずつ
列挙する。fileを変更せず、Claude、外部CLI、外部送信を起動しない。
