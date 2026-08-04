# DEC-WORK4A-REBUILD-DESIGN-002

## Decision

Humanは`docs/design/2026-08-04-work-4a-rebuild-design-v2-proposal.md`を承認し、Work 4A実装の正本をv2へ切り替えた。

## 承認範囲

- `SRCU-WORK4A-TOOLS-PY-V1`のsource universe
- Policy artifact、Operational Human Decision、Baseline current導出、canonical Digestの規則
- legacy Task Contractに根拠が欠ける場合の`evidence_insufficient`停止
- Relationを含むv2 E2E acceptance
- revert mapを実装開始条件とすること

## 効力

- v1は履歴として保持するが、実装正本ではない。
- `c4bfb57`の試作moduleとv1 E2E testはactual artifactまたはWork 4A完了の根拠に使わない。
- v2の実装は、Policy artifact schema、source universe、revert mapをv2の開始条件として確認してから行う。

## 根拠

- Human approval：2026-08-04の会話における「承認」。
- 対象設計：`docs/design/2026-08-04-work-4a-rebuild-design-v2-proposal.md`
