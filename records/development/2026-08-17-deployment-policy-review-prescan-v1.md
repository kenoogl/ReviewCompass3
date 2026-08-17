# デプロイ方針再検討 事前走査 v1

- 記録日：2026-08-17
- 指示者：利用者（Human）。選択文言：「デプロイ設計の再検討を新しい作業単位として範囲を相談
  したい」→範囲3案の提示後「案2で進める。メモ取り込み→事前走査→論点整理の提示まで」
  （いずれも2026-08-17 chat）
- 記録者：Claude
- 種別：**方針検討（文書のみ）の事前走査**。scope-prescan-run.mdの6手順のうち所在特定・
  接続点・digest固定を適用。手順5（正式再利用検索）は適用外——開発方針123行の適用条件
  「新しい処理の追加または既存処理の変更」に該当しない（成果物は方針Decision recordの見込み）
- 範囲：案2＝メモ取り込み→棚卸し→論点整理→論点別Human裁定→方針Decision record固定。
  設計書起草・実装・要求権限束の改定は含まない
- 基準commit：`3f7f3d0`（メモ取り込みcommit・作業tree clean）

## 0. 一枚要約（人向け）

repo外の検討メモ（Task Runtime Platform＋Task Package登録構想）は、**計画正本
`docs/current/reviewcompass3-plan-current.md`へ既に消化・置換済み**だった——§11.4が配布・更新
単位を4分割（Runtime Core／Integration Client／Capability Adapter／Project Artifacts）で定め、
「元検討のTask Package／Task Registryはこの二分へ置換し、任意codeをloadするplugin systemや
汎用Task orchestrationは初期範囲へ入れない」と明記。§11.5はstable／development bootstrap
（別code・Manifest・state・data root、staging root、migration dry-run、rollback）を規定。
§4.7はPortable Lifecycle 4要件（`REQ-PORTABLE-001`〜`004`）を持つ。**残る問題は設計の不在では
なく、(1) これらが要求権限束（現行50要求）へ未昇格、(2) 現実体が未実装（単一パッケージ・
分離なし）、(3) 昨日新設の`record_run.py`だけが絶対パス固定という可搬性の穴、の3点**である。

## 1. 手順1：所在特定（棚卸し）【実測】

| 資産 | 所在 | 状態 |
| --- | --- | --- |
| 検討メモ（取り込み済み） | `docs/design/2026-08-17-deployment-method-consideration-import-v1.md`（原文SHA-256一致の機械証明つき・commit `3f7f3d0`） | 時点検討の記録。固定入力化済み |
| 概念正本 | `docs/concepts/2026-07-27-task-runtime-concept.md` | 「現行実装は固定bootstrapレビューpipelineであり汎用Task Runtimeではない」と不足10点を列挙。後続の進め方（intent→requirements→design→既存実装を`conformant/adapt/replace/defer`分類）を規定 |
| 計画正本の配布規定 | `docs/current/reviewcompass3-plan-current.md` §4.7（Portable 4要件）・§11.4（配布・更新単位の4分割とTask Package構想の置換裁定）・§11.5（stable／dev bootstrap） | **設計方針は既定**。権限束へ未昇格 |
| 要求権限束v2 | `records/requirements/authority/rc3-requirements-authority-2026-08-03--v2.json` | 配布・デプロイ関連の語の出現0（機械確認）。REQ-PORTABLE系は未昇格 |
| 配置の実装資産 | `tools/deployment/local_integrated_roots.py`（4種root分離：install／project／runtime／sensitive。Layout Baseline v3が唯一のauthority）・`checkout_relocation.py`・`trusted_claude_transport.py`（固定配布物の配置検査）・`tools/layout/baseline.py` | 部分実装あり（Work 7A・Work 1A） |
| 現在の配布形 | `pyproject.toml`：単一パッケージ・CLI 16件登録・依存2件のみ（PyYAML・platformdirs）・Python>=3.9 | 技術的な配布障害は小さい |
| 可搬性の穴 | `tools/session_logs/record_run.py`のみ絶対パス固定4箇所（`DEFAULT_SYSTEMS`・`DEFAULT_PRIVATE_ROOT`。2026-08-17新設） | tools配下で`/Users/`固定はこの1 fileだけ（機械検索） |

## 2. 手順4：接続点【実測】

1. 計画正本§11.4・§11.5・§4.7——本作業の方針裁定はこの既定の**確認・昇格・着手順の決定**で
   あり、新設計の起草ではない。
2. 概念文書の「後続段への送り」——API境界・Registry意味情報などはTask Runtimeの
   requirements／design段の主題として送られており、デプロイ方針で先取りしない接続が自然。
3. `record_run.py`（契約014系・受入済み）——絶対パスの設定化は同fileの小改定になる（着手時は
   通常の変更手続き）。
4. レビュー基盤module（休止）・session log系（完了）——本作業はどちらでもない第3の主題。
5. G30運用契約——§11.4のCapability Adapter概念に将来接続（本作業では変更しない）。

## 3. 手順5：正式再利用検索——適用外【記録】

成果物は方針Decision record（文書）の見込みでコード変更なし。適用条件に該当しない。
着手範囲が実装（例：絶対パス設定化）へ及ぶ場合は、その作業単位で改めて判断する。

## 4. digest表（論点整理・方針Decisionの固定入力）【実測】

```text
be59d427f26312b172a04fbbe28de3650ed4d547355d469b2af50c4c754a4968  docs/design/2026-08-17-deployment-method-consideration-import-v1.md
be501be50b04cd327e97cbd2ea3e3b26082065144c43a36f3e3899e12c4dba13  docs/concepts/2026-07-27-task-runtime-concept.md
1a73597605eafb65a2259ccf19431e3aba041564d03fdb279150042a9bd0962f  docs/current/reviewcompass3-plan-current.md
31e4e319c366cfbf51d58b691c11bdf6fb7c43636ac9ad3bfa7777c43cb5a149  tools/deployment/local_integrated_roots.py
c34ed2ceb3ec37e36065cd43fb852d0bc2879bfbf184293e45f0ec3595fac0d2  tools/deployment/trusted_claude_transport.py
2a81b11d1355f5bcde1381ff40dd9cd9337781e2719cbb696befc5d60d44eed1  tools/deployment/checkout_relocation.py
1e240112be0152af433061171cc2418632b565e080442a6182bd36a3e3969a97  tools/layout/baseline.py
a7b37a45c72ceba50e4ebf28c3f3039a9bc89dd1f1712d55bccb4ac764b2ef87  pyproject.toml
a3ddec9c2e2152cd72408bfa96da4b56a4810529f36846ed885f14a691ca220e  tools/session_logs/record_run.py
760e33ea2ecf6937f56d7bf8d2bd703b18b47dbd2bd6b2bd5919e0dd556d9dae  records/requirements/authority/rc3-requirements-authority-2026-08-03--v2.json
```

## 5. 論点整理へ渡す発見【記録】

1. 「設計の再検討」の実態は「既定方針（§4.7・§11.4・§11.5）の確認と、昇格・着手順の裁定」。
2. 検討メモとcurrent planの残差はTask Package／Registry構想の置換裁定（§11.4）に集約される。
3. 可搬性の現状は良好（絶対パス固定1 file・依存2件）で、実装の第一歩は小さく切れる。
4. stable／dev分離（§11.5）は規則（AGENTS.md §4「自己適用はstable機能だけ」）はあるが物理分離が
   未実装。
5. デプロイ先の想定（ローカルのみ／研究室サーバ視野）は要求前提のHuman裁定で、権限束昇格の
   範囲を決める。

## 6. 未実施

- 論点別Human裁定、方針Decision record v1の作成、（その後の）権限束改定・設計書・実装。
