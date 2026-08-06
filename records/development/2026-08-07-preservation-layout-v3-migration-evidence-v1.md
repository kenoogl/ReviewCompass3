# セッションログ書庫 Layout v3移行 Evidence v1

- 承認Decision：`DEC-PRESERVATION-LAYOUT-V3-MIGRATION-001`
  （`records/development/2026-08-06-preservation-layout-v3-migration-decision-v1.md`、SHA-256
  `b9aa5bc3bc2f6324e42032d3537e3b96f48a63e44c19f530dddafbcf0054843e`）
- Migration Receipt：`records/development/2026-08-07-preservation-layout-v3-migration-receipt-v1.json`
  （SHA-256 `29a3af432c408e8f479a747706cc8ce406c9c7d123c95d02cbb4f02719235914`）
- 実行時刻：2026-08-07T00:53:21+09:00
- 実行環境：Python 3.9.6、pytest 8.4.2、venv公式runner、fallback `false`

## 0. 範囲の明示

セッションログ書庫を旧OS標準配置から現行Layout v3のdevelopment profile sensitive root配下へ
**byte-exactに移行し、active archiveを切り替えた**。旧書庫は**変更も削除もせず**rollback copyとして
保持している。本Evidenceはvalue-safeであり、会話本文とhome絶対pathを含まない。

## 1. 時間関係（既存recordから確認）

| 時刻 | 出来事 |
| --- | --- |
| 2026-08-04T00:51:19+09:00 | 旧Storage DecisionがOS標準data rootを承認 |
| 2026-08-04T15:30:44+09:00 | Layout v3承認（既存dataの移行は当時の承認対象外と明記） |
| 2026-08-06T09:13:46+09:00 | 再記録Decisionが旧Storage Decisionを再利用し、旧配置へ追記 |
| 2026-08-06（本移行指示） | Humanがbyte-exact移行と保存先切替を承認 |

## 2. 実施内容

1. **TDD**：移行の契約を7 testへRED先行で固定（`ModuleNotFoundError`による7 failed、
   commit `edd9514`）→新module `tools/session_logs/preservation_migration.py`で
   GREEN（7 passed、公式全Test 1047 passed、commit `d7d2f3f`）。
   移行先の導出は既存`resolve_project_runtime_layout`の再利用であり、別resolverを実装していない。
   `deployment_paths.py`のOS標準path定義は変更していない（consumer 5 moduleに影響なし）。
2. **実行前の停止条件再検査**：旧書庫5 fileのSHA-256が既存recapture receiptの記載と全件一致。
3. **移行先導出**：正本baseline record（v3 candidate）を読み込み、
   `<runtime_root>/projects/reviewcompass3/development/sensitive/eventual-preservation`を導出。
   sensitive rootは設計どおり`initialize_project_runtime_layout`で0700作成。
4. **dry-run**：file 5件、93,878,980 bytes、衝突0、rollback可能（source不変設計）。
5. **移行実行**：`action: migrated`。一時領域経由のbyte-exact copy→検証→atomic配置。
6. **照合**：12 checks全合格（file数・相対path・size・SHA-256全件一致、rawはUTF-8有効JSONLで
   parse issue 0、**rawから実rendererで再生成したverbatimが保存verbatimとbyte一致**、
   cursor・Provenance・ledgerのidentity一致、directory 0700・file 0600、一時／lock残留0）。
7. **冪等再実行**：`action: unchanged`（何も書かない）。
8. **旧書庫の確認**：移行後も5 fileのSHA-256・permission（0600）が不変。削除していない。

## 3. 検証結果の要約

| 項目 | 結果 |
| --- | --- |
| 移行対象 | source content ID `b12edc2408fa1263`、file 5件、93,878,980 bytes |
| Digest照合 | source＝既存receipt＝target、全件一致 |
| verify_migration | `status: pass`、12 checks全true（詳細はReceipt） |
| 冪等再実行 | `unchanged` |
| 旧書庫 | 不変・未削除・rollback copyとして保持 |
| active path | Layout v3のtargetへ切替（authority＝本Decision）。旧pathはactiveでない |
| 対象Test | `tests/test_preservation_migration.py` 7 passed |
| 公式全Test | **1047 passed**（failed 0） |
| `git diff --check` | 合格 |

## 4. 補足事実

- 旧書庫のdirectoryは28個（空のlock directory鎖5個を含む）、移行先は23個である。差は
  **file実体の無い空のlock directory鎖**であり、copyしていない。lock directoryはcollectorが
  必要時に0700で再作成する設計である（`_secure_parent_chain`）。lock残留の検査は0件で合格。
- 移行先の中間directory（`projects/`〜`development/`）は既存の755のままである。機微性の境界は
  sensitive root自身（0700）とその配下（全0700）で守られている。
- 実装が`eventual_preservation._complete_jsonl_prefix`（private helper）をimport再利用している。
  複製禁止を優先した選択であり、公開helperへの昇格は将来の改善候補である。

## 5. 未実施事項

- 旧配置の削除（承認範囲外。別のHuman判断）。
- `deployment_paths.py`のOS標準path定義の変更。
- 他projectやruntime profileへの一般化。
- push、PR、外部送信。

## 6. 変更ファイル

| path | 種別 |
| --- | --- |
| `records/development/2026-08-06-preservation-layout-v3-migration-decision-v1.md` | 新規（Decision、commit `edd9514`） |
| `tests/test_preservation_migration.py` | 新規（RED 7件、commit `edd9514`） |
| `tools/session_logs/preservation_migration.py` | 新規（GREEN、commit `d7d2f3f`） |
| `records/development/2026-08-07-preservation-layout-v3-migration-receipt-v1.json` | 新規（本作業単位） |
| 本Evidence | 新規（本作業単位） |

既存file（既存Decision、Task Contract、receipt、Evidence、`deployment_paths.py`）は変更していない。
