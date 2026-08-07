# 伏字化規則の設計 承認Decision v1

- decision ID：`DEC-REDACTION-RULES-DESIGN-001`
- decision maker：Human
- decided at：2026-08-07
- 指示：本sessionのHuman文言「承認」（2026-08-07。提案修正後）

## 1. Humanの決定

伏字化規則の設計提案v1（`docs/design/2026-08-07-redaction-rules-design-proposal.md`、SHA-256
`d6e1b15309e52aa5875176bfc9fcfaa1a7253b7be1d842fdc337c977bd79321a`）を承認した。
承認は提案§8の4判断点すべてに及ぶ。

1. **二種類の規則という構成**：値の形で見つける`pattern`規則（区分1〜3）と、役割名だけを持つ
   `environment_reference`規則（区分A・B）
2. **`pattern`規則の初版5件**：`email`、`bearer_token`、`api_key_assignment`、
   `private_key_block`、`aws_access_key_id`。網羅ではなく出発点であり、追加はHuman判断
3. **`environment_role`の3種と解決元**：`home_directory`（`Path.home()`）、
   `user_name`（ホームdirectoryの名前部分）、`host_name`（`socket.gethostname()`）
4. **実装順**：確立済み関門（再観測→実装前検索gate→宣言→RED対応表→実行照合→RED固定→
   GREEN→stale再検査）を通す

## 2. 実装が満たすべき核心（提案§3）

環境依存値が伏字化の副産物として漏れないこと。

- 置換先には役割名だけを出す（実値を出さない）
- 規則digestの入力は`environment_role`の名前とし、解決後の実値を入れない
- 診断・報告（`write_sensitive_report`、`HighEntropyFinding`）に実値を出さない性質を壊さない

## 3. 実装後に行うこと

`redaction.py`は機密保護の要であり`work-review-protocol` §3の既定`high`である。実装後に
§4.4の反証レビューを適用し、**実値漏れを狙った反証**（置換先・digest・診断のそれぞれに
環境の値が出ないか）を新作して試す。

## 4. この決定が承認していないこと

- 二次の網（高entropy検出）への変更——閾値、分断対策、層の位置づけの宣言を含む（提案§5・§6）
- 既存の保全済みデータへの遡及適用と、その内容の検査
- C（内部の未公開情報）とD（会話に混入した外部データ）の扱い
- 外部送信の承認設計（出口。別Task Contractで扱う）
