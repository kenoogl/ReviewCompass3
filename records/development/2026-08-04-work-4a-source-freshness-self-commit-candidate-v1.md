# Work 4A Source Freshness Self-commit Candidate v1

- status：`blocking / Human decision required`
- observation：Ledger commit前Snapshot `7806b871…` と現HEAD `812a4bb…`の対象228 source file Digestは全件一致した。
- problem：Source Snapshot IDがGit HEADを含むため、Ledger artifactだけをcommitしてもSnapshot IDは`2a301efe…`へ変わる。Ledgerは旧Snapshotへ結線されるため、厳格なHEAD比較では自分自身の保存commitでstaleになる。

対処候補は、(A) source universe content identityとGit HEAD provenanceを分離し、対象source Digestが同一ならfreshと判定する、または(B) artifact commit後のSnapshotを新たに採取し、Ledger bindingを更新する、である。Bは更新commitで再びHEADが変わるため循環する。推奨はAである。

この判断前にWork 4A完了、implementation_ready、Ledger freshnessの確定は行わない。
