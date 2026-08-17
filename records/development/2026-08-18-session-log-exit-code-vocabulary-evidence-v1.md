# 終了コード語彙の是正（候補3） 実装Evidence v1

- 記録日：2026-08-18
- 記録者：Claude
- 作業票：`docs/development/2026-08-18-session-log-exit-code-vocabulary-work-ticket-v1.md`
- 事前走査：`records/development/2026-08-18-session-log-exit-code-vocabulary-prescan-v1.md`
- 対象候補：`IC-SESSION-LOG-EXIT-CODE-VOCABULARY-001`（仕分け＝採用）

## 1. 実装【実測】

- 正式再利用検索：`start_allowed: true`・直接一致12件（commit `b141860`）。
- RED：`tests/test_session_log_eventual_preservation.py`へ新設1本（partialで4を返す）。
  実装前に失敗（単独終了コード1）——commit `703d300`。
- GREEN：`tools/session_logs/eventual_preservation.py`——
  - 終了コードの意味を定数化（`EXIT_OK=0`・`EXIT_UNSUPPORTED=4`・`EXIT_FAILED=5`）。cli.pyは
    依存が重いためimportせず、**値の一致を試験で機械固定**（新設のもう1本）。
  - `run()`の返り値を`ok→0／partial→4／それ以外→5`へ変更（生の数字5の3値分岐を廃止）。
- 期待値の更新：`tests/test_session_log_record_run.py`の1箇所（`exit_code == 5`→`== 4`）。
  **試験の意図は保存**（partialの系統が包み役では成功扱い＝`overall_ok`真、の検査は不変）。
- 手順書：`docs/development/prompts/session-log-record-run.md` §2を実装に合わせて更新。

## 2. 受入条件の充足【実測】

| # | 条件 | 状態 | 根拠 |
| --- | --- | --- | --- |
| 1 | RED先行・失敗確認 | 充足 | commit `703d300`（単独終了コード1） |
| 2 | GREEN：session_logs系全通過 | 充足 | 359本全通過（session_log・session_artifact・redaction系。事前走査時の233本より広い範囲で確認・単独終了コード0） |
| 3 | partial系統でも包み役は0 | 充足 | 既存試験（`overall_ok is True`）維持＋実環境確認（下記） |
| 4 | 手順書§2が実装と一致 | 充足 | §1のとおり更新 |
| 5 | RQ2材料無変更・正解表digest一致 | 充足 | 変更0件・`shasum -c`12件OK |
| 6 | 正式検索証明書 | 充足 | `start_allowed: true`（commit `b141860`） |
| 7 | commit・移行検証 | 充足 | 本record commit時に最終確認 |

## 3. 実環境での動作確認【実測・要約JSONの転記】

```json
{"in_progress": {"files": [], "note": "進行中のため対象外（保全は実行時点まで完了。以後の内容は次回実行で追記保全）", "total": 1}, "overall_ok": true, "systems": [{"counts": {"failed": 0, "missing": 0, "succeeded": 553, "unsupported": 7}, "exit_code": 4, "in_progress_count": 1, "label": "claude", "status": "partial"}, {"counts": {"failed": 0, "missing": 0, "succeeded": 1152, "unsupported": 0}, "exit_code": 0, "in_progress_count": 0, "label": "codex現行", "status": "ok"}, {"counts": {"failed": 0, "missing": 0, "succeeded": 19, "unsupported": 0}, "exit_code": 0, "in_progress_count": 0, "label": "codex保管", "status": "ok"}]}
```

包み役の終了コード＝**0**。claude系統は`partial`（非対応7件＝本文なし前置のみfile等の既知の
正常状態）で`exit_code: 4`となり、**正常状態に失敗コード5を使う紛れが解消された**。件数は
2026-08-17の遡及実測（553／7）と一致しており、挙動の意味は変わっていない。

## 4. 範囲外に残したもの

- `read_only_entry.py`の独自語彙（`EXIT_PARTIAL=3`）：自分の語彙の中では正直な値であり、
  消費側の分析が別途要るため触っていない（作業票§3）。統合するなら別の作業単位。
- `cli.py`の語彙定義そのもの：無変更。
