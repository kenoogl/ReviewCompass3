# Identity Chain Preflight

- Work：
- 変更対象：
- Decision／Authority：

## Identity chain

```text
source content identity → provenance (HEAD等) → derived output → authoritative record → commit後freshness
```

| 結線 | ID／Digest | 保存先 | version更新 | commit後の扱い | validator／Test |
| --- | --- | --- | --- | --- |
| source content |  |  |  |  |  |
| provenance |  |  |  |  |  |
| derived output |  |  |  |  |  |
| authoritative record |  |  |  |  |  |

## 必須確認

- [ ] source内容変更と、artifact／文書だけのcommitを区別する。
- [ ] immutable outputの新version、旧versionの保持、current authorityを定める。
- [ ] write → commit → re-read → freshness判定の最小E2EをAcceptance Testに含める。
- [ ] ID、version、Digest、Decision、consumerの全結線を列挙する。
- [ ] 一結線が欠けた場合の停止条件とHuman判断点を定める。
