---
evidence_id: RC3-WORK1B-DURABLE-RED-2026-08-03-V1
evidence_version: 1
recorded_at: 2026-08-03
work_id: Work 1B
work_item_id: RC3-WORK1B-DURABLE-CAPTURE
status: verified_red
workflow_state: active
confidentiality_class: project-internal
---

# Work 1B durable capture red Evidence

## 1. 結果

green済みのpure bootstrap mappingを変更せず、raw、派生物、Session EvidenceをLayout Baselineの
project外rootへdurable保存する境界を、独立fixture 1件とAcceptance Test 4件へ固定した。targeted Testと
全Testは、durable writer APIが未実装であることだけを理由に失敗した。

Work 1Bのmapping／restore／projection 7件はgreenのままである。現在のWork Item
`RC3-WORK1B-DURABLE-CAPTURE`は`active / red`であり、Work 1B全体は未完了である。

## 2. 固定入力とartifact

| role | identity／path | SHA-256 |
|---|---|---|
| 直前green Evidence | `records/development/2026-08-03-work-1b-green-evidence-v1.md` | `fdaeeb439226c6e86b17b8aa33e0e11fbdc64512ccd3b2c3f9a14f0970e169b9` |
| green実装 | `tools/development/session_log_bootstrap.py` | `eeacccb8635820ef4e15a7e7dd7b47a973096727830c8637092b06198e0b9fa8` |
| green Acceptance Test | `tests/test_session_log_bootstrap.py` | `7b7f46b2c5df5de55032eb311632cafc10b885399ad00d3d8ff7f8ec714aa685` |
| durable capture Test | `tests/test_session_log_durable_capture.py` | `36aab68bcc65966f20ac04e8d2f1f20ec527629020b5c3fef1cd4b776359366e` |
| expected Session Evidence | `tests/fixtures/development/session-log-durable-capture/expected-session-evidence.json` | `bc98331a48667ec3799ba2533710db080601ed1b829a2afcf0b2b78809d15906` |
| Layout Baseline Record | `records/development/2026-08-03-layout-baseline-v1.json` | `c18ee7a14a5720e578ea24b71e0cc120524fcfc2bca9df87a81de795cfc36cc2` |

既存green実装とgreen Acceptance TestのDigestは、durable capture Test追加の前後で一致した。durable
fixtureはlogical root名とroot-relative pathだけを保存し、端末固有絶対path findingは0件である。

## 3. 固定した保存境界

### 正常系

- raw bytesを`SENSITIVE_ROOT/sessions/<session_id>/raw/session.jsonl`へ保存する。
- transcript、summary、index、Session Evidenceを`DATA_ROOT/sessions/<session_id>/`へ保存する。
- Session Evidenceへsource identity、取得範囲、時刻、Digest、完全性、confidentiality、access、retention、
  mutation、availability、logical root-relative storage identityを記録する。
- 保存後に全fileを再読込し、固定raw／派生物／Session Evidenceのbyte列と一致させる。
- `PROJECT_ROOT`へruntime fileを書かない。

### failure境界

- profileと復元派生物のDigestが一致しない場合、保存を開始しない。
- 保存先fileが一件でも既存なら上書きせず、他のcapture fileも作成しない。
- write途中で失敗した場合、今回作成したfileと空directoryをrollbackし、正常完了Evidenceを残さない。

## 4. red Test Evidence

### targeted red

- command：`python3 -m pytest -q tests/test_session_log_durable_capture.py`
- result：`4 failed in 0.04s`
- failure oracle：全4件が
  `AttributeError: module 'tools.development.session_log_bootstrap' has no attribute 'persist_session_capture'`
  で失敗した。
- 判断：期待するdurable writer APIが未実装であることによる正しいred。

### 全Testでの分離確認

- command：`python3 -m pytest -q`
- result：`4 failed, 426 passed in 1.88s`
- failure oracle：失敗4件は新しいdurable capture Testだけで、既存426件はgreenである。

## 5. fixture・Test整合

- expected Session Evidenceを`python3 -m json.tool`で再読込した。
- Acceptance Testをcache書込みなしの`compile()`で検査し、`compile_ok`を確認した。
- expected Session Evidenceの管理対象絶対path検査は`managed_absolute_path_findings=0`だった。
- Test、fixture、green実装、green TestのSHA-256を再計算し、記録identityと一致した。
- `git diff --check`と新規fileの末尾空白検査が通過した。

## 6. 次作業

固定したdurable capture Testを変更せず、`persist_session_capture`を最小実装する。全出力をwrite前に生成・
Digest検証し、全保存先の衝突をpreflightした後に書込み、今回作成したfileだけをfailure時にrollbackする。

実装green後も、実session開始／終了でshort／detailed textを使用して保存後状態を再読込するまでは
Work 1Bを完了にしない。

## 7. 関門

| 関門 | 判定 | Evidence |
|---|---|---|
| durable保存期待値の固定 | pass | fixture 1件、Test 4件 |
| writer未実装を理由とするred | pass | targeted `4 failed` |
| 既存greenの維持 | pass | full `426 passed, 4 failed` |
| durable writer実装 | not_started | `persist_session_capture`不在 |
| Work 1B完了 | not_reached | writer green、実session利用待ち |

blocking conflict、blocker、Human判断待ちはない。
