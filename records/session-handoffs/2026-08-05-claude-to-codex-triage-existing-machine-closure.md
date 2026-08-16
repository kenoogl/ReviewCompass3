# Claude → Codex：既存機械対策で閉じた5候補のHuman triage記録 完了報告

指示：`records/session-handoffs/2026-08-05-codex-to-claude-triage-existing-machine-closure.md`

指示の実施範囲をすべて完了した。作成したのは5件のdecision record、test receipt、TODO更新だけである。
正式Issue、Plan、Work、実装は作成していない。

## commit

- commit SHA：`28d2b1da13db0d78570e51161b8a820378aed7bd`
- 内容：decision record 5件、TODO更新、作成後の全test receipt 1件（計7file、185行追加・6行削除）
- `git diff --check`：stage前後とも合格
- commit後の追跡fileのworktree：clean（未追跡のまま残るのは、commitへ混ぜないsession-handoffsの
  完了報告9件のみ。本報告を含む）

## 5 decision ID

保存先：`.reviewcompass/workflow/triage-decisions-v4/`、schema version 2、`decision_version: 1`、
`decided_at: 2026-08-05T13:56:32+09:00`（5件共通）。

| decision ID | candidate ID | file SHA-256 | content digest |
| --- | --- | --- | --- |
| `DEC-HTC-3AFBA652` | `HTC-3AFBA652` | `8026c52517ae6d7b62be99383977da51e37ec5d2f4ef0d1196ecaf8f1abecc8e` | `dd7ca5b03704a8242afdd855135e032e4d82c9bebcd4bbe2842ee1c645dde3fb` |
| `DEC-HTC-75C717E1` | `HTC-75C717E1` | `d936213147b2cc2a2f0c0f5cd1fba9d9d89a3d3e740b390db74bca0ef08fac97` | `443e9159b888a6eca9ed9f8886d3085cd604a01a28092b0138b9efce5c309438` |
| `DEC-HTC-E7E2F692` | `HTC-E7E2F692` | `5190ed493715dfffa236b8ed5c150b24891c42cd3f9f405999a2769bab9777a0` | `478af37128fd56dc014824b0f65ac496bc7233222a5118c837c613e48e98e25c` |
| `DEC-HTC-5C059B48` | `HTC-5C059B48` | `21904aac89129266b3a0b0bc06bdc99063a0fcc959588bc3b65e588ee6c3bc39` | `cde696f90bb3985f1af3d8a92d861c0bfaccedaa5175ad2731481ee1b85e8ff5` |
| `DEC-HTC-E183A02B` | `HTC-E183A02B` | `aef6b74e60e9ff3e324a0676281a711df7d0481fd8f1e8761a1197c3c060e452` | `f1a99f24ad47f056c96829435589252a61c5464e8dc1692331bcf2515febcb48` |

5件とも指示どおり次の値である（機械確認済み）。

- `unresolved: false`、`recurrence: false`、`impact: not_applicable`、`priority: not_applicable`、
  `promote_to_issue: false`
- `disposition: historical_completed`、`blocking: false`
- `issue_promotion: {"approved": false, "issue_id": null}`
- `supersedes: null`

`rationale`には、何が既存の機械対策で閉じているのかを候補ごとに平易に記した。

- `HTC-3AFBA652`：既存の共通読み取り関数`resolve_effective_requirement_ids()`へ切り替えて合格している。
- `HTC-75C717E1`：既存の公式Testが回帰を検出し、既存の契約へ復旧している。
- `HTC-E7E2F692`：その回の文書化で手戻り・転記訂正・失敗が発生しておらず、追跡すべき問題を含まない。
- `HTC-5C059B48`：commit前に安定した引き継ぎ内容を検査するvalidatorで恒久対策済みである。
- `HTC-E183A02B`：既存の単一subject Testが誤配置を検出し、版付きの正しい経路へ修正している。

あわせて5件とも、次の趣旨を明記した。

> ここでの`historical_completed`は、経緯やEvidenceを捨てるという意味ではない。既存の機械検査または
> 恒久対策ですでに閉じており、現在の独立したIssueとしては追跡しない、という意味である。
> 元のPlan、Decision、Evidence、code、testは変更しない。

`next_action`は5件とも「候補bundleを変更せず、この判断recordを既存の機械対策で閉じた記録として
保持する。正式Issue、Plan、Workは作らない。」とした。

## 検証結果

1. **record単体検証**：5件とも`validate_human_triage_decision()`に合格した。bundleの相対pathと
   SHA-256、候補IDとcontent digest、decisionのpathとcontent digestをすべて再確認している。
2. **decision集合検証**：`validate_triage_decision_repository()`が有効decision 22件を返し、競合は無い。
   V4 decision directoryのfile数も22件で一致する。
3. **V4 Issue集合検証**：`validate_v4_issue_repository()`の結果は2件で、いずれも`registered`である。

## 候補bundle不変確認

- SHA-256は`e01c0feb082712f8ef0f77bfa4f031fbdc4530ed51f331f7dafbfd133d479a3e`のまま変わらない。
- 候補41件すべての`human_fields`は`null`のままである。
- Git履歴上、bundle fileを変更したcommitは生成時の`3ef8759`だけである。

## V4 Issue数とactive Issue数

- V4 Issueは2件：`ISSUE-HTC-BEB5E0BD`と`ISSUE-HTC-C9F6C917`。いずれも`state: registered`、
  参照decisionは`blocking: false`。
- active Issue数は0。
- `.reviewcompass/workflow/issues-v4/`のGit履歴の最新commitは`b6ac2c8`のままで、今回のcommitは
  触れていない。新しい正式Issueは作っていない。

## 全test結果

公式Test runner（`tools/development/policy_test_runner.py`、suite `full`。実コマンドは
`.venv/bin/python3 -m pytest -q`、Python 3.9.6、pytest 8.4.2、fallback false）で実行した。

- receipt：`records/development/2026-08-05-triage-existing-machine-closure-test-receipt-v1.json`
  （SHA-256 `e353c4772f0c1d3b9d79571384713bc9053ffea7e93902e2ac5fc8081866561e`）
- status：`passed`、exit code：`0`、結果：`815 passed`

TODOの最終更新後にも全testを再実行し、`815 passed`を確認した（このrunはreceiptを上書きしないため、
receiptは上記1件のままである）。TODOの参照digest27件はすべて一致し、commit安定Git節も合格。
8,777 bytesで上限内。active ID projectionは`ISSUE-PILOT-TODO-GROWTH-001`の1件のままである。

## TODO更新

現在位置だけを更新した。判断済み22件、残り19件、正式Issue2件、active Issue 0件、
`ISSUE-HTC-BEB5E0BD`と`ISSUE-HTC-C9F6C917`はともに`registered`かつnonblocking、
次の一作業は残り19候補のHuman triage、と記載した。全test receiptへのlinkとdigestも今回のものへ
差し替えた。詳細は再累積していない。

## 未実施事項（指示どおり行っていないこと）

- 正式Issue、Plan、Work、実装の作成：行っていない。
- 残る19候補の判断：行っていない。
- 既存17 decision、既存2 Issue、候補bundle、Plan、Decision、Evidence、code、test、configの変更：
  行っていない。今回のcommitに含まれるのはdecision record 5件、TODO、receiptだけである。
- push、PR、外部送信、Work 4B、Work 6A、E2以降：開始していない。
- 本完了報告はcommitに混ぜていない。
