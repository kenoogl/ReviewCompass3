# Codex → Claude：Work 5A Provenance閉包不整合の設計修正指示

## 誰が何をするか

- **Human**は、最初の実Review結果を承認した。
- **Codex**が独立照合で、受理recordのProvenance辺に設計上の不整合を発見した。
- **Claude**は、この不整合を根本から直すための設計提案だけを作成する。
- **Human**が設計を承認するまで、Claudeはrevert、実装、テスト変更、受理recordの再作成を行わない。

## 発見した事実

commit `9e8cf00` の次のrecordには、最後の辺がある。

```json
{
  "from": "human_decision",
  "to": "provenance_verdict",
  "to_digest": "a240921a..."
}
```

`a240921a...`は`human_decision`のDigestであり、`provenance_verdict`のDigest
`7975c761...`ではない。`to`と`to_digest`が指すrecordが一致しない。

原因は局所的な値の修正ではない。Provenance verdictが自分自身のDigestを内部の`to_digest`に入れると、
record内容が変化してDigestも変化するため、自己参照の循環になる。現行testは辺数と名称だけを確認し、
この不一致を検出していない。

従って、commit `9e8cf00`の`provenance_verdict: verified`と`accepted_artifact`は、現時点で正本として使わない。
Humanの承認判断そのものは有効であり、失われていない。

## Claudeが作るもの

次の新規設計提案を一件だけ作る。

`docs/design/2026-08-05-work5a-provenance-closure-repair-proposal.md`

状態は`awaiting_human_approval`とする。Decision recordは作らない。

提案は少なくとも次を固定する。

1. **循環を作らないrecord構造**
   - Provenance verdictは、検証対象となる上流record群（Human decisionを含む）を`record_ref`で参照する。
   - Provenance verdict自身へ向かうedgeを、そのrecord内容に含めない。
   - accepted artifactは、Provenance verdictとHuman decisionを参照する後続recordとする。
   - edgeに`to`と`to_digest`を併記するなら、両者は必ず同じ既存recordを指す。自己参照を許さない。
2. **検証規則**
   - 必須node、必須edge、record kind、record ID、Digestの不一致でfail-closedにする。
   - 辺の本数ではなく、各edgeの両端のidentityとDigestを照合する。
   - `verified`は全照合後だけに発行する。
3. **TDD受入条件**
   - 正常経路のほか、最終edgeの宛先DigestがHuman decisionのまま、edgeの名称だけ差替え、record kind差替え、
     record ID差替え、Digest差替え、自己参照の導入の各負例を拒否する。
   - 誤ったProvenance verdictからaccepted artifactを作れないことを確認する。
4. **既存の誤記録の扱い**
   - `9e8cf00`をhistory rewriteせず、どのようにrevertまたはinvalidatedとして扱うかを提案する。
   - 不正なrecordを上書きしない。Human承認を新しい正しいHuman decision recordへ再束縛する方法を示す。
5. **実施単位の分割**
   - 設計承認後の順序を、誤記録の無効化、RED test、実装、GREEN、正しい受理record再作成、独立検証の順に示す。
   - 各単位の停止条件と、Human承認が必要な箇所を明記する。

## 禁止事項

- `tools/task_contract/`、`tests/`、`TODO_NEXT_SESSION.md`、Current Plan、checklist、Requirementを変更しない。
- `9e8cf00`をrevertしない。recordを削除・上書きしない。
- LLM、外部送信、外部`DATA_ROOT`、push、PR、CI、Work 4B、Work 6A、E2以降を開始しない。

## 検証・コミット・完了報告

- 設計文書の内部参照と`git diff --check`を確認する。
- 設計文書一件だけを一つのコミットにする。
- 完了報告はコミットに混ぜず、次へ新規保存する。

`records/session-handoffs/2026-08-05-claude-to-codex-work5a-provenance-closure-repair-design.md`

報告には、commit SHA、提案した循環回避方式、誤記録の扱い案、未実施事項を記す。
