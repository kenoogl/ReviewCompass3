---
lifecycle: provisional
normative_status: non-normative
promotion_required: true
---

# 第4段：機能分割と requirements 作業計画

## 1. 目的

承認済みintentと承認済みエッセンス台帳を入力として、ReviewCompass3の機能を
意味単位へ分割し、外部から検証できるrequirementsを作る。

## 2. 固定入力

- intent revision 5
  - material digest:
    `4bed543815e294ba9bc001e0dbea8e8ea8ba8f86e2314e134918853f623ee189`
  - 利用者承認:
    `records/intent/stage-three-user-approval.json`
- エッセンス台帳47項目
  - ledger digest:
    `6b6b4220117b6426be67b273ac151684579e0baa11041d19f37ff440d165849e`
  - 利用者承認:
    `records/extraction/stage-two-user-approval.json`
- 再構築計画
  - `docs/plan/2026-07-27-reviewcompass3-rebuild-plan.md`

入力の内容またはDigestが変わった場合は、変更後の入力を再承認するまで後続成果物を
更新しない。

## 3. 由来の契約

各requirementは、少なくとも次の両方をIDまたは節参照で持つ。

- intentの根拠
- エッセンス台帳の根拠

次を機械検出できる記録を作る。

- 受け先のないエッセンス
- intentへ結線しないrequirement
- エッセンスへ結線しないrequirement
- 根拠のないrequirement
- 理由のない不採用
- 未定義の参照先

Task Runtimeの概念文書は説明材料として参照できるが、単独ではrequirementの
採用根拠にしない。

## 4. requirementの記述範囲

各requirementには必要に応じて次を記述する。

- 外部から観測できる振る舞い
- 入出力
- 停止条件
- 復旧条件
- 失敗時に保存されるもの
- 受け入れ条件
- 対象外

実装方法、クラス構成、保存技術、特定のLLM製品は固定しない。

## 5. 作業単位

1. 固定入力を照合し、由来記録のSchemaと検査条件を定める。
2. intentとエッセンスを基に機能分割候補を作り、重複と責務境界を検査する。
3. 全エッセンスを採用先または理由付き不採用へ割り当てる。
4. 機能単位でrequirementsを起草し、受け入れ条件まで記述する。
5. intent、エッセンス、requirementsの双方向被覆を独立にレビューする。

各作業単位は、入力、出力、検査結果およびDigestを別記録へ固定する。

## 6. 最初の作業単位

最初に作るのはrequirement本文ではなく、由来記録のSchemaと固定入力の照合記録である。
この単位では、要件ID、intent参照、エッセンスID、採否、理由および検査結果の
表現を確定する。

## 7. 完了境界

第4段は、次をすべて満たしたときだけ完了候補とする。

- 機能分割が意味単位で一意に識別できる。
- 全requirementがintentとエッセンス台帳の両方へ結線される。
- 全エッセンスに採用先または理由付き不採用がある。
- requirementが第4節の必要項目を満たす。
- 未定義参照、未被覆、競合および未解決指摘がゼロである。
- 利用者がrequirementsを承認する。
