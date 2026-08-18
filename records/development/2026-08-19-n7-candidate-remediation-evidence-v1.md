# N7未充足候補4件の是正 実行Evidence v1

- 記録日：2026-08-19。指示者：利用者（Human）「N7未充足4件の是正を1作業単位で実施。作業票と
  事前走査から入って」（chat）
- 範囲固定：作業票`docs/development/2026-08-19-n7-candidate-remediation-work-ticket-v1.md`／
  事前走査同prescan v1。基準`8d9bb2c`→文書・計画（writer）`06de937`→証明書`a70cc9f`→
  実装は本record同一commit

## 1. 成果物

候補4件（contract-014正準列・launch-metrics表題・終了コード語彙2件）を規定形へ**機械再生成**
（意味内容保存）：(a) `related_candidates`と`source_identity.section`の値を`problem`末尾へ文と
して移記し欄を除去、(b) 無効分類を対応表で置換（`documentation`→`process_improvement`・
`design`→`implementation`。有効値保持）、(c) 追加の是正1点＝`source_version`の値規則
（検証器は1固定）への適合（旧値2は`problem`へ移記。§2の手戻り）、(d) `content_digest`正準
再計算。**実anchor（出所recordのpath＋SHA-256）は全件不変**。他欄・`created_at`不変。

## 2. 手戻りの記録（正直な記載）

事前走査の形状探針は**欄集合と語彙だけを検査し、値規則（`source_version == 1`固定）を見て
いなかった**。受入1回目の測定ブロック（`…-evidence-measurements-v1.md`・失敗の記録として保存）
で検証器が`source reference identity is invalid`で停止し発覚。是正規則へversion表記の適合を
追加して再生成した。教訓＝形式診断は検証器の規則を**部分模倣せず、検証器自体を通す**こと。

## 3. 受入

**受入測定ブロック`records/development/2026-08-19-n7-candidate-remediation-evidence-measurements-v2.md`
参照**（4件のv3検証器単独合格・N7単独exit 0＝事前走査で機械固定したREDからのGREEN・台帳関連
試験群68本exit 0・再生成4件のdigest固定・全entry二重実行一致）。`git diff --check`合格。

## 4. 根因と再発防止（観測）

4件は2026-08-18の同一commit（`3b76b97`）で、**検証器を通さずに登録された**（AGENTS §3
「台帳recordは正規tool（検証器を含む）だけで作成」の違反例）。同じ台帳への本日の登録2件
（safe_storage候補とその仕分け決定）は正規経路（機械生成→検証器→commit）で合格しており、
**登録時に検証器を1回実行するだけで防げた**。既存規範の再確認で足り、新規則は追加しない。

## 5. 未実施

TODO反映とcommit。push（利用者の運用に従う）。
