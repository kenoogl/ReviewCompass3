# RQ2副産物の文言修正（候補1・2） 作業票 v1（範囲固定・軽量）

- 作成日：2026-08-18
- 指示者：利用者（Human）。選択文言「候補1と2を即時で直す。候補2は注記形式で。軽量作業票から
  進めて」（2026-08-18 chat）
- 作成者：Claude
- 種別：範囲固定文書（軽量作業票）。**文言修正のみ**であり、挙動・判定・schemaの変更を含まない
  ため契約形態にはあたらない（仕分けrecord§5の裁定どおり）
- 上位：仕分けrecord`records/development/2026-08-18-rq2-byproduct-candidates-triage-decision-v1.md`
- 対象候補：`IC-SESSION-LOG-EXIT-CODE-DOC-DRIFT-001`・`IC-LAUNCH-METRICS-ACCEPTANCE-TITLE-001`

## 1. 目的

RQ2実験の副産物として見つかった、運用中の文書2件の記述の誤りを直す。どちらも独立レビューが
検出したものである。

## 2. 正本範囲（成果物）

1. **候補1（改訂）**：`docs/development/prompts/session-log-record-run.md`
   - 第1節の括弧書き「0=全系統成功、5=いずれか失敗」を**実装の現挙動**に合わせる。実装
     （`tools/session_logs/record_run.py` 149〜150行・203行）は、系統の状態が`ok`でも`partial`
     でもないときだけ失敗とし、`partial`を含む場合は0を返す。
   - 第1節と第2節が語る対象（**包み役**の終了コードと**系統ごと**の終了コード）の区別を文面へ
     明示する。独立レビュー4回中4回がこの区別を取り違えた（実測）。
2. **候補2（注記）**：`docs/development/2026-08-17-launch-metrics-recoverability-work-ticket-v1.md`
   - **原文は1文字も変えない**（受入済み作業票であり、承認時点の記録を保つ）。
   - 末尾へ注記節を追加し、受入条件4の表題「実機確認1回」と内容（模擬実行で代替）のずれと、
     実際に実施したのは模擬実行であることを補う。出所と改善候補IDを併記する。

## 3. 範囲外

- 終了コードの**値そのもの**の変更（候補3`IC-SESSION-LOG-EXIT-CODE-VOCABULARY-001`で扱う）。
- `record_run.py`・`eventual_preservation.py`・`read_only_entry.py`の挙動変更。
- **RQ2実験のケース材料`docs/evaluation/rq2-cases/case-008/session-log-record-run.md`の更新**。
  これは実験時点の複製であり、正解表v2のdigest表で封じられている。**触らない**（更新すると
  実験の再現性が壊れる）。
- 候補2の原文の書き換え（注記形式と裁定済み）。
- 他の作業票の一斉点検。

## 4. 受入条件

1. 候補1の修正後の記述が、実装の挙動（`partial`を含む場合に0）と**一致する**こと。
2. 候補2の**原文が1文字も変わっていない**こと（`git diff`で追加のみを機械確認）。
3. RQ2実験の材料`docs/evaluation/rq2-cases/`配下が**無変更**であること（`git diff`で確認）。
4. 正解表v2のdigest表が引き続き全件一致すること（`shasum -c`の終了コード0）。
5. `git diff --check`・意味単位commit・`work_unit_transition`合格。

## 5. 実施順序

1. 候補1の改訂 → 実装との一致を目視と行番号で確認。
2. 候補2の注記追加 → 原文無変更を`git diff`で確認。
3. 受入条件3・4の機械確認 → commit → 移行検証 → 完了報告。
