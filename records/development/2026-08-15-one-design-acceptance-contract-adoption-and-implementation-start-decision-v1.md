# 一件の設計・受入条件照合 契約採用・実装開始判断 v1

- Decision ID：`DEC-ONE-DESIGN-ACCEPTANCE-CONTRACT-ADOPTION-2026-08-15-V1`
- 判断日：2026-08-15
- 判断主体：利用者
- 利用者の文言：`承認`
- 採用契約：`TC-RC3-PRODUCT-ONE-DESIGN-ACCEPTANCE-CONFORMANCE-004` version 3
- 契約path：`records/task-contract/2026-08-15-one-design-acceptance-conformance-candidate-v3.md`
- 契約SHA-256：`8d8b4a608372162c68665155ecde9c1dce8122402ab1ebea0dc40e2c621bac80`
- 独立確認path：`records/development/2026-08-15-one-design-acceptance-contract-v3-independent-rereview-v1.md`
- 独立確認SHA-256：`4e216990f74b963ac159ce5997dbe599d40746a78786b6bc919f006bbd210f9e`
- 判断：`contract_adopted_option_c_implementation_authorized`

## 1. 判断

【記録】利用者は、目的、根拠、合否基準、影響、3案、独立確認結果の説明を受けた後、次のとおり明示した。

> 承認

【判断】契約v3と案Cを採用し、失敗試験を先に作る実装を開始してよい。

## 2. 採用した範囲

1. 明示された設計JSON一件と受入条件JSON一件を読む。
2. 一意な`subject`で対応させ、4つの固定比較で満たす・欠落・矛盾・未参照を整理する。
3. 入力自由値と絶対pathを表示せず、全条件を人の判断一覧へ残す。
4. 新しい副作用のない照合核、安全読取り入口、配布用実行名、対象試験だけを追加する。
5. 既存G08の2実装fileと2試験fileを変更しない。

## 3. 採用していない範囲

- 自由文、Markdown、Word、PDF、画像の意味解析。
- 外部AI、通信、外部送信、外部process、保存、Git、環境値解決。
- 複数設計の探索・一括処理。
- 受入条件、設計、最終採否の自動修正または自動決定。
- 既存G08、既存schema、G30汎用状態管理の変更または正式化。
- 製品受入。実装・検証・独立完了確認後に別途判断する。

## 4. 開始条件

【実測】契約候補v3の独立限定再確認は、止める原因0件、未接続条件0件、退行0件で`開始可`だった。

【判断】実装前に、契約20条件を4境界の失敗試験、最小実装、不変条件へ対応させた作業票を固定し、
別担当が読取り専用で開始前確認する。修正要なら製品コードへ進まない。
