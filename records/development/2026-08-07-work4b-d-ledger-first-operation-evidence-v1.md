# 構成D 台帳（既存経路再利用）初回実運用 Evidence v1

- 作成日：2026-08-07
- 承認：`DEC-WORK4B-D-LEDGER-REUSE-001`（1案）、Entry labelのHuman裁定は本sessionの
  Human文言「承認」（2026-08-07。8件すべて`as_is`の提示に対する承認）

## 1. 実施（既存経路v3.3の型どおり、新codeなし）

1. **候補run**：観測`5cea442a…`からcandidate run `4699a776…`（候補1245件）を外部DATA_ROOTへ
   new-only生成した。
2. **証明書**：`OBSATT-5cea442a…`を台帳配下`attestations/`へ作成した（schema 2、
   Profile `b4ba016e…`結線。commit `34b9e9a`）。
3. **Human Decision**：`DEC-RRL-HELPER-ENTRIES-001`
   （`.reviewcompass/design-decisions/dec-rrl-helper-entries-001.json`、human_id `kenoogl`、
   decided_at `2026-08-07T14:12:51+09:00`）。対象8 symbol、処置は全件`as_is`。
   処置の出所検証（`human_decision`以外は停止）は既存機構が実施した。
4. **Baseline v1**：`append_baseline`でEntry 8件（`entries/rrl-*--v1.json`）とBaseline
   （`ledger-baseline--v1.json`、entry_refs結線、relations 0件、prior無し）をnew-only追記した。

Entryの内訳：`reuse_search_record.py`の6件（検索・検証・保存・gate・digest計算・例外）、
`declaration_red_map_check.py`の2件（検査・例外）。`RRL-RSR-SHA-001`には、同種digest計算の
複製が他moduleにあり統合の要否は順位表経由で扱う旨を注記した（labelの先取りなし）。

## 2. Test結果

公式全Test `1080 passed`、exit `0`。既存test・既存対応表・既存recordの変更なし。

## 3. 初回実運用が見つけた所見（レビューと分離、修正未実施）

**`validate_current`（台帳の現在状態検査）が`digest_mismatch: docs/development/2026-08-02-development-policy.md`で停止する。**
原因は、source universe record v1（2026-08-04作成）が固定する`development_policy_ref`のDigestが、
その後の開発方針改定（Policy v5）に追随していないこと。観測・証明書・Baseline追記の経路は
このrefを検証しないため成立するが、現在状態検査だけが通らない。参照Digest drift類型
（`ISSUE-AUTHORITY-REFERENCE-DIGEST-CHECK-001`）の新しい実例であり、処置候補は
universe record v2の作成（refの現行化）。着手はHuman判断とする。

## 4. Work 5B defer項目の完了戻し

`DEC-WORK5B-LEDGER-ITEM-DEFER-001`の再開条件（台帳整備後、helper 2件の台帳Entry記録）は
本Evidenceで満たされた。checklist §10の4番目の項目を完了へ戻す。
