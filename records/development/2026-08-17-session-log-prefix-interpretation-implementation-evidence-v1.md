# 契約014（セッションログ前置record解釈）実装・遡及実測 Evidence v1

- 記録日：2026-08-17
- 記録者：Claude
- 契約正本：`records/task-contract/2026-08-17-session-log-prefix-interpretation-candidate-v3.md`
  （v3。§1〜6・8・10と§7.2〜7.6はv2 `…-candidate-v2.md`を引き継ぐ）
- 採用：`records/development/2026-08-17-session-log-prefix-interpretation-contract-adoption-decision-v1.md`
  （v1採用・残余risk4点受容）。§7.4改定（v2）・§7.1修正（v3）は各版冒頭の利用者文言で承認

## 1. 実装（§9-1〜3）【実測】

- RED：`tests/test_session_log_prefix_interpretation.py`新設（commit `42ec177`・15本）。
  失敗7本（新仕様）・通過8本（互換とfail-closed既定の証明）・単独終了コード1。
  dequeue形の追加RED（commit `f3fa69c`・3本追加）：失敗2・通過1（enqueue `content`必須維持の
  証明）・単独終了コード1。
- GREEN：`tools/session_logs/source_kind.py`（正準列判定・補助分類の本文基準化・
  `is_known_prefix_record`共有定義）＋`tools/session_logs/parse_claude.py`（前置の無issue
  スキップ5行）——commit `1ded1ed`。dequeue形（`content`なし）の受理——commit `ef59575`。
- 試験結果：新設18本全通過・session_logs系全域330本全通過（いずれも単独実行・終了コード0）。
- 既存試験の書換え：**0 file**（§5.1-3の承認一覧6 fileの範囲内。既存fixtureはすべて本文なし形で
  新仕様と整合。`git diff`のfile一覧で機械確認：変更は実装2 fileのみ）。

## 2. 遡及の受入実測（§9-5・§7.5-2）【実測】

実環境`record-run`（手順書`docs/development/prompts/session-log-record-run.md`の1コマンド・
現セッションは既定の進行中分離）の前後比較。claude系統のcounts（要約JSONの機械転記）：

| 時点 | succeeded | unsupported | failed | missing |
| --- | --- | --- | --- | --- |
| 2026-08-16実測（基準） | 475 | 68 | 0 | 0 |
| v2実装後・1回目（**不合格**） | 476 | 84 | 0 | 0 |
| v3修正後・2回目（**成立**） | **553** | **7** | 0 | 0 |

- 1回目の不合格：`queue-operation`の`dequeue`recordが`content`を持たない実物形のため、
  正準列2 record目でfail-closed打ち切りが発生（誤解釈は無し・安全側に倒れていた）。
  全81 fileの網羅調査で、判定に落ちる前置型recordはこの1形のみ（76件）と機械特定し、
  契約候補v3（§7.1の操作別分岐）で修正。
- 2回目の成立：**77件が非対応から解釈済みへ遷移**。codex 2系統は変化なし（ok・1,152件/19件）。
- 残存の全数照合：source側現物で非対応は5件——`custom-title`開始3件・`mode`開始2件、
  **いずれも本文recordを持たない前置のみのfile**（契約の期待どおりの正当な残存）。
  **本文ありで非対応のfileは0件**＝遷移漏れなし。集計7件との差2件は実行時点の書きかけ状態に
  よる揺れ（次回実行で解消される性質）。
- 保全：全経過でfailed 0・missing 0（raw先行保存は無傷）。

## 3. 受入条件の充足状況（候補v3 §9）

| # | 条件 | 状態 | 根拠 |
| --- | --- | --- | --- |
| 1 | RED先行・失敗確認 | 充足 | commit `42ec177`・`f3fa69c`（単独終了コード1） |
| 2 | GREEN全通過 | 充足 | commit `1ded1ed`・`ef59575`（全域330本・単独終了コード0） |
| 3 | 書換えが一覧の範囲内 | 充足 | 書換え0 file（機械確認） |
| 4 | 手順書§2改定 | 充足 | commit `b260bf2` |
| 5 | 遡及の受入実測 | 充足 | §2（77件遷移・遷移漏れ0・残存は本文なしのみ） |
| 6 | 意味単位commit・移行検証 | 充足 | `work_unit_transition`＝`passed`（終了コード0） |

## 4. 未実施

- 完了レビュー（正式経路：assemble→記入→check→起動は利用者指示ごと）と製品受入判断。
- 残存5件（本文なし前置のみfile）の扱いの確定（現状は非対応＝正当な縮退として放置可）。
