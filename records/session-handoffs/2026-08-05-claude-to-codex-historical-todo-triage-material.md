# Claude → Codex：過去TODO候補のHuman triage資料 作成完了報告

## 実施内容

指示（`records/session-handoffs/2026-08-05-codex-to-claude-historical-todo-triage-material.md`）に従い、Human triage資料を一件だけ作成した。

- 作成file：`records/development/2026-08-05-historical-todo-intake-triage-material-v1.md`
- 入力正本：`records/development/2026-08-05-historical-todo-intake-candidates-v1.json`（無変更）
- 入力正本のSHA-256：`e01c0feb082712f8ef0f77bfa4f031fbdc4530ed51f331f7dafbfd133d479a3e`（資料内に記載済み）

## commit

- commit SHA：`88f8cacd56800b735631303f7502d6353cb56809`
- commit内容：資料1fileのみ、247行追加。他fileの変更なし。
- `git diff --check`：合格（exit 0）。stage後の`git diff --cached --check`も合格。
- この完了報告はcommitに含めていない。

## 束の数

9束（束A〜束I）。内訳は次のとおり。

| 束 | テーマ | 件数 |
| --- | --- | --- |
| 束A | 機械が組み立てるべき命令をLLMが直接組み立てて失敗した | 5 |
| 束B | 記録そのものの生成・配置を機械化する候補 | 5 |
| 束C | 機械側で起きた観測で、その場で閉じたもの | 4 |
| 束D | 着手していない実装・設計の項目 | 6 |
| 束E | 記録の保存場所・保存期間・自動化に関する運用判断 | 4 |
| 束F | どれが正本かと、古い版の保持 | 7 |
| 束G | 承認された範囲と、まだ承認していない範囲の境界 | 4 |
| 束H | 検証手順と報告様式の取り決め | 2 |
| 束I | 作業の開始・再開の条件（blocker） | 4 |
| 合計 | | 41 |

## 候補41件の一致確認（機械確認）

Pythonで入力JSONと資料本文の候補ID集合を照合した。結果は次のとおり。

- 入力候補数：41
- 束セクション（第3節）に出現する候補ID：unique 41／延べ 41 → 各IDちょうど1回、入力集合と完全一致、重複・欠落なし
- 判断表（第5節）に出現する候補ID：unique 41／延べ 41 → 入力集合と完全一致、表の行数41行、列数はすべて一致
- 資料全体に、入力集合に存在しない候補IDの出現なし

## 未実施事項（指示どおり行っていないこと）

- 候補一覧、config、schema、validator、code、test、既存Issue、TODO、Plan、checklist、Decision recordの変更：なし
- triage decision、正式Issue、root cause candidate、Plan、Workの作成：なし
- `human_fields`の記入：なし（資料の判断表は`未解決`以降すべて`Human記入`のまま）
- 採否、priority、Issue昇格、統合、再開の決定：なし
- 実装、外部送信、push、PR、CI、Work 4B、Work 6A、E2以降の開始：なし

## 補足

- 資料冒頭に、非権威資料であること、正本は候補一覧であること、束分けと確認順は提案であること、この資料が正式Issue・triage decision・Plan・Workの根拠にならないことを明記した。
- `duplicate_suspect: false`が機械的照合の結果にすぎず、意味的な重複なしを保証しない旨を第1節に明記した。
- 引用が短く現状が読み取れない候補には`原文確認が必要`と明記した（束D全6件、および`HTC-E7E2F692`、`HTC-BEB5E0BD`、`HTC-045A8FB5`の一部、`HTC-14D810C7`）。
- 確認順は3段階の提案として記載し、各段階に置いた理由を明記した。priorityとdispositionは確定していない。束Aの`HTC-C9F6C917`はGit書込み権限に触れるため段階1寄りの扱いをHumanが選ぶ余地がある旨を注記し、位置を確定していない。
