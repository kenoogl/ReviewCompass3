# ReviewCompass3

ReviewCompass3は、仕様駆動開発の成果物、レビュー、判断と一次証拠を結び、
人が根拠を確認しながら開発を進めるための支援システムです。

## 現在地

第5段の設計・ブートストラップ適合性監査までの候補成果を保持しています。
段完了のHuman判断後は、新しい抽象基盤を増やす前に、決定的なstub reviewerを
用いた最小E2E縦切りへ進みます。

Task ContractをRequirementsとRuntimeのcontrol and provenance planeとする後継方針を
現在レビューしています。この候補は旧第5段成果を上書きせず、Task Contract単位のTDD、
契約間統合、評価可能なProvenance、配置非依存のdeploymentを追加します。review入力は、
文書全体ではなく変更から導出した影響閉包と必須材料に応じて構成する方針です。

- 後継候補の索引：`docs/README.md`
- Intent統合最新版：`docs/current/reviewcompass3-intent-current.md`
- 統合用語集：`docs/current/reviewcompass3-glossary-current.md`
- 計画統合最新版：`docs/current/reviewcompass3-plan-current.md`
- 初期変更記録：`records/task-contract/task-contract-centered-documentation-v1.json`
- 開発レーン改定記録：`records/task-contract/task-contract-centered-documentation-v2.json`
- LLMGP先行実験の反映記録：`records/task-contract/task-contract-centered-documentation-v3.json`
- 旧第5段設計の継承記録：`records/task-contract/task-contract-centered-documentation-v4.json`
- 共通ルーチン台帳の継承記録：`records/task-contract/task-contract-centered-documentation-v5.json`
- Issue→Plan経路の計画反映記録：`records/task-contract/task-contract-centered-documentation-v6.json`
- 実装文書projectionの計画反映記録：`records/task-contract/task-contract-centered-documentation-v7.json`
- Intent・計画統合最新版の生成記録：`records/task-contract/task-contract-centered-documentation-v8.json`
- Intent平易化の変更記録：`records/task-contract/task-contract-centered-documentation-v9.json`
- AIへの判断委譲方針の変更記録：`records/task-contract/task-contract-centered-documentation-v10.json`
- AI判断委譲計画の変更記録：`records/task-contract/task-contract-centered-documentation-v11.json`
- ReviewCompass3用語統制の変更記録：`records/task-contract/task-contract-centered-documentation-v12.json`
- デプロイtopology継承の変更記録：`records/task-contract/task-contract-centered-documentation-v13.json`
- 変更規模比例review入力の補強記録：`records/task-contract/task-contract-centered-documentation-v14.json`
- ReviewCompass2横断知見の反映記録：`records/task-contract/task-contract-centered-documentation-v15.json`
- 全出典の保持・再構築状態：`records/sources/2026-08-02-source-catalog.json`
- 文書revision再構築可能性監査：`records/task-contract/2026-08-02-documentation-reconstructability-audit.json`
- 整合性修正記録：`records/task-contract/task-contract-centered-documentation-v16.json`

## 開発方針

開発はSDDとリスクベースのテストファーストで進めます。振る舞いの変更には
関連テストを先行または同一変更内で用意し、統合対象のコミットは原則として
緑に保ちます。green実装前には既存関数と共通ルーチン台帳を照合し、再利用、拡張、
統合または理由付き分離を判断します。高コストな検証とHuman承認は、リスクと判断責務に
応じて適用します。

最初の製品実装より前にlogical root、相対参照、Manifest、BindingをLayout Baselineとして
固定します。続いてbootstrap中の議論と判断を残すSession Log Bootstrapを準備します。その配置を
基準に全関数・methodのSource Symbol IndexとReusable Routine Ledgerの初期版を整備し、coverageと
freshnessを確認してから最小E2Eへ進みます。

- 方針正本：`docs/development/2026-08-02-development-policy.md`
- 実行設定：`config/development-policy.json`
- 実装記録：`records/development/development-policy-v2.json`
- 再構築計画の改定：`docs/plan/2026-08-02-development-policy-amendment.md`
- intentの改定：`docs/intent/2026-08-02-development-policy-amendment.md`

上記の固定方針とbaselineに対するTask Contract中心化の差分は、後継候補の索引から
参照します。Human承認と差分監査が完了するまでは、後継候補を承認済み正本として
扱いません。

## テスト

```shell
python3 -m pytest -q
```
