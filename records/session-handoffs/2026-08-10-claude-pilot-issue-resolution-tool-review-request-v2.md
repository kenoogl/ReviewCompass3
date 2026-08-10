# レビュー依頼 v2：V4 Issue resolve tool — IR-COMP-001〜003修正後の再レビュー

- 作成日：2026-08-10
- Pilot：Claude／Reviewer：Codex／Closer：Codex
- collaboration mode：`role_neutral_pilot_review`、risk：`high`
- 先行依頼書：v1（完了Claimは完了レビューv1によりstale。変更せず保持）

## 1. 経緯

完了レビューv1（`records/session-handoffs/2026-08-10-codex-review-result-issue-resolution-v4-v1.md`、
SHA-256 `94f3230526add0f20ad4166aafdee5d0c14c405a73dbff6ec0fd49707829b926`、
`report_execution_mismatch`・blocking 3件）に対し、Humanが裁定
（2026-08-10「IR-COMP-001と002の修正を承認する。IR-COMP-003は(a)scope改定とする」）。
scope v3（`records/session-handoffs/2026-08-10-claude-pilot-issue-resolution-tool-scope-v3.md`、
SHA-256 `24defe59bb1b299e41467abdb3e6edf143905b2c806bb221e06c71386e6f5ca4`）が
裁定と修復契約（裁定recordの構造化束縛・原子的書込みの無残留・実config読み取り専用
fixtureの正規化）を固定した。

## 2. 修正commit列（review request v1以後）

| SHA | 役割 | 内容 |
| --- | --- | --- |
| `fd2e09c` | Pilot | review request v1（先行） |
| `5be1d56` | Reviewer | 完了レビューv1 result record |
| `a873544` | Pilot | SCOPE v3：Human裁定・修復契約・fixture境界改定のみ |
| `4f39479` | Pilot | 修正RED：裁定fixture厳密形化＋束縛違反6態様＋障害注入2系統。実装前は新規8件のみ反証どおり失敗、先行16件合格、exit `1` |
| `9cef9ac` | Pilot | 修正GREEN：実装・Evidence修正節・receipt更新のみ。Testは修正RED以後未変更 |

本依頼書のcommit SHAは自己参照のため記載せず、Reviewerがgitから特定する。

## 3. Claim（修正分）

- **IR-COMP-001**：裁定recordを厳密形JSON（6 fieldちょうど）とし、
  `decision_maker=="human"`・human_id／decided_at（timestamp形式）のCLI一致・
  対象issue_id／遷移先の一致・wording非空をfail-closed検証。反証で使われた
  自動処理record・任意文字列・不正日時はすべて`human_ruling_invalid`で拒否。
- **IR-COMP-002**：全書込み（issue更新・復元・解決record）を一時file＋原子的置換へ。
  部分書込み障害の注入下でも、issue bytes不変（または完全復元）・解決record非存在・
  一時file残骸なしをTestで固定。
- **IR-COMP-003**：scope v3のHuman裁定によりfixture境界を改定（実configの読み取り専用
  利用を正規化）。Test変更は不要となった。
- **結果**：targeted 24 passed、関連回帰67 passed、公式全Test 1381 passed・status
  `passed`（receipt再読込みでfailed 0確認）、`git diff --check`指摘なし、worktree clean。
- **未実施**：実Issueのresolve、TODO・checklist反映（Closer）、schema・config・既存tool変更。

## 4. 成果物SHA-256（修正後）

| file | SHA-256 |
| --- | --- |
| `tools/development/issue_resolution_v4.py` | `770585427e6185730506ec6aa5da8004a79d77e2cee00e9b4210290d03a2bae8` |
| `tests/test_issue_resolution_v4.py`（24 Test） | `d1d09ab998ebed10a85a9f93613463ba756593052a214853d02b52aab749a4fb` |
| Evidence（§7修正節追記） | `35d38a4a4b80ef7e44aa92719f2b3fa3f3a24fe786b303077a09f9466c4dc525` |
| receipt（更新） | `1f351b652e45722c4c64932841baa6957caae3d421fb2c1b7a53e1ea7544d006` |

## 5. Reviewerへの確認観点

- 完了レビューv1の反証3系統（非Human裁定・issue側部分書込み・record側部分書込み）が
  不成立になること（前回のpath表現差異——`/var`と`/private/var`——のresolve()教訓を含む）
- 修正REDの失敗理由が反証そのものであること、既存Testを弱めていないこと
- scope v3の裁定転記がHuman文言と一致し、fixture境界の改定が正しく適用されていること
- targeted・関連回帰・公式全Testの独立再実行とDigest再計算
