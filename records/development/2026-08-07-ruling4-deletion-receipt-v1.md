# 裁定4 削除実施Receipt v1

- 作成日：2026-08-07
- 承認：`DEC-FOUR-RULINGS-2026-08-07-001`裁定4（Human文言「4．削除」）

## 1. 旧書庫の削除（不可逆・実施済み）

- 対象：`~/Library/Application Support/ReviewCompass3/eventual-preservation`
  （Layout v3移行のrollback保持分。file 5件、93,878,980 bytes、source content ID `b12edc2408fa1263`）
- **削除前検証【実測】**：移行Receipt（`2026-08-07-preservation-layout-v3-migration-receipt-v1.json`）
  記載のSHA-256に対し、旧書庫5/5件一致、移行先（v3 sensitive root配下）5/5件一致。
  両側の一致を確認したうえで削除した。
- 対象外：同じ親directoryの`backups/`と`preservation-ledger.json`は裁定の対象外であり
  変更していない。
- 現用の書庫（移行先）は無変更である。

## 2. 検索record旧位置の削除（6件、git管理下＝履歴から復元可能）

外部化のbyte一致検証と証明書作成が完了済み（`591e998`）の7件のうち、機械参照走査
（tests・tools・config・schemas）で参照0件の**6件を削除**した：

candidate-ranking、integration-exclusions-helper、reuse-search-externalization、
reuse-search-freshness、reuse-search-record-helper、routine-ledger の各`*-reuse-search-v1.json`。

**1件を保留**：`2026-08-07-declaration-red-map-checker-reuse-search-v1.json`。
Work 5B Contract（`TC-WORK5B-DECLARATION-RED-MAP-CHECK-001`）の固定sourceと
`tests/test_work5b_contract.py`がpath・Digestで束縛しており、削除すると固定testが壊れる。
参照の解消（Contract v2化）までは削除せず、黙って壊さない原則に従い本Receiptで報告する。

## 3. 事後状態

- 各recordの外部本体（DATA_ROOT `work4b/reuse-searches/`）と証明書
  （`*-reuse-search-attestation-v1.json`）は健在であり、証明書gateで解決できる。
- repositoryは検索record 6件分（約2.1MB）軽くなった。
