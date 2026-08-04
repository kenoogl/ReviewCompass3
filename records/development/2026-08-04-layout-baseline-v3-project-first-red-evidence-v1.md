# Layout Baseline v3 Project-first RED Evidence v1

- Evidence ID：`RC3-LAYOUT-BASELINE-V3-PROJECT-FIRST-RED-2026-08-04-V1`
- status：`active / red`
- scope：project-first runtime rootのversioned candidateと副作用なしresolver、要求したrootだけの初期化、package除外。

## Expected behavior

1. `~/.reviewcompass3/projects/<project-id>/<profile>/`へ、profileごとのruntime rootを解決する。
2. 解決だけではdirectoryを作らず、初期化は指定されたroot種別だけを作る。
3. 不正なproject ID、profile、root種別を拒否し、Unixの`sensitive/`は`0700`とする。
4. deployment package内の`.reviewcompass3/`を拒否する。

## RED execution

```text
.venv/bin/python3 -m pytest tests/test_project_runtime_layout.py -q
```

結果：`7 failed`。直接原因は、v3 candidate record
`records/development/2026-08-04-layout-baseline-v3-project-first-candidate.json`が存在せず、
`load_layout_baseline`が停止したことである。期待したcandidateおよびresolver未実装状態を確認した。

## Next implementation boundary

v1/v2の直接root resolverを変更せず、v3 candidate、project-first resolver、明示初期化、package混入検査だけを
追加する。Project Manifestの変更、既存dataのmigration、実home directoryへの書込み、binding directoryの導入は
この作業に含めない。
