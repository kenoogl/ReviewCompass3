# レビュー依頼：守り役後追いレビュー対象一覧（deferred #6・第1単位）

- 作成日：2026-08-10
- Pilot：Claude／Reviewer：Codex／Closer：Codex
- collaboration mode：`role_neutral_pilot_review`、risk：`low`
- 範囲固定：`records/session-handoffs/2026-08-10-claude-pilot-guard-backfill-inventory-scope-v1.md`
  （SHA-256 `b81ecaacfbe866719e25cb35764cd4754092d72ad55af63c83b7c429b6567204`、SCOPE commit `b1f96dc`）
- Human承認（2026-08-10）：「#6 risk lowを確定、着手を承認する」

## 1. commit列

| SHA | 役割 | 内容 |
| --- | --- | --- |
| `b1f96dc` | Pilot | SCOPE（範囲固定のみ） |
| `4bed486` | Pilot | INVENTORY：一覧record 1件のみ |

本依頼書のcommit SHAは自己参照のため記載せず、Reviewerがgitから特定する。

## 2. Claim

- `tools/`配下の全133 module（`__init__.py` 3件を除く）を列挙し、
  work-review-protocol §3の定義に照らして守り役該当82・非該当51を判定、
  各行に1行理由を付した。
- レビュー状況を3区分で記録：①現基準済4件（Evidence 4件をpath＋SHA-256で参照）、
  ②旧体制で反証歴あり3件（同2件参照）、③後追い対象75件。
- ③に優先度提案（高19・中44・低12）と理由を付した。確定はHuman裁定。
- 境界事例5件は「要Human判定」と明示し、停止せず暫定判定で計上した（scope §9-3）。
- §7の集計値は表からの機械集計で照合済み（行数133＝列挙件数）。
- 成果はrecord 1件のみ。code・test・既存recordの変更なし、worktree clean。

## 3. 成果物SHA-256

| file | SHA-256 |
| --- | --- |
| `records/development/2026-08-10-guard-code-backfill-review-inventory-v1.md` | `1af9d804bfab59aaa90250b2c67df270e108bba7fe31832b584950a2221d91fa` |

## 4. Reviewerへの確認観点（`low`規定＝再実行照合、§11比例原則の範囲で）

- 網羅性：`find tools -name "*.py" -not -name "__init__.py" | sort` を再実行し、
  全moduleが§4の表に1回ずつ現れることを照合する。
- **過小分類の検査**：非該当51件のうち、§3定義（他の成果物の合否を決めるcode）に
  照らして守り役と判定すべきものが紛れていないか。疑義はfindingとして挙げる
  （境界事例は「要Human判定」への追加提案でよい）。
- 区分①②のEvidence参照（§3）のpath＋SHA-256の実在一致。
- 集計（§7）と表の一致。
