# Work 4A Rebuild Design v3 Proposal

状態：`approved_for_implementation`
対象：Work 4A Reusable Routine Ledger
承認記録：`DEC-WORK4A-REBUILD-DESIGN-003`

これはv2の外部`DATA_ROOT`参照方式に見つかった設計矛盾を、局所patchではなく参照モデルの改訂として解決する設計である。
Humanの承認によりv2を`superseded_for_implementation`とし、このv3だけを実装の正本とする。

### 改訂履歴

| 版 | 変更 |
| --- | --- |
| 初版 | 設計案の作成。未決事項5点をHuman判断へ提出（旧§19） |
| 第二版 | Organizerの判断を反映。未決事項5点を決定事項へ移行（§19）。`root_overlap`をPolicyのchange classから外し、layout段階の`invalid_layout`として常にfail-closedとする（§11、§12.1） |
| 第三版 | v2残余の処分範囲を訂正。未コミット分の破棄と、commit済みv2試作のrevertを別作業単位に分離する（§16.1、§18-5、§19） |
| 第四版 | Human承認により`approved_for_implementation`へ移行。§18の開始条件を承認済みとして確定（§18） |

## 1. v2の矛盾（再現済みの事実）

v2は次の三つを同時に要求しており、これらは同時に満たせない。

| 出所 | 要求 |
| --- | --- |
| v2 §1（`ref`定義） | すべての`ref`の`path`はproject相対である |
| v2 §4（配置表） | Observation、Index、Candidate Runは`DATA_ROOT`配下（project外）に置く |
| v2 §5（結線） | Operational DecisionはCandidate Runの`ref`を、BaselineはObservationとCandidate Runの`ref`を保存する |

試作moduleでも同じ地点で停止する。`write_operational_decision`が`DATA_ROOT`内のcandidate fileに対して`ref`を作ろうとし、
project脱出検査が`record path escapes project`で拒否する（`tools/development/work4a_rebuild_v2.py`の`_ref`）。
**安全検査が正しく、設計が誤っている。**したがって検査側に例外を作る方向の修正は採らない。

さらにLayout Baseline v3候補（`records/development/2026-08-04-layout-baseline-v3-project-first-candidate.json`）は
`relative_path_policy`で「相対pathはproject artifactに限る、base rootは`project_root`、escapeは拒否」と既に定めている。
v2の矛盾は、この既存規則に反する参照をproject artifactへ持ち込もうとしたことに起因する。

## 2. v3が採る方式（Observation Attestation）

外部観測をproject artifactから直接指すのをやめ、project内に不変の**Observation Attestation（観測証明）**を一枚置き、
これを外部への唯一の橋にする。

```text
DATA_ROOT（project外、Git外、再採取可能）
  Source Observation ─┐
  Candidate Run ──────┤ 内容Digestと最小要約だけをproject内へ写像
                      ▼
PROJECT_ROOT（Git管理、配布先ではread-only）
  Observation Attestation  ← advisory locatorはここにだけ存在する
        ▲            ▲
        │            │ project相対ref
  Operational Human Decision
        ▲
        │ project相対ref
  Baseline ── Entry / Relation / Policy / Source Universe（すべてproject相対ref）
```

不変条件は次のとおりである。

1. Operational Human DecisionとBaselineは`DATA_ROOT`を直接参照しない。参照するのはAttestationだけである。
2. `DATA_ROOT`内の位置情報は、Attestation内の`advisory_locator`にだけ置く。これは正本性の根拠ではなく、
   current Baseline検証の必須条件でもない。
3. `DATA_ROOT`が存在しない配布先やCIでも、project artifactだけでcurrent Baselineを検証できる。
4. `DATA_ROOT`が解決でき、対象fileが存在する場合にだけlocatorを照合する。Digest不一致は停止、file不在は
   `locator_unresolved`として非停止とする。

## 3. v2との相違一覧

| 項目 | v2 | v3 |
| --- | --- | --- |
| `ref`の種類 | 一種類（project相対path前提） | 二種類（project ref／advisory locator）を別schemaにする |
| 外部観測の参照 | Decision・Baselineが`DATA_ROOT`のfileを直接ref | Attestation経由のみ。Decision・Baselineは外部を指さない |
| 外部pathの表現 | project相対（不可能） | 構造化fieldでLayout v3のroot語彙から解決。path文字列にrootやproject IDを埋めない |
| 外部file不在時 | 検証不能または検査を緩める必要 | `locator_unresolved`で非停止。currentは確定できる |
| 外部配置 | `DATA_ROOT/projects/<project_id>/reuse/` | `<runtime_root>/projects/<project_id>/<profile>/data/work4a/`（Layout v3の構造に従属） |
| 判断対象の説明可能性 | 外部fileが消えると説明不能 | Attestationの最小要約とEntry・Decisionで説明可能 |
| 配布先での連続性 | 未定義 | `continuous_fresh`／`content_diverged`／`universe_diverged`を定義。後二者で自動昇格しない |
| Digestのalgorithm表明 | 暗黙 | `digest_algorithm`をrecord fieldとして明示 |
| profile（stable／development） | 未考慮 | Attestationに記録し、異profileのlocatorは照合しない |

v2から**変更せず継承する**のは次である。これらはv3でも正本とする。

- canonical JSON規則とcontent Digestの算出（v2 §1）
- source universe `SRCU-WORK4A-TOOLS-PY-V1`とその除外規則（v2 §2）
- Policy artifactとchange class、`revalidation_required`（v2 §3）
- Entry・Relationのnew-onlyとimmutable（v2 §6）
- current Baselineの導出（連番最大＋全Digest照合、可変pointer fileを作らない）（v2 §6）
- legacy Task Contractの`evidence_insufficient`規則（v2 §7）
- revert mapを実装開始条件とすること（v2 §9、`records/development/2026-08-04-work-4a-v1-revert-map-v1.md`）

## 4. Layout v3への従属

独自のroot語彙を作らない。v3の参照はLayout Baseline v3候補の定義に従属する。

| v3が使う概念 | 従属先 | 値域 |
| --- | --- | --- |
| `root_kind` | `logical_roots`の区分 | `project`（＝`project_root`）または`data`（＝`data_root`） |
| `root_selector` | `project_runtime_layout.root_kinds` | `data`（本Workで使うのはこれだけ） |
| `profile` | `project_runtime_layout.profiles` | `development`または`runtime` |
| 外部pathの組立 | `project_relative_prefix`＋`project_id`＋`profile`＋`root_kind` | `<runtime_root>/projects/<project_id>/<profile>/data/` |
| project相対pathの可否 | `relative_path_policy` | `project_artifacts_only`、base rootは`project_root`、escapeは拒否 |
| 絶対pathの保存 | `project_manifest.absolute_path_storage` | 禁止 |

したがってadvisory locatorは、runtime root、`projects`接頭辞、project ID、profile、root kindを**path文字列に含めない**。
これらは構造化fieldとして持ち、解決はLayout v3のresolverに委ねる。文字列前置一致による検査に依存しないため、
別projectのpathを紛れ込ませる余地が構造的に無くなる。

## 5. Project ref schema

Decision、Baseline、Entry、Relation、Policy、Source Universe、Attestationを指すときは、この一種類だけを使う。

```json
{
  "root_kind": "project",
  "record_kind": "work4a_ledger_entry",
  "record_id": "RRL-BUNDLE-DIGEST",
  "version": 2,
  "relative_path": ".reviewcompass/reuse/reusable-routine-ledger/entries/rrl-bundle-digest--v2.json",
  "digest_algorithm": "sha256",
  "file_sha256": "<64桁小文字hex>",
  "content_digest": "<64桁小文字hex>"
}
```

- `path`は`relative_path`へ改名する。base rootは常に`project_root`である。
- `content_digest`を併記するのは、整形差による不一致と改竄を区別して報告するためである。どちらも停止させるが、
  fail-closed codeを分ける。
- v2の`development_policy_ref`のように`path`だけを持つ簡略参照は廃止し、この形へ統一する。

## 6. Advisory locator schema

Attestationの中にだけ現れる。ほかのrecordがこの形を持つことを禁止する。

```json
{
  "root_kind": "data",
  "root_selector": "data",
  "profile": "development",
  "project_id": "reviewcompass3",
  "relative_path": "work4a/candidates/<candidate_run_id>.json",
  "digest_algorithm": "sha256",
  "file_sha256": "<64桁小文字hex>",
  "evidentiary_role": "advisory_locator"
}
```

- `relative_path`は`<runtime_root>/projects/<project_id>/<profile>/data/`からの相対POSIX pathである。
  絶対path、`..`、drive文字、UNC、制御文字を禁止する。
- `evidentiary_role`は`advisory_locator`固定とする。この値以外は拒否する。
- **この情報は「どこで観測したか」の記録であり、正しさの根拠ではない。**正しさの根拠は`content_digest`である。

## 7. Observation Attestation schema

配置：`<PROJECT_ROOT>/<artifact_roots.reuse>/reusable-routine-ledger/attestations/obsatt-<snapshot_id>--v1.json`

```json
{
  "record_kind": "work4a_observation_attestation",
  "schema_version": 1,
  "digest_algorithm": "sha256",
  "attestation_id": "OBSATT-<snapshot_id>",
  "attestation_version": 1,
  "project_id": "reviewcompass3",
  "profile": "development",
  "source_universe_id": "SRCU-WORK4A-TOOLS-PY-V1",
  "source_universe_version": 1,
  "source_universe_ref": { "root_kind": "project", "…": "project ref" },
  "policy_ref": { "root_kind": "project", "…": "project ref" },
  "source_content_id": "<64桁小文字hex>",
  "observation": {
    "record_kind": "work4a_source_observation",
    "snapshot_id": "<64桁小文字hex>",
    "content_digest": "<64桁小文字hex>",
    "head": "<40桁hex>",
    "tool_version": "v3",
    "captured_at": "2026-08-04T20:00:00+09:00",
    "source_file_count": 41,
    "advisory_locator": { "…": "advisory locator" }
  },
  "candidate_run": {
    "record_kind": "work4a_candidate_run",
    "candidate_run_id": "<64桁小文字hex>",
    "observation_snapshot_id": "<64桁小文字hex>",
    "source_content_id": "<64桁小文字hex>",
    "content_digest": "<64桁小文字hex>",
    "advisory_locator": { "…": "advisory locator" }
  },
  "candidate_summary": {
    "candidate_count": 128,
    "symbol_id_list_digest": "<64桁小文字hex>",
    "classification_counts": { "reuse": 12, "extend": 3, "merge": 1, "split": 0, "new": 112 },
    "sensitive_content_included": false
  },
  "supersedes_attestation": null,
  "content_digest": "<64桁小文字hex>"
}
```

### 7.1 最小要約の規則

- `symbol_id_list_digest`は、候補symbol IDを昇順に並べたJSON配列に対するcanonical Digestとする。
  外部fileが消えた後でも、再採取した候補一覧が当時と同一かを機械照合できる。
- `classification_counts`のkeyはPolicyの閉じたdisposition語彙とし、語彙外keyは拒否する。
- 要約にsource本文、file path列、symbol名の実体、機密情報を入れない。`sensitive_content_included`は常に`false`であり、
  `true`のrecordは書込みも読込みも拒否する。
- **人が判断した対象そのものはDecisionとEntryに残る。**要約は「その判断が置かれた文脈（候補全体の規模と同一性）」を
  説明するためのものであり、候補一覧の代替ではない。この限界は§16に明記する。

### 7.2 supersedes

配布先や別環境で採り直したAttestationは、`supersedes_attestation`に旧Attestationの`attestation_id`と`content_digest`を持つ。
これにより、どの環境のどの観測から連続しているかがIDの連鎖で追える。

## 8. Operational Human Decision schema（改訂）

配置：`<PROJECT_ROOT>/<artifact_roots.design_decisions>/`（v2 §4から変更しない）

```json
{
  "record_kind": "work4a_operational_decision",
  "schema_version": 1,
  "digest_algorithm": "sha256",
  "decision_id": "DEC-WORK4A-OPS-001",
  "attestation_ref": { "root_kind": "project", "…": "project ref" },
  "approved_candidate_run_id": "<64桁小文字hex>",
  "approved_candidate_content_digest": "<64桁小文字hex>",
  "approved_source_content_id": "<64桁小文字hex>",
  "approved_targets": [
    { "symbol_id": "tools.development.work4a_rebuild_v3:append_baseline", "disposition": "reuse" }
  ],
  "human_id": "kenoogl",
  "decided_at": "2026-08-04T21:00:00+09:00",
  "content_digest": "<64桁小文字hex>"
}
```

`approved_*`の三つはAttestationにも存在するが、二重の正本ではない。**人が何に同意したかの明示的な宣言**であり、
Attestation側の値と食い違えば停止させるための相互検査である。`candidate_ref`（外部を直接指すfield）は廃止する。

## 9. Baseline schema（改訂）

配置：`<PROJECT_ROOT>/<artifact_roots.reuse>/reusable-routine-ledger/ledger-baseline--v<n>.json`（v2 §6から変更しない）

```json
{
  "record_kind": "work4a_ledger_baseline",
  "schema_version": 1,
  "digest_algorithm": "sha256",
  "baseline_id": "RRL-BASELINE",
  "baseline_version": 3,
  "project_id": "reviewcompass3",
  "source_universe_id": "SRCU-WORK4A-TOOLS-PY-V1",
  "source_universe_version": 1,
  "source_content_id": "<64桁小文字hex>",
  "universe_ref": {}, "policy_ref": {}, "attestation_ref": {}, "decision_ref": {},
  "prior_baseline_ref": {},
  "entry_refs": [], "relation_refs": [],
  "content_digest": "<64桁小文字hex>"
}
```

Baseline内に現れる参照はすべてproject refである。**Baseline JSONに絶対path、`..`、advisory locatorが現れてはならない。**
これは文字列検査として受入testに含める（§17 A1）。

## 10. 配置規則

| record | 配置 | Git | 手編集 |
| --- | --- | --- | --- |
| Source Observation、Index、Candidate Run | `<runtime_root>/projects/<project_id>/<profile>/data/work4a/` | 対象外 | 禁止 |
| Observation Attestation | `<artifact_roots.reuse>/reusable-routine-ledger/attestations/` | 管理 | 禁止。writerのみ |
| Operational Human Decision | `<artifact_roots.design_decisions>/` | 管理 | 人が作成・承認 |
| Entry、Relation、Baseline | `<artifact_roots.reuse>/reusable-routine-ledger/` | 管理 | 禁止。writerのみ |
| Historical Contract Status | `<artifact_roots.contracts>/historical-status/` | 管理 | 禁止。Human Decision必須 |
| Continuity Receipt | `<runtime_root>/projects/<project_id>/<profile>/data/work4a/receipts/` | 対象外 | 禁止 |
| Development Decision、revert map、legacy inventory | `records/development/` | 管理 | 開発証跡 |

Continuity Receiptをproject内に置かないのは、Layout v3の`environment_isolation`が
`shared_root: project_root_read_only_for_stable`、`cross_write: reject`としているためである。
配布先（stable）での連続性検証は読み取り専用の検査であり、project_rootへ書いてはならない。

## 11. Validation順序

順序に意味がある。前段が通らなければ後段を評価しない。**外部照合は必ず最後に置く。**

| phase | 内容 | 外部依存 |
| --- | --- | --- |
| P0 | Project Manifestの読込、`schema_version`、`project_id`の確認 | なし |
| P1 | Layout解決。`artifact_roots`の解決、root安全性、root重なりの検査（`invalid_layout`はここで停止し、P2のPolicy読込へ進まない） | なし |
| P2 | Source Universe recordとPolicy recordの読込・Digest照合・change class判定 | なし |
| P3 | Baseline series（連番・欠番・重複）→ current候補の決定 | なし |
| P4 | current候補の全project refの検証（Attestation、Decision、Entry、Relation、Policy、Universe、prior Baseline） | なし |
| P5 | Attestation内部の同一性整合（observation／candidate_run／summary／project_id／universe） | なし |
| P6 | Decisionの相互検査（`approved_*`とAttestationの一致） | なし |
| P7 | advisory locatorの照合（解決でき、同一profile、fileが存在する場合のみ） | あり・非必須 |
| P8 | freshness（source再採取、`source_content_id`比較、連続性判定） | source読取のみ |
| P9 | 書込み時のnew-only、原子的書込み、書込み後の読み戻し照合 | なし |

**P0からP6までで、current Baselineは確定できる。**P7が実行できなくても、実行して不在だったとしても、current判定は変わらない。
これが「配布先・CIでproject artifactだけで検証できる」の実体である。

## 12. Fail-closed条件

| code | 条件 | 挙動 |
| --- | --- | --- |
| `invalid_manifest` | Manifestが読めない／`schema_version`未知／`project_id`空 | 停止 |
| `unsafe_root` | 解決後のartifact rootがPROJECT_ROOTの真の子孫でない | 停止 |
| `root_overlap` | `DATA_ROOT`がPROJECT_ROOT配下、またはPROJECT_ROOTが`DATA_ROOT`配下 | 停止（分類は`invalid_layout`。§12.1） |
| `unknown_root_kind` | `root_kind`／`root_selector`／`profile`が閉じた語彙の外 | 停止 |
| `path_traversal` | `relative_path`が絶対、`..`を含む、drive文字・UNC・制御文字を含む | 停止 |
| `root_escape` | 実体解決後にbase rootの真の子孫でない | 停止 |
| `non_regular_file` | symbolic linkまたは通常fileでない | 停止 |
| `missing_record` | project refの対象fileが存在しない | 停止 |
| `digest_mismatch` | `file_sha256`不一致 | 停止 |
| `content_digest_mismatch` | 再計算した`content_digest`が記録値と不一致 | 停止 |
| `identity_mismatch` | `record_kind`／`record_id`／`version`が申告と不一致 | 停止 |
| `unknown_field` | schema外のfieldが存在する | 停止 |
| `foreign_project_data` | Attestationまたはlocatorの`project_id`がManifestと不一致 | 停止 |
| `unlinked_candidate` | `candidate_run.observation_snapshot_id`が`observation.snapshot_id`と不一致 | 停止 |
| `content_identity_mismatch` | observation／candidate_run／Attestationの`source_content_id`が三者一致しない | 停止 |
| `summary_vocabulary_violation` | `classification_counts`にPolicy語彙外のkey、または`sensitive_content_included: true` | 停止 |
| `decision_candidate_mismatch` | Decisionの`approved_*`がAttestationと不一致 | 停止 |
| `stale_observation_reuse` | 新Baseline作成時に再採取した`source_content_id`がAttestationの値と不一致 | 停止 |
| `immutable_violation` | 既存Entry／Relation／Attestation／Baselineのfile bytesが変化、または既存pathへの書込み | 停止 |
| `baseline_series_broken` | Baseline連番に欠番・重複がある | 停止 |
| `policy_revalidation_required` | change classが`security`／`authority`／`irreversible` | 停止 |
| `data_root_escape` | locator解決後の実体が`DATA_ROOT`の子孫でない | 停止 |
| `observation_tampered` | locatorの対象fileが存在するのに`file_sha256`不一致 | 停止 |
| `write_verification_failed` | 書込み後の読み戻しでDigest不一致 | 停止 |
| `partial_write_detected` | 途中生成物を検出 | 停止 |
| `locator_unresolved` | `DATA_ROOT`が解決できない、または対象fileが存在しない | **非停止・記録のみ** |
| `locator_profile_mismatch` | locatorの`profile`が現在のprofileと異なる（照合を行わない） | **非停止・記録のみ** |

非停止は上記二つだけである。それ以外はすべて停止し、部分的な書込みを残さない。

### 12.1 `invalid_layout`分類

`root_overlap`はPolicyのchange class（`ordinary`／`security`／`authority`／`irreversible`）に**含めない**。
rootの重なりは「不可逆操作」ではなく、起動前に拒否すべき危険な構成だからである。

- 分類名は`invalid_layout`とし、Policyの語彙から独立した別枠として定義する。
- 判定はP1（Layout解決）で行う。Policy recordを読む前に停止するため、Policyの内容や承認状態に左右されない。
- Policy artifactが存在しない、読めない、またはHumanが未承認であっても、この停止は常に有効である。
- Human承認やrisk受容によって迂回できない。`revalidation_required`のような再検証経路を持たない。

この決定は`root_overlap`だけを対象とする。`unsafe_root`など他のlayout段階の条件の分類は本決定では変更せず、
現行のまま（無条件停止）とする。

## 13. Freshnessと配布先での連続性

配布先にはproject artifact（read-only）だけがあり、`DATA_ROOT`は空である。

1. project artifactだけでcurrent Baselineを決める（P0〜P6）。
2. `universe_ref`からsource universe定義を読む。
3. 配布先のsourceから採り直し、`source_content_id'`を計算する。
4. 判定は次の三値とする。

| 判定 | 条件 | 効力 |
| --- | --- | --- |
| `continuous_fresh` | universe（IDとversion）一致、かつ`source_content_id'`がBaselineの値と一致 | 過去のDecisionは有効。Baseline更新不要 |
| `content_diverged` | universe一致、`source_content_id'`が不一致 | 過去のDecisionは履歴として有効。現行の再利用許可には使えない |
| `universe_diverged` | universeのIDまたはversionが不一致 | 全Baselineを`stale`とする（v2 §2を継承） |

5. `content_diverged`と`universe_diverged`では、**新しいCandidate Runと新しいOperational Human Decisionなしに
   Baselineを進めてはならない。**自動昇格を禁止する。
6. HEADの差、`captured_at`の古さ、`DATA_ROOT`の物理的な存在は、いずれも判定に使わない。
   `tool_version`がPolicyの許容集合外の場合だけ`policy_revalidation_required`とする。
7. 判定結果はContinuity Receiptとして`data` root配下へnew-only保存する（§10）。`locator_unresolved`と
   `locator_profile_mismatch`はreceiptの注記として残す。

## 14. 参照してよい過去の観測の範囲

- 新Baselineが参照できるAttestationは、universeが現行定義と一致し、かつ`source_content_id`が
  **その場で採り直した値**と一致するものだけである。
- 同一Attestationを複数のBaselineが再参照してよい。これが「HEADだけの差では古くならない」の実体である。
- どのAttestationにも束ねられていない、`DATA_ROOT`に存在するだけの観測は参照できない（v2 §5-5を継承し、Attestation経由で機械化する）。

## 15. legacy Task Contract

v2 §7を変更せず継承する。inventoryを`records/development/`へ記録し、根拠が一つでも欠ける契約は
`evidence_insufficient`で停止する。v3の最初のactual artifactでもlegacy Contractをhistoricalへ移行しない。
受入範囲は、欠落した根拠を拒否する負例までとする。

## 16. 未コミットのv2修正を採用しない理由

現在`tools/development/work4a_rebuild_v2.py`に未コミットの修正があり、`tests/test_work4a_rebuild_v2_contract.py`が未追跡で存在する。
v3はこれらを根拠にせず、変更もしない。理由は次の五点である。

1. **前提そのものがv3で置き換わる。**未コミット修正は「すべての`ref`はproject相対」というv2の公理の上に、
   脱出検査と全ref検証を追加したものである。v3はその公理を二種類の参照へ分割する。このまま引き継げば、
   外部参照を通すために脱出検査へ例外分岐を入れることになり、今回禁止された継ぎ足しそのものになる。
2. **矛盾を解消していない。**この修正はむしろ矛盾を露出させた変更であり、`write_operational_decision`は
   依然として`DATA_ROOT`のpathに対して`_ref`を呼ぶため、実行すると必ず停止する。
3. **絶対path保存が残っている。**`development_policy_ref`は渡されたpath文字列をそのまま保存しており、
   project相対である保証がない。Layout v3の`project_manifest.absolute_path_storage: prohibited`と
   `relative_path_policy`に反する。v3ではこの簡略参照を廃止し、project refへ統一する（§5）。
4. **外部配置がLayout v3に反している。**観測の配置が`DATA_ROOT/projects/<project_id>/reuse/`であり、
   Layout v3が定める`projects/<project_id>/<profile>/<kind>/`のprofileとkindの階層を欠く。
   参照形式だけの修正では是正されない。
5. **開始条件に反する。**v2 §10は、承認と開始条件がそろうまで試作moduleを拡張しないことを求めている。
   未コミット修正はその拡張にあたる。

したがって、これらの未コミット変更の破棄または保持はHumanの判断事項とし、v3設計はその内容に依存しない。

### 16.1 v2残余の処分範囲

v2の試作には、未コミットのものとcommit済みのものがある。両者は復旧可能性が異なるため、**同じ承認・同じ操作にまとめない**。

| 対象 | 状態 | 処分 | 復旧可能性 |
| --- | --- | --- | --- |
| `tools/development/work4a_rebuild_v2.py`の未コミット差分 | 未コミット | 破棄済み（Humanが実施） | 復元不能 |
| `tests/test_work4a_rebuild_v2_contract.py` | 未追跡 | 破棄済み（Humanが実施） | 復元不能 |
| `tools/development/work4a_rebuild_v2.py`本体（`33218e0`） | commit済み | 別作業単位でrevert | Git historyに残る |
| `tests/test_work4a_rebuild_v2_e2e.py`（`df2bd3c`） | commit済み | 別作業単位でrevert | Git historyに残る |

commit済みv2試作のrevertは、v1と同じ規律で行う。historyを書き換えず、revert commitで戻し、
**revert対象、保持対象、理由を対応表**として`records/development/`へnew-only保存する
（`records/development/2026-08-04-work-4a-v1-revert-map-v1.md`と同じ形式）。
一括resetを使わず、実行時に対象commitを再確認する。

commit済みv2をrevertするまでの間、`work4a_rebuild_v2.py`と`test_work4a_rebuild_v2_e2e.py`は
実装正本でもactual artifactの根拠でもない。v3実装はこれらのmoduleを参照・import・拡張しない。

## 17. v3 E2E acceptance

以下を同一のtest群としてREDから確認する。途中の一部をもって完了と報告しない。

**A. 参照モデル**
- A1 `DATA_ROOT`の候補からAttestationを作り、Decision→Baselineまでproject refだけで連鎖が閉じる。
  Baseline JSONに絶対path、`..`、advisory locatorが一つも現れない（文字列検査）。
- A2 Decisionが外部pathを直接refしようとすると拒否される（`candidate_ref`相当のfieldは`unknown_field`）。

**B. 外部非依存**
- B1 `DATA_ROOT`を丸ごと削除しても、current Baselineの決定と検証が成功し、receiptに`locator_unresolved`が残る。
- B2 profileが異なるlocatorは照合されず、`locator_profile_mismatch`として非停止で記録される。

**C. 外部照合**
- C1 `DATA_ROOT`のcandidate fileを改竄すると`observation_tampered`で停止する。
- C2 別`project_id`を指すlocator、または`project_id`不一致のAttestationは`foreign_project_data`で停止する。
- C3 locatorの解決先が`DATA_ROOT`の外を指す場合は`data_root_escape`で停止する。

**D. path安全性**
- D1 `..`を含む相対path、絶対path、symbolic linkを、それぞれ`path_traversal`／`root_escape`／`non_regular_file`で拒否する。
- D2 `DATA_ROOT`をPROJECT_ROOT配下に設定すると`root_overlap`で拒否する。Policy artifactが存在しない状態でも
  P1で停止し、Policyのchange class判定に到達しないことを併せて確認する。

**E. 同一性と鮮度**
- E1 source変更後に古いAttestationを再利用して新Baselineを作ろうとすると`stale_observation_reuse`で停止する。
- E2 source無変更でHEADだけを変えた再採取は`continuous_fresh`になる。
- E3 source内容の変更は`content_diverged`、universe定義の変更は`universe_diverged`になり、
  いずれも新Decisionなしに新Baselineを作れない。
- E4 Attestation内部の`source_content_id`が三者一致しない場合は`content_identity_mismatch`で停止する。
- E5 Decisionの`approved_*`を書き換えると`decision_candidate_mismatch`で停止する。

**F. 台帳の不変性**
- F1 新Entry一件と新Relation一件を追加しても、既存Entryと既存Relationの`file_sha256`が変わらない。
- F2 Baselineの欠番・重複は`baseline_series_broken`で停止する。
- F3 書込み途中で失敗させても何も書かれない（`partial_write_detected`が発生せず、部分生成物も残らない）。

**G. Policyとlegacy**
- G1 Policy artifactまたはOperational Human Decisionが無いBaseline書込みを拒否する。
- G2 `security`／`authority`／`irreversible`のPolicy変更は`policy_revalidation_required`で停止する。
- G3 creation Policy Digestまたはcreation commitが欠けるlegacy Contractは`completed_historical`を拒否し、
  `evidence_insufficient`だけを許可する。

**H. 要約**
- H1 `classification_counts`にPolicy語彙外のkeyがある、または`sensitive_content_included: true`のAttestationは
  `summary_vocabulary_violation`で拒否する。
- H2 候補一覧を再採取して`symbol_id_list_digest`が一致することを確認できる。

actual artifactは、このtest群がGREENで、初回Observationと候補を機械生成し、対象routineとdispositionを
Humanが承認した後にだけ作る。

## 18. 実装開始条件

`DEC-WORK4A-REBUILD-DESIGN-003`により、次はすべて充足した。

1. 本v3設計のHuman承認とv2の`superseded_for_implementation`化。`完了`
2. §19の未決事項に対する判断。`完了`（Organizer決定を§19へ反映済み）
3. Policy artifactへの検証結果語彙（fail-closed code）とdisposition語彙の追加承認。`完了`
   `invalid_layout`はPolicy語彙の外にあり、この承認の対象に含めない（§12.1）。
4. `root_kind`／`root_selector`／`profile`をLayout v3の語彙と解決規則へ従属させることの承認。`完了`
5. 未コミットv2修正と未追跡testの破棄。`完了`（Humanが実施済み。§16.1）
   commit済みv2試作のrevertはこの条件に含めない。別作業単位として§16.1の規律で行う。

revert mapはv2 §9の要求どおり既に固定済みであり（`records/development/2026-08-04-work-4a-v1-revert-map-v1.md`）、
v3では新たにcommit済みv2試作のrevert mapを作る。

### 18.1 自律実行の範囲と停止条件

承認済み設計の範囲では、実装途中の細かな判断で停止せず自律実行する。次の場合だけは局所patchを行わず停止して報告する。

- 設計レベルの矛盾（v2で起きた形の、設計要求どうしが同時に満たせない状態）
- security、authority、不可逆操作に影響する問題
- actual artifactの対象routine選定とHuman disposition
- 破棄、revert、外部`DATA_ROOT`の初期化（対象と影響を示して承認を待つ）

## 19. 決定事項（初版の未決5点）

Organizerの判断により、初版の未決事項は次のとおり決定した。決定内容は本文へ反映済みである。

| # | 論点 | 決定 | 反映先 |
| --- | --- | --- | --- |
| 1 | 候補symbol ID一覧の保存 | 一覧の実体は保存せず、Digestと件数だけをAttestationへ持つ。判断対象はDecisionの`approved_targets`とEntryのsymbol bindingに残るため十分とする | §7.1（変更なし） |
| 2 | `root_overlap`の分類 | Policyのchange classに入れない。別枠の`invalid_layout`として、layout段階で常にfail-closedとする | §11 P1、§12、§12.1、§17 D2 |
| 3 | Continuity Receiptの配置 | `data` rootへ保存する。Layout resolverでprofileを確定し、stableがproject_rootへ書かないことを守る | §10、§13-7（変更なし） |
| 4 | v2の扱い | v3承認時に`superseded_for_implementation`とし、履歴として保持する | §18-1（変更なし） |
| 5 | v2残余の処分 | 未コミット分と未追跡testは破棄する（実施済み）。commit済みv2試作は、対象commitを確認したうえで別作業単位でrevertし、対応表を残す。破棄とrevertを同じ承認・同じ操作に混ぜない | §16、§16.1、§18-5 |

決定2だけが初版からの設計変更である。他の3点は初版の内容を追認したものであり、本文の技術内容は変わっていない。

決定5は第二版から範囲を訂正した。第二版までは処分対象を未コミット分だけと記述していたが、
commit済みのv2試作module（`33218e0`）と受入test（`df2bd3c`）が残る点を見落としていた。
処分対象が未コミット分に限られていると、誤った直接外部参照モデルを実装したcommit済みcodeが残り、
再利用される余地はむしろそちらに残る。第三版でこれを§16.1として訂正した。

## 20. 現在の停止点

v3は`approved_for_implementation`であり、§18の開始条件はすべて充足した。

次の作業単位は、commit済みv2試作（`33218e0`の`tools/development/work4a_rebuild_v2.py`、
`df2bd3c`の`tests/test_work4a_rebuild_v2_e2e.py`）のrevert対象を提示し、Humanのrevert承認を得ることである。
その後、§17 A〜HのRED testを固定し、GREEN、全test、commitまで進める。
