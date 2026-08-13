# 参照Digest正式Issueの解決状態反映・軽量作業票 v1

## 1. 目的と位置

- 対象：`ISSUE-AUTHORITY-REFERENCE-DIGEST-CHECK-001`
- 現在位置：立て直し計画第3段、G01現役接続の独立完了レビュー後。
- 目的：Humanが承認した意味的裁定を正規経路で記録し、実装・検証済みの実態と、正式Issueの
  `registered`状態を一致させる。
- この作業はG01のコード実装ではない。Issueの状態反映だけを一つの意味単位として扱う。

## 2. 固定材料

- 観測開始commit：`7246526`
- Issue：`.reviewcompass/workflow/issues-v4/issue-authority-reference-digest-check-001--v1.json`
  - 作業前SHA-256：`d260ed570598f56ada2cd6b4e54f15543bba0e792db65c14403a038f8100afbe`
  - 作業前state：`registered`
- 正規設定：`config/development-issue-resolution-pilot-v4.json`
  - SHA-256：`ed274e487318d44baed701ffbc8a1130df3e9d81cadca96515848a2bea228a8e`
- 実施Evidence：
  `records/development/2026-08-14-stage3-g01-authority-reference-guard-activation-evidence-v1.md`
  - SHA-256：`52022b04a72b1c5df458f949f80bde1383ef4238f8d6b6b024977eac6ad398cd`
- 独立完了レビュー：
  `records/development/2026-08-14-stage3-g01-authority-reference-guard-activation-independent-completion-review-v1.md`
  - SHA-256：`c441ef796f34959cadf5a111826af50fa02e46a3e367f896768a417940f78515`
  - 判定：`verified`、止める指摘0件、報告不一致0件
- Human判断：本作業開始直前の利用者発言「承認」。直前に明示した
  `ISSUE-AUTHORITY-REFERENCE-DIGEST-CHECK-001`の`resolved`反映を対象とする。

## 3. 三案比較

| 案 | 内容 | 単純さ | 処理時間 | メモリ使用量 | 頑健さ | 変更範囲 | 保守負担 | 戻しやすさ |
|---|---|---|---|---|---|---|---|---|
| A | `registered`のまま、Human判断記録だけを残す | 操作は最少 | 最小 | 最小 | 実態と台帳が不一致のままで不十分 | 判断記録1件 | 不一致の説明を将来も要する | 判断記録の取消しだけで容易 |
| B | 既存の正規`issue_resolution_v4`を使う | 既存機能だけで完結 | 小 | 小 | schema、Digest、参照、状態遷移を同時検証し、失敗時に巻き戻す | Human判断記録、Issue 1件、解決記録1件 | 新機構0、既存正規経路だけ | Gitで当該意味単位を回復可能 |
| C | Issueと解決記録を手編集する | 見かけ上は短い | 小 | 小 | 正規検証・巻戻しを迂回し、誤記の危険が高い | Bと同程度 | 手順の二重化を生む | Gitでは戻せるが誤状態を固定し得る |

案Bを採用する。理由は、新しいコード・設定・検査器を作らず、`.reviewcompass/workflow/`を正規toolだけで
変更する既存規則を守りながら、Human判断、Evidence、状態遷移、Digestを一つの検証済み記録へ結べるためである。
案Aは目的を満たさず、案Cは正規経路を迂回する。

## 4. 実施範囲

### 作成するfile

- Human判断記録：
  `records/development/2026-08-14-authority-reference-issue-resolution-ruling-v1.json`
- 正規toolが作る解決記録：
  `records/development/2026-08-14-authority-reference-issue-resolution-v1.json`
- 独立完了レビュー記録1件。

### 正規toolだけで更新するfile

- `.reviewcompass/workflow/issues-v4/issue-authority-reference-digest-check-001--v1.json`
  - `state`を`registered`から`resolved`へ変更する。
  - その変更に対応する`content_digest`だけを再計算する。
  - `issue_version`、problem、候補参照、仕分けDecision参照は変更しない。

### 完了後に通常更新するfile

- `TODO_NEXT_SESSION.md`

## 5. 実施順序

1. 本作業票について、固定材料、三案比較、正規経路、変更境界、停止条件の独立開始前レビューを行う。
2. Human判断記録を機械可読JSONで作成し、schemaと発言文脈を再読込確認して単独commitする。
3. Human判断記録のSHA-256を計算する。
4. `.venv/bin/python3 -m tools.development.issue_resolution_v4`を単独commandで実行する。
   - `--to resolved`
   - Human判断記録のpathとSHA-256
   - 上記の実施Evidenceと独立完了レビューを`--evidence path=sha256`で指定
   - 上記の解決記録pathを指定
5. 正規toolが作成・更新した2 fileだけを再読込し、関連validatorと対象試験を実行する。
6. 独立完了レビューで、Human判断との一致、変更key、Evidence参照、Digest、状態遷移、禁止範囲を照合する。
7. `verified`後にTODOを更新する。

## 6. 停止条件

次のいずれかが起きた場合、修正を連鎖させず停止してHumanへ返す。

- 正規toolが終了コード0以外を返す。
- 作業前IssueのSHA-256またはstateが固定材料と異なる。
- `state`と`content_digest`以外の既存Issue項目が変わる。
- 解決記録がHuman判断または固定Evidenceと一致しない。
- repository validatorまたは`tests/test_issue_resolution_v4.py`が不合格になる。
- コード、試験、設定、G01成果物、他Issueへの変更が必要になる。
- 先に存在する今回無関係の作業ツリー差分と競合する。

## 7. 完了条件

- Human判断記録が実発言の対象、判断者、判断時刻、`resolved`を機械可読に固定している。
- 正規toolの終了コードが0である。
- 対象Issueは`resolved`で、既存項目の差分は`state`と`content_digest`だけである。
- 解決記録が新規作成され、Human判断と2件のG01 EvidenceをDigest付きで参照する。
- repository全体のIssue整合検証と`tests/test_issue_resolution_v4.py`が成功する。
- 独立完了レビューが`verified`、止める指摘0件、報告不一致0件である。
- コード、試験、設定、他Issueは変更されていない。
- TODOが状態反映済みと次作業を示す。

## 8. 対象外

- コード・試験・設定の変更。
- Issue schema、正規tool、Human承認境界の変更。
- 他Issueの状態変更。
- G01再実装、第3段完了判断、第4段作業、外部送信。
- 作業開始時に存在した無関係な第4段計画差分とDecisionへの変更・stage・commit。
