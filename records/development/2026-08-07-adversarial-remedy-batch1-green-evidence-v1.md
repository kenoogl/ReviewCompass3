# 反証レビュー第1束 処置（B案）GREEN Evidence v1

- 作成日：2026-08-07
- 承認：`DEC-ADVERSARIAL-REMEDY-BATCH1-001`
- 所見の正本：`records/development/2026-08-07-adversarial-review-batch1-new-modules-v1.md`
- 対応表：`records/development/2026-08-07-adversarial-remedy-batch1-declaration-red-map-v2.json`
  （v1は歴史として保持）

## 1. 塞いだ穴（型1・型2の8件）

| 反証 | 導入した拒否 |
| --- | --- |
| R-2、R-4 | 検索recordの`freshness.target_paths`が`declaration.target_paths`と一致しない場合、検証器が拒否する。範囲を片方だけ狭めてgateの監視対象を減らせない |
| R-5、R-6 | 証明書gateが、証明書の記述（hit件数・source identity・schema版）を外部record本体から再構成して照合する。要約だけを書き換えて通せない |
| X-1 | 除外宣言の`authority_refs`は`path`必須で、file実在まで検証する。ID文字列だけの「名乗り」を拒否する |
| G-1 | 順位表の生成が、受け取った除外宣言を`validate_integration_exclusions`で検証してから行う |
| C-3 | 複数の宣言が同一testを共有する対応表を検査器が拒否する。宣言の数だけ被覆があるように見せられない |
| C-1（部分） | `test_files`欄と宣言側のtest集合の**双方向一致**を要求する（欄からの欠落・宣言からの欠落の両方を検出） |

## 2. C-1が部分修正にとどまった理由（設計判断へ送る）

反証C-1の完全な解消には「fileに実在するtest全体」を判定対象にする必要がある。これを実装して
既存対応表10枚へ機械適用したところ、**Intake V4対応表2枚が36〜39件の未対応testで失敗**した。
原因は実装の欠陥ではなく、「変更したtestだけを列挙する」という部分列挙の設計と新規則の衝突で
ある。対応表が扱う範囲をどう宣言するかは設計判断であり、`DEC-ADVERSARIAL-REMEDY-BATCH1-001`
§1の型3（設計提案とHuman承認が先）へ移す。実装は双方向一致検査までとし、限界を
`tools/development/declaration_red_map_check.py`のcomment と本Evidenceへ記録した。

## 3. Test結果

- 処置test：`tests/test_adversarial_remedy_batch1.py` 9 test。RED 9/9 → GREEN 9/9。
- 公式全Test：`1093 passed`、exit `0`（新規9件を含む）。
- fixture更新：`test_integration_exclusions.py`・`test_candidate_ranking.py`の
  `authority_refs`へ`path`を補った（新しい検証規則への適合。検証を弱める変更はしていない。
  `DEC-ADVERSARIAL-REMEDY-BATCH1-001` §2の許可範囲）。

## 4. stale閉包（検査器変更に伴う旧合格の再検査）

新しい検査器・検証器で現存recordを全件再検査した【実測】。

- **宣言→RED対応表 10枚**：8枚`passed`。失敗2枚は(a)処置対応表v1（C-1のtest改名前）→v2で解消、
  (b)Intake対応表v1（superseded済みの歴史record、`DEC-INTAKE-V4-RED-MAP-SUPERSEDE-001`により
  運用検査の対象外）。**現行運用中の対応表はすべて合格**。
- **統合除外宣言**：v1が`authority reference has no path`で失敗。承認済み3 entryの意味を変えず
  `path`を補った**v2**を作成し合格（`integration-exclusions-001--v2.json`）。
- **検索record証明書 8件**：5件が通過、3件が`profile_stale`。これは修正後にmoduleが変わった
  ことを判定時点で再計測した正しい結果である（各gateは実装開始時に役目を果たし済み）。
- **順位表**：v1は除外宣言v1（不備あり）を参照していたため再生成が拒否された。再観測後、
  除外宣言v2で**v2を生成**（順位748件、脱落68件。件数増はProfile更新による）。v1は履歴として
  保持する。

## 5. 残余

- 型3（`R-3`検索したふり、`C-2`空summary、`C-4` red_nowの実行照合、`X-2`広範囲接頭辞）と
  C-1の完全解消は設計提案待ち。
- 反証は同一実行者が作成した限界が残る（合意順序④の外部APIレビュー対象）。
- 第1束の残り（`operation_routing`系、Intake／Pilot検証器群）のレビューは未実施。
