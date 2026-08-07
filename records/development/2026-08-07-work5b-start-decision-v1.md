# Work 5B開始・対象helper選定 承認Decision v1

- decision ID：`DEC-WORK5B-START-001`
- decision maker：Human
- decided at：2026-08-07
- 指示：本sessionのHuman文言「承認」（2026-08-07。直前のClaude提案
  「Work 5B開始・対象helper＝宣言→RED対応表検査器」に対する承認）

## 1. Humanの決定

1. **Work 5B（内部Implementation Task Contract Pilot）の開始**を承認した。
2. **対象helperを「宣言→RED対応表検査器」**（仮称`declaration_red_map_check`、
   `tools/development/`配下の1 module）とすることを承認した。
3. あわせて、宣言→RED対応表照合の**恒久tool化の導入**を承認した（TODO登録済みリマインドの判断）。
   恒久tool化はこのWork 5B対象helperの実装として行い、別系統の仕組みは作らない。

## 2. 検査器の承認範囲（最小）

対応表JSONとtest fileを読み、次を機械判定して結果を返す。

1. 列挙されたtest関数の実在（AST解析による）
2. testの無い宣言が0件であること
3. 宣言に結ばれないtestが0件であること

hook、自動実行、commit連動は付けない。判定はfail-closed（file欠落・解析不能は不合格）とする。

## 3. 進行条件（checklist §10 Work 5Bに従う）

- 実装前に、Work 4B最小試行で作った`reuse_search_record`のgateを通す
  （検索record無しでは実装を開始しない。gate判定は
  `tools/development/reuse_search_record.py`、SHA-256
  `e3ab3048f003ed1ce7bb13bdf2d6181a2e34196921a4317db4ee568bba9bb7b1`）。
- Contract、redを固定した後、**Humanの`implementation_ready`判断を記録するまでgreen実装を
  開始しない**。
- Testを弱めずgreenにし、post-write verification、Provenance、分割commitを確認する。
- provisionalな自己適用能力を正式Runtime既定にしない。

## 4. 参照

| 種別 | path | SHA-256 |
| --- | --- | --- |
| Work 4B最小試行 GREEN Evidence | `records/development/2026-08-07-work4b-reuse-search-green-evidence-v1.md` | `3284f77507a2ad09992404cae1ced846a6fe5ccdd564af8c8c0e8772e0588e0c` |
| Work 4B範囲提案 承認Decision | `records/development/2026-08-07-work-4b-minimal-pilot-scope-approval-decision-v1.md` | `4db98a488c76a7d15c1ddffca5c8f94139c29eadcc985930f30af5636b59adfc` |

## 5. この決定が承認していないこと

- `implementation_ready`判断（Contract・RED固定後に別途行う）
- Work 5Bの段完了、Work 4Bの段完了
- 検査器のhook化・自動実行、既存3枚の対応表の書き換え
- Entry・Relation・Baseline台帳の形式確定
