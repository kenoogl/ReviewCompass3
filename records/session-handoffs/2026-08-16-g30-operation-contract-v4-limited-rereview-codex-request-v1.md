# 最小運用契約実行 契約候補v4 限定再確認依頼record v1（Claude→Codex）

- 作成日：2026-08-16
- 依頼元：Claude（操縦・契約候補v4の訂正担当）
- 依頼先：Codex（レビュー専任）
- 受け渡し方式：`docs/development/pilot-driven-record-handoff.md`のrecord正本方式
- レビュー種別：訂正1点と退行の有無だけの限定再確認（読取り専用）
- 共通手順：`docs/development/work-review-protocol.md`

## 1. 役割分担

- **Codexが行うのは§4の限定再確認と、判定record 1件の作成・単独commitだけ**である。全面再走査をしない。
- 判定後の後続はClaudeが実施する。

## 2. 対象と前提

- 対象契約候補v4：`records/task-contract/2026-08-16-minimal-operation-contract-execution-candidate-v4.md`
  - SHA-256：`d7b1861ccc73cb8f1c305294bf7c7e2a5fddd6ddb3fb46eab74e3204e8a2a7a1`
  - 固定commit：`918e838fd9d7bc4d102030274158fbcacdeb1f81`
- 直前版契約v3（採用済み・開始可判定済み）：`records/task-contract/2026-08-16-minimal-operation-contract-execution-candidate-v3.md`
  - SHA-256：`d97a742bd2c67946f4336a06167767c4060a38157073e13cb42e5ecbf2117f85`
- v3開始可の判定record：`records/development/2026-08-16-minimal-operation-contract-execution-v3-limited-rereview-v1.md`
  - SHA-256：`daa414658c2d6fc8ef712ceb47ae9b188cd787c1214be1ab826209795e97689e`
- 経緯：v3採用後の実装で、対象試験（RED、58件、commit `fd24453`）の正例が機微停止した。原因は
  固定操作名`requirement_candidate_check`（27文字、`[A-Za-z0-9_-]`の連続）が§8.2の高乱雑性検査
  （既定24文字以上・乱雑さ3.5以上）へ実測3.63で一致することである。`design_acceptance_check`は23文字で
  一致しない。実装の誤りではなく§8.2の除外規則の穴であり、契約どおり実装するとG24操作の正例が必ず停止する。
  実装途中の製品fileはrepository外へ退避済みで、作業treeはcleanである。
- v4の訂正は1点だけである：§8.2へ手順3b「正確な位置`/operation`にあり、§6.1の固定registry操作名と完全一致する
  値だけを検査対象から外す」を追加し、受入条件10を同じ定義（2操作の正例が停止しないこと、registry操作名と
  一致しない`/operation`値は除外されないこと）へ合わせ、見出しと§15の次作業文を更新した。これ以外の本文は
  変更していない。

## 3. 開始時の確認（Codexの鮮度検査）

1. 自分宛の最新依頼recordが本recordであることをGit履歴から機械特定する。
2. `git status --short`が空であることを確認する。
3. §2の3 fileの内容識別値を機械計算し、本record記載値と一致することを確認する。
4. 不一致・宛先違い・前提不一致の場合は、作業せずその旨を判定recordへ書いて停止する。
5. Python実行は常に`.venv/bin/python3`を使う。

## 4. 限定再確認の内容

契約候補v4を成果物変更なしで読み、次の2点だけを確認する。

1. **訂正1点が閉じたか**：手順3bの除外により2操作の正例が機微停止しなくなるか
   （`find_high_entropy`の実測で`requirement_candidate_check`が3.63、`design_acceptance_check`が非一致で
   あることの機械確認を含む）。除外が「`/operation`位置」かつ「固定registry操作名との完全一致」だけに限定され、
   利用者の識別子・自由文・path・未知keyへ拡大しないこと、後決め要素がないこと。
2. **退行がないか**：v3とv4の全文差分が§2記載の訂正範囲に限定され、v3で開始可とされた境界
   （書込み境界の確定点定義、registry縮小、目的縮小、束縛照合、固定識別値）に退行がないか。

必須の機械確認（各単独command・終了コード個別判定）：

- `find_high_entropy`による2操作名の実測（27文字側が一致、23文字側が非一致）
- §6.1の再利用4 file、§6.2の1 file、§6.3の保護10 pathの内容識別値の一致

## 5. 判定recordの作成と停止（Codexの成果物）

1. 判定recordを次のpathへ作成する。
   `records/development/2026-08-16-minimal-operation-contract-execution-v4-limited-rereview-v1.md`
2. recordの冒頭に、Reviewerのmodel名とreasoning effort（起動時に表示された値）を記載する。
3. 判定は`開始可`または`修正要`とし、根拠を書く。事実の主張には【実測】【記録】【推測】のラベルを付ける。
4. **そのrecord 1件だけをstageして単独commitし、停止する。** record以外のfileを変更しない。

## 6. Claudeの事後照合（参考）

Claudeは応答後に、(a) 判定recordのcommitが対象commit`918e838fd9d7bc4d102030274158fbcacdeb1f81`より後にあること、
(b) 変更pathが判定record 1件だけであること、(c) 判定内容、を機械照合してから後続へ進む。

## 7. 依頼完了条件

本recordを意味単位commitへ固定し、`git status --short`が空であること、`git diff --check`が終了コード0であることを
確認する。
