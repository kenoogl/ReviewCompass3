# universe record v2 作成結果と診断訂正 Evidence v1

- 作成日：2026-08-07
- 承認：`DEC-UNIVERSE-RECORD-V2-TIMING-001`

## 1. 実施

`write_source_universe`でuniverse record v2
（`.reviewcompass/policies/work4a-source-universe-v2.json`、content digest `b67e1f79…`）を
作成した。v2の`development_policy_ref`は現行の開発方針（Policy v5、digest `0d348803…`）を指す。

## 2. 機械確認の結果（裁定§1-3の事前確認）

`validate_current`は**依然として同じ`digest_mismatch`で停止する**。原因の再特定【実測】：

- 検証が失敗する箇所は`_current_policy`であり、検証対象は**freshness policy v4自身の
  `development_policy_ref`**（旧Digest `9078276…`、2026-08-04作成時点の開発方針を指す）。
- universe recordの同種参照は`validate_current`の停止点ではなかった。先のEvidence
  （`2026-08-07-work4b-d-ledger-first-operation-evidence-v1.md` §3）の「universe record v1が原因」
  という記述は**部分的に誤り**であり、本Evidenceで訂正する（旧Evidenceは不変のまま保持）。

## 3. 残余の処置候補（Human判断待ち）

freshness policy v5の作成（既存`write_freshness_policy_v4`関数でpolicy_version 5として機械生成。
参照Digestの現行化のみで、判定語彙・閾値は変更しない）。`DEC-UNIVERSE-RECORD-V2-TIMING-001`は
universe v2だけを承認しており、policy v5は承認範囲外のため着手しない。

なお、これで参照Digest drift類型の実例は**4例目**（checklist front matter、候補evidence参照、
universe record、freshness policy）となり、恒久検査器Issue
（`ISSUE-AUTHORITY-REFERENCE-DIGEST-CHECK-001`）の判断材料が増えた。
