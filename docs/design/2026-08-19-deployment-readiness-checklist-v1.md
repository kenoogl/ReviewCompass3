# デプロイ準備checklist v1

- 作成日：2026-08-19
- 種別：考察record（残開発事項の棚卸し。**裁定ではない**——各項目の着手・順序の裁定は
  デプロイ版作業単位とその合図で行う）
- 指示者：利用者（Human）。文言「RC3をデプロイして、具体的なアプリ開発を実施したい。そのために
  必要な残開発事項は何か」「この棚卸しをデプロイ準備checklistとしてdocs/designへ固定して」
  （2026-08-19 chat）
- 正本参照：デプロイ方針record（`records/development/2026-08-17-deployment-policy-decision-v1.md`
  訂正版P3・§4〜5）・還流2経路設計memo（`docs/design/2026-08-19-deployed-feedback-two-route-design-memo-v1.md`）・
  全体設計観測record（`records/development/2026-08-19-architecture-conformance-observation-v1.md`）

## 0. 済（デプロイの負担を既に下げた分）

- [済] 配置依存3箇所の解消・パス解決一元化（`roots.py`・指紋pin。2026-08-18）
- [済] issue経路の可搬化（lane道具一式の`--project-root`対応・一括検証`workflow_ledger_verify`。
  2026-08-19実測）
- [済] pip導入の骨格（`pyproject`に6コマンド登録・開発環境内で導入動作実績）

## A. デプロイ版作業単位の本体（方針P3・未着手）

1. [未] **RC3版deploy-manifest**：配布物allowlist＋「新しい置き場は登録してから」の規約
   （ソース側の命名・配置規約の明文化を兼ねる）
2. [未] **絶対パス混入lint**：RC2からの移植（配布物対象・recordsは対象外）
3. [未] **入口文書テンプレート**：対象アプリ側の最小1枚（記入欄＝実体化日・パッケージversion・
   調整記録）＋既存入口（CLAUDE.md／AGENTS.md）への挿入行
4. [未] **RC3版`next`最小形**：状態正本を持たず機械観測から次作業種別を返す起点コマンド
   （`--json`一行。返答語彙の細部は後日の裁定のまま最小で）
5. [未] **pip導入手順の確立**：別環境への導入手順と**版指紋**（version＋package digest。
   還流設計の必須欄）
6. [未] **権限束昇格**：着手する要件だけの要求化（論点3の裁定どおり作業単位内で）

## B. 持ち出し・還流の仕分け（同作業単位内・入力は固定済み）

7. [未] AGENTS一般規範の持ち出し仕分け（配布物側文書への抽出・論点4aの型）
8. [未] issue経路の持ち出し4項目（lane設定の配布・区画初期化・Decision record置き場・
   実態調書の拘束flagのnext型対応）
9. [未] RC3バグ還流の3判断（受付窓口・梱包toolのscope・外部patch規約）。
   梱包toolの最小実装は自分用にも有用（経路α）

## C. 前提材料の調査（checkpoint枠・WSSE初稿後）

10. [未] **lifecycle棚卸し**（暫定100・正式1・未宣言73＝2026-08-19実測→配布／昇格／開発専用の
    3区分）＝**deploy-manifestの直接材料**。アーキテクチャ整合検査
    （`IC-ARCHITECTURE-CONFORMANCE-CHECK-001`）の宣言初版と同枠。検査器のフル実装は
    デプロイの厳密な前提ではない

## D. Human裁定（開発ではない）

11. [裁定待ち] **他アプリ開発開始の決定**＝デプロイ版作業単位の合図そのもの
12. [裁定待ち] **生ログの保持・削除・暗号化方針**（`ISSUE-HTC-BEB5E0BD`・registered）。
    アプリ側でもセッションログ保全を回すならデプロイ前に裁定が要る種類

## 順序の提案（考察）

論文初稿（〜2026-08-30）→ checkpoint枠（C-10＋safe_storage語彙統合）→ デプロイ版作業単位
（A＋B。manifest＋lint／入口文書＋pip／next最小形の2〜3作業単位へ分割可【推測】）→
アプリ開発開始 → 運用実測 → projection導出の本実装（方針P3の順序）。棚卸し（C-10）を先に
すればmanifestの材料が揃い、手戻りがない。
