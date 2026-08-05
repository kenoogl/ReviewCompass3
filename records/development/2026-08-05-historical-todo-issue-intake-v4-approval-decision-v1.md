# Issue Intake V4 承認Decision v1

- decision ID：`DEC-HISTORICAL-TODO-ISSUE-INTAKE-001`
- decision maker：Human
- decided at：2026-08-05
- 対象設計：`docs/design/2026-08-05-historical-todo-issue-intake-proposal.md`
- 改善候補：`IC-HISTORICAL-TODO-ISSUE-INTAKE-001`
- 指示：`records/session-handoffs/2026-08-05-codex-to-claude-approve-and-close-v4-issue-intake.md`

## 1. 承認の効力

HumanはIssue Intake V4を、**開発用・暫定（development-only provisional）の限定機能**として使用することを
承認した。具体的に許可するのは次である。

- 複数の`registered` Issueを同時に保持すること。登録済みIssue数に上限を置かない。
- 作業中（`in_progress`）のIssueを最大1件に制限すること。
- Humanのtriage判断recordを正本とし、その判断に基づいてのみ候補を正式Issueへ昇格すること。
- 候補bundleを機械抽出時の観測として保持し、`human_fields`を書き換えないこと。

`pilot_mode`は`development_only_provisional`のまま維持する。

## 2. 承認対象と実際のDigest

### 設計・config・validator・test

| path | SHA-256 |
| --- | --- |
| `docs/design/2026-08-05-historical-todo-issue-intake-proposal.md` | `8475cd94b449e0709eb97e6d487b86cceef86e0307b3bbb7e78351d8f43147a9` |
| `config/development-issue-resolution-pilot-v4.json` | `ed274e487318d44baed701ffbc8a1130df3e9d81cadca96515848a2bea228a8e` |
| `tools/development/issue_intake_v4.py` | `7a1d557e82acd6554c3e137345f02ba476cbf448184a9a0348dca6beec26e27a` |
| `tests/test_issue_intake_v4.py` | `0d9b3f0356294cf83cc80848675c1eb7e2d602afebd3f44b21109bcb58493bbd` |

### GREEN Evidence

| path | SHA-256 |
| --- | --- |
| `records/development/2026-08-05-issue-intake-v4-green-evidence-v1.md` | `28809b220e8e5b16f3f643c8994ea9bdeb73ac83d3e506daaea6baceb751e75f` |
| `records/development/2026-08-05-v4-human-triage-persistence-green-evidence-v1.md` | `41fcbbbd6acc278055dd3e43e64fcb0c603627319eae1fb13b853262bda305d7` |
| `records/development/2026-08-05-v4-issue-persistence-green-evidence-v1.md` | `3ae17b4b5828429ee8c7f1b6dfbc3b80d9439da4bace685542cee3845640b731` |

### 候補bundle

| path | SHA-256 |
| --- | --- |
| `records/development/2026-08-05-historical-todo-intake-candidates-v1.json` | `e01c0feb082712f8ef0f77bfa4f031fbdc4530ed51f331f7dafbfd133d479a3e` |

候補数は41件、`human_fields`は全件`null`、`promotion_status`は`none`である。

### V4 Human triage decision（41件）

保存先：`.reviewcompass/workflow/triage-decisions-v4/`

| decision ID | candidate ID | disposition | file SHA-256 |
| --- | --- | --- | --- |
| `DEC-HTC-045A8FB5` | `HTC-045A8FB5` | `historical_completed` | `18b70725b3d007216cc9d321e71d45b3cc07e686c5c6a6097ca9973ec19d88d0` |
| `DEC-HTC-094589CA` | `HTC-094589CA` | `reject` | `a2cb341e0aec3ac92d51d7e62bda70fb9ddd506be2bc8f0bdcf9442704065881` |
| `DEC-HTC-14D810C7` | `HTC-14D810C7` | `historical_completed` | `022d3e25ffb3dd991cf4add659b8baf6e8a26960820a189e5c8f96343d0c3b07` |
| `DEC-HTC-152E0FB3` | `HTC-152E0FB3` | `reject` | `131c4d26062b5c32e72615181b1fc6abb04dd1ca8558620df1ca8953645e7be5` |
| `DEC-HTC-186E9B83` | `HTC-186E9B83` | `defer` | `94c102c1313f21e799df8e4bca992663238b605c561c75869a55a3024d0aff62` |
| `DEC-HTC-1AB699F7` | `HTC-1AB699F7` | `historical_completed` | `841139138a4216e5500801ebe8a8cf804d5bd956edb1eb416ae16119f3f327a1` |
| `DEC-HTC-1D5B5102` | `HTC-1D5B5102` | `historical_completed` | `190305f4a05f33c453ac4df6e707d5435497ab7cef496a5491b04948e4a009d5` |
| `DEC-HTC-21C3CE46` | `HTC-21C3CE46` | `historical_completed` | `3a78429b82fccfa20f11dfaa1c05e6f07b5795cb7c6c0812ab924734b483c9f4` |
| `DEC-HTC-243BE1FF` | `HTC-243BE1FF` | `dependency` | `8390aeb5918d6c9a752940dd0d697ae0627304b66bd59e9186cddc3a8ada6e21` |
| `DEC-HTC-328144E4` | `HTC-328144E4` | `defer` | `5b336873368cf264477912aeffdcdbadcf5eef725c5c85fe9638edd2b1a6c951` |
| `DEC-HTC-3AFBA652` | `HTC-3AFBA652` | `historical_completed` | `8026c52517ae6d7b62be99383977da51e37ec5d2f4ef0d1196ecaf8f1abecc8e` |
| `DEC-HTC-45B611EF` | `HTC-45B611EF` | `defer` | `271ea7bb6a13fecb94e65f164cb9950458a6cfad6b85483df64213bd7d032ddf` |
| `DEC-HTC-477EA1A4` | `HTC-477EA1A4` | `defer` | `9e4d76f2e791deaa8c8bfd5fbb97e2ff01aff4449828a01d439e29cac3498d78` |
| `DEC-HTC-49795CC0` | `HTC-49795CC0` | `reject` | `54464f901b101e75f69f31107a756cabb21792106bdebf229f3c6f72ca23cd61` |
| `DEC-HTC-4ED2C5B1` | `HTC-4ED2C5B1` | `dependency` | `5df48b31a0e9fca0ee3daf6d3f49275c14cc98c9485295af579907d40c0697dc` |
| `DEC-HTC-5C059B48` | `HTC-5C059B48` | `historical_completed` | `21904aac89129266b3a0b0bc06bdc99063a0fcc959588bc3b65e588ee6c3bc39` |
| `DEC-HTC-62719E1C` | `HTC-62719E1C` | `reject` | `5b4f09f9a85d67795839860347fecdc65380f8ff043f19782b34735ddf35479b` |
| `DEC-HTC-66C3E6CA` | `HTC-66C3E6CA` | `issue_resolution` | `bb2cfbb618f5b1ee918018a1ae4ae78d74a25eccb26a7cd46e07685571c31e5f` |
| `DEC-HTC-6ABDDC35` | `HTC-6ABDDC35` | `historical_completed` | `6c6320b220f72a49462e492e09c58b568b6b129693e95d2e435943e9932fc67d` |
| `DEC-HTC-7071DD99` | `HTC-7071DD99` | `reject` | `d2dfcede969732f35b25b700a4cb82344d26a45e7cbf034a2e124d2a16294587` |
| `DEC-HTC-75C717E1` | `HTC-75C717E1` | `historical_completed` | `d936213147b2cc2a2f0c0f5cd1fba9d9d89a3d3e740b390db74bca0ef08fac97` |
| `DEC-HTC-7DDF463E` | `HTC-7DDF463E` | `reject` | `8a804f272a9c864c8328090f148724b071640372b2e21e542cd62156af111012` |
| `DEC-HTC-876989C2` | `HTC-876989C2` | `reject` | `5cbb32ff1567134d5248822ce50f3271cf3de9ad200aee6c420bf19c958a8dc4` |
| `DEC-HTC-8AEF6A5F` | `HTC-8AEF6A5F` | `reject` | `8de4549b8b3d21feed86981d0cc45c06b48d7993f0197845ff6fb8b83e986f9a` |
| `DEC-HTC-9DCE8503` | `HTC-9DCE8503` | `defer` | `8088e41b42a2e59b78bcb5717c9328c6e0a0eb0f50914efb518097c65844c606` |
| `DEC-HTC-A5D1BCCA` | `HTC-A5D1BCCA` | `defer` | `5f8c771d6bf70b834e759b4c960debee7279906f2673090d16534e75f218628f` |
| `DEC-HTC-ABE70CFC` | `HTC-ABE70CFC` | `reject` | `68d2ba601462332da8a82e2373d695445bb5dff18fd808fff525a79070d1ba1b` |
| `DEC-HTC-B53A2670` | `HTC-B53A2670` | `reject` | `6414bdf04f0306961d23a3cf31719f0da9282386027fcdafb3a0cf752d0dc95e` |
| `DEC-HTC-BE5E1F67` | `HTC-BE5E1F67` | `historical_completed` | `b3af147c2c01e4aca5f9b9a705a875a05336927a0e582e10bb2d4e965ab42d24` |
| `DEC-HTC-BEB5E0BD` | `HTC-BEB5E0BD` | `issue_resolution` | `ac95dcdd4cb9064418dc3a386ccf834730d43059952194f9b055cd893227e133` |
| `DEC-HTC-C05BE65C` | `HTC-C05BE65C` | `reject` | `0aa55a118cbc2aaed1257ac545c869690525fbe44692ee200c56805666707ebf` |
| `DEC-HTC-C2E642ED` | `HTC-C2E642ED` | `defer` | `72285ca2a23dbbeb0b7fc253efb5e84b837634bf75c5a4cc5fb16f8fd6d1eda8` |
| `DEC-HTC-C3193ABF` | `HTC-C3193ABF` | `reject` | `a4d23319b4d2820fad76bcea3844f6b36c74526c802efa1cefc7061af90c19d5` |
| `DEC-HTC-C9F6C917` | `HTC-C9F6C917` | `issue_resolution` | `5b698bd0e9069128710bef161e3d60475002c89c4a4b70cce015a39c31bbf444` |
| `DEC-HTC-CD984CD0` | `HTC-CD984CD0` | `dependency` | `83757b19d71a6ce4f76ea3e1e7fdab6c170b6b6d64f82aa38d5f3cfcd785d70e` |
| `DEC-HTC-D34A113E` | `HTC-D34A113E` | `defer` | `cb482b7bb9e18050472ea766ac7c4143e42cf9ba75d8f6a5c2d3e40988d0242e` |
| `DEC-HTC-D65B4A8E` | `HTC-D65B4A8E` | `defer` | `00041dcebed4f0bc58b5b01fc98118cb970b5e8f0eeec2fe513135dc9f874790` |
| `DEC-HTC-D7E1F8C3` | `HTC-D7E1F8C3` | `defer` | `75a07e0b0dc0279c477c4abd5be44d2e9947cc7bc5956bea2093b4ccb1e88ff3` |
| `DEC-HTC-E183A02B` | `HTC-E183A02B` | `historical_completed` | `aef6b74e60e9ff3e324a0676281a711df7d0481fd8f1e8761a1197c3c060e452` |
| `DEC-HTC-E7E2F692` | `HTC-E7E2F692` | `historical_completed` | `5190ed493715dfffa236b8ed5c150b24891c42cd3f9f405999a2769bab9777a0` |
| `DEC-HTC-ECE89CA2` | `HTC-ECE89CA2` | `reject` | `65407685f051bd9a8544be62d5c7aff4689fe9fbfac6abdb9b1d29e04ba1acf6` |

disposition別の内訳：

| disposition | 件数 |
| --- | --- |
| `defer` | 10 |
| `dependency` | 3 |
| `historical_completed` | 12 |
| `issue_resolution` | 3 |
| `reject` | 13 |

### V4 Issue（3件）

| issue ID | state | path | file SHA-256 |
| --- | --- | --- | --- |
| `ISSUE-HTC-66C3E6CA` | `registered` | `.reviewcompass/workflow/issues-v4/issue-htc-66c3e6ca--v1.json` | `56e0911d6f565915ca0ad7737eae7befbb30d686d344eb5367ecc95598a8c732` |
| `ISSUE-HTC-BEB5E0BD` | `registered` | `.reviewcompass/workflow/issues-v4/issue-htc-beb5e0bd--v1.json` | `a4a1511e609005193a3d127080a3eabf4f56a67529c5bd9b4e0f55b467422d62` |
| `ISSUE-HTC-C9F6C917` | `registered` | `.reviewcompass/workflow/issues-v4/issue-htc-c9f6c917--v1.json` | `66cfe50ce79136bca5e92b35b72502cedfb8b6f6f3e20ade1e027bcbf1fec0ed` |

## 3. 明示的な対象外

次はこの承認に含まれない。開始しない。

- 上記3正式IssueのPlan化と実装
- 正式製品schema、UI
- hook、watcher、scheduler、background service
- automation全般
- Work 8評価
- 外部送信

## 4. 参照

- 閉鎖Evidence：`records/development/2026-08-05-historical-todo-issue-intake-v4-closure-evidence-v1.md`
- 全test receipt：`records/development/2026-08-05-historical-todo-issue-intake-v4-closure-test-receipt-v1.json`
