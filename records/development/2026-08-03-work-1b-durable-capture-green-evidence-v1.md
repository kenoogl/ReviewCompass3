---
evidence_id: RC3-WORK1B-DURABLE-GREEN-2026-08-03-V1
evidence_version: 1
recorded_at: 2026-08-03
work_id: Work 1B
work_item_id: RC3-WORK1B-DURABLE-CAPTURE
status: verified_green
workflow_state: active
confidentiality_class: project-internal
---

# Work 1B durable capture green Evidence

## 1. 結果

固定済みのdurable capture Testとfixtureを変更せず、`persist_session_capture`を実装した。raw、3派生物、
Session EvidenceをLayout Baselineのproject外rootへ保存して再読込し、Digest不一致と既存file衝突を
write前に拒否し、write途中の失敗では今回作成したfileをrollbackする。durable 4件、bootstrap 7件、
全430件はgreenである。

durable capture Work Itemは`verified / green`である。実session開始／終了でのtext利用と保存後状態確認は
未実施なので、Work 1B全体は`active / green`とする。

## 2. 固定入力と実装identity

| role | identity／path | SHA-256 |
|---|---|---|
| durable red Evidence | `records/development/2026-08-03-work-1b-durable-capture-red-evidence-v1.md` | `a25c7cfde5817ff35375b07087e740820a7080b67bec8b6921fac167eb5e862d` |
| durable Acceptance Test | `tests/test_session_log_durable_capture.py` | `36aab68bcc65966f20ac04e8d2f1f20ec527629020b5c3fef1cd4b776359366e` |
| expected Session Evidence | `tests/fixtures/development/session-log-durable-capture/expected-session-evidence.json` | `bc98331a48667ec3799ba2533710db080601ed1b829a2afcf0b2b78809d15906` |
| bootstrap Acceptance Test | `tests/test_session_log_bootstrap.py` | `7b7f46b2c5df5de55032eb311632cafc10b885399ad00d3d8ff7f8ec714aa685` |
| 実装 | `tools/development/session_log_bootstrap.py` | `fd2b286e2d0d72a05eb1f4f0cc0f19650eb41a4c9d2e7921eb9b61b374066339` |
| Layout Baseline Record | `records/development/2026-08-03-layout-baseline-v1.json` | `c18ee7a14a5720e578ea24b71e0cc120524fcfc2bca9df87a81de795cfc36cc2` |

durable TestとfixtureのSHA-256はred時点から変わっていない。

## 3. 実装した保存処理

1. capture profileとraw Digestを検証する。
2. rawから3派生物をmemory上で生成し、全Digestをprofileへ照合する。
3. raw、派生物、Session Evidenceの全保存先に既存fileがないことをpreflightする。
4. raw、index、summary、transcriptの順に保存し、正常完了を示すSession Evidenceを最後に保存する。
5. 全fileを再読込してwrite前のbyte列と一致することを確認する。
6. 途中失敗時は今回作成したfileを逆順に削除し、今回作成した空directoryだけを除去する。

preflight前から存在したfileは上書きしない。rollback前から存在したdirectoryは記録してcleanup対象外とする。
session IDはpath separatorと`.`／`..`を拒否し、保存先がlogical root外へ逸脱しないようにした。

Session Evidenceは端末絶対pathを保存せず、`data_root | sensitive_root`とroot-relative pathで保存identityを
表す。`PROJECT_ROOT`にはruntime fileを書かない。

## 4. green Test Evidence

### durable targeted

- command：`python3 -m pytest -q tests/test_session_log_durable_capture.py`
- result：`4 passed in 0.02s`
- 判断：固定Testを変更せず、正常保存、Digest拒否、既存file保護、部分書込みrollbackをgreenにした。

### bootstrap regression

- command：`python3 -m pytest -q tests/test_session_log_bootstrap.py`
- result：`7 passed in 0.02s`

### 最終関連Test

- command：`python3 -m pytest -q tests/test_session_log_durable_capture.py tests/test_session_log_bootstrap.py`
- result：`11 passed in 0.05s`

### full

- command：`python3 -m pytest -q`
- result：`430 passed in 1.83s`

## 5. post-write verification

- 実装を再読込し、cache書込みなしの`compile()`で`compile_ok`を確認した。
- 実装、固定Test、fixtureのSHA-256を再計算し、記録値と一致した。
- `git diff --check`と新規fileの末尾空白検査が通過した。
- Session Evidenceの管理対象絶対path検査はred時点の`managed_absolute_path_findings=0`を維持する。
- 手編集する`STATUS.md`、WebUI、常駐service、外部送信は追加していない。

## 6. 未実施と次作業

次はbootstrap自身の一sessionを固定入力として、session開始／終了eventをdurable captureし、保存済みeventと
固定Plan identityからshort／detailed textを生成するE2E Testを先に作る。その後、実際の開始／終了で表示を
使用し、保存file、Digest、freshnessを再読込してWork 1B完了判断へ接続する。

## 7. 関門

| 関門 | 判定 | Evidence |
|---|---|---|
| 固定durable Testを変更しないgreen | pass | Test SHA-256、`4 passed` |
| raw／派生物／Evidence durable保存 | pass | 正常保存・再読込Test |
| write前Digest／衝突拒否 | pass | negative Test 2件 |
| 部分書込みrollback | pass | injected write failure Test |
| bootstrap回帰と全Test | pass | `11 passed`、全`430 passed` |
| 実session開始／終了での利用 | not_reached | 次作業 |
| Work 1B完了 | not_reached | 実使用Evidence待ち |

blocking conflict、blocker、Human判断待ちはない。
