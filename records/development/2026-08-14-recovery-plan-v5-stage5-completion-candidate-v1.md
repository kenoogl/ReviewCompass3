# 立て直し計画v5 第5段 全体完了候補 v1

- 候補ID：`CANDIDATE-RECOVERY-PLAN-V5-STAGE5-COMPLETION-2026-08-14-V1`
- 作成日：2026-08-14
- 第5段開始基準commit：`5fdff893b081637b987b0c3539fe7fdbc89a779f`
- 観測commit：`515db1d78ab9afcae72a5edc3dcad7943b20e860`
- 上位計画：`docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md`
- 上位計画SHA-256：`8c814067511797e445d66779ad144f42ea0b139501ff6002a7d6c46e6706055c`
- 状態：`completion_candidate_pending_independent_overall_review_and_human_decision`

## 1. 平易な結論

【判断】第5段の機械確認可能な完了条件は満たした候補である。

ReviewCompass3には、利用者が許可した一件のローカルSession記録を読み、機微情報を伏せた会話記録、要約、
元記録との対応情報を画面へ返す、最初の正式・安定した製品入口ができた。通常利用する実行名から動き、利用者が
製品として受け入れ、独立レビューにも合格した。

ただし、本記録は第5段完了を決めない。新規担当とClaudeによる全体レビューを経た後、利用者が段完了を判断する。

## 2. 第5段の作業手順との対応

| 上位計画の作業 | 実際の成果 | 状態 |
| --- | --- | --- |
| 1. Task Contract案と独立した定義挑戦 | Task Contract v1を作成し、定義挑戦で安全な出力境界と配布正本の二点を訂正した | 完了 |
| 2. 利用者が契約の意味と実装開始を判断 | 利用者が機能、用途、入力、出力、限界、三案を確認して実装開始を承認した | 完了 |
| 3. 確定した小部品だけへTDDを適用 | 新入口固有試験を先に失敗させ、実装で成功へ移した。追加の絶対path二例も失敗から成功へ移した | 完了 |
| 4. 正規入口の結合試験と利用者向け受入 | 導入済み実行名から三形式を処理し、利用者が製品入口を受け入れた | 完了 |
| 5. 契約適合確認と最終挑戦 | Claudeを含む独立完了レビューで変更範囲、安全出力、禁止副作用、配布物、試験を確認した | 完了 |
| 6. 必要な修正後確認と段完了判断 | 絶対path二例と成熟度表示を限定修正し、それぞれ独立確認済み。段完了判断だけは本候補後に利用者へ残す | 判断待ち |

## 3. 第5段の完了条件との対応

### 3.1 製品処理が正規入口から証拠付きで動く

【実測】`pyproject.toml`は実行名`reviewcompass3-session-artifact`を
`tools.session_logs.read_only_entry:main`へ接続している。Claudeの修正後完了レビューは、観測commitから
配布物を作り、別の仮想環境へ導入し、導入済み実行名から合成Claude記録を処理して終了コード0、伏字化済みの
成功結果を得た。

【実測】現在の製品入口先頭は`stable / normative / promotion_required: false`である。利用者の製品受入判断と
正式・安定表示への昇格判断があり、昇格後の独立レビューは`verified`、止める指摘0件、報告不一致0件である。

【判断】人がPython関数を手でつなぐ一時経路ではなく、導入後に使える一つの正式な実行名が完成経路である。
Claudeへの手動レビュー受渡しは開発レビューの経路であり、この製品入口の通常利用経路には含まれない。

### 3.2 次作業が製品計画とTask Contractの関係から導かれる

【記録】承認済みの最初のTask Contractは、入力一件の読取り、伏字化、要約、来歴生成、画面への一回出力だけを
扱い、raw保存、派生物保存、探索、複数file処理、保持、削除、外部送信を明示的に対象外とする。

【記録】統合製品計画候補`docs/current/reviewcompass3-plan-current.md`は、Session Log Bootstrapでrawを
機微情報用領域へ、伏字化派生物を別のデータ領域へ保存し、追記と改変を区別して復元できることを次の段階として
示す。同fileは`provisional`で、SHA-256は
`1a73597605eafb65a2259ccf19431e3aba041564d03fdb279150042a9bd0962f`である。要求候補の
`REQ-SESSION-002`、`REQ-SESSION-003`、`REQ-PORTABLE-002`、`REQ-PORTABLE-004`も同じ不足へ対応するが、
まだ正式な要求ではない。

【記録】第4段の在庫では、保存を含む既存G26を保留としている。`repository_root`を省略すると安全な保存境界を
強制しない反例が成立しているため、G26をそのまま正式利用してはならない。

【判断】第5段完了後の次の製品作業候補を、次のように導く。

> 利用者が許可したSession記録一件と、現在の正式入口が作る伏字化結果を、安全な別領域へ保存して再読込みできる
> 範囲を、二つ目のTask Contract候補として定義し、独立した定義挑戦を行う。

これは実装開始ではない。暫定の製品計画と要求候補、最初のTask Contractが残した対象外、G26の既知反例を入力に、
保存対象、保存場所、機微情報の扱い、保持期間、削除、部分失敗からの復旧、G26を再利用するかを利用者が判断できる
契約候補を作る作業である。G26の修正、保存機能の実装、上流候補の正式化は、次の契約承認まで行わない。

### 3.3 開発基盤の完全性を完了条件にしていない

【実測】G30のTask Contract生成器・状態機械、G26の保存、G27の配置・定期実行、外部送信は未完成または保留の
ままである。

【判断】最初のTask Contractと一つの製品処理は、これらを前提にせず完成した。上位計画が明記するため、未完成の
開発基盤を第5段完了の不合格理由にも、暗黙の完了扱いにも使わない。

## 4. Task Contractと製品受入の固定材料

| 役割 | path | SHA-256 |
| --- | --- | --- |
| 承認済みTask Contract | `records/task-contract/2026-08-14-g25-session-artifact-preparation-candidate-v1.md` | `20e4e0551c5b1357ba3e66d6ba849f19566da27c58c54ef98e8fa1db110fb72b` |
| 定義訂正後の独立確認 | `records/development/2026-08-14-stage5-g25-session-artifact-task-contract-definition-correction-review-v1.md` | `8f07d74cb03e4ab6134a1774af8b775e1d01c57d836f32720ad6296dd1099e91` |
| 実装開始承認 | `records/development/2026-08-14-stage5-g25-session-artifact-task-contract-approval-decision-v1.md` | `dde3ad7be1a31f1c7f77e253a90fe952496950e5b6a402fcdf473388d211ae39` |
| Claude修正後完了レビュー | `records/development/2026-08-14-stage5-g25-session-artifact-entry-claude-completion-review-result-v1.md` | `2eda7a0ac9f89d53df9a75298ad494d75a613b89606ecc20ca6f17bd251ee637` |
| 古い状態結び付きの訂正裁定 | `records/development/2026-08-14-stage5-g25-session-artifact-entry-receipt-binding-adjudication-v1.md` | `0479601e87114a438afaf0536f0327d321c87dd6e534a042907d6869dec7ae2f` |
| 製品受入判断 | `records/development/2026-08-14-stage5-g25-session-artifact-product-entry-acceptance-decision-v1.md` | `57818c4390c02b866c55708b4292e965144d281a2349a5d12ad27bc4d31b7187` |
| 正式・安定表示への昇格判断 | `records/development/2026-08-14-stage5-g25-session-artifact-maturity-promotion-decision-v1.md` | `b0529f44d202c4b9c49600624417a54a611ad8eb77581ee9515c941291f850d1` |
| 昇格Evidence | `records/development/2026-08-14-stage5-g25-session-artifact-maturity-promotion-evidence-v1.md` | `51df5b3b84ce3ca846fc7206b0c1c9ad290db6021bb0dbe91f5f2dd4297bd6a4` |
| 昇格独立完了レビュー | `records/development/2026-08-14-stage5-g25-session-artifact-maturity-promotion-independent-completion-review-v1.md` | `3258ca6ea289852ef6a065bc5d103928fa654a15a4b56a455ee3e24741adfb92` |

【判断】Task Contract本体の先頭に残る「候補・未開始」は作成時点の表示である。Task Contract本体を履歴上書き
せず、定義訂正レビュー、実装開始承認、製品受入、昇格判断を順に結んで現在状態を決める。

## 5. 試験結果の再利用と古い証跡の除外

【実測】正式・安定表示への独立レビューは、変更commitの履歴付き複製で対象試験12件、G25直接関連55件、
正規全試験1,740件を実行し、すべて成功、失敗・error・skip 0、終了コード0を確認した。昇格前後へ同じ合成入力を
与え、出力がバイト単位で一致することも確認した。

【実測】独立レビューcommit `a8fb13792c10534c671b363355b7e51265aa3c9c`から観測commitまで、`tools/`、
`tests/`、`config/`、`pyproject.toml`、`setup.py`、`conftest.py`の差分は0件である。したがって、全試験を
儀式的に再実行せず、同じコード・試験・設定へ結び付いた独立結果を再利用する。

【判断】状態識別値`4251a948...`が限定GREEN commitへ結び付くという古い説明と、その説明に依存した内部レビュー
判定は使用しない。上記の履歴付き複製での独立再実行、状態結び付き訂正裁定、製品受入判断、昇格レビューだけを
現在の根拠に使う。

## 6. 第5段で追加・変更した20経路と役割

【実測】第4段完了commitから観測commitまでの終点差分は20経路で、追加18、変更2、削除0、重複0である。
内訳は製品コード1、試験1、実行名設定1、Task Contract 1、開発記録13、Claude受渡し指示2、現在位置の引継ぎ1で
あり、未分類はない。

| 構成物 | 現在の利用先と守る性質 | 区分 | 役割終了時の扱い |
| --- | --- | --- | --- |
| `tools/session_logs/read_only_entry.py` | 導入済み実行名が使う正式製品入口。安全な項目だけを返し、機微情報残存や絶対pathでは停止する | 現在の動作保証 | 製品入口を廃止する別判断まで維持する |
| `pyproject.toml`の実行名一件 | 利用者を正式製品入口へ接続する | 現在の動作保証 | 入口廃止時にコードと同じ単位で除去する |
| `tests/test_session_log_read_only_entry.py` | 三形式、root逸脱、機微情報残存、安全な出力、配布実行名を検査する | 試験 | 入口の契約変更または廃止時に意味単位で再判断する |
| Task Contract、承認・受入・昇格Decision、訂正裁定、現在の独立レビュー | 現在の責務、Human判断、安全限界、合格根拠を固定し、将来の監査にも使う | 両方 | 後継契約ができても履歴として維持し、現役参照だけを後継へ移す |
| 定義挑戦、実装・訂正Evidence、初回の不合格レビュー | 失敗、訂正、REDからGREEN、過大表示を含む経緯を残す | 履歴・監査資料 | staleな主張を現役根拠にせず、Git履歴として維持する |
| Claude受渡し指示v1・v2 | 外部レビューへ渡した固定入力を復元する | 履歴・監査資料 | 受渡し役は終了。通常入口にせず履歴として維持する |
| `TODO_NEXT_SESSION.md` | 人が現在位置と次の一作業を読む入口 | 現在の動作保証 | 次の状態へ機械生成で置換し、過去履歴を本文へ累積しない |

【判断】役割終了として直ちに削除する構成物は0件である。製品入口三経路は現役であり、履歴資料は失敗とHuman
判断を復元する用途がある。ただし、履歴資料を現在の製品動作の合否判定器として再利用しない。

## 7. 現在も維持する限界

1. この製品入口は、利用者が許可した一件のローカルSession記録だけを処理する。
2. 保存、探索、複数file処理、外部送信、ネットワーク通信、外部処理、Git操作、権限変更は行わない。
3. 出力は外部送信許可済みではない。
4. 既定規則、高い乱雑性の検査、絶対path検査の範囲を守るが、すべての機微情報を必ず検出するとは保証しない。
5. 正式・安定表示は、ReviewCompass3自身の全作業へこの入口を必須適用する意味ではない。
6. 上流候補9件、統合製品計画候補、要求候補、G26、G30、他142 pathは本候補で正式化しない。
7. 試験1,740件は観測値であり、恒久合格値や試験増加目標ではない。

## 8. 独立全体レビューで確認する点

1. 第5段の六作業と完了条件の対応に欠落または循環がないか。
2. 正規入口が人の手作業で部品をつなぐ一時経路ではないか。
3. 古い状態識別値の誤った結び付きを根拠へ混入していないか。
4. 独立全試験後にコード・試験・設定が変わっていないか。
5. 20経路の列挙、分類、役割終了時の扱いに漏れがないか。
6. 次のTask Contract候補が、暫定計画やG26を無承認で正式化していないか。
7. 第5段完了を先取りせず、利用者判断を残しているか。

## 9. 利用者が判断する点と未実施

【判断】内部全体レビューとClaude全体レビューの後、利用者が第5段を完了とするか判断する。

【未実施】第5段完了、次のTask Contractの採用・承認・実装、G26の修正、保存・探索・外部送信の実装、上流候補
9件の正式化、要求候補の採用、G30の利用、他142 pathの変更、Issue状態変更は行っていない。製品コード、試験、
設定、Task Contractも本候補では変更していない。外部送信、push、tag、amend、rebase、reset、履歴書換えも
行っていない。
