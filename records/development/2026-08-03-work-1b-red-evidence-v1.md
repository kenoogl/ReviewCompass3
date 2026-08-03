---
evidence_id: RC3-WORK1B-RED-2026-08-03-V1
evidence_version: 1
recorded_at: 2026-08-03
work_id: Work 1B
work_name: Session Log Bootstrapと現在位置text表示
status: verified_red
workflow_state: active
confidentiality_class: project-internal
---

# Work 1B固定fixture・red Test Evidence

## 1. 結果

Layout Baselineを入力に使うSession Log Bootstrapとbootstrap Current Work Projectionについて、期待する
入出力を13個の固定fixtureと7件の受入Testへ固定した。対象Testと全Testは、新しいdevelopment bootstrap
moduleが未実装であることだけを理由に失敗した。

本Evidenceが確認するのは`red`までである。Work 1Bは`active / red`であり、完了またはgreenではない。

## 2. 固定sourceとartifact

| role | identity／path | SHA-256／identity |
|---|---|---|
| 現行Plan | `docs/current/reviewcompass3-plan-current.md` | `0ae6bef979192b008a8a71fc090f709279c4bd1f0db159f9faadf947e929156f` |
| Work 1A Evidence | `records/development/2026-08-03-work-1a-layout-evidence-v1.md` | `5d54c7de759388ae81c1fefebcc50c817c0b38ae2bcdc65444f47aa48cc8e899` |
| Layout Baseline Record | `records/development/2026-08-03-layout-baseline-v1.json` | `c18ee7a14a5720e578ea24b71e0cc120524fcfc2bca9df87a81de795cfc36cc2` |
| Acceptance Test | `tests/test_session_log_bootstrap.py` | `7b7f46b2c5df5de55032eb311632cafc10b885399ad00d3d8ff7f8ec714aa685` |
| fixture root | `tests/fixtures/development/session-log-bootstrap` | ordered file-Digest inventory `7b713d65afffa3267954b42eb028e37b17906681ddc1570bc2deebc0f76e50e3` |
| raw synthetic fixture | `raw/session.jsonl` | `461d29923f1b3c5ac5926458c469620ce1f945a863daab86b120de3a36d8db23` |
| workflow event fixture | `workflow-events.jsonl` | `8009712a3c673e935aa60434839acc104bae6ab606638538f172df1d43c4b024` |

fixture rootのinventory Digestは、root配下のfile pathをbyte順に並べ、各fileのSHA-256を
`<digest><two spaces><path>\n`として連結した出力のSHA-256である。raw fixtureは実sessionではなく、
機密値を含まない合成Test入力である。

## 3. 固定した振る舞い

### Session Evidenceと保存境界

- session ID、source identity／revision、event取得範囲、開始／取得時刻、capture deadlineを記録する。
- raw Digest、派生物Digest、完全性、confidentiality、access、retention、mutation、availabilityを記録する。
- raw保存先を`SENSITIVE_ROOT/sessions/<session_id>/raw/`へ置く。
- transcript、summary、indexを`DATA_ROOT/sessions/<session_id>/`へ置く。
- 合成rawから3派生物を再生成し、固定byte列とDigestを照合する。
- 正常な空sourceを`source_missing | source_expired | non_reconstructable`と区別する。

### bootstrap Current Work Projection

- `session_started | session_ended`、`work_started`、pause／resume、blocker発生／解消、Human判断要求／決定、
  upstream revision、stale／再検証、cancel／deferを固定eventとして扱う。
- 同じeventと固定入力から同じstructured projectionを生成する。
- 全体Stage／Work、active作業、TDD状態、次作業、blocker、Human判断待ち、stale、入力identity／Digest、
  生成時刻、freshnessを表示する。
- session開始用short textと調査用detailed textを同じprojectionから生成する。
- authority入力欠落を`incomplete`、同時刻の競合active workを`inconsistent`として表示し、推測で埋めない。

## 4. red Test Evidence

### targeted red

- command：`python3 -m pytest -q tests/test_session_log_bootstrap.py`
- result：`7 failed in 0.06s`
- failure oracle：全7件が
  `ModuleNotFoundError: No module named 'tools.development.session_log_bootstrap'`で失敗した。
- 判断：期待するbootstrap mapping moduleが未実装であることによる正しいred。

### 全Testでの分離確認

- command：`python3 -m pytest -q`
- result：`7 failed, 419 passed in 1.90s`
- failure oracle：失敗7件はすべて新しい`tests/test_session_log_bootstrap.py`の同じ未実装moduleである。
- 判断：既存419件はgreenのままであり、新規red以外の回帰失敗は観測しなかった。

## 5. fixture整合検査

- JSON：capture profile、availability cases、projection inputs、expected JSONを`python3 -m json.tool`で検査し、
  全件通過した。
- JSONL：raw、通常event、競合eventの全lineを`json.loads`で再読込した。
- Digest：raw、transcript、summary、indexの実Digestをcapture profileの固定Digestと照合した。
- projection input：event streamの実Digestをinput manifestおよびexpected projectionと照合した。
- syntax：cache書込みを行わない`compile()`でAcceptance Testを検査し、`compile_ok`。
- diff：Evidence更新前の`git diff --check`は通過した。最終差分で再実行する。

## 6. 非目標と次作業

本作業では`tools.development.session_log_bootstrap`を実装していない。既存の暫定
`tools/session_logs`、手編集する`STATUS.md`、製品schema、WebUI、常駐serviceも変更または追加していない。

次の一作業は、本Testを変更せず、`tools.development.session_log_bootstrap`へ最小mapping、restore、
projection、text rendererを実装してtargeted Testをgreenにすることである。

## 7. 関門

| 関門 | 判定 | Evidence |
|---|---|---|
| 固定fixtureと期待入出力 | pass | fixture 13 file、Test 7件、Digest整合検査 |
| bootstrap mapping未実装を理由とするred | pass | targeted `7 failed` |
| 既存Testからのfailure分離 | pass | full `419 passed, 7 failed` |
| Session Log Bootstrap実装 | not_started | module不在 |
| Work 1B green／完了 | not_reached | 次作業で実装・検証する |

blocking conflict、blocker、Human判断待ちはない。
