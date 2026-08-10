# group B 公式検証oracle修正 範囲レビュー結果 v1

- レビュー日：2026-08-10
- Reviewer：Codex
- collaboration mode：`role_neutral_pilot_review`
- レビュー段階：scope（実装前の範囲レビュー）
- risk：`high`（Human確定済み）
- 判定：`verified`
- Finding：blocking 0件、non-blocking 0件、defer 0件
- model来歴：`~/.codex/config.toml`の実効値 `model = "gpt-5.6-sol"`、
  `model_reasoning_effort = "high"`

## 1. 固定対象と開始状態

- 対象：
  `records/session-handoffs/2026-08-10-claude-pilot-official-oracle-fix-scope-v1.md`
- 対象SHA-256：`afa7b1733b2eabb33e0feb8997674c7b4ac3345bc00ce7eee48e2be522d8b323`
- 対象commit：`c5cd440ff2942d3c74525e6d53e2d424ced2462a`
- 対象commitの親：`271826a544e40db6b66640be785444204d9930f5`
- branch：`main`
- 許可範囲：本判定record 1件の新規作成と単独commit、読取り、決定的な照合
- 禁止範囲：対象scope、code、test、既存record、config、schema、上流設計、TODO、
  checklistの変更、RED、GREEN、外部送信、push、履歴書換え

【実測】対象commitの親はscope記載のbase `271826a`と一致し、変更pathは対象scope 1件の
追加だけだった。レビュー開始時のworktreeとindexはcleanだった。対象commitの
`git diff --check`は終了コード0だった。

【実測】本recordの予定pathに対する`git check-ignore --no-index`は終了コード1、作成前の
`test ! -e`は終了コード0だった。

【実測】scope §3の固定入力5件と対象実装4件のSHA-256を内容から再計算し、9／9で記載値と
一致した。

## 2. 5 Findingと修正境界

【記録】上流のgroup B判定recordは、F-B1からF-B5を次の4 moduleへ結び、P1・P2・P3・
S1・S2・D1・D2・D3・W1・W2の10反証をblocking根拠としている。

| Finding | scope §4の対象 | 境界照合 |
| --- | --- | --- |
| F-B1 | `policy_test_runner.py` | 古いsummaryの再利用と実合格0件の公式合格を拒否する |
| F-B2 | `policy_test_runner.py` | receipt出力と実行sourceの同一化を拒否する |
| F-B3 | `pytest_summary.py` | 同一node・phaseの重複計上と収集error欠落を拒否する |
| F-B4 | `declaration_red_map_check.py` | complete全省略、偽boolean、project root外testを拒否する |
| F-B5 | `work_unit_transition.py` | index非表示と別Git root差替えによるcommit関門迂回を拒否する |

【判断】5件の取りこぼしはない。各方針は既存の公式Test receipt、宣言→RED対応表、
完了作業単位のcommit関門を誤って合格させないための適合修正に閉じている。新しいreceipt field、
receipt kind、schema、方針値、command種別を受入条件に加えていない。

【判断】fake・stale receiptを`work_unit_transition.py`へ新たに束縛することや、receipt生成後の
改竄検出は対象Findingに含めていない。group B判定recordがFindingにしなかった境界を先取りしておらず、
group C・Dの12件にもはみ出していない。

## 3. 変更可能pathと関連Testの機械照合

【実測】`rg`で対象module名のimport、文字列参照、入口参照を`tests/`全体から列挙した。
§7の6 file以外で結線が見つかったのは次の5 fileだった。

- `tests/test_adversarial_remedy_batch1.py`
- `tests/test_red_verification_collection_error.py`
- `tests/test_verification_boundary_layer1.py`
- `tests/test_todo_handoff_prompt_entrypoints.py`
- `tests/test_todo_update_path.py`

【実測】§7の6 fileを単独実行した結果は`34 passed`、終了コード0だった。上記5 fileを
単独実行した結果は`50 passed`、終了コード0だった。

【実測】前3 fileは`declaration_red_map_check.py`の既存の双方向照合、complete／partial範囲、
RED実行結果の収集error扱いを検査する。後2 fileは`work_unit_transition`の共通TODO入口文字列と、
`policy_test_runner.execute`をfakeへ差し替えるTODO更新経路を検査する。いずれも今回廃止する
欠陥側の合格を正例として固定していない。

【実測】`pytest_summary.py`の実行時結線先としてrepository直下の`conftest.py`、利用側として
`tools/development/todo_record_generation.py`も見つかった。receiptの7件数fieldはscopeで
変更禁止のschemaのままであり、両fileの変更を必須にする固定値または指紋pinは見つからなかった。

【実測】対象4 moduleの現行SHA-256を固定する活動中のTestは見つからなかった。過去の
`records/development/2026-08-07-candidate-ranking-v1.json`と`v2.json`等には作成時点の
source SHA-256が残るが、これらを現行bytesへ追随させるTest結線はなく、scopeも既存recordの変更を
禁止している。

【判断】§7外の5 test fileは変更対象ではなく回帰確認対象である。scope §5.3の公式全Test合格に
含まれるため、失敗を見落として`verified`にする経路はない。指紋pinの派生値更新も不要であり、
group Aで発生した「許可pathを守ると公式全Testを合格させられない」という境界欠陥は再現しない。

【判断】実装中に`conftest.py`を含む§7外pathの変更が必要と判明した場合は、scope §8.2により
Humanへ停止する。範囲レビューでは実装方式を指定せず、この停止境界を維持する。

## 4. Human境界と停止条件

【記録】包括承認record `271826a`は、group Bについてrisk `high`の確定、着手、RED開始、
GREEN着手、レビュー依頼を事前承認している。Human停止として、変更可能path外、上流設計・config・
schema変更、既存台帳・既存recordの再計算または移行、RED後のtest変更、完了レビューblocking後の
修正、その他の意味的裁定を残している。

【判断】scope §2は包括承認の対象identityと事前承認範囲を正しく引いている。§6はRED以後の
test変更にHuman承認と理由記録を要求し、§8は§7外path、既存receipt再生成・既存record移行、
正常な公式runの`passed`不成立、上流設計・config・schema変更を停止条件にしている。
既存台帳・recordの再計算が必要な場合も§7外変更として§8.2で停止するため、包括承認が残した
Human境界に穴はない。

【判断】本範囲レビューの`verified`後は、包括承認により追加のrisk確定・着手・RED開始確認を
要しない。停止条件または修正承認に該当した場合だけHumanへ戻る。

## 5. 受入条件、RED、commit境界

【判断】危険側は上流10反証をIDで全件固定し、拒否またはstatus `failed`を要求している。
正例側は本repositoryの公式`--suite full`が`passed`のままであること、receipt件数と実行実績の
一致、対象Testと公式全Testの合格を要求する。危険側だけを一律拒否して正常runも壊す実装、
または件数だけを捏造する実装を合格させない双方向の機械照合になっている。

【判断】SCOPE、testだけのRED、実装・新規Evidence・新規receiptのGREEN、review requestを
別commitにする境界は、group E scope v3とgroup A scope v2で承認済みの運用と一致する。
REDは新規反証と欠陥のある旧契約を写した既存testの契約更新だけを許し、削除・緩和を禁止する。
実装前は変更testだけが反証どおり失敗し、他は合格、単独commandの終了コード1を要求するため、
REDの意味も維持されている。

## 6. Finding（`work-review-protocol.md` §11）

| §11区分 | scope段階の件数 | 判定 |
| --- | ---: | --- |
| 類型1：上流authorityとの矛盾 | 0 | なし |
| 類型2：Human境界・必要な承認の欠落 | 0 | なし |
| 類型3：誤った合格を許す受入条件・検証の欠陥 | 0 | なし |
| 類型4：禁止事項違反またはscope・schema境界の破り | 0 | なし |
| non-blocking | 0 | なし |
| defer | 0 | なし |

【判断】§11.2の比例原則に従い、command option、hook配置、内部の集合表現、fixture構成などの
実装細部は判定していない。scope段階でblockingにできる閉じた4類型に該当する未解消事項はない。

## 7. 判定と次

判定：`verified`

【判断】対象scopeはF-B1〜F-B5、変更可能path、Human境界、危険側と正例側の受入条件、
REDとcommit境界を矛盾なく固定している。対象commit、固定入力Digest、禁止範囲、停止地点も
repositoryの事後状態と一致する。

Human境界：維持。包括承認の停止条件または修正承認に触れた場合だけHumanへ戻す。

未実施：対象scope、code、test、既存record、config、schema、上流設計、TODO、checklistの変更、
RED、GREEN、完了レビュー、Closer作業、push、履歴書換え。

次：Pilotは包括承認の範囲内でREDへ進む。
