---
evidence_id: RC3-WORK1B-SESSION-E2E-RED-2026-08-03-V1
evidence_version: 1
recorded_at: 2026-08-03
work_id: Work 1B
work_item_id: RC3-WORK1B-SESSION-E2E
status: verified_red
workflow_state: active
confidentiality_class: project-internal
---

# Work 1B session lifecycle E2E red Evidence

## 1. 結果

session開始／終了eventのdurable captureから、保存済みeventの再読込、Current Work Projection、short／
detailed text生成までを一続きに検証するE2E境界を、独立fixture 10件とAcceptance Test 4件へ固定した。
targeted Testと全Testは、E2E orchestration APIが未実装であることだけを理由に失敗した。

既存のbootstrap／durable capture関連11件とその他419件はgreenのままである。現在のWork Item
`RC3-WORK1B-SESSION-E2E`は`active / red`であり、Work 1B全体は未完了である。

## 2. 固定入力とartifact

| role | identity／path | SHA-256 |
|---|---|---|
| durable green Evidence | `records/development/2026-08-03-work-1b-durable-capture-green-evidence-v1.md` | `7ab01e1a106c6d8cb2711f1b8bc4df150d34761d94c7d0f13f033332783f2f22` |
| green実装 | `tools/development/session_log_bootstrap.py` | `fd2b286e2d0d72a05eb1f4f0cc0f19650eb41a4c9d2e7921eb9b61b374066339` |
| E2E Acceptance Test | `tests/test_session_bootstrap_e2e.py` | `ca4486fb43b3e5f4bd32175b0e177efb1a8612c08e2b43edaa98206e453eaedb` |
| E2E fixture root | `tests/fixtures/development/session-bootstrap-e2e` | ordered file-Digest inventory `0c3fad4328c9e151e18e44aff06699043cde555e0c6807af32e5496f1b58a837` |
| raw workflow event stream | `raw/session.jsonl` | `d106284d8ae71ba4a12a70a65a1425f7cf26454962a4458774a745ded9b7b5b8` |
| expected Session Evidence | `expected/session-evidence.json` | `a4656bf38680f726d04ca2149ab507ba7737799e28c26fe8d195928d728c9dab` |
| 現行Plan | `docs/current/reviewcompass3-plan-current.md` | `0ae6bef979192b008a8a71fc090f709279c4bd1f0db159f9faadf947e929156f` |

fixture rootのinventory Digestは、root配下のfile pathをbyte順に並べ、各fileのSHA-256を
`<digest><two spaces><path>\n`として連結した出力のSHA-256である。fixtureは合成eventだけを含み、
管理対象絶対path findingは0件である。

## 3. 固定したE2E境界

### 正常系

- `session_started | work_started | session_ended`の3 eventをrawとしてdurable captureする。
- 保存済みraw、3派生物、Session Evidenceを再読込し、固定byte列とDigestを照合する。
- event stream Digestをprojection input identityへ接続する。
- 固定Planとevent streamから同じstructured projectionを生成する。
- 同じprojectionからshort／detailed textを生成し、生成時刻とfreshnessを表示する。
- session lifecycleを`started: true | ended: true | event_count: 3`として観測する。

### failureの分離

- text rendererだけが失敗しても、validなdurable captureとstructured projectionを破棄しない。
- renderer failureは`display_status: failed / display_error: renderer_failed`として値を漏らさず区別する。
- authority入力欠落は`authority_status: incomplete`とし、rendererは正常に不完全状態を表示する。
- authority欠落を表示器failureとして扱わず、表示器failureをauthority欠落として扱わない。

## 4. red Test Evidence

### targeted red

- command：`python3 -m pytest -q tests/test_session_bootstrap_e2e.py`
- result：`4 failed in 0.04s`
- failure oracle：全4件が
  `AttributeError: module 'tools.development.session_log_bootstrap' has no attribute 'run_session_bootstrap'`
  で失敗した。
- 判断：期待するE2E orchestration APIが未実装であることによる正しいred。

### 全Testでの分離確認

- command：`python3 -m pytest -q`
- result：`4 failed, 430 passed in 2.01s`
- failure oracle：失敗4件は新しいE2E Testだけで、既存430件はgreenである。

## 5. fixture・Test整合

- JSON fixtureを`python3 -m json.tool`、Acceptance Testをcache書込みなしの`compile()`で検査した。
- rawからの3派生物restore、Session Evidence生成、projection、short／detailed textを既存green関数で個別に
  再生成し、全固定期待値と一致した。結果は`e2e_fixture_integrity=passed`。
- raw実Digestをcapture profile、projection inputs、expected projectionへ照合した。
- E2E fixtureの管理対象絶対path検査は`managed_absolute_path_findings=0`だった。
- Test、fixture inventory、green実装のSHA-256を再計算し、記録identityと一致した。

## 6. 次作業

固定したE2E Testを変更せず、`run_session_bootstrap`を最小実装する。durable capture完了後に保存rawを
再読込してworkflow eventをprojectし、authority状態とdisplay状態を別々に返す。renderer failureを捕捉しても
captureまたはprojectionを無効化しない。

E2E green後、実際のsession開始／終了でshort／detailed textを使用し、Work 1B完了Evidenceへ接続する。

## 7. 関門

| 関門 | 判定 | Evidence |
|---|---|---|
| E2E固定入力と期待値 | pass | fixture 10件、Test 4件、integrity check |
| orchestration未実装を理由とするred | pass | targeted `4 failed` |
| 既存greenの維持 | pass | full `430 passed, 4 failed` |
| session lifecycle orchestration | not_started | `run_session_bootstrap`不在 |
| Work 1B完了 | not_reached | E2E green、実session利用待ち |

blocking conflict、blocker、Human判断待ちはない。
