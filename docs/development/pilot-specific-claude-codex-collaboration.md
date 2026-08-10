# 操縦者別のClaude／Codex連携方法

状態：運用メモ（試行）

決定日：2026-08-11

共通レビュー基準：`docs/development/work-review-protocol.md`

関連文書：

- `docs/development/pilot-driven-record-handoff.md`
- `docs/development/codex-claude-collaboration.md`
- `docs/development/role-neutral-pilot-review-collaboration.md`

## 1. 目的

ClaudeとCodexの分担を、操縦者に応じて二つの方式へ分ける。

ここでいう操縦者（`pilot`）とは、Humanから作業項目を受け取り、上流文書を確認し、作業範囲を固定し、
次の担当へ依頼し、停止地点を管理する担当をいう。

本書を適用する作業では、次の二つだけを認める。

1. `pilot: claude`：Claudeが依頼、実装、進行管理を行い、Codexがレビューする。
2. `pilot: codex`：Codexが依頼、進行管理、レビューを行い、Claudeは実装だけを行う。

`pilot: codex`でClaudeをレビュー担当にする方式は使わない。

作業開始時に`collaboration_method: pilot_specific_claude_codex`を固定した場合、本書を役割分担の
入口とする。同じ作業へ`role_neutral_pilot_review`を同時に適用しない。
`pilot-driven-record-handoff.md`は`pilot: claude`でCodexをレビュー担当として起動する方法に使い、
`codex-claude-collaboration.md`は`pilot: codex`でClaudeへ実装を依頼する方法に使う。

## 2. Humanの決定

Humanは2026-08-11、次の分担を決定した。

- ClaudeからCodexを起動し、Claudeが実装、Codexがレビューする方式は、`pilot: claude`の場合に限る。
- `pilot: codex`の場合は、以前の連携方式と同じく、Codexが実装依頼を作り、Claudeが実装だけを行い、
  Codexが実装結果をレビューする。

この決定は、既存の作業記録を遡って変更しない。本書を参照して開始する新しい作業から適用する。

## 3. 共通規則

### 3.1 内容の正本

担当間で受け渡す作業指示、実装結果、レビュー結果の正本は、Gitへコミットした記録だけとする。
チャットの文章、起動時の短い指示、担当者の終了報告は、通知または開始合図として扱う。

ただし、Humanによる作業項目の指定、危険度の確定、再開・段完了の承認、意味的な裁定は、Humanの
チャット文言を正とする。操縦者はその文言を範囲固定文書または依頼書へ転記し、対象と内容を固定する。

### 3.2 実装とレビューの分離

実装担当とレビュー担当は同じ担当にしない。

- 実装担当は、承認された範囲内でテストを先に作り、実装し、検証結果を記録する。
- レビュー担当は、実装を変更せず、上流文書、差分、テスト、記録、実行後の状態を独立に確認する。
- レビューで修正が必要になった場合は、操縦者が修正依頼を固定し、実装担当へ戻す。

### 3.3 Human境界

方針変更、外部送信、不可逆操作、意味的な裁定、危険度の確定、再開・段完了は、担当間の受け渡し方法に
かかわらずHumanの承認を必要とする。

## 4. `pilot: claude`の方式

### 4.1 分担

| 作業 | 担当 |
| --- | --- |
| Humanとの窓口 | Claude |
| 上流文書の確認 | Claude |
| 範囲固定と実装計画 | Claude |
| 実装依頼の管理 | Claude |
| テスト作成と実装 | Claude |
| 実装結果のレビュー | Codex |
| 修正依頼と再開管理 | Claude |
| 完了反映 | Humanが指定した担当 |

### 4.2 手順

1. ClaudeがHumanから作業項目を受け取り、範囲固定文書を作成して単独コミットする。
2. 必要なHuman承認を得た後、Claudeがテスト先行で実装する。
3. Claudeがレビュー依頼書を作成して単独コミットする。
4. Claudeが固定した短い起動文でCodex CLIを実行し、Codexをレビュー担当として起動する。
5. Codexは実装を変更せず、独立レビューを行い、結果記録だけを単独コミットして停止する。
6. Claudeは結果記録とGitの状態を照合し、修正または完了反映へ進む。

この方式では、Codexは実装を行わない。Claudeの実装中に同じファイルを変更しない。

Codex CLIが利用できない、認証が切れている、または異常応答となった場合は、自動的に別経路へ切り替えず、
ClaudeがHumanへ状況を報告して停止する。Human中継を使う場合も、受け渡す内容の正本はコミット済みの
記録とする。

## 5. `pilot: codex`の方式

### 5.1 分担

| 作業 | 担当 |
| --- | --- |
| Humanとの窓口 | Codex |
| 上流文書の確認 | Codex |
| 範囲固定と実装計画 | Codex |
| Claude向け実装依頼 | Codex |
| テスト作成と実装 | Claude |
| 実装結果のレビュー | Codex |
| 修正依頼と再開管理 | Codex |
| 完了反映 | CodexまたはHumanが指定した担当 |

### 5.2 手順

1. CodexがHumanから作業項目を受け取り、上流文書、受入条件、変更可能範囲、禁止事項、停止条件を確認する。
2. CodexがClaude向け実装依頼書を作成し、単独コミットする。
3. 必要なHuman承認を得た後、Claudeへ実装依頼書の場所だけを伝えて実装を開始させる。
4. Claudeは依頼書の範囲内でテストを先に作り、実装、検証、実装結果の記録を行い、指定された単位で
   コミットして停止する。
5. CodexはClaudeの終了報告を完了根拠にせず、コミット、差分、テスト、検証結果、停止境界を独立に確認する。
6. Codexがレビュー結果を記録する。修正が必要なら、修正範囲を新しい依頼書へ固定してClaudeへ戻す。
7. レビュー結果が`verified`（必要な証拠が揃い、実状態と一致する状態）になった後だけ、完了反映へ進む。

この方式では、Claudeは実装担当であり、依頼内容の決定、レビュー、Human判断の代行を行わない。
「実装」には、依頼書で指定されたテストの作成、実装コードの変更、決定的な検証、実装証拠の記録を含む。

CodexからClaudeを直接起動する承認済み経路が完成するまでは、
`docs/development/codex-claude-collaboration.md`のHuman中継を使う。承認済み経路の完成後は、運搬だけを
直接起動へ置き換え、Codexが依頼とレビューを行い、Claudeが実装だけを行う分担は変えない。

## 6. 危険度が高い作業

外部送信、承認関門、検証器、改竄拒否など、誤った合格が重大な影響を生む作業は危険度`high`とする。

- `pilot: claude`では、Claudeが作成した範囲と実装をCodexが独立にレビューする。
- `pilot: codex`では、Codexが範囲と依頼を作り、Humanが危険度と実装開始を承認する。Claudeが実装した後、
  Codexが実装前の予想やClaudeのテストだけに頼らず、上流文書から確認条件と反証を独立に導出してレビューする。

危険度`high`では、レビュー担当が実装担当のテストにない反証を最低1件作り、機械実行する。
外部送信そのものを重複実行して反証にしてはならない。

## 7. 禁止事項

- `pilot: claude`で、ClaudeがCodexへ実装を任せ、Claude自身がレビュー担当になること。
- `pilot: codex`で、Claudeをレビュー担当にすること。
- `pilot: codex`で、Claudeが依頼範囲、受入条件、Human承認の意味を独自に変更すること。
- レビュー担当がレビュー中に実装対象を修正すること。
- コミットされていないチャット報告だけで、実装完了またはレビュー合格と判断すること。
- 直接起動に失敗した際、承認のない別経路、別の認証、別の送信先へ自動的に切り替えること。

## 8. 作業開始時の固定項目

各作業は、開始時に最低限、次を記録する。

```text
collaboration_method: pilot_specific_claude_codex
pilot: claude | codex
implementer: claude
reviewer: codex
closer: codex | claude | humanが指定した担当
work_item: <一つの作業項目>
```

`pilot: claude`では`pilot`と`implementer`が同じになる。
`pilot: codex`では`pilot`と`reviewer`が同じになるが、実装担当はClaudeとして分離する。

本書が定めるのは担当と受け渡し方法である。レビュー手順、テスト先行、Git規律、証拠規則、Human承認境界は、
既存の共通文書を変更せず、そのまま適用する。
