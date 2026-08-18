# 測定ブロックの機械生成tool 実行Evidence v1

- 記録日：2026-08-18
- 指示者：利用者（Human）。選択文言「単位2（測定ブロックの機械生成）に着手してください。
  事前走査から」（2026-08-18 chat）
- 記録者：Claude
- 範囲固定：作業票`docs/development/2026-08-18-measurement-block-work-ticket-v1.md`
- 事前走査：`records/development/2026-08-18-measurement-block-prescan-v1.md`
- 基準commit：`82089b4`→文書commit `2efdb39`→証明書commit `a815365`→実装は本recordと同一commit

## 1. 成果物

| file | 内容 | SHA-256 |
| --- | --- | --- |
| `tools/development/measurement_block.py`【新設】 | 宣言JSON→argv実行→機械生成markdown（new-only・fence耐性・切り詰め印・0／1／2） | `2fb69a27d4b1449cfb61c52ecffda3dde385fdf8299eac7c65396a5da45118e4` |
| `tests/test_measurement_block.py`【新設】 | 7本（生成内容・new-only・入力不備・非0はデータ・**fence偽装**・切り詰め印・spawn失敗） | `362ed3807083a0f9dcf03c5e52a43bda36b74390cebbecc37a5a6490a40120d3` |
| `records/development/2026-08-18-measurement-block-dogfood-commands-v1.json`【新設】 | dogfooding用の宣言JSON（LLMが書くのは意味の選定＝これだけ） | 生成物冒頭に機械埋め込み |
| `records/development/2026-08-18-measurement-block-dogfood-measurements-v1.md`【新設・機械生成】 | 本作業単位のGREEN測定の機械固定（下記§3） | `15ed9bb306f4211e6438820fe828f651421e6482033045b341104c0936255dfa` |
| `docs/development/prompts/scope-prescan-run.md`【改定】 | 数値の記録規律1〜2項を「測定ブロックが原則・転記は例外」へ | `aabdd3ee4c5c7626edce96559f91c97b9e30e1078ece04212a0f725a596f5abf` |

## 2. RED【機械出力の転記・tool新設前のため例外的に転記】

```text
$ .venv/bin/python3 -m pytest tests/test_measurement_block.py -q
7 failed in 0.03s
RED exit=1
```

## 3. GREEN【転記なし・機械生成fileを参照】

**`records/development/2026-08-18-measurement-block-dogfood-measurements-v1.md`を参照**
（本tool自身による機械生成。新設7本・流用元保護10本・掃引25本の各単独緑と、遡り一元化の維持
（`parents[`は`tools/common/roots.py`の1件のみ）が、**LLMの転記を経由せず**固定されている）。
`git diff --check`合格。

## 4. 受入条件の照合

| # | 条件 | 結果 |
| --- | --- | --- |
| 1 | RED：新設試験が実装前に失敗 | 合格（§2・exit 1） |
| 2 | GREEN：新設＋record_run系＋掃引 各単独0 | 合格（§3の機械生成fileが根拠） |
| 3 | dogfooding：Evidence測定を本tool自身で生成 | 合格（§3。宣言JSON→生成→参照の全周） |
| 4 | fence偽装の敵対fixture試験を含む | 合格（試験(e)。外側fenceが自動で伸び内容は無加工） |
| 5 | 証明書`start_allowed: true` | 合格（commit `a815365`・直接一致23件。検索は`--plan`のみの新CLIで実行＝前単位の成果の初実戦） |
| 6 | diff・意味単位commit・transition | diff合格。commit・transitionは本record commit後に実施 |

## 5. 効果（構造的に消えた手作業）

事前走査・Evidenceの実測節で、LLMがやることは**宣言JSONを書くこと（どのコマンドで測るかの意味
選定）だけ**になった。実行・出力の固定・時刻・宣言fileのdigest埋め込みは機械が行い、転記・省略・
推測の余地が行為として存在しない。転記は「生成物を使えない例外」へ格下げされた（手順書改定）。

## 6. 未実施

- TODO反映とcommit。push（利用者の運用に従う）。
- 過去recordの実測節の遡及書き換えは範囲外のまま（以後の新規作業から適用）。
