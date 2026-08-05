# Codex → Claude：Issue Intake V4 設計訂正指示

## 誰が何をするか

- **Human**は、登録済みIssue数に上限を設けないことを決定した。
- **Human**は、同時に作業中のIssueを一件に絞る場合でも、新しい問題の発見で作業が
  行き詰まらず、依存関係の循環にも対応できることを求めた。
- **Codex**は、この決定を設計訂正として固定するよう指示する。
- **Claude**は、既存の設計提案だけを訂正する。実装・テスト・Issue生成は行わない。

## 対象と前提

訂正対象は次の承認待ち提案だけである。

`docs/design/2026-08-05-historical-todo-issue-intake-proposal.md`

既存の提案commit `472c7ad`、旧Pilotの記録、候補record、config、validator、test、Plan、TODOは
変更しない。訂正後の提案も状態は`awaiting_human_approval`のままとする。

## 必ず反映する設計訂正

### 1. 登録済みIssue数に上限を置かない

- `maximum_registered_issues`をV4設計から除く。
- 登録数を超えた場合の拒否規則・受入試験（現行J9）も除く。
- 登録しただけのIssue、候補、保留中Issueは、作業中Issue数に数えないことを明記する。
- TODOは引き続き、現在作業中のIssueの入口だけを表示し、登録済み全件の詳細を再累積しない。
  登録件数の表示も必須にしない。

### 2. 状態を分ける

少なくとも次を区別し、各状態が作業中上限に数えられるかを表で示す。

| 状態 | 意味 | 同時作業中上限への算入 |
| --- | --- | --- |
| registered / untriaged | 発見・保存されたが人の裁定前 | 算入しない |
| deferred | 人が後回しと決めた | 算入しない |
| in_progress | 現在、解決作業をしている | **算入する。常に最大1件** |
| suspended | 別の阻害問題のため中断した | 算入しない |
| resolved / rejected | 終了した | 算入しない |

既存のrecord語彙と異なる名称を採用する場合は、既存語彙との対応とschema版上げの必要性を
明示する。名称だけを既存recordへ遡及適用しない。

### 3. 新しい問題が見つかった場合の中断規則

- 新しい問題は、現在`in_progress`のIssueがあっても**登録できる**。
- 新しい問題が現行作業を止める阻害要因でない限り、現行Issueを中断しない。
- 阻害要因なら、現行Issueを`suspended`へ移し、新しいIssueを唯一の`in_progress`にできる。
- 新しいIssueの登録だけで、現行Issueを自動中断してはならない。
- 元のIssueの再開には、阻害Issueが`resolved`であること、またはHumanの明示的な再開裁定を
  必須にする。

### 4. 循環する阻害関係を禁止し、根本原因へエスカレーションする

`blocks`（「Aを進めるにはBの解決が必要」）を有向関係として定義する。

- 関係追加時に有向循環を機械検出する。自己循環も拒否する。
- `A → B → A`のような循環を検出した場合、機械は個別Issueを相互に再開して往復させない。
- 検出時は関係するIssueを`suspended`にし、作業中Issueを0件にする。
- 機械は`root_cause_escalation_candidate`を作成してよいが、根本原因Issueへの昇格、
  優先順位、既存Issueの統合・再開は**Humanだけが決める**。
- Humanが根本原因Issueを承認した場合だけ、それを唯一の`in_progress`にできる。
  根本原因Issueの解決またはHumanの裁定なしに、循環に含まれたIssueを再開できない。

「循環」は個別修正を増やす合図ではなく、依存関係・設計・方針を根本から見直す必要がある
信号であることを平易に説明する。

### 5. 受入条件と実施計画

既存のI1〜I6、J1〜J10を上の変更に合わせて改訂する。少なくとも次の正例・負例を追加する。

- 登録済み・保留中Issueが複数でも、`in_progress`が一件なら有効。
- 非阻害の新規Issue登録では、作業中Issueが中断されない。
- 阻害Issueへの切替では、旧Issueが`suspended`、新Issueだけが`in_progress`となる。
- 二件目の`in_progress`開始は拒否する。
- 自己循環および二Issue以上の`blocks`循環は拒否し、作業中Issueを残さない。
- Human裁定なしにroot cause candidateをIssue化、または循環中Issueを再開しようとすると拒否する。

実施計画は、設計承認後にRED→実装→GREEN→過去TODO候補の提示→Human triageとなる順序を
保つ。今回の訂正は設計だけであり、失敗中のtestを局所的に直す作業を始めない。

## 禁止事項

- config、schema、validator、code、test、既存Issue、TODO、Plan、checklist、Decision recordを変更しない。
- 過去TODOから候補やIssueを新規作成しない。
- LLM、外部送信、外部`DATA_ROOT`、push、PR、CI、Work 4B、Work 6A、E2以降を開始しない。

## 検証・コミット・完了報告

1. 対象設計文書の参照整合と`git diff --check`を確認する。
2. 設計提案一件だけを一つのコミットにする。
3. 完了報告はコミットに混ぜず、次の新規ファイルに保存する。

`records/session-handoffs/2026-08-05-claude-to-codex-historical-todo-issue-intake-design-correction.md`

報告には、commit SHA、変更した状態遷移、循環検出時の停止・Human判断境界、未実施事項を記す。
