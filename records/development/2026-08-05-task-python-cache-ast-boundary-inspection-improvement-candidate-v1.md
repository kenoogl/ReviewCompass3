---
candidate_id: IC-TASK-PYTHON-CACHE-AST-BOUNDARY-001
observed_at: 2026-08-05
origin_stage: initial-development
origin_work: task専用Python cache root最小slice
origin_commit: c9587dbf6135524f4abdee4cd8e02cf16319088d
candidate_kind: improvement_candidate
classification: Test／oracle不良
priority: P1
status: adopted_for_next_slice
suggested_route: existing_issue_repair
related_issue: ISSUE-HTC-C9F6C917
confidentiality_class: project-internal
---

# 禁止操作の検査が文字列一致だったために誤検知した

## 1. 発生元

| identity | value |
| --- | --- |
| 作業 | task専用Python cache root最小slice |
| commit | `c9587dbf6135524f4abdee4cd8e02cf16319088d` |
| 既存Evidence | `records/development/2026-08-05-machine-operation-routing-task-python-cache-green-evidence-v1.md` |
| 該当節 | 同Evidenceの「3. RED Testに1点だけ訂正を入れた」 |
| 対象Test | `tests/test_task_python_cache.py::test_module_has_no_deletion_or_retention_or_global_environment_change` |
| 対象module | `tools/development/task_python_cache.py` |

## 2. 事象

`tools/development/task_python_cache.py`が禁止操作を含まないことを確かめる受入検査は、
禁止語の一覧をsource文字列に対して部分一致で探していた。

禁止語に`environ`を入れたため、指示が求める正しい公開関数名`bytecode_environment`の中の
`environ`まで違反として拾った。実装が何をしていても必ず失敗する検査になっていた。

その場では禁止語を`os.environ`へ狭めてGREENにした。振る舞いは正しくなったが、
**同じ方式のまま**であり、再発防止になっていない。

## 3. 原因

操作の**意味**ではなく、文字の**出現**だけを検査したことである。

Pythonのsourceでは、同じ文字列が識別子の一部にも、docstringにも、実際の操作にも現れる。
文字列一致はこれらを区別できない。逆に、aliasを使った`import os as runtime_os`のような
書き方は、禁止語の文字列が現れないため見逃す。誤検知と見逃しの両方を持つ検査である。

## 4. 影響

- 今回の実装`tools/development/task_python_cache.py`の振る舞いは壊していない。
  cacheの配置、初期化範囲、環境mapping、安全境界はすべて別のTestで固定されており、
  公式全Testは`942 passed`である。
- 影響は検査側にある。同じ方式を他の境界検査へ複製すると、正しい命名が違反として弾かれ、
  Testを緩める方向の手戻りが繰り返し起きる。alias経由の本物の違反も見逃す。

## 5. route

既存Issue`ISSUE-HTC-C9F6C917`（LLMが機械操作の実行手順を都度組み立てている根本原因）へ紐付ける。
新しい正式Issue、Plan、Task Contract、policyは作らない。

この作業単位で、禁止語の文字列検索をPythonのAST（抽象構文木。sourceを構文として解析した木）に
よる操作検査へ置き換えて修復する。

## 6. この候補が許可しないこと

この候補は検査方式の修復だけを対象とする。次は**許可しない**。

- 実際の`~/.reviewcompass3`での初期化、`ReviewCompass3-data`、既存`DATA_ROOT`、
  `SENSITIVE_ROOT`への書込み。
- cacheの配置・所有・保持規則の変更、Layout v3の変更。
- cache初期化、掃除、保持期限の自動化、既存runner／executorへの接続、
  環境変数のglobal（process全体）変更、Windows adapter、既存操作の移行、外部送信。
- 既存Decision、Issue state、Task Contract、policy、configの変更。
