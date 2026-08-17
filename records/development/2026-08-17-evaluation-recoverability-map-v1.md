# 評価指標の復元可能性表 v1

- 記録日：2026-08-17
- 記録者：Claude
- 上位計画：評価データ取得計画v1（`docs/development/2026-08-17-evaluation-data-acquisition-plan-v1.md`）
  §3。作業票＝`docs/development/2026-08-17-launch-metrics-recoverability-work-ticket-v1.md`
- 型の出自：初代ReviewCompassの`docs/notes/api-review-exchange-log-analysis/recoverability.md`
  （指標の復元可能性を正直に固定する流儀）
- 凡例：**可**＝現記録から機械復元できる／**追記後可**＝本作業（launch計測メタ・commit
  `b33b72b`）以後の実行から取得できる（過去分は不能または近似）／**装置後可**＝実験装置
  （計画§4順序2〜4）の新設後に生成される／**不能**＝記録がなく復元できない（対策を併記）

## 1. RQ1（Contract completeness）——実験時に生成（記録依存なし）

| 指標 | 復元可否 | 手段・根拠 |
| --- | --- | --- |
| obligation-to-plan coverage | 装置後可 | 既存compiler（`tools/task_contract/contract.py`の`PLAN_VIEWS` 6種・実在確認済み）のcompile出力と義務の機械照合 |
| Requirement-to-obligation coverage | **可** | `REQUIREMENT_OBLIGATIONS`表（16要求・contract.py）から機械算出 |
| 同一入力からの再生成一致率 | 装置後可 | compile再実行のbyte／構造比較（決定性の実証） |
| negative case検出率・誤停止率 | 装置後可 | 欠落・競合・stale注入fixture（敵対fixtureの既存流儀） |

## 2. RQ2（Context scalability）

| 指標 | 復元可否 | 手段・根拠 |
| --- | --- | --- |
| review input tokens | **可（過去分も）** | raw応答内の`usage`・`input_tokens`（cr-014-001実物で存在確認【実測】）を`reviewer.raw.json`から機械解析 |
| review input bytes（prompt規模） | **追記後可** | `launch.json`の`prompt_bytes`（本作業で追加）。過去分は`prompt_sha256`のみで**不能**（sha256から長さは導出できない） |
| 実行時間 | **追記後可** | `launch.json`の`started_at`／`finished_at`／`elapsed_seconds`。過去分はセッションログのツール実行タイムスタンプから**近似復元可** |
| source universe bytes・impact closure size | 装置後可 | paired evaluation装置（計画§4順序4）が生成 |
| Evidence Coverage・Finding recall／precision・責務外Finding率 | 装置後可＋人手 | 正解付きケースの人手固定が前提（素材：cr-系判定record 12件のfindings＝根拠path・行つき）。findingsの根拠被覆のみ現recordから部分算出可 |
| Human escalationの正否 | **可** | 判定recordの`unexamined`欄・停止reason（`LaunchStop`系）の記録から機械抽出 |
| 金銭費用 | **不能（直接記録なし）** | raw応答に費用欄なし（実物で`cost` 0箇所【実測】）。対策：トークン数×単価の近似で代替し、近似であることを明示する |

## 3. 従軸（運用計測）

| 指標 | 復元可否 | 手段・根拠 |
| --- | --- | --- |
| H4：assemble／check／launchの所要時間 | **可（近似）** | セッションログ（全量保全・契約014で前置つきfileも構造化解釈可）のツール実行タイムスタンプから復元。launchは追記後`elapsed_seconds`で正確化 |
| H4：手動記入箇所数・自動導出率 | **可** | 依頼recordのplaceholder（`<<記入:`）計数と雛形の機械欄比率（request-builderのcheckが同形式を検査済み） |
| H5：追跡可能率・Provenance完全性 | **可** | records/のdigest束縛（受入判断の束縛表）と私有領域raw対応の機械照合 |
| H7：承認点の分布・問い合わせ数 | **可** | Decision recordの承認文言欄（全記録に転記済み）＋セッションログの復元 |
| コスト：セッションの道具呼び出し数・時間 | **可** | セッションログから機械集計（実証例：2026-08-17朝の「指示から10分00秒・45回」計測） |

## 4. 本作業で塞いだ欠落と残る欠落

- 塞いだ：レビュー起動の時間・prompt規模（`launch.json` 4項目・commit `b33b72b`。以後の全起動が
  自動で論文データになる）。
- 残る欠落（正直な申告）：(a) 過去起動（cr-011〜014）のprompt bytesは復元不能、(b) 金銭費用の
  直接記録なし（近似のみ）、(c) Finding品質系は正解付きケースの人手固定なしには算出できない。
- 次に効く事実：トークンはraw応答から過去分も取れるため、**過去12起動もRQ2の部分データとして
  使える**。

## 5. 受入条件との対応（作業票v1 §4）

1. 正式検索証明書：`records/development/2026-08-17-launch-metrics-reuse-search-attestation-v1.json`
   （commit `39d2881`・`start_allowed: true`・直接一致16件）
2. RED：commit `ac26811`（新試験1本のみ失敗・既存67本緑・単独終了コード1）
3. GREEN：commit `b33b72b`（reviewer_launch 68本＋request_builder 40本＝108本、G30運用契約
   75本——各単独終了コード0）
4. 実機確認：試験（模擬実行）で代替（外部起動は承認境界のため。次回の実運用起動が初実データ）
5. 復元可能性表：本record
6. commit・transitionは完了報告時に最終確認
