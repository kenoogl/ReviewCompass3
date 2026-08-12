# Pilot Git実行時読取り専用ガード 独立開始前レビュー v1

- レビュー記録ID：`REV-PILOT-GIT-RUNTIME-READ-ONLY-GUARD-START-001`
- レビュー日：2026-08-12
- レビュー担当：作業担当とは異なる実行単位
- 対象作業票：`docs/development/2026-08-12-pilot-git-runtime-read-only-guard-bootstrap-work-ticket-v1.md`
- 作業票ID：`BTW-PILOT-GIT-RUNTIME-READ-ONLY-GUARD-001`
- 作業票SHA-256：`79b13d2a01e2ce2c70033efb5fcb2d06645c560b306adef59a34972ade645904`
- 作業票commit：`9285e1e289d9de47d6f127035c41ea9a9a1c2a18`
- 基準commit：`f85d70f5f9f8a7700ee742f0e892d6a4057b22dd`
- 元の完了レビュー：`records/development/2026-08-12-stage2-official-test-entry-restoration-completion-review-v1.md`
- 元の完了レビューSHA-256：`6518fbbb6662399590900e3069ce2d46a2bc9a69080a69d38b388c762a9bd02c`
- 採用する指摘：`CR-OTE-001`
- 危険度：`high`
- 判定：`開始可`

## 1. 判定

【判断】製品codeの`_run_git`自身が、第一副命令を`ls-tree`、`show`、`cat-file`の固定集合と完全一致で
検査する方向は、呼出し元のalias、動的名前解決、無名関数などの表現に依存しない。同じ関数へ到達する限り
外部process前に一つのruntime境界が働くため、`CR-OTE-001`を原因位置で閉じる方向として妥当である。

【判断】`PilotStop("internal_error")`は、外部利用者の入力不備を安全停止codeへ追加するのではなく、製品内部の
禁止Git経路を内部失敗として既存契約へ載せる。CLIの8-key結果形式、`result=failed`、終了コード1、
`stop_code=internal_error`と整合し、新しい停止code、結果schema、CLI変更を要しない。

【実測】開始を止める指摘は0件、報告不一致は0件である。上位計画v5 §6.1・§6.4と
`work-review-protocol` §11.1の四類型に該当する開始阻害要因を確認しなかった。

## 2. runtime境界と現行利用箇所

【実測】現行`tools/development/pilot_collaboration.py`の直接`_run_git` callsiteは次の3件だけである。

```text
ls-tree
show
cat-file
```

構文木抽出では定義一件、直接call三件であり、他の副命令を使う現行callsiteはなかった。作業票の許可集合は
現在の全利用箇所と完全一致する。許可後続引数、戻り値、`binary`によるtext/bytes切替えを変えないため、
公開CLIの入力や結果形式を拡張しない。

【実測】現行`_run_git`をfake `subprocess.run`へ接続すると、許可3種、`push`、`commit`、`reset`、`tag`、
空引数、`None`、先頭optionの全例がfakeへ各1回到達した。`getattr(module, "_run" + "_git")`で取得した関数への
`push`もfakeへ1回到達した。値のない現行runtime guardを、外部Gitを実行せず確認した。

【実測】作業票の最小guardを一時関数で模擬すると、許可3種はfakeへ各1回到達し、直接禁止4種、空、`None`、
先頭optionは`PilotStop.code=internal_error`、`detail=None`、fake呼出し0回となった。さらに同じ原因の変種として、
別のGit命令`status`、大小文字違い`SHOW`、先頭空白、bytes、boolを与えても、完全一致により同じくfake呼出し0回
だった。分割名`getattr`で得た同じguard関数への`push`もfake呼出し0回だった。

【判断】この完全一致集合は、承認された代表反例だけを個別列挙して防ぐのではなく、許可3種以外を閉じた集合で
拒否する。同じ原因の空・型・表現・副命令変種を開始方向として一括確認できる。

## 3. `internal_error`とCLI契約

【実測】v6要求は、成功を終了コード0、安全停止を2、予期しない内部失敗を1とし、終了コード1を
`result=failed`、`stop_code=internal_error`へ固定する。終了コード2の閉じた停止code集合に
`internal_error`は含まれない。

【実測】現行`pilot_collaboration_cli.run`へ、`prepare`が`PilotStop("internal_error")`を送出する一時差替えを
与えると、終了コード1で次を返した。標準出力のkey集合は既存8-key形式で、`detail`は`null`だった。

```json
{"command":"prepare","detail":null,"event_id":null,"result":"failed","run_id":null,"schema_version":1,"state":null,"stop_code":"internal_error"}
```

【判断】`_run_git`は製品内部helperであり、許可外副命令は既存CLIへの新しい利用者入力条件ではなく、製品内部で
禁止されたprocess経路である。これを`internal_error`として外部process前に止める方向は、現在の結果形式と
停止code集合を変えず安全側に失敗する。引数値を`detail`へ含めない境界も明確である。

## 4. RED、GREEN、変更範囲

【判断】既存`test_pilot_git_processes_are_read_only`へruntime例を加えるREDは、次の理由で修正前後を区別できる。

1. 製品moduleの`subprocess.run`をmonkeypatchしたfakeへ差し替えるため、実Git書込み、network、外部送信を行わない。
2. 現行実装では`push`等がfakeへ到達するので、外部process前拒否という期待で失敗する。
3. GREEN後は許可3種だけがfakeへ各1回到達し、禁止4種、空、非文字列、先頭option、分割名`getattr`は
   `internal_error`かつfake呼出し0回になる。
4. `PilotStop.code`、`detail`、process呼出し回数を同時に確認するため、別理由の例外だけでは合格しない。

【実測】現行の静的`test_pilot_git_processes_are_read_only`は1件成功、CLI試験fileは7件成功で、いずれも終了コード0
だった。REDはこの既存正常状態へruntimeの失敗条件を追加するものである。

【判断】変更範囲は最小で意味単位が分かれている。

- RED：`tests/test_pilot_collaboration.py`一件だけ。
- GREEN：`tools/development/pilot_collaboration.py`と新規Evidence一件だけ。RED試験を変えない。
- 対象外：CLI、v6要求本文、対応表、他の製品code・既存試験、元の設定・runner・RED・Evidence・完了レビュー、
  Python、依存関係、第2段完了、Git書込み、外部送信。

【実測】作業票commitは作業票文書一件の追加だけであり、基準commitはその直前の祖先である。開始前レビュー時の
worktreeはcleanで、試験・製品code・既存成果物に先行変更はない。

## 5. Human境界と修正後確認

【記録】利用者は、元の独立完了レビューが示した選択肢から「製品側のGit実行関数へ読取り専用命令の許可一覧を
設ける」を選択肢`1`で承認した。承認対象は固定3命令、外部process前の`internal_error`、RED一file、
GREEN製品一fileとEvidence一件という作業票の意味単位である。

【判断】技術的な`開始可`は、第2段完了、候補採用、Python 3.13移行、外部送信、履歴書換えを承認しない。
目的、許可命令、停止結果の意味を変える必要が出た場合は、作業票の停止条件どおり利用者へ戻す。

【判断】本作業は元の完了レビューで一件にまとめた`CR-OTE-001`だけを原因位置で修正する。修正後確認が、
元の公式試験入口正常化の完了条件、`CR-OTE-001`の動的表現反証、本作業のRED/GREEN、公式receipt、変更path、
対象外を一回でまとめて確認する構成は、上位計画v5 §6.7の一回上限と整合する。同じ事実を別々のレビューへ
分割しない。

## 6. 機械確認結果

各commandの終了コードを単独で判定した。

| 目的 | 実行内容 | 終了コード | 結果 |
| --- | --- | ---: | --- |
| 固定材料 | `shasum -a 256`、`git rev-parse`、`git show --stat` | 0 | 作業票、上位計画、元レビュー、製品・試験・v6要求の固定値とcommitが一致 |
| base関係 | `git merge-base --is-ancestor <base> <ticket-commit>` | 0 | 基準commitは作業票commitの祖先 |
| 作業票差分 | `git diff --name-status <base> <ticket-commit>` | 0 | 作業票文書一件の追加だけ |
| 現行callsite | Python構文木で`_run_git`定義・参照・直接callを抽出 | 0 | `ls-tree`、`show`、`cat-file`の三call |
| 現行runtime | fake processで正常・禁止・空・型・option・分割名を呼出し | 0 | 全例がfakeへ到達。REDが検出すべき現象 |
| guard方向 | 一時guardとfake processで同じ例と同原因変種を実行 | 0 | 許可3種だけ到達、他は`internal_error`・detailなし・0 call |
| CLI契約 | `PilotStop("internal_error")`を送る一時差替えで`cli.run` | 0 | CLI自身の返却は終了コード1、8-key failed形式 |
| 既存対象試験 | `pytest -q ...::test_pilot_git_processes_are_read_only` | 0 | 1 passed |
| 既存CLI試験 | `pytest -q tests/test_pilot_collaboration_cli.py` | 0 | 7 passed |
| 差分形式 | `git diff --check`、`git diff --cached --check` | 0 | 問題なし |

## 7. 未実施と次の一作業

【未実施】作業票、既存成果物、試験、製品code、設定、Evidence、TODO、Python環境は変更していない。実Git書込み、
push、外部送信、履歴書換え、公式全試験、本作業の実装、第2段の採用・完了判断は実施していない。

【次】利用者が作業票へ記録した選択肢`1`の範囲で、`tests/test_pilot_collaboration.py`一件だけに先行runtime例を
追加する。対象nodeを単独実行し、実Gitを書かず、現行guard不在により意図どおり失敗する場合だけRED commitへ
固定する。
