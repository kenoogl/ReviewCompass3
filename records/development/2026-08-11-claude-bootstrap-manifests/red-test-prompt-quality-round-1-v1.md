# 無工具Claude疎通 RED受入試験 指示文品質確認 round 1

- 日付：2026-08-11
- 状態：`human_decision_required`
- 使用可否：`false`
- 操縦者：Codex主担当
- 操縦者モデル：`gpt-5.6-sol`
- 監査担当：Codex指示文監査用サブエージェント
- 判定担当：Codex指示文判定用サブエージェント
- 監査・判定モデル：`gpt-5.6-terra`
- 指示書：
  `records/development/2026-08-11-claude-bootstrap-manifests/red-test-implementation-request-v1.md`
- 指示書commit：`c7ecaa4d7df0ed2d213d96067cb2fdfbac9d88a4`
- 指示書SHA-256：`878067a952f8ca9d6ff842a9ddf80e4085fd6ee8e5cebf3621d7521a9345a002`
- 要求集合SHA-256：`75a87828c665c9e5096614858e3e8f4bd8b3413ff4487e13e66aaadfc1b7e85d`
- 品質確認周回：1 / 2

## 1. 機械検査

【実測】`python3 /private/tmp/reviewcompass3_red_prompt_preflight_v1.py`は終了コード0だった。検査器版は
`reviewcompass3-red-prompt-preflight-v1`である。

次を全件確認した。

- 指示書と固定材料9件について、指定commitのGit blob、現在file、記載SHA-256が一致した。
- 作業開始HEADは`c7ecaa4d7df0ed2d213d96067cb2fdfbac9d88a4`で、作業treeは変更なしだった。
- `AC-CB-001〜013`、`NG-CB-001〜007`、`ST-CB-001〜007`、`OUT-CB-001〜005`の32件は、
  宣言、参照ともに欠落0、重複0、未知参照0だった。
- 実行担当、対象、変更可能範囲、禁止範囲、停止条件、結果形式、モデル分離、RED限定、外部送信なしを
  検査した。
- 指示書は18,968 byteで機械上限1,000,000 byte未満、囲み記号の不整合0件だった。

【実測】既存の`pilot_collaboration`共通入口による`prepare`は終了コード2、
`stop_code: config_invalid`で保存前停止した。同入口は
`records/session-handoffs/2026-08-11-pilot-collaboration-entry-implementation-request-v6.md`を固定pathとして
要求するため、今回の新しい指示書には再利用できない。専用検査は実施したが、今回の実行段階台帳と結果保存は
`connected`とは扱わず、範囲固定どおり`specified_only`のままとする。

## 2. 指示文監査

- 未加工結果の保存種別：Git外のprivate local file
- 未加工結果SHA-256：`f553bf73e80496a1153b520a6e4b5e3093bffb24e2d5ad45d067681b363d5a23`
- 正規化済み監査結果SHA-256：`2bcc55e29459dfdcd4ee1aac8a16c0eb343041f57c6bef9c31605f1539a31913`
- 要求確認：32 / 32、欠落0、重複0、未知参照0

監査所見は4件だった。

### `PA-CB-RED-001`

- 分類：`target_mismatch`
- 重大度：`high`
- 対象要求：`AC-CB-012`、`OUT-CB-001`
- 根拠：範囲固定v3はprocess基準目録の入力を
  `e54fcdaec38ab4b755f67371dbbdd20604447b95`へ固定するが、指示書は
  `18ca2481233a9d6211c3b0b776cac5ec8527321c`へ差し替えている。両commit間の`tools/**/*.py`に差分がなくても、
  authorityが固定した入力identityと一致しない。

### `PA-CB-RED-002`

- 分類：`insufficient_material`
- 重大度：`high`
- 対象要求：`ST-CB-001`、`ST-CB-002`
- 根拠：指示書§2の固定材料には、範囲固定v3 §3が固定したIntent、用語集、計画、外部経路選択Human裁定、
  無工具段階選択Human裁定、範囲レビュー所見Human裁定が含まれない。このため、それらの変更をRED開始前停止へ
  結び付けられない。

### `PA-CB-RED-003`

- 分類：`insufficient_material`
- 重大度：`high`
- 対象要求：`AC-CB-009`、`ST-CB-002`、`OUT-CB-005`
- 根拠：指示書はClaude 2.1.220成功objectの必須keyを列挙するが、optional keyと失敗objectの`errors`を
  将来作るfixture由来記録へ委ねている。完全な正規化schema、または再現可能な静的抽出物とそのSHA-256が
  固定入力にないため、実装担当の推定を排除できない。

### `PA-CB-RED-004`

- 分類：`omission`
- 重大度：`high`
- 対象要求：`OUT-CB-001`
- 根拠：`declaration_red_map_check`は宣言数、test実在、共有test、`red_now`を検査するが、宣言keyが正本の
  32要求ID集合と一致することは検査しない。指示書にも、別testまたは別の機械検査で正本集合と完全一致させる
  明示がない。

## 3. 指示文判定

- 未加工結果の保存種別：Git外のprivate local file
- 未加工結果SHA-256：`c05daa37121bf2d3a486143a127541a65e3ac132b47030440aa258b7c5731eae`
- 正規化済み判定結果SHA-256：`4e216af9739c0ba99264fca624a48c87bfa9f6ebae46b6310f961252a1a3796f`
- 監査結果参照SHA-256：`2bcc55e29459dfdcd4ee1aac8a16c0eb343041f57c6bef9c31605f1539a31913`
- 所見照合：4 / 4、欠落0、重複0、未知参照0

判定担当は`PA-CB-RED-001〜004`をすべて`accept`推奨とした。理由はそれぞれ、authority上の基準commit
identity不一致、固定入力集合の不足、版固定schemaを再現する固定材料の不足、正本要求ID集合の機械照合不足が
実在するためである。

## 4. Human判断境界

【判断】モデルの推奨はHumanの採否ではない。4所見の採用、不採用、保留が指示書SHA-256
`878067a952f8ca9d6ff842a9ddf80e4085fd6ee8e5cebf3621d7521a9345a002`へ束縛して記録されるまで、指示書を
実装担当へ渡さない。

4件を全件採用する場合の修正候補は次のとおりである。

1. process基準目録の入力commitを範囲固定v3の値へ戻す。
2. 範囲固定v3 §3の固定入力を、重複転記せず対象commitの表から機械抽出して開始前検査へ接続する。
3. Claude 2.1.220の外側JSON完全schemaを、静的抽出の由来と内容指紋を持つ固定材料として先に作る。
4. 宣言key集合と正本32要求ID集合の完全一致を別の機械検査または固有testで固定する。

## 5. 未実施

- Humanによる4所見の採否
- 指示書v2の作成
- RED受入試験、fixture、process基準目録、宣言対応表の作成
- production実装、既存test変更、Claude起動、認証、外部送信、実Run、TODO更新、push
