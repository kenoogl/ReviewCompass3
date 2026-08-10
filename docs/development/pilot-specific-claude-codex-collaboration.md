# 操縦者別のClaude／Codex連携方法

状態：運用メモ（試行）

決定日：2026-08-11

## 1. 本書の位置づけ

本書は、ClaudeとCodexが共同で開発作業を行うときの役割分担と受け渡し方法の入口である。
作業開始時に`collaboration_method: pilot_specific_claude_codex`を選んだ場合、本書を最初に読む。

本書を適用する作業では、`role_neutral_pilot_review`を同時に適用しない。
既存の作業記録は遡って変更せず、その作業で固定済みの方式を使う。

関連する既存文書の位置づけは次のとおりである。

| 文書 | 位置づけ | 適用する場面 | 適用しない場面 |
| --- | --- | --- | --- |
| `docs/development/work-review-protocol.md` | 共通のレビュー基準 | Claudeが実装した結果をCodexが確認するとき | 担当者や起動方向の決定 |
| `docs/development/pilot-driven-record-handoff.md` | ClaudeからCodexを起動する方法の詳細 | `pilot: claude`でCodexをレビュー担当として起動するとき | `pilot: codex`からClaudeへ実装を依頼するとき |
| `docs/development/codex-claude-collaboration.md` | CodexからClaudeへ実装を依頼する方法と、人による中継方法の詳細 | `pilot: codex`でClaudeへ実装を依頼するとき | `pilot: claude`からCodexをレビュー担当として起動するとき |
| `docs/development/role-neutral-pilot-review-collaboration.md` | 先行試行の役割方式 | その文書を参照して開始済みの既存作業 | 本書を参照して開始する新しい作業 |

担当者を決める規則は本書を正とする。既存三文書は、本書で決めた担当を変更せず、該当する方向の
受け渡し方法または過去作業の解釈にだけ使う。

## 2. 用語と固定する役割

操縦者（`pilot`）とは、Humanから作業項目を受け取り、上流文書を確認し、範囲を固定し、次の担当へ依頼し、
停止地点を管理する担当をいう。

実装担当（`implementer`）とは、固定された依頼に従って、テスト作成、実装、機械検証、実装証拠の記録を
行う担当をいう。

レビュー担当（`reviewer`）とは、実装を変更せず、上流文書、差分、テスト、証拠、実行後の状態を独立に
確認する担当をいう。

本書では、操縦者がどちらの場合も、実装担当とレビュー担当を次のように固定する。

```text
implementer: claude
reviewer: codex
```

操縦者だけを、作業ごとにClaudeまたはCodexから選ぶ。

## 3. Humanの決定

Humanは2026-08-11、次の分担を決定した。

- `pilot: claude`では、Claudeが依頼、実装、進行管理を行い、Codexがレビューする。
- `pilot: codex`では、Codexが依頼、進行管理、レビューを行い、Claudeは実装だけを行う。
- ClaudeからCodexを起動する方式は、`pilot: claude`の場合に限る。
- `pilot: codex`でClaudeをレビュー担当にしない。

二つの方式で異なるのは、Humanとの窓口、範囲固定、実装依頼、修正管理を誰が行うかである。
実装担当がClaude、レビュー担当がCodexである点は共通とする。

## 4. 二つの方式の対応表

| 作業段階 | `pilot: claude` | `pilot: codex` |
| --- | --- | --- |
| Humanとの窓口 | Claude | Codex |
| 上流文書の確認 | Claude | Codex |
| 範囲固定 | Claude | Codex |
| 危険度の提案 | Claude | Codex |
| 危険度と再開の承認 | Human | Human |
| 実装依頼の作成 | Claude | Codex |
| テスト作成と実装 | Claude | Claude |
| 実装証拠の記録 | Claude | Claude |
| レビュー依頼の作成 | Claude | Codex |
| 実装結果のレビュー | Codex | Codex |
| 修正範囲の固定 | Claude | Codex |
| 修正実装 | Claude | Claude |
| 完了反映 | Humanが指定した担当 | CodexまたはHumanが指定した担当 |

`pilot: claude`では、Claudeが操縦者と実装担当を兼ねる。
`pilot: codex`では、Codexが操縦者とレビュー担当を兼ねるが、実装はClaudeへ分離する。

## 5. 共通の作業順序

二つの方式は、同じ順序で進める。担当だけを§4の対応表で切り替える。

| 順序 | 作業 | `pilot: claude`の担当 | `pilot: codex`の担当 |
| --- | --- | --- | --- |
| 1 | Humanから作業項目を受け取る | Claude | Codex |
| 2 | 上流文書、受入条件、変更範囲、禁止事項、停止条件を固定する | Claude | Codex |
| 3 | 必要なHuman承認を得る | Claudeが依頼する | Codexが依頼する |
| 4 | テストを先に作り、失敗を確認してから実装する | Claude | Claude |
| 5 | 実装結果と証拠をコミットして停止する | Claude | Claude |
| 6 | 実装を変更せず独立レビューする | Codex | Codex |
| 7 | 不合格なら修正範囲を固定して実装担当へ戻す | Claude | Codex |
| 8 | 合格後に完了反映する | Humanが指定した担当 | CodexまたはHumanが指定した担当 |

レビュー結果が`verified`（必要な証拠が揃い、実状態と一致する状態）になるまで、完了反映へ進まない。

## 6. 起動方向と受け渡し方法

役割分担と起動方法を混同しない。起動は作業を渡す手段であり、担当を決める根拠ではない。

| 操縦者 | 起動方向 | 起動される担当 | 目的 | 方法 |
| --- | --- | --- | --- | --- |
| Claude | ClaudeからCodex | レビュー担当のCodex | 実装結果の独立レビュー | `pilot-driven-record-handoff.md`の固定起動文とCodex CLI |
| Codex | CodexからClaude | 実装担当のClaude | 固定済み依頼の実装 | 承認済みのClaude起動経路。完成までは`codex-claude-collaboration.md`のHuman中継 |

直接起動が使えない、認証が切れている、または異常応答となった場合は、自動的に別の認証、別の送信先、
別の権限へ切り替えない。操縦者が事象と未実施範囲をHumanへ報告して停止する。

Human中継を使う場合、Humanはコミット済み記録の場所と開始・停止の合図だけを運ぶ。作業指示や判定内容を
チャットだけで作り直さない。

## 7. 内容の正本

担当間で受け渡す作業指示、実装結果、レビュー結果の正本は、Gitへコミットした記録だけとする。
チャットの文章、起動時の短い指示、担当者の終了報告は、通知または開始合図として扱う。

ただし、Humanによる作業項目の指定、危険度の確定、再開・段完了の承認、意味的な裁定は、Humanの
チャット文言を正とする。操縦者はその文言を範囲固定文書または依頼書へ転記し、対象と内容を固定する。

## 8. 危険度が高い作業

外部送信、承認関門、検証器、改竄拒否など、誤った合格が重大な影響を生む作業は危険度`high`とする。

| 確認事項 | `pilot: claude` | `pilot: codex` |
| --- | --- | --- |
| 範囲と危険度の提案 | Claude | Codex |
| 危険度と実装開始の確定 | Human | Human |
| 実装 | Claude | Claude |
| 完了レビュー | Codex | Codex |
| 独立した反証 | Codexが新作して機械実行 | Codexが新作して機械実行 |

CodexはClaudeのテストだけに頼らず、上流文書から確認条件と反証を独立に導出する。
危険度`high`では、Claudeのテストにない反証を最低1件作り、機械実行する。
外部送信そのものを重複実行して反証にしてはならない。

## 9. 禁止事項

- `pilot: claude`で、Codexを実装担当、Claudeをレビュー担当にすること。
- `pilot: codex`で、Claudeをレビュー担当にすること。
- Claudeが固定済みの依頼範囲、受入条件、Human承認の意味を独自に変更すること。
- Codexがレビュー中に実装対象を修正すること。
- コミットされていない終了報告だけで、実装完了またはレビュー合格と判断すること。
- 直接起動に失敗した際、承認のない別経路、別の認証、別の送信先へ切り替えること。
- 一つの作業に本書と`role_neutral_pilot_review`を同時適用すること。

## 10. 作業開始時の固定項目

各作業は、開始時に最低限、次を記録する。

```text
collaboration_method: pilot_specific_claude_codex
pilot: claude | codex
implementer: claude
reviewer: codex
closer: codex | claude | humanが指定した担当
work_item: <一つの作業項目>
```

本書が定めるのは担当と受け渡し方法である。レビュー手順、テスト先行、Git規律、証拠規則、Human承認境界は、
`docs/development/work-review-protocol.md`と開発方針をそのまま適用する。
