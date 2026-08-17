# 改善候補4件の仕分け Human判断record v1

- 判断日：2026-08-17
- 判断者：利用者（Human）
- 記録者：Claude
- 対象：登録済み改善候補4件（各観測recordが正本）

## 1. 承認文言【記録】

> 推奨どおり仕分けを確定する。仕分けrecord作成→TODO更新まで進めて

（2026-08-17 chat。Claudeが提示した候補別推奨の全文承認）

## 2. 仕分け結果

| 候補 | 正本（観測record） | 仕分け | 実施時機・条件 |
| --- | --- | --- | --- |
| `IC-BACKEND-REGISTRY-DEEPENING-001`（backend登録形の深化） | `2026-08-17-backend-registry-shallow-generalization-observation-v1.json` | **採用** | **codex-cli第3 backend追加の縦切りと同時**に実施（単独着手しない。疎通回復が合図） |
| `IC-REQUEST-BUILDER-MODEL-CHECK-SCOPE-001`（組み立て器のmodel照合範囲） | `2026-08-17-request-builder-union-model-check-observation-v1.json` | 保留 | 上記候補1と**同時機に再評価**（登録形が持つbackend別一覧を参照する契約011小改定として解くのが自然） |
| `IC-REUSE-SEARCH-GATE-CONNECTION-001`（正式再利用検索の機械gate接続） | `2026-08-17-reuse-search-gate-disconnection-observation-v1.json` | 保留継続 | **縦C事前走査でもう1件の運用実測**を得てから、強制点の設計とともに再仕分け |
| `IC-ADVERSARIAL-FIXTURE-CATALOG-001`（敵対fixtureの類型網羅） | `2026-08-17-adversarial-fixture-catalog-observation-v1.json` | **採用** | **縦C契約のRED段要求へ組み込む**（起草時に類型→検査器→fixture対応表を作成し、該当類型の先行失敗試験を受入条件へ含める。独立の作業単位は立てない） |

## 3. 帰結

- 新しい作業単位は本仕分けでは発生しない。全候補が「合図が来たら動く」状態に置かれた。
- 次の実作業が縦C（合議）の契約候補作成になる場合、候補3の実測（事前走査6手順の運用）と
  候補4の組み込み（RED段要求）を**兼ねる**。
- codex-cli疎通回復時は、第3 backend追加の縦切りに候補1を含め、候補2を再評価する。

## 4. 未実施

- 各候補の実施そのもの（上記の時機・条件が満たされたときに着手）。次の作業単位の順序選択。
