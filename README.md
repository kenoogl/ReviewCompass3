# ReviewCompass3

ReviewCompass3は、仕様駆動開発の成果物、レビュー、判断と一次証拠を結び、
人が根拠を確認しながら開発を進めるための支援システムです。

## 現在地

第5段の設計・ブートストラップ適合性監査までの候補成果を保持しています。
段完了のHuman判断後は、新しい抽象基盤を増やす前に、決定的なstub reviewerを
用いた最小E2E縦切りへ進みます。

## 開発方針

開発はSDDとリスクベースのテストファーストで進めます。振る舞いの変更には
関連テストを先行または同一変更内で用意し、統合対象のコミットは原則として
緑に保ちます。高コストな検証とHuman承認は、リスクと判断責務に応じて適用します。

- 方針正本：`docs/development/2026-08-02-development-policy.md`
- 実行設定：`config/development-policy.json`
- 再構築計画の改定：`docs/plan/2026-08-02-development-policy-amendment.md`
- intentの改定：`docs/intent/2026-08-02-development-policy-amendment.md`

## テスト

```shell
python3 -m pytest -q
```
