# ReviewCompass3

ReviewCompass3は、仕様駆動開発の成果物、レビュー、判断と一次証拠を結び、
人が根拠を確認しながら開発を進めるための支援システムです。

## 現在地

第5段の設計・ブートストラップ適合性監査までの候補成果を保持しています。
段完了のHuman判断後は、新しい抽象基盤を増やす前に、決定的なstub reviewerを
用いた最小E2E縦切りへ進みます。

Task ContractをRequirementsとRuntimeのcontrol and provenance planeとする後継方針を
現在レビューしています。この候補は旧第5段成果を上書きせず、Task Contract単位のTDD、
契約間統合、評価可能なProvenance、配置非依存のdeploymentを追加します。

- 後継候補の索引：`docs/README.md`
- 初期変更記録：`records/task-contract/task-contract-centered-documentation-v1.json`
- 開発レーン改定記録：`records/task-contract/task-contract-centered-documentation-v2.json`
- LLMGP先行実験の反映記録：`records/task-contract/task-contract-centered-documentation-v3.json`

## 開発方針

開発はSDDとリスクベースのテストファーストで進めます。振る舞いの変更には
関連テストを先行または同一変更内で用意し、統合対象のコミットは原則として
緑に保ちます。高コストな検証とHuman承認は、リスクと判断責務に応じて適用します。

- 方針正本：`docs/development/2026-08-02-development-policy.md`
- 実行設定：`config/development-policy.json`
- 再構築計画の改定：`docs/plan/2026-08-02-development-policy-amendment.md`
- intentの改定：`docs/intent/2026-08-02-development-policy-amendment.md`

上記の固定方針とbaselineに対するTask Contract中心化の差分は、後継候補の索引から
参照します。Human承認と差分監査が完了するまでは、後継候補を承認済み正本として
扱いません。

## テスト

```shell
python3 -m pytest -q
```
