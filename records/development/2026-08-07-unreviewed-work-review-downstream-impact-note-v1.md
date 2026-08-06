# 未レビューcode後追いレビューにおける下流影響の扱い（参考情報）v1

- 状態：参考情報（authorityではない。Issue着手時の計画材料）
- 作成日：2026-08-07
- 対象Issue：`ISSUE-UNREVIEWED-WORK-REVIEW-BACKLOG-001`
  （`.reviewcompass/workflow/issues-v4/issue-unreviewed-work-review-backlog-001--v1.json`）
- 関連：トリアージメモ`records/development/2026-08-07-unreviewed-work-review-triage-memo-v1.md`、
  `docs/development/work-review-protocol.md`

## 1. 問い

本Issueの対応であるcodeを修正した場合、そのcodeを使う下流のcodeへ影響が及ぶ。
この問題に対処できるか（2026-08-07のHumanの問い）。

## 2. 答え：影響は三つに分解でき、二つは既存の仕組みで対処済み、一つはWork 4Bが恒久解

### 第一層：呼び出し元の機械的な列挙（今すぐ可能）

修正対象moduleを使う下流はimport文の走査で機械的に列挙できる。work-review-protocol §3は
開始時に許可範囲・禁止範囲・期待成果を固定するため、**修正の作業単位の固定入力へ
「当該moduleを使う下流の一覧」を含めれば**、影響範囲を推測でなく列挙で扱える。

### 第二層：全テストの常時実行（対処済み）

全テスト（2026-08-07時点1047件・約6秒）がコミット条件に含まれ、下流に振る舞いテストがあれば
破壊はここで捕まる。検出が実際に働いた先例：候補record 1件の追加が下流の固定テストと3回衝突し、
その都度検出された（`ISSUE-TEST-GROWTH-STATE-PINNING-001`）。
ただしテストは作成者の盲点を共有するため、下流被覆の完全性は保証されない（本Issueの前提と同じ）。

### 第三層：過去の合格のstale閉包（対処済み・先例あり）

最も深刻な下流影響は、守り役のcodeを修正した場合に**そのcodeが過去に出した合格も疑わしくなる**
時間方向の影響である。既存規則：AGENTS.md開発方針「validatorまたは入力前提を変更した場合は
旧合格をstaleとし、risk別の正例・負例・境界例と必要な独立oracleを再実行する」、
work-review-protocol §7「修正後は、変更した検査器、入力前提、影響する過去verdictをstaleとして
再確認する」。先例：receipt改竄欠陥の訂正時、初回GREEN Evidenceをstaleとし訂正側を有効な
完了根拠へ差し替えた（`DEC-MACHINE-OPERATION-ROUTING-RECEIPT-INTEGRITY-001`）。

### 穴：下流依存の権威的な台帳が無い（恒久解はWork 4B）

第一層のimport走査はその場の機械操作であり、「このroutineを誰が使い、どのbaselineに属すか」の
正式な台帳は未整備である（CL-6A-06が基盤未整備で保留されている理由と同一）。恒久解は
Work 4B（実装前の既存routine検索、Entry・Relation・Baselineのnew-only記録、共通候補ごとの
振る舞いテスト固定）であり、素材はWork 4Aのroutine 1003件・682比較groupとして生成済みである。

## 3. Issue着手時への含意

1. **順序**：本線のWork 4Bを先に進め、本Issueを後に着手する現在の順序は、下流影響への備えとして
   合理的である。台帳完成後なら、下流影響の列挙が台帳照合になる。
2. **着手時の運用案**：修正の作業単位ごとに「下流利用者の列挙」を開始時の固定入力へ含める。
   台帳完成前でも第一層で穴を塞げる。採否は着手時のHuman判断とする。
3. **レビューと修正の分離**：レビューで欠陥が見つかっても承認なしに修正へ移らない
   （work-review-protocol §2-5、§7）。修正は別作業単位とし、その単位で本noteの三層を適用する。

## 4. 本noteの限界

- 本noteは対処の実施も順序変更も承認しない。Issue `registered`のまま、着手はHuman判断である。
- テスト件数・module数は2026-08-07時点の実測値であり、着手時に再測定する。
