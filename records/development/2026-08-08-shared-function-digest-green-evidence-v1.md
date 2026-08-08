# 共通関数化（digest系）GREEN Evidence v1

- 実施：2026-08-08。根拠：`DEC-SHARED-FUNCTION-POLICY-001`（複製禁止・共通関数化・module起動統一）
- TDD：RED 13件（commit `766b0a5`）→実装→**全suite 1220 passed**【実測・単独実行】

## 実施内容

1. 正本新設：`tools/common/digests.py`（`sha256_hex`・`canonical_content_digest`。
   最小・安定・標準libraryのみ・変更はHuman承認）
2. **10定義を正本へ結線**（写しを削除しimport 1行へ。A系6file＋C系4file。呼び出し47か所・
   既存テストは無修正）。`todo_snapshot.py`のみ凍結契約のfile指紋固定により残置し、
   出力一致テストで守る
3. **起動方式の統一**：生きている5文書のcommand記載9か所を`python3 -m`形式へ書換え
   （AGENTS.md・TODO手順書・checklist・development-policy・TODO template）。歴史recordは不変更
4. AGENTS.md機械規律へ2規則を明文化：意図的な複製の禁止（reuse-search台帳確認→`tools/common/`へ
   一元化）、module起動統一（sys.path定型の複製も禁止）
5. テスト：正本の独立oracle検算・結線の同一性固定（`is`照合10件）・残置写しの出力一致・
   **`-m`起動の実機動作2件**（前回の破壊を恒久検出する回帰テスト）。
   分岐検出テスト（前方針）は後継テストへ置換。文書の期待文字列テスト1件を理由記録つき更新
6. 連鎖Digestの追随：development-policy改定→checklist front matter→TODO Evidence欄

## 検証【実測・単独実行】

全suite 1220 passed／`-m`起動2経路の実機確認（テスト内subprocess）／`git diff --check`合格
