# 外部送信の機微検査精密化と送信路改名 作業契約候補 v2

- 契約ID：`TC-RC3-PRODUCT-EXTERNAL-SEND-SCAN-REFINEMENT-009`
- 契約版：2
- 契約種別：製品処理・受入済み送信路（契約008）の精密化縦切り＋残名整理
- 状態：`candidate_pending_independent_review`
- 作成日：2026-08-16
- 直前の製品契約：`TC-RC3-PRODUCT-EXTERNAL-REVIEWER-SINGLE-SEND-008 / v5`（受入済み）
- supersedes：`records/task-contract/2026-08-16-external-send-scan-refinement-candidate-v1.md`、
  SHA-256 `a76a7ed489e37cbe937eddf06a1cd96f07e30a47017acec82d7f3865cfd5e85d`
- 訂正根拠：起草側自己レビュー
  `records/development/2026-08-16-external-send-scan-refinement-v1-self-review-v1.md`の
  SR-C9-1（§7一律適用が識別子停止仕様と両立しない・機械検証済み）、SR-C9-2（定数直書きの明示）、
  SR-C9-3（RED定義の向きの明確化）
- 入力：改善候補`IC-EGRESS-SENSITIVE-SCAN-FALSE-POSITIVE-001`、利用者指示「機微検査精密化の契約候補に
  改名を含めて作成せよ」（2026-08-16 chat）
- 実装状態：未開始
- 危険度：高
- 危険の理由：機微検査（外部漏えい防止の中心的な守り）の検知範囲を狭める変更である。緩めすぎれば
  鍵漏えいの保険を失い、狭めなければ実用文書を送れない

## 1. 位置と縮小境界

【記録】受入済みの送信路は、高乱雑性検知が開発文書の可読file名・digest記載を鍵候補として誤検知するため、
実用文書（`records/`・`docs/`配下のほぼ全部）を送信できない（観測record
`records/development/2026-08-16-egress-sensitive-scan-false-positive-observation-v1.json`）。

【判断】本契約は、**高乱雑性検知への契約固定の除外3形式の追加（適用範囲を限定した検査呼出しの変更）と、
v1由来の残名の改名**だけを行う縮小縦切りである。

- 既定5 pattern検知（email・Bearer・鍵代入形式・秘密鍵ブロック・AWS key ID）は一切変更しない。
- `redaction.py`は変更しない（公開引数`allow_patterns`の利用だけで実現する）。
- 送信規則（宛先・payload・台帳・上限・鍵扱い）は契約008 v5のまま一切変更しない。
- 応答解析・監査自動化・旧設計統合・複数送信は引き続き後続契約に残す。

## 2. Human承認境界

契約008 v5 §2の決定（送信ごとの人の確認なし・行為の起点は利用者の指示・機械層が内容の守りの実体)を
そのまま引き継ぐ。**検知範囲を狭める本変更の承認は、本契約の採用判断で満たす**（除外の正確な形と適用範囲は
§7で契約固定し、実装者の裁量を残さない）。

## 3. 権威、証拠

| 役割 | path |
| --- | --- |
| 誤検知の観測（実測値つき） | `records/development/2026-08-16-egress-sensitive-scan-false-positive-observation-v1.json` |
| 改善候補（検証器合格） | `.reviewcompass/workflow/improvement-candidates/ic-egress-sensitive-scan-false-positive-001--v1.json` |
| 契約008の製品受入判断 | `records/development/2026-08-16-external-reviewer-single-send-product-acceptance-decision-v1.md` |
| 採用中の契約008 v5（改名は§11が後続整理と明記） | `records/task-contract/2026-08-16-external-reviewer-single-send-candidate-v5.md` |
| 外部レビュー機械化目標 | `records/development/2026-08-16-external-review-preparation-mechanization-goal-v1.md` |
| 起草側自己レビュー（SR-C9-1〜3） | `records/development/2026-08-16-external-send-scan-refinement-v1-self-review-v1.md` |

## 4. 実装方法の3案

| 案 | 内容 | 判断 |
| --- | --- | --- |
| A 正規hex値だけ除外 | SHA-1／SHA-256形式の2 patternだけ`allow_patterns`へ渡す | 起草時実測でAGENTS.md・pyproject等が不合格のまま（下線連結・大文字ID・長断片が残検知）。実用に届かず不採用 |
| B 契約固定の除外3形式＋適用範囲の限定 | §7の3形式を、`order_identifier`を除く検査にだけ`allow_patterns`として渡す | 起草時実測で観測3文書とTODO・契約文書が合格し、乱雑列6種の停止と64hex識別子の停止が維持された。推奨 |
| C 由来fileの高乱雑検知を全面免除 | allowlist合格fileは5 pattern検知のみ | 未知形式の鍵への保険を全て失う。不採用 |

## 5. 範囲

### 5.1 範囲内

- 送信核の機微検査呼出しへの契約固定`allow_patterns`（§7の3形式）の追加。適用は§7.2の範囲だけとし、
  `order_identifier`の検査は従来どおり除外なしで行う（検査呼出しの出し分けを含む）。
- 送信路の改名（§8）。
- 精密化の対象試験（誤検知解消・敵対耐性・境界値・識別子停止維持）の追加と、既存対象試験の改名追随。

### 5.2 範囲外

- `redaction.py`・既定5 pattern・egress 7 module・受入済み4製品の変更。
- 送信規則（契約008 v5 §7〜§10）の変更。累計上限・台帳・鍵扱いの変更。
- 応答解析、監査自動化、旧設計統合、複数送信、依頼組み立て器、prompt品質gate（後続）。
- 歴史的record・台帳・Evidence内の旧名表記の書き換え（歴史的記録として不変）。

## 6. 固定再利用部品と保護基準

保護基準commitは本候補の固定commitとする。次を変更しない：`tools/session_logs/redaction.py`、
`tools/egress/`7 module、受入済み4製品（G02・G08・G24・実行器）とその試験、`tools/task_contract/`5 file。
契約008の成果物（送信核・入口・対象試験・`pyproject.toml`の実行名）は**本契約§9の変更上限内でのみ**変更する。

## 7. 契約固定の除外3形式と適用範囲（本契約の中心的な取り決め）

### 7.1 除外3形式

`find_high_entropy(text, allow_patterns=...)`へ渡す除外は次の3形式**だけ**とする（トークン全体一致）。
3形式は**送信核へ直書きする契約固定の定数**とし、設定file・環境変数・引数・送信指示のいずれからも
追加・変更できない。

| 名 | 正規表現（fullmatch） | 意図 |
| --- | --- | --- |
| X1a | `[0-9a-f]{40}` | gitのcommit識別値（SHA-1）の正規形。40桁ちょうどの小文字hexだけ |
| X1b | `[0-9a-f]{64}` | 内容識別値（SHA-256）の正規形。64桁ちょうどの小文字hexだけ |
| X2 | `(?=.*[G-Zg-z_])[A-Za-z0-9]{1,20}(?:[-_]+[A-Za-z0-9]{1,20})+` | 可読な連結名（file名・関数名・ID等）。hex外の文字を最低1つ含み、区切り（hyphen・下線、連続可）で結ばれた20文字以下の断片2つ以上 |

### 7.2 適用範囲（SR-C9-1の訂正）

除外3形式を適用するのは次の検査**だけ**である。

- 送信指示の`purpose`と`source_files[].path`（および§8除外欄以外の文字列一般）の高乱雑性検査
- 由来fileの内容の高乱雑性検査

**`order_identifier`の高乱雑性検査には適用しない**（従来どおり除外なしで検査する）。これにより
契約008 v5 §8の仕様「24文字以上の乱雑な識別子（64hexを含む）は`sensitive_data_remaining`で停止し、
識別子には24文字未満の可読形を用いる」が不変のまま維持される。既定5 pattern検査は全fieldで従来どおり
除外なしで行う。

**起草時実測（採用判断の材料。受入条件で再現する）**：

- 誤検知の解消：観測recordの3文書（`pyproject.toml`・`AGENTS.md`・開発方針）、record file名、
  `TODO_NEXT_SESSION.md`、契約008 v5本文の全てが合格へ変わる。
- 停止の維持：全小文字乱雑24字・大小混在乱雑・hexだけの断片連結・Base64風・39／41／63／65桁hexの
  乱雑列、および64hexの`order_identifier`は引き続き停止する。

**残余risk（明示的に受容を諮る）**：

1. 40桁または64桁ちょうどの小文字hex形式の実鍵は、X1a／X1bを通り得る（`purpose`・path・由来file内容に
   限る。識別子経由の台帳流し込みは§7.2で引き続き停止する）。
2. 大文字を含む乱雑な[-_]連結（ライセンスキー風）は、X2を通り得る。
3. UUIDは従来からエントロピー閾値（3.5）未満で検知対象外である（本契約で変わらない事実の明示）。

緩和：(a)既定5 patternは不変で、主要な鍵形式（AWS ID・Bearer・代入形式・秘密鍵ブロック・email）を
引き続き止める。(b)由来fileはcommit済み限定であり、送れるのはgit履歴に既在の情報だけである。
(c)鍵は`~/.zshrc`管理でrepository文書に書かない運用である。(d)台帳とgit履歴が事後監査線である。

## 8. 送信路の改名（契約008 v5 §11の「後続の整理」の履行）

| 旧 | 新 |
| --- | --- |
| `tools/external_review/gemini_send.py` | `tools/external_review/send.py` |
| `tools/external_review/gemini_send_entry.py` | `tools/external_review/send_entry.py` |
| 実行名`reviewcompass3-gemini-send` | `reviewcompass3-external-review-send` |
| `tests/test_gemini_send.py` | `tests/test_external_review_send.py` |

- 実体は3 provider切り替え式であり、旧名は宛先がGemini単独だったv1の残名である。
- 旧実行名は残さない（併存させない）。歴史的record・台帳・Evidence内の旧名表記は書き換えない。
- 台帳root・record名形式・送信指示schemaは変更しない（改名の影響は実行名とmodule pathだけ）。

## 9. 変更上限

1. `tools/external_review/send.py`（gemini_send.pyの改名＋§7.1の定数直書きと、§7.2の適用範囲を実現する
   検査呼出しの出し分けだけ）。
2. `tools/external_review/send_entry.py`（改名＋import先更新だけ）。
3. `pyproject.toml`の実行名1行の置換。
4. `tests/test_external_review_send.py`（改名＋import・実行名期待の更新＋§10の精密化試験の追加）。
5. Evidence、独立確認、受入判断、TODO更新。

## 10. 受入条件

実装開始後は失敗試験を先に固定し、期待どおり失敗してから最小実装を行う。

1. RED（SR-C9-3の明確化）：可読file名（観測recordの誤検知と同形）の資料を持つ送信指示が
   **停止しないこと**を期待する試験を先に固定する。精密化前の現実装ではこの試験が失敗し（現状は
   誤検知で停止する）、§7適用後に合格する。
2. 誤検知の解消：§7.2の起草時実測（観測3文書・record file名・TODO・契約文書の合格）を試験で再現する。
3. 停止の維持（敵対）：§7.2記載の乱雑列6種と、40／64桁の前後1桁（39・41・63・65桁）の乱雑hexが
   引き続き停止する。**64hexの`order_identifier`が引き続き停止する**（適用範囲の出し分けの実証）。
4. 既定5 pattern（AWS ID・Bearer・代入形式・秘密鍵ブロック・email）の検知が全fieldで維持される。
5. 改名の完了：コード・設定・試験から旧名（`gemini_send`・`gemini-send`）の残存0を全文検索で確認する
   （`records/`・`docs/`・台帳の歴史的記載を除く）。
6. 既存対象試験49件相当が改名後も全緑。egress関連107件・受入済み各製品・正規全試験（隔離条件）が
   各単独終了コード0。保護対象が基準commitから差分0。
7. 固定commitを独立レビュー（暫定体制：Gemini手動・Human中継）が、誤合格・未接続・禁止作用・
   上位目的への悪影響0件、および**§7の残余riskの受容妥当性**として確認する。
8. 利用者の指示の下で、実用文書（例：観測record自身）を資料とする実送信E2Eを一回行い、精密化後の
   経路で実文書が送れることを実環境で確認する。
9. 利用者が残余risk（§7）と改名結果を確認して製品処理を受け入れる。

## 11. 停止条件

- §7の3形式と適用範囲で、誤検知解消・乱雑列停止・識別子停止の三立が固定できない
  （形式・範囲の追加変更が必要になる）。
- `redaction.py`・既定5 pattern・egress 7 module・受入済み製品の変更が必要になる。
- 対象、関連、正規全試験または独立確認が不合格になる。

## 12. 影響、未実施、次作業

【判断】受入後は、`records/`・`docs/`配下の実用文書（レビュー依頼の実資料）を契約008の守りつきで
送信できるようになり、外部APIレビュー6段のうち送信段(5)が実用になる。名称も実体（3 provider切り替え）と
一致する。依頼組み立て器・prompt品質gate・判定取り込み（機械化目標の縦切り(a)(b)(c)）は後続に残る。

【未実施】契約採用、実装、改名、実送信、既存成果物変更は行っていない。

次は本候補を固定commitへ記録し、暫定体制（Gemini・Human中継）の独立確認を受ける。`開始可`の後、
利用者へ縮小境界の採用と実装開始を一判断として求める。
