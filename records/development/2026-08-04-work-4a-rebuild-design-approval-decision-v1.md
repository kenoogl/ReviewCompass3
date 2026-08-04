# DEC-WORK4A-REBUILD-DESIGN-001

## Decision

Humanは、`docs/design/2026-08-04-work-4a-rebuild-design-proposal.md`のWork 4A再設計を承認した。

## 承認範囲

- 新規追加で既存Entry／Relationを複製しないnew-only ledgerモデル
- source content identityによるfreshness判定
- project artifact、`DATA_ROOT`、deployment packageの境界
- Historical Contract StatusをHuman Decision必須の別recordにする規則
- 旧Work 4A patch群をhistoryを書き換えずrevertし、E2E acceptanceから再実装する順序

## 禁止事項

個別の失敗または不整合を理由に、旧Work 4A patchへ局所修正を重ねることを禁じる。
設計外の問題が出た場合は、現行の実装を継ぎ足して解消せず、影響、原因、設計との矛盾を記録して
Human判断へ戻す。

## 根拠

- Human approval：2026-08-04の会話における「承認する。進めよ。モグラたたき式に対応することを厳しく禁じる。」
- 対象設計：`docs/design/2026-08-04-work-4a-rebuild-design-proposal.md`
