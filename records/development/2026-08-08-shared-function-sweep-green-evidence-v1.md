# 掃討処置GREEN・反証レビュー完結 Evidence v1

- 実施：2026-08-08。Human裁定「OK」（処置案1〜5全承認＋凍結元Decision確認）
- TDD：RED 15件（commit `cfaea40`）→実装→**全suite 1268 passed**【実測・単独実行】

## 1. 処置の実施

- **I-1**：canonical写し6fileを正本へ結線（pilotは凍結symbol行範囲452行以降と非交差を機械確認：
  差分は56行付近のみ）。todo_snapshotは残置し出力一致監視テストを追加
- **I-2**：config.pyの`_within`を結線
- **I-3**：正本へ`file_sha256`を追加（Human承認済み）し5か所を結線。実装中にpilotの合成写し
  `_sha256_file`を追加発見し結線（計6か所）
- **I-4**：恒久guardテストを追加——再発明のrepo全体走査（canonical・1行sha256・file読みhash・
  file直接起動文字列）、正本5fileの**指紋pin**（無承認変更を検出。更新はHuman承認記録を伴う）、
  例外の兄弟隔離、`-m`起動到達6module
- 処置5：残置台帳＝todo_snapshotの`_sha256`と`_canonical_digest`の**2種**（所見recordの
  「file_sha256相当」は誤記であり本Evidenceで訂正。凍結解除時に一括追随、監視テストあり）

## 2. 凍結元Decisionの確認【実測】

`DEC-FROZEN-LANE-GUIDANCE-CORRECTION-001`（除外E1のauthority_ref）：凍結の意味は「旧Pilot記録は
旧規則・旧検証器のまま保持し、新規則で再判定しない」。解除は旧Pilot経路の役目終了または実例の
fixture化等の**Human裁定**による（明文の自動解除条件は無し）。

## 3. 反証レビューの完結

観点全消化：再発明残存（的中→処置済み）、結線迂回（`is`固定＋再発明走査で恒久化）、正本の
無承認変更（指紋pinで恒久化）、基底変更の波及（兄弟隔離テスト）、起動経路（`-m`到達＋直接起動
残存走査）。**共通化の最終形：正本5関数へ計37定義を一元化**（digest10＋B/D/E14＋掃討13）、
残置は凍結file内の2種のみ。
