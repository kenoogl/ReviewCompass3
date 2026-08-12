# 第2段 公式試験入口の正常化 範囲追加 独立開始前レビュー v1

- レビュー記録ID：`REV-STAGE2-OFFICIAL-TEST-ENTRY-RESTORATION-SCOPE-EXTENSION-START-001`
- レビュー日：2026-08-12
- レビュー担当：作業担当とは異なる実行単位
- 対象作業票：`docs/development/2026-08-12-stage2-official-test-entry-restoration-bootstrap-work-ticket-v2.md`
- 作業票ID：`BTW-STAGE2-OFFICIAL-TEST-ENTRY-RESTORATION-002`
- 作業票SHA-256：`6cbb24eae0397198f48bb25ba6bd56874c020119a8f443b6d5251ca04266d018`
- 作業票コミット：`53a49d65526766ab9e723c748ff39f510c3045b3`
- 範囲追加判断：`records/development/2026-08-12-stage2-official-test-entry-restoration-scope-extension-decision-v1.md`
- 範囲追加判断SHA-256：`a85b2cadf585b2ec7377475124b9823f88da5d7b1beb11267b2f5ea9a8ccbd62`
- 基準コミット兼REDコミット：`354c57e1d7dd28eaa6b2e271ea3dae60ce949720`
- 危険度：`high`
- 判定：`修正要`

## 1. 判定

【判断】追加範囲を一fileの`TRACEABILITY`三keyへ限定する境界、v1の目的、RED三fileと保持中GREENの
不変境界、要求本文・試験関数・製品codeを変更しない境界は明確である。削除済み試験名を除けば、現行の
対応表試験が検出している未定義参照は解消する。

一方、`OUT-PC-006`を二つの変更範囲試験だけへ対応させる案は、同要求が含む意味的に完結したcommit、停止、
push・履歴書換え・外部送信の禁止を検証しない。構文上は対応表試験を成功させながら要求との対応を偽るため、
作業開始前に修正を要する。

【実測】開始を止める指摘は1件である。

## 2. 止める指摘

| ID | 区分 | 段階 | 根拠類型 | 事象 | 必要な修正 |
| --- | --- | --- | --- | --- | --- |
| `SR-SE-001` | blocking | scope | `work-review-protocol` §11.1 類型1・3 | v6の`OUT-PC-006`は「意味的に完結した変更をcommitして停止し、push・履歴書換え・外部送信を行わない」である。提案された二試験は、使い捨てGitで許可外pathとhandoff配下へ隠したcodeを検出するだけで、これらを検査しない。提案どおり三keyを置換する構文木上の模擬では未定義参照0となるため、要求未検証のまま対応表試験が合格する。さらに既存のprocess検査は`git push`を違反0として受理した | `OUT-PC-006`を、要求本文に即した検証先とEvidenceへ結び直す。現行四試験file内には同要求全体を検証する既存試験がない。新しい恒久試験、既存試験の変更、または対応表の意味変更が必要なら、現行の一file・三keyだけという承認範囲を広げる前に新版作業票と利用者判断を得る |

【判断】本指摘は表現改善ではない。上流Requirementと対応表の意味が矛盾し、未検証要求を被覆済みとして
成功させる反証があるため、類型1と類型3に該当する。同じ類型の三keyを一回で確認し、別原因のblocking所見は
追加しなかった。

## 3. 三keyの対応先

| key | v6要求の要点 | 妥当な対応先 | 判断 |
| --- | --- | --- | --- |
| `NG-PC-007` | 関係ない整形、全体indent変更、既存試験書換えを行わない | `test_change_scope_rejects_forbidden_commit_before_later_allowed_commit`、`test_change_scope_does_not_hide_code_inside_handoff_directory` | 【判断】許可外pathとhandoff配下へ隠したcodeを見逃さない恒久的な反例として妥当。要求のうち変更範囲に関する機械証拠である |
| `ST-PC-001` | 範囲外の設計・schema・既存試験変更が必要なら停止 | 同上二試験 | 【判断】後続の許可変更や記録で先行する許可外変更を隠せないことを示し、範囲拡張の検知先として妥当。実際の停止判断は作業時Evidenceと完了レビューでも確認する |
| `OUT-PC-006` | 意味的に完結した変更をcommitして停止し、push・履歴書換え・外部送信をしない | 現行の二試験だけでは妥当な対応先なし | 【判断】`test_pilot_code_uses_only_array_git_subprocess_run`は外部process制限により近い既存試験だが、`git push`反証を受理するため単独でも十分でない。commitの意味的完結性、停止、Git副作用は結果commitとGit Evidenceによる完了時確認も必要である |

## 4. 範囲、原因、境界の確認

【実測】v2はv1の変更可能path六件へ`tests/test_pilot_collaboration.py`一件を加え、追加変更箇所を
`NG-PC-007`、`ST-PC-001`、`OUT-PC-006`の三keyにある削除済み試験名だけへ限定する。Python 3.13、
重大な欠陥12件、外部送信、第2段完了は引き続き対象外である。

【実測】失敗結果記録のSHA-256は
`49c87a585b2f203ad8d8a7964cfbb19405ffaf55b973894679ad6c8b35296efe`で一致した。公式全試験は
1,735件中1,734件成功、1件失敗、終了コード1であり、唯一の失敗は
`test_requirement_traceability_covers_all_26_ids`が削除済み
`test_change_scope_contains_only_v6_allowlisted_paths`を未定義参照として検出したものである。同nodeを単独再実行して
同じ失敗を確認した。

【実測】提案どおり三keyを構文木上の値だけで模擬すると、26 keyを保ち、未定義参照は0になる。したがって、
削除済み試験名を除くことは現在の構造的失敗だけを解消する最小変更である。しかし、この成功条件は参照する
試験関数名の実在だけを検査し、要求本文との意味整合を検査しないため、`SR-SE-001`を解消しない。

【実測】基準兼REDコミットは試験三fileだけを変更した。基準コミットから作業票コミットまでと現在の未コミット差分に、
そのRED三fileの追加変更はない。現在の作業treeの既存差分は、承認済みGREENとして保持されている
`config/development-test-runner.json`と`tools/development/policy_test_runner.py`の二件だけであり、本レビューでは
内容変更もstageもしていない。

## 5. 機械確認結果

合否は各commandの終了コードを単独で確認した。

| 目的 | 実行内容 | 終了コード | 結果 |
| --- | --- | ---: | --- |
| 固定材料 | `shasum -a 256` | 0 | v2、範囲追加判断、v1、失敗結果記録、対象試験fileが提示値と一致 |
| commitと変更範囲 | `git rev-parse`、`git show --stat`、`git diff --name-only` | 0 | 作業票commitを完全SHAへ解決。REDは試験三fileだけ |
| 現行失敗の再現 | `.venv/bin/python3 -m pytest -q tests/test_pilot_collaboration.py::test_requirement_traceability_covers_all_26_ids` | 1 | 削除済み試験名一件だけを未定義参照として検出 |
| 残す二試験 | `.venv/bin/python3 -m pytest -q`で指定二nodeを単独集合として実行 | 0 | 2件成功 |
| 提案置換の構造確認 | Python構文木から対応表、定義済み試験、三keyを抽出し、提案値をmemory上で置換 | 0 | 26 key、未定義参照0、三keyは同じ二試験 |
| `OUT-PC-006`反証 | 現行`_process_policy_violations`へliteral arrayの`git push origin main`を入力 | 0 | 違反一覧は空。既存の近接検査でもpush禁止を証明できない |
| 文書・既存差分 | `git diff --check`、`git diff --cached --check` | 0 | 問題なし |

## 6. 利用者判断境界、未実施、次の一作業

【記録】利用者が承認した範囲追加は`tests/test_pilot_collaboration.py`一件と対応表三keyだけである。本レビューは
その承認を、新規試験、既存試験変更、要求本文変更、製品code変更へ広げない。技術的な開始可否と、範囲追加、
意味変更、第2段完了の利用者判断を分離する。

【未実施】対応表、RED試験、保持中GREEN、要求本文、設定、実装、Evidence、TODOは変更していない。公式全試験の
再実行、外部送信、Python 3.13移行、重大な欠陥12件の修復、第2段の採用・完了判断は行っていない。

【次】対応表を変更せず、操縦役は`OUT-PC-006`の検証方法を一件の範囲修正案として利用者へ返す。現行範囲外の
試験または対応表の意味を変える場合は、承認後に新版作業票を作り、そこで改めて開始条件を固定する。
