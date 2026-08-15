# 最小運用契約実行 実装成功Evidence v1

- 実施日：2026-08-16
- 契約：`TC-RC3-PRODUCT-MINIMAL-OPERATION-CONTRACT-EXECUTION-006 / v4`
- 採用経緯：v3採用judgment（`records/development/2026-08-16-minimal-operation-contract-execution-adoption-decision-v1.md`）
  の条件付き事前承認の下、v4訂正（操作名除外）はCodex限定再確認`開始可`（blocking 0件）で確認済み。
  v4判定record：`records/development/2026-08-16-minimal-operation-contract-execution-v4-limited-rereview-v1.md`、
  単独commit `a5377a1020b344f9a303ac09bded2d02920a14e6`
- 実装担当：Claude
- 方式：テスト駆動（失敗試験の固定→最小実装）

## 1. 失敗試験の固定（RED）と契約欠陥の発見

【実測】対象試験`tests/test_operation_contract_run.py`を先に作成し、単独実行で58件失敗・1件合格
（合格は実装不要の部品内容識別値照合）を確認し、commit `fd24453`へ固定した。

【実測】最小実装後の正例試験で、契約v3の定義欠陥を発見した。固定操作名`requirement_candidate_check`
（27文字）が§8.2の高乱雑性検査へ乱雑さ3.63で一致し、G24操作の正例が必ず機微停止する。契約候補v4で
`/operation`位置の固定registry操作名だけの限定除外（手順3b）を追加し、Codex限定再確認で`開始可`を得てから
実装を再開した。失敗試験を先に固定する進め方が、契約の穴を受入前に露見させた。

## 2. 最小実装（GREEN）

【実測】契約§12の変更上限内で次を実装した。

1. 実行核 `tools/operations/operation_contract_run.py`（新規package `tools/operations/`）
2. 入口 `tools/operations/operation_contract_run_entry.py`
3. `pyproject.toml`へ実行名`reviewcompass3-operation-run`一件を追加
4. 対象試験へv4準拠の3試験（操作名の非停止・非registry操作名の非除外・短い契約IDの正例）を追加し61件とした

書込み境界は契約§7どおり、一時名`*.partial`の新規作成→bytes再読込照合→hard linkによる上書き不能な
原子公開→一時名削除の二段で実装した。公開確定後の削除失敗は`partial_cleanup_failed`（終了コード6）で停止する。

## 3. 機械確認（各単独command・終了コード個別判定）

【実測】

- 対象試験：61件成功、終了コード0（書込み反証16b・16c、部品停止転記、束縛不一致、機微6種を含む）
- G08対象：107件成功、終了コード0
- G24対象：111件成功、終了コード0
- G02対象：158件成功、終了コード0
- G30基盤e2e：38件成功、終了コード0
- 再利用・保護path（基準commit `bb55a1f`からの差分）：差分0、終了コード0
- 正規全試験（既存の禁止認証隔離条件）：2,299件成功、終了コード0
- `git diff --check`：終了コード0

## 4. 合成一件E2E（受入条件17・21）

【実測】`pip install -e .`で配置した正式実行名`reviewcompass3-operation-run`を、repository外の現在位置
`/private/tmp/g30-e2e/outside`から実行した。終了コード0、標準エラー0 bytes。

- 運用契約：`OC-E2E-G30`、操作`requirement_candidate_check`、`human_approved: true`
- 実行記録が`out/OC-E2E-G30--execution-v1.json`へ着地し、標準出力と完全一致（`stdout==file: True`）
- 束縛照合：catalog・candidateとも期待値と部品報告値が一致
- 契約内容識別値：`31f12148bf5dabb484bd5dd012a60b53128c129c2735b78640314d2b43b26d3d`
- 実行記録内容識別値：`a3839a373d855222b4c7732cb48ceb5ba535633d5ba2f05918deedbe0f744781`
- 部品verdict：`trace_complete_pending_human_decision`を無変更で埋め込み、`decision_status: pending_human_decision`
- 一時名`*.partial`の残留なし。出力rootには最終名一件だけ

## 5. 受入条件の対応

【実測】受入条件1〜17は対象試験61件が覆う。18・19は§3の各単独commandで確認した。20の独立完了レビューと
21の合成提示・22の利用者受入のうち、レビューと受入は未実施の後続である。

## 6. 未実施

- 独立完了レビュー（受入条件20、Codex）
- 利用者の製品受入（受入条件22）
- G02操作の追加、G25・安全保存統合、複数操作の連鎖、既存G30基盤の正式化（後続縦切り）
