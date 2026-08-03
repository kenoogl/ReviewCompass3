# Work 3 Deferred Scope Audit Evidence V1

## Identity

- Evidence ID：`RC3-WORK3-DEFERRED-SCOPE-EVIDENCE-2026-08-03-V1`
- recorded at：`2026-08-03T21:12:12+09:00`
- stage／work：`initial-development / Work 3`
- status：`verified / human_decision_pending`

## Candidate

- path：`records/development/2026-08-03-work-3-deferred-scope-candidate-v1.json`
- file SHA-256：`01da1ea0c6c4f6adad8fdcd09085f97b387ea4639d01b0811b80dc5957916210`
- candidate digest：`8993a6e4671679ab8cfe665322efdaf862cf085a8f1fab7d500d15f5fd7deb84`
- authority：`proposed_only`
- approved effect：13候補のowner、成果、論理配置、有効化条件、初期非依存境界、scope leak監査規則を
  Work 3の設計入力として固定する。各能力の実装、有効化、Requirement／Plan変更は行わない。

## Fixed Sources

- 50 Requirement authority bundle：
  `records/requirements/authority/rc3-requirements-authority-2026-08-03--v1.json`
  - file SHA-256：`fc6d945a6bef1ebea0c4ef22705d70fac6177a8c561be0f992ca94474a8a7509`
  - bundle digest：`497bcc4374e3224acbfbb08e38c7d9f3d4e5373f59df505179b6a19bc035a02c`
- current Plan：`docs/current/reviewcompass3-plan-current.md`
  - SHA-256：`0ae6bef979192b008a8a71fc090f709279c4bd1f0db159f9faadf947e929156f`
- `REQ-CONTRACT-008` definition：
  `records/requirements/definitions/req-contract-008--v1.json`
  - file SHA-256：`8667ebfa669112c7a9045257795428a0fc4a832eb5c530257aa155e08a51eab2`
  - canonical payload digest：`efa3bd0f5b637b286af6dfb6e751bcf00e3a31a937613393557308c5b574f0c0`
- 承認済みNFR Profile candidate／Decision／completion Evidence：
  - candidate SHA-256：`08d5159a483d16507c5652857e5245993b42559ed3bcc24c9434e70b0d5c2381`
  - Decision SHA-256：`6cdb1f74c8b92bcc7257bf8087158f78e8c980428d1b0fa725a20e2dd8e96373`
  - completion Evidence SHA-256：`c8c99ca93d9eb29c112febbc18fa53fbf5476d703399a07888b7733cb9fb379f`

固定sourceのfile Digestとlogical Digestは再読込時に全件一致した。

## Audit Semantics

`scope_leak`は、deferred成果を初期Requirement、Profile、Contract、Test、Workまたはreleaseの無条件な
必須入力、受入条件、実行能力、authorityにすることとした。次は暗黙依存ではなく、許可する将来互換境界である。

- 将来用identity／relationの保持
- inactiveなDeferred Acceptance
- 手作業またはshadow観測
- 現行profileでの明示的`not_applicable`
- 未実施または不成立が初期releaseをblockしない条件付きPilot

能力固有の停止条件は、その能力を別Task Contractでcurrent scopeへ入れた後だけ有効にする。

## Deferred Inventory

- 総数：13
- `explicit_deferred`：9
- `conditional_pilot`：2
- `not_adopted_without_new_evidence`：2
- ID重複：0
- owner、成果、論理配置、有効化条件、初期scope規則の欠落：0
- 未知Requirement参照：0
- 未知NFR Profile参照：0
- 初期release blocker：0

13件は次の境界へ分離した。

1. As-Built projection
2. AI decision delegation
3. shared／distributed deployment
4. Issue Resolution automation
5. improvement automation
6. `bounded_parallel` conditional Pilot
7. generic orchestration／plugin
8. Current Work UI
9. advanced semantic search
10. terminology runtime
11. report Claim automation
12. external portability conditional Pilot
13. CI provider mutation

`REQ-CONTRACT-008`は50 Requirement authorityに含まれるが、definition自身が初期開発範囲外、初期vertical
sliceの完了条件またはrelease条件にしないと定める。このためRequirement identityと将来relationを保持しつつ、
最初のContractと初期releaseの必須成果にはしていない。

## Initial Consumer Audit

次の9 consumerを監査し、`scope_leak`は0だった。

- 50 Requirement authority
- NFR Verification Profiles
- first Review Task Contract／Work 5A
- Work 6A
- Work 7A
- Work 8
- Work 8A
- Work 7B
- Stage G／release

Work 5AはAs-Built、Implementation Contract、renderer、generic plugin、UIを除外し、
`single_active_leaf`とread-only local Gitへ限定する。Work 6Aのdeferred負例はinactive Catalogに置く。
Work 7Aは複数Work Itemを同時実行しない。Work 8は手作業またはshadow観測に限定する。Work 8Aは条件付きで、
未実施・不成立がrelease blockerにならず、Work 7Bは直列profileだけでも完了できる。

## Negative Audit

in-memory copyへ次の既知違反を一件ずつ注入し、全6件が期待分類で拒否された。

- consumer結果を`scope_leak`へ変更
- activation conditionを空にする
- deferred候補を初期release blockerにする
- `not_adopted_without_new_evidence`をactive配置へ先行予約する
- deferred deployment Profileを初期必須にする
- As-Builtの初期nonblocking規則を削除する

結果：`NEGATIVE_AUDIT_OK mutations=6 baseline=passed`

## Problem and Treatment

初回監査は50 Requirement authority bundleのIDを各recordの`requirement_id`から取得しようとし、0件として
誤停止した。bundleは追加13件を`definition_refs[].logical_id`、既存37件を
`legacy_authority_bindings[].requirement_ids`で結線する形状である。監査側のID取得をこの実形状へ合わせ、
50件を確認して再実行した。candidateの意味内容は変更していない。

全Testの初回起動は既存記録の`.venv/bin/python3`が現workspaceに存在せず、shell exit 127となった。
system `python3`の`pytest 8.4.2`を確認し、同じtest collectionを`python3 -m pytest -q`で再実行して
448件すべての合格を確認した。これはTest failureではなく実行器pathの参照切れである。

## Verification Results

- candidate digest：passed
- fixed source Digest：passed
- authority Requirement：`50`
- deferred inventory：`items=13 explicit=9 conditional=2 not_adopted=2`
- initial consumer audit：`consumers=9 leaks=0`
- negative audit：`mutations=6 baseline=passed`
- full Test：`448 passed in 2.03s`
- diff check：`git diff --check` passed、post-write candidate再読込 `items=13 consumers=9 leaks=0`

## Result

候補は`verified / human_decision_pending`である。deferred能力の存在、将来の受け先、有効化条件は固定したが、
初期Requirement、NFR Profile、最初のContract、後続Work、releaseへ無条件依存として混入していない。
Human承認前はWork 3の「deferred候補を初期Requirementの暗黙依存にしていない」checkboxを未完了に保つ。
