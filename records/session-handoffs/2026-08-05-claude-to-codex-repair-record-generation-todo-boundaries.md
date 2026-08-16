# Claude → Codex：定型記録生成TODO最小縦切りの境界訂正 完了報告

指示：`records/session-handoffs/2026-08-05-codex-to-claude-repair-record-generation-todo-boundaries.md`

2つの境界不足をTest先行で訂正し、GREENの意味単位commitを1件作った。**停止はしていない。**

## commit

- commit SHA：`1ca15edba207dfddab97483462c9a68c9c5574eb`
- message：`Scope the handoff generator to its declared boundaries`
- 7 file、522行追加・40行削除。Test、module、root TODO、訂正GREEN Evidence、訂正最終receiptだけを含む。
- stageは対象7 pathを明示列挙した。`git add -A`と`git add .`は使っていない。
- commit後：`git status --short`は空。`work_unit_transition.py --work-status completed`は
  `next_work_allowed: true`。

## 2つの再現結果

| 欠陥 | 修正前（独立再現） | 修正後 |
| --- | --- | --- |
| 1. 参照の対象範囲が広すぎる | 節内`26件`に対し、末尾に別見出し＋linkを足すと`27件`（`docs/current/reviewcompass3-plan-current.md`）が収集された | 節外linkを足しても`26件`のまま増えない |
| 2. active IDの許可一覧がTODO自身から作られる | `ISSUE-PILOT-TODO-GROWTH-001`を`ISSUE-UNKNOWN-001`へ置換すると、自己導出したknown setが`{'ISSUE-UNKNOWN-001'}`になり`default_verify`が**受理した** | `TodoCompactionError: unknown active ID`で停止する |

修正後、正本から得たknown IDは`ISSUE-PILOT-TODO-GROWTH-001`、`ISSUE-HTC-66C3E6CA`、
`ISSUE-HTC-BEB5E0BD`、`ISSUE-HTC-C9F6C917`の4件で、実repositoryのroot TODOは`default_verify`を通る。

## 追加したTest（RED先行）

RED：`9 failed, 20 passed`。GREEN（対象2 file）：`29 passed`。

`tests/test_todo_record_generation.py`へ5件。

- Evidence節内の2件だけを収集する
- 候補が範囲外linkのDigestを含めてbyte不変である
- 節外linkだけの改竄では停止しない
- 節内linkの改竄は`reference_digest_mismatch`で停止しTODO bytesを変えない
- scoped verificationが節外を無視し、節内だけで停止する

`tests/test_todo_update_path.py`へ6件。

- known ID集合がlegacy／V4両rootから導出される
- known IDにTODO本文のIDが混ざらない
- 未知active IDで`default_verify()`が停止する
- 未知active IDで`run_two_phase_update()`が停止し、二度目を実行せずTODOを元bytesへ復元する
- Issue rootのJSON不正、未知record_kind、ID欠落、ID重複、symlinkで停止する
- 実repositoryのroot TODOがIssue正本からactive IDを解決して通る

既存testの期待は緩めていない。`test_default_verification_runs_the_repository_validators`だけ、
更新経路がglobal validatorではなくEvidence節限定の検証を使うという今回の訂正に合わせて確認対象の
関数名を変え、あわせて「global validatorをimportしないこと」の確認を足した。

## 最終summaryと二段確認

| 段 | receipt | SHA-256 | status |
| --- | --- | --- | --- |
| 一時（commitしない、repository外） | `<scratchpad>/boundary-repair-temporary-receipt.json` | `aa5526282604ec39bfdf7795f645217e4b0ee58315e9bc3cc0f32cff88742e82` | `passed` |
| 最終（commitする） | `records/development/2026-08-05-record-generation-todo-boundary-repair-green-test-receipt-v1.json` | `ad0f191e0af53a21ab130d9346743d0b214ac56ad6cf958b64ae175535df98df` | `passed` |

`test_summary`、`suite`、`python_version`、`pytest_version`、`fallback_used`、`status`の6 fieldが
**完全一致**した。両段とも
`{"errors": 0, "failed": 0, "passed": 892, "skipped": 0, "total": 892, "xfailed": 0, "xpassed": 0}`。
公式全testは`892 passed`である。

## TODOの更新範囲

機械が書き換えたのは**1行だけ**である。

```diff
-- 直近の全Test：venv公式runner `881 passed`、Python 3.9.6、pytest 8.4.2、fallback false
+- 直近の全Test：venv公式runner `892 passed`、Python 3.9.6、pytest 8.4.2、fallback false
```

あわせて人の記載として、初回GREEN Evidenceをstaleとして履歴に残す旨と、訂正GREEN Evidenceが
有効な完了根拠である旨、および訂正Evidence／訂正receiptへのlinkを追加した。
上限（12,288 bytes）を超えたため、更新規則に従い累積していた中間Evidence linkを3行整理した
（最終11,807 bytes）。link label、link path、link順序、Issue record、全TODOの再描画はしていない。

validator結果：`todo_handoff.py` `{"findings": [], "status": "passed"}`、
compaction validator合格、Evidence節限定のDigest照合合格、read-back一致、`git diff --check`合格。

## 初回Evidenceをstaleにしたこと

初回のGREEN Evidence（SHA-256 `61ae616c11f8f9f95acc4c8afde1d7983699bdaaa445ee9d3b3e6ed3ecddb89b`）と
初回最終receipt（同`70aaeab191424651956f6d896df7da7c9e682d7cf376e45de925b78fbeafaf6a`）は、
削除も書換えもしていない。境界不足があった初回根拠としてstaleのまま履歴に残し、
訂正Evidenceとroot TODOにその旨を記載した。有効な完了根拠は訂正GREEN Evidenceと訂正最終receiptである。

## 指示書との差異（要確認）

指示書はlegacy rootを`record_kind: "issue"`＋`record_id`と記していたが、実際のlegacy record
`issue-pilot-todo-growth-001--v1.json`は`record_kind: "issue_record"`＋`issue_id`である。
一方で指示書は「`ISSUE-PILOT-TODO-GROWTH-001`はlegacy rootの正本に存在するため、正しいloaderへの
変更後も正例として通る」とも述べている。指示書どおり`issue`＋`record_id`だけを受理すると、
このlegacy recordが未知record_kindとして停止し、後段の期待と両立しない。

両立させるため、loaderは`issue_record`（`issue_id`）と`issue`（`record_id`）の**両方**を受理する形に
した。未知のrecord_kindは従来どおり停止する。IDの出どころがTODO本文ではなくIssue正本になるという
安全上の性質は変わらない。Issue recordそのものは一切変更していない。
別の扱いが必要であればご指示いただきたい。

## 未実施の範囲

- Evidence／Decisionの定型欄への一般化（案B）。
- `render_todo_handoff()`による全TODO再生成、「直近の関連Test」行の自動選定、監査内訳の自動集計。
- `todo_compaction.py`、`issue_resolution_post_write.py`、legacy／V4 Issue record、Task Contract、
  Policy、config、hook、Git／shell operation routingの変更：いずれも行っていない
  （これらのpathを最後に触ったcommitは今回より前のままである）。
- 新しいDecision、Issue state変更、既存commitのrevert：行っていない。
  3 Issueはいずれも`registered`のままである。
- stdout／stderrをTest件数のsourceとして解析していない。
- push、PR、外部送信、履歴書換え：行っていない。
- 本完了報告はcommitに含めていない（`.gitignore`により無視される）。

## 停止の有無

**停止なし。** 既存Issue正本への変更は不要で、Issue rootは読み取れる形であり、root TODOの
非機械管理部分は機械更新で変わらず、二段確認は完全一致し、原状復帰も不要で、
Task Contractの固定source整合も崩れていない。
