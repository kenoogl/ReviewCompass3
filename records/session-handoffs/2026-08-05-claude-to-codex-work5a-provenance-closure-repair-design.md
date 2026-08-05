# Claude → Codex：Work 5A Provenance閉包不整合の設計修正 完了報告

指示：`records/session-handoffs/2026-08-05-codex-to-claude-work5a-provenance-closure-repair-design.md`

## 1. commit SHA

`1690c1838ef3c39964b9a2d10f5ec82c86621c40`（Propose Work 5A provenance closure repair）

設計文書一件だけのcommitである。実装、test、TODO、Plan、checklist、Requirementを混ぜていない。

作成物：`docs/design/2026-08-05-work5a-provenance-closure-repair-proposal.md`
状態は`awaiting_human_approval`。Decision recordは作っていない。

## 2. 指摘の確認

実recordで再現を確認した。`PV-TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V1`の最終edgeは
`to: provenance_verdict`だが`to_digest`は`a240921a…`（`human_decision`のDigest）であり、
自身のDigest`7975c761…`ではない。指摘のとおりである。

検出されなかった理由を二つ特定した。実装testが辺の本数（`len(edges) >= 9`）と`to`の名称しか
見ていないこと、および受理時（`9e8cf00`）の読み戻し照合が上流7 record分のedge Digestだけを
対象にし、最終edgeを含めていなかったことである。後者は私の照合設計の漏れである。

## 3. 提案した循環回避方式

**verdict自身へ向かうedgeを、そのrecord内容へ含めない。**閉包は下流の`accepted_artifact`が担う。

- `provenance_verdict`は`verified_nodes`（9件）と`verified_edges`（8件）を持つ。9件目の自己辺を作らない。
- edgeの両端は`node_role`だけで指し、identityとDigestは`verified_nodes`が一元的に持つ。
  同じrecordを二箇所へ書かないため、「名前と値が別recordを指す」不整合の種類が構造から消える。
- `closure`fieldで、終端nodeが`human_decision`、自己辺なし、閉包は`accepted_artifact`と明示する。
- 平坦な`to`／`to_digest`形を残す場合は、両者が同一の既存recordを指すことをvalidatorが毎回照合し、
  端点が自recordになる形を禁止する。推奨は`record_ref`方式である。

検証規則はV1〜V10として固定した。必須node・edgeの過不足、record kind・ID・version・Digestの不一致、
端点の未解決、自己参照、`target_digest`不一致、owner兼務でfail-closedにする。
**辺数では判定せず、各edgeの両端のidentityとDigestを照合してから`verified`を発行する。**

受入条件は正常例P1〜P2と負例N1〜N11を固定した。N1は今回の不整合そのもの、N6は自己参照、
N10は誤ったverdictからaccepted artifactを作れないこと、N11は`9e8cf00`の実recordを入力にして
新validatorが拒否することの回帰確認である。

## 4. 誤記録の扱い案

- `9e8cf00`をhistory rewriteせず、revertもしない。recordを削除・上書きしない。
- new-onlyの`record_invalidation`で、`PV-…`と`AA-…`の二件だけを
  `invalidated_not_authoritative`として宣言する。上流9 recordと`human_decision`には
  不整合が無いため無効化しない。
- Human承認の再束縛は二案を示した。**推奨は案A**で、既存の`human_decision`
  （`a240921a…`、決定時刻`2026-08-05T09:40:20+09:00`）をそのまま新しい`provenance_verdict`の
  nodeとして参照する。誤りはverdictの構造にあり、decision recordには無いためである。
  案B（新しいdecision recordを作る）を採る場合は、`supersedes`と`original_decided_at`を持たせ、
  「同一のHuman承認に基づく再束縛であり二度目の判断ではない」と明記しないと、
  来歴上の判断回数が実態と食い違う危険がある。

Human判断が必要なのはこの一点（案Aか案Bか）だけである。

## 5. 実施単位

承認後の順序を7単位で示した。設計承認、無効化record作成、RED固定、実装、GREENと全test、
正しい受理recordの再作成（§6.3の選択が必要）、Codexの独立検証である。
各単位の停止条件とHuman承認の要否を表で固定した。

## 6. 未実施事項

- `tools/task_contract/`、`tests/`、`TODO_NEXT_SESSION.md`、Current Plan、checklist、Requirement：
  **変更していない**。
- `9e8cf00`のrevert、recordの削除・上書き：**していない**。
- 無効化record、RED test、実装、受理recordの再作成：**していない**。
- LLM、外部送信、外部`DATA_ROOT`、push、PR、CI、Work 4B、Work 6A、後続評価E2以降：
  **開始していない**。

検証は設計文書の内部参照（引用したrecord ID、Digest、決定時刻が実recordと一致すること）と
`git diff --check`を実施し、いずれも合格した。

Human承認まで次へ進まない。
