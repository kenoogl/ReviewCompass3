---
evidence_id: RC3-WORK1B-SESSION-E2E-GREEN-2026-08-03-V1
evidence_version: 1
recorded_at: 2026-08-03
work_id: Work 1B
work_item_id: RC3-WORK1B-SESSION-E2E
status: verified_green
workflow_state: active
confidentiality_class: project-internal
---

# Work 1B session lifecycle E2E green Evidence

## 1. 結果

固定済みのE2E Testとfixtureを変更せず、`run_session_bootstrap`を実装した。session開始／終了eventを
durable captureし、保存済みrawを再読込してCurrent Work Projectionを生成し、同じprojectionからshort／
detailed textを生成する。E2E 4件、関連15件、全434件はgreenである。

表示器だけが失敗してもcaptureとstructured projectionを保持し、authority入力欠落とは別状態で返す。
E2E Work Itemは`verified / green`である。実際のsession開始／終了でtextを使用していないため、Work 1B
全体は`active / green`とする。

## 2. 固定入力と実装identity

| role | identity／path | SHA-256 |
|---|---|---|
| E2E red Evidence | `records/development/2026-08-03-work-1b-session-e2e-red-evidence-v1.md` | `84cf75898883b73d4db996dbcdf465ada0a6a8b2375551c866d6a22a3e3429ab` |
| E2E Acceptance Test | `tests/test_session_bootstrap_e2e.py` | `ca4486fb43b3e5f4bd32175b0e177efb1a8612c08e2b43edaa98206e453eaedb` |
| E2E fixture root | `tests/fixtures/development/session-bootstrap-e2e` | `0c3fad4328c9e151e18e44aff06699043cde555e0c6807af32e5496f1b58a837` |
| raw workflow event stream | `raw/session.jsonl` | `d106284d8ae71ba4a12a70a65a1425f7cf26454962a4458774a745ded9b7b5b8` |
| 実装 | `tools/development/session_log_bootstrap.py` | `5ce2f77d671d48c8627cc3072a1b2111a4fc4ef615f3454d7b353d3b9ad2ac97` |
| 現行Plan | `docs/current/reviewcompass3-plan-current.md` | `0ae6bef979192b008a8a71fc090f709279c4bd1f0db159f9faadf947e929156f` |

E2E Test、fixture inventory、raw event streamのSHA-256はred時点から変わっていない。

## 3. 実装したE2E orchestration

1. `persist_session_capture`でraw、派生物、Session Evidenceをdurable保存する。
2. callerが渡したmemory上のeventでなく、保存済みrawを再読込する。
3. `session_started | session_ended`とevent数をsession lifecycle観測として返す。
4. 保存済みworkflow eventと固定projection inputsからstructured projectionを生成する。
5. projection diagnosticsの`complete`を`authority_status: valid`へ写像し、`incomplete | inconsistent`を
   別状態のまま返す。
6. 同じprojectionからshort／detailed textを生成する。
7. renderer exceptionを値非公開の`display_error: renderer_failed`へ変換し、capture、projection、
   authority statusを維持する。

## 4. green Test Evidence

### E2E targeted

- command：`python3 -m pytest -q tests/test_session_bootstrap_e2e.py`
- result：`4 passed in 0.03s`
- 判断：固定E2E Testを変更せずgreenにした。

### 関連Test

- command：`python3 -m pytest -q tests/test_session_bootstrap_e2e.py tests/test_session_log_durable_capture.py tests/test_session_log_bootstrap.py`
- result：`15 passed in 0.07s`

### full

- command：`python3 -m pytest -q`
- result：`434 passed in 1.93s`

## 5. post-write verification

- 実装を再読込し、cache書込みなしの`compile()`で`compile_ok`を確認した。
- 実装、固定E2E Test、raw fixture、red EvidenceのSHA-256を再計算し、記録identityと一致した。
- `git diff --check`と新規fileの末尾空白検査が通過した。
- renderer failure Testでcapture fileとSession Evidenceが残り、projection diagnosticsが`complete`、
  displayだけが`failed`であることを確認した。
- authority欠落Testでcaptureとrendererは正常、projectionとauthorityだけが`incomplete`であることを確認した。

## 6. 未実施と次作業

次は、実際のsession開始時にshort text、終了時にdetailed textを生成して使用する。生成に使ったPlan、event、
保存file、Digest、generated_at、freshnessを再読込し、Work 1Bの残りcheckboxと完了関門をEvidenceへ接続する。

実使用で入力欠落または表示不整合が見つかった場合、正常表示とせずWork 1Bを停止して修復する。

## 7. 関門

| 関門 | 判定 | Evidence |
|---|---|---|
| 固定E2E Testを変更しないgreen | pass | Test SHA-256、`4 passed` |
| 保存rawからprojection生成 | pass | E2E正常系・再読込Test |
| short／detailed同一projection | pass | text固定期待値 |
| display failure／authority欠落分離 | pass | negative Test 2件 |
| 関連／全Test green | pass | `15 passed`、全`434 passed` |
| 実session開始／終了での利用 | not_reached | 次作業 |
| Work 1B完了 | not_reached | 実使用Evidence待ち |

blocking conflict、blocker、Human判断待ちはない。
