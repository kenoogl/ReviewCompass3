# Reviewer起動アダプタ 判定record（機械転記） e2e-012-001

- Reviewer：provider `anthropic`／model `claude-opus-5`（アダプタ照合済み）
- 独立性：Tier 3（アダプタ判定。契約010 §5.1-4）
- 起動方式：headless機械起動（backend `claude-subagent`）
- 依頼record：`records/session-handoffs/2026-08-17-claude-subagent-backend-implementation-completion-review-subagent-request-v1.md`（SHA-256 `e32b525ddd54380602522f76c3536ac63eb538a73c57fdf35d95fc96c86cd57f`）
- 未加工出力：保存先種別 `private_root_immutable_store`、SHA-256 `799be2864cae38f12adf4053badff3e08dce006320c43607a07a9d74e5c96a72`、参照権限：repo外私有領域（利用者とClaude）
- 実行識別子：`e2e-012-001`
- 判定：**rejected**
- 判定要旨：反証点2（tier受容機構）・反証点3（claude起動固定形と訂正3件）は反証できず、実装は依頼recordの主張どおりだった。tier受容は、別プロバイダがTier 1で従来どおり通り（core.py 371-372行）、claude-subagentは --accept-tier の欠落・不一致で reviewer_not_independent_tier、一致でも受容根拠fileが無ければ acceptance_reference_missing で、いずれも子processを起動する前に止まる（tests 889-930行が facade.calls == [] で実効を固定）。一致かつ実在のときだけ起動へ進み、起動recordへ tier・accept_tier・acceptance_reference が入り（core.py 687-708行、tests 1124-1149行）、判定recordにも Tier が刻まれる（record.py 246行）。claude固定引数は Read,Glob,Grep のみで、書込み道具も --dangerously-skip-permissions 類も無く、両向きで固定されている（core.py 323-354行、tests 1075-1110行）。訂正3件も契約v2＋overlayどおりで、--verbose は stream-json 直後、通過変数9種と抑制注入9種は実行器の値と同値であることが試験で固定され（tests 991-1010行・1037-1048行）、agy子環境には USER も注入keyも入らないことが実効的に押さえられている（tests 1025-1034行・1064-1072行）。認証遮断6種も実行器定数と同値である。一方、反証点1は反証できてしまった。agy経路の応答model照合が和集合 ALLOWED_RESPONSE_MODELS を使っており（core.py 617行）、agyの実効許可model一覧が1値から2値へ広がっている。agy専用定数 _AGY_ALLOWED_RESPONSE_MODELS は和集合の材料にしか使われておらず、契約012 §7.1・§5.1-1が求める「agy値は移設のみ・一切変えない」に反する。実害の確率は低いが、これは黙って独立性・model同一性の守りが緩む種類の変更であり、契約が中心に置いた不変そのものが破れているため blocking とした。修正は617行の1行差し替えと、和集合を差し替えないagy照合の固定試験の追加で済む。反証点4は、model照合は許可・不許可の両向きが固定されている（tests 1124-1149行・1166-1179行）が、判定JSONの抽出不能・schema不適合による停止をclaude形式の合成streamで確かめる試験が無く、契約§9-6の両向き要求が片側未達である（F-3）。他に受容根拠pathのrepository内包検査の欠落、認証遮断の挙動試験が6種中1種、登録形の一般化が契約記述より浅い点を非blockingとして挙げた。
- 鮮度（Reviewer申告）：not_computable（expected `e32b525ddd54380602522f76c3536ac63eb538a73c57fdf35d95fc96c86cd57f`／observed `not_computable`）。理由：この実行環境は読み取り専用で端末commandを実行できないため、digestの機械計算ができない。読取り道具で開いた対象recordの見出し・§1 digest表・§3反証点4件・§5の別名依頼の記載は、起動promptが渡した対象path・期待SHA-256と整合しており、内容が別物である兆候はない。
- 未検査：§1 digest表10件および本依頼recordの実SHA-256の照合。端末commandを実行できないため機械計算は行っていない（freshnessは not_computable）。、試験の実行結果。対象51件・契約011の32件・G30 75件・正規全試験2,464件の終了コード0は、file読取りによる静的確認のみで、この環境では再実行していない。、契約012 §6保護対象（request_builder・bootstrap・実行器4 file・operation_contract_run.py 等）の基準commitからの差分0。gitを実行できないため未確認（operation_contract_run.py はG30登録箇所の読取りのみ実施）。、実装基準commit 6b2eacbb944f8f53f7e76ee16b63f5f278a2670f がHEADであることの確認。git実行不可のため、target.commit は依頼record冒頭の記載を転記した。、claude CLIの実挙動：--tools Read,Glob,Grep と --permission-mode dontAsk が実際に書込み道具を無効化するか、--allowedTools に列挙されていない Glob・Grep が実起動で使えるか。起動が行えないため未検証（許可model承認record §2.3のinit実測 tools=[Glob,Grep,Read]・permissionMode=dontAsk を間接根拠として読んだのみ）。、docs/development/prompts/reviewer-launch-run.md への導線追記の内容（契約012 §8-5）。反証点4件の対象外として読んでいない。、範囲外とされた事項（codex-cli backend・縦C・自由文類型・外部API直接送信経路・歴史的recordの書き換え・契約011成果物）。依頼record §5に従い検査していない。、§7.4残余risk 4点の受容の当否。§9-11の利用者判断事項として扱い、判断していない。

## findings

- F-1（severity: medium／blocking: true）：反証点1の不変が破れている。agy経路の応答model照合が、agy専用一覧ではなく和集合を使っている。core.py 617行で agy分岐が allowed_models = ALLOWED_RESPONSE_MODELS（＝("gemini-3.1-pro-high", "claude-opus-5")）を選び、742行の照合 any(model not in allowed_models) がその一覧で行われる。そのためagy起動でstreamが claude-opus-5 を名乗っても response_model_not_allowed で止まらず、agyの実効許可model一覧が1値から2値へ広がっている。契約012 §7.1「agy定義の値（引数・prompt・許可model・禁止環境変数）は一切変えない（移設のみ）」および §5.1-1「agyの現行値を不変のまま移設」に反する。46行の _AGY_ALLOWED_RESPONSE_MODELS は「agyの許可model一覧」と注記されながら和集合の組み立て（53-55行）以外に使われておらず、分岐での使い忘れと判断できる。契約011の互換記号としての和集合維持（§5.1-4）は、起動時の照合まで和集合にする根拠にはならない。要求modelは allowed_models[0] のため gemini-3.1-pro-high のままで、この点は不変。修正は617行を _AGY_ALLOWED_RESPONSE_MODELS へ替える1行で足りる。（根拠：`tools/reviewer_launch/core.py` 46行・53-55行・610-619行（特に617行）・742行）
- F-2（severity: medium／blocking: false）：反証点1の不変を機械で押さえる試験が無い。agy経路の試験は補助関数 _launch が ALLOWED_RESPONSE_MODELS を試験用値へ差し替える（202行）ため、F-1の広がりを検出できない。363-368行の test_allowed_models_fixed_to_approved_value と880-886行の test_union_allowed_models_preserved は定数の値（和集合）を固定するだけで、agy起動時にどの一覧で照合されるかを固定していない。反証点1が求める「agy値の不変の機械証明」は、定数の値の固定までしか成立していない。（根拠：`tests/test_reviewer_launch.py` 199-221行（_launch の202行）・363-368行・880-886行）
- F-3（severity: medium／blocking: false）：反証点4のうち、判定取り込み側の両向きが片側しか固定されていない。claude形式の合成streamを使う試験は、平文JSON成功（1124-1149行）・```json囲み成功（1151-1164行）・許可外modelでの停止（1166-1179行）の3件で、抽出不能や schema不適合による verdict_schema_nonconforming の停止を claude経路で確かめる試験が無い。同種の停止試験は agy経路の 524-553行にあるだけで、_claude_extract_verdict／_parse_json_text（core.py 510-547行）の失敗経路は未固定である。code自体は不適合時に停止し（raw保存は744行より前の728行で完了済み）、validate_verdict も backend共通で適用される（748-751行）ため実装の欠陥ではないが、契約012 §9-6が求める「JSON抽出・schema検証が両向きで働く」の試験固定は未達である。（根拠：`tests/test_reviewer_launch.py` 822-833行（合成stream）・1124-1179行・比較対象として524-553行）
- F-4（severity: low／blocking: false）：受容根拠pathの実在検査が、repository内であることを確かめていない。core.py 626-629行は (Path(repository) / acceptance_ref).is_file() だけを見るため、acceptance_ref に repository外の絶対pathを渡すと連結結果がその絶対pathとなり検査を通る。契約012 §7.3は受容根拠を「`--acceptance-ref <repo相対path>`」と定めており、repository内の（できればcommit済みの）recordであることまでは機械で担保されていない。起動の起点は利用者指示であるため実害は限定的だが、受容根拠の由来固定としては緩い。（根拠：`tools/reviewer_launch/core.py` 622-629行）
- F-5（severity: low／blocking: false）：認証遮断の挙動試験が6種のうち1種しか通っていない。960-988行の test_subagent_forbidden_env_stops は ANTHROPIC_API_KEY だけを設定して起動前停止を確かめる。agy側の同種試験（227-238行）が4種すべてをparametrizeしているのと非対称である。991-999行の同値性試験と core.py 357-360行の定数走査により実効は担保されるが、契約012 §9-5「6種が…存在時は起動前停止」の押さえとしては1種分の実証にとどまる。（根拠：`tests/test_reviewer_launch.py` 227-238行・960-999行）
- F-6（severity: low／blocking: false）：backend登録形の一般化が契約012 §5.1-1の記述より浅い。BACKENDS（core.py 114-127行）が持つのは provider・executable・declared_tier・read_tool_name の4項目だけで、契約が登録形へ含めるとした「引数組み立て関数・stream解析関数・許可model一覧・禁止環境変数一覧・requested model」は if backend_name == "claude-subagent" のname比較分岐（610-619行・633行・659-666行・683-686行・744-747行）で切り替えられている。現状の2 backendでは挙動は同じだが、第3 backend追加時に登録行の追加では済まず分岐の改修が要る。F-1の取り違えも、許可model一覧が登録形に入っていないこの構造が誘発している。（根拠：`tools/reviewer_launch/core.py` 114-127行・610-619行・633行・659-666行・683-686行・744-747行）
- F-7（severity: low／blocking: false）：_claude_observed_models のmessage内model読み取り（core.py 502-506行）に試験が無い。合成streamは top levelのmodelしか流さない（tests 822-833行）ため、実streamのassistantイベントが持つ message.model 経路（許可model承認record §2.3の実測転記に現れる形）は静的読解でしか確認できていない。code上は両方をmodels配列へ積むため許可外検出は働く。（根拠：`tools/reviewer_launch/core.py` 494-507行（tests/test_reviewer_launch.py 822-833行と対））

## 判定JSON（verbatim）

```json
{
  "findings": [
    {
      "blocking": true,
      "claim": "反証点1の不変が破れている。agy経路の応答model照合が、agy専用一覧ではなく和集合を使っている。core.py 617行で agy分岐が allowed_models = ALLOWED_RESPONSE_MODELS（＝(\"gemini-3.1-pro-high\", \"claude-opus-5\")）を選び、742行の照合 any(model not in allowed_models) がその一覧で行われる。そのためagy起動でstreamが claude-opus-5 を名乗っても response_model_not_allowed で止まらず、agyの実効許可model一覧が1値から2値へ広がっている。契約012 §7.1「agy定義の値（引数・prompt・許可model・禁止環境変数）は一切変えない（移設のみ）」および §5.1-1「agyの現行値を不変のまま移設」に反する。46行の _AGY_ALLOWED_RESPONSE_MODELS は「agyの許可model一覧」と注記されながら和集合の組み立て（53-55行）以外に使われておらず、分岐での使い忘れと判断できる。契約011の互換記号としての和集合維持（§5.1-4）は、起動時の照合まで和集合にする根拠にはならない。要求modelは allowed_models[0] のため gemini-3.1-pro-high のままで、この点は不変。修正は617行を _AGY_ALLOWED_RESPONSE_MODELS へ替える1行で足りる。",
      "evidence_location": "46行・53-55行・610-619行（特に617行）・742行",
      "evidence_path": "tools/reviewer_launch/core.py",
      "identifier": "F-1",
      "severity": "medium"
    },
    {
      "blocking": false,
      "claim": "反証点1の不変を機械で押さえる試験が無い。agy経路の試験は補助関数 _launch が ALLOWED_RESPONSE_MODELS を試験用値へ差し替える（202行）ため、F-1の広がりを検出できない。363-368行の test_allowed_models_fixed_to_approved_value と880-886行の test_union_allowed_models_preserved は定数の値（和集合）を固定するだけで、agy起動時にどの一覧で照合されるかを固定していない。反証点1が求める「agy値の不変の機械証明」は、定数の値の固定までしか成立していない。",
      "evidence_location": "199-221行（_launch の202行）・363-368行・880-886行",
      "evidence_path": "tests/test_reviewer_launch.py",
      "identifier": "F-2",
      "severity": "medium"
    },
    {
      "blocking": false,
      "claim": "反証点4のうち、判定取り込み側の両向きが片側しか固定されていない。claude形式の合成streamを使う試験は、平文JSON成功（1124-1149行）・```json囲み成功（1151-1164行）・許可外modelでの停止（1166-1179行）の3件で、抽出不能や schema不適合による verdict_schema_nonconforming の停止を claude経路で確かめる試験が無い。同種の停止試験は agy経路の 524-553行にあるだけで、_claude_extract_verdict／_parse_json_text（core.py 510-547行）の失敗経路は未固定である。code自体は不適合時に停止し（raw保存は744行より前の728行で完了済み）、validate_verdict も backend共通で適用される（748-751行）ため実装の欠陥ではないが、契約012 §9-6が求める「JSON抽出・schema検証が両向きで働く」の試験固定は未達である。",
      "evidence_location": "822-833行（合成stream）・1124-1179行・比較対象として524-553行",
      "evidence_path": "tests/test_reviewer_launch.py",
      "identifier": "F-3",
      "severity": "medium"
    },
    {
      "blocking": false,
      "claim": "受容根拠pathの実在検査が、repository内であることを確かめていない。core.py 626-629行は (Path(repository) / acceptance_ref).is_file() だけを見るため、acceptance_ref に repository外の絶対pathを渡すと連結結果がその絶対pathとなり検査を通る。契約012 §7.3は受容根拠を「`--acceptance-ref <repo相対path>`」と定めており、repository内の（できればcommit済みの）recordであることまでは機械で担保されていない。起動の起点は利用者指示であるため実害は限定的だが、受容根拠の由来固定としては緩い。",
      "evidence_location": "622-629行",
      "evidence_path": "tools/reviewer_launch/core.py",
      "identifier": "F-4",
      "severity": "low"
    },
    {
      "blocking": false,
      "claim": "認証遮断の挙動試験が6種のうち1種しか通っていない。960-988行の test_subagent_forbidden_env_stops は ANTHROPIC_API_KEY だけを設定して起動前停止を確かめる。agy側の同種試験（227-238行）が4種すべてをparametrizeしているのと非対称である。991-999行の同値性試験と core.py 357-360行の定数走査により実効は担保されるが、契約012 §9-5「6種が…存在時は起動前停止」の押さえとしては1種分の実証にとどまる。",
      "evidence_location": "227-238行・960-999行",
      "evidence_path": "tests/test_reviewer_launch.py",
      "identifier": "F-5",
      "severity": "low"
    },
    {
      "blocking": false,
      "claim": "backend登録形の一般化が契約012 §5.1-1の記述より浅い。BACKENDS（core.py 114-127行）が持つのは provider・executable・declared_tier・read_tool_name の4項目だけで、契約が登録形へ含めるとした「引数組み立て関数・stream解析関数・許可model一覧・禁止環境変数一覧・requested model」は if backend_name == \"claude-subagent\" のname比較分岐（610-619行・633行・659-666行・683-686行・744-747行）で切り替えられている。現状の2 backendでは挙動は同じだが、第3 backend追加時に登録行の追加では済まず分岐の改修が要る。F-1の取り違えも、許可model一覧が登録形に入っていないこの構造が誘発している。",
      "evidence_location": "114-127行・610-619行・633行・659-666行・683-686行・744-747行",
      "evidence_path": "tools/reviewer_launch/core.py",
      "identifier": "F-6",
      "severity": "low"
    },
    {
      "blocking": false,
      "claim": "_claude_observed_models のmessage内model読み取り（core.py 502-506行）に試験が無い。合成streamは top levelのmodelしか流さない（tests 822-833行）ため、実streamのassistantイベントが持つ message.model 経路（許可model承認record §2.3の実測転記に現れる形）は静的読解でしか確認できていない。code上は両方をmodels配列へ積むため許可外検出は働く。",
      "evidence_location": "494-507行（tests/test_reviewer_launch.py 822-833行と対）",
      "evidence_path": "tools/reviewer_launch/core.py",
      "identifier": "F-7",
      "severity": "low"
    }
  ],
  "freshness": {
    "expected": "e32b525ddd54380602522f76c3536ac63eb538a73c57fdf35d95fc96c86cd57f",
    "observed": "not_computable",
    "reason": "この実行環境は読み取り専用で端末commandを実行できないため、digestの機械計算ができない。読取り道具で開いた対象recordの見出し・§1 digest表・§3反証点4件・§5の別名依頼の記載は、起動promptが渡した対象path・期待SHA-256と整合しており、内容が別物である兆候はない。",
    "result": "not_computable"
  },
  "reviewer": {
    "model": "claude-opus-5",
    "provider": "anthropic"
  },
  "summary": "反証点2（tier受容機構）・反証点3（claude起動固定形と訂正3件）は反証できず、実装は依頼recordの主張どおりだった。tier受容は、別プロバイダがTier 1で従来どおり通り（core.py 371-372行）、claude-subagentは --accept-tier の欠落・不一致で reviewer_not_independent_tier、一致でも受容根拠fileが無ければ acceptance_reference_missing で、いずれも子processを起動する前に止まる（tests 889-930行が facade.calls == [] で実効を固定）。一致かつ実在のときだけ起動へ進み、起動recordへ tier・accept_tier・acceptance_reference が入り（core.py 687-708行、tests 1124-1149行）、判定recordにも Tier が刻まれる（record.py 246行）。claude固定引数は Read,Glob,Grep のみで、書込み道具も --dangerously-skip-permissions 類も無く、両向きで固定されている（core.py 323-354行、tests 1075-1110行）。訂正3件も契約v2＋overlayどおりで、--verbose は stream-json 直後、通過変数9種と抑制注入9種は実行器の値と同値であることが試験で固定され（tests 991-1010行・1037-1048行）、agy子環境には USER も注入keyも入らないことが実効的に押さえられている（tests 1025-1034行・1064-1072行）。認証遮断6種も実行器定数と同値である。一方、反証点1は反証できてしまった。agy経路の応答model照合が和集合 ALLOWED_RESPONSE_MODELS を使っており（core.py 617行）、agyの実効許可model一覧が1値から2値へ広がっている。agy専用定数 _AGY_ALLOWED_RESPONSE_MODELS は和集合の材料にしか使われておらず、契約012 §7.1・§5.1-1が求める「agy値は移設のみ・一切変えない」に反する。実害の確率は低いが、これは黙って独立性・model同一性の守りが緩む種類の変更であり、契約が中心に置いた不変そのものが破れているため blocking とした。修正は617行の1行差し替えと、和集合を差し替えないagy照合の固定試験の追加で済む。反証点4は、model照合は許可・不許可の両向きが固定されている（tests 1124-1149行・1166-1179行）が、判定JSONの抽出不能・schema不適合による停止をclaude形式の合成streamで確かめる試験が無く、契約§9-6の両向き要求が片側未達である（F-3）。他に受容根拠pathのrepository内包検査の欠落、認証遮断の挙動試験が6種中1種、登録形の一般化が契約記述より浅い点を非blockingとして挙げた。",
  "target": {
    "commit": "6b2eacbb944f8f53f7e76ee16b63f5f278a2670f",
    "path": "records/session-handoffs/2026-08-17-claude-subagent-backend-implementation-completion-review-subagent-request-v1.md"
  },
  "unexamined": [
    "§1 digest表10件および本依頼recordの実SHA-256の照合。端末commandを実行できないため機械計算は行っていない（freshnessは not_computable）。",
    "試験の実行結果。対象51件・契約011の32件・G30 75件・正規全試験2,464件の終了コード0は、file読取りによる静的確認のみで、この環境では再実行していない。",
    "契約012 §6保護対象（request_builder・bootstrap・実行器4 file・operation_contract_run.py 等）の基準commitからの差分0。gitを実行できないため未確認（operation_contract_run.py はG30登録箇所の読取りのみ実施）。",
    "実装基準commit 6b2eacbb944f8f53f7e76ee16b63f5f278a2670f がHEADであることの確認。git実行不可のため、target.commit は依頼record冒頭の記載を転記した。",
    "claude CLIの実挙動：--tools Read,Glob,Grep と --permission-mode dontAsk が実際に書込み道具を無効化するか、--allowedTools に列挙されていない Glob・Grep が実起動で使えるか。起動が行えないため未検証（許可model承認record §2.3のinit実測 tools=[Glob,Grep,Read]・permissionMode=dontAsk を間接根拠として読んだのみ）。",
    "docs/development/prompts/reviewer-launch-run.md への導線追記の内容（契約012 §8-5）。反証点4件の対象外として読んでいない。",
    "範囲外とされた事項（codex-cli backend・縦C・自由文類型・外部API直接送信経路・歴史的recordの書き換え・契約011成果物）。依頼record §5に従い検査していない。",
    "§7.4残余risk 4点の受容の当否。§9-11の利用者判断事項として扱い、判断していない。"
  ],
  "verdict": "rejected",
  "verdict_note_not_in_schema": null
}
```
