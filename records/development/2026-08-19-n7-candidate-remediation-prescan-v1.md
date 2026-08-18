# N7未充足候補4件の是正 事前走査 v1

- 記録日：2026-08-19
- 指示者：利用者（Human）。文言「N7未充足4件の是正を1作業単位で実施。作業票と事前走査から入って」
  （2026-08-19 chat）
- 記録者：Claude
- 上位：仕分けrecord`records/development/2026-08-19-safe-storage-entry-exit-code-triage-decision-v1.md`
  §4a（訂正済みの観測＝未充足4件）
- 基準commit：`8d9bb2c`（本走査の生成物2件を除きclean）
- 実測：測定ブロック
  `records/development/2026-08-19-n7-candidate-remediation-prescan-measurements-v1.md`
  （guard付き・全4entry二重実行一致）

## 1. 実測から確定した事実

1. **対象4件は同一commit由来**：`ic-contract-014-canonical-sequence-gaps-001`・
   `ic-launch-metrics-acceptance-title-001`・`ic-session-log-exit-code-doc-drift-001`・
   `ic-session-log-exit-code-vocabulary-001`（いずれも初回commit `3b76b97`＝2026-08-18の
   RQ2副産物登録・改版数1）。検証器を通さない手書き登録が根因（AGENTS §3の台帳規律の違反例）。
2. **ずれは同型で機械是正できる**：全4件とも (a) 余分欄`related_candidates`、(b) 出所束縛
   `source_identity`に余分key`section`、(c) 無効な分類語彙（3件=`documentation`・1件=`design`）。
   欠け欄0・route語彙は全件有効。
3. **意味内容の束縛は全件生存**：出所record（RQ2裁定record v2）のpath・SHA-256一致、
   evidence_refsの束縛も全件一致。是正は**形だけ**の問題で、内容の再判断は不要。
4. **N7は是正前RED**：単独実行でexit 1（`1 failed`）。是正後の合格がそのままGREEN判定になる
   （既存保護試験が赤→緑の役を果たすため、新設試験は不要）。
5. 仕分け結果はMarkdown記録（2026-08-18の副産物仕分けrecord・launch含む）に存在する。
   candidate fileの是正で同recordの候補digest参照はstale（版の前進）になる——束縛照合の
   `history_match`型で追跡可能（運用集計の既知パターン）。

## 2. 設計（作業票へ渡す論点）

1. **是正方式3案**：案A＝**形の是正**（各fileを正規形へ機械再生成・意味内容保存・v1のまま
   置き換え）→条件(a)＝validator合格で充足。案B＝V4決定化で条件(c)充足（形の不正が台帳に残置
   されるため不採用）。案C＝A＋B（Markdown裁定の転記確認というHuman往復が増え範囲最大）。
   **採用候補は案A**（最小・原則「台帳は機械検証可能な形」へ直結）。
2. **意味内容の保存規則**：`related_candidates`の値と`section`の値は削除せず`problem`末尾へ
   文として移記する。無効分類は対応表（`documentation`→`process_improvement`・`design`→
   `implementation`）で置換し、有効な既存値は保持する。`created_at`・`candidate_id`・
   `source_work`・その他の欄は不変。`content_digest`は正準計算で再埋め込み。
3. **検証**：各file単独でv3検証器合格（4件）→N7単独0→台帳関連試験群（intake単体・intake v4・
   pilot・lane guidance）単独0。
4. 分類の置換は意味判断を含むため**覆せる形**でHuman確認点に載せる（分類はAI提案欄であり、
   確定はHuman仕分け側にある）。

## 3. 手順5：正式再利用検索

草稿→writer finalize→先行commit→`--plan`のみ。証明書は
`records/development/2026-08-19-n7-candidate-remediation-attestation-v1.json`。

## 4. 未実施

手順5、作業票の適用、再生成、検証、Evidence、TODO反映。
