# Completion Evidence：Work 7A第2項 前駆slice — checkout relocation read-only Git捕捉

- 作成日：2026-08-09
- Closer：Codex
- collaboration mode：`role_neutral_pilot_review`
- 対象：Work 7A第2項の前駆sliceだけ
- status：`verified / completed`

## 1. 完了根拠

Human裁定「分割案1」により、Work 7A第2項を次の3 sliceへ分割したうち、最初の前駆sliceを完了とする。

1. read-only GitによるRepository Binding／Source Snapshot／Change Setの捕捉とcheckout移動後照合
2. Project Bindingの耐久保存・復元
3. Verification Runの復元

本Evidenceが完了とするのは1だけである。2と3は未実施であり、Initial Development Checklistの
「別checkoutとproject移動後にBinding、Snapshot、Change Setを復元できる」checkboxは開けたまま維持する。

| role | path | SHA-256／identity |
| --- | --- | --- |
| scope | `records/session-handoffs/2026-08-09-claude-pilot-work7a-checkout-relocation-scope-v2.md` | `f127351d05bc621af95a042506dc726790ca59ecc928cec4c34257ee23d473a8` |
| RED | commit | `a7e58eb2f212c78e2c62e95947718fcf4da3ad9f` |
| GREEN | commit | `86f0f63cb24feda35de740f835a04b8c0782eb68` |
| 修正RED 1 | commit | `2b27b4d4a00a7ee6989d29fc6a35e92ef01d8b56` |
| 修正GREEN 1 | commit | `af8e005f8844520042eec16252d48ef64ccee368` |
| 修正RED 2 | commit | `0e1952195d0c40c5b3285fc151a55ac0ebf085cf` |
| 修正GREEN 2 | commit | `2c834b4e686c8c0c95779e5784853b508663ecc3` |
| GREEN Evidence | `records/development/2026-08-09-work7a-checkout-relocation-green-evidence-v1.md` | `c20a8d4056cbe55870defd61f7a3f3de61942f945a1fe9cb7bfb696d34105c10` |
| 公式全Test receipt | `records/development/2026-08-09-work7a-checkout-relocation-green-test-receipt-v1.json` | `b4384813ff82ca0e7aa9a133996dc618710658a7f5a7ca1c405c63805f9d9a9e` |
| 独立review result | `records/session-handoffs/2026-08-09-codex-review-result-work7a-checkout-relocation-v3.md` | SHA-256 `ec30754f1ff8d6e06b791b1be78c58dd558e1966b80c34716807b15c0d497a3c`、verdict `verified`、commit `bb9723baaa4899df9f946977ed60e5ed662f95a0` |

## 2. 検証結果

- targeted：23 passed
- 関連回帰：83 passed
- 公式全Test：1338 passed、failed 0、fallback false
- RR-P1-004追加独立反証：1 passed
- Reviewer新規反証：dangling symlinkとfile→symlink種別変化の2 passed
- blocking Finding：0

Repository Bindingの暫定lineage ID限定、実HEAD束縛、dirty／staged／対象untrackedのChange Set、
Git config隔離、tracked symlink payload identity、read-only Git境界を独立レビューで確認した。

## 3. 未実施と次の一作業

- 未実施：Project Bindingの耐久保存・復元、binding directory、Verification Run復元、Work 7A第2項checkbox完了
- 次の一作業：Work 7A第2項内のProject Binding耐久保存・復元slice
- その後：Verification Run復元slice

次sliceはLayout v3の承認済みstorage shape
`state_root/projects/<project_id>/bindings/<binding_id>.json`をconsumerとし、前駆sliceの
Repository Binding値を耐久Project Bindingへ接続する。開始にはHuman着手指示と新しい範囲固定を要する。

## 4. Human境界と禁止操作

- Human裁定「分割案1」とrisk `high`を維持した。
- TODOは次の一作業だけを後続sliceへprojectionし、段完了を表示しない。
- checklistの第2項checkbox、Plan、Decision、実装、schema、Testは本Closer作業で変更しない。
- push、tag、PR、履歴書換え、外部送信、不可逆操作は行わない。
