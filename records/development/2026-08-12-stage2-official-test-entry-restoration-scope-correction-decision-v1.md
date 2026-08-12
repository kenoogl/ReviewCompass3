# 第2段 公式試験入口の正常化 範囲修正判断 v1

- 判断ID：`DEC-STAGE2-OFFICIAL-TEST-ENTRY-RESTORATION-SCOPE-CORRECTION-001`
- 判断日：2026-08-12
- 状態：`approved_to_implement`
- 作業票：`docs/development/2026-08-12-stage2-official-test-entry-restoration-bootstrap-work-ticket-v4.md`
- 作業票SHA-256：`8f6632ec7754b48d88c661682c76d6c8de5ee56c5b9d2997341aa45f99131bc8`
- 直前レビュー：`records/development/2026-08-12-stage2-official-test-entry-restoration-scope-correction-review-v1.md`
- 直前レビューSHA-256：`bd09762fa42fede4254cc7f34d878f6c199c2fee1e453aed54ab3f3baac6668f`

## 1. 利用者判断

【記録】利用者は、v3修正後確認が示した間接`_run_git`呼出し3変種の偽陰性と、同一file・同一新規試験へ
反例を加える限定案を確認し、選択肢`1`で承認した。

## 2. 承認範囲

承認対象は、作業票v4が固定する`tests/test_pilot_collaboration.py`一件、対応表3 key、新規恒久試験一件、
直接Git書込み4種、間接呼出し3変種の反例だけである。

製品コード、要求本文、他の試験file、保持中GREEN、Python 3.13、第2段完了、外部送信、push、履歴書換えは
含まない。完了レビュー前に、Git書込み禁止の試験結果と、実際に外部操作をしなかった事後Evidenceを分けて残す。
