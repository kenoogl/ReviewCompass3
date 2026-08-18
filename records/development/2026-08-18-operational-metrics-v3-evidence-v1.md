# 運用集計v3（書式C照合）実行Evidence v1

- 記録日：2026-08-18
- 指示者：利用者（Human）。文言「候補1」（2026-08-18 chat）
- 範囲固定：作業票`docs/development/2026-08-18-operational-metrics-v3-work-ticket-v1.md`
- 事前走査：`records/development/2026-08-18-operational-metrics-v3-prescan-v1.md`
- 基準commit：`0dc25e1`→文書・計画（writer仕上げ）commit `f85faa8`→証明書commit `00f83f0`→
  実装は本recordと同一commit

## 1. 成果物

- `tools/evaluation/operational_metrics.py`【拡張】：書式C（表cell束縛）の行単位fail-closed
  組抽出（裸hex-cell×1・path様cell×1の行のみ採点。hexがfile名の一部・pathの無いhex行は採点
  しない）。`schema_version` 3。
- `tests/test_operational_metrics.py`【拡張】：追加3本＝計12本。schema固定試験は3へ改名・
  期待値更新（意図保存＝現行schema値の固定。exit-code前例の型）。
- `records/development/2026-08-18-operational-metrics-dataset-v3.json`【新設・機械固定】。

## 2. RED→GREEN（正直な記載）

- RED：追加3本中**2本失敗**（表行の採点・pathless行のunpaired）。「hexがfile名の一部を採点
  しない」は書式C未実装の現状でも自明に成立するためRED不能——偽装への恒久固定として追加。
- GREEN・受入：**受入測定ブロック
  `records/development/2026-08-18-operational-metrics-v3-evidence-measurements-v1.md`参照**——
  12本 exit 0（決定的射影）・dataset v1／v2の不変（既知digest一致）とv3・装置・試験のdigest固定。
  全entry二重実行一致。`git diff --check`合格。

## 3. dataset v3の要旨（従軸H5の拡充）

- 採点対象**268→1,193組（+925＝書式Cの寄与）**：一致848（71.1%）・不一致311（26.1%）・
  欠落34（2.9%）。採点外＝組の閉じない出現585・総hex 2,881・走査713 record。
- 定義の限界（正直な記載）：書式Cのpathはrepo root以外を基点に書かれた行（私有領域相対等）を
  含み、欠落34にはその種の「基点違い」が混在しうる。基点別解決はv4の論点。

## 4. 受入条件の照合

1 RED＝§2どおり合格（RED不能1本は明記）／2 GREEN 12本＝合格／3 dataset v3固定・v1 v2不変＝
合格／4 計画writer仕上げ・証明書`start_allowed: true`（`00f83f0`）＝合格／5 diff・commit・
transitionは本record commit後に実施。

## 5. v4へ繰り越し

H4手動記入率・コスト（セッションログ時系列）・`digest_differs`履歴照合・書式C欠落の基点別解決。

## 6. 未実施

- TODO・見取り図反映とcommit。push（利用者の運用に従う）。
