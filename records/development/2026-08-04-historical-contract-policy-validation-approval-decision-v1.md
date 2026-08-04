# Historical Contract Policy Validation Approval Decision v1

- Decision：`DEC-HISTORICAL-CONTRACT-POLICY-VALIDATION-001`
- decision maker：Human
- instruction：`条件付きで採用`
- status：`approved_effective`

completedかつhistoricalなContractは、作成時に固定したPolicy DigestとGit provenanceで検証する。現行workspaceの
Policy Digest一致を要求しない。active Contract、再利用する成果、security・authority・不可逆操作に影響するPolicy変更は
現行Policyへの再確認を必須とし、旧Contractを開始許可または現在の完了根拠へ流用しない。

次の実装ではContract status、historical provenance、例外時の`revalidation_required`、正例・負例をTDDで固定する。
