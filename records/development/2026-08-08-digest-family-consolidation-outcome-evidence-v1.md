# digest系統合の結果Evidence v1（統合せず・分岐検出テストで守る）

- 実施：2026-08-08。Human判断の経緯（逐語）：「実施。仮案どおい」→2段の発見の報告後「ｂ」
  （統合取り消し・分岐検出テスト）→「見落としていた件を判定にフィードバック」
- 根拠：digest系材料record（`ea1ec1ab…`）、`DEC-CONSOLIDATION-EVAL2-APPROVAL-001`

## 1. 実施の経過と2段の発見【実測】

1. TDDで統合を実施（共通module新設・10定義をaliasへ置換）。module importとしては
   全suite合格（1220 passed）
2. **発見1**：凍結レーン（歴史的Task Contract `TC-RC3-…-TODO-COMPACTION-2026-08-04-V2`）は
   symbol一覧に加えて**`todo_snapshot.py`のfile指紋を固定**しており、同fileの編集が契約identity
   検査2件を破った → 同fileを除外
3. **発見2**：documented手順のscript起動（`python3 tools/development/todo_compaction.py`）が
   `No module named 'tools'`で破損。編集10fileは全てsys.path処理を持たない**標準libraryのみの
   自己完結script**であり、**11か所の重複は自己完結設計の代償**（構造的理由のある重複）だった。
   材料recordの効果評価（alias 1行・約−17行）は前提が誤りだった

## 2. 結論（Human判断「ｂ」）

- 統合は**取り消し**（10fileをHEADへ復元、共通moduleは削除。REDテストは分岐検出テストへ
  書き換え——理由記録つきのテスト修正規定による）
- 守りたかった本来の保証（canonical仕様が4実装で食い違わないこと）は
  **分岐検出テスト**`tests/test_digest_divergence_guard.py`で固定：全11実装の出力を独立oracleと
  照合（8 test、sha256系4入力×7実装・canonical系4文書×4実装）。仕様が1か所でも分岐すれば即RED
- 検証：全suite **1213 passed**（1205＋8）、script起動の回復を確認【実測・単独実行】

## 3. 判定基準への恒久フィードバック（Human指示）

評価②の残系統（B例外・D_within・E印字・F dataclass）の材料づくりでは、次の2点を必須の
照合・実測項目に加える：

1. **手順1（照合）に追加**：凍結・契約の照合はsymbol一覧だけでなく、**契約recordが固定する
   file指紋（fixed_sources・carried_forward_work等）まで機械照合**する
2. **手順2（実測）に追加**：**起動方式の実測**——対象fileがscriptとして単独起動されるか
   （sys.path処理の有無、documented手順・cron・他toolからの起動）。自己完結scriptの重複は
   設計の代償であり、統合でなく分岐検出テストが既定の守り方

## 4. 残系統への含意

B（fail-closed例外7class）・D（_within 4file）・E（JSON印字3file）は**同じ自己完結script群**に
属する可能性が高く、統合でなく分岐検出テスト方式が予備見立て。系統ごとの確認と総括はHuman判断へ。
