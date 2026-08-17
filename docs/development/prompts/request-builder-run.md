# Request builder run

契約の正本は`records/task-contract/2026-08-17-request-builder-candidate-v3.md`（契約011）である。
雛形・機械検査・機微検査の規則は正本を参照し、この入口には複製しない。

## 用途

レビュー依頼record（3類型：契約レビュー`contract_review`・完了レビュー`completion_review`・
自由文レビュー`free_text`）の草稿を雛形から機械生成し（機械欄＝digest表・鮮度検査・判定形式・手順・
命名。LLM記入欄＝`<<記入:`placeholder）、LLM記入後の完成recordを機械検査（7項目写像＋
`git check-ignore`＋機微検査）で検査する。外部送信・外部起動は行わない完全local処理である。

## 類型の使い分け（契約013 §7.2の規律）

- `free_text`（自由文レビュー）は、**既存2類型に当てはまらない**レビュー依頼専用である
  （Task Contract以外の文書・的を絞った反証の問い・調査結果の妥当性・複数recordの横断整合）。
- **既存2類型の代用にしない**：契約候補の独立確認は`contract_review`、実装完了レビューは
  `completion_review`を必ず使う（正式手続きの迂回路禁止）。
- 対象はrepository内のcommit済みfileに限る。書込み依頼・生成的依頼（文章作成・案出し）・
  多往復対話・repo外対象は扱えない。判定形式（5語彙＋findings）で答えられる問いに限る。
- 記入欄は「依頼内容（自由記入）」と「判断済み・範囲外」の2箇所（反証点の番号一覧は不要）。
  規模は節度を守る（実測目安45KB。巨大対象×網羅観点は分割——文字列理解の原則record参照）。
- 起動の承認境界は従来どおり（headless起動は利用者の明示指示ごと）。

## 単体入口

草稿生成（new-only書込み。出力は`records/session-handoffs/<date>-<slug>-request-v1.md`）：

```text
reviewcompass3-request-builder assemble \
  --repository <対象repositoryの絶対パス> \
  --type <contract_review|completion_review|free_text> \
  --date <YYYY-MM-DD> \
  --slug <小文字とhyphenの識別名> \
  --title <表題> \
  --target <対象fileのrepo相対パス（繰り返し可）>
```

機械検査（LLM記入とcommitの後。commit前の実行は`request_record_uncommitted`だけが不合格となる
状態を正常な途中経過とし、最終合格はcommit済み状態での全項目合格）：

```text
reviewcompass3-request-builder check \
  --repository <対象repositoryの絶対パス> \
  --request <依頼recordのrepo相対パス>
```

出力は正準JSON一行。終了コードは成功`0`、入力不備または検査不合格`2`、内部失敗`1`。
合格出力の`request.sha256`が、そのまま`reviewcompass3-reviewer-launch launch`の
`--expected-sha256`になる。

## G30操作

操作名`request_builder_check`として`reviewcompass3-operation-run`へ登録済み（入力`request`、
束縛位置`request.sha256`）。
