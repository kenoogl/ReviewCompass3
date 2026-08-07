# 伏字化規則（環境依存参照）RED Evidence v1

- 作成日：2026-08-07
- 承認：`DEC-REDACTION-RULES-DESIGN-001`、`DEC-RED-VERIFICATION-ADOPTION-001`（手順）
- 実装前検索：`records/development/2026-08-07-redaction-rules-reuse-search-attestation-v1.json`
  （gate `assessed_fresh`、該当139 routine）

## 1. 固定する内容

承認された設計に従い、二種類の規則を導入する。核心は**環境依存値が伏字化の副産物として
漏れないこと**であり、宣言E3・E4・E5がそれを担う。

| 宣言 | 内容 |
| --- | --- |
| E1・E2 | 規則は役割名だけを持ち、実値は実行時に環境から解決する |
| **E3** | 置換先には役割名だけが出る（実値が置換先へ漏れない） |
| **E4** | 規則digestの入力は役割名であり、解決後の実値を含まない（digestが環境情報の写しにならない） |
| **E5** | 診断・報告に実値が出ない性質を壊さない |
| E6・E7 | 承認された初版pattern規則5件の登録と動作 |
| E8 | 適用順序が決定的である |

testで使う値は**すべて合成した架空の文字列**であり、実在の秘密は使わない。

## 2. 宣言→RED対応表

`records/development/2026-08-07-redaction-environment-rules-declaration-red-map-v1.json`
（`scope: complete`）。静的検査`passed`、宣言8件（E1〜E8）。

## 3. 実行照合（`DEC-RED-VERIFICATION-ADOPTION-001`）

RED固定commit前に照合した【実測】：

    checked=8  verified=8  mismatched=0  unknown=0  → passed

## 4. 状態と次

本RED作業単位のcommit後、固定testを変更せずGREEN実装へ進む。実装後は`work-review-protocol`
§4.4に従い、**実値漏れを狙った反証**（置換先・digest・診断のそれぞれに環境の値が出ないか）を
新作して試す（`DEC-REDACTION-RULES-DESIGN-001` §3）。
