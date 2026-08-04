# Work 4A Rebuild Design v3.1 Amendment

状態：`approved_for_implementation`
対象：Work 4A Reusable Routine Ledger
基準文書：`docs/design/2026-08-04-work-4a-rebuild-design-v3-proposal.md`（`approved_for_implementation`）
関連提案：`docs/design/2026-08-04-conformance-evaluation-scope-relaxation-proposal.md`（`approved`）
承認記録：`DEC-WORK4A-REBUILD-DESIGN-004`

Humanの承認により、本改訂はv3の差分として実装正本に加わる。
LLMによるDisposition Proposalの生成は、Routine Profileの実データ確認後の別承認とする。

v3を置き換えず、差分だけを定義する。v3の参照モデル、validation順序、fail-closed条件、
new-only規則は変更しない。追加するのは、922件の候補にHumanが処置labelを付けるための判断材料と、
その語彙である。

## 1. 背景と目的

実source観測で候補が922件になった（`records/development/2026-08-04-work-4a-v3-actual-observation-evidence-v1.md`）。
内訳はmodule直下の関数648、class 274（うち例外class 81）、非公開`_`始まり393、
docstringあり124のみ、class内method 20（現行の候補に未収録）。
関数の行数は中央値16、最大1181、5行以下が92。

目的は、**922件のcodeを人が1件ずつ読まずに処置labelを判断できるようにすること**である。
そのために`conformance-evaluation`の責務をWork 4Aに限定して利用する。
利用の可否は関連提案のHuman承認に依存する。

## 2. v3から変更しないもの

- Observation Attestationを外部`DATA_ROOT`への唯一の橋とすること。
- project refとadvisory locatorの分離。
- validation順序P0〜P9とfail-closed条件（`invalid_layout`を含む）。
- Entry・Relationのnew-only、current Baselineの導出。
- 機械がHuman dispositionを先取りしないこと。

## 3. 三層の役割分担

判断を三層に分け、各層が越えてよい境界を固定する。

| 層 | できること | 出力 | 権威 |
| --- | --- | --- | --- |
| 機械 | 構文解析、依存参照、呼出関係、類似候補、行数、型注記、構文的痕跡の抽出 | Routine Profile | 機械事実として権威を持つ |
| LLM | 責務の意味分析、処置labelの提案、理由、不確実性、確認点の作成 | Disposition Proposal | **非権威。advisory** |
| Human | `reuse`／`extend`／`merge`／`split`／`as_is`の確定 | Operational Human Decision | 唯一の確定権限 |

規律は次のとおりである。

- **LLMは最終処置を決めない。**Entryの`disposition`はHuman Decisionからしか設定できない。
- 根拠が足りない場合、LLMはlabelを強制せず`human_review_required: true`とする。
  `recommended_disposition`は`null`にしてよい。
- Disposition ProposalからDecision、Entry、Relation、Baselineを自動生成しない。
  Decisionは`consulted_proposal_ref`としてProposalを参照してよいが、権威としては扱わない。
- Proposalを権威として使った書込みは`advisory_used_as_authority`で停止する（新しいfail-closed code）。

## 4. 分類軸の分離

v3ではdisposition語彙一つが、機械の候補分類とHumanの処置の両方に使われていた。三軸へ分ける。
第二軸の語彙は前身`conformance-evaluation`から継承する。

| 軸 | field | 語彙 | 決める主体 |
| --- | --- | --- | --- |
| 候補分類 | `candidate_classification` | `known`（既存Entryと同じsymbol ID）／`unknown` | 機械 |
| 責務の性質 | `responsibility_class` | `public_responsibility`／`implementation_detail`／`ownership_unclear` | 機械が提案、Humanが確定 |
| 処置 | `disposition` | `reuse`／`extend`／`merge`／`split`／`as_is` | Humanのみ |

- `candidate_classification`はv3の`new`／`reuse`混用を解消する。初回は全件`unknown`である。
- 第二軸は前身の`implementation-detail`と`ownership-unclear`を継承する。
  前身の`spec-missing`／`code-missing`／`mismatch`は上流文書との差分用であり、Work 4Aでは使わない。
- `as_is`は「台帳に載せるが今回は手を入れない」を表す。
- Policy artifactは`policy_version` 2へ上げ、三つの語彙を別fieldとして持つ。
  change classは`ordinary`とする（security、authority、不可逆操作のいずれにも触れないため）。

機械が`responsibility_class`へ初期値を置いてよいのは、次の決定的規則による場合だけである。
規則はPolicy artifactに書き、呼出側の文字列で判定しない。**上から順に、最初に一致したものを採る。**

1. 例外class（基底が例外型） → `ownership_unclear`
2. nested function → `implementation_detail`
3. symbol名が`_`で始まり、source universe内の他moduleから参照されない → `implementation_detail`
4. source universe内のどこからも参照されない → `ownership_unclear`
5. それ以外 → `public_responsibility`

規則1は`DEC-WORK4A-REBUILD-DESIGN-004`の決定による。例外classは責務の帰属がcodeからは決まらないため、
`implementation_detail`と断定せず`ownership_unclear`としてHumanの確定を要求する。

初期値は提案であり、Humanが変更できる。Humanが確定するまでEntryを作らない。

## 5. 抽出対象と除外対象

「台帳には全て載せる」方針に従い、実装を持つ構文単位は原則すべて候補にする。
除外する場合は、理由と件数をRoutine Profileへ記録し、黙って落とさない。

| 構文単位 | 扱い | 理由 |
| --- | --- | --- |
| module直下の通常関数（`def`） | 含める | 再利用単位として第一級 |
| module直下のasync関数（`async def`） | 含める | 呼出規約が違うだけで再利用単位は同じ |
| class | 含める | 責務の単位。dataclass、例外classも含む |
| instance method | 含める | classの責務の内訳。全て載せる方針に従う |
| static method、class method | 含める | 同上。`symbol_kind`で区別する |
| property | 含める | 実装を持つ。`symbol_kind: property` |
| nested function（関数内定義） | 含める | 実装を持つ。ただし親の実装詳細である可能性が高く、`responsibility_class_proposal`の既定は`implementation_detail`。`enclosing_symbol_id`を持つ |
| lambda | **除外（既定）** | 安定した識別子を持たない。行位置でしか特定できず、行が動くたびにIDが変わりnew-only台帳の同一性が壊れる。件数と位置を`excluded_constructs`へ記録する。§15の未決事項1 |
| module直下の代入、定数、import | 除外 | routineではない。件数のみ記録する |

### 5.1 symbol_idの形式

`extraction_rule_version` 2では、Pythonの`__qualname__`規約に合わせる。

| 種別 | 形式 | 例 |
| --- | --- | --- |
| 関数 | `<path>:<name>` | `tools/development/todo_handoff.py:validate_todo` |
| class | `<path>:<Class>` | `tools/layout/baseline.py:LayoutError` |
| method | `<path>:<Class>.<method>` | `tools/layout/baseline.py:LayoutResolution.roots` |
| nested function | `<path>:<outer>.<locals>.<inner>` | `tools/x.py:build.<locals>.helper` |

v3（`extraction_rule_version` 1）は`<path>:<name>`のみでmethodを含まなかった。
形式が変わるため、既存のCandidate Runとは別のIDになる。§8を参照。

### 5.2 symbol_idの一意性

nested functionを含めると、同一moduleで同じqualnameが複数生じうる。
条件分岐で同名のnested functionを二度定義する場合、`try`／`except`で同名関数を再定義する場合、
同名methodを再定義する場合などである。

**同一Routine Profile内でsymbol_idが重複したら`symbol_id_collision`で停止する。**

- 後から現れた定義で黙って上書きしない。
- 行番号、序数、出現順による識別子の付け足しで回避しない。
  これらはcodeの増減で移動するため、new-only台帳の同一性を壊す。
- 重複を検出した場合は、重複したsymbol_idと該当する全`code_reference`を停止理由に含める。
- 解消はHumanの判断とする。source側の改名か、symbol_id規約の改訂かを選ぶ。
  規約を改訂する場合は`extraction_rule_version`を上げる。

この規則はCandidate Run、Routine Profile、Entry生成のいずれの段階でも同じである。

## 6. Routine Profile（機械事実のみ）

配置：`<runtime_root>/projects/<project_id>/<profile>/data/work4a/profiles/<profile_run_id>.json`（外部）

**このrecordは機械抽出の事実だけを持つ。LLM由来の記述を入れない。**
`profile_run_id`は内容Digestである。

```json
{
  "record_kind": "work4a_routine_profile",
  "schema_version": 1,
  "digest_algorithm": "sha256",
  "profile_run_id": "<64桁hex>",
  "observation_snapshot_id": "<64桁hex>",
  "source_content_id": "<64桁hex>",
  "extraction_rule_version": 2,
  "marker_detection": {
    "method": "syntactic_call_name_match",
    "detection_is_syntactic_only": true,
    "absence_does_not_imply_no_effect": true,
    "follows_aliases": false,
    "follows_indirect_calls": false
  },
  "routines": [
    {
      "symbol_id": "tools/development/todo_handoff.py:validate_todo",
      "symbol_kind": "function",
      "enclosing_symbol_id": null,
      "code_reference": {
        "relative_path": "tools/development/todo_handoff.py",
        "start_line": 42,
        "end_line": 67
      },
      "signature": {
        "parameters": [
          { "name": "document", "kind": "positional", "annotation": "bytes", "has_default": false }
        ],
        "returns_annotation": "int"
      },
      "docstring_first_line": "TODOに表示したpathとDigestを実fileへ照合する。",
      "syntactic_effect_markers": ["file_read"],
      "internal_reference_count": 3,
      "line_count": 26,
      "structure_digest": "<64桁hex>",
      "structural_match_group_id": "STRUCT-MATCH-0007",
      "candidate_classification": "unknown",
      "responsibility_class_proposal": "public_responsibility"
    }
  ],
  "excluded_constructs": [
    { "construct": "lambda", "count": 0, "reason": "no_stable_identifier" },
    { "construct": "module_level_assignment", "count": 0, "reason": "not_a_routine" }
  ],
  "content_digest": "<64桁hex>"
}
```

### 6.1 構文的痕跡（旧`side_effect_markers`）

v3.1では`syntactic_effect_markers`へ改名する。これは**副作用そのものではなく、構文的に検出した痕跡**である。

閉じた語彙と検出規則は次のとおりで、Policy artifactへ固定する。

| marker | 検出規則（呼出名の構文一致のみ） |
| --- | --- |
| `file_read` | `open`の読みmode、`read_text`、`read_bytes`、`exists`、`iterdir`、`glob`、`rglob`、`json.load` |
| `file_write` | `open`の書きmode、`write_text`、`write_bytes`、`mkdir`、`unlink`、`replace`、`rename`、`chmod`、`shutil.*` |
| `process_spawn` | `subprocess.*`、`os.system`、`os.exec*`、`os.spawn*` |
| `network` | `urllib.*`、`http.*`、`socket.*`、`requests.*` |
| `environment` | `os.environ`、`os.getenv`、`os.putenv` |
| `global_mutation` | `global`文、`nonlocal`文、module直下の可変objectへの代入 |

検出は別名輸入も間接呼出も追わない。したがって**未検出は「痕跡が見つからなかった」ことしか意味せず、
「副作用が無い」ことを意味しない**。この意味をschema上でも表すため、
`marker_detection.absence_does_not_imply_no_effect`を必須fieldとし、値が`true`でないrecordは拒否する。

### 6.2 構造一致group（旧`similarity_cluster_id`）

`structure_digest`は、識別子名を正規化したAST構造のDigestである。
`structural_match_group_id`は、**同一の`structure_digest`を持つroutineへ機械的に割り当てるgroup ID**である。

名称を`similarity_cluster_id`から改めたのは、「類似」という語が意味的な近さや統合の結論を
含意するためである。この値が示すのは次のことだけである。

- **示すこと**：AST構造が正規化後に完全一致した、という構文上の事実。
- **示さないこと**：責務が同じであること、統合してよいこと、統合すべきこと。

したがって`structural_match_group_id`は**統合の結論ではなく、HumanとLLMが確認するための手掛かり**である。
同じgroupに入っていても責務が異なる場合があり（定型的な委譲や検査の形が一致しただけの場合）、
逆に責務が同じでも構造が違えば別groupになる。

この値をgroup条件に使ってよいのは、Humanが個別に確認したうえで`merge`を確定する場合であり、
値の一致だけで`merge`を自動確定しない。

## 7. Disposition Proposal（LLMの非権威record）

配置：`<runtime_root>/projects/<project_id>/<profile>/data/work4a/disposition-proposals/<proposal_run_id>.json`（外部）

Routine Profileとは**別record**とする。混ぜない。

```json
{
  "record_kind": "work4a_disposition_proposal",
  "schema_version": 1,
  "digest_algorithm": "sha256",
  "advisory": true,
  "proposal_run_id": "<64桁hex>",
  "routine_profile_run_id": "<64桁hex>",
  "observation_snapshot_id": "<64桁hex>",
  "source_content_id": "<64桁hex>",
  "generation_provenance": {
    "provider": "<提供者識別子>",
    "model": "<モデル識別子>",
    "template_id": "WORK4A-DISPOSITION-PROPOSAL-TEMPLATE",
    "template_version": 1,
    "template_digest": "<64桁hex>",
    "routine_profile_content_digest": "<64桁hex>",
    "generated_at": "2026-08-05T10:00:00+09:00",
    "output_digest": "<64桁hex>"
  },
  "proposals": [
    {
      "symbol_id": "tools/development/todo_handoff.py:validate_todo",
      "responsibility_summary": "TODO本文の参照pathとDigestを実fileへ照合する。",
      "input_summary": "TODO文書のbytesとproject root。",
      "output_summary": "照合できた参照件数。不一致は例外で停止。",
      "semantic_dependencies": ["tools/development/issue_resolution_post_write.py:validate_todo_reference_digests"],
      "similar_routines": ["tools/development/todo_snapshot.py:verify_reference"],
      "merge_candidates": [],
      "recommended_disposition": "as_is",
      "alternative_dispositions": ["reuse"],
      "confidence": "medium",
      "reason": "参照検査の入口であり、他routineから3件参照される。責務は単一。",
      "human_review_point": "issue_resolution_post_writeの同名処理と統合すべきかは呼出側の意図に依存する。",
      "human_review_required": false,
      "evidence_refs": [
        {
          "kind": "routine_profile_field",
          "symbol_id": "tools/development/todo_handoff.py:validate_todo",
          "field": "internal_reference_count"
        },
        {
          "kind": "code_reference",
          "symbol_id": "tools/development/issue_resolution_post_write.py:validate_todo_reference_digests",
          "relative_path": "tools/development/issue_resolution_post_write.py",
          "start_line": 140,
          "end_line": 176
        }
      ]
    }
  ],
  "content_digest": "<64桁hex>"
}
```

規律は次のとおりである。

- `advisory`は`true`固定。`false`のrecordは書込みも読込みも拒否する。
- `recommended_disposition`は`null`を許す。根拠が足りないときはlabelを強制せず、
  `human_review_required: true`とする。
- `confidence`は`high`／`medium`／`low`の閉じた語彙とする。
- 本文（source code）を転記しない。要約に限る。
- `generation_provenance`の全fieldを必須とする。欠けるrecordは拒否する。
- このrecordはEntryの`disposition`の根拠にならない。Human Decisionだけが根拠になる。

### 7.1 参照範囲の制限

`semantic_dependencies`、`similar_routines`、`merge_candidates`に書けるのは、
**同一Routine Profile（`routine_profile_run_id`が一致するもの）に存在するsymbol IDだけ**である。

- Profileに無いsymbol ID、綴りが違うID、source universe外への参照は
  `advisory_reference_unresolved`で停止する。
- 自分自身への参照も停止させる。
- 存在しないroutineを指す提案を、注記や補正で通さない。

これは、LLMが実在しないroutineを挙げた場合に、その提案が判断材料として流通することを防ぐためである。

### 7.2 根拠参照（`evidence_refs`）

各提案は`evidence_refs`を**必須**とし、少なくとも一件を持つ。空配列は`advisory_evidence_missing`で停止する。
指せる根拠は次の二種類だけである。

| `kind` | 指すもの | 検証 |
| --- | --- | --- |
| `routine_profile_field` | `symbol_id`とProfileのfield名 | Profileに当該symbolが存在し、当該fieldを持つこと |
| `code_reference` | `symbol_id`と`relative_path`、`start_line`、`end_line` | Profileの同symbolの`code_reference`と完全一致すること |

- `symbol_id`が同一Profileに無ければ`advisory_reference_unresolved`。
- `field`がProfileのschemaに無ければ`advisory_reference_unresolved`。
- `code_reference`の値がProfileの値と食い違えば`advisory_reference_unresolved`。
- `evidence_refs`が空、または`kind`が上記以外なら`advisory_evidence_missing`。

いずれもfail-closedであり、注記で続行しない。
根拠を持てない提案は、`recommended_disposition`を`null`とし`human_review_required: true`として書く。

## 8. Attestationの拡張

Attestationに二つの節を追加する。v3のschemaは未知fieldを拒否するため、これはschema変更である。
`schema_version`を2へ上げる。既存のschema_version 1のAttestationは読めるままとする。

```json
"routine_profile": {
  "record_kind": "work4a_routine_profile",
  "profile_run_id": "<64桁hex>",
  "content_digest": "<64桁hex>",
  "extraction_rule_version": 2,
  "advisory_locator": { "root_kind": "data", "…": "advisory locator" }
},
"disposition_proposal": {
  "record_kind": "work4a_disposition_proposal",
  "proposal_run_id": "<64桁hex>",
  "content_digest": "<64桁hex>",
  "advisory": true,
  "advisory_locator": { "root_kind": "data", "…": "advisory locator" }
}
```

- 両節の`observation_snapshot_id`はAttestationの`observation.snapshot_id`と一致しなければならない。
  不一致は`unlinked_candidate`で停止する。
- `disposition_proposal.advisory`が`true`でなければ`advisory_used_as_authority`で停止する。
- 外部fileが無い場合はv3と同じく`locator_unresolved`として非停止とする。
- `disposition_proposal`節は省略可とする。LLM分析を行わない運用を妨げない。

## 9. group単位の判断支援

922件を1件ずつ判断させない。次の二段にする。

1. **group決定**：Humanが`responsibility_class`と`disposition`をgroup単位で決める。
2. **展開**：機械がgroup条件を各routineへ適用し、Entryを生成する。
   各Entryは適用されたgroup条件のIDを持つ。

### 9.1 group条件の記法

LLMは類似責務、呼出関係、構文的特徴に基づくgroup候補を提案してよい。
ただし**Human Decisionへ渡せるのは、機械評価可能な決定的条件式に落とせるものだけ**である。
自然文でgroupを定義しない。

条件式は「field、演算子、値」の三つ組の連言（AND）だけとする。任意式、正規表現、
自由文の述語を許さない（§12の未決事項2）。

| 使えるfield | 出どころ |
| --- | --- |
| `package`、`symbol_kind`、`name_prefix`、`name_suffix`、`is_private` | Routine Profile |
| `syntactic_effect_markers`、`marker_count` | Routine Profile |
| `internal_reference_count`、`line_count` | Routine Profile |
| `structural_match_group_id`、`structure_digest` | Routine Profile |
| `responsibility_class_proposal`、`candidate_classification` | Routine Profile |
| `base_is_exception` | Routine Profile（classのみ） |

演算子は`equals`、`not_equals`、`in`、`contains`、`lte`、`gte`に限る。

### 9.2 提示できるべきgroup例

設計は、少なくとも次のgroupを処置候補と根拠付きで提示できる形にする。

| group | 条件式の例 | 想定処置 |
| --- | --- | --- |
| 例外class群（81件） | `symbol_kind equals class` AND `base_is_exception equals true` | `as_is` |
| 解析群 | `package equals session_logs` AND `name_prefix equals parse_` | `as_is`または`merge` |
| 設定・環境変数群 | `syntactic_effect_markers contains environment` | `as_is`。要確認点あり |
| 構造一致群（統合候補の手掛かり） | `structural_match_group_id equals STRUCT-MATCH-0007` | `merge`候補。個別確認が必要 |
| 巨大かつ複数痕跡群 | `line_count gte 100` AND `marker_count gte 2` | `split`候補。個別確認 |

目標は、Humanが「このgroupは原則`as_is`、明示した例外だけ別処置」と判断できる形である。

### 9.3 取りこぼしを許さない

Operational Human Decisionに`group_rules`を追加する。個別指定は`explicit_targets`で上書きする。
どのgroupにも該当しないroutineが一件でも残る場合は、Entryを作らず`ownership_unclear`として
Humanへ差し戻す。既定値で埋めない。

## 10. Entryの追加field

| field | 内容 |
| --- | --- |
| `responsibility_class` | 第二軸の確定値 |
| `applied_group_rule_id` | どのgroup条件で決まったか。個別指定なら`null` |
| `routine_profile_ref` | Attestation経由の参照。外部を直接指さない |
| `disposition_source` | `human_decision`固定。他の値は`advisory_used_as_authority`で停止 |

v3で自由文だった`side_effects`は、`syntactic_effect_markers`の配列とし、機械抽出値を採る。
Humanが上書きする場合は`side_effects_override`に理由とともに記録する。

## 11. 現在の観測との関係

`ee12e9b`で固定したObservationと922件のCandidate Runは**歴史記録として保持する**。

- Observation（`snapshot_id: be323010fd…`）は変更しない。`source_content_id`も変わらない。
- Candidate Run（`candidate_run_id: c2df7640…`）は書き換えない。
- v3.1承認後に`extraction_rule_version`を2へ更新した場合だけ、新しいCandidate Runを
  new-onlyで作る。IDが変わるのはsymbol_id形式とmethod収録が変わるためである。
- 既存recordのin-place更新、削除、移動を行わない。

## 12. Work 9との境界

本改訂はDeferred Work 9のAs-Built projector、Markdown renderer、Documentation Conformance gateを
実装しない。Routine ProfileとDisposition ProposalはWork 4Aの判断材料であり、人間向け文書を生成しない。
Work 4Aの完了条件はWork 9の完了条件を含まない。

前身`conformance-evaluation`のcodeは複製しない。継承するのは責務と語彙であり、
継承元は`records/sources/2026-08-02-reviewcompass-conformance-evaluation.md`の固定commitとDigestで示す。

## 13. v3.1 E2E acceptance

v3の22件は変更せず維持する。次を追加する。

- I1 Routine Profileを生成し、§5の抽出対象（method、nested functionを含む）を漏れなく収録できる。
  除外した構文単位は`excluded_constructs`へ件数と理由が記録される。
- I2 `marker_detection.absence_does_not_imply_no_effect`が`true`でないRoutine Profileを拒否する。
- I3 `syntactic_effect_markers`に閉じた語彙外の値があれば拒否する。
- I4 Routine ProfileにLLM由来のfieldがあれば`unknown_field`で拒否する。
- I5 `advisory`が`true`でないDisposition Proposalを`advisory_used_as_authority`で拒否する。
- I6 `generation_provenance`のfield（`provider`、`model`、`template_id`、`template_version`、
  `template_digest`、`routine_profile_content_digest`、`generated_at`、`output_digest`）が
  一つでも欠けるDisposition Proposalを拒否する。
  `routine_profile_content_digest`が対象Routine Profileの`content_digest`と一致しない場合も拒否する。
- I7 `recommended_disposition`が`null`かつ`human_review_required`が`true`のProposalは正常に扱える。
- I8 Disposition Proposalを根拠にEntryの`disposition`を設定しようとすると`advisory_used_as_authority`で停止する。
- I9 `routine_profile`または`disposition_proposal`の`observation_snapshot_id`がAttestationと
  不一致なら`unlinked_candidate`で停止する。
- I10 外部のRoutine ProfileとDisposition Proposalが無くてもcurrent Baselineを検証でき、
  `locator_unresolved`を注記する。
- I11 group条件に該当しないroutineが残る場合、Entryを作らず停止する。
- I12 group条件から展開したEntryが`applied_group_rule_id`を持ち、個別指定は`null`になる。
- I13 `responsibility_class`の機械初期値は提案であり、Humanの確定値と異なってもEntryはHuman値を採る。
- I14 抽出規則をv2にすると新しいCandidate Runが作られ、既存Candidate Runは書き換わらない。
- I15 Attestation schema_version 1の既存recordを読めることを確認する。
- I16 同一`structure_digest`のroutineが同一`structural_match_group_id`になる。
  `structural_match_group_id`の一致だけでは`merge`を確定できず、Human Decisionを要する。
- I17 同一Routine Profile内でsymbol_idが重複した場合、`symbol_id_collision`で停止する。
  後の定義で上書きせず、行番号や序数による識別子の付け足しで回避しない。
  停止理由に重複したsymbol_idと全`code_reference`が含まれる。
- I18 `semantic_dependencies`、`similar_routines`、`merge_candidates`が同一Routine Profileに
  存在しないsymbol IDを指す場合、`advisory_reference_unresolved`で停止する。自己参照も停止する。
- I19 `evidence_refs`が空、または`kind`が閉じた語彙外なら`advisory_evidence_missing`で停止する。
- I20 `evidence_refs`の`code_reference`がRoutine Profileの値と食い違う場合、
  `advisory_reference_unresolved`で停止する。注記で続行しない。
- I21 根拠を持てない提案は`recommended_disposition`が`null`かつ`human_review_required`が`true`で
  あれば受理される。

## 14. 承認後の実行順序

**以下はいずれも承認後に行う。現時点では未実施である。**

1. 本改訂とconformance-evaluation利用範囲の緩和提案のHuman承認。
2. Policy artifactを`policy_version` 2へ上げ、三軸語彙、group条件の記法、痕跡語彙、
   検出規則を固定する。
3. I1〜I21をREDで固定する。
4. Routine Profile生成、抽出規則v2、Attestation schema 2を実装しGREENにする。
5. 実sourceでRoutine Profileを生成し、**機械抽出列だけ**を提示する。
6. LLMによるDisposition Proposal生成を、Humanが承認してから実施する。
7. group条件とdispositionをHumanが決める。
8. Entry、Relation、Baselineを生成する。

段階5と6を分けるのは、機械抽出だけで判断できる範囲を先に見て、LLM生成の範囲を必要最小限に
するためである。例外class 81件、5行以下の関数92件、非公開393件のうち相当数は、
機械事実だけでgroup判断できる見込みがある。

## 15. 決定事項（提案時の未決五点）

`DEC-WORK4A-REBUILD-DESIGN-004`により次のとおり決定した。本文へ反映済みである。

| # | 論点 | 決定 |
| --- | --- | --- |
| 1 | lambdaの扱い | 除外し、件数と位置を`excluded_constructs`へ記録する（§5のとおり） |
| 2 | group条件式の記法 | 三つ組の連言（AND）のみ。正規表現とORを許さない（§9.1のとおり） |
| 3 | 例外classの機械初期値 | `ownership_unclear`（§4の規則1） |
| 4 | Disposition Proposalの生成単位 | 922件全件をbatch生成する |
| 5 | nested functionの機械初期値 | `implementation_detail`（§4の規則2） |

決定3だけが提案時の推奨と異なる。提案は`implementation_detail`を推奨していたが、
例外classの責務帰属はcodeから決まらないため、Humanの確定を要求する`ownership_unclear`とした。

## 16. 旧未決事項の原文

1. **lambdaの扱い。**現案は除外し、件数と位置を`excluded_constructs`へ記録する。
   「全て載せる」方針を厳密に取るなら、`<path>:<enclosing>.<lambda#序数>`のような序数IDで
   収録する選択肢もあるが、序数は要素の増減で移動するため同一性が弱い。
   設計者の推奨は現案（除外して明示記録）である。
2. **group条件の記法。**現案は三つ組の連言のみ。正規表現やORを許すかは未決。
   許すと表現力は上がるが、条件式の等価性判定と再現性が落ちる。
3. **例外class 81件の機械初期値。**現行の三規則では`public_responsibility`に寄る可能性がある。
   `base_is_exception`を第四の規則として`implementation_detail`の既定にしてよいか。
4. **Disposition Proposalの生成単位。**922件を一括生成するか、group判断に必要な範囲だけに
   絞るか。後者なら生成量を大幅に減らせる。
5. **nested functionの既定。**現案は`implementation_detail`。親が公開責務でも子は実装詳細とする
   扱いでよいか。
