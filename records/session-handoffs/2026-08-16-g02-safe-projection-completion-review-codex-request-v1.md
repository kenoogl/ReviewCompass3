# 一件レビュー安全投影 独立完了レビュー依頼record v1（Claude→Codex）

- 作成日：2026-08-16
- 依頼元：Claude（操縦・実装担当）
- 依頼先：Codex（レビュー専任。本契約の作成・実装を担当していない）
- 受け渡し方式：`docs/development/pilot-driven-record-handoff.md`のrecord正本方式
- レビュー種別：実装完了後の独立完了レビュー（契約v2受入条件11）
- 共通手順：`docs/development/work-review-protocol.md`

## 1. 役割分担

- **Codexが行うのは§4のレビューと、判定record 1件の作成・単独commitだけ**である。
- 判定後の後続（合格時の受入提示、不合格時の最小修正）はClaudeが実施する。

## 2. 固定対象

- 実装commit（GREEN）：`9e7bd97fa7c8df1252ceb91eeebcbab9eb54dd6b`
- 失敗試験固定commit（RED）：`23be5e0`（prepare 8試験を追加、7件失敗を確認済み）
- 採用済み契約v2：`records/task-contract/2026-08-16-one-item-review-safe-projection-candidate-v2.md`
  - SHA-256：`9a35a25fc6481a62e8978574f8f1e73dc123eda2f96e9acb213851686d10f603`
- 採用判断：`records/development/2026-08-16-one-item-review-safe-projection-adoption-decision-v1.md`
  - SHA-256：`17b4f4f522810db3a851b1bc8dd1ab65bb90fb9ce5df2276ae60a42fcb19ec99`
- 実装成功Evidence：`records/development/2026-08-16-one-item-review-safe-projection-green-evidence-v1.md`
  - SHA-256：`6b9e6dbd7c43f1d34dc456f3fff6bc5e17c82103a8aa5db623f0b841be84fb63`
- 製品成果物（契約§8の変更上限どおり実行核と対象試験だけが変更されている）：

| path | SHA-256 |
| --- | --- |
| `tools/operations/operation_contract_run.py` | `7ce02906cf5be3c6976ed602488516bdd9c4331fbe6193d16a2eb60bcc170a08` |
| `tests/test_operation_contract_run.py` | `2d2bd889b24af8e1e57cba86a779b83121bc86e8045685bf5ba0205214ee73e6` |

## 3. 開始時の確認（Codexの鮮度検査）

1. 自分宛の最新依頼recordが本recordであることをGit履歴から機械特定する。
2. `git status --short`が空であることを確認する。
3. §2の対象fileの内容識別値を機械計算し、本record記載値と一致することを確認する。
4. 不一致の場合は、作業せずその旨を判定recordへ書いて停止する。
5. Python実行は常に`.venv/bin/python3`を使う。

## 4. レビューの内容（受入条件11）

固定commitの成果物を変更せず、次を検証する。反証の新作は一時領域のみ使用する。

1. **誤合格の反証**：対象試験75件が契約§9の受入条件を実質的に覆うか。特に：
   - 投影の自由文遮断：allowlist外の項目（`material.content`、`review_spec.goal`・`criteria`・`constraints`）が
     どの経路でも実行記録へ入らないこと（G02結果の項目追加・内容変異への耐性を含む）。
   - 変換の閉じた8理由：集合外理由（`stale_material`相当）が`internal_failure`になること、8理由の転記と
     部品コード（sensitiveのみ3）が一意なこと。
2. **未接続の反証**：契約§9の受入条件で試験・Evidenceに接続されていないものがないか。
3. **禁止作用の反証**：実行核の変更分に通信、外部process、時刻取得、乱数、入力外探索、G02の許可2関数以外の
   呼出しがないか。
4. **上位目的への悪影響の反証**：G02本体・入口・`pyproject.toml`・既存2操作・保護対象に変更がないか
   （保護基準commit `a052312`）。既存2操作の実行記録形式に退行がないか。
5. **必須の機械確認**（各単独command・終了コード個別判定）：
   - `.venv/bin/python3 -m pytest -q tests/test_operation_contract_run.py`（直近75件成功）
   - `.venv/bin/python3 -m pytest -q tests/test_one_item_review.py`（直近158件成功）
   - `.venv/bin/python3 -m pytest -q tests/test_one_design_acceptance.py`（直近107件成功）
   - `.venv/bin/python3 -m pytest -q tests/test_one_requirement_feature_source.py`（直近111件成功）
   - `.venv/bin/python3 -m pytest -q tests/test_first_review_task_contract_e2e.py`（直近38件成功）
   - 隔離条件の正規全試験（直近2,313件成功）：
     `env -u ANTHROPIC_API_KEY -u ANTHROPIC_AUTH_TOKEN -u ANTHROPIC_BASE_URL -u ANTHROPIC_FOUNDRY_API_KEY -u ANTHROPIC_VERTEX_PROJECT_ID -u AWS_BEARER_TOKEN_BEDROCK .venv/bin/python3 -m pytest -q`

参考：通常host環境では既存`tests/test_claude_implementation_executor.py`の12件だけが不合格になる既知事象がある。

## 5. 判定recordの作成と停止（Codexの成果物）

1. 判定recordを次のpathへ作成する。
   `records/development/2026-08-16-one-item-review-safe-projection-independent-completion-review-v1.md`
2. recordの冒頭に、Reviewerのmodel名とreasoning effort（起動時に表示された値）を記載する。
3. 判定は`verified`または`correction_required`とし、blocking／non-blockingの件数と根拠を書く。
   事実の主張には【実測】【記録】【推測】のラベルを付ける。
4. **そのrecord 1件だけをstageして単独commitし、停止する。** record以外のfileを変更しない。

## 6. Claudeの事後照合（参考）

Claudeは応答後に、(a) 判定recordのcommitが対象commit`9e7bd97fa7c8df1252ceb91eeebcbab9eb54dd6b`より後にあること、
(b) 変更pathが判定record 1件だけであること、(c) 判定内容、を機械照合してから後続へ進む。

## 7. 依頼完了条件

本recordを意味単位commitへ固定し、`git status --short`が空であること、`git diff --check`が終了コード0であることを
確認する。
