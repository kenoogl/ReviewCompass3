# 契約016 実装Evidence（RED先行→最小実装→GREEN） v1

- 実施日：2026-08-20
- 担当：Claude
- 契約：`TC-RC3-PRODUCT-MODEL-SELECTION-CORRESPONDENCE-016` v2
- 実測の正本：測定ブロック
  `records/development/2026-08-20-contract-016-green-measurements-v1.md`（宣言
  `records/development/2026-08-20-contract-016-green-commands-v1.json`。10項目・二重実行一致・
  非決定0件。**合否はすべて`exec`置換の単独実行＝entry exitがpytest自身の終了コード**＝契約015
  の是正C15-REVIEW-001の教訓を最初から適用）
- RED再現の正本：`records/development/2026-08-20-contract-016-red-replay-output.txt`
  （C15-REVIEW-002の教訓の先回り適用。第三者はgit履歴だけから次の3 commandで機械再現できる）

```text
git worktree add <一時dir> dee7523
git -C <一時dir> checkout 6172a26 -- tests/test_reviewer_launch.py tests/test_request_builder.py
（<一時dir>で）.venv/bin/python3 -m pytest tests/test_reviewer_launch.py tests/test_request_builder.py -q --tb=no -p no:cacheprovider
```

結果＝**単独pytest終了コード1・`17 failed, 139 passed`**（現行試験を実装前commit `dee7523`の
コードへ適用。契約016の新規挙動が実装前に失敗することの機械証明）。

## 1. RED先行の確認【実測・例外転記】

失敗試験を先に固定した（新規20本＋既存pin 3本の整理）。実装前の初回実行（例外転記。揺れは
実行時間のみ）：

- 再現コマンド：`.venv/bin/python3 -m pytest tests/test_reviewer_launch.py tests/test_request_builder.py -q --tb=no -p no:cacheprovider`
- 末尾出力：`18 failed, 138 passed in 9.85s`
- 読み：新規20本のうち18本が失敗（期待どおりの赤）。設計上改修前でも通る2本（組み立てgolden
  pin＝改修前実装から機械取得した正規化SHA・登録簿data-driven pin）と既存全数が合格。

## 2. 途中の是正2件（試験側。製品コードの手戻りではない）

新設の起動前照合（記載と実行の対応＝必須gate）により、起動helperと既存試験1本が使っていた
「依頼先行なしのfixture record」が停止するようになったため：

1. 起動helper 3種を「照合に適合する正準依頼先行つき依頼recordを機械生成する」形へ書き換え
   （既存試験の本体・assertは無変更。subagentの受容根拠参照は従来のfixture recordへ戻して
   既存assertを維持）。
2. `test_agy_model_check_uses_agy_list_not_union`（起動を直接組む既存試験）のrecord生成を
   依頼先行つきへ変更（assert無変更）。fixture record自体は無変更のまま、依頼先行の無いrecordの
   fail-closed停止を確認する新規試験（`test_launch_missing_reviewer_line_fails_closed`）の
   素材として残す。

## 3. GREEN【実測＝測定ブロック参照】

- 5 suite（reviewer_launch／request_builder＝契約011対象／G30契約操作／RQ2装置／RQ2運搬部品）の
  **単独実行の終了コードすべて0**（各節のentry exit）。収集件数は測定ブロック参照
  （reviewer_launch・request_builder・波及3suite合算の各節）。
- **既定不変golden**：`--backend`／`--model`省略時の組み立て出力が改修前実装の正規化SHA-256
  （固定入力・改修前に機械取得）とbyte一致（§9-2。試験`test_assemble_default_output_byte_
  invariant_golden`）。
- **後方互換**：実record依頼先行の逐語fixtureで抽出互換（§9-3a）、既定組み立てrecordの新check
  合格（既存試験群が無変更で全緑＝§9-3b）。
- **保護対象**：契約§6の保護pathは基準commit（候補v2固定＝`3eab124`）から**差分0**（測定ブロック
  該当節・出力空）。
- 敵対fixture：fence内偽依頼先行・本文中同形行・backtick欠落・正準行除去の各騙されで
  fail-closed（新規試験で両向き固定）。

## 4. 実装内容（変更上限内・8 file）

1. `tools/reviewer_launch/core.py`：正準抽出核`extract_request_reviewer_line`（単一実装＝
   SR-C16-1どおり縦B側。fence状態追跡・正準領域限定）、`launch_review`の`model`任意入力
   （既定＝一覧先頭・非所属は`model_not_allowed`）、起動前の記載照合（新設2語彙
   `request_backend_mismatch`・`request_model_mismatch`・抽出不能はfail-closedで前者）。
2. `tools/reviewer_launch/entry.py`：`--model`任意旗。
3. `tools/request_builder/core.py`：`assemble`の`backend`／`model`入力（既定agy＝現行文言
   byte不変・他backendは新形差し込み）、checkの正準位置検査＋backend別所属検査（文書全体検索
   `_MODEL_PATTERN`の廃止。和集合記号は互換維持）。
4. `tools/request_builder/entry.py`：`--backend`・`--model`任意旗。
5. 試験2 file：新規20本＋pin整理3本＋helper適合（§2）。
6. 手順書2 file：選択の使い方・移行整理・**モデル追加手続き**（承認record＋定義1行＋pin 1行）。

## 5. 契約受入条件との対応

§9-1 RED先行＝§1・RED再現raw。§9-2 既定不変golden＝改修前取得pinとの一致。§9-3 後方互換＝
逐語fixture＋既存試験無変更全緑。§9-4 新設2語彙の両向き。§9-5 登録定型化＝data-driven試験＋
backendごとの承認pin 1本＋手順書節。§9-6 既存試験・保護差分0（正規全試験は受入段で実行）。

## 6. 未実施

- §9-7 実E2E（`--backend codex-cli --model gpt-5.6-terra`＝terra初起動。利用者の明示指示待ち）。
- §9-6の正規全試験（禁止認証隔離条件）は受入段で実行。§9-8 完了レビュー（agy）。§9-9 残余risk
  4点の確認と製品受入。
