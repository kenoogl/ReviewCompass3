# 契約010 実E2E第2試行（e2e-010-002）Evidence v1

- 記録日：2026-08-16
- 記録者：Claude
- 実施根拠：利用者の明示指示「e2e-010-002で再実施して」（2026-08-16 chat）
- 結果：**停止（`response_model_unobserved`・終了コード2）。§9-8は未成立のまま**。ただし
  agyのstream実形式と停止の真因を完全に実測でき、訂正を適用した

## 1. 実施と停止【実測】

- 起動：第1試行と同一対象・同一期待SHA-256、run-id `e2e-010-002`、訂正済み引数（`--print=<本文>`）。
- agy process終了コード0。未加工出力・起動recordは私有領域`e2e-010-002/`へ不変保存。

## 2. 判明した実形式【実測】

1. streamのevent鍵は`event`（`init`／`step_update`／`result`）である（想定していた`type`鍵ではない）。
2. **model表記は`init.model`にあり、値は`gemini-3.1-pro-high`（許可一覧と一致）**。停止理由
   `response_model_unobserved`は、旧実装がtop-levelの`model`鍵だけを探していたための解析側の問題。
3. 最終`result`は`{"status":"SUCCESS","response":"","usage":{...}}`で**`response`が空文字列**。
4. 空になった真因：`init.permission_mode`は`request-review`（道具使用ごとに人の承認を求める方式）。
   headlessでは承認者が不在のため、Reviewerが起動promptの指示どおり`shasum`を実行しようとした時点で
   `User denied permission to run command`（step_updateのERRORに記録）となり、会話がそのまま終了した。
5. Reviewerへ提供される道具56種には読取り系（`view_file`・`grep_search`・`list_dir`等）が存在する。
   consumption：入力20,133 token・出力905 token・9.6秒（依頼recordの内容は読まれる前に終了）。

## 3. 訂正【実測】

1. **読み取り専用相当の確定**：固定引数へ`--mode=plan`を追加。契約§7.1が「sandbox・作業ディレクトリの
   扱いはRED段の実測で確定」と留保した事項の確定であり、禁止対象（`--dangerously-skip-permissions`・
   書込みを許す`--mode=accept-edits`）は不使用のまま。
2. **固定promptの訂正**：端末command実行の指示を撤去し、「読取り道具のみ使用・許可を求める道具の不使用・
   digest機械計算が不能な場合はfreshnessを`not_computable`＋理由で申告・最終応答は判定JSONのみ・
   未検査はunexaminedへ明示」へ変更（自己レビューSR-C10-2の設計どおり、鮮度の硬い関門はアダプタの
   二重再計算のまま）。
3. **stream解析の訂正**：model抽出を`init.model`へ、判定抽出を`event=="result"`の`result.response`
   （JSON本文の文字列）へ変更。`response`空は`verdict_schema_nonconforming`で停止（本試行の事象を
   固定する試験を追加）。
4. 検証：対象試験33件単独緑、禁止認証隔離条件の正規全試験2,408件成功・終了コード0。

## 4. 残り

- §9-8実E2Eは未成立。再実施は新識別子`e2e-010-003`で利用者指示を得て行う。
- 残る未知：plan modeで読取り道具が実際に自動許可されるか、`--json-schema`の強制が最終`response`へ
  実際に働くか。不成立なら同じ型（停止→raw診断→訂正→承認→新識別子）で反復する。
