# Claude → Codex：Issue Intake V4 設計の最終整合訂正 完了報告

指示：`records/session-handoffs/2026-08-05-codex-to-claude-historical-todo-issue-intake-design-correction-2.md`

## 1. commit SHA

`c0c07f0a7c85a28d879f39161cf6546d37de3a8e`（Align issue intake v4 acceptance and cycle evidence）

設計提案一件だけのcommitである。config、schema、validator、code、test、既存Issue、TODO、Plan、
checklist、Decision record、候補recordを変更していない。

| file | SHA-256 |
| --- | --- |
| `docs/design/2026-08-05-historical-todo-issue-intake-proposal.md` | `0fe666f78d7b08626144b163431f9bfe55f711acdb07e5facdbd56f2e3a2cb50` |

状態は`awaiting_human_approval`のままである。

## 2. 修正した受入条件

### 2.1 実施計画の番号整合

§6の単位2を、旧番号`I1〜I6、J1〜J10`から**`I1〜I9、J1〜J16`の全件**へ訂正した。
負例の追加により最終番号がJ16になったため、指示のJ14からさらに広がっている。

あわせて、単位2の下へ「実装前のREDから検証する対象」を明記した。
中断規則（J9）、二件目の作業開始拒否（J7）、自己循環（J10）、複数Issue循環（J11）、
循環candidateの証跡欠落（J12）、原子性違反（J13）、Human裁定なしの昇格（J14）、
循環中Issueの無断再開（J15）である。
これらを後回しにすると実装後に「動くから正しい」と誤認しやすい旨も記した。

### 2.2 J10〜J16の改訂

| # | 内容 |
| --- | --- |
| J10 | 自己循環を拒否し、提案関係を正本の`blocks`へ保存しない |
| J11 | 二Issue以上の循環を拒否。循環する関係を正本へ保存せず、影響Issueを`suspended`にして作業中0件。機械が相互に再開しない |
| J12 | candidateが必須証跡8 fieldのいずれかを欠くと拒否する |
| J13 | candidate作成と`suspended`化の一方だけが成功する状態を拒否し、`cycle_detection_partial_write`で停止していずれも書き込まない |
| J14 | candidateだけではIssue化、Plan化、Work開始、既存Issue再開ができない |
| J15 | 根本原因の`resolved`またはHuman裁定なしの再開を拒否する |
| J16 | TODOへ禁止markerを書き込もうとすると拒否する |

I1〜I9とJ1〜J16がいずれも連番で重複が無いことを機械照合した。

## 3. 循環candidateの必須証跡と原子性

### 3.1 検出と保存の順序

新しい`blocks`関係は、まず**提案関係**として検査する。**循環検出の前に正本へ保存しない。**
循環になる場合は正本へ保存せず、`root_cause_escalation_candidate`を作成し、
循環に含まれるIssueを`suspended`にして作業中Issueを0件にする。
循環にならない提案関係だけが正本の`blocks`へ保存される。

これにより「循環する関係を拒否する」と「関係するIssueを止める」の併記による矛盾を解消した。
拒否するのは**正本への保存**であり、**発見した事実と根拠は残す**。

### 3.2 必須証跡

| field | 内容 |
| --- | --- |
| `proposed_blocker_issue_id` | 提案した関係の阻害側 |
| `proposed_blocked_issue_id` | 提案した関係の被阻害側 |
| `cycle_path_issue_ids` | 循環を構成する既存経路のIssue ID列（順序どおり） |
| `cycle_path_relation_ids` | 同じ経路を構成する既存`blocks`関係のID列 |
| `affected_issue_ids` | `suspended`へ移したIssueのID列 |
| `detection_reason` | `blocks_cycle_detected`固定 |
| `input_digest` | 検査に使った入力（既存`blocks`集合と提案関係）のcontent digest |
| `content_digest` | candidate自身のcontent digest |

一つでも欠ければ拒否する（J12）。

### 3.3 原子性

candidateの作成と影響Issueの`suspended`化は、同じ検証済み入力から**一単位で成功するか、
どちらも書き込まない**。candidateだけが残ってIssueが`in_progress`のままの状態、
Issueだけが`suspended`で理由のcandidateが無い状態を、いずれも禁止する。
途中失敗の検出は`cycle_detection_partial_write`で停止する（J13）。

### 3.4 candidateの権限

`root_cause_escalation_candidate`は問題の存在を保存するだけであり、
Issueを作る、Planを作る、Workを開始する、`suspended`を再開する、のいずれの権限も持たない。
昇格、優先順位、統合、再開はHumanの明示裁定だけが決める（J14、J15）。

平易な説明も残した。「循環する矢印を正本に残さず、循環を発見した事実と根拠だけを残す。
これにより、同じ往復を繰り返さず、誰が何を根本から見直すべきかを判断できる」。

## 4. 未実施事項

- config、schema、validator、code、test、既存Issue、TODO、Plan、checklist、Decision record、
  候補record：**変更していない**。
- 過去TODOからの候補・Issueの新規作成：**行っていない**。
- 失敗中のtestの局所修正：**行っていない**。§0の失敗はV4導入で解消する順序のままである。
- LLM、外部送信、外部`DATA_ROOT`、push、PR、CI、Work 4B、Work 6A、後続評価E2以降：
  **開始していない**。

検証は、訂正14項目の反映確認（単位2の番号、旧番号の残存なし、REDで検証する項目の列挙、
提案関係の先行検査、必須証跡8件、`blocks_cycle_detected`、原子性、部分書込みの停止code、
candidateの無権限、平易な説明、I1〜I9とJ1〜J16の連番と重複なし）と`git diff --check`を実施し、
いずれも合格した。

Human承認まで実装へ進まない。
