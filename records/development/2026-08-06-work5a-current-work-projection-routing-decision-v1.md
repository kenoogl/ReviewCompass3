# Work 5A Current Work Projection後続route 案A承認Decision v1

- Decision ID：`DEC-WORK5A-PROJECTION-ROUTING-001`
- decision maker：Human
- decided at：`2026-08-06T08:27:31+09:00`
- decision：`approved`（案A）
- decision class：`route_decision`
- authority mode：`human`

## 承認対象

`docs/design/2026-08-06-work5a-current-work-projection-routing-proposal.md`の**案A**。

案Aの内容は次である。

1. Work 5Aの`bootstrap Current Work Projectionを正式recordへ写像する`項目と、
   `同じTestを変更せずgreenにし、refactor後も再確認する`項目を、必要な正式recordが揃うまで
   未完了のまま`deferred`に維持する。
2. defer理由、必要入力、再開条件をチェックリストとTODOへ記録する。
3. 次の実行工程を、Current Plan §17の初期実装順11に従いWork 6Aの中核negative pathとする。
4. Work 6Aでは、正式入力欠落、第二正本化、欠測推測、stale／競合の誤表示をRED fixtureとして
   先に固定する。正式projection本体を同時に発明しない。
5. 正式Portfolio／Work Item／Workflow stateの最小recordが承認された後にProjection写像を再開する。

## Human判断の経緯

2026-08-06、Codexから開発継続がClaudeへ委譲された。委譲指示は案Aの承認ではないため、
Claudeは固定Digest、Git、Test、TODO、チェックリストを照合したうえで、案Aの承認可否を
Humanへ一度だけ確認した。Humanは「承認」と回答した。

## 承認範囲

- 本Decision recordのnew-only作成。
- チェックリストWork 5A節への、Projection写像とrefactor後再確認のdefer理由・必要入力・
  再開条件の記録。checkboxは未完了のまま維持する。
- TODOを共通手順だけでWork 6A RED開始待ちへ更新すること。
- Work 6A項目と既存Testの対応を機械的にinventory化すること。
- 既存Testで被覆済みの負例を重複させず、未被覆の中核項目だけをRED testとして追加すること。
- 実装を変更せずREDであることを確認し、意味的に完結した単位でcommitすること。

## 非承認範囲

**この承認はGREEN実装の承認ではない。**

- Work 6AのGREEN実装。RED testの独立確認後に、GREEN実装範囲を別途Human判断で確定する。
- Current Work Projectionの正式写像、正式projection schema、UI、dashboard、automation。
- Portfolio／Work Item／汎用Workflow stateの先行実装。
- Work 4B、Work 5B、Work 7、Work 8。
- Contract、Requirement、Plan、Policyの変更。
- LLM reviewer、外部送信、push、PR、CI、不可逆操作。
- Work 5Aの段完了。二項目は未完了のまま残る。

GREENの意味範囲に新しいschema、state、authority、Contract変更が含まれる場合は、
実装前にHuman判断を得る。

## 再開条件（案A §5より）

Current Work Projectionの正式写像は、少なくとも次が固定された後に再開する。

- Stage／Work／Work Item identityとstate owner
- Plan、Portfolio、Work Item、Task Contractの型付きrelation
- dependency、cycle、pause／resume、termination、Human decision、staleの正式record
- 次の実行可能作業を導出するWorkflow規則
- 欠測、競合、stale、表示器failureを区別するnegative test

再開時もprojectionは派生viewとし、手編集可能な状態正本、独立status database、
UI固有authorityを作らない。

## 固定Evidence

| path | SHA-256 |
| --- | --- |
| `docs/design/2026-08-06-work5a-current-work-projection-routing-proposal.md` | `c061be7d5abd1f428497f59d2b4ccc352b699d657d038d11f1d359a76e587809` |
| `records/session-handoffs/2026-08-06-codex-to-claude-development-continuation.md` | `5d488a132777bf012bc433e7929c4db60c8a174077f543936b8d786f918f2563` |
| `records/development/2026-08-06-work5a-contract-v2-review-acceptance-records-v1.json` | `151c63c838850a3da319b5f1eaa8cf0d02379aed85b0a592f124e3624c275354` |
| `records/development/2026-08-06-work5a-contract-v2-review-acceptance-evidence-v1.md` | `3edf6f88bd85619c9e75868f066ddc1d0b66c41e842d27cd05abffac64d9bed5` |
| `records/development/2026-08-05-work5a-definition-challenge-first-run-records-v1.json` | `aace8f35b79cbe4e3113433b55e903e86e0171f04738b180e1728eb83bd93ca6` |
| `records/development/2026-08-05-work5a-definition-challenge-first-run-evidence-v1.md` | `ad7b82ae74cec8655c205191feb4bf89801353eb8c7838f239f8b1c7da4c6658` |

判断時点のGitとTestは、branch `main`、worktree clean、公式venv runnerの全Test`1007 passed`
（Python 3.9.6、pytest 8.4.2、fallback `false`）、Work 5A関連Test`83 passed`である。

## 既存recordへの影響

new-onlyで作成した。既存record、Contract、accepted artifact、Provenanceの上書き、削除、
無効化、stale化は行っていない。
