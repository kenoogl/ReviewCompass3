# 既定値化の横展開（reviewer-launch・request-builder）実行Evidence v1

- 記録日：2026-08-18
- 指示者：利用者（Human）。文言「精査結果をrecordに固定し、対策1（既定値化の横展開）に着手して
  ください。事前走査から」（2026-08-18 chat）
- 記録者：Claude
- 範囲固定：作業票`docs/development/2026-08-18-cli-defaults-rollout-work-ticket-v1.md`
- 事前走査：`records/development/2026-08-18-cli-defaults-rollout-prescan-v1.md`（実測＝測定ブロック2枚）
- 基準commit：`ccf2edc`→文書commit `156bac7`→証明書commit `a53b182`→実装は本recordと同一commit

## 1. 成果物（digestは受入測定ブロック§「変更4fileのdigest固定」が正）

- `tools/reviewer_launch/entry.py`【変更】：launchの`--repository`・`--private-root`を任意化。
  既定＝cwd・`default_private_root()`（home配下私有領域）。checkのG30形は不変。
- `tools/request_builder/entry.py`【変更】：parserへ`optional=()`対応を追加。assembleの
  `--date`（既定＝機械の当日日付）・`--repository`（既定cwd）、単体checkの`--repository`
  （既定cwd）を任意化。G30の`--input-root`形は不変。
- `tests/test_reviewer_launch.py`・`tests/test_request_builder.py`【拡張】：追加4本
  （既定解決の機械確認・既定値・当日日付・check省略）。既存試験は無変更。
- 手順書2件【縮小】：雛形から廃止placeholder行を削除し自動解決の注記へ（run-id＝意味符号で
  操作者命名、の明記を含む）。

## 2. RED→GREEN

- RED：追加4本のみ失敗（launch側2・builder側2）・既存108本緑・単独終了コード1
  （tool新設前の例外的転記。以後の測定は機械生成）。
- GREEN・受入確認：**受入測定ブロック
  `records/development/2026-08-18-cli-defaults-rollout-evidence-measurements-v1.md`を参照**——
  launch 70本・builder 42本・bridge 4本 各単独0／既定`private_root`の実機値が従来の正準保存先と
  一致／廃止placeholderの残存検索が該当なし（exit 1＝合格側）／変更4fileのdigest固定。
  `git diff --check`合格。

## 3. 受入条件の照合

| # | 条件 | 結果 |
| --- | --- | --- |
| 1 | RED：追加4本のみ失敗・既存緑 | 合格（§2） |
| 2 | GREEN：3試験file各単独0 | 合格（受入測定ブロック） |
| 3 | 手順書に廃止placeholder残存なし | 合格（同・grep該当なし） |
| 4 | 既定値の実機確認を測定ブロックで固定 | 合格（同） |
| 5 | 証明書`start_allowed: true` | 合格（commit `a53b182`・直接一致2件＝検索CLIの`default_runtime_root`前例） |
| 6 | diff・意味単位commit・transition | diff合格。commit・transitionは本record commit後に実施 |

## 4. 効果と裁定の記録

- 起動・組み立ての手入力は**束縛系（request・expected-sha256）と意味系（run-id・slug・title・
  type）だけ**になった。正準path・日付・repositoryの手組み立ては行為として消滅。
- **run-idは機械採番の対象外と裁定**（意味符号。精査record §2の該当箇所はこの趣旨で読む）。
- repository既定＝**cwd**（`roots.repo_root()`はRC3自身のrootでありpip導入後の対象アプリでは
  誤るため。デプロイ整合の設計判断＝事前走査§2-4）。

## 5. Humanの確認が要る点（覆せる形）

1. private基底（`~/.reviewcompass3-private`）文字列の共有化（`roots.py`へ集約＝指紋pin更新と
   Issue限定再開を伴う）。現状2箇所（検索CLI・本件）。
2. 対策2（計画JSON writer）・対策3（review-planのcommit既定取得）の着手時機。

## 6. 未実施

- TODO反映とcommit。push（利用者の運用に従う）。対策2・3。
