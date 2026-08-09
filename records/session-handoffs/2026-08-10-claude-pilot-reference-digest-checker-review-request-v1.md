# レビュー依頼：authority参照Digest検査器（deferred #5）

- 作成日：2026-08-10
- Pilot：Claude／Reviewer：Codex／Closer：Codex
- collaboration mode：`role_neutral_pilot_review`、risk：`high`（Human確定済み）
- 受け渡し：`docs/development/pilot-driven-record-handoff.md`

## 1. 対象とHuman承認

- 有効scope：`records/session-handoffs/2026-08-10-claude-pilot-reference-digest-checker-scope-v2.md`
  （SHA-256 `c37b7742a05592f514fac85f5bed606c8e396410a9df7deeac22a7afe46f9172`）
- 再範囲レビューv2：`verified`・blocking 0（commit `40ccd3b`）
- Human承認（2026-08-10）：①「#5 risk highを確定、7 key allowlist（authority_order,
  operational_policy, policy_decision, related_design, intent_ref, glossary_ref,
  reconciliation_ref）を承認、RED開始を承認する」②「RED訂正を承認する」

## 2. commit列（SCOPE v2以後）

| SHA | 役割 | 内容 |
| --- | --- | --- |
| `34f44da` | Pilot | SCOPE v2のみ |
| `40ccd3b` | Reviewer | 再範囲レビューv2 record |
| `c3bcb0f` | Pilot | RED：Test 15件のみ（455行）。単独実行で15件全てがModuleNotFoundErrorだけを理由に失敗、exit `1` |
| `6706cff` | Pilot | 訂正RED：fixture参照数の数え違い（10→11・9→10）の数値2箇所のみ。Human承認②に基づく。検査の緩和なし |
| `f61eeca` | Pilot | GREEN：検査器・allowlist宣言・Evidence・receiptのみ。Testは訂正RED以後未変更 |

本依頼書のcommit SHAは自己参照のため記載せず、Reviewerがgitから特定する。

## 3. Claim

- **結果**：targeted 15 passed（exit `0`）、関連回帰21 passed（exit `0`）、公式全Test
  1353 passed・status `passed`（exit `0`、receipt再読込みでfailed 0確認）、
  `git diff --check`指摘なし、worktree clean。
- **実装の要点**：allowlist宣言（7 key・期待形・承認情報）を唯一の判別規則とし、
  front matter限定・専用解析・fail-closed（不正形・空合格禁止・resolve後のroot外
  脱出拒否）・時点固定pin非対象・読み取り専用。
- **未実施**：実docsへの適用と不一致修復（別単位・Human指示待ち）、Issue stateの
  resolve（deferred #1の対象）、TODO・checklist反映（Closer）。

## 4. 成果物SHA-256

| file | SHA-256 |
| --- | --- |
| `tools/development/authority_reference_checker.py` | `8641ceb7fb615c217ff9d67fd15229409d6a30dd1fb3a443ce556a1425cb707f` |
| `tools/development/authority_reference_keys.json` | `560a835103765149f7e02b52876b6d2cec2e4817e7ec94c8ab1cfea85cd744b2` |
| `tests/test_authority_reference_checker.py` | `b6edd8ce4f9c598a8240eb7562fccdeb267404ba961fcd341f8813c6241e398c` |
| Evidence | `0a4211136354e51f7b293f843046c32f8a699d4ece9d2365da5c068ee3859724` |
| receipt | `5de14a42510d26721327db1b610b2b0c9c66cff4ea2ed5c67a09cbb497a0f518` |

## 5. Reviewerへの確認観点

- scope v2受入条件13件と実装時確認事項2件のTest対応・独立再実行
- allowlist宣言がHuman承認内容（7 key）と一致し、宣言だけが対象を決めること
- `high`のためPilot fixtureに無い反証を最低1件機械実行
  （優先：allowlist key内のずれ見逃し方向、時点固定pinの誤拒否方向、実docs形式での挙動）
- 訂正REDが検査を弱めていないこと（数値2箇所のみ）
