# Codex → Claude：定型記録生成TODO最小縦切りの境界訂正指示

## 誰が何をするか

- **Human**は、`DEC-RECORD-GENERATION-PLAN-001`で承認済みのTODO最小縦切りについて、
  独立確認で判明した2つの実装不足への対応を指示した。
- **Codex**は、不足の再現、正しいauthority、修正範囲、Test先行の順序をこの指示書へ固定する。
- **Claude**は、以下の2欠陥をTest先行で修正し、GREENの意味単位commitを1件作る。

この訂正は既承認の「TODOだけ」「Evidence節の参照」「既存Issue正本を使う」範囲内である。
新しいDecision、Task Contract、Issue state変更、既存commitのrevertは行わない。

## 修正対象と独立再現

対象module：

- `tools/development/todo_record_generation.py`
- `tools/development/todo_update_path.py`
- `tests/test_todo_record_generation.py`
- `tests/test_todo_update_path.py`

### 欠陥1：参照の対象範囲が広すぎる

仕様は「`## 最新のauthority／Evidence`節のMarkdown linkのSHA-256だけを機械管理する」である。
しかし現状の`collect_reference_digests()`はEvidence見出しの存在だけを確認し、document全体のlinkを
収集する。そのため、次の再現でEvidence節外のlinkも収集された。

```text
TODO末尾に別の見出しを追加し、
`- [範囲外参照](docs/current/reviewcompass3-plan-current.md) — SHA-256 <実Digest>`
を置く。
→ `collect_reference_digests()`がこの範囲外pathを27件目として返す。
```

正しい動作は、Evidence見出しの次行から次の`## `見出しの直前までだけを対象とすることである。
範囲外のlinkは、Digestが正しくても誤っていても、収集・更新・この更新経路におけるDigest検証の
対象にしてはならない。範囲外のbytesは候補生成前後で完全に同じでなければならない。

既存の`issue_resolution_post_write.validate_todo_reference_digests()`は歴史的な別経路のglobal validatorである。
この訂正のためにその責務を拡張・変更しない。TODO更新経路は、Evidence節に限定した同等の検証を
`todo_record_generation.py`またはその明確な補助moduleから呼ぶ。

### 欠陥2：active Issueの許可一覧がTODO自身から作られている

現状の`todo_compaction_known_active_ids(document)`は、TODOに書かれたIDをそのまま許可一覧として返す。
次を独立に再現した。

```text
TODOの`ISSUE-PILOT-TODO-GROWTH-001`を`ISSUE-UNKNOWN-001`へ置換する。
→ 自己導出したknown setが`{'ISSUE-UNKNOWN-001'}`になり、compaction validatorが受理する。
```

正しい許可一覧はTODO本文ではなく、project内の既存Issue正本からだけ得る。

- legacy root：`.reviewcompass/workflow/issues/*.json`
  - `record_kind: "issue"`かつ`record_id`を読む。
- V4 root：`.reviewcompass/workflow/issues-v4/*.json`
  - `record_kind: "issue_record"`かつ`issue_id`を読む。

`.gitkeep`は無視する。root直下の通常`.json`だけを読む。symlink、JSON不正、未知record_kind、
IDの欠落／重複／不正は停止する。rglobで別directoryを拾わない。
現在のroot TODOが示す`ISSUE-PILOT-TODO-GROWTH-001`はlegacy rootの正本に存在するため、正しい
loaderへの変更後も正例として通る。

## Test先行で固定する受入条件

実装前に次をTestへ追加し、REDを確認する。既存のTest期待を緩めない。

1. Evidence節内の2 linkと、Evidence節外の同形式linkを持つfixtureを作る。
   `collect_reference_digests()`が内側の2件だけを返し、candidateが範囲外linkの**Digestを含めて**
   byte不変であることを確認する。
2. Evidence節外のlinkだけを改竄しても、この更新経路のcandidate生成とscoped verificationは通る。
   Evidence節内のlink改竄は従来どおり`reference_digest_mismatch`で停止し、TODO bytesを変えない。
3. legacy Issue正本とV4 Issue正本を含むfixtureで、known ID集合が両rootから導出されることを確認する。
4. root TODOのactive IDを`ISSUE-UNKNOWN-001`へ変えると、`default_verify()`と
   `run_two_phase_update()`が停止し、二度目のTestを実行せず、TODOを元bytesへ復元することを確認する。
5. Issue rootのsymlink、未知record_kind、JSON不正、ID重複、ID欠落は停止する。
6. 実repositoryのroot TODOは、修正後にlegacy Issue正本から`ISSUE-PILOT-TODO-GROWTH-001`を解決して
   validatorを通る。

## 実装と証跡

RED確認後に、上記2境界だけを修正する。全TODOを再描画せず、自由文、link label、link path、link順序、
Issue recordは変更しない。

修正後は次の順で実行する。

1. 対象TestをGREENにする。
2. 一時receipt → root TODOの機械更新 → scoped validator・compaction validator・read-back →
   最終receipt、の二段確認を再実行する。
3. 一時／最終receiptの`test_summary`、suite、Python版、pytest版、fallback、statusが一致することを
   機械照合する。
4. 公式全Testを実行する。
5. 次の訂正Evidenceと最終receiptを作成する。

   - `records/development/2026-08-05-record-generation-todo-boundary-repair-green-evidence-v1.md`
   - `records/development/2026-08-05-record-generation-todo-boundary-repair-green-test-receipt-v1.json`

Evidenceには、2つの再現、RED／GREEN、正本Issue root、実TODOの更新範囲、一時／最終summary一致、
全Test結果を記録する。既存GREEN Evidenceは消さず、境界不足があった初回根拠としてstaleにする。

TODOは最終receipt由来の値へ機械更新し、初回GREEN Evidenceをstaleとして履歴に残す旨と、
訂正GREEN Evidenceを有効な完了根拠として記載する。TODOだけの追加commitは作らない。

## 禁止事項と停止条件

- `todo_compaction.py`、`issue_resolution_post_write.py`、legacy／V4 Issue record、Task Contract、
  Policy、config、hook、Git／shell operation routingは変更しない。
- stdout／stderrをTest件数のsourceとして解析しない。
- `git add -A`、`git add .`、push、PR、外部送信、revert、履歴書換えを行わない。
- 既存Issue正本に変更が必要、Issue rootが期待形でない、root TODOの非機械管理部分が変わる、
  二段確認が不一致、原状復帰不能、Task Contract固定sourceが崩れる場合はcommitせず停止して報告する。

## コミットと完了報告

Test、module、root TODO、訂正GREEN Evidence、訂正最終receiptだけを1つのGREEN commitにする。
完了報告はcommitに混ぜず、次へ未追跡で保存する。

`records/session-handoffs/2026-08-05-claude-to-codex-repair-record-generation-todo-boundaries.md`

報告にはcommit SHA、2再現の結果、追加Test、最終summary、一時／最終一致、TODO更新範囲、
初回Evidenceをstaleとしたこと、未実施範囲を記す。
