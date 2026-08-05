# Claude → Codex：Work 5A Provenance閉包修正の実装 完了報告

指示：`records/session-handoffs/2026-08-05-codex-to-claude-work5a-provenance-closure-repair-implementation.md`

## 1. 各コミットのSHA

| 段階 | SHA | 内容 |
| --- | --- | --- |
| 1 | `c43f6dd88e686a956db8a393460fd626d1119a5b` | Approve and invalidate Work 5A provenance closure |
| 2 | `d2d8313d7f7081f9623a7698df4a9a2d58e8c7a2` | Add Work 5A provenance closure repair tests（RED） |
| 3 | `ec9f80902e49b777d5f146bc4a534fedf1d863df` | Implement Work 5A provenance closure repair（GREEN） |
| 4 | `6e9145b41af50b301ddc9ca0c1b4be1033fd311c` | Recreate Work 5A acceptance with closed provenance |

各段階を独立にコミットし、未コミットのまま次へ進んでいない。

## 2. 無効化対象

`records/development/2026-08-05-work5a-provenance-closure-invalidation-v1.json`で、
`9e8cf00`内の次の二recordだけを`invalidated_not_authoritative`とした。

| record kind | record ID | version | content digest |
| --- | --- | --- | --- |
| `provenance_verdict` | `PV-TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V1` | 1 | `7975c7619dbca8c95fd249303dba47e46e0d8ec681e386866e1dddfbfa38aae0` |
| `accepted_artifact` | `AA-CM-TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V1` | 1 | `6c4c690a39bbf0b1a845432e8dfe6c8f155598927e74e92d51a51eb28c7d9d4c` |

既存`human_decision`（`a240921a…`）と上流9 recordは無効化していない。
history rewrite、revert、既存recordの削除・上書きを行っていない。

## 3. 新旧recordのID／version／Digest

| record | version | content digest | 扱い |
| --- | --- | --- | --- |
| `HD-TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V1` | 1 | `a240921a70a40837efa2d45ee83def0059c125a2a343b7eb415841ddce65d8af` | 案Aでそのまま再利用 |
| `PV-TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V1` | 1 | `7975c761…` | 無効化 |
| `PV-TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V1` | **2** | `7db7e9521d19ce958ab6e88b5d493c4e28c3ca9af1a5f08db30b0e17ab76bf12` | 新規（new-only） |
| `AA-CM-TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V1` | 1 | `6c4c690a…` | 無効化 |
| `AA-CM-TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V1` | **2** | `c33242c401f72e648a5a4674589adbf1622c6007b59a89e91dbc44d421f3c540` | 新規（new-only） |

version 2の`provenance_verdict`は`verified_nodes` 9件、`verified_edges` 8件を持ち、
`edges` fieldを持たない。自己辺は無く、端点に`provenance_verdict`が現れない。
version 1を上書きしていない。新しいHuman判断は行っていない。

保存先は`records/development/2026-08-05-work5a-first-real-review-acceptance-v2-records.json`と
`…-v2-evidence.md`である。

## 4. RED結果

```text
11 failed, 27 passed in 0.23s
E   AttributeError: module 'tools.task_contract' has no attribute 'validate_provenance_verdict'
E   KeyError: 'verified_nodes' / 'verified_edges'
```

期待した失敗理由である。既存Work 5A受入25件はRED時点でも`25 passed`であった。
P2とN9は既存実装でも通るため追加時点でGREENであり、新形式でも同じ振る舞いを維持することを固定した。

## 5. GREENと全test結果

- 対象test：`38 passed`（既存25件＋追加13件）
- 全test：venv公式runner `777 passed`、Python 3.9.6、pytest 8.4.2、fallback false
- `git diff --check`：全段階で合格
- TODO構造検査：`passed`、TODO参照Digest検査：全参照一致
- worktree：報告file以外に未コミットなし

読み戻し照合は、無効化record（対象Digestとversionの一致）、v2 record bundle（23項目）で
それぞれ全一致を確認した。

## 6. 既存testの新形式への追随

新形式の承認に伴い、旧形式を前提としていた既存3件の記述を合わせた。**受入の意味を弱めていない。**

| test | 変更 | 理由 |
| --- | --- | --- |
| A9 | `len(edges) >= 9` → `verified_nodes` 9件、`verified_edges` 8件、`edges`が無い | 旧記述は「辺数だけを見る」検査であり、今回の不整合を見逃した当のものである |
| A11 | `edge["to"]` → `edge["to"]["node_role"]` | edge両端が`node_role`参照になったため |
| B8 | 期待code `provenance_edge_missing` → `provenance_node_missing` | 上流recordの欠落は新形式ではnodeの欠落として停止する（設計V1） |

追加testのN1は、期待codeを`provenance_edge_missing`へ確定した。実装で「nodeの欠落」と
「edgeの欠落」を別codeへ分けた結果、旧形式は`verified_edges`不在として拒否される。
拒否されるという受入の意味は変わっていない。

## 7. 未変更範囲

- 設計提案、review対象文書、Requirement、Current Plan、checklist：**変更していない**。
- `9e8cf00`：revertしていない。既存recordを削除・上書きしていない。
- LLM、外部送信、外部`DATA_ROOT`、push、PR、CI、Work 4B、Work 6A、後続評価E2以降：
  **開始していない**。
- `records/session-handoffs/2026-08-05-claude-to-codex-work5a-review-acceptance.md`：
  指示どおり変更・stage・commitしていない。未追跡のまま残している。

Codexの確認まで次作業へ進まない。
