# 最小運用契約実行 独立完了再レビュー依頼record v1（Claude→Codex）

- 作成日：2026-08-16
- 依頼元：Claude（操縦・訂正担当）
- 依頼先：Codex（レビュー専任）
- 受け渡し方式：`docs/development/pilot-driven-record-handoff.md`のrecord正本方式
- レビュー種別：blocking 3件の訂正確認と退行確認の独立完了再レビュー
- 共通手順：`docs/development/work-review-protocol.md`

## 1. 役割分担

- **Codexが行うのは§4の再レビューと、判定record 1件の作成・単独commitだけ**である。
- 判定後の後続はClaudeが実施する。

## 2. 対象と前提

- 訂正commit：`13e8b3d33e53e2aacde38ed2b4b473894f800cb0`
- 先行完了レビュー（判定`correction_required`、blocking 3件）：
  `records/development/2026-08-16-minimal-operation-contract-execution-independent-completion-review-v1.md`
  - SHA-256：`38460b84e469cc81950633b3026cb195d6c308e4aaa171a22d10458cd0e13281`
- 訂正Evidence：`records/development/2026-08-16-minimal-operation-contract-execution-correction-evidence-v1.md`
  - SHA-256：`c2a386c87e542a7f626e77b931bb24672fd6bf392fda71e216a5c19923959c30`
- 訂正後の製品成果物：

| path | SHA-256 |
| --- | --- |
| `tools/operations/operation_contract_run.py` | `a0fdc2eacaa6ce6d5baafc54daa133f215dc3b0285772af7f16f7d0f94b8c689` |
| `tools/operations/operation_contract_run_entry.py` | `06c01aefbff568f80ff0919af398dfff2fabc405927419fe0acd5e52a1a88abb` |
| `tests/test_operation_contract_run.py` | `1d96fb6ff03326a2febfb47963ab1c2560fc35f6cac7f08c1d340dd9921005b5` |

- 訂正は3点だけである：B-01（同一性比較へ`st_mtime_ns`・`st_ctime_ns`を追加）、B-02（入口と実行核の
  path検査でNUL・単独サロゲートを読取り前に`invalid_path / arguments`拒否）、B-03（bearer token・
  API key代入・秘密鍵blockの停止試験3件を追加、対象試験67件）。契約v4本文と他成果物の変更はない。

## 3. 開始時の確認（Codexの鮮度検査）

1. 自分宛の最新依頼recordが本recordであることをGit履歴から機械特定する。
2. `git status --short`が空であることを確認する。
3. §2の対象fileの内容識別値を機械計算し、本record記載値と一致することを確認する。
4. 不一致の場合は、作業せずその旨を判定recordへ書いて停止する。
5. Python実行は常に`.venv/bin/python3`を使う。

## 4. 再レビューの内容

訂正commitの成果物を変更せず、次を確認する。反証の新作は一時領域のみ使用する。

1. **B-01の閉鎖**：先行レビューと同じ「初回読取り後の同一inode・同一size書換え」反証が
   `unreadable_input / contract`・終了コード2で停止するか。
2. **B-02の閉鎖**：NUL・単独サロゲートを含む`--contract`値が読取り前に`invalid_path / arguments`・
   終了コード2の固定停止形で止まるか。
3. **B-03の閉鎖**：機微patternからbearer token・API key代入・秘密鍵blockの3規則を外す変異の下で
   対象試験が失敗する（変異を検出する）か。無変異では対象67件が成功するか。
4. **退行の有無**：訂正3点以外の差分がないこと。次の各単独command（終了コード個別判定）：
   - `.venv/bin/python3 -m pytest -q tests/test_operation_contract_run.py`（直近67件成功）
   - `.venv/bin/python3 -m pytest -q tests/test_one_design_acceptance.py`（直近107件）
   - `.venv/bin/python3 -m pytest -q tests/test_one_requirement_feature_source.py`（直近111件）
   - `.venv/bin/python3 -m pytest -q tests/test_one_item_review.py`（直近158件）
   - `.venv/bin/python3 -m pytest -q tests/test_first_review_task_contract_e2e.py`（直近38件）
   - 隔離条件の正規全試験（直近2,305件成功）：
     `env -u ANTHROPIC_API_KEY -u ANTHROPIC_AUTH_TOKEN -u ANTHROPIC_BASE_URL -u ANTHROPIC_FOUNDRY_API_KEY -u ANTHROPIC_VERTEX_PROJECT_ID -u AWS_BEARER_TOKEN_BEDROCK .venv/bin/python3 -m pytest -q`

## 5. 判定recordの作成と停止（Codexの成果物）

1. 判定recordを次のpathへ作成する。
   `records/development/2026-08-16-minimal-operation-contract-execution-independent-completion-rereview-v1.md`
2. recordの冒頭に、Reviewerのmodel名とreasoning effort（起動時に表示された値）を記載する。
3. 判定は`verified`または`correction_required`とし、blocking／non-blockingの件数と根拠を書く。
   事実の主張には【実測】【記録】【推測】のラベルを付ける。
4. **そのrecord 1件だけをstageして単独commitし、停止する。** record以外のfileを変更しない。

## 6. Claudeの事後照合（参考）

Claudeは応答後に、(a) 判定recordのcommitが対象commit`13e8b3d33e53e2aacde38ed2b4b473894f800cb0`より後にあること、
(b) 変更pathが判定record 1件だけであること、(c) 判定内容、を機械照合してから後続へ進む。

## 7. 依頼完了条件

本recordを意味単位commitへ固定し、`git status --short`が空であること、`git diff --check`が終了コード0であることを
確認する。
