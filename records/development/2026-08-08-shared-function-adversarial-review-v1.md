# 共通化一式 反証レビュー結果 v1（的中あり・処置裁定待ち）

- 実施：2026-08-08。着手指示はHuman「実行」。対象：digest＋B/D/E共通化（19file＋正本4module）
- 方法：`work-review-protocol` §3 `high`。攻撃観点の初手「再発明の残存」をrepository全体の
  pattern走査で実施した【実測】

## 1. 的中した所見

| ID | 所見 | 実測 |
| --- | --- | --- |
| I-1 | **canonical digest計算の写しが7file残存**。共通化の対象列挙が順位表上位20組由来で、repository全体を網羅していなかった | `todo_compaction`・`operation_routing`・`issue_resolution_pilot`・`issue_resolution_post_write`・`work4a_rebuild_v3`・`task_contract/identity`・`todo_snapshot`（凍結）に`if key != "content_digest"`の同型が残存。整形違い（複数行／1行／補助関数経由）はあるが意味は同一 |
| I-2 | **`_within`の写しが1file残存** | `tools/session_logs/config.py:50`（D系統の列挙4fileに含まれず） |
| I-3 | **file指紋計算（`sha256(Path(path).read_bytes())`）が5か所で同型** | `reuse_search_record`・`candidate_ranking`・`integration_exclusions`・`work4a_rebuild_v3`・`identity`。共通化には正本への新関数`file_sha256`の追加が必要＝**Human承認事項**（DEC-SHARED-FUNCTION-POLICY-001） |
| I-4 | **根本原因**：対象列挙が候補順位表（上位20）に依存し、複製禁止の検査がrepository全体のpattern走査になっていなかった | 本レビューの走査手順そのものが検出器として機能した |

## 2. 未実施の攻撃観点（処置と同じ単位で実施予定）

結線迂回の恒久走査（再発明検出テスト）、正本4moduleの指紋pin（変更にHuman承認記録を強制）、
例外の兄弟隔離（`except IntakeError`が他moduleの例外を誤捕捉しないこと）、`-m`起動到達の恒久テスト
（本日の手動確認8moduleをテスト化）、file直接起動の残存走査のテスト化。

## 3. 処置案（裁定待ち）

1. **I-1処置**：編集可能な6fileのcanonical写しを`canonical_content_digest`へ結線
   （todo_snapshotは凍結残置。pilotは凍結symbol行範囲452行以降と非交差を機械確認のうえ実施）
2. **I-2処置**：config.pyの`_within`を`within`へ結線
3. **I-3処置**：正本`tools/common/digests.py`へ`file_sha256(path)`を**追加**（Human承認が必要）し、
   5か所を結線
4. **I-4処置**：§2の恒久テスト一式を追加（再発明の走査・pin・兄弟隔離・起動到達・直接起動残存）
5. 残置の全量（todo_snapshotの`_sha256`・canonical・`file_sha256`相当）は凍結解除時に一括追随

## 4. 境界

- 本recordは所見の固定であり、処置の実施はHuman裁定による
