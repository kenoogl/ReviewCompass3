# 構成D 台帳の既存経路再利用（1案）承認Decision v1

- decision ID：`DEC-WORK4B-D-LEDGER-REUSE-001`
- decision maker：Human
- decided at：2026-08-07
- 指示：本sessionのHuman文言「1案」（2026-08-07。実装前検索が既存台帳機構を発見した報告への裁定）

## 1. 背景

構成Dの実装前再利用検索（`records/development/2026-08-07-routine-ledger-reuse-search-v1.json`、
鮮度gate `assessed_fresh`通過）が、Work 4A v3.3で実装済み・未運用の台帳機構を発見した：
`tools/development/work4a_rebuild_v3.py`の`build_entry_documents`（処置の出所が
`human_decision`以外なら停止）、`append_baseline`（Entry・Relation・Baselineのnew-only系列追記、
証明書とHuman Decisionへの結線検証つき）、処置label 5語彙（`reuse|extend|merge|split|as_is`）、
置き場`.reviewcompass/reuse/reusable-routine-ledger/`。設計束§5の要件と適合する。

## 2. Humanの決定（1案）

構成Dは**新moduleを作らず、既存台帳経路の初回実運用として実施する**。設計束
（`DEC-WORK4B-MAIN-DESIGN-BUNDLE-001`）§5の「`.reviewcompass/workflow/routine-ledger/`へ
schema・検証器を新設する」という記述は、本Decisionで**既存経路の再利用へ読み替える**。
不足が見つかった場合は適合修正だけを入れる（発見は記録し、修正はレビューと分離する）。

## 3. 実施手順（既存経路v3.3の型どおり)

1. 現行観測（snapshot `5cea442a…`）のcandidate runを生成し、観測の証明書（attestation）を
   台帳配下へ作成する
2. Work 5B defer項目の対象helper 2件のEntry候補と処置label案を提示し、**labelのHuman裁定**を得る
3. 裁定を`write_operational_decision`（Human Decision record）として固定する
4. `append_baseline`でEntry・RelationをBaseline v1として追記する
5. Work 5B defer項目（checklist §10の4番目）を完了へ戻す

## 4. この決定が承認していないこと

- Entry候補の処置label（手順2で別途Human裁定）
- 全routineの一括台帳化（対象はdefer項目の2件から始める）
- 構成C（外部化）の実施
