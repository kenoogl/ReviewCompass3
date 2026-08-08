# 共通関数化（B/D/E系統）GREEN Evidenceと統合レーン結論 v1

- 実施：2026-08-08。根拠：`DEC-SHARED-FUNCTION-POLICY-001`。着手指示はHuman「次へ」（誤入力「町」の
  確認停止を挟み「打ち間違い。進め」で再開）
- TDD：RED 18件（commit `dcb3f0c`）→実装→**全suite 1238 passed**【実測・単独実行】

## 1. 実施内容

| 系統 | 正本 | 結線 |
| --- | --- | --- |
| B（fail-closed例外） | `tools/common/errors.py`の基底`FailClosedError`（`if detail`判定を逐語踏襲） | 7クラスを継承1行へ（クラス名・docstring維持＝捕捉の意味を保存。`__init__`削除） |
| D（path境界判定） | `tools/common/paths.py`の`within` | 4fileの`_within`をaliasへ |
| E（JSON印字） | `tools/common/output.py`の`print_json` | 3定義をaliasへ（`todo_update_path`の入れ子`_report`はmodule水準のaliasへ引き上げ） |

- テスト18件：基底の挙動（detail有無・空文字）、7クラスの継承と`__init__`非再定義の固定、
  `within`挙動と4結線の同一性、印字のcanonical出力と3結線の同一性

## 2. 既存テスト2件の理由記録つき更新

`python_ast_boundary_check`と`task_python_cache`には「importは最小限」という設計不変条件を
固定するテストが存在し、正本への結線と衝突した。複製禁止方針（Human決定）を優先し、
**許可集合へ`tools.common.errors`だけを追加**する形で更新（実行系・外部processを持ち込まない
という不変条件の趣旨は維持）。

## 3. 統合レーンの結論（総括record `45438e4c…` を方針転換で上書き）

- 実施済み：digest系（10定義）＋B/D/E系統（14定義）を`tools/common/`の正本4moduleへ一元化。
  **F系統は対象外**（処理を持たない入れ物。形の一致は役割の異なる正当な構造）
- 残置：`todo_snapshot.py`の`_sha256`1件（凍結契約のfile指紋固定。出力一致テストで監視、
  凍結解除はHuman判断）
- 前提の規律：意図的な複製の禁止・reuse-search台帳の事前確認・module起動統一（AGENTS.md明文化済み）

## 4. 残作業（次の作業単位）

- **反証レビュー`high`**：共通化の変更一式（digest＋B/D/E、守り役含む計19file＋正本4module）。
  評価②手順7の必須条件であり未実施。観点：結線の迂回（localで再定義できるか）、基底変更の
  波及、正本の変更がHuman承認なしに通らないか、alias越しの挙動差
- checklist Work 4B 3項目目への反映は本Evidenceを根拠に実施
