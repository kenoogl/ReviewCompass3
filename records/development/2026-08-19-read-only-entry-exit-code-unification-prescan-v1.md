# read_only_entry終了コード統合 事前走査 v1

- 記録日：2026-08-19
- 指示者：利用者（Human）。文言「read_only_entry独自語彙の統合」（2026-08-19 chat・着手指示）
- 記録者：Claude
- 上位：`IC-SESSION-LOG-EXIT-CODE-VOCABULARY-001`（仕分け＝採用）の残件。候補3是正の作業票
  （2026-08-18）§3が「統合するなら別の作業単位」と定めた分
- 必読照合：文字列理解の失敗類型と対策原則——本件は機械が読む出力（終了コード）の語彙統一で、
  原則1（fail-closed維持）・原則5（読み手の分離＝詳細はJSONのerror欄が運ぶ）に沿う。本文運搬・
  解析器の新設はない
- 基準commit：`48ba5d3`（本走査の生成物2件を除きclean）
- 実測：測定ブロック
  `records/development/2026-08-19-read-only-entry-exit-code-unification-prescan-measurements-v1.md`
  （guard付き・全4entry二重実行一致）

## 1. 実測から確定した事実

1. **現状の語彙（4入口・定数行の機械転記）**：`cli.py`＝0／2／3（対象なし）／4（非対応）／5（失敗）
   ／6〜10。`read_only_entry.py`＝0・**partial=3・stopped=4**。`eventual_preservation.py`＝
   0・4・5（2026-08-18是正済み・共通語彙と同値）。`safe_storage_entry.py`＝0・stopped=4
   （＋生の数字3=StorageIncomplete）。
2. **値の衝突**：read_only_entryの3（部分成功＝正常寄り）はcli語彙の3（対象なし）と、4（停止＝
   異常）はcli語彙の4（非対応＝正常寄り）と、**同じ数字が逆向きの意味**で並存している。partialを
   4へ動かすなら、現行stopped=4も同時に動かさないと衝突する。
3. **終了コードの消費側は1箇所**：`safe_storage_entry.py` 80行の`source_exit_code != EXIT_OK`
   （0以外は一律停止・値の区別なし）。他の参照（`safe_storage.py`）は補助関数
   `_contains_absolute_path`とmanifest欄名`read_only_entry_version`で、終了コード非結合。
4. **保護試験の値結合**：`tests/test_session_log_read_only_entry.py`＝parametrize期待値
   （0／3／4）＋直接assert（`== 3`が1箇所・`== 4`が3箇所・`== 5`は0箇所）。
   `tests/test_session_artifact_safe_storage_entry.py`＝模擬値`(3, "partial")`・`(4, "stopped")`
   各1（gate検査の入力。自身の期待`exit_code == 4`はsafe_storage_entry側の語彙で不変）。
5. **文書側の結合なし**：read_only_entryのCLI終了コードを記載した現行手順書・promptは0件。
   RQ2ケース材料（`docs/evaluation/rq2-cases/`）は封緘済みの複製で対象外（前作業票§3と同じ）。

## 2. 設計（作業票へ渡す論点）

1. **対応表**：ok→0（不変）／partial→**4**（`EXIT_UNSUPPORTED`。eventual_preservationのpartial
   と同値・同義＝「一部が解釈非対応だが成果は返せた」）／stopped→**5**（`EXIT_FAILED`。
   fail-closed停止＝安全に結果を返せない失敗）。停止理由別の細分（機微=2等）は採らない——
   消費側は0／非0しか見ておらず、詳細はJSONの`error`欄が運ぶ（原則5）。
2. **実現方式3案**：案A＝局所定数を共通語彙名（`EXIT_OK`・`EXIT_UNSUPPORTED`・`EXIT_FAILED`）へ
   改名し値を0／4／5にして、`cli.py`との値一致を試験で機械固定（2026-08-18是正と同型）。
   案B＝`cli.py`を直接import（読み取り専用入口が書込み系CLI moduleへ依存し境界が濁る）。
   案C＝共通定数moduleの新設と4入口の一斉移行（stable部品3つの同時変更・範囲最大。将来候補として
   記録のみ）。**採用候補は案A**（単純・前例同型・変更2file）。定数名の改名はmodule内2参照のみで
   外部参照なし（実測§1-4：試験は数値literal・safe_storage_entryは自前定義）。
3. **試験の扱い**：新設RED 1本＝値一致pin（read_only_entryの定数==cli.pyの対応定数）。意図保存
   更新＝direct試験の期待値（3→4・4→5）と、safe_storage_entry試験の模擬値の現行化（(4,"partial")・
   (5,"stopped")。gate検査の意図＝0以外は転送せず停止、は不変）。
4. **範囲外で観測記録**：safe_storage_entry自身の語彙（0・生の3・stopped=4）は別の外向き取り決め
   （storage系）であり消費側分析が別途要る。観測として本record・Evidenceへ残し、改善候補routeへ
   （登録はHuman仕分け）。

## 3. 手順5：正式再利用検索

草稿→writer finalize→先行commit→`--plan`のみ。証明書は
`records/development/2026-08-19-read-only-entry-exit-code-unification-attestation-v1.json`。

## 4. 未実施

手順5、作業票の適用、RED、GREEN、Evidence、TODO反映。
