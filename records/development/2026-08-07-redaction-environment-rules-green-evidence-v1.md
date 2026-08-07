# 伏字化規則（環境依存参照）GREEN Evidence v1

- 作成日：2026-08-07
- 承認：`DEC-REDACTION-RULES-DESIGN-001`
- RED Evidence：`records/development/2026-08-07-redaction-environment-rules-red-evidence-v1.md`
- 対応表：`records/development/2026-08-07-redaction-environment-rules-declaration-red-map-v2.json`
  （E9追加によりv2。v1は歴史として保持）

## 1. 実装

`tools/session_logs/redaction.py`へ二種類の規則を導入した。

- **`EnvironmentRule`**：役割名だけを持つ宣言（`home_directory`、`user_name`、`host_name`）。
  実値を持たない。
- **`resolve_environment_rules`**：実行時に環境から解決する。長い値から先に消す順序とし、
  短い値が長い値の一部を先に置換して結果が入力順に依存することを防ぐ。
- **`DEFAULT_PATTERN_RULES`**：承認済み初版5件（`email`、`bearer_token`、
  `api_key_assignment`、`private_key_block`、`aws_access_key_id`）。
- **`redact_with_environment`**：環境依存参照→pattern規則→（strictなら）高entropy網の順に
  決定的に適用する入口。
- **`redaction_rules_digest_payload`**：digestの入力を返す。環境規則は役割名だけを入れる。

- targeted：`tests/test_redaction_environment_rules.py` 8 test（RED 8→GREEN 8）＋E9で9 test。
- 公式全Test：`1139 passed`、exit `0`。

## 2. 反証レビュー（`DEC-REDACTION-RULES-DESIGN-001` §3の要求）

実装後、**実値漏れを狙った反証7件**を新作して機械で試した【実測】。値は出力せず真偽のみを判定した。

| ID | 反証 | 初回 | 修正後 |
| --- | --- | --- | --- |
| L-1 | 伏字化後のテキストに実値が残る | held | held |
| L-2 | findingのlabelに実値が混ざる | held | held |
| L-3 | digestの入力に実値が入る | held | held |
| **L-4** | **解決済み規則をそのままdigestへ渡すと実値が入る** | **LEAKED** | **held** |
| L-5 | 例外メッセージに実値が乗る | held | held |
| L-6 | 診断報告に実値が乗る | held | held |
| L-7 | 宣言済み規則をJSON化すると実値が出る | held | held |

**L-4が成立した。** 解決済み規則は`pattern`に実値を含むため、これを誤って`redaction_rules_digest`へ
渡すとdigestの入力に環境情報が入る経路だった。処置として`ResolvedEnvironmentRule`型を導入し、
digestの入力生成が宣言済み・解決済みのどちらでも**役割名だけを使う**ようにした。誤用しても
漏れない構造である。

修正後は**漏れ0/7**。この反証をE9として恒久testへ固定した（対応表v2）。

**GREEN後の反証レビューが実際に1件を捕まえた**——設計提案§7で予告した手順が機能した実例である。

## 3. 適用範囲（重要）

本実装は規則と適用経路を用意したにとどまる。**既存の保全済みデータへの適用、設定への登録、
実際の伏字化の実行は行っていない**（承認範囲外。`DEC-REDACTION-RULES-DESIGN-001` §4）。
`OBS-RC3-REDACTION-RULES-ABSENT-2026-08-07-V1`が記録した「唯一の実データは逐語保存のまま」という
状態は変わっていない。

## 4. 残余

- 設定への登録と実行経路への接続（別作業単位。Human判断）
- 既存データへの遡及適用とその内容の検査（機密の取り扱いを伴うためHuman判断）
- 二次の網（高entropy検出）は本実装で変更していない。位置づけの宣言は出口の設計時に扱う（§5）
- C（内部の未公開情報）とD（会話に混入した外部データ）の扱い
