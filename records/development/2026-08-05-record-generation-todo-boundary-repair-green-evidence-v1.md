# 定型記録生成 TODO最小縦切り 境界訂正GREEN Evidence v1

- 対象Issue：`ISSUE-HTC-66C3E6CA`
- 承認：`DEC-RECORD-GENERATION-PLAN-001`（TODO最小縦切りだけ。新しいDecisionは作っていない）
- 指示：`records/session-handoffs/2026-08-05-codex-to-claude-repair-record-generation-todo-boundaries.md`

独立確認で判明した2つの境界不足を、Test先行で訂正した。訂正は既承認の「TODOだけ」「Evidence節の参照」
「既存Issue正本を使う」範囲内である。

## 1. 独立再現（修正前）

### 欠陥1：参照の対象範囲が広すぎる

`collect_reference_digests()`はEvidence見出しの存在だけを確認し、document全体のlinkを収集していた。

```text
TODO末尾に別見出しを足し、
- [範囲外参照](docs/current/reviewcompass3-plan-current.md) — SHA-256 <実Digest>
を置く。
→ 節内26件に対し、27件目として範囲外pathが返る。
```

実測：節内 `26件` → 節外link追加後 `27件`、27件目は`docs/current/reviewcompass3-plan-current.md`。

### 欠陥2：active Issueの許可一覧がTODO自身から作られている

`todo_compaction_known_active_ids(document)`がTODO本文のIDをそのまま許可一覧にしていた。

```text
TODOの`ISSUE-PILOT-TODO-GROWTH-001`を`ISSUE-UNKNOWN-001`へ置換する。
→ 自己導出したknown setが{'ISSUE-UNKNOWN-001'}になり、compaction validatorが受理する。
```

実測：`default_verify`が**受理してしまった**。

## 2. 修正後の再確認

| 再現 | 修正後の結果 |
| --- | --- |
| 欠陥1 | 節外linkを足しても収集は`26件`のまま増えない |
| 欠陥2 | `default_verify`が`TodoCompactionError: unknown active ID`で停止する |

正本から得たknown ID：`ISSUE-HTC-66C3E6CA`、`ISSUE-HTC-BEB5E0BD`、`ISSUE-HTC-C9F6C917`、
`ISSUE-PILOT-TODO-GROWTH-001`。実repositoryのroot TODOは`default_verify`を通る。

## 3. 正本とするIssue root

許可するactive IDは、TODO本文ではなく次のroot直下の通常`.json`からだけ得る。`rglob`は使わない。

| root | record_kind | IDを読むfield |
| --- | --- | --- |
| `.reviewcompass/workflow/issues` | `issue_record` | `issue_id` |
| `.reviewcompass/workflow/issues-v4` | `issue_record` | `issue_id` |
| （指示書記載の旧形） | `issue` | `record_id` |

**指示書との差異**：指示書はlegacy rootを`record_kind: "issue"`＋`record_id`と記していたが、
実際のlegacy record`issue-pilot-todo-growth-001--v1.json`は`record_kind: "issue_record"`＋`issue_id`
である。指示書は同時に「`ISSUE-PILOT-TODO-GROWTH-001`はlegacy rootの正本に存在するため、
正しいloaderへの変更後も正例として通る」とも述べている。両立させるため、loaderは
`issue_record`と`issue`の両方を受理し、それぞれ`issue_id`／`record_id`から読む形にした。
未知のrecord_kindは従来どおり停止する。IDの出どころがTODO本文でなくIssue正本になるという
安全上の性質は変わらない。

symlink、JSON不正、未知record_kind、IDの欠落・不正・重複はいずれも`issue_root_invalid`で停止する。
`.gitkeep`は`.json`ではないため読まない。

## 4. Evidence節に限定した検証

`todo_record_generation.evidence_section_bounds()`が、Evidence見出しの次行から次の`## `見出しの
直前までを範囲として返す。収集、更新、Digest照合はこの範囲だけを対象にする。

`todo_record_generation.verify_reference_digests()`を新設し、更新経路の`default_verify()`は
これを呼ぶ。歴史的なglobal validator`issue_resolution_post_write.validate_todo_reference_digests()`
の責務は拡張も変更もしていない。更新経路からは呼ばなくなった。

範囲外のlinkは、Digestが正しくても誤っていても、収集・更新・照合の対象にしない。候補生成の前後で
範囲外のbytesは完全に同じである。

## 5. RED／GREEN

| 段階 | 結果 |
| --- | --- |
| RED（訂正test追加後） | `9 failed, 20 passed` |
| GREEN（対象test 2 file） | `29 passed` |
| GREEN（公式全test） | `892 passed` |

追加したtestは次の6条件を満たす。

1. Evidence節内2件＋節外1件のfixtureで、収集が内側2件だけになり、候補が範囲外linkのDigestを含めて
   byte不変である。
2. 節外linkだけの改竄では候補生成とscoped verificationが通り、節内linkの改竄は
   `reference_digest_mismatch`で停止しTODO bytesを変えない。
3. legacy／V4両rootからknown ID集合が導出される。
4. root TODOのactive IDを`ISSUE-UNKNOWN-001`に変えると`default_verify()`と
   `run_two_phase_update()`が停止し、二度目のTestを実行せずTODOを元bytesへ復元する。
5. Issue rootのsymlink、未知record_kind、JSON不正、ID重複、ID欠落で停止する。
6. 実repositoryのroot TODOがlegacy正本から`ISSUE-PILOT-TODO-GROWTH-001`を解決して通る。

既存testの期待は緩めていない。`test_default_verification_runs_the_repository_validators`だけは、
更新経路がglobal validatorではなくEvidence節限定の検証を使うという今回の訂正に合わせ、
確認対象の関数名を変えたうえで「global validatorをimportしないこと」の確認を足した。

## 6. 二段確認と実TODOの更新範囲

| 段 | receipt | SHA-256 | status |
| --- | --- | --- | --- |
| 一時（commitしない、repository外） | `<scratchpad>/boundary-repair-temporary-receipt.json` | `aa5526282604ec39bfdf7795f645217e4b0ee58315e9bc3cc0f32cff88742e82` | `passed` |
| 最終（commitする） | `records/development/2026-08-05-record-generation-todo-boundary-repair-green-test-receipt-v1.json` | `ad0f191e0af53a21ab130d9346743d0b214ac56ad6cf958b64ae175535df98df` | `passed` |

`test_summary`、`suite`、`python_version`、`pytest_version`、`fallback_used`、`status`の6 fieldが
**完全一致**した。両段とも
`{"errors": 0, "failed": 0, "passed": 892, "skipped": 0, "total": 892, "xfailed": 0, "xpassed": 0}`。

機械が書き換えたのは**1行だけ**である。

```diff
-- 直近の全Test：venv公式runner `881 passed`、Python 3.9.6、pytest 8.4.2、fallback false
+- 直近の全Test：venv公式runner `892 passed`、Python 3.9.6、pytest 8.4.2、fallback false
```

自由文、link label、link path、link順序、Issue recordは変更していない。全TODOの再描画もしていない。

## 7. 初回GREEN Evidenceの扱い

初回のGREEN Evidence
`records/development/2026-08-05-record-generation-todo-green-evidence-v1.md`と、その最終receipt
`records/development/2026-08-05-record-generation-todo-green-test-receipt-v1.json`は削除も書換えも
していない。境界不足があった初回根拠として**staleのまま履歴に残す**。

TODO最小縦切りの有効な完了根拠は、本訂正Evidenceと訂正最終receiptである。

## 8. 未実施の範囲

- Evidence／Decisionの定型欄への一般化（案B）。
- `render_todo_handoff()`による全TODO再生成。
- 「直近の関連Test」行の自動選定、監査内訳の自動集計。
- Issueのstate変更、Task Contract、Workflow permit、Policy、config、hook、
  Git／shell operation routing（`ISSUE-HTC-C9F6C917`の範囲）。
- `todo_compaction.py`、`issue_resolution_post_write.py`、legacy／V4 Issue recordの変更。
  いずれも触っていない。
