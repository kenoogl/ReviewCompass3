# 無工具Claude疎通 実行時host安全停止 v2

- 日付：2026-08-12
- approval ID：`RC3-CB-APPROVAL-20260811-002`
- 正規入口：`.venv/bin/reviewcompass3-pilot`
- 結果：`host_safety_rejected_before_entrypoint`

## 実行結果

正規入口の実体化とHumanの再承認後、文書どおりの
`reviewcompass3-pilot bootstrap --manifest-digest <固定値> --approval-id <固定値>`を一度だけ要求した。
host安全審査は、正規入口processの作成前に拒否した。

- 正規入口process作成数：0
- Claude事前検査process作成数：0
- payload process作成数：0
- 外部送信数：0
- raw／launch／receipt：作成なし
- approval token：`pending`に一件だけ存在
- 自動再試行：なし
- 別経路への迂回：なし

## v1診断の再評価

`2026-08-11-claude-bootstrap-host-route-diagnosis-v1.md`は、内部module直接起動がhost拒否の主因である
可能性を推測として示した。今回、正規入口を実体化して同じ拒否となったため、この推測は反証された。

【実測】host拒否理由は、正規入口を経由していてもClaude／Anthropicへの直接外部送信が、hostの信頼済み
ReviewCompass workflowではないことである。リポジトリ内の入口名やPython起動方法の修正だけでは解消しない。

## 停止判断

同じ要求の再承認依頼、再試行、直接Claude起動、shellや別toolによる迂回を行わない。hostが信頼する外部送信
workflowの追加はリポジトリ実装だけでは認められず、新しい外部authorityを要するため、本経路を停止する。
