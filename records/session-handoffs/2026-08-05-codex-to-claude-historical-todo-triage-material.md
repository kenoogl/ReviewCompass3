# Codex → Claude：過去TODO候補のHuman triage資料作成指示

## 誰が何をするか

- **Human**は、過去TODOから機械抽出された41候補を、正式Issueにするかどうか判断する。
- **Codex**は、Humanが41件を一件ずつ生の記録から読む負担を減らすため、判断資料の作成を指示する。
- **Claude**は、候補を平易に要約し、確認しやすい束へ整理した判断資料だけを作る。
- **Claudeは、採否、priority、Issue昇格、統合、再開を決めない。**

## 固定入力

唯一の入力正本は次である。

`records/development/2026-08-05-historical-todo-intake-candidates-v1.json`

- 候補数：41
- 候補ID：`HTC-...`
- `human_fields`：全件`null`
- 正式Issueへの昇格：0件

この候補一覧を修正しない。候補の原文引用とsource位置は、候補一覧を正本とする。

## Claudeが作るもの

次の新規資料一件だけを作る。

`records/development/2026-08-05-historical-todo-intake-triage-material-v1.md`

資料の冒頭に、次を明記する。

- これはHuman判断を助けるための**非権威の説明資料**である。
- 正本は上記の候補一覧である。
- Claudeによる要約・束分け・確認順は提案であり、Humanの裁定ではない。
- この資料は正式Issue、triage decision、Plan、Workを作る根拠にならない。

## 資料の内容

### 1. 全体像

次を短く示す。

- 41件の見出し別内訳（未実施7、残余risk15、手戻り・機械化候補14、blocker・Human判断待ち5）
- 重複疑い0件であること
- すべての`human_fields`が未記入であること
- 「候補がある」は「問題が未解決である」ことを意味しないこと。Humanが確認して初めて決まること。

### 2. Humanが判断する項目の平易な説明

各候補に対してHumanが決める5項目を、一行ずつ平易に説明する。

- 未解決か
- 再発しうるか
- 影響
- 優先順位
- 正式Issueへ昇格するか

### 3. 確認用の束

候補を、**Humanがまとめて読めるテーマの束**として提案する。

- 各候補IDをちょうど一回だけ含める。
- 束には、短いテーマ名、含めた理由、候補ID一覧、各候補の一〜二文の平易な説明を置く。
- 原文引用を言い換える場合、推測を事実のように書かない。原文確認が必要なら`原文確認が必要`と明記する。
- 束は「同じ処置をすべき」という結論ではない。Humanが比較して判断しやすくする並べ方である。
- `duplicate_suspect: false`は機械的な重複が無かった意味だけであり、意味的な重複なしを保証しないと明記する。

### 4. Humanの確認順の提案

確認順は提案として、次の三段階に分ける。

1. **先に一件ずつ確認するもの**：blocker、権限・安全・受入基準・外部副作用に触れそうな候補。
2. **束で比較してから確認するもの**：同種の手戻り・機械化候補、残余risk。
3. **後回しにできる可能性があるもの**：現状では影響が小さい可能性がある未実施・defer候補。

ただし、候補をこの順へ置く理由を明記し、priorityやdispositionを確定しない。

### 5. Human用の判断表（未記入）

41候補すべてについて、次の空欄を持つ表を作る。

| candidate ID | 平易な要約 | 未解決 | 再発性 | 影響 | priority | Issueへ昇格 | Humanメモ |

`未解決`以降の欄は、空欄または`Human記入`とする。Claudeが値を埋めない。

## 禁止事項

- 候補一覧、config、schema、validator、code、test、既存Issue、TODO、Plan、checklist、Decision recordを変更しない。
- triage decision、正式Issue、root cause candidate、Plan、Workを作らない。
- `human_fields`を埋めない。
- 実装、外部送信、push、PR、CI、Work 4B、Work 6A、E2以降を開始しない。

## 検証・コミット・完了報告

1. 資料中の候補ID集合が入力の41件と一致し、重複・欠落がないことを機械確認する。
2. 入力候補一覧のSHA-256を資料へ記す。
3. `git diff --check`を確認する。
4. 資料一件だけを一つのコミットにする。
5. 完了報告はコミットに混ぜず、次に保存する。

`records/session-handoffs/2026-08-05-claude-to-codex-historical-todo-triage-material.md`

報告には、commit SHA、束の数、候補41件の一致確認、未実施事項を記す。
