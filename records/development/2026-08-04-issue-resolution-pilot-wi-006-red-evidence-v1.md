# Issue Resolution Pilot WI-006 RED Evidence v1

## 対象

- Work Item：`WI-006`
- Test：`tests/test_issue_resolution_state.py`
- Test SHA-256：`b0fd75602017d9552972e54f4696c9b5f7f8b796d5cfef5b406a2a0ba2579d9c`
- WI-002 GREEN containing commit：`93785da70fc21ebff61ff1364a99a894b2a0ca0e`

## 固定した境界

- `triage_pending`から`resolved / unresolved`まで13通りの許可stateをEvidence ID付きで導出する。
- 同じkindでは最新versionだけを選択し、旧versionを根拠から除外する。
- 必須上流record欠落、同version競合、binding Digest不一致、手入力state不一致を`indeterminate`として拒否する。
- Task Contractのworking tree／HEAD境界とWI-001開始Evidenceを別stateとして扱う。

## RED確認

- targeted：`18 failed in 0.11s`
- 全体：`18 failed, 606 passed in 2.65s`
- 失敗identity：全18件が`ModuleNotFoundError: tools.development.issue_resolution_state`。

## 判定

期待したREDである。resolver実装、実snapshot、TODO compactionは未着手。RED containing commitとclean transition後だけ
固定Testを変更せず実装へ進む。
