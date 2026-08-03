---
evidence_id: RC3-WORK1B-GREEN-2026-08-03-V1
evidence_version: 1
recorded_at: 2026-08-03
work_id: Work 1B
work_name: Session Log Bootstrapと現在位置text表示
status: verified_green
workflow_state: active
confidentiality_class: project-internal
---

# Work 1B最小bootstrap mapping green Evidence

## 1. 結果

固定済みのAcceptance Testとfixtureを変更せず、Session Evidenceの保存先mapping、source availability判定、
rawからの派生物restore、bootstrap Current Work Projection、short／detailed text rendererを一つの
development bootstrap moduleへ実装した。targeted 7件と全426件はgreenである。

本Evidenceが確認するのは固定Test Contractに対する最小実装のgreenまでである。実sessionのdurable capture、
session開始／終了でのtext利用、Work 1B完了判断は未実施なので、Work 1Bは`active / green`とする。

## 2. 固定入力と実装identity

| role | identity／path | SHA-256 |
|---|---|---|
| Work 1B red Evidence | `records/development/2026-08-03-work-1b-red-evidence-v1.md` | `079277ae1f3f1c5277672d2ad24e4e1650983c0e0fc3eec5da4ee6f56d79604a` |
| 固定Acceptance Test | `tests/test_session_log_bootstrap.py` | `7b7f46b2c5df5de55032eb311632cafc10b885399ad00d3d8ff7f8ec714aa685` |
| fixture inventory | `tests/fixtures/development/session-log-bootstrap` | `7b713d65afffa3267954b42eb028e37b17906681ddc1570bc2deebc0f76e50e3` |
| 実装 | `tools/development/session_log_bootstrap.py` | `eeacccb8635820ef4e15a7e7dd7b47a973096727830c8637092b06198e0b9fa8` |
| Layout Baseline Record | `records/development/2026-08-03-layout-baseline-v1.json` | `c18ee7a14a5720e578ea24b71e0cc120524fcfc2bca9df87a81de795cfc36cc2` |

red確認後のTest source SHA-256とgreen確認後のTest source SHA-256は同じであり、Testを弱めたり期待値を
実装へ合わせたりしていない。

## 3. 実装した振る舞い

### capture profileとLayout mapping

- capture profileのversion、session／source identity、event範囲、時刻、Digest、access、retentionを検査する。
- raw bytesのDigestをprofileと照合する。
- Work 1AのLayout Resolutionから`SENSITIVE_ROOT`と`DATA_ROOT`を取得し、異なる絶対pathであることを確認する。
- rawを`sensitive_root/sessions/<session_id>/raw/session.jsonl`、index／summary／transcriptを
  `data_root/sessions/<session_id>/`へmappingする。
- profileのconfidentiality、access、retention、deadline、completeness、mutation、availabilityを
  `CapturePlan`へ保持する。

### availabilityとrestore

- 正常な空sourceを`available / normal_empty`として扱う。
- access不能、期限切れ、完全取得不能を`source_missing | source_expired | non_reconstructable`へ分ける。
- UTF-8 JSONLのsession identity、event数、先頭／末尾event IDをprofileと照合する。
- rawからtranscript、summary、indexを決定的に再生成し、rawと各派生物のDigestをprofileへ照合する。

### projectionとtext

- Work、pause／resume、blocker、Human判断、stale、defer、cancel eventを順に畳み込む。
- 同じ入力から同じstructured projectionを生成する。
- authority入力欠落を`incomplete`、同時刻のactive work競合を`inconsistent`とし、active workを推測しない。
- structured projectionからsession開始用short textと調査用detailed textを生成する。
- 入力identity／Digest、生成時刻、freshnessをdetailed textへ表示する。

## 4. green Test Evidence

### targeted

- command：`python3 -m pytest -q tests/test_session_log_bootstrap.py`
- result：`7 passed in 0.02s`
- 判断：固定した7件を変更せずgreenにした。

### full

- command：`python3 -m pytest -q`
- result：`426 passed in 2.19s`
- 判断：新規7件と既存419件がすべてgreenである。

## 5. post-write verification

- 実装を再読込し、cache書込みを行わない`compile()`で`compile_ok`を確認した。
- 実装SHA-256、固定Test SHA-256、red Evidence SHA-256を再計算し、記録値と一致した。
- `git diff --check`と新規fileの末尾空白検査が通過した。
- project内に手編集する`STATUS.md`が存在しないことを確認した。
- Test実行後も固定Test SHA-256は
  `7b7f46b2c5df5de55032eb311632cafc10b885399ad00d3d8ff7f8ec714aa685`のままである。

## 6. 未実施と次作業

次は、実sessionで利用するdurable capture境界とsession開始／終了時のprojection入力をtest-firstで確認する。
その後、short／detailed textを実際に生成し、authority、Digest、freshness、raw／派生物の保存先を再読込して
Work 1B完了Evidenceへ接続する。

本実装はpureなbootstrap mapping／restore／projectionであり、rawまたは派生物を永続化するwriter、外部送信、
製品schema、WebUI、常駐serviceを追加していない。既存の暫定`tools/session_logs`も変更していない。

## 7. 関門

| 関門 | 判定 | Evidence |
|---|---|---|
| 固定Testを変更しないgreen | pass | Test SHA-256、targeted `7 passed` |
| raw／派生物root mapping | pass | capture plan Test |
| availabilityとrestore | pass | availability／Digest restore Test |
| deterministic projectionとtext | pass | projection／renderer Test |
| 全Test green | pass | `426 passed` |
| durable captureと実session利用 | not_reached | 次作業 |
| Work 1B完了 | not_reached | 実使用Evidence待ち |

blocking conflict、blocker、Human判断待ちはない。
