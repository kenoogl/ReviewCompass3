# 反証レビュー第1束 処置（B案）承認Decision v1

- decision ID：`DEC-ADVERSARIAL-REMEDY-BATCH1-001`
- decision maker：Human
- decided at：2026-08-07
- 指示：本sessionのHuman文言「B案」（2026-08-07。選択肢提示への裁定）
- 所見の正本：`records/development/2026-08-07-adversarial-review-batch1-new-modules-v1.md`

## 1. Humanの決定（B案）

- **型1・型2の8件を修正する**：R-2、R-4（範囲の内部整合）、C-1、C-3（対応表の整合）、
  R-5、R-6（証明書の記述照合）、X-1（根拠参照の解決）、G-1（順位表での除外宣言検証）。
- **型3は修正せず、設計提案を作ってHuman承認後に扱う**：C-2（空summary）、C-4（`red_now`の
  実行照合）、X-2（広範囲接頭辞）。**R-3（検索したふり）もここへ移す**——機械修正には
  gate時の再検索（決定的再生成の照合）が必要で、費用と設計判断を伴うため。所見recordの
  型分類ではR-3が型に割り当てられていなかった誤記も本Decisionで訂正する。
- 残りのレビュー（`operation_routing`系、Intake／Pilot検証器群）は修正と並行して続行する。

## 2. 修正に付随して許可されること

- 修正はTDDの型どおり（反証を拒否テストとしてRED固定→GREEN）。実装前の再観測と再利用検索
  gateを通す。
- **検査器・検証器の変更に伴うstale閉包**：修正後、現存する全対応表・除外宣言・順位表を
  新しい検査器で再検査し、結果を記録する。
- 修正が既存recordの形式不備を露呈する場合（例：除外宣言の`authority_refs`にpathが無い、
  Intake対応表v2の部分列挙が完全列挙検査と衝突）、**後継version（新形式への機械的な写し替え）
  の作成を本Decisionで許可する**。意味内容は変えない。
- 固定testのfixtureが新しい検証規則を満たさない場合、理由を記録してfixtureを新規則適合へ
  更新できる（検証を弱める方向の変更は不可）。

## 3. この決定が承認していないこと

- 型3（R-3、C-2、C-4、X-2）の修正（設計提案とHuman承認が先）
- 検査の緩和、既存所見recordの書き換え
