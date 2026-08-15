# 一件の要求候補整合検査 実装成功Evidence v1

- 実施日：2026-08-16
- 契約：`TC-RC3-PRODUCT-ONE-REQUIREMENT-FEATURE-SOURCE-005 / v3`（採用済み）
- 採用判断：`records/development/2026-08-15-one-requirement-candidate-consistency-check-adoption-decision-v1.md`、commit `18731d6981dd5dd19bf164a2e5956f6472180a8d`
- 実装担当：Claude
- 方式：テスト駆動（失敗試験の固定→最小実装）

## 1. 失敗試験の固定（RED）

【実測】対象試験`tests/test_one_requirement_feature_source.py`を先に作成し、単独実行で111件全件が
実装未存在により失敗することを確認した（`111 failed`、終了コード1）。RED状態をcommit
`da8c700`（試験1 fileのみ）へ固定した。

## 2. 最小実装（GREEN）

【実測】契約§12の変更上限内で次を実装した。

1. 検査核 `tools/requirements/one_requirement_feature_source.py`（新規）
2. 入口 `tools/requirements/one_requirement_feature_source_entry.py`（新規。G08の`read_input_pair`だけを再利用し、
   停止元`design`→`catalog`、`acceptance`→`candidate`へ変換）
3. `pyproject.toml`へ実行名`reviewcompass3-requirement-candidate-check`一件を追加

## 3. 試験の訂正2件（理由の記録）

【記録】GREEN到達前に、試験側の作成誤り2件だけを訂正した。実装・契約に合わせた変更ではなく、
試験自身が契約と食い違っていた箇所である。

1. `test_selected_candidate_and_historical_enter_queue_in_fixed_order`：正常結果の`obligation_sources`は
   義務ID昇順で返る契約（§10）に対し、試験が並べ替え前の先頭位置`[0]`を参照していた。義務IDで対象項目を
   特定する形へ訂正した。
2. `test_aws_key_in_sha256_member_still_stops`：AWS鍵形式の後に44文字を連結した値は語境界が消えて
   既定patternに一致しない。契約§11「SHA-256欄の形を判断できない場合は除外せず機微検査する」の意図どおり、
   AWS鍵形式そのもの（20文字）を置く形へ訂正した。

## 4. 機械確認（各単独command・終了コード個別判定）

【実測】

- 対象試験：`.venv/bin/python3 -m pytest -q tests/test_one_requirement_feature_source.py`
  → 111件成功、終了コード0
- G24関連（5 file）：59件成功、終了コード0
- 要求artifact関連（2 file）：21件成功、終了コード0
- G08対象：107件成功、終了コード0
- G24保護10 path：`git diff --exit-code 0583863e…`終了コード0、差分0
- 正規全試験（既存の禁止認証隔離条件
  `env -u ANTHROPIC_API_KEY -u ANTHROPIC_AUTH_TOKEN -u ANTHROPIC_BASE_URL -u ANTHROPIC_FOUNDRY_API_KEY -u ANTHROPIC_VERTEX_PROJECT_ID -u AWS_BEARER_TOKEN_BEDROCK`）：
  2,238件成功、終了コード0
- 通常host環境の全試験は既存`tests/test_claude_implementation_executor.py`の12件だけが不合格。実装前の
  clean HEAD（`da8c700`）を一時worktreeへ展開して同fileを単独実行し、同一の12件が不合格であることを確認した。
  既知のhost認証環境差であり、本実装の退行ではない（G08受入時と同じ判断）。
- `git diff --check`：終了コード0

## 5. 合成一件E2E（受入条件17・22）

【実測】`pip install -e .`で配置した正式実行名`reviewcompass3-requirement-candidate-check`を、
repository外の現在位置から実行した。終了コード0、標準エラー0 bytes。

- catalog：`CAT-E2E-G24`、出典3件（effective・candidate・historical各1）
- 全出典採否：3件selected。全原子義務8件が採用出典へ対応
- counts：`candidate_sources` 1、`effective_sources` 1、`historical_sources` 1、`selected_sources` 3、
  `not_selected_sources` 0、`traced_obligations` 8
- 人の判断一覧：`requirement_candidate`→`candidate_source_selection`（SRC-DRAFT）→
  `historical_source_selection`（SRC-OLD）の固定順
- verdict：`review_required_pending_human_decision`、`promotion_status: not_promoted`
- 内容識別値：catalog `cac33259d53649a2154ed2a37b32c6b59bb8a186334fc69fe0ebfc18ba402ec6`、
  candidate `66f6db08e480977747326fbfee901a43edae332bacb60ca44d44e51621cca083`、
  feature `9c76c7864002e29b2eab5fb69a14cae29e8fff6cc2e39f4113499a24c2a37a24`、
  requirement `00237822773c4b0d6c56155f6b568e8adf01ab181c5b5b3e2097a390aaadb23d`、
  trace `cb361d4f06cda8ca22e60701d42750371839c445c6db7f83b94e5a507945639e`、
  result `a65268bc962e82db5437191f3b4bbef10d20869b374ed8a776f89cc3391a50d8`
- 安全表示：出力へ入力自由文、採否理由、出典SHA-256、絶対pathの漏えい0件を機械確認した

## 6. 受入条件の対応

【実測】受入条件1〜17は対象試験111件が覆う（§10完全一致、表現順不変、独立oracle再計算、機微6種、
規則file照合、path安全、停止表、別現在位置同一bytes、禁止作用不在を含む）。18〜20は§4の各単独commandで確認した。
21の独立確認と22の提示、23の利用者受入は未実施の後続である。

## 7. 未実施

- 独立完了レビュー（受入条件21）
- 利用者の製品受入（受入条件23）
- G24の要求作成責務、候補4以降、外部送信
