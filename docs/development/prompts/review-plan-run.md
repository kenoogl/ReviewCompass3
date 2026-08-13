# 機械的レビュー計画の入口

レビューの対象、確認項目、独立レビュー担当の有無、最大周回数は、LLMではなく次の入口で生成する。

```text
reviewcompass3-review-plan \
  --base-commit <作業開始commit> \
  --target-commit <確認対象commit> \
  --risk <low|medium|high> \
  --stage <scope|completion> \
  --classification <対象分類JSON>
```

対象分類JSONは、次の形で変更pathと対象種別を一対一に対応付ける。対象path自体は二つのcommitの
Git差分から生成し、分類入力で追加または除外しない。

```json
{
  "schema_version": 1,
  "targets": [
    {"path": "docs/example.md", "kind": "documentation"},
    {"path": "tools/example.py", "kind": "validator_code"}
  ],
  "actions": ["semantic_adjudication"]
}
```

対象種別は`documentation`、`product_code`、`test_code`、`validator_code`、`configuration`、
`structured_data`の六つである。未分類path、余分なpath、未知の対象種別は出力に警告として残るが、
終了コードは0のままである。読めないJSON、重複path、絶対path、親directory参照、型不正は、
不正な入力として終了コード2になる。

外部送信、不可逆操作、意味的裁定、段完了は`actions`へ記し、既存の利用者承認条件へ接続する。
path、担当数、周回数を追加指定する入口は持たない。出力の`plan_sha256`へ束縛された計画だけを
後続処理へ渡す。

この入口は計画生成だけを行う。LLM起動、Claude起動、認証、外部送信、レビュー結果の裁定は行わない。
