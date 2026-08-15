# 最小運用契約実行 独立完了レビュー依頼record v1（Claude→Codex）

- 作成日：2026-08-16
- 依頼元：Claude（操縦・実装担当）
- 依頼先：Codex（レビュー専任。本製品の契約作成・実装を担当していない）
- 受け渡し方式：`docs/development/pilot-driven-record-handoff.md`のrecord正本方式
- レビュー種別：実装完了後の独立完了レビュー（契約v4受入条件20）
- 共通手順：`docs/development/work-review-protocol.md`

## 1. 役割分担（本依頼の境界）

- **Codexが行うのは本record§4のレビューと、判定record 1件の作成・単独commitだけ**である。
- 判定後の後続——合格時の利用者への製品受入提示（受入条件22）、不合格時の最小修正——は**Claudeが実施**する。

## 2. 固定対象

- 実装commit（GREEN）：`b1ad31ad497d8b47877cbaccc1b2878d6e88b3df`
- 失敗試験固定commit（RED）：`fd24453`（58件失敗を確認済み。その後v4準拠の3試験を追加し61件）
- 採用中の契約v4：`records/task-contract/2026-08-16-minimal-operation-contract-execution-candidate-v4.md`
  - SHA-256：`d7b1861ccc73cb8f1c305294bf7c7e2a5fddd6ddb3fb46eab74e3204e8a2a7a1`
- 採用judgment（条件付き事前承認の成立）：`records/development/2026-08-16-minimal-operation-contract-execution-adoption-decision-v1.md`
  - SHA-256：`5f8c9fab3e3512376359f4b58ca528b87adcb74d0d488e1e86af1af06f2b6614`
- 実装成功Evidence：`records/development/2026-08-16-minimal-operation-contract-execution-green-evidence-v1.md`
  - SHA-256：`145f4938b7358acf301195901dfcacdf633b712927e60539c2db8e956c088336`
- 製品成果物：

| path | SHA-256 |
| --- | --- |
| `tools/operations/operation_contract_run.py` | `b09a41e1396263a6be48c5e062c18983f8d343034aa25946af8d387d0aa000f4` |
| `tools/operations/operation_contract_run_entry.py` | `a7521c5a2ed314c248b91738d390e1b4144287a1b840b51235971f2b2a6a0a21` |
| `tests/test_operation_contract_run.py` | `1b03ab702e9347b5dd31784f99cdf6001a3b3ef7d70c5326fe2f486584586c65` |
| `pyproject.toml` | `bea8151c9c055d9fe696672013b64e566579d9a7365f3c753b9eedae7885d5ef` |

## 3. 開始時の確認（Codexの鮮度検査）

1. 自分宛の最新依頼recordが本recordであることをGit履歴から機械特定する。
2. `git status --short`が空であることを確認する。
3. §2の対象fileの内容識別値を機械計算し、本record記載値と一致することを確認する。
4. 不一致・宛先違い・前提不一致の場合は、作業せずその旨を判定recordへ書いて停止する。
5. Python実行は常に`.venv/bin/python3`を使う。

## 4. レビューの内容（受入条件20）

固定commitの成果物を変更せず、次を検証する。高riskのため反証を新作してよい（一時領域のみ使用し、
repositoryへは判定record以外を残さない）。

1. **誤合格の反証**：対象試験61件が受入条件1〜17を実質的に覆い、合格が試験の穴によるものでないか。
   特に書込み境界（一時成果→照合→hard link原子公開→清掃、16b・16cの失敗注入反証）と、§8.2手順3・3bの
   除外の限定（束縛値のhex64・registry操作名の完全一致だけ）を確認する。
2. **未接続の反証**：契約の受入条件で試験・Evidenceに接続されていないものがないか（18・19はEvidence§3の
   各単独command、21はEvidence§4の合成E2E）。
3. **禁止作用の反証**：製品2 fileに通信、外部process、subprocess、Git、外部値の解決、時刻取得、乱数、
   入力外探索、既存fileの上書き・削除（自作一時成果の回収・清掃を除く）がないか。
4. **上位目的への悪影響の反証**：再利用4 file・保護10 path・既存G30基盤に変更がないか。実行記録・運用契約を
   正式要求・正式Workflow stateへ昇格していないか。部品の停止形式・安全表示を壊す埋め込みがないか。
5. **必須の機械確認**（各単独command・終了コード個別判定）：
   - `.venv/bin/python3 -m pytest -q tests/test_operation_contract_run.py`（直近61件成功）
   - `.venv/bin/python3 -m pytest -q tests/test_one_design_acceptance.py`（直近107件成功）
   - `.venv/bin/python3 -m pytest -q tests/test_one_requirement_feature_source.py`（直近111件成功）
   - `.venv/bin/python3 -m pytest -q tests/test_one_item_review.py`（直近158件成功）
   - `.venv/bin/python3 -m pytest -q tests/test_first_review_task_contract_e2e.py`（直近38件成功）
   - 隔離条件の正規全試験：`env -u ANTHROPIC_API_KEY -u ANTHROPIC_AUTH_TOKEN -u ANTHROPIC_BASE_URL -u ANTHROPIC_FOUNDRY_API_KEY -u ANTHROPIC_VERTEX_PROJECT_ID -u AWS_BEARER_TOKEN_BEDROCK .venv/bin/python3 -m pytest -q`（直近2,299件成功）

参考：通常host環境では既存`tests/test_claude_implementation_executor.py`の12件だけが不合格になる既知事象がある
（host認証環境差、G08受入時から変わらず）。

## 5. 判定recordの作成と停止（Codexの成果物）

1. 判定recordを次のpathへ作成する。
   `records/development/2026-08-16-minimal-operation-contract-execution-independent-completion-review-v1.md`
2. recordの冒頭に、Reviewerのmodel名とreasoning effort（起動時に表示された値）を記載する。
3. 判定は`verified`または`correction_required`とし、blocking／non-blocking Findingの件数と内容、根拠を書く。
   事実の主張には【実測】【記録】【推測】のラベルを付ける。
4. §4.5の各commandの結果（件数と終了コード）を記載する。
5. **そのrecord 1件だけをstageして単独commitし、停止する。** record以外のfileを変更しない。

## 6. Claudeの事後照合（参考）

Claudeは応答後に、(a) 判定recordのcommitが対象commit`b1ad31ad497d8b47877cbaccc1b2878d6e88b3df`より後にあること、
(b) 変更pathが判定record 1件だけであること、(c) 判定内容、を機械照合してから後続へ進む。

## 7. 依頼完了条件

本recordを意味単位commitへ固定し、`git status --short`が空であること、`git diff --check`が終了コード0であることを
確認する。
