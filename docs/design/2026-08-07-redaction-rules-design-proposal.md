# 伏字化規則の設計提案 v1

- 状態：`human_decision_pending`（Human承認まで実装しない）
- 作成日：2026-08-07
- 承認根拠：`DEC-SENSITIVE-DEFINITION-001`（機微情報の定義と環境依存値の扱い）

## 1. 固定入力

| 固定入力 | path | SHA-256 |
| --- | --- | --- |
| 機微情報の定義Decision | `records/development/2026-08-07-sensitive-definition-decision-v1.md` | `93d0e63f2466de5cb037e8eff3ca92c97e8cf5c00bd816927391cd4f783adc8f` |
| 規則不在の観測 | `records/development/2026-08-07-redaction-rules-absent-observation-v1.json` | `c77d4c385a7ac8b4cb52128acfd19e51da8655df2e8e9f70033aa36c27f88673` |
| 現行の伏字化module | `tools/session_logs/redaction.py` | `300e41bb5d756f79863f1cf31fc6631d989bc0c06ed4986d1eee448cfd72f7c0` |

## 2. 二種類の規則

現行の`Rule`は`label`と`pattern`（正規表現の文字列）だけを持つ。定義した5区分のうち、
1〜3は今の形で書けるが、A・Bは実値を書けないため**規則の種類を分ける**。

### 2.1 `pattern`規則（区分1〜3。現行のRuleをそのまま使う）

値の形で見つけるもの。環境に依存しない。

| label | 対象 | 備考 |
| --- | --- | --- |
| `email` | メールアドレス | 区分2 |
| `bearer_token` | `Bearer <token>`形式 | 区分1 |
| `api_key_assignment` | `api_key=...`、`token: ...`などの代入形 | 区分1 |
| `private_key_block` | 秘密鍵のPEM block | 区分1 |
| `aws_access_key_id` | 外部サービスの識別子形式 | 区分3 |

**この一覧は初版の出発点であり、網羅ではない。** 追加はHuman判断とする（層2と同じ性質）。

### 2.2 `environment_reference`規則（区分A・B。新設）

実値を持たず、**役割の名前だけ**を持つ。実際の値は実行のたびに環境から解決する。

    {"label": "home_directory", "environment_role": "home_directory"}
    {"label": "user_name",      "environment_role": "user_name"}
    {"label": "host_name",      "environment_role": "host_name"}

解決の対応（実装時に固定する）：

| `environment_role` | 解決元 |
| --- | --- |
| `home_directory` | `Path.home()` |
| `user_name` | ホームdirectoryの名前部分 |
| `host_name` | `socket.gethostname()` |

**規則fileに書かれるのは`environment_role`の名前だけ**であり、解決した実値は規則にも
派生物にもlogにも残さない。

## 3. 環境依存値が漏れない仕組み（本提案の核心）

環境依存値を扱うと、伏字化の副産物として値が別の場所へ漏れる経路が生まれる。次の3点で塞ぐ。

**3.1 置換先に値を出さない**
置換文字列は`[REDACTED:home_directory]`のように**役割名だけ**とする。現行の`redact_text`は
`[REDACTED:<label>]`を出すため、labelに実値を入れなければこの要件を満たす。

**3.2 規則digestに実値を入れない**
`redaction_rules_digest`は現在`label`と`pattern`を含める。環境依存規則では`pattern`が実行時に
生成されるため、**解決後のpatternをdigestへ入れると環境情報がdigestの入力になる**。
`environment_role`の名前をdigestの入力とし、解決後の値は入れない。

**3.3 診断・報告に実値を出さない**
`write_sensitive_report`と`HighEntropyFinding`は位置と長さだけを持ち、値を出さない設計に
なっている。環境依存規則の追加でこの性質を壊さないことを、negative testで固定する。

## 4. 適用順序

環境依存値は長いpathを含み、他の規則より先に消すと後続の一致が変わる。順序を決定的にする。

1. `environment_reference`規則（長いpathから先に）
2. `pattern`規則（`Rule`の登録順）
3. 高entropy網（`redact_text_strict`）

**同じ入力から同じ結果が出ることをtestで固定する。**

## 5. 二次の網（高entropy検出）の扱い——本提案では変更しない

第2束の反証で6件の抜けが確認された（長さ・複雑さの閾値直下、区切り文字による分断、
広いallow patternによる無効化）。閾値を下げれば誤検出が増え、上げれば漏れが増える。
**この網は本質的に網羅しない。**

当初案では、これを層2と位置づけて`verification_boundary.py`の宣言へ加えることを提案していた。
**Humanの指摘によりこれを取り下げる**——宣言は防御力を持たず、実効的な防御が別に無い段階で
宣言だけを足せば、それは免罪符になる（2026-08-07のHuman指摘：「宣言は免罪符になり得る点から
すると、位置づけは書かずに、実際の防御は出口に置くだけでもよくないか」）。

したがって順序を次のとおりとする。

1. **実際の防御を出口に置く**——派生物を外部へ出す経路そのものをHuman承認事項とする。
   網の精度に頼らず、出口をHumanが握る。
2. **宣言は、出口の設計が決まった時点で、その設計の一部として書く**。そのとき宣言は
   免罪符ではなく、「この合格は根拠にならないので出口で判断せよ」という誘導として働く。

**出口の承認設計は本提案の範囲外**であり、外部APIレビューのTask Contractで扱う。
本提案では二次の網に一切手を触れない（閾値も、位置づけの宣言も、変更しない）。

なお、**規則が一件も登録されておらず唯一の実データが伏字化を経ていないという事実**は
観測record `OBS-RC3-REDACTION-RULES-ABSENT-2026-08-07-V1`に固定済みである。これは
「守らないと決めた」という宣言ではなく「守られていない」という観測であり、性格が異なるため
そのまま保持する。

## 6. 非対象

- 既存の保全済みデータへの遡及適用と、その内容の検査（機密の取り扱いを伴うためHuman判断）
- **二次の網（高entropy検出）への一切の変更**——閾値、分断対策、層の位置づけの宣言を含む（§5）
- C（内部の未公開情報）とD（会話に混入した外部データ）の扱い
- 外部送信の承認設計（出口。別Task Contractで扱う）

## 7. risk

`redaction.py`は機密保護の要であり、`work-review-protocol` §3の**既定`high`**である。
実装後は§4.4の反証レビュー（実装者のfixtureに無い反証の新作）を適用する。
とくに§3の3点（置換先・digest・診断に実値が出ないこと）は、**実値漏れの反証**を新作して試す。

## 8. Human判断点

1. 二種類の規則という構成の承認
2. `pattern`規則の初版5件（追加・削除・変更の要否）
3. `environment_role`の3種と解決元の対応
4. 実装順（本提案の承認後、確立済み関門を通して実装）

二次の網の位置づけは§5のとおり本提案の判断点から外した（出口の設計時に扱う）。
