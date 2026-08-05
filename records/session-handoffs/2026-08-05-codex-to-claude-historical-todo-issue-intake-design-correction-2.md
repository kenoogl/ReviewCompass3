# Codex → Claude：Issue Intake V4 設計の最終整合訂正指示

## 誰が何をするか

- **Human**は、登録済みIssue数を無制限とし、作業中Issueを一件に限定し、阻害関係の循環を
  根本原因の判断へ渡す方針を承認した。
- **Codex**は、前回の設計訂正を確認し、実装時の保証範囲と循環検出の証跡に不足を見つけた。
- **Claude**は、承認待ちの設計提案一件だけを訂正して、これらの不足を解消する。

## 対象と変更禁止範囲

訂正対象は次だけである。

`docs/design/2026-08-05-historical-todo-issue-intake-proposal.md`

状態は`awaiting_human_approval`のままとする。config、schema、validator、code、test、既存Issue、
TODO、Plan、checklist、Decision record、候補recordを変更しない。

## 必ず直す点

### 1. 実施計画と受入条件の番号を一致させる

提案§5の受入条件は現在I1〜I9、J1〜J14である。しかし§6の単位2は旧番号の
`I1〜I6、J1〜J10`を参照している。単位2を**I1〜I9、J1〜J14の全件をREDで固定する**に訂正する。

これは単なる表記ではない。中断、二件目の作業開始拒否、自己循環、複数Issue循環、
Human裁定なしの根本原因Issue化、循環中Issueの無断再開拒否を、実装前のREDから検証することを
明示する。

### 2. 循環検出の証跡と原子性を定義する

現案は「循環する`blocks`関係を拒否する」と「関係するIssueをすべて`suspended`にする」を
併記している。循環する関係を保存しないなら、なぜどのIssueを止めたかを後から追えない。
次のように一貫した規則へ訂正する。

1. 新たな`blocks`関係は、まず**提案関係**として検査する。循環検出前に正本の`blocks`へ保存しない。
2. 自己循環または既存経路と合わせて循環になる場合、正本の`blocks`へは保存せず、
   `root_cause_escalation_candidate`を作成する。
3. このcandidateには、少なくとも次を必須にする。
   - `proposed_blocker_issue_id`と`proposed_blocked_issue_id`
   - 既存の経路を表す`cycle_path_issue_ids`と`cycle_path_relation_ids`
   - 循環に含まれる`affected_issue_ids`
   - 検出理由`blocks_cycle_detected`
   - 入力・candidate自身のcontent digest
4. candidateと、影響Issueを`suspended`へ移す状態変更は、同じ検証済み入力から**一単位で成功するか、
   どちらも書き込まない**。一方だけが残る中間状態を禁止する。
5. `root_cause_escalation_candidate`は問題の存在を保存するだけであり、Issue、Plan、Work、再開の
   権限にはならない。Humanの明示裁定だけが次へ進める。

平易な説明も残す。「循環する矢印を正本に残さず、循環を発見した事実と根拠だけを残す。これにより、
同じ往復を繰り返さず、誰が何を根本から見直すべきかを判断できる」とする。

### 3. 受入条件を補う

既存のJ10〜J13を上の規則に合わせる。少なくとも次を明記する。

- 循環する`blocks`関係は正本に保存されない。
- 循環candidateは、提案した辺、既存経路、影響Issue、理由、digestを欠くと拒否する。
- candidate作成と影響Issueの`suspended`化の一方だけが成功する状態を拒否する。
- candidateだけではIssue化、Plan化、Work開始、既存Issue再開ができない。

## 検証・コミット・完了報告

1. 設計文書の参照整合と`git diff --check`を確認する。
2. 設計提案一件だけを一つのコミットにする。
3. 完了報告はコミットに混ぜず、次へ新規保存する。

`records/session-handoffs/2026-08-05-claude-to-codex-historical-todo-issue-intake-design-correction-2.md`

報告には、commit SHA、修正した受入条件、循環candidateの必須証跡、未実施事項を記す。
