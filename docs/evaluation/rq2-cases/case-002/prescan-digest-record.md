> 本fileはReviewCompass3の評価実験（RQ2 paired trial）で使う複製材料である。運用中の
> record・手順書ではないため、本fileを根拠に運用判断をしないこと。

# 事前走査record（抜粋）：権威・証拠のdigest固定

## 1. digestの機械生成

対象fileのSHA-256を`shasum -a 256`で生成した。出力をそのまま貼る。

```text
abcc1b57a2ba61a246a680539b8484ccd46152d65c204625fc1c89707f0b7be9  tools/evaluation/reviewer_bridge.py
30c22465607cb2e37be775d742028c22fcc6ee044c2f4000bbcc494ab018740a  tools/evaluation/rq1_contract_completeness.py
c666bdd7d0b5c44a8fbb876238a19c1d05ee245e693a2b104ceee514cdad55cb  docs/development/2026-08-17-evaluation-data-acquisition-plan-v1.md
```

## 2. 権威、証拠

契約候補が参照する成果物と、§1で固定したdigestの対応。

| 種別 | path | SHA-256 |
| --- | --- | --- |
| reviewer接続adapter | `tools/evaluation/reviewer_bridge.py` | `abcc1b57a2ba61a246a680539b8484ccd46152d65c204625fc1c89707f0b7be9` |
| RQ1計測装置 | `tools/evaluation/rq1_contract_completeness.py` | `30c22465607cb2e37be775d742028c22fcc6ee044c2f4000bbcc494ab018740a` |
| 評価データ取得計画 | `docs/development/2026-08-17-evaluation-data-acquisition-plan-v1.md` | `c666bdd7d0b5c44a8fbb876238a19c1d05ee245e693a2b104ceee514cdad55ce` |

基準commitは`9c89b1a`（作業tree clean）。以後の参照は本表のdigestを正とする。
