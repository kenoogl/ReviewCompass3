# 一件の設計・受入条件照合 契約候補v3 独立限定再確認 v1

- 実施日：2026-08-15
- 対象契約：`TC-RC3-PRODUCT-ONE-DESIGN-ACCEPTANCE-CONFORMANCE-004` version 3
- 対象path：`records/task-contract/2026-08-15-one-design-acceptance-conformance-candidate-v3.md`
- 対象SHA-256：`8d8b4a608372162c68665155ecde9c1dce8122402ab1ebea0dc40e2c621bac80`
- 対象commit：`7a60e9e7d197f92a3b7efa037a9f40a0941cf269`
- 確認担当：v2を反証した独立AI実行単位
- 確認方法：読取り専用。v2の4原因と他条件の退行だけを限定確認
- 判定：`ready_to_start`
- 止める原因：0件
- 未接続受入条件：0件
- 他条件の退行：0件

## 1. 前回4原因の解消

### 1.1 JSON同名項目

【実測】root、入れ子、escape復号後に同名となる`"subject"`と`"\u0073ubject"`の3反例を、
いずれも正規化前に拒否する規則へ接続した。

```json
{"all_duplicate_counterexamples_rejected":true,"cases":{"escaped":true,"nested":true,"root":true}}
```

- 反例命令の終了コード：0

### 1.2 4比較の不成立側

【実測】受入条件1に、4比較それぞれの成立・不成立と、集合比較で設計値が配列でない例が固定された。
次の欠陥模擬を全て検出した。

- 型を見ない`equals`。
- 常に成立する`not_equals`。
- 常に成立する`contains_all`。
- 常に成立する`contains_none`。

```json
{"all_mutants_caught":true,"correct_rule_passes_all_cases":true}
```

- 欠陥模擬命令の終了コード：0

### 1.3 入力root途中のsymlink

【実測】file system起点`/`から入力rootまでを一要素ずつsymlink非追跡で開く規則になった。
親要素へsymlinkを置いた反例では、root自身だけの単一openは誤って通り、起点からの要素別openは拒否した。

```json
{"single_root_open_accepted_intermediate_symlink":true,"slash_to_root_component_walk_rejected_it":true}
```

- 反例命令の終了コード：0

### 1.4 危険度

【記録】危険度は高へ訂正され、設計適合、受入真偽、機微情報を理由として明記された。
【判断】上位方針と一致する。

## 2. 退行確認

【実測】

- 受入条件：1〜20が連続し、20件のまま。
- 受入条件1、9、10の接続検査：終了コード0。
- 既存G08の2実装fileと2試験file：基準commitから差分0。
- 関連試験：31件成功、終了コード0。
- v2、v2独立確認、開発方針の参照SHA-256：全て一致。
- 停止元、内容識別値、出力順序、禁止作用、利用者承認境界：意味変更なし。
- 終了時HEAD：対象commitと一致。
- 作業場所と索引：変更なし、未記録差分なし。

【手戻り】受入条件の自動文面確認で、最初は命令組立ての引用符、次は正規表現の逆斜線を誤った。
いずれも補助命令だけの誤りで、訂正版を終了コード0で再実行した。成果物、TODO、Gitへの変更はない。

## 3. 判断

【判断】契約候補v3は、利用者による契約採用と案Cの実装開始判断へ進める。
本確認は契約採用、実装開始、製品受入を代行しない。
