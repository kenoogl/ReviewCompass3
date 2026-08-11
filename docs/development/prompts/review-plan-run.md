# 機械的レビュー計画の入口

レビューの対象、確認項目、独立レビュー担当の有無、最大周回数は、LLMではなく次の入口で生成する。

```text
reviewcompass3-review-plan \
  --base-commit <作業開始commit> \
  --target-commit <確認対象commit> \
  --risk <low|medium|high> \
  --stage <scope|completion>
```

対象pathは二つのcommitのGit差分から生成する。path、担当数、周回数を追加指定する入口は持たない。
出力の`plan_sha256`へ束縛された計画だけを後続処理へ渡す。

この入口は計画生成だけを行う。LLM起動、Claude起動、認証、外部送信、レビュー結果の裁定は行わない。
