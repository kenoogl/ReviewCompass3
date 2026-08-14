# Claude向け 立て直し計画v5 第3段 完了前全体レビュー指示 v1

次の固定材料だけを入口に、読み取り専用で第3段完了候補の全体レビューを行ってください。
これは利用者が手動で渡す、第3段で予定された最後の他社モデル確認です。

## 1. 固定材料

- 観測commit：`79172ef2385a3e8b8f5ea81197c38180fbdb6495`
- 第3段完了候補：`records/development/2026-08-14-stage3-completion-candidate-v1.md`
  - SHA-256：`ab9fe71622c435a8e01bf1385d682ae66814f77928edaf648fd3b3355eb6b1e4`
- 採用済み立て直し計画v5：`docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md`
  - SHA-256：`8c814067511797e445d66779ad144f42ea0b139501ff6002a7d6c46e6706055c`
- 現行開発方針：`docs/development/2026-08-02-development-policy.md`
  - SHA-256：`422d234a0503670e61936edfe98cd13451f4e7af6bfc1506a07824f2904f0fac`
- 第3段を正しい実装の誤拒否確認へ限定する判断：
  `records/development/2026-08-14-stage3-correct-behavior-witness-method-amendment-decision-v1.md`
  - SHA-256：`76aa813046a07176650e0bc5db5d5308f569a8e51011f15cd2c21341852e0d2f`
- 既知の正しい現在状態による実施Evidence：
  `records/development/2026-08-14-stage3-known-correct-state-witness-execution-evidence-v1.md`
  - SHA-256：`5d65e67b6239f9f267eaac8fce749b28267e81618ca7ea01c26614eb2ac0ebc4`
- 同独立完了レビュー：
  `records/development/2026-08-14-stage3-known-correct-state-witness-independent-completion-review-v1.md`
  - SHA-256：`623095ce50005400977749fa323e6bea00213db46b9487651ea42e01337afd97`
- 第3段成果物ライフサイクル整理Evidence：
  `records/development/2026-08-14-stage3-created-artifact-lifecycle-inventory-evidence-v1.md`
  - SHA-256：`ae20e42659624b76ec378b0f7a1123a29fd277d1f345f880e06bf1b38d14e5f1`
- 同独立完了レビュー：
  `records/development/2026-08-14-stage3-created-artifact-lifecycle-inventory-independent-completion-review-v1.md`
  - SHA-256：`ea06bdb6566bc7e9f5653fa8a45e573b2966aed12e2e70fcd6de0a482a1544c8`
- 手動の他社モデル確認回数Decision：
  `records/development/2026-08-13-stage3-manual-external-review-limit-decision-v1.md`
  - SHA-256：`9c0bd9d371b1f6b59be49818b759d17e3877d645f42ff6dc4a4c0eacbeb05136`

最初に、上記fileのSHA-256と観測commitの実在を照合してください。申告値が一致しない場合は、
その影響を受ける判断を`reported_unverified`または`report_execution_mismatch`として止めてください。

## 2. 確認する中心判断

次の主張を支持する材料が揃っているか、結論をなぞる前に反証してください。

> 現行Planが第3段へ要求する「正しい現在状態の誤拒否確認」と「第3段中の成果物ライフサイクル確認」は、
> 固定Evidenceと独立レビューで満たされ、未処置の誤拒否、未分類成果物、役割終了成果物は残っていない。

具体的には、次だけを確認してください。

1. 第3段の現行完了条件が、古い参照文字列抽出や試験数削減ではなく、正しい現在状態の誤拒否確認へ
   本当に置き換わっているか。
2. 承認済み二確認点が現在設計から導かれ、観測状態で再現され、同じ状態の正規全試験1,728件成功へ
   結び付いているか。件数を恒久的な合格値にしていないか。
3. 失敗試験0件という結果から「今回の二確認点について未処置の誤拒否なし」とする限定された判断が妥当か。
   あらゆる将来実装の受理まで過大主張していないか。
4. 第3段開始基準からの127 pathが19意味群へ重複・未分類なく入り、コード、文書、構造化記録、試験で
   確認方法を分けているか。`役割終了0`が局所的な文書整合だけで決められていないか。
5. 127 path観測後の作業票、レビュー、完了候補、Claude指示、TODOをclosing deltaとして扱い、
   全列挙を再帰的にやり直さない境界に、未分類の実装成果物を隠す余地がないか。
6. 現在境界を持つD11、D17、D15、D16、現役コードC01と、履歴だけのD02、D14等を取り違えていないか。
7. 既に個別承認・独立確認済みの変更を自動的に戻さず、同時に今後の削除の前例にもしていないか。
8. 誤った実装の受理、守れない保証表示、安全方針に反する副作用の見逃しを、第3段完了済みと偽っていないか。

中心判断を否定する反証を少なくとも一つ試してください。既存の機械結果を再利用できる箇所では再利用し、
同じ1,728試験や127 pathの全面確認を儀式的に繰り返さないでください。

## 3. 深さと禁止事項

本質から外れた過剰な修正案を出さないでください。このレビューの目的は、第3段完了候補の真偽を判断することです。
次は依頼していません。

- 全1,728試験の一件ずつの必要性・要求対応・内部実装の詳細レビュー。
- 127成果物すべての全文再審査。
- 試験数、文書数、実行時間を減らすための整理。
- 誤った実装の受理、保証表示、副作用を対象とするWork 8の開始。
- 新しい台帳、検査器、試験、関門、恒久script、schema、コード変更の提案。
- 第4段の設計や実施。
- 既に独立確認済みの削除や訂正の全面的なやり直し。

止める指摘がある場合は、中心判断を崩す具体的な一原因へまとめてください。修正方向は、完了候補の真偽を
判断するために不可欠な最小範囲だけを示してください。将来の改善、好み、一般論を混ぜないでください。

## 4. 出力形式

1. 判定：`verified`、`correction_required`、`reported_unverified`、`report_execution_mismatch`のいずれか
2. 止める指摘（0件なら0件）
3. 報告不一致（0件なら0件）
4. 現行完了条件と完了候補の対応
5. 正しい現在状態、1,728試験、誤拒否0件の結び付き
6. 127 path・19意味群・ライフサイクル分類の確認
7. 試した反証と結果
8. 利用者が段完了前に判断する点
9. 未実施事項

第3段の完了承認を代行しないでください。fileの作成・変更、stage、commit、push、履歴書換え、外部送信、
コード・試験・設定・Issue・TODOの変更は行わないでください。
