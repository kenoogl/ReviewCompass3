# レビュー依頼：V4 Issue resolve tool（deferred #1・案B）

- 作成日：2026-08-10
- Pilot：Claude／Reviewer：Codex／Closer：Codex
- collaboration mode：`role_neutral_pilot_review`、risk：`high`（Human確定済み）
- 受け渡し：`docs/development/pilot-driven-record-handoff.md`

## 1. 対象とHuman承認

- 有効scope：`records/session-handoffs/2026-08-10-claude-pilot-issue-resolution-tool-scope-v2.md`
  （SHA-256 `ddc4b312ca529f58c38f2ad90127e0ec5ef065b03ffb1af17c1b10076eff2ee7`）
- `high`範囲レビューv2：`verified`・blocking 0（commit `f7c2255`）
- Human承認（2026-08-10）：①「#1 risk highを確定。案Bでscope v2を承認する。遷移元は
  registeredのみとする」②「RED開始を承認する」

## 2. commit列（SCOPE v2以後）

| SHA | 役割 | 内容 |
| --- | --- | --- |
| `21daf5e` | Pilot | SCOPE v2のみ |
| `f7c2255` | Reviewer | `high`範囲レビューv2 record |
| `48bb6ad` | Pilot | RED：Test 16件のみ（486行）。単独実行で16件全てがModuleNotFoundErrorだけを理由に失敗、exit `1` |
| `380e501` | Pilot | GREEN：実装・Evidence・receiptのみ。Testは未変更 |

本依頼書のcommit SHAは自己参照のため記載せず、Reviewerがgitから特定する。

## 3. Claim

- **結果**：targeted 16 passed（exit `0`）、関連回帰67 passed（exit `0`）、公式全Test
  1373 passed・status `passed`（exit `0`、receipt再読込みでfailed 0確認）、
  `git diff --check`指摘なし、worktree clean。
- **実装の要点**：`registered`限定のin-place遷移（stateとdigestのみ更新、file名・
  issue_version不変）、事前・事後の正規検証（`validate_v4_issue_record`＋
  `validate_v4_issue_repository`）、事後失敗時の完全復元、Human根拠・Evidence参照の
  fail-closed検証、`records/development/`へのnew-only解決record。schema・config・
  既存tool不変。
- **fixture注記**：合成台帳はintake testの正規生成経路の再利用で構築し、configは
  repository committedの実configを**読み取り専用**で使用（既存intake testと同一
  pattern。scope文言の「合成config」に対する軽微な逸脱として明示する。台帳・裁定・
  Evidenceはすべて`tmp_path`内の合成）。
- **未実施**：実Issueのresolve実行（tool `verified`後にHuman裁定を得て別単位）、
  TODO・checklist反映（Closer）。

## 4. 成果物SHA-256

| file | SHA-256 |
| --- | --- |
| `tools/development/issue_resolution_v4.py` | `c4b5c57dcfe69b8ce87c370361171f8eaba664f38186f1fd3db54d43c6405216` |
| `tests/test_issue_resolution_v4.py` | `29be67ce761ad0449f1adc2ba5d58e8a9a1d27ebaade4b2d7a7c8c8586e2e4a6` |
| Evidence | `5c7130f8e3576123fc7be28c3e8aed054c45c3bafddc911be94c28e650f17ef8` |
| receipt | `a4887275f7074302b464020b171effdd1691d14011589cfea348588326341fe5` |

## 5. Reviewerへの確認観点

- scope v2受入条件11件と実装時確認事項3件のTest対応・独立再実行
- `high`のためPilot fixtureに無い反証を最低1件機械実行
  （推奨方向：非Human裁定での遷移、部分書込みの残留、`registered`以外からの遷移、
  台帳内の他recordへの影響、digest未更新のstate書換え、実configとの整合）
- fixture注記（実configの読み取り専用利用）の受容可否
- 既存Testを弱めていないこと、実台帳への非接触
