# Claude向け 第2段最小信頼基盤・再判定レビュー指示 v1

あなたは、ReviewCompass3の第2段「最小信頼基盤を選び、既存資産を評価する」の独立レビュー担当です。
作業担当とは独立に、固定された再判定候補が利用者の採用判断に使えるかを確認してください。
成果物は変更せず、読み取りと検証だけを行ってください。

## 1. レビュー対象

- 対象：`records/development/2026-08-13-stage2-minimum-trust-foundation-reassessment-candidate-v1.md`
- 対象SHA-256：`30e8b70d26dfc41955867ad8b7d9a09b3215cbbe85be3916763b0d0e72ea7d08`
- 観測対象コミット：`89649713d99ec1edc86444e3e39cca4152972286`

## 2. 固定材料

最初に次のfileを読んでください。必要な確認は、この一覧の記述が直接参照するpath、Git object、
および現在のread-only Git状態に限定してください。

1. `docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md`
2. `docs/development/2026-08-12-stage2-minimum-trust-foundation-bootstrap-work-ticket-v1.md`
3. `records/development/2026-08-12-stage2-minimum-trust-foundation-adoption-table-candidate-v1.md`
4. `records/development/2026-08-12-stage2-minimum-trust-foundation-completion-review-v1.md`
5. `records/development/2026-08-12-stage2-minimum-trust-foundation-post-fix-review-v1.md`
6. `docs/development/2026-08-12-stage2-official-test-entry-restoration-bootstrap-work-ticket-v4.md`
7. `records/development/2026-08-12-stage2-official-test-entry-restoration-evidence-v1.md`
8. `records/development/2026-08-12-stage2-official-test-entry-restoration-completion-review-v1.md`
9. `docs/development/2026-08-12-pilot-git-runtime-read-only-guard-bootstrap-work-ticket-v1.md`
10. `records/development/2026-08-12-pilot-git-runtime-read-only-guard-bootstrap-start-review-v1.md`
11. `docs/development/work-review-protocol.md`の§11.1
12. レビュー対象の再判定候補

復旧時の公式試験結果記録が読める場合は、次も照合してください。存在しない場合は、それだけで候補全体を
不合格にせず、Git内のEvidenceと現状態から代替確認できるかを判断してください。

- `/private/tmp/reviewcompass-pilot-git-runtime-guard-recovery-receipt-v1.json`
- 申告SHA-256：`a8ac242f7bf7da867cd456daa0997b85f05ac8f1d0eeedf4af516e9180db2185`

## 3. 本質と判定する問い

本レビューの本質は、四領域の入口を採用、保留、使用停止のどれに置くかと、第2段完了判断へ進める材料が
揃ったかを確認することです。次の問いへ答えてください。

1. 履歴保存を`採用候補を維持`とする根拠は十分か。
2. 開発コード管理を`採用候補を維持`とする根拠は十分か。
3. テストコード管理を`採用候補へ変更する案`とすることは妥当か。特に、公式runnerの稼働可否と、
   runnerが実行する個別の静的Git検査の保証範囲を分ける判断が、上位計画と整合するか。
4. レビューを`採用候補。ただし今回の独立レビュー待ち`とすることは妥当か。
5. Python 3.13移行は第2段完了前の必須条件か、採用後の独立作業か。既存記録と利用者判断を
   勝手に変更していないか。
6. 候補の報告とGit実状態、結果記録、上位計画に不一致があるか。
7. 候補を利用者判断へ渡すと、第3段で重大な誤りを広げる具体的危険があるか。

中心となる判断を否定できる反証を最低一つ試してください。ただし、反証のためにfileを変更したり、
新しい仕組みを作ったりしてはいけません。

## 4. 本質から外れた過剰対応の禁止

ここは特に厳守してください。

- コード、試験、設定、計画、TODO、記録を変更しないでください。
- Git runtime guard、静的解析の一般化、Python移行方法、新しい管理制度、追加validatorを設計しないでください。
- 個別のGit検査を完全化する方法をレビューの主題にしないでください。
- 範囲外の問題、将来の改善、表現改善を止める指摘にしないでください。
- 問題を見つけた場合は、四領域の候補判定または第2段完了可否へどう影響するかだけを述べてください。
- 修正案は原則として出さないでください。判定に不可欠な場合だけ、必要最小限の方向を一文で示してください。
- 指摘数、実行した試験数、文書量をレビュー品質とみなさないでください。
- 「念のため」「より堅牢にするため」という理由だけで対象を広げないでください。

## 5. 実行上の禁止

- fileの作成、変更、削除、stage、commitをしない。
- push、tag、amend、rebase、reset、force push、履歴書換えをしない。
- 外部送信、ネット検索、別repositoryの探索をしない。
- 書込みを伴う試験を実行しない。既存file、Git object、既存receiptの読み取りと、read-only commandに限る。

## 6. 出力形式

日本語で、次の順に簡潔に出力してください。

1. `判定`：`verified`、`reported_unverified`、`report_execution_mismatch`、`blocked`のいずれか。
   ここで`verified`は「再判定候補を利用者判断の材料にできる」という意味であり、第2段完了の承認ではありません。
2. `四領域`：履歴保存、開発コード管理、テストコード管理、レビューについて、それぞれ
   `採用候補`、`保留`、`使用停止候補`の一つと理由を一文。
3. `Python 3.13`：第2段完了前の必須条件か、採用後の独立作業か、証拠不足か。
4. `止める指摘`：0件なら`0件`。ある場合は、根本原因ごとに一件へまとめ、
   `work-review-protocol` §11.1の類型、証拠、四領域または段完了への影響だけを示す。
5. `報告不一致`：0件なら`0件`。ある場合は証拠と影響を示す。
6. `試した反証`：commandまたは照合、終了コード、結果、中心判断への影響。
7. `利用者が判断する点`：技術判定で代行しない事項だけ。
8. `未実施`：変更、外部送信、段完了をしていないこと。

余分な改善案、代替設計、長い将来計画は出力しないでください。
