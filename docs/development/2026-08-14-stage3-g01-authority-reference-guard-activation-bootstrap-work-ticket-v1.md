# 第3段 G01権威参照検査の現役接続 軽量作業票 v1

- 作成日：2026-08-14
- 基準commit：`8772630`
- 対象Issue：`ISSUE-TEST-GROWTH-STATE-PINNING-001`
- 関連Issue：`ISSUE-AUTHORITY-REFERENCE-DIGEST-CHECK-001`
- 利用者承認：2026-08-14、G01再評価Evidenceの案Cを「承認」
- 危険度案：高。他の文書の現在有効性を判定する守り役コードを現役化する。ただし外部送信、権限変更、不可逆操作はない
- 作業担当：操縦役
- 開始前レビュー担当：新規サブエージェント一者
- 完了レビュー担当：開始前レビューと異なる新規サブエージェント一者
- 外部モデル確認：行わない。第3段完了前の一回を残す

## 1. 目的

現在能力を持つが正式接続されていない権威参照検査を、既存の正規全試験へ接続する。同時に、同じ欠陥を
確認する重複2入力を、現行19件が見逃す2境界へ入れ替える。新しい検査器、台帳、設定、関門は作らず、
Human承認済みの初期開発チェックリストと現行Planだけを通常の検査対象とする。

## 2. 入力と根拠

- `records/development/2026-08-14-stage3-g01-authority-reference-reassessment-evidence-v1.md`
  - SHA-256：`995b90e03a4d7c9cc29bb26b9a896df1610cec0a1524a086e009012ced28f7a8`
- `records/development/2026-08-14-stage3-g01-authority-reference-reassessment-independent-completion-review-v1.md`
  - SHA-256：`56f2a5a12f674ffbe39beb4d5956050c7f3d98c1f59d70e5978e7e3f5c47cd92`
- `records/session-handoffs/2026-08-10-claude-pilot-reference-digest-checker-scope-v2.md`
- `tools/development/authority_reference_checker.py`
- `tools/development/authority_reference_keys.json`
- `tests/test_authority_reference_checker.py`
- `docs/development/2026-08-03-initial-development-checklist.md`
- `docs/current/reviewcompass3-plan-current.md`
- 正規全試験入口`tools.development.policy_test_runner --suite full`

## 3. 三つの実装案と選択

| 案 | 内容 | 簡潔さ | 記憶・実行資源 | 頑健さ | 保守性 | 判断 |
| --- | --- | --- | --- | --- | --- | --- |
| A 使用停止 | 検査コード、許可一覧、19件を削除し、履歴だけを残す | 現行コードは最小 | 最小 | 既知の参照ずれを通常作業で検出できない | 再発時に手作業へ戻る | 不採用 |
| B 手動案内 | 現行コードと19件を維持し、既存文書へ手動commandだけを追記する | 変更は小さい | 現状同等 | 実行忘れを防げず、不足2境界も残る | 暫定状態が続く | 不採用 |
| C 既存全試験へ接続 | 合成正常例を実文書2件へ置換し、重複2入力を不足2境界へ入れ替え、例外処理だけを直す | 既存2コードpath内で完結 | メモリ差は実質なし。実行時間は中心理由にしない | 正規全試験が実文書ずれと不足境界を検出する | 大きな合成fixtureを除き、利用先が明確になる | 採用 |

【判断】案Cを採用する。中央の作業遷移処理へ新しい関門を追加する案、設定fileを新設する案、全Markdownを
自動探索する案は、結合範囲と誤拒否を増やすため採用しない。

## 4. 作業範囲と対象外

変更可能pathは次の3件だけとする。

- `tests/test_authority_reference_checker.py`
- `tools/development/authority_reference_checker.py`
- `records/development/2026-08-14-stage3-g01-authority-reference-guard-activation-evidence-v1.md`

試験変更は次へ限定する。

- 合成の7キー正常fixtureと、そのfixtureだけが使う補助処理を削除する。
- 正常例は、Human承認済みの実文書2件・11参照を既存検査コードで照合する形へ置き換える。
- 許可キー行の同居値4入力を、単一参照形式と複数参照形式の各1入力へ縮める。
- 不正経路の既存入力表へNUL文字を1入力追加する。
- 空参照の既存入力表へ、正常文書と参照0件文書を同時に渡す1入力を追加する。

検査コード変更は次へ限定する。

- 経路の生成または解決が出す`ValueError`と`OSError`を、既存の`invalid`判定へ写す。
- 冒頭の状態宣言を、暫定から現役の運用検査へ変更する。

許可一覧、実文書、設定、TODO、Issue、既存Evidence、中央の作業遷移処理、他の試験は変更しない。
全Markdown探索、新しい検査器・台帳・設定・関門、外部送信、Claude確認、別群、第3段完了判断は対象外とする。

## 5. TDDの順序

1. 対象試験だけを変更する。検査コードは変更しない。
2. 単独実行し、新しいNUL文字の境界だけが、現行実装の例外により失敗することを確認する。
3. 試験変更だけをRED commitとして固定する。
4. 試験を変更せず、検査コードの例外処理と状態宣言だけを変更する。
5. 対象19件と実文書2件の単独検査を成功させる。
6. リポジトリ外の一時複製で、実文書Digestずれ、同居値拒否、複数入力中の空参照、NUL文字の4条件を反証する。
7. 正規全試験、Evidence、独立完了レビューへ進む。

## 6. 期待する成果

- G01は引数展開後19件を維持するが、大きな合成正常fixtureを実文書照合へ置き換え、試験fileの構造を小さくする。
- 正規全試験が初期開発チェックリスト8参照と現行Plan 3参照のずれを検出する。
- 複数文書の一部だけが空の場合とNUL文字経路を既存試験が検出する。
- 検査コードは`active`（現役）・`operational-guard`（運用上の守り役）として、現在利用先を正規全試験と説明できる。
- 変更成果物を`現在の動作保証`、Evidenceとレビュー記録を`履歴・監査資料`へ分類できる。

## 7. 機械確認

- RED：`.venv/bin/python3 -B -m pytest -q tests/test_authority_reference_checker.py`
- 実文書：`.venv/bin/python3 -B -m tools.development.authority_reference_checker docs/development/2026-08-03-initial-development-checklist.md docs/current/reviewcompass3-plan-current.md`
- 正規全試験：`.venv/bin/python3 -B -m tools.development.policy_test_runner --project-root . --suite full --receipt <repository外path>`
- 一時変異：実文書Digest一文字変更、同居値拒否分岐の無効化、文書ごとの空参照判定の無効化、NUL文字入力
- 参照と件数：`rg`、Python構文木、`pytest --collect-only`
- 成果物：SHA-256、再読込み、`git diff --check`、commit後のGit物体照合

## 8. レビューで判断する事項

- 実文書2件の明示列挙が元のHuman承認範囲と一致し、全Markdown探索へ広がっていないか。
- 合成正常fixtureの削除が、実文書2件・7キー・11参照で同じ正常保証を維持するか。
- 重複2入力の削除と不足2境界の追加が、件数合わせではなく検出能力の改善になっているか。
- 例外処理がNUL文字だけの場当たり対応でなく、経路生成・解決の不正を既存`invalid`へ写す最小境界か。
- 状態宣言と実際の利用先が一致するか。
- 新しい仕組みや中央関門を追加していないか。
- 実行時間ではなく、接続、理解、変更、復旧、誤判定の総費用で案を選んでいるか。

## 9. 停止条件と完了条件

停止条件：

- 変更可能3 path以外の変更が必要になる。
- REDがNUL文字の既知例外以外で失敗する。
- 実文書2件以外を正式対象へ加える必要が判明する。
- 許可一覧、設定、中央関門、Issueの同時変更が必要になる。
- 元の19件、実文書、正規全試験、4反証のいずれかが不合格になる。

完了条件：

- RED commitでは試験fileだけが変わり、NUL文字境界だけが失敗する。
- GREEN中に試験を変更せず、検査コードの限定修正だけで19件が成功する。
- 実文書2件・11参照が成功し、正規全試験が成功する。
- 4条件の反証を既存試験または実文書検査が検出する。
- 変更範囲、現在利用先、守る性質、四分類がEvidenceに記録される。
- 一回の独立完了レビューが`verified`と判定する。
- Issue状態反映と第3段完了判断を別作業へ残す。
