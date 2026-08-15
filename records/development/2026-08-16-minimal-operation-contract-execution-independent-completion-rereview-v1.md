# 最小運用契約実行 独立完了再レビュー v1

- Reviewer model：【記録】`gpt-5.6-sol`
- reasoning effort：【記録】`high`
- 実施日：【記録】2026-08-16
- 依頼record：【記録】`records/session-handoffs/2026-08-16-g30-operation-run-completion-rereview-codex-request-v1.md`
- 先行レビュー：【記録】`records/development/2026-08-16-minimal-operation-contract-execution-independent-completion-review-v1.md`
- 訂正commit：【記録】`13e8b3d33e53e2aacde38ed2b4b473894f800cb0`
- review risk：【判断】`high`
- 方法：【記録】依頼record §3の鮮度検査と§4の再レビューだけ
- 判定：【判断】`verified`
- Finding：【判断】blocking 0件、non-blocking 0件

## 1. 結論

【判断】先行レビューのblocking Finding B-01、B-02、B-03はすべて閉鎖された。各訂正の反証、無変異の
対象67件、関連試験、隔離条件付き正規全試験に成功し、訂正3点以外の製品差分はなかった。依頼record §4の
再レビュー範囲について、報告と事後状態は一致し、判定は`verified`である。

【判断】新たなblocking Findingとnon-blocking Findingはない。本判定は独立完了再レビューの成立を示すが、
利用者による製品受入を代替しない。

## 2. 開始時の鮮度検査

【実測】開始時のbranchは`main`、HEADは
`74b0cd227b2db6c0917fe7a391b83d01115486c0`だった。`git status --short`は出力なし、終了コード0だった。

【実測】`git log -12 --format=%H%x09%P%x09%s -- records/session-handoffs`は終了コード0だった。最新の
Codex宛て依頼は本依頼recordで、そのcommitは`74b0cd227b2db6c0917fe7a391b83d01115486c0`、親は訂正commit
`13e8b3d33e53e2aacde38ed2b4b473894f800cb0`だった。`git merge-base --is-ancestor 13e8b3d HEAD`は
終了コード0だった。

【実測】依頼record §2の固定5 fileについてSHA-256を`.venv/bin/python3`で再計算し、全件が記載値と
一致した。

| 固定入力 | 再計算したSHA-256 |
| --- | --- |
| 先行完了レビュー | `38460b84e469cc81950633b3026cb195d6c308e4aaa171a22d10458cd0e13281` |
| 訂正Evidence | `c2a386c87e542a7f626e77b931bb24672fd6bf392fda71e216a5c19923959c30` |
| 実行核 | `a0fdc2eacaa6ce6d5baafc54daa133f215dc3b0285772af7f16f7d0f94b8c689` |
| 入口 | `06c01aefbff568f80ff0919af398dfff2fabc405927419fe0acd5e52a1a88abb` |
| 対象試験 | `1d96fb6ff03326a2febfb47963ab1c2560fc35f6cac7f08c1d340dd9921005b5` |

【判断】依頼の宛先、開始状態、固定入力に不一致はなく、鮮度停止条件には該当しなかった。

## 3. Claim、変更範囲、Provenanceの照合

【実測】対象commit列は`b1ad31a`（訂正前実装）→`e5778d4`（先行レビュー依頼）→`06742d9`
（先行レビュー判定）→`13e8b3d`（訂正）→`74b0cd2`（本再レビュー依頼）だった。

【実測】訂正commit `13e8b3d`の変更pathは、訂正Evidence、対象試験、実行核、入口の4件だけだった。
製品差分3件を再読込みした結果、実行核は読取り前後比較への`st_mtime_ns`・`st_ctime_ns`追加、入口と
実行核はNUL・単独サロゲートのpath拒否、対象試験はB-01反証1件、B-02反証2件、B-03停止試験3件の
追加に限定されていた。契約本文と他の製品成果物に訂正差分はなかった。

【実測】訂正commitから再レビュー開始時HEADまでの追加変更は、本依頼record 1件だけだった。

【判断】変更範囲は依頼record §2の訂正3点と一致し、必須stepの順序、対象identity、Human境界に
不一致はなかった。

## 4. blocking Finding 3件の閉鎖

### B-01：同一inode・同一sizeの読取り中変更

【実測】先行レビューと同型の反証
`tests/test_operation_contract_run.py::test_same_size_modification_during_read_stops`を単独実行した。初回読取り後に
同一fileへ同一sizeの別内容を書き戻した場合、`unreadable_input / contract`・終了コード2で停止し、試験1件は
成功、command終了コードは0だった。

【判断】B-01は閉鎖された。

### B-02：NUL・単独サロゲートを含む引数path

【実測】
`tests/test_operation_contract_run.py::test_nul_and_surrogate_paths_stop_before_reading`を単独実行した。NUL文字と
単独サロゲートの2変種は、どちらも読取り前に`invalid_path / arguments`・終了コード2の固定停止形となり、
試験2件は成功、command終了コードは0だった。

【判断】B-02は閉鎖された。

### B-03：機微pattern 3規則の変異検出

【実測】実行核へ束縛された既定patternからbearer token、API key代入、秘密鍵blockの3規則を実行時に外し、
対象試験全件を実行した。追加された3件だけが期待値との差を検出して失敗し、64件は成功、pytestの終了コードは1
だった。3規則を外した状態で対象試験が誤って全件成功する事象は再現しなかった。

【実測】無変異の対象試験67件はすべて成功し、終了コード0だった。

【判断】B-03は閉鎖された。

## 5. 必須の機械確認

【実測】次を各単独commandとして実行し、各終了コードで判定した。

| command | 件数 | 結果 | 終了コード |
| --- | ---: | --- | ---: |
| `.venv/bin/python3 -m pytest -q tests/test_operation_contract_run.py::test_same_size_modification_during_read_stops` | 1 | 成功 | 0 |
| `.venv/bin/python3 -m pytest -q tests/test_operation_contract_run.py::test_nul_and_surrogate_paths_stop_before_reading` | 2 | 成功 | 0 |
| 機微pattern 3規則を実行時に除去した対象試験 | 67 | 3件失敗、64件成功 | 1 |
| `.venv/bin/python3 -m pytest -q tests/test_operation_contract_run.py` | 67 | 成功 | 0 |
| `.venv/bin/python3 -m pytest -q tests/test_one_design_acceptance.py` | 107 | 成功 | 0 |
| `.venv/bin/python3 -m pytest -q tests/test_one_requirement_feature_source.py` | 111 | 成功 | 0 |
| `.venv/bin/python3 -m pytest -q tests/test_one_item_review.py` | 158 | 成功 | 0 |
| `.venv/bin/python3 -m pytest -q tests/test_first_review_task_contract_e2e.py` | 38 | 成功 | 0 |
| 依頼record §4の認証環境値を外した`.venv/bin/python3 -m pytest -q` | 2,305 | 成功 | 0 |

## 6. Human境界、未実施、次

【実測】再レビュー中に訂正commitの成果物、契約、既存record、再利用部品を変更していない。反証は試験の
一時領域だけを使用した。外部送信、push、製品受入、後続縦切り、既存recordの修正は実施していない。

【判断】Human境界は維持した。利用者による製品受入は未実施であり、本判定の範囲外である。

【提案】次の一作業は、Claudeが本判定recordとcommitの変更範囲を事後照合し、利用者による製品受入の判断へ
渡すことである。
