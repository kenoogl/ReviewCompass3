# レビュー依頼 v2：authority参照Digest検査器 — AR-P1-001修正後の再レビュー

- 作成日：2026-08-10
- Pilot：Claude／Reviewer：Codex／Closer：Codex
- collaboration mode：`role_neutral_pilot_review`、risk：`high`
- 先行依頼書：v1（SHA-256 `99569c2e7f786b4624f3aa4ba1f81e3fb93a1aa4b7100cfa24d3cb396dc1f308`。
  完了Claimは完了レビューv1によりstale。変更せず保持）

## 1. 経緯

完了レビューv1（`records/session-handoffs/2026-08-10-codex-review-result-authority-reference-checker-v1.md`、
判定`report_execution_mismatch`、AR-P1-001 blocking）に対し、Humanが修正を承認
（2026-08-10「AR-P1-001の修正を承認する」）。scope v2・allowlist・risk・他のHuman承認は不変。

## 2. 修正commit列（review request v1以後）

| SHA | 役割 | 内容 |
| --- | --- | --- |
| `929e662` | Pilot | review request v1（先行） |
| `56ad56c` | Reviewer | 完了レビューv1 result record |
| `2914e39` | Pilot | 修正RED：反証4変種のTestのみ追加（53行）。実装前は4件とも「合格してしまう」失敗、先行15件合格、exit `1` |
| `f07d94b` | Pilot | 修正GREEN：実装1箇所修正・Evidence修正節追記・receipt更新のみ。Testは修正RED以後未変更 |

本依頼書のcommit SHAは自己参照のため記載せず、Reviewerがgitから特定する。

## 3. Claim（修正分）

- **修正内容**：`_extract_references`で、許可key行のコロン後に空白以外の値がある場合は
  下位の参照対を解析せずinvalid（exit `5`）とする。宣言形の意味（mapping／mapping_listの
  形以外を受け付けない）をkey行にも適用した。
- **結果**：targeted 19 passed（exit `0`）、関連回帰21 passed（exit `0`）、公式全Test
  1357 passed・status `passed`（exit `0`、receipt再読込みでfailed 0確認）、
  `git diff --check`指摘なし、worktree clean。
- **未実施**：実docsへの適用・修復、Issue resolve、TODO・checklist反映（Closer）、
  allowlistの変更。

## 4. 成果物SHA-256（修正後）

| file | SHA-256 |
| --- | --- |
| `tools/development/authority_reference_checker.py` | `584c9669c5b0230f2fa460ce9d0b975d7c416371529cf6f6f2a9d2221ca8ffcf` |
| `tests/test_authority_reference_checker.py`（19 Test） | `ef97b9af746f5a60023476c900c1dffae2cca116885e8fbe1567fadd7158f350` |
| `tools/development/authority_reference_keys.json`（不変） | `560a835103765149f7e02b52876b6d2cec2e4817e7ec94c8ab1cfea85cd744b2` |
| Evidence（§7修正節追記） | `c8114e642ae1ba5c00eac9ef63f35737327e11a90b866e4dca499d855f4a2462` |
| receipt（更新） | `065f6260a0e810cdca27231833ece3fe60d4f18f5f2eb570105907df1e183fb5` |

## 5. Reviewerへの確認観点

- AR-P1-001の4反証（mapping：`unexpected`・`[]`／mapping_list：`unexpected`・`{}`）が
  不成立（exit `5`）になること
- 修正REDの失敗理由が反証そのもの（実装前は合格してしまう）であること、既存Testを
  弱めていないこと
- 実docs 2件（checklist・現行Plan）の読み取り確認が引き続き11 checked・11 matched・
  exit `0`であること（正常系の非退行）
- targeted・関連回帰・公式全Testの独立再実行とDigest再計算
