---
record_id: RC3-PROJECT-MANIFEST-V2-RED-EVIDENCE-2026-08-04-V1
recorded_at: 2026-08-04T06:35:00+09:00
status: verified_red
---

# ReviewCompass3 Project Manifest v2 RED Evidence V1

## 固定対象

| role | artifact | SHA-256 |
|---|---|---|
| current Layout approval | `records/development/2026-08-04-layout-baseline-v2-approval-decision.json` | `856345948af57bcfa373eb2766768d9c38078d7ba5fe65b0d76d68e452ceaa7e` |
| RED／GREEN共通Test | `tests/test_layout_baseline.py` | `fb122cee9186ba22883ba081e578fcc5fd617ba400ae5a908bc30808844bc077` |

## 実行

```text
python3 -m pytest tests/test_layout_baseline.py -q
```

結果は`1 failed, 11 passed in 0.09s`だった。

失敗は`test_reviewcompass3_project_manifest_uses_approved_v2_boundary`の一件だけで、
repository rootに`.reviewcompass/project-manifest.json`が存在しないため
`LayoutError: Cannot load Project Manifest`となった。承認対象v2 Digest、既存v1／v2 Test 11件は合格した。

期待する実repository用Manifestとartifact rootが未配置であることだけを理由とする正しいREDと判断した。
