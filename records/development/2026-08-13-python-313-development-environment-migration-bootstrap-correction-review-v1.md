# Python 3.13開発環境移行 修正後確認 v1

- レビュー記録ID：`REV-PYTHON-313-DEVELOPMENT-ENVIRONMENT-MIGRATION-CORRECTION-001`
- レビュー日：2026-08-13
- 対象作業票：`docs/development/2026-08-13-python-313-development-environment-migration-bootstrap-work-ticket-v2.md`
- 作業票SHA-256：`1d5836efed25fd049ce35772c6de60aaf4e40a952bfe8c580e7004a5ab5c5d16`
- 作業票コミット：`4726d899d1ef1f02af020b6cad1b5c66d7f67e0d`
- 先行開始前レビュー：`records/development/2026-08-13-python-313-development-environment-migration-bootstrap-start-review-v1.md`
- 先行レビューSHA-256：`96ad99ff4da9b713b321870ce47f267f4a57c016e69963582ff04f76f806c04a`
- 危険度：`high`（先行判断を継承）
- 判定：`開始可`

## 1. 確認範囲と判定

【判断】本確認は、作業票v1からv2へ追加されたHomebrew対策だけを対象とする一回限りの修正後確認である。
変更されていない目的、7 path、RED・GREEN・Evidenceの順序、Python 3.9環境のbackupと復旧、設定版、
外部実装経路の使用停止は再レビューせず、先行レビューの判断を引き継いだ。

【判断】先行レビューが止めた1件は解消された。止める指摘は0件であり、作業票v2は利用者の明示承認を
得る段階へ進める。

## 2. 変更点の照合

1. 【実測】v2は実行直前に`brew deps --tree python@3.13`で直接依存と推移的依存を含む依存閉包を取得し、
   `python@3.13`とその閉包だけを許可対象にする。閉包外をdry-runが示せば停止する。
2. 【実測】依存木、`install --dry-run`、TTY上の`install --ask`の3 commandは、すべて同じ次の4変数を
   明示する。機械抽出では3 command、4変数、停止条件3種が作業票に揃い、終了コード0だった。
   - `HOMEBREW_NO_AUTO_UPDATE=1`
   - `HOMEBREW_NO_INSTALLED_DEPENDENTS_CHECK=1`
   - `HOMEBREW_NO_INSTALL_CLEANUP=1`
   - `HOMEBREW_NO_INSTALL_UPGRADE=1`
3. 【実測】ローカルのHomebrew 6.0.14の公式helpと`env_config.rb`は、4変数をそれぞれ自動更新、
   install後の既存依存先検査と付随更新・再導入、cleanup、install済み対象のupgradeを抑止する設定としている。
4. 【実測】ローカルの`cmd/install.rb`は、確認modeでdry-run情報を先に表示してから確認処理へ進む。
   `install.rb`の`ask_formulae`も、導入処理を`dry_run: true`で表示した後に確認入力を呼ぶ。
5. 【実測】v2はTTY計画と直前のdry-runの対象集合が一致し、依存閉包内の場合だけ同意する。不一致、
   閉包外、確認入力なしの場合は同意せず停止するため、禁止対象の変更開始前に止められる。

【判断】依存閉包、同条件dry-run、同条件TTY計画、確認前停止が一続きになり、先行指摘の原因だった
「既定の追加処理と不足した依存範囲を変更前に検出できない」状態は残っていない。

## 3. 維持したHuman判断境界

【記録】技術的な`開始可`は実行承認ではない。Python 3.13と確認済み依存の外部取得、`/opt/homebrew`への
限定書込み、正式`.venv`の退避・置換と失敗時復元は、先行レビューどおり利用者の明示承認後にだけ行う。
外部送信、外部実装経路の再開、Git検査の修正、第2段完了、履歴書換えは承認対象に含めない。

## 4. 未実施と次の一作業

【未実施】Homebrewの依存木取得、dry-run、TTY本実行、package導入、権限迂回、`.venv`操作、試験・設定・
依存固定・作業票の変更、外部送信は行っていない。変更のない作業票部分を再レビューしていない。

【次】利用者が、作業票v2に固定されたHomebrewの外部取得・限定書込みと正式`.venv`切替えを含む作業開始を
承認するか判断する。承認前はRED試験の変更もHomebrew commandも開始しない。
