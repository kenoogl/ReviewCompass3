# Codex → Claude：Work 5A Provenance閉包修正の実装指示

## 承認と担当

- **Human**は2026-08-05に、`docs/design/2026-08-05-work5a-provenance-closure-repair-proposal.md`を承認し、
  §6.3の**案A**（既存`human_decision`をそのまま使用）を選んだ。
- **Claude**は、以下の固定範囲をTDDで実装する。
- **Codex**は、Claudeの完了報告を独立検証する。ClaudeはCodexの確認前に次作業へ進まない。

## 目的

`provenance_verdict`が自分自身を指す循環を廃止する。過去のHuman承認は維持し、
誤った`provenance_verdict`と`accepted_artifact`だけを無効化する。正しい新形式で来歴を検証し直し、
新しい受理recordを作る。

## 実施順序

各単位は独立にコミットする。完了済み単位を未コミットのまま次へ進まない。

### 1. 承認と無効化の記録

次のnew-only recordを作成する。

1. `records/development/2026-08-05-work5a-provenance-closure-repair-approval-decision-v1.md`
   - Humanの承認文言「案Aで承認」を引用する。
   - 承認範囲：循環除去設計、§6.3案A、後続の無効化・TDD・実装・正しい受理record再作成。
2. `records/development/2026-08-05-work5a-provenance-closure-invalidation-v1.json`
   - `9e8cf00`内の旧`provenance_verdict`（Digest `7975c7619dbca8c95fd249303dba47e46e0d8ec681e386866e1dddfbfa38aae0`）と
     旧`accepted_artifact`（Digest `6c4c690a39bbf0b1a845432e8dfe6c8f155598927e74e92d51a51eb28c7d9d4c`）だけを
     `invalidated_not_authoritative`とする。
   - 既存`human_decision`（Digest `a240921a70a40837efa2d45ee83def0059c125a2a343b7eb415841ddce65d8af`）と上流9 recordは無効化しない。
   - history rewrite、revert、既存recordの削除・上書きは行わない。

この二fileだけを第一コミットにする。

### 2. RED test

`tests/test_first_review_task_contract_e2e.py`へ、設計提案§5のP1〜P2、N1〜N11を実現するテストを追加する。

- 特に、今回の旧形式「`to: provenance_verdict`だが`to_digest`がHuman decision」を拒否する負例、
  自己参照を拒否する負例、`9e8cf00`の旧recordを実データfixtureとして拒否する負例、
  不正verdictからaccepted artifactを作れない負例を含める。
- 既存testを弱めない。実装はこの時点で変更しない。
- 追加testが、期待する失敗理由でREDになることを確認する。

RED testだけを第二コミットにする。

### 3. 実装とGREEN

`tools/task_contract/`を、設計提案§3・§4の新形式へ実装する。

- `provenance_verdict`は、Human decisionを終端とする9 node・8 edgeを検証する。
- `provenance_verdict`自身を端点とするedgeを保存しない。
- `verified_nodes`には各上流recordの`record_ref`相当のidentity・version・Digestを保存し、
  `verified_edges`は既存node role間だけを結ぶ。
- validatorはV1〜V10の全不一致をfail-closedで拒否する。辺数だけで`verified`にしてはならない。
- `accepted_artifact`は新形式の`verified` verdictと既存Human decisionを参照した場合だけ作る。
- 旧形式を互換入力として受理しない。旧形式はN11の拒否fixtureに限る。

新しいrecordはnew-onlyとする。旧recordと同じ`record_id`を使う場合は`record_version: 2`とし、
旧version 1を上書きしない。受理recordもversion 2とする。

追加test、既存Work 5Aの25件、全testを通し、GREENの実装と必要なGREEN Evidenceだけを第三コミットにする。

### 4. 正しい受理recordの再作成

既存の`human_decision` version 1をそのまま参照して、新形式の次をnew-onlyで作る。

- `provenance_verdict` version 2
- `accepted_artifact` version 2
- `records/development/2026-08-05-work5a-first-real-review-acceptance-v2-records.json`
- `records/development/2026-08-05-work5a-first-real-review-acceptance-v2-evidence.md`

上流record bundle、上流Evidence、target、既存Human decision、無効化record、設計承認Decisionへの参照とDigestを
明記する。受理Evidenceには、受理対象が最小Review経路の実行結果であり、対象文書の品質保証ではないことを
平易に記す。

`TODO_NEXT_SESSION.md`を、Work 5Aの最初のhappy pathが正しい`accepted_artifact`まで完了した状態へ更新する。
Current Planとchecklistは変更しない。

上記record、Evidence、TODOだけを第四コミットにする。

## 各段階の検証

- 全段階：`git diff --check`。
- record作成後：新規recordのDigest、上流参照、target Digest、versionの読み戻し照合。
- RED：追加testが新実装の前に期待理由で失敗すること。
- GREEN：対象test、既存Work 5Aの25件、公式venv runnerの全test。
- 最終：TODO構造検査、TODO参照Digest検査、worktree状態の確認。

## 禁止事項と停止条件

- 設計提案、review対象文書、Requirement、Current Plan、checklistを変更しない。
- `9e8cf00`をrevertしない。既存recordを削除・上書きしない。
- LLM、外部送信、外部`DATA_ROOT`、push、PR、CI、Work 4B、Work 6A、E2以降を開始しない。
- 設計と実装が矛盾する、既存Human decisionの参照が不可能、REDが期待理由で失敗しない、
  またはGREEN／全testが通らない場合は、局所patchを重ねず停止して報告する。
- 既存の未追跡`records/session-handoffs/2026-08-05-claude-to-codex-work5a-review-acceptance.md`は、
  誤った受理結果を報告するため変更・stage・commitしない。Codexが別途扱う。

## ClaudeからCodexへの完了報告

コミットに混ぜず、次へ新規保存する。

`records/session-handoffs/2026-08-05-claude-to-codex-work5a-provenance-closure-repair-implementation.md`

各コミットのSHA、無効化対象、新旧recordのID／version／Digest、RED結果、GREENと全test結果、
未変更範囲を記す。
