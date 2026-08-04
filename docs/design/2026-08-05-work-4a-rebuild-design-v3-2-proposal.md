# Work 4A Rebuild Design v3.2 Proposal

状態：`awaiting_human_approval`
対象：Work 4A Reusable Routine Ledger
基準文書：`docs/design/2026-08-04-work-4a-rebuild-design-v3-1-amendment.md`
関連メモ：`docs/design/2026-08-05-work-4a-llm-analysis-context-memo.md`
承認記録（予定）：`DEC-WORK4A-REBUILD-DESIGN-005`

これはv3.1を置換しない差分提案である。目的は、LLMによるDisposition Proposalの前に、
処置labelを人が判断しやすい機械的特徴をRoutine Profileへ追加することである。

承認されるまで、実装、test、Routine Profileの再生成、外部DATA_ROOTへの書込み、
LLMによるDisposition Proposal生成を行わない。

## 1. 背景

v3.1のRoutine Profileは966件について、symbol ID、signature、行数、docstring、静的参照数、
構文的操作痕跡、AST構造一致groupを抽出できた。しかし、`reuse`、`extend`、`merge`、`split`、
`as_is`を判断するには、呼出関係、例外の流れ、責務の分割度、Testとの結び付き、公開性の情報が不足する。

この提案は、LLMへ無関係な全sourceを一括投入する方式を採らない。機械抽出した判断カードを先に渡し、
情報が不足する場合だけ限定した周辺codeを渡す三層方式を採る。

## 2. 変更しない境界

- Routine Profileは機械事実のみを持つ。LLM由来の説明やlabelを混入させない。
- Disposition Proposalは非権威の外部recordであり、Human Decisionを置き換えない。
- LLM提案からEntry、Relation、Baselineを自動生成しない。
- 既存Routine Profileは書き換えず、追加特徴を含むProfileをnew-onlyで作る。
- 未検出は「存在しない」の証明ではない。各featureの検出範囲と限界をrecordへ明示する。

## 3. 新しいRoutine Profile v2

`schema_version`を2、`extraction_rule_version`を3へ上げる。Profile v1は歴史recordとして保持する。

### 3.1 直接呼出関係

各routineへ次を追加する。

- `direct_callee_symbol_ids`：同一source universe内で、構文上直接解決できた呼出先
- `direct_caller_symbol_ids`：同じ規則で逆引きした呼出元
- `unresolved_direct_call_count`：名前解決できなかった直接呼出数
- `call_graph_detection`：別名import、動的属性、reflection、callback、`eval`／`exec`を追わないことを明記

`direct_callee_symbol_ids`と`direct_caller_symbol_ids`に記録できるのは、同一Profileにあるsymbol IDだけとする。
解決済みIDがProfileに無い場合は`profile_reference_unresolved`で停止する。

### 3.2 例外の流れ

各routineへ次を追加する。

- `raised_exception_names`：`raise`文に構文上現れる例外名
- `caught_exception_names`：`except`節に構文上現れる例外名
- `bare_except_count`
- `exception_detection`：例外の実行時型、呼出先から伝播する例外、動的生成例外を確定しないことを明記

例外名は解決不能でも文字列として保持してよい。ただし、解決済みsymbol IDと混同しない。

### 3.3 責務分割度

意味的な責務数を機械が断定しない。代わりに、分割検討のための構文指標を持つ。

- `branch_count`：`if`、`match`、loop、comprehensionの分岐数
- `return_count`
- `raise_count`
- `try_count`
- `max_nesting_depth`
- `effect_marker_count`
- `complexity_signal`：上記値から決定的に算出する`low`／`medium`／`high`

`complexity_signal`は`split`の結論ではなく、LLMとHumanが周辺codeを読む優先度である。

### 3.4 Testとの結び付き

`tests/`はsource universeに含めない。Profileに次の独立したTest参照情報を持つ。

- `direct_test_reference_paths`：test sourceのASTから、対象symbolへの直接参照を解決できたtest fileの相対path
- `direct_test_reference_count`
- `test_reference_detection`：同一repositoryの`tests/**/*.py`だけを対象とし、文字列参照、fixture経由、動的import、
  統合testの間接検証を網羅しないことを明記

test pathはproject root相対で記録し、`tests/`から脱出してはならない。

### 3.5 公開APIらしさ

公開性を最終決定しない。以下の構文的・静的な指標だけを記録する。

- `is_private_name`：名前が`_`始まりか
- `is_exported_by_all`：同一moduleの`__all__`に含まれるか
- `cross_package_caller_count`：別packageからの直接呼出数
- `cli_entrypoint_marker`：`if __name__ == "__main__"`、argparse／click／typerの直接登録に該当するか
- `public_api_signal`：上記指標から決定的に算出する`low`／`medium`／`high`

`public_api_signal`は公開契約の証明ではない。外部利用、plugin、設定file、reflectionによる利用は検出範囲外である。

### 3.6 構造一致と意味的重複候補

`structural_match_group_id`は引き続き、正規化ASTの完全一致だけを表す。これは統合の結論ではない。

LLMへ意味的重複を検討させる候補集合として、各routineに次を追加する。

- `semantic_comparison_candidate_ids`：同一package、同一`structural_match_group_id`、入出力形、呼出先、
  例外・操作痕跡の重なりから決定的に選ぶ上限10件のsymbol ID
- `semantic_candidate_selection_reason`：候補に選んだ機械的理由

この候補集合は、LLMが読む比較対象を絞るためだけに使う。`merge`の根拠または結論にしない。

## 4. 判断カード

LLMへ最初に渡す判断カードは、Profile v2の値から作る。最低限、次を含める。

- symbol ID、code reference、signature、docstring
- 呼出元・呼出先と未解決呼出数
- raise・catch関係
- 責務分割度の構文指標
- 構文的操作痕跡
- 関連Test
- 公開API指標
- 構造一致groupと意味的比較候補

判断カードだけで根拠が足りない場合に限り、対象routine、直接caller/callee、比較候補、関連Testの
source本文を追加する。全source treeを一括で渡してはならない。

## 5. Disposition Proposalへの影響

Disposition Proposal v1の`evidence_refs`は、Profile v2の新fieldまたは既存`code_reference`を参照できる。
LLMは根拠が不足する場合、`recommended_disposition: null`と`human_review_required: true`を返す。

LLMの意味的重複候補、処置label、説明はすべてadvisoryである。機械特徴との不一致は停止ではなく、
Humanが確認すべき不確実性として記録する。ただし存在しないsymbol IDまたは範囲外のTest pathを
参照するProposalは従来どおり拒否する。

## 6. 受入条件

v3.1の受入条件を維持し、次を追加する。

- J1：同一source universe内の直接caller/calleeだけを相互に記録できる。
- J2：alias、動的呼出、reflectionが未解決呼出として記録され、解決済みと偽装されない。
- J3：raise・catch、bare exceptを構文上抽出でき、伝播例外を確定しない。
- J4：分割度の各構文指標と`complexity_signal`を決定的に生成できる。
- J5：`tests/**/*.py`内の直接参照だけを記録し、範囲外pathを拒否する。
- J6：`__all__`、cross-package呼出、CLI入口からpublic API指標を生成できる。
- J7：構造一致groupだけで`merge`を確定しない。
- J8：意味的比較候補は同一Profileのsymbol IDだけから上限10件を決定的に選ぶ。
- J9：Profile v1とv2を併存して検証でき、どちらも書き換えない。
- J10：判断カードが不足する場合、限定した周辺codeだけを選べる。全source treeを選ばない。

## 7. 実装順序

1. 本提案をHumanが承認する。
2. Policy artifact v3で抽出語彙、検出範囲、上限値を固定する。
3. J1〜J10をREDで固定する。
4. Profile v2を実装しGREENにする。
5. 実sourceからProfile v2をnew-onlyで生成し、機械抽出結果を提示する。
6. Humanが確認した後、LLMによるDisposition Proposalを別承認で生成する。

## 8. Human判断が必要な点

1. `semantic_comparison_candidate_ids`の上限を10件とするか。
2. `complexity_signal`の閾値（現案はPolicy v3で決定する）。
3. Test参照を直接AST参照だけに限定するか。
4. `public_api_signal`を`low`／`medium`／`high`の3段階とするか。
