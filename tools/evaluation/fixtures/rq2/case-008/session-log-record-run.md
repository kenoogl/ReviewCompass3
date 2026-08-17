> 本fileはReviewCompass3の評価実験（RQ2 paired trial）で使う複製材料である。運用中の
> record・手順書ではないため、本fileを根拠に運用判断をしないこと。

# Session log record run

セッションログ（Claude・Codexの生ログ）の全件保全を実行するときは、この手順だけを使う。
実行・集計・進行中分離はすべて機械処理（record-run wrapper）で行い、LLMは要約の転記と意味の
説明だけを行う。ファイル検索・実装ソースの読解・過去セッションからのコマンド発掘をしない。

## 1. 実行

次の1コマンドを単独で実行する（3系統＝claude・codex現行・codex保管の値と保全先はwrapperの
コードに固定済み。tools/session_logs/record_run.py）。

```bash
.venv/bin/python3 -m tools.session_logs.entry record-run
```

- 合否は**このコマンド単独の終了コード**で確認する（0=全系統成功、5=いずれか失敗）。
- 最終行の要約JSON（系統別status・件数・進行中件数）をそのままchatへ転記する。件数を手書き
  しない。
- 現セッションを含む「進行中」のfileは既定で要約から分離される（§3）。要約へ含める必要を
  利用者が指定した場合のみ`--include-in-progress`を付ける（実行時点までの保全状態が報告される）。

## 2. 結果の読み方（機械出力の意味）

- `status: ok`＝全file解釈・保全済み。`status: partial`＝**保全は全件完了**、一部が解釈非対応
  （既知の正常状態。§下記）。系統の`exit_code`はokで0・partialで5になるが、**partialのexit 5は
  失敗ではない**（wrapperが成功扱いで集約し、`overall_ok`に反映済み）。
- `status: runner_error`＝子プロセスの故障（失敗。全体不合格になる）。
- 解釈非対応（unsupported）＝既知の前置record（待ち行列操作`queue-operation`・動作モード
  `mode`・表題変更`custom-title`・下請けagent開始`started`）だけで本文（会話record）を持たない
  file、または未知種別のfile。**前置recordに続いて本文があるfileは契約014（2026-08-17）で解釈
  対象になった**ため非対応には数えられない。生ログの保全は非対応でも完了しており、件数の急変時
  以外は調査しない（急変は新しい前置種別の出現の合図——契約014 §7.6残余risk1）。

## 3. 進行中セッションの扱い（既定除外）

- 実行中に変化したfile・実行開始直前の活動窓（600秒）内に更新のあったfile（**現セッションを
  常に含む**）は、機械判定で要約から分離され、件数と注記だけが出る。LLMは分離判定・現セッション
  の特定・当該fileの読取りをしない。
- 保全自体は全件行われる（進行中fileも実行時点まで保全済み。以後の内容は次回実行で追記保全）。

## 4. 保全先と裁定済み事項

- 保全先（repo外私有領域）＝
  `~/.reviewcompass3/projects/reviewcompass3/development/sensitive/eventual-preservation`。
  権威系譜：`records/development/2026-08-04-session-transcript-eventual-preservation-storage-decision.json`
  →`records/development/2026-08-06-preservation-layout-v3-migration-decision-v1.md`
  →`records/development/2026-08-07-preservation-layout-v3-migration-evidence-v1.md`・同receipt。
- 機微削除規則（`--config`）は未指定が正（保全先は私有領域のため。作業票v2論点3の裁定）。
- 実行後の受領recordは毎回作らない。要約の転記までを標準とし、record化はHuman指示時のみ
  （作業票v2論点4の裁定）。

## 根拠

- 作業票v2（範囲固定・2026-08-17承認）：
  `docs/development/2026-08-17-session-log-run-procedure-work-ticket-v2.md`
- 事前走査record：`records/development/2026-08-17-session-log-run-procedure-prescan-v1.md`
- 試験：`tests/test_session_log_record_run.py`（10本。3系統固定値・partial成功扱い・進行中分離・
  機微/絶対path非出力・entry委譲を固定）
