# Reviewer起動アダプタ 判定record（機械転記） e2e-012-002

- Reviewer：provider `anthropic`／model `claude-opus-5`（アダプタ照合済み）
- 独立性：Tier 3（アダプタ判定。契約010 §5.1-4）
- 起動方式：headless機械起動（backend `claude-subagent`）
- 依頼record：`records/session-handoffs/2026-08-17-claude-subagent-backend-implementation-completion-rereview-subagent-request-v1.md`（SHA-256 `2e3e9c29f7220727c5c1dfece5ff422a314bc5cff6fd6bdf930d0008ae68507a`）
- 未加工出力：保存先種別 `private_root_immutable_store`、SHA-256 `20755a3515db63d14adbc661bff7ff28978c92767df7b9b2bb361070c0fefd7f`、参照権限：repo外私有領域（利用者とClaude）
- 実行識別子：`e2e-012-002`
- 判定：**verified_with_findings**
- 判定要旨：反証点1〜4のいずれも反証できず、F-1の修正は実効的である。agy分岐の応答model照合は core.py 619行で _AGY_ALLOWED_RESPONSE_MODELS（46行・1値）へ差し替わり、744行の照合はこの一覧で行われる。和集合 ALLOWED_RESPONSE_MODELS は53-55行の組み立てと契約011側のimport（tools/request_builder/core.py 14行）だけに残り、起動経路のどこからも参照されていない（repository全体のgrepで、起動側の参照は612行のsubagent一覧と619行のagy一覧のみ）。固定試験 test_agy_model_check_uses_agy_list_not_union（tests 363-393行）は、agy専用一覧を1値に、和集合を2値に別々へ差し替えたうえで claude-opus-5 を名乗るstreamを流し、response_model_not_allowed での停止を要求する。もし619行が和集合へ戻れば起動は成功して例外が出ず試験が落ちるため、この試験は差し替えを機械的に検出できる。反証点2の回帰も無い。差し替え対象は補助関数 _launch（202行）と個別試験3件（348行・413行・442行）の計4箇所で、いずれも旧来と同じ値（TEST_MODEL または空tuple）を同じ意味で与える。要求modelは allowed_models[0] のままなので agy起動の要求modelは一覧先頭で不変（tests 502-524行が result[model]==TEST_MODEL を維持）、空一覧時は632-633行の allowed_models_unfixed が project束縛解決（635行）より前に働き、停止理由も従来どおりである（tests 340-360行）。空検査は和集合ではなくbackend別一覧に対して行われるようになったぶん、むしろ安全側へ寄っており新たな穴は見当たらない。反証点3のF-3対処は試験2件が実在し実効である。結果本文にJSONが無い場合（tests 1070-1083行、平文「構造化出力はありません。」→ core.py 510-529行の直接解析・fence・括弧範囲がすべて失敗して停止）と、JSONだがschema必須鍵を欠く場合（tests 1086-1097行、{"verdict":"verified"} → record.py 71-72行が reviewer 等の欠落で VerdictInvalid、core.py 750-753行が verdict_schema_nonconforming へ変換）の双方が固定され、契約§9-6の両向き要求は満たされた。未加工出力の保存が停止前に完了していることは前者の試験が raw fileの実在（run_id/reviewer.raw.json＝raw_review_store.py 119-122行の命名）で押さえているが、後者には同じ確認が無く、これを非blockingのR-1として挙げた。反証点4の前回成立事項も維持されている。tier受容は accept_tier 欠落・不一致で reviewer_not_independent_tier、一致でも受容根拠fileが無ければ acceptance_reference_missing となり、いずれも facade.calls == [] で起動前停止が固定されたまま（tests 922-963行）、成功時は起動recordへ tier・accept_tier・acceptance_reference が入る（tests 1187-1211行）。claude固定引数は Read,Glob,Grep のみで書込み道具も危険旗も無く（tests 1138-1173行）、訂正3件（--verbose の位置・通過変数9種・抑制注入9種）と認証遮断6種の実行器定数との同値も従来どおり固定されている（tests 1024-1043行・1100-1124行）。実装差分がF-1〜F-3対処に限定されている点は、gitを実行できないため直接確認できないが、前回判定recordが引用した行番号がすべて一定量のshiftで現行fileへ対応する（core.pyは+2、tests は挿入2箇所ぶんの+33／+63）ことから、注記2行と1行の差し替え、および試験3件の追加のほかに変更が入った形跡は読み取れない。blocking所見は0件で、非blockingはR-1（schema不適合側の試験にraw保存確認が無い）とR-2（互換記号として残る和集合が request_builder の照合を2値にしている点。契約§5.1-4の設計どおりでHuman仕分け向けの情報）の2件である。
- 鮮度（Reviewer申告）：not_computable（expected `2e3e9c29f7220727c5c1dfece5ff422a314bc5cff6fd6bdf930d0008ae68507a`／observed `not_computable`）。理由：この実行環境は読み取り専用で端末commandを実行できないため、SHA-256の機械計算ができない。読取り道具で開いた対象recordは、見出し（契約012実装 F-1〜F-3修正後の独立確認依頼）・§1の13行digest表（前回判定recordを含む）・§3の反証点4件・§5の別名依頼（slug末尾-subagent）の記載が、起動promptの渡した対象pathと期待SHA-256の文脈と整合しており、内容が別物である兆候はない。
- 未検査：§1 digest表13件および本依頼recordの実SHA-256の照合。端末commandを実行できないため機械計算は行っていない（freshnessは not_computable）。、実装差分がF-1〜F-3対処に限定されていることのgitによる直接確認。git実行不可のため、前回判定recordの引用行番号と現行fileの行位置の整合（core.pyは617行以降が一律+2行、tests側は363行付近で+33行・1070行付近で+30行の一括shiftとして矛盾なく説明できること）による静的な状況証拠までしか取れていない。基準commit b55903d076fa9435061e3eadc8d96bb1ae336316 がHEADであることも未確認で、target.commit は依頼record §冒頭の記載を転記した。、試験の実行結果。正規全試験2,467件の終了コード0は依頼recordの記載であり、この環境では再実行していない（試験codeの静的読解のみ）。、契約012 §6保護対象（request_builder・bootstrap・実行器4 file・operation_contract_run.py 等）の基準commitからの差分0。gitを実行できないため未確認。、claude CLIおよびagy CLIの実挙動（道具制限・許可の実効、stream実形式）。起動が行えないため未検証で、合成streamを用いた試験の読解にとどまる。、docs/development/prompts/reviewer-launch-run.md の導線記述。反証点4件の対象外として読んでいない。、前回判定のF-4〜F-7（受容根拠pathの内包検査・認証遮断挙動試験の対称性・backend登録形の深さ・応答内model欄の試験）。依頼record §5により再指摘不要とされたため、修正の有無を評価していない。、範囲外事項（codex-cli backend・縦C・自由文類型・外部API直接送信経路・歴史的recordの書き換え・契約011成果物の変更）。依頼record §5に従い検査していない。、§7.4残余risk 4点の受容の当否。§9-11の利用者判断事項として扱い、判断していない。

## findings

- R-1（severity: low／blocking: false）：反証点3が求めた2件のうち、schema不適合側の試験に「未加工出力の保存が停止前に完了している」ことの確認が入っていない。1070-1083行の test_subagent_result_without_json_stops は停止理由 verdict_schema_nonconforming に加えて raw_path.is_file() を確かめているが、1086-1097行の test_subagent_schema_nonconforming_verdict_stops は停止理由だけを確かめ、raw保存の確認が無い。実装上は raw保存（core.py 730-740行）が model照合（744行）・判定抽出（747行）・validate_verdict（751行）よりも前に一度だけ行われる共通経路であり、前者の試験が同じ経路で保存を押さえているため実害は無い。依頼recordの文言（両向きの双方で保存完了まで固定する）に対して、片方が理由のみの固定にとどまる差である。（根拠：`tests/test_reviewer_launch.py` 1070-1083行（raw確認あり）・1086-1097行（raw確認なし）／対照：tools/reviewer_launch/core.py 730-753行）
- R-2（severity: low／blocking: false）：F-1修正で和集合 ALLOWED_RESPONSE_MODELS は起動時照合から外れたが、契約011互換の記号として残った和集合は現在2値（gemini-3.1-pro-high・claude-opus-5）であり、その唯一の実利用先である request_builder の照合では、依頼recordのmodel欄に claude-opus-5 と書かれても検査を通る状態になっている（tools/request_builder/core.py 377行の `model_match.group(1) not in ALLOWED_RESPONSE_MODELS`。245行の既定値は和集合先頭＝gemini-3.1-pro-high のままで不変）。これは契約v2 §5.1-4が定めた「全backend許可modelの和集合として名称・tuple意味を維持する」という互換設計の当然の帰結であり、契約違反ではない。契約011成果物は本レビューの範囲外のため変更は求めないが、和集合が「組み立て器の入力検査基準」として残る限り、model同一性の守りは起動側（agy専用一覧）だけが厳密であるという構造をHuman仕分けの材料として記す。（根拠：`tools/reviewer_launch/core.py` 46行・50行・53-55行（和集合の組み立て）／tools/request_builder/core.py 14行・234行・245行・377行）

## 判定JSON（verbatim）

```json
{
  "findings": [
    {
      "blocking": false,
      "claim": "反証点3が求めた2件のうち、schema不適合側の試験に「未加工出力の保存が停止前に完了している」ことの確認が入っていない。1070-1083行の test_subagent_result_without_json_stops は停止理由 verdict_schema_nonconforming に加えて raw_path.is_file() を確かめているが、1086-1097行の test_subagent_schema_nonconforming_verdict_stops は停止理由だけを確かめ、raw保存の確認が無い。実装上は raw保存（core.py 730-740行）が model照合（744行）・判定抽出（747行）・validate_verdict（751行）よりも前に一度だけ行われる共通経路であり、前者の試験が同じ経路で保存を押さえているため実害は無い。依頼recordの文言（両向きの双方で保存完了まで固定する）に対して、片方が理由のみの固定にとどまる差である。",
      "evidence_location": "1070-1083行（raw確認あり）・1086-1097行（raw確認なし）／対照：tools/reviewer_launch/core.py 730-753行",
      "evidence_path": "tests/test_reviewer_launch.py",
      "identifier": "R-1",
      "severity": "low"
    },
    {
      "blocking": false,
      "claim": "F-1修正で和集合 ALLOWED_RESPONSE_MODELS は起動時照合から外れたが、契約011互換の記号として残った和集合は現在2値（gemini-3.1-pro-high・claude-opus-5）であり、その唯一の実利用先である request_builder の照合では、依頼recordのmodel欄に claude-opus-5 と書かれても検査を通る状態になっている（tools/request_builder/core.py 377行の `model_match.group(1) not in ALLOWED_RESPONSE_MODELS`。245行の既定値は和集合先頭＝gemini-3.1-pro-high のままで不変）。これは契約v2 §5.1-4が定めた「全backend許可modelの和集合として名称・tuple意味を維持する」という互換設計の当然の帰結であり、契約違反ではない。契約011成果物は本レビューの範囲外のため変更は求めないが、和集合が「組み立て器の入力検査基準」として残る限り、model同一性の守りは起動側（agy専用一覧）だけが厳密であるという構造をHuman仕分けの材料として記す。",
      "evidence_location": "46行・50行・53-55行（和集合の組み立て）／tools/request_builder/core.py 14行・234行・245行・377行",
      "evidence_path": "tools/reviewer_launch/core.py",
      "identifier": "R-2",
      "severity": "low"
    }
  ],
  "freshness": {
    "expected": "2e3e9c29f7220727c5c1dfece5ff422a314bc5cff6fd6bdf930d0008ae68507a",
    "observed": "not_computable",
    "reason": "この実行環境は読み取り専用で端末commandを実行できないため、SHA-256の機械計算ができない。読取り道具で開いた対象recordは、見出し（契約012実装 F-1〜F-3修正後の独立確認依頼）・§1の13行digest表（前回判定recordを含む）・§3の反証点4件・§5の別名依頼（slug末尾-subagent）の記載が、起動promptの渡した対象pathと期待SHA-256の文脈と整合しており、内容が別物である兆候はない。",
    "result": "not_computable"
  },
  "reviewer": {
    "model": "claude-opus-5",
    "provider": "anthropic"
  },
  "summary": "反証点1〜4のいずれも反証できず、F-1の修正は実効的である。agy分岐の応答model照合は core.py 619行で _AGY_ALLOWED_RESPONSE_MODELS（46行・1値）へ差し替わり、744行の照合はこの一覧で行われる。和集合 ALLOWED_RESPONSE_MODELS は53-55行の組み立てと契約011側のimport（tools/request_builder/core.py 14行）だけに残り、起動経路のどこからも参照されていない（repository全体のgrepで、起動側の参照は612行のsubagent一覧と619行のagy一覧のみ）。固定試験 test_agy_model_check_uses_agy_list_not_union（tests 363-393行）は、agy専用一覧を1値に、和集合を2値に別々へ差し替えたうえで claude-opus-5 を名乗るstreamを流し、response_model_not_allowed での停止を要求する。もし619行が和集合へ戻れば起動は成功して例外が出ず試験が落ちるため、この試験は差し替えを機械的に検出できる。反証点2の回帰も無い。差し替え対象は補助関数 _launch（202行）と個別試験3件（348行・413行・442行）の計4箇所で、いずれも旧来と同じ値（TEST_MODEL または空tuple）を同じ意味で与える。要求modelは allowed_models[0] のままなので agy起動の要求modelは一覧先頭で不変（tests 502-524行が result[model]==TEST_MODEL を維持）、空一覧時は632-633行の allowed_models_unfixed が project束縛解決（635行）より前に働き、停止理由も従来どおりである（tests 340-360行）。空検査は和集合ではなくbackend別一覧に対して行われるようになったぶん、むしろ安全側へ寄っており新たな穴は見当たらない。反証点3のF-3対処は試験2件が実在し実効である。結果本文にJSONが無い場合（tests 1070-1083行、平文「構造化出力はありません。」→ core.py 510-529行の直接解析・fence・括弧範囲がすべて失敗して停止）と、JSONだがschema必須鍵を欠く場合（tests 1086-1097行、{\"verdict\":\"verified\"} → record.py 71-72行が reviewer 等の欠落で VerdictInvalid、core.py 750-753行が verdict_schema_nonconforming へ変換）の双方が固定され、契約§9-6の両向き要求は満たされた。未加工出力の保存が停止前に完了していることは前者の試験が raw fileの実在（run_id/reviewer.raw.json＝raw_review_store.py 119-122行の命名）で押さえているが、後者には同じ確認が無く、これを非blockingのR-1として挙げた。反証点4の前回成立事項も維持されている。tier受容は accept_tier 欠落・不一致で reviewer_not_independent_tier、一致でも受容根拠fileが無ければ acceptance_reference_missing となり、いずれも facade.calls == [] で起動前停止が固定されたまま（tests 922-963行）、成功時は起動recordへ tier・accept_tier・acceptance_reference が入る（tests 1187-1211行）。claude固定引数は Read,Glob,Grep のみで書込み道具も危険旗も無く（tests 1138-1173行）、訂正3件（--verbose の位置・通過変数9種・抑制注入9種）と認証遮断6種の実行器定数との同値も従来どおり固定されている（tests 1024-1043行・1100-1124行）。実装差分がF-1〜F-3対処に限定されている点は、gitを実行できないため直接確認できないが、前回判定recordが引用した行番号がすべて一定量のshiftで現行fileへ対応する（core.pyは+2、tests は挿入2箇所ぶんの+33／+63）ことから、注記2行と1行の差し替え、および試験3件の追加のほかに変更が入った形跡は読み取れない。blocking所見は0件で、非blockingはR-1（schema不適合側の試験にraw保存確認が無い）とR-2（互換記号として残る和集合が request_builder の照合を2値にしている点。契約§5.1-4の設計どおりでHuman仕分け向けの情報）の2件である。",
  "target": {
    "commit": "b55903d076fa9435061e3eadc8d96bb1ae336316",
    "path": "records/session-handoffs/2026-08-17-claude-subagent-backend-implementation-completion-rereview-subagent-request-v1.md"
  },
  "unexamined": [
    "§1 digest表13件および本依頼recordの実SHA-256の照合。端末commandを実行できないため機械計算は行っていない（freshnessは not_computable）。",
    "実装差分がF-1〜F-3対処に限定されていることのgitによる直接確認。git実行不可のため、前回判定recordの引用行番号と現行fileの行位置の整合（core.pyは617行以降が一律+2行、tests側は363行付近で+33行・1070行付近で+30行の一括shiftとして矛盾なく説明できること）による静的な状況証拠までしか取れていない。基準commit b55903d076fa9435061e3eadc8d96bb1ae336316 がHEADであることも未確認で、target.commit は依頼record §冒頭の記載を転記した。",
    "試験の実行結果。正規全試験2,467件の終了コード0は依頼recordの記載であり、この環境では再実行していない（試験codeの静的読解のみ）。",
    "契約012 §6保護対象（request_builder・bootstrap・実行器4 file・operation_contract_run.py 等）の基準commitからの差分0。gitを実行できないため未確認。",
    "claude CLIおよびagy CLIの実挙動（道具制限・許可の実効、stream実形式）。起動が行えないため未検証で、合成streamを用いた試験の読解にとどまる。",
    "docs/development/prompts/reviewer-launch-run.md の導線記述。反証点4件の対象外として読んでいない。",
    "前回判定のF-4〜F-7（受容根拠pathの内包検査・認証遮断挙動試験の対称性・backend登録形の深さ・応答内model欄の試験）。依頼record §5により再指摘不要とされたため、修正の有無を評価していない。",
    "範囲外事項（codex-cli backend・縦C・自由文類型・外部API直接送信経路・歴史的recordの書き換え・契約011成果物の変更）。依頼record §5に従い検査していない。",
    "§7.4残余risk 4点の受容の当否。§9-11の利用者判断事項として扱い、判断していない。"
  ],
  "verdict": "verified_with_findings"
}
```
