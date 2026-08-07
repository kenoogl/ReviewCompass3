# RED固定時の実行照合を手順へ採用 承認Decision v1

- decision ID：`DEC-RED-VERIFICATION-ADOPTION-001`
- decision maker：Human
- decided at：2026-08-07
- 指示：本sessionのHuman文言「採用」（2026-08-07）
- 根拠Evidence：`records/development/2026-08-07-c4-red-verification-green-evidence-v1.md` §3

## 1. Humanの決定

宣言→RED対応表の`red_now`実行照合を、**RED固定commitの前に毎回行う手順として採用する**。

## 2. 手順（作業への組み込み）

宣言→RED対応表を作る作業単位では、次の順で進める。

1. 対応表を作成し、静的検査（列挙testの実在、testの無い宣言0件、双方向一致）に合格させる
2. **実行照合を行う**：

   `PYTHONPATH=. .venv/bin/python3 -c "import json; from tools.development.declaration_red_map_check import check_declaration_red_map; print(json.dumps(check_declaration_red_map(map_path='<map path>', project_root='.', verify_red=True), ensure_ascii=False))"`

3. 結果（`red_verification`の`checked`／`verified`／`mismatched`／`unknown`）をRED Evidenceへ記録する
4. `mismatched`または`unknown`が残る場合、**commitせずに原因を解消する**。解消できない場合は
   停止してHumanへ報告する

## 3. 採用の理由（時点意味論）

`red_now`はRED固定時点の主張であり、実装完了後に同じtestを走らせれば成功するのが正しい。
したがって実行照合はRED固定の瞬間にしか成立せず、事後にまとめて確認することはできない
（GREEN後の既存対応表13枚では`red_now: true`の宣言がすべて不一致になることを実測済み）。
毎回その場で行うと定めない限り、この機能は使われないままになる。

## 4. 適用範囲と例外

- 適用：本Decision以後に新規作成する宣言→RED対応表のすべて
- 既存の対応表13枚には遡及しない（GREEN後は`red_now: true`の照合が原理的に成立しないため）
- 境界例（`red_now: false`）の照合は事後でも成立するため、必要に応じて任意に実行してよい
- 既定の静的検査は変更しない。実行照合は本手順で明示的に呼ぶ

## 5. あわせて許可されること

`docs/development/work-review-protocol.md`への手順追記（本Decisionを根拠として記載する）。
