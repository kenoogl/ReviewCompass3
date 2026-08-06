# 報告の信頼性規則をAGENTS.mdへ追記する 承認Decision v1

- Decision ID：`DEC-RELIABLE-REPORTING-RULE-001`
- decision maker：Human
- decided at：`2026-08-07T06:28:01+09:00`
- decision：`approved`（Human文言「信頼できる報告を得る方法として、提案してもらった内容は効果がある。AGENTS.mdへ追記しよう。」）
- decision class：`operational_guidance_decision`
- 関連Decision：`DEC-DEEP-DIVE-STOP-RULE-001`

## 1. 経緯

2026-08-06、Claudeが「本線を進めればすぐ負例に当たる」という主張を、検証済みの対応表record
（`records/development/2026-08-06-work6a-negative-path-test-inventory-v1.json`）に答えがあるにも
かかわらず、その場の浅い検索だけで出し、誤りだった（3項目中2項目は被覆済みだった）。
Humanは「調査が甘いので、2点3点する。信頼できる報告はどうやったら得られるか」と問い、
Claudeが再発防止の方法を提案した。以後このsessionで実際に運用し、Humanが
「効果がある」と評価して`AGENTS.md`への追記を承認した。

## 2. 追記内容

`AGENTS.md`へ新しい節「報告の信頼性規則」を追加した。要点は次である。

- 事実の主張に出どころのラベルを付ける：【実測】（commandを実行して確認、commandと結果を示す）、
  【記録】（検証済みrecordから引用、pathを示す）、【推測】（未確認）。
- 人の判断に影響する主張は【実測】か【記録】だけで出す。
- 主張を出す前に、答えを持つ既存recordを先に探す（検索よりrecordが先）。
- 重要な主張は、出す前に反証を1つ機械で試す。
- ラベルの無い主張は確認を省いた印であり、利用者は出どころを問い返してよい。

既存節の削除・書換えはしていない。規則は判断の規則であり機械では守らせられないことを、
深掘りの停止規則と同様に本文へ明記した。

## 3. 検証

| 項目 | 結果 |
| --- | --- |
| `AGENTS.md`のSHA-256（追記後） | `b0e4039b1f14a5eccda001b8c700324b5df57544fc3d43de77c74f6084bf3f58` |
| 入口Testと経路Test（`test_todo_handoff_prompt_entrypoints.py`＋`test_agents_lane_guidance.py`） | `6 passed` |

## 4. 既存recordへの影響

new-onlyで作成した。既存recordの上書き、削除、無効化、stale化はしていない。
