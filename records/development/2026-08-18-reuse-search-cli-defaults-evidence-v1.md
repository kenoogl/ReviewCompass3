# 正式再利用検索CLIの引数廃止 実行Evidence v1

- 記録日：2026-08-18
- 指示者：利用者（Human）。選択文言「1（引数の廃止）から着手してください。事前走査から。」
  （2026-08-18 chat）
- 記録者：Claude
- 範囲固定：作業票`docs/development/2026-08-18-reuse-search-cli-defaults-work-ticket-v1.md`
- 事前走査：`records/development/2026-08-18-reuse-search-cli-defaults-prescan-v1.md`
- 基準commit：`8c9b29b`→文書commit `a69b0ce`→証明書commit `597a755`→実装は本recordと同一commit

## 1. 成果物

| file | 内容 | SHA-256 |
| --- | --- | --- |
| `tools/development/formal_code_reuse_search.py`【変更】 | `default_runtime_root()`・`latest_policy_file()`新設。`--runtime-root`／`--universe`／`--policy`任意化＋自動解決、`--captured-at`旗を削除 | `f9faab7074e0320d385937f27b52f9d387a6041e008a1723c62c0ac781af0077` |
| `tests/test_formal_code_reuse_search.py`【拡張】 | 追加4本（数値最大版選択・既定保存先・解決不能停止・旗拒否）＝計12本 | `649739902416485867c1c3e5aedf761237f2b79717f394b5f066da17cac0773d` |
| `docs/development/prompts/scope-prescan-run.md`【縮小】 | コマンド雛形を`--plan`のみへ。正準値転記の指示を自動解決の説明へ置換、規律節5項を「既定値へ実装して引数ごと消す」へ改定 | `62a82c8a41e7d4429bc0560081b6b981d62791d7e075347800d4f0f161ade9e1` |

## 2. RED→GREEN【機械出力の転記】

- RED：`4 failed, 8 passed`・単独終了コード1（旗拒否試験は当初、別理由で偶然通ったため
  stderr文言`unrecognized arguments: --captured-at`の検査へ厳密化してから確認した）。
- GREEN：`12 passed`・`tests/test_layout_baseline.py`緑——各単独終了コード0。
  `git diff --check`合格。

## 3. 既定解決の実機確認【機械出力の転記】

```text
default_runtime_root: /Users/keno/.reviewcompass3-private/reuse-search
universe: .reviewcompass/policies/work4a-source-universe-v8.json
policy: .reviewcompass/policies/work4a-freshness-policy-v11.json
```

従来の正準保存先と一致し、方針fileは数値最大版（freshness v11＝辞書順ならv9を誤選するところ、
数値比較で正しくv11）を返す。

## 4. 受入条件の照合

| # | 条件 | 結果 |
| --- | --- | --- |
| 1 | RED：追加4本のみ失敗・既存8本緑 | 合格（§2。厳密化の経緯も同節） |
| 2 | GREEN：12本＋layout系 各単独0 | 合格 |
| 3 | 既定解決の実機一致（保存先・universe v8・freshness v11） | 合格（§3） |
| 4 | 手順書雛形が`--plan`のみ | 合格（§1） |
| 5 | 証明書`start_allowed: true`（変更前CLIの最終実行） | 合格（commit `597a755`・直接一致4件） |
| 6 | diff・意味単位commit・transition | diff合格。commit・transitionは本record commit後に実施 |

## 5. 効果（構造的に消えた手作業）

検索実行の手入力は「作業別計画のpath」1つだけになった。保存先の手組み立て（誤指定事故の型）・
方針fileの版選び（辞書順の罠）・時刻の手書きは、以後**行為として存在しない**。

## 6. 未実施

- TODO反映とcommit。push（利用者の運用に従う）。
- 提案の単位2（測定ブロックの機械生成tool）は未着手のまま。
