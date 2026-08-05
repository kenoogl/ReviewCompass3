# Work 5A Provenance閉包不整合の修正設計提案

状態：`awaiting_human_approval`
対象：`tools/task_contract/`の`provenance_verdict`と`accepted_artifact`
関連commit：`9e8cf00`（受理record作成）、`cee88d7`（Work 5A実装）
発見者：Codexの独立照合

**これはDecision recordではない。**承認までrevert、実装、test変更、受理recordの再作成を行わない。

## 1. 事実

`9e8cf00`で作成した`PV-TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V1`の最終edgeは次である。

```json
{ "from": "human_decision", "to": "provenance_verdict",
  "to_digest": "a240921a70a40837efa2d45ee83def0059c125a2a343b7eb415841ddce65d8af" }
```

`a240921a…`は`human_decision`のDigestであり、`provenance_verdict`自身のDigest`7975c761…`ではない。
`to`が名指しするrecordと`to_digest`が指すrecordが一致しない。

実装（`tools/task_contract/execution.py`の`verify_provenance`）は、chainの最後に
`from: human_decision`／`to: provenance_verdict`のedgeを足し、その`to_digest`へ
`human_decision["content_digest"]`を入れている。

## 2. 根本原因

**値の写し間違いではなく、構造上不可能な要求を置いたことが原因である。**

recordのDigestは自分自身の内容から計算する。`provenance_verdict`が自分のDigestを内部の
`to_digest`へ入れると、内容が変わりDigestも変わる。自己参照は不動点になり成立しない。
実装はこの不可能を回避するため、名前だけ`provenance_verdict`とし、値に上流のDigestを入れた。

検出されなかった理由は二つある。

- 実装testは辺の本数（`len(edges) >= 9`）と`to`の名称だけを見ており、両端のidentityとDigestの
  一致を照合していない。
- 受理時の読み戻し照合（`9e8cf00`）は、上流7 record分のedge Digestは照合したが、
  最終edgeの宛先Digestを照合対象に含めていなかった。

したがって`9e8cf00`の`provenance_verdict: verified`と`accepted_artifact`は、
現時点で正本として使わない。**Humanの承認判断そのものは有効であり、失われていない。**

## 3. 循環を作らないrecord構造

### 3.1 原則

- `provenance_verdict`は、検証対象の上流record群（`human_decision`を含む）だけを参照する。
- **`provenance_verdict`自身へ向かうedgeを、そのrecord内容へ含めない。**
- 閉包は下流recordが担う。`accepted_artifact`が`provenance_verdict`と`human_decision`を参照する。
- edgeの両端は、必ず既存recordを指す。自己参照（`from == to`、または端点が自recordの場合）を許さない。

この方向は既存の設計と同じである。下流が上流を参照する形だけを使い、上流が下流を先取りしない。

### 3.2 `provenance_verdict`の形

edgeの両端を`record_ref`にする。名称とDigestを別fieldに分けないため、
「名前と値が別recordを指す」という不整合の種類自体が構造から消える。

```json
{
  "record_kind": "provenance_verdict",
  "record_id": "PV-<contract id>",
  "record_version": 1,
  "status": "verified",
  "verified_nodes": [
    { "node_role": "requirement_binding", "record_kind": "requirement_binding",
      "record_id": "RB-...", "record_version": 1,
      "digest_algorithm": "sha256", "content_digest": "<digest>" }
  ],
  "verified_edges": [
    { "edge_kind": "precedes",
      "from": { "node_role": "requirement_binding" },
      "to":   { "node_role": "review_task_contract" } }
  ],
  "closure": {
    "terminal_node_role": "human_decision",
    "self_edge_present": false,
    "closed_by": "accepted_artifact"
  },
  "content_digest": "<digest>"
}
```

- `verified_nodes`は9件。`requirement_binding`、`review_task_contract`、`compile_verdict`、
  `context_manifest`、`workflow_permit`、`finding_set`、`conformance_verdict`、
  `final_challenge_verdict`、`human_decision`。
- `verified_edges`は8件。node列の隣接だけを結ぶ。**9件目（自分自身への辺）を作らない。**
- edgeは`node_role`だけで両端を指す。identityとDigestは`verified_nodes`が一元的に持つ。
  同じrecordを二度書かないため、名前とDigestが食い違う余地が無い。
- `closure`で、終端nodeが`human_decision`であること、自己辺が無いこと、
  閉包は`accepted_artifact`が担うことを明示する。

もし`to`と`to_digest`を併記する平坦な形を残す場合は、両者が同一の既存recordを指すことを
validatorが毎回照合し、端点が`provenance_verdict`自身になる形を禁止する。
設計者の推奨は上記の`record_ref`方式である。不整合の種類を構造から消せるためである。

### 3.3 `accepted_artifact`の形

変更しない。`provenance_verdict`と`human_decision`を`record_ref`で参照する後続recordのままとする。
これが唯一の閉包点である。

## 4. 検証規則

`verified`は、次の全照合を通過した後だけ発行する。一つでも満たさなければfail-closedで停止する。

| # | 規則 | 停止code |
| --- | --- | --- |
| V1 | 必須node 9件が過不足なく存在する。重複しない | `provenance_node_missing` / `provenance_node_duplicated` |
| V2 | 各nodeの`record_kind`が期待と一致する | `provenance_node_kind_mismatch` |
| V3 | 各nodeの`record_id`と`record_version`が実recordと一致する | `provenance_node_identity_mismatch` |
| V4 | 各nodeの`content_digest`が実recordのDigestと一致する | `provenance_node_digest_mismatch` |
| V5 | 必須edge 8件が過不足なく存在し、順序が一致する | `provenance_edge_missing` / `provenance_edge_unexpected` |
| V6 | 各edgeの両端`node_role`が`verified_nodes`に存在する | `provenance_edge_endpoint_unresolved` |
| V7 | `from == to`のedgeが無い | `provenance_self_reference` |
| V8 | 端点に`provenance_verdict`が現れない | `provenance_self_reference` |
| V9 | `human_decision`の`target_digest`が`context_manifest`のDigestと一致する | `decision_digest_mismatch` |
| V10 | Conformance、Final Challenge、Human decisionのownerが三者とも異なる | `owner_separation_violated` |

**辺の本数だけでは判定しない。**各edgeの両端のidentityとDigestを照合する。

redactした`source_snapshot`と`context_manifest`は、保存物からDigestを再計算できない。
V4はこの二recordについて、記録した`unredacted_content_digest`と、
それを参照する下流recordの参照Digestの一致で代替する。代替であることをrecordへ明示する。

`accepted_artifact`は、`provenance_verdict.status == "verified"`かつ
`human_decision.decision == "approved"`かつ両者のDigest参照が一致する場合だけ作る。

## 5. TDD受入条件

正常経路に加え、次の負例をすべてREDで固定してから実装する。

### 正常例

- P1：正しいchainから`verified`と9 node・8 edgeが得られる。自己辺が無い。
- P2：`accepted_artifact`が`provenance_verdict`と`human_decision`を参照して作られる。

### 負例

- N1：**最終edgeの宛先Digestが`human_decision`のまま**（今回の不整合そのもの）→ 拒否。
- N2：edgeの名称だけ差替え（node_roleを別のものへ）→ 拒否。
- N3：nodeの`record_kind`差替え → 拒否。
- N4：nodeの`record_id`差替え → 拒否。
- N5：nodeの`content_digest`差替え → 拒否。
- N6：自己参照の導入（`from == to`、または端点が`provenance_verdict`）→ 拒否。
- N7：必須node欠落、node重複 → 拒否。
- N8：必須edge欠落、余分なedge追加 → 拒否。
- N9：`human_decision`の`target_digest`不一致 → 拒否。
- N10：**誤った`provenance_verdict`から`accepted_artifact`を作れない** → 拒否。
- N11：`9e8cf00`の実recordを入力にすると拒否される（回帰の実データ負例）。

N11は、今回の誤記録そのものを固定入力として使い、新しいvalidatorが拒否することを確認する。
実データによる回帰防止であり、誤記録を正本として扱うものではない。

## 6. 既存の誤記録の扱い

### 6.1 原則

- `9e8cf00`をhistory rewriteしない。revertもしない。
- 誤ったrecordを削除・上書きしない。
- 無効であることを、new-onlyの別recordで宣言する。

### 6.2 無効化record

`records/development/`へ次をnew-onlyで作る。

```json
{
  "record_kind": "record_invalidation",
  "invalidation_id": "INV-WORK5A-PROVENANCE-CLOSURE-001",
  "invalidated": [
    { "record_kind": "provenance_verdict", "record_id": "PV-TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V1",
      "content_digest": "7975c761...", "outcome": "invalidated_not_authoritative" },
    { "record_kind": "accepted_artifact", "record_id": "AA-CM-TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V1",
      "content_digest": "6c4c690a...", "outcome": "invalidated_not_authoritative" }
  ],
  "containing_commit": "9e8cf00",
  "reason": "provenance_verdictの最終edgeでtoとto_digestが別recordを指す。自己参照は構造上成立しない。",
  "human_approval_status": "unchanged"
}
```

無効化の対象は`provenance_verdict`と`accepted_artifact`の二件だけとする。
上流9 recordと`human_decision`には不整合が無いため、無効化しない。

### 6.3 Human承認の再束縛

Humanの承認判断は有効であり、失われていない。再束縛には二案がある。

**案A（推奨）：既存の`human_decision` recordをそのまま使う。**

- `HD-TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V1`（`a240921a…`）は検証を通り、不整合が無い。
- 新しい`provenance_verdict`は、この既存recordをnodeとして参照する。
- 決定時刻`2026-08-05T09:40:20+09:00`と決定内容が保存され、判断が一度であった事実も保たれる。

**案B：新しい`human_decision` recordを作る。**

- 作る場合、**同一の承認を二度行ったように見えてはならない。**新recordは
  `supersedes`で旧recordを指し、`original_decided_at`と「同一のHuman承認に基づく再束縛であり、
  二度目の判断ではない」旨を明記する必要がある。
- 決定時刻が新しくなるため、来歴上の判断回数が実態と食い違う危険がある。

設計者の推奨は案Aである。誤りは`provenance_verdict`の構造にあり、`human_decision`には無いためである。

## 7. 実施単位の分割

各単位は独立してコミットし、完了済み単位を未コミットのまま次へ進まない。

| # | 単位 | 停止条件 | Human承認 |
| --- | --- | --- | --- |
| 1 | 本設計の承認 | — | **必要** |
| 2 | 誤記録の無効化record作成 | 対象Digestが実recordと不一致なら停止 | 不要（承認済み設計の範囲） |
| 3 | N1〜N11とP1〜P2のRED固定 | 既存testを弱める必要が生じたら停止 | 不要 |
| 4 | `verify_provenance`と`accept_artifact`の実装 | 設計を満たせない矛盾が出たら停止 | 不要 |
| 5 | GREEN、既存Work 5A受入25件、全test | 一件でも失敗したら停止 | 不要 |
| 6 | 正しい受理recordの再作成 | 案A／案Bの選択が未確定なら停止 | **必要**（§6.3の選択） |
| 7 | Codexによる独立検証 | — | 不要 |

単位4では、既存の`verify_provenance`の後方互換を取らない。旧形式のedgeを受け付けず、
新形式だけを正本とする。旧形式を読む必要が生じるのは単位3のN11だけであり、
そこでは「拒否されること」を確認する入力として使う。

## 8. Human判断が必要な点

一点だけである。

**§6.3の案A（既存`human_decision`をそのまま使う）と案B（新しい`human_decision`を作る）のどちらを採るか。**

これは来歴上「Humanが何回判断したか」の表現に関わる意味の判断であり、実装の細部ではない。
設計者の推奨は案Aである。

## 9. 本提案で行っていないこと

- `tools/task_contract/`、`tests/`、`TODO_NEXT_SESSION.md`、Current Plan、checklist、Requirementの変更
- `9e8cf00`のrevert、recordの削除・上書き
- 無効化record、RED test、実装、受理recordの再作成
- LLM、外部送信、外部`DATA_ROOT`、push、PR、CI、Work 4B、Work 6A、後続評価E2以降
