# 外部送信の出口設計 提案 v1

- 状態：`human_decision_pending`（Human承認まで実装しない）
- 作成日：2026-08-07
- 承認根拠：`DEC-CONFIDENTIALITY-WORK-ORDER-001`（実施順序の1番目）

## 1. この提案が答える問い

伏字化の規則は実装したが、**登録も実行もされておらず、実際には何も伏字化されていない**
（`OBS-RC3-REDACTION-RULES-ABSENT-2026-08-07-V1`）。そして二次の網（高entropy検出）は
反証レビューで6件の抜けが確認され、本質的に網羅しない。

したがって、**外部へ出す判断を伏字化の合格に依存させてはならない**。本提案は、
出口そのものをHumanが握る仕組みを設計する。

## 2. 固定入力

| 固定入力 | path | SHA-256 |
| --- | --- | --- |
| 実施順序Decision | `records/development/2026-08-07-confidentiality-work-order-decision-v1.md` | `ca5c4a89adb6ab2807887bb7834c4778f4e8658a697deb9f64617893dd67de09` |
| 設計議論の証跡（機密境界の原則） | `records/development/2026-08-07-work5b-discussion-outcomes-decision-v1.md` | `8cfc4a1581ed53513d97f70fa78323f6dc574eb2555bbd35ed78c7a4e1214a9d` |
| 機微情報の定義 | `records/development/2026-08-07-sensitive-definition-decision-v1.md` | `93d0e63f2466de5cb037e8eff3ca92c97e8cf5c00bd816927391cd4f783adc8f` |
| 伏字化規則 GREEN Evidence | `records/development/2026-08-07-redaction-environment-rules-green-evidence-v1.md` | `9dae5c2df9d39be08a63e22f47936fb27336d42c9032d8b5442bca8d7df68f85` |

既存の合意（`DEC-WORK5B-DISCUSSION-OUTCOMES-001` §2 論点4）：送るのは判定に必要な候補コード断片と
機械的特徴量のみ。生のsession記録と`SENSITIVE_ROOT`の内容は送らない。送信前に機械検査を通す。

## 3. 中核となる考え方

**「送ってよいもの」を列挙する。「送ってはいけないもの」を除外するのではない。**

除外方式は、除外規則の網羅性に安全が依存する。今日の反証で、その網羅性が成り立たないことは
実証済みである。列挙方式なら、**未知のものは既定で送られない**。

## 4. 提案する仕組み

### 4.1 送信payloadの構成規則（`egress_payload`）

外部へ送るものは、次の3種のみから機械的に組み立てる。**それ以外を含むpayloadは作れない。**

| 種別 | 内容 | 由来 |
| --- | --- | --- |
| `code_fragment` | 指定したsymbol IDのcode断片 | Routine Profileが指すcode reference |
| `machine_feature` | 機械的特徴量（行数、複雑度、structure digest、basis kind等） | Profile／Discoveryのfield |
| `question` | 判定してほしい内容の定型文 | 承認済みtemplateから選ぶ |

**session記録、`SENSITIVE_ROOT`配下、記録類の本文、Human裁定文は構成要素に含まれない**
（型として渡せない）。

### 4.2 出口の関門（`egress_gate`）

payloadを送る前に、次をすべて満たさなければ送信できない。

1. **構成の検証**：payloadが§4.1の3種だけで構成されている
2. **由来の解決**：各`code_fragment`が、指定したProfileのcode referenceから機械的に取り出された
   ものであること（手で書いた文字列を混ぜられない）
3. **伏字化の適用**：組み立て後のpayload全体へ伏字化を適用する。ただし**その合格を送信の
   根拠にしない**（下記4.3）
4. **Human承認record**：送信先、payloadのcontent digest、件数、目的を固定した承認recordが存在する
5. **fail-closed**：いずれか一つでも欠ければ送信しない

### 4.3 伏字化との関係（重要）

伏字化は**適用するが、根拠にしない**。理由は、規則が網羅しないことが実証済みだからである。

- 伏字化で何かが伏字になった場合、**それは送信を止める信号**として扱う（payloadに機微情報が
  混ざる構成になっている＝構成規則の設計が誤っている）
- 伏字化が何も検出しなかった場合、**それは安全の証明ではない**。送信可否はHuman承認recordが決める

この扱いにより、伏字化の精度が上がっても下がっても、出口の安全性は変わらない。

### 4.4 送信receiptと事後確認

送信後、payloadのcontent digest、送信先、承認record参照、応答の要約をreceiptへ残す。
**応答本文の扱いは本提案の範囲外**（別途判断）。

## 5. 段階的な導入

1. **payload構成規則と出口関門の実装**（送信機能なし）。組み立てと検証だけを作り、
   実際の送信は行わない
2. **dry-run**：実際のcode断片でpayloadを組み立て、何が含まれるかをHumanが目視できる形で出力する
3. **Human承認recordの形式確定**
4. **送信の実装**——ここで初めて外部通信が入る。別のHuman承認を要する

**本提案で承認を求めるのは1〜3まで**である。4は別提案とする。

## 6. 非対象

- 実際の外部送信の実装（段階4。別提案）
- 応答本文の扱い
- 伏字化規則の設定への登録（実施順序の2番目。本提案の後）
- C（内部の未公開情報）とD（会話に混入した外部データ）の定義（実施順序の3番目）
- 既存の保全済みデータの扱い（実施順序の4番目）

## 7. risk

出口の関門は不可逆な外部送信を制御する守り役codeであり、`work-review-protocol` §3の
**既定`high`**である。実装後は§4.4の反証レビューを適用し、とくに
**「構成規則を迂回して任意の文字列をpayloadへ混ぜられるか」**を狙った反証を新作して試す。

## 8. Human判断点

1. 列挙方式（送ってよいものだけを構成要素にする）という中核の承認
2. 送信payloadの3種の構成要素（過不足の要否）
3. 出口関門の5条件
4. 伏字化を「適用するが根拠にしない」扱いとすること
5. 段階1〜3までを本提案の範囲とし、実際の送信を別提案とすること
