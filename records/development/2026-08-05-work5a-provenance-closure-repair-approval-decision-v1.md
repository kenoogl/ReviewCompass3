# DEC-WORK5A-PROVENANCE-CLOSURE-REPAIR-001

## Decision

Humanは2026-08-05に`docs/design/2026-08-05-work5a-provenance-closure-repair-proposal.md`を承認し、
§6.3の**案A**を選んだ。

> 案Aで承認

案Aは、既存の`human_decision` version 1（`HD-TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V1`、
Digest `a240921a70a40837efa2d45ee83def0059c125a2a343b7eb415841ddce65d8af`）を
そのまま新しい`provenance_verdict`のnodeとして参照する方式である。
新しい`human_decision` recordを作らない。Humanの判断は一度であり、その事実を保つ。

## 承認範囲

- 循環除去設計。`provenance_verdict`自身を端点とするedgeを、そのrecord内容へ含めない。
  閉包は下流の`accepted_artifact`が担う。
- `verified_nodes`（9件）と`verified_edges`（8件）による構造。edgeの両端は`node_role`で指し、
  identity・version・Digestは`verified_nodes`が一元的に持つ。
- 検証規則V1〜V10のfail-closed。辺数だけで`verified`を発行しない。
- §6.3の案A。既存`human_decision` version 1をそのまま使う。
- 後続の作業単位。誤記録の無効化、RED test、実装、GREEN、正しい受理recordの再作成、独立検証。

## 無効化の範囲

`9e8cf00`に含まれる次の二recordだけを`invalidated_not_authoritative`とする。

| record kind | record ID | version | content digest |
| --- | --- | --- | --- |
| `provenance_verdict` | `PV-TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V1` | 1 | `7975c7619dbca8c95fd249303dba47e46e0d8ec681e386866e1dddfbfa38aae0` |
| `accepted_artifact` | `AA-CM-TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V1` | 1 | `6c4c690a39bbf0b1a845432e8dfe6c8f155598927e74e92d51a51eb28c7d9d4c` |

既存`human_decision`と上流9 recordは無効化しない。これらに不整合は無い。
**Humanの承認判断そのものは有効であり、失われていない。**

## 禁止事項

- `9e8cf00`のrevert、history rewrite、既存recordの削除・上書き。
- 旧形式のprovenance edgeを互換入力として受理すること。旧形式は拒否fixtureとしてだけ使う。
- 設計提案、review対象文書、Requirement、Current Plan、checklistの変更。
- LLM、外部送信、外部`DATA_ROOT`、push、PR、CI、Work 4B、Work 6A、後続評価E2以降。

## 根拠

- Human approval：2026-08-05。対象は
  `docs/design/2026-08-05-work5a-provenance-closure-repair-proposal.md`、選択は§6.3案A。
  実装範囲の固定は
  `records/session-handoffs/2026-08-05-codex-to-claude-work5a-provenance-closure-repair-implementation.md`。
- 不整合の発見：Codexの独立照合。
- 先行Decision：`DEC-WORK4-FIRST-REVIEW-CONTRACT-DESIGN-001`
