# 一件の要求候補整合検査 独立完了レビュー依頼record v1（Claude→Codex）

- 作成日：2026-08-16
- 依頼元：Claude（操縦・実装担当）
- 依頼先：Codex（レビュー専任。本製品の契約作成・実装を担当していない）
- 受け渡し方式：`docs/development/pilot-driven-record-handoff.md`のrecord正本方式。Claudeが`codex exec`で起動し、Humanは運搬しない
- レビュー種別：実装完了後の独立完了レビュー（契約v3受入条件21）
- 共通手順：`docs/development/work-review-protocol.md`

「独立完了レビュー」は、実装担当以外が固定commitの成果物を変更なしで検証し、誤合格・未接続・禁止作用・
上位目的への悪影響を反証する作業である。

## 1. 役割分担（本依頼の境界）

- **Codexが行うのは本record§4のレビューと、判定record 1件の作成・単独commitだけ**である。
- 判定後の後続——合格時の利用者への製品受入提示（受入条件23）、不合格時の最小修正——は**Claudeが実施**する。
- 利用者との会話接点はClaudeのみである。Codexは判定と根拠だけを判定recordへ書く。

## 2. 固定対象

- 実装commit（GREEN）：`db36e1de8de250a4cb2b3b0e313c336a0087562d`
- 失敗試験固定commit（RED）：`da8c700`（対象試験のみ、111件失敗を確認済み）
- 採用済み契約v3：`records/task-contract/2026-08-15-one-requirement-candidate-consistency-check-candidate-v3.md`
  - SHA-256：`7ad6da3c77632f3fc82bdbbabcb71d431d490bc78e12004d2331ef44cfdf0081`
- 利用者の採用判断：`records/development/2026-08-15-one-requirement-candidate-consistency-check-adoption-decision-v1.md`
  - SHA-256：`35eb9a0b34d6ecf3e7d503498ca0a0f04234fd4519c33eecee3b816cf8dd5c41`
- 実装成功Evidence：`records/development/2026-08-16-one-requirement-candidate-consistency-check-green-evidence-v1.md`
  - SHA-256：`50386e4a981e039e21af3bcec1fb3c37ba078739ff506b9afa19d63d806be6d2`
- 製品成果物：

| path | SHA-256 |
| --- | --- |
| `tools/requirements/one_requirement_feature_source.py` | `725c886a97bba63fc6d9d5c0d23a5fdc8e67f86eda2752ae587093c9bcdd14d7` |
| `tools/requirements/one_requirement_feature_source_entry.py` | `db702231fbf179a16c2742e1335d1c7f8198743baae2263ee2b1844e09ca7bd6` |
| `tests/test_one_requirement_feature_source.py` | `e746f55a7da7c67d8f208cc6a03b7ecaef52e12017c1eca09f0f5acadb17eab6` |
| `pyproject.toml` | `de5b60d6b37907e4976eeeae36b5b832e96c77a41b2ec59173420c3ec0a63f2b` |

## 3. 開始時の確認（Codexの鮮度検査）

1. 自分宛の最新依頼recordが本recordであることをGit履歴から機械特定する。
2. `git status --short`が空であることを確認する。
3. §2の対象fileの内容識別値を機械計算し、本record記載値と一致することを確認する。
4. 不一致・宛先違い・前提不一致の場合は、作業せずその旨を判定recordへ書いて停止する。
5. Python実行は常に`.venv/bin/python3`を使う。

## 4. レビューの内容（受入条件21）

固定commitの成果物を変更せず、次を検証する。高riskのため反証を新作してよい（一時領域のみ使用し、
repositoryへは判定record以外を残さない）。

1. **誤合格の反証**：対象試験が受入条件1〜17を実質的に覆い、合格が試験の穴によるものでないか。
   契約§8〜§11の固定（schema、機微検査順、正準JSON、内容識別値の計算対象、停止表）と実装・試験の一致を確認する。
2. **未接続の反証**：契約の受入条件で試験・Evidenceに接続されていないものがないか
   （18〜20はEvidence§4の各単独command、22はEvidence§5の合成E2E）。
3. **禁止作用の反証**：製品2 fileに通信、外部process、file書込み、Git、外部値の解決、入力外探索がないか。
   §6.2の再利用が`default_pattern_rules`と`find_high_entropy`だけか。
4. **上位目的への悪影響の反証**：G24保護10 path・G08固定3 file・要求schema・現行50要求に変更がないか。
   要求候補の自動昇格や権限変更が入っていないか。
5. **必須の機械確認**（各単独command・終了コード個別判定）：
   - `.venv/bin/python3 -m pytest -q tests/test_one_requirement_feature_source.py`（直近111件成功）
   - `.venv/bin/python3 -m pytest -q tests/test_requirements_feature_partition.py tests/test_requirements_fixed_inputs.py tests/test_requirement_boundary_relations.py tests/test_requirements_source_trace.py tests/test_requirements_batch.py`（直近59件成功）
   - `.venv/bin/python3 -m pytest -q tests/test_requirements_artifact_layout.py tests/test_requirements_unified_migration.py`（直近21件成功）
   - `.venv/bin/python3 -m pytest -q tests/test_one_design_acceptance.py`（直近107件成功）
   - `git diff --exit-code 0583863e4612f7f14b5db131beb627677b99017a -- tools/requirements/boundary_relations.py tools/requirements/feature_partition.py tools/requirements/fixed_inputs.py tools/requirements/requirement_batch.py tools/requirements/source_trace.py tests/test_requirements_feature_partition.py tests/test_requirements_fixed_inputs.py tests/test_requirement_boundary_relations.py tests/test_requirements_source_trace.py tests/test_requirements_batch.py`（差分0）
   - 隔離条件の正規全試験：`env -u ANTHROPIC_API_KEY -u ANTHROPIC_AUTH_TOKEN -u ANTHROPIC_BASE_URL -u ANTHROPIC_FOUNDRY_API_KEY -u ANTHROPIC_VERTEX_PROJECT_ID -u AWS_BEARER_TOKEN_BEDROCK .venv/bin/python3 -m pytest -q`（直近2,238件成功）

参考：通常host環境では既存`tests/test_claude_implementation_executor.py`の12件だけが不合格になる。実装前の
clean HEADで同一再現を確認済みの既知事象であり、本製品の退行ではない（Evidence§4）。

参考：Evidence§3に試験側の作成誤り2件の訂正理由が記録されている。訂正が契約の意図に合致するかもレビュー対象に含める。

## 5. 判定recordの作成と停止（Codexの成果物）

1. 判定recordを次のpathへ作成する。
   `records/development/2026-08-16-one-requirement-candidate-consistency-check-independent-completion-review-v1.md`
2. recordの冒頭に、Reviewerのmodel名とreasoning effort（起動時に表示された値）を記載する。
3. 判定は`verified`または`correction_required`とし、blocking／non-blocking Findingの件数と内容、
   根拠を書く。事実の主張には【実測】【記録】【推測】のラベルを付ける。
4. §4.5の各commandの結果（件数と終了コード）を記載する。
5. **そのrecord 1件だけをstageして単独commitし、停止する。** record以外のfileを変更しない。TODO更新、製品修正、
   利用者への提案、後続作業への着手を行わない。

## 6. Claudeの事後照合（参考）

Claudeは応答後に、(a) 判定recordのcommitが対象commit`db36e1de8de250a4cb2b3b0e313c336a0087562d`より後にあること、
(b) 変更pathが判定record 1件だけであること、(c) 判定内容、を機械照合してから後続へ進む。

## 7. 依頼完了条件

本recordと更新済み`TODO_NEXT_SESSION.md`を一つの意味単位commitへ固定し、`git status --short`が空であること、
TODO検査と`git diff --check`が終了コード0であることを確認する。
