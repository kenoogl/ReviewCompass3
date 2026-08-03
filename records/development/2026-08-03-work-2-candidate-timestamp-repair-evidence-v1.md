# Work 2判断候補timestamp修復Evidence V1

- evidence_id: `RC3-WORK2-CANDIDATE-TIMESTAMP-REPAIR-2026-08-03-V1`
- repaired_at: `2026-08-03T15:45:48+09:00`
- Decision: `DEC-WORK2-CANDIDATE-TIMESTAMP-2026-08-03-V1`
- Decision record SHA-256: `9dcc7570d80bde8711049c688e5f03ec4a607457a96179fd146c512c288f271a`

## 修復

Work 2 Human判断候補の意味内容を変更せず、誤って再利用したWork 1完了承認時刻を、最初に検証可能な
Work 2 session境界へ訂正した。frontmatterに旧時刻、旧Digest、修復Decision、理由を保持した。

| item | before | after |
|---|---|---|
| `generated_at` | `2026-08-03T14:35:03+09:00` | `2026-08-03T14:56:34+09:00` |
| candidate SHA-256 | `2666511bcf95a2fdc5237257b5c5e38fbc7dc1c80fd829064b02e34b759e6ab9` | `bfec3b29cf8ebb5ffeedc349e39b2215922ebef8e4105a258e73279a7226a252` |

Intent、統合用語集、Plan本文は変更していない。

## 再監査

```text
audit: passed
Intent required sections: 8 / 8
authority boundaries: 3 / 3
registered canonical tokens: 109
required tokens: 13 / 13
missing tokens: 0
duplicate tokens: 0
```

Plan current refs、Work 1 corrective snapshotの3 artifact Digest、candidateの訂正metadataを再照合した。

## Session Evidence

旧候補を対象にした`rc3-work2-operational-20260803-001`は、判断関門としてsupersededとする。rawと
Session Evidenceは問題発生記録として保持し、削除または成功扱いへの上書きをしない。

新しい`rc3-work2-operational-20260803-002`では、旧candidate Digestの`artifact_stale`、新Digestの
`artifact_reverified`、新Digestに束縛した`human_decision_requested`を順に保存した。

| artifact | SHA-256 |
|---|---|
| raw event stream | `71346c1f6689fc686d1e26debb6d3572d12854f1859aaa53799f74b7c7af7cae` |
| index | `0f2d3e020f6346c080fbcdeda4b1af2f2002c93a121b3d8e6060d4834f66ab1c` |
| summary | `22aa23090cefb8bad43ecb09fe8f32c5bb352c0b3ac219d437927d14363af17e` |
| transcript | `794e454ba051b705228040972e1a8de988c58f7a5595451ff098acf238fc9088` |
| Session Evidence | `9af96cd068b61a093b4f7068bfd7e553b3bdc475d3ba87f93771434700ae340a` |

保存後にrawと3派生物を再読込し、Session EvidenceのDigestと一致した。sessionは開始・終了済み7 event、
authority `valid`、display `rendered`、projection `paused`、Human判断1件、blocker／staleなし、次actionは
訂正済みWork 2候補のHuman判断である。独立検査結果は`verification: passed`だった。

## Outcome

生成時刻、candidate Digest、判断要求eventの不整合は閉じた。Work 2の内容監査結果は再現され、訂正済み
candidateをHuman判断対象として使用できる。修復DecisionはIntent／用語集の承認、promotion、Work 3開始を
含まないため、現在地はWork 2 `verified / human_decision_pending`である。
