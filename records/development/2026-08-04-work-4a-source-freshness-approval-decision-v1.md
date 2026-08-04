# Work 4A Source Freshness Approval Decision v1

- Decision：`DEC-WORK4A-SOURCE-FRESHNESS-001`
- decision maker：Human
- instruction：`承認`
- status：`approved_effective`

Source Snapshotの対象source content identityとGit HEAD provenanceを分離する。対象source file Digestと
source universeが同一ならfreshと判定し、HEADは採取時点の来歴として別に保持する。Ledger artifactだけの
commitでsource freshnessを失わせない。

次作業は、この規則のRED Acceptance Test、schema version、旧Snapshotの扱い、freshness validatorを実装する。
このDecisionだけで旧Snapshotをfreshへ書換えず、Work 4Aを完了にしない。
