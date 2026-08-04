# Work 4A v3 共有コンテキスト（Codex引き渡し用）

作成日：2026-08-04
作成者：Claude（Work 4A v3実装担当）
宛先：Codex
目的：Work 4A Reusable Routine Ledgerの現在地、決定済み事項、未決事項、守るべき規律を、
この文書だけで把握できるようにする。

この文書は経緯の共有用であり、規範正本ではない。正本は各設計文書とDecision recordである。

---

## 1. 三行で言うと

- v2設計に「project外の観測をproject相対pathで参照する」という同時に満たせない要求があり、実装が停止した。
- v3で参照モデルを作り直した。Observation Attestationをproject内に置き、外部への唯一の橋にした。実装は完了しGREEN。
- いま922件の候補にHumanがラベルを付ける段で、その判断材料の設計（v3.1）と、
  そこで使う`conformance-evaluation`の利用範囲緩和が、**いずれも提案中でHuman承認前**である。

---

## 2. 何が壊れていて、何を直したか

### 2.1 v2の矛盾

v2設計は次の三つを同時に要求していた。

| 出所 | 要求 |
| --- | --- |
| v2 §1 | すべての`ref`の`path`はproject相対である |
| v2 §4 | Observation、Candidate Runは`DATA_ROOT`（project外）に置く |
| v2 §5 | DecisionとBaselineはCandidate Runの`ref`を保存する |

project外のfileをproject相対pathで参照することはできない。実装の脱出検査が
`record path escapes project`で正しく拒否し、そこで停止した。

**この時、検査側に例外を作る修正はしなかった。**設計の誤りであり、局所patchで通すことを
Humanが明示的に禁じたためである。

### 2.2 v3の解法：Observation Attestation

```text
DATA_ROOT（project外、Git外、再採取可能）
  Source Observation ─┐
  Candidate Run ──────┤ 内容Digestと最小要約だけをproject内へ写像
                      ▼
PROJECT_ROOT（Git管理、配布先ではread-only）
  Observation Attestation  ← 外部位置情報(advisory_locator)はここにだけ存在する
        ▲
  Operational Human Decision（project相対ref）
        ▲
  Baseline ── Entry / Relation / Policy / Source Universe（すべてproject相対ref）
```

不変条件は四つである。

1. DecisionとBaselineは`DATA_ROOT`を直接参照しない。参照するのはAttestationだけ。
2. 外部位置情報はAttestation内の`advisory_locator`にだけ置く。正本性の根拠ではない。
3. `DATA_ROOT`が無い配布先やCIでも、project artifactだけでcurrent Baselineを検証できる。
4. 外部fileがある時だけ照合する。Digest不一致は停止、file不在は`locator_unresolved`で非停止。

### 2.3 なぜ「root_kindを足すだけ」にしなかったか

当初案は`ref`に`root_kind: project | data`を足す方式だった。これは採らなかった。

- 外部refにもDigest照合を必須にすると、`DATA_ROOT`が空の環境で全Baselineが不正になる。
  必須にしなければ脱出検査に穴が開く。root_kindだけではこの二択から抜けられない。
- Layout v3の`relative_path_policy`が既に「相対pathはproject artifactに限る」と定めている。
  外部への参照をproject artifactへ持ち込むこと自体が既存規則違反だった。

root_kind自体は採用したが、外部位置情報の中だけに置き、権威を持たせなかった。

---

## 3. 現在の実装状態

### 3.1 commit列（`33218e0`以降）

| commit | 内容 |
| --- | --- |
| `61e635f` | v3設計承認、v2をsuperseded、`DEC-WORK4A-REBUILD-DESIGN-003`作成 |
| `2750ce3` | commit済みv2試作をrevert（2 file削除）。全663 passed |
| `6180b8c` | v3受入test 22件をREDで固定 |
| `5d3932a` | v3実装。受入22件、全685 passed |
| `5c468d1` | v1試作を撤去（2 file削除）。全681 passed |
| `7877763` | 外部`DATA_ROOT`の初期化（3 directory作成） |
| `1fb48af` | 初期化証跡の訂正 |
| `ee12e9b` | 実source観測と候補抽出。全681 passed |

### 3.2 主要fileとDigest

| file | SHA-256 |
| --- | --- |
| `docs/design/2026-08-04-work-4a-rebuild-design-v3-proposal.md` | `a9e0419dcac556789e82f6f51292dd70399000f988e0720d240286c9a05c2b37` |
| `records/development/2026-08-04-work-4a-rebuild-design-v3-approval-decision-v1.md` | `c358f730c84d2cdc3d981c7668d21f1898a12eadd04e9af04800b9c5f26900a1` |
| `records/development/2026-08-04-work-4a-v3-actual-observation-evidence-v1.md` | `75e0eb3d30c4ec559b33e3f9678ff8bbf1752d3a20f6b6a1f5ec4631d9cf25b1` |
| `tools/development/work4a_rebuild_v3.py` | `b2cdcbed4fe13f4d6ce2515e5b48d78055f351e4c47e4091d8c08a62855ae1a2` |
| `tests/test_work4a_rebuild_v3_e2e.py` | `1b6ee11c89c92e66c5c143e0f79919fc7f0e24adaf5ff79d6f93fd4aa1841476` |

提案文書（Human承認前）：

| file | 状態 |
| --- | --- |
| `docs/design/2026-08-04-work-4a-rebuild-design-v3-1-amendment.md` | `awaiting_human_approval` |
| `docs/design/2026-08-04-conformance-evaluation-scope-relaxation-proposal.md` | `awaiting_human_approval` |

**どちらもDecisionではない。**承認前に、実装、REDテスト作成、外部`DATA_ROOT`への追加書込み、
候補再抽出、LLM説明生成、Decision・Entry・Relation・Baselineの作成を行わない。

### 3.3 実データ

外部data root：`~/.reviewcompass3/projects/reviewcompass3/development/data/work4a/`

| 項目 | 値 |
| --- | --- |
| `source_content_id` | `6c0d9ab2edd80b536084a078c11a3cc1efd126964a421cd09366fa75ca14243d` |
| `snapshot_id` | `be323010fdcd343525ddcdb4d49b57c14913ec5a6baf2a4e586490646707be61` |
| `candidate_run_id` | `c2df7640968a319da1cede5fc2ea00a2eb581486c3e3dcb9f896d72f88fed8d2` |
| 対象file | `tools/**/*.py` 101件 |
| 候補 | 922件（module直下の関数648、class 274） |
| HEAD | `1fb48afe7d9229b1b95d6fcb05219ec50c382111` |

候補の内訳：例外class 81、非公開`_`始まり393、docstringあり124のみ、
class内method 20（**現在の候補に未収録**）。関数の行数は中央値16、最大1181、5行以下が92。

package別：session_logs 334、development 193、extraction 144、bootstrap 103、
requirements 102、layout 26、design 20。

---

## 4. 実装APIの要点

`tools/development/work4a_rebuild_v3.py`。例外は`V3ValidationError`で、`code`と`classification`を持つ。

| 関数 | 役割 |
| --- | --- |
| `write_source_universe` / `write_freshness_policy` | project内のPolicy成果物を作る |
| `resolve_data_root` | Layout v3語彙で外部rootを解決。root重なりを`invalid_layout`で停止 |
| `capture_observation` | 外部へ観測を書く |
| `build_candidate_run` | 外部へ候補を書く。内容Digestがfile名 |
| `write_attestation` | project内へ証明を書く。外部への唯一の橋 |
| `write_operational_decision` | project内へ人の決定を書く |
| `append_baseline` | Entry／Relation／Baselineをnew-onlyで書く |
| `validate_current` | P0〜P7の順序でcurrentを検証 |
| `evaluate_continuity` | 配布先での連続性を三値で判定 |
| `record_historical_status` | legacy Contractの歴史的状態を別identityで記録 |

### 4.1 validation順序（順序に意味がある）

P0 manifest → P1 layout解決（`invalid_layout`はここで停止）→ P2 Policy →
P3 Baseline連番 → P4 project ref → P5 Attestation内部 → P6 Decision相互検査 →
P7 外部locator照合 → P9 書込み時のnew-onlyと原子的書込み。

**P0〜P6で現在のBaselineは確定する。外部fileを一切読まない。**これが配布先で成立する根拠である。

### 4.2 非停止は二つだけ

`locator_unresolved`（外部file不在）と`locator_profile_mismatch`（profile違いで照合しない）。
それ以外の27条件はすべて停止し、部分的な書込みを残さない。

### 4.3 連続性の三値

`continuous_fresh`（universe一致かつsource内容一致）／`content_diverged`／`universe_diverged`。
後二者では新しいCandidate Runと新しいHuman Decisionなしにbaselineを進められない。
HEAD差、採取時刻の古さ、外部fileの存在は判定に使わない。

---

## 5. 決定済み事項

| Decision | 内容 |
| --- | --- |
| `DEC-WORK4A-REBUILD-DESIGN-002` | v2承認（現在はsuperseded） |
| `DEC-WORK4A-REBUILD-DESIGN-003` | v3承認。Policy語彙追加、Layout v3従属、v2 supersede |

**未承認**（提案中。Decision recordは存在しない）：

| 予定Decision ID | 提案文書 |
| --- | --- |
| `DEC-CONFORMANCE-SCOPE-RELAXATION-001` | `docs/design/2026-08-04-conformance-evaluation-scope-relaxation-proposal.md` |
| `DEC-WORK4A-REBUILD-DESIGN-004` | `docs/design/2026-08-04-work-4a-rebuild-design-v3-1-amendment.md` |

処分済みのもの：

- v1試作（`c4bfb57`のmodule、`377c610`のtest）→ 削除。対応表あり
- v2試作（`33218e0`のmodule、`df2bd3c`のtest）→ 削除。対応表あり
- 過去commitはrevertせず、historyは書き換えていない
- 外部`DATA_ROOT`の旧観測（v1時代の3 directory、19件）は削除も移動もしていない

---

## 6. conformance-evaluationの扱い（重要）

前身ReviewCompassに、実装codeからrequirementsとdesignを推定する`conformance-evaluation`がある。
継承記録は`records/sources/2026-08-02-reviewcompass-conformance-evaluation.md`
（前身固定commit `cab302d4b32af790628b811b3566f39d55781fa5`）。

このrepositoryには二つの制限がある。

1. 管理下で開発したcodeでは、LLM逆推定を通常経路にしない（継承記録§5）
2. 本Workは初期開発へ入れない（Deferred Work 9）

**この二つをWork 4Aの範囲で緩和することを提案中である。Human承認前であり、まだ緩和されていない。**
提案文書は`docs/design/2026-08-04-conformance-evaluation-scope-relaxation-proposal.md`。
承認された場合にだけ`DEC-CONFORMANCE-SCOPE-RELAXATION-001`を作成する。

提案で緩和するのは「使ってよいか」だけである。次の規律は緩和対象に含めず、維持する。

- 文書生成と適合判定を分離する
- 推定時に既存仕様を遮断し、後段で比較する
- 推定根拠としてcode referenceを保持する
- 生成物は`draft_only`とし、派生文書から規範正本を直接更新しない
- 意味変更候補はHuman判断へ渡す
- 機械がHuman dispositionを先取りしない
- LLM由来の記述は非権威とし、生成元を記録する

前身のcodeは複製しない。継承するのは責務と語彙である。

---

## 7. いま議論している問題

Humanの方針は「台帳には922件すべて載せ、`reuse` `extend` `merge` `split` または`as is`のlabelを付ける。
人がcodeを見て判断するのは現実的でないので、全codeを調べ、入力・出力・何をしているかの一覧表を作り、
それを元に分類する」である。

これに対しv3.1改訂案（承認待ち）が提案しているのは次の六点である。

### 7.0 三層の役割分担

| 層 | できること | 出力 | 権威 |
| --- | --- | --- | --- |
| 機械 | 構文解析、依存参照、呼出関係、類似候補、行数、型注記、構文的痕跡の抽出 | Routine Profile | 機械事実として権威を持つ |
| LLM | 責務の意味分析、処置labelの提案、理由、不確実性、確認点 | Disposition Proposal | **非権威。advisory** |
| Human | `reuse`／`extend`／`merge`／`split`／`as_is`の確定 | Operational Human Decision | 唯一の確定権限 |

LLMは最終処置を決めない。根拠が足りない場合はlabelを強制せず`human_review_required: true`とする。
Proposalを権威として使った書込みは`advisory_used_as_authority`で停止する。

### 7.1 分類軸を三つに分ける

v3ではdisposition語彙一つが、機械の候補分類とHumanの処置の両方に使われていた。

| 軸 | 語彙 | 決める主体 |
| --- | --- | --- |
| 候補分類 | `known` / `unknown` | 機械 |
| 責務の性質 | `public_responsibility` / `implementation_detail` / `ownership_unclear` | 機械が提案、Humanが確定 |
| 処置 | `reuse` / `extend` / `merge` / `split` / `as_is` | Humanのみ |

第二軸は前身conformance-evaluationの`implementation-detail`と`ownership-unclear`を継承する。
非公開関数393件の扱いに直接効く。

### 7.2 Routine Profile（機械事実だけの外部record）

記号、code位置、引数と型注記、戻り値、docstring 1行目、行数、被参照数、構文的痕跡、
構造Digest、類似cluster IDを持つ。**LLM由来のfieldを入れない。**混入は`unknown_field`で拒否する。

`side_effect_markers`は`syntactic_effect_markers`へ改名した。副作用そのものではなく、
呼出名の構文一致で検出した痕跡だからである。別名輸入も間接呼出も追わない。
**未検出は「副作用なし」を意味しない。**この意味をschemaで表すため、
`marker_detection.absence_does_not_imply_no_effect`を必須fieldとし、`true`でなければ拒否する。

### 7.3 Disposition Proposal（LLMの非権威record）

Routine Profileとは別recordにする。責務の説明、入出力の意味的要約、意味的依存、類似routine、
統合候補、`recommended_disposition`、代替候補、`confidence`、`reason`、`human_review_point`、
`advisory: true`、`human_review_required`を持つ。

生成元として、モデル、テンプレート版、対象`source_content_id`、生成日時、生成物Digestを記録する。
このrecordからDecision、Entry、Baselineを自動生成しない。

### 7.4 判断をgroup単位にする

922件を一件ずつ確認するのは表があっても現実的でない。LLMはgroup候補を提案してよいが、
**Human Decisionへ渡せるのは機械評価可能な決定的条件式に落とせるものだけ**である。
条件式はfield・演算子・値の三つ組の連言に限り、自然文でgroupを定義しない。

例：例外class群81件、解析群、環境変数の痕跡を持つ群、同一構造Digestの重複群、
巨大かつ痕跡が複数の群。Humanが「このgroupは原則`as_is`、明示した例外だけ別処置」と
判断できる形を目標とする。どのgroupにも該当しないroutineが残る場合、既定値で埋めず差し戻す。

### 7.5 抽出対象を固定する

通常関数、async関数、class、instance／static／class method、property、nested functionを含める。
lambdaは安定した識別子を持たないため既定で除外し、件数と位置を`excluded_constructs`へ記録する
（黙って落とさない）。symbol_idはPythonの`__qualname__`規約に合わせる。

これにより`extraction_rule_version`が2になり、新しいCandidate Runを作る。
`ee12e9b`のObservationと922件のCandidate Runは歴史記録として保持し、書き換えない。

### 7.6 未決五点

1. lambdaの扱い（現案：除外して件数と位置を明示記録）
2. group条件の記法（現案：三つ組の連言のみ、正規表現とORは不可）
3. 例外class 81件を機械の初期値で`implementation_detail`にしてよいか
4. Disposition Proposalを922件一括で生成するか、group判断に必要な範囲だけにするか
5. nested functionの既定を`implementation_detail`としてよいか

---

## 8. Codexが引き継ぐ場合に守ること

これらはHumanが繰り返し明示した規律である。破ると作業が差し戻される。

1. **局所patchで通さない。**設計レベルの矛盾を見つけたら、実装を継ぎ足さず停止して報告する。
   v2の失敗はこれを守らなかった場合に起きる形である。
2. **推奨は承認ではない。**Humanの承認文言を受け取るまで、実装・破棄・revertを開始しない。
   承認を推測してDecision recordへ書き込まない。Decision recordは承認の言葉をそのまま引用する。
3. **破棄とrevertを同じ操作にまとめない。**前者は復元不能、後者はhistoryに残る。承認も分ける。
4. **停止して承認を待つ操作**：破棄、revert、外部`DATA_ROOT`への追加書込み、候補再抽出、
   LLMによる説明・label提案の生成、actual artifactの対象routine選定とHuman disposition。
5. **TDD**：期待を先に固定し、実装中に緩めない。REDを確認してからGREENにする。
6. **TODO更新**は`docs/development/prompts/todo-handoff-update.md`の手順だけを使う。
   state導出、Digest、件数は機械処理にする。手入力で推測しない。
7. **test実行**は公式runnerを使う：
   `python3 -m tools.development.policy_test_runner --project-root . --suite full --receipt <path>`
8. **作業単位の遷移**は`tools/development/work_unit_transition.py --work-status completed`で確認する。
   未commitなら次作業へ進まない。
9. **Python字下げは4 space**（既存codebaseの統一に合わせている。global方針は2 spaceだが、
   本repositoryの既存code全体が4 spaceのため踏襲した。Humanへ申し送り済み）。
10. **v1／v2試作を参照・import・復元しない。**削除済みであり、実装正本ではない。

---

## 9. 次の一手

**現在の停止点：v3.1設計とconformance-evaluation利用範囲の、いずれもHuman承認待ち。**

1. 二つの提案のHuman承認（`DEC-WORK4A-REBUILD-DESIGN-004`、`DEC-CONFORMANCE-SCOPE-RELAXATION-001`）と
   未決五点の判断。
2. Policy artifactを`policy_version` 2へ上げ、三軸語彙・group条件の記法・痕跡語彙・検出規則を固定する。
3. v3.1受入test I1〜I16をREDで固定する。
4. Routine Profile生成、抽出規則v2、Attestation schema 2を実装しGREENにする。
5. 実sourceでRoutine Profileを生成し、**機械抽出列だけ**を提示する。
6. LLMによるDisposition Proposal生成を、Humanが承認してから実施する。
7. group条件とdispositionをHumanが決める。
8. Entry、Relation、Baselineを生成する。

段階5と6を分けているのは、機械抽出だけでどこまで判断できるかを先に見て、
LLM生成の範囲を必要最小限にするためである。

段階1より前に、実装、REDテスト作成、外部`DATA_ROOT`への追加書込み、候補再抽出、
LLM説明生成、Decision・Entry・Relation・Baselineの作成を行わない。
