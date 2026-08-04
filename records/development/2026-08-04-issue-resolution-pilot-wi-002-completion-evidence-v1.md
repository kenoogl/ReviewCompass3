# Issue Resolution Pilot WI-002 Completion Evidence v1

## 成果物

- 実装：`tools/development/todo_compaction.py`
- 実装SHA-256：`0e446f9aa100d8128c32a3ddbcaca601e66aead9548db349b11a9f5adde89a1f`
- 固定Test：`tests/test_todo_compaction.py`
- Test SHA-256：`c5dd608f2561130d3fb46ffa23bb6363e823d65eaa89c89b14a4741e788315a1`
- 追加path safety Test：`tests/test_todo_compaction_path_safety.py`
- path safety Test SHA-256：`e50963846bcc4024a47124bbd1e68e8baec47c978cd43e834306634997e5158d`
- RED containing commit：`7e435d1f4e53d9885b907b1d6aaff70da7cf13e5`

## 実装した境界

- TODO全体をUTF-8 bytesで計測し、12288 bytesを許可、12289 bytes以上を拒否する。
- 過去Claim、手戻り詳細section、session時系列logを拒否する。
- active Issue IDは既知の一件だけを許可し、欠落、未知、重複、複数を拒否する。
- Markdownのrepository相対参照をproject root内へ限定し、参照先file不在を拒否する。
- manifestのcanonical Digest、snapshot SHA-256、bytes、source identityを検査してからrestoreする。
- restore後のbytesとDigestを再読込し、不一致またはwrite失敗時は変更前TODOへrollbackする。
- restore対象をroot `TODO_NEXT_SESSION.md`、snapshot／manifestを`records/session-handoffs/`内へ限定する。
- 一時fileは衝突しない機械生成名を使用し、原子的に置換する。

path限定は復元操作の安全境界であるため、元の12 Testを変更せず別Test 4件へ固定した。限定処理を外した状態で
`4 failed`、限定処理を戻した後に`4 passed`となり、失敗理由はroot TODO以外またはsession-handoffs外を早期拒否
しないことだけだった。

## 検証結果

- targeted：`python3 -m pytest -q tests/test_todo_compaction.py tests/test_todo_compaction_path_safety.py`
- 結果：元の固定Test `12 passed`、path safetyを含む`16 passed in 0.04s`
- RED Test SHA-256：変更なし
- 公式runner receipt：
  `records/development/2026-08-04-issue-resolution-pilot-wi-002-green-test-receipt-v1.json`
- receipt SHA-256：`44cbebe8f86111d3c9ea8738bf4cd5c27484df25075a72511380481952ed8bac`
- 全体結果：`606 passed in 2.71s`、`fallback_used: false`
- `git diff --check`：合格

## 判定

WI-002のvalidator／restore実装はGREENである。検証はtemp fixtureだけを対象とし、実TODO、実snapshot、manifest、
WI-006、TODO compaction、Resolution Verdictは未実施である。WI-002 containing commitとclean transition確認後、
次の独立作業単位としてWI-006 REDへ進める。
