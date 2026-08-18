# N7未充足候補4件の是正 作業票 v1（範囲固定・軽量）

- 作成日：2026-08-19
- 指示者：利用者（Human）。文言「N7未充足4件の是正を1作業単位で実施。作業票と事前走査から入って」
  （2026-08-19 chat）
- 種別：範囲固定文書（軽量作業票）。台帳候補record 4件の**形の是正のみ**（意味内容・仕分け結果・
  出所束縛は不変）。契約は立てない
- 固定入力：事前走査record
  `records/development/2026-08-19-n7-candidate-remediation-prescan-v1.md`

## 1. 正本範囲

1. 候補4件（`ic-contract-014-canonical-sequence-gaps-001`・`ic-launch-metrics-acceptance-title-001`・
   `ic-session-log-exit-code-doc-drift-001`・`ic-session-log-exit-code-vocabulary-001`の各`--v1.json`）
   を正規形へ**機械再生成**（事前走査§2案A）：
   (a) `related_candidates`と`source_identity.section`の値を`problem`末尾へ文として移記し欄を除去、
   (b) 無効分類を対応表で置換（`documentation`→`process_improvement`・`design`→`implementation`。
   有効値は保持）、(c) 他欄・`created_at`不変、(d) `content_digest`正準再計算。
2. 検証：各file単独でv3検証器合格（4件）→**N7単独0（是正前REDは事前走査で機械固定済み）**→
   台帳関連試験群（`test_issue_intake_v4_single_candidate.py`・`test_issue_intake_v4.py`・
   `test_issue_resolution_pilot.py`・`test_agents_lane_guidance.py`）単独0。
3. Evidence（guard付き測定ブロック・決定的射影）。

## 2. 範囲外

- V4決定の遡及作成（Markdown仕分けrecordが正本のまま。必要なら別判断）。
- 検証器・N7試験・allowlistの変更。候補の意味内容・仕分け結果の変更。
- 2026-08-18のMarkdown仕分けrecord自体の更新（候補digest参照のstale化は版の前進として
  束縛照合の追跡に委ねる）。

## 3. 受入条件

1 各候補のv3検証器単独0（4件）／2 N7単独0（事前走査のRED→GREEN）／3 台帳関連試験群単独0／
4 意味内容の保存（欄毎の対応：移記2欄・置換分類・他欄不変を機械diffで確認）／
5 計画writer仕上げ・証明書`start_allowed: true`／6 `git diff --check`・意味単位commit・
`work_unit_transition`合格。

## 4. Humanの確認が要る点（覆せる形）

1. 分類の対応表（`documentation`→`process_improvement`・`design`→`implementation`）。分類は
   AI提案欄で確定は仕分け側にあるため、置換は候補の効力を変えない。
2. 是正方式＝案A（形の是正のみ）。V4決定の遡及作成（案C）は行わない。
3. v1のまま置き換え（改版番号を上げない）。旧形はgit履歴が保持する。
