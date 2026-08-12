# Python 3.13開発環境移行 独立開始前レビュー v1

- レビュー記録ID：`REV-PYTHON-313-DEVELOPMENT-ENVIRONMENT-MIGRATION-START-001`
- レビュー日：2026-08-13
- レビュー担当：作業担当とは異なる新規実行単位
- 対象作業票：`docs/development/2026-08-13-python-313-development-environment-migration-bootstrap-work-ticket-v1.md`
- 作業票ID：`BTW-PYTHON-313-DEVELOPMENT-ENVIRONMENT-MIGRATION-001`
- 作業票SHA-256：`ee9ee13bf1059672ec135d97055be121926c3ee4aef0c291d53eec3aba1c51f0`
- 基準コミット：`80dba8ee1f82e904a34a9e9a5fb8446a78bdcd52`
- 作業票コミット：`f880f806a666d91ee5ec2c7a9fad9aa3b0b2863c`
- 危険度：`high`
- 判定：`修正要`

## 1. 判定と止める指摘

【判断】Python 3.13移行の目的、7 pathの変更範囲、RED・GREEN・Evidenceの順序、3.9環境の退避と
復旧、外部実装経路を使用停止のまま維持する境界は開始可能な方向である。ただし、Homebrewの副作用を
実行前に止める手順が不足するため、作業を開始しない。

止める指摘は次の1件である。

1. 【実測】作業票の本実行commandは`brew install python@3.13`である。現在のHomebrewヘルプでは、既定で
   install前の自動更新、古い依存先のupgradeまたは再install、install後のcleanup、install済み対象の
   upgradeが起き得る。作業票はPython 3.13と同formulaの必須依存以外を禁止するが、現在のcommandでは
   禁止対象の変更開始前に確実に停止できない。また、`brew deps --tree python@3.13`は、直接依存4件に加え、
   推移的な必須依存として`ca-certificates`と`readline`を示した。直接依存4件だけを必須依存全体として
   扱うと実状態と一致しない。

【判断】同じ原因への最小修正は、Human承認後に副作用を抑止した`--dry-run`で導入対象と推移的依存を先に
確認し、本実行でも自動更新、既存依存先検査、cleanup、install済み対象のupgradeを明示的に抑止し、
dry-runとの差があれば停止する手順へ固定することである。環境管理機構、複数Python対応、CI設計は追加しない。

## 2. 主要照合

- 【実測】作業票SHA-256、作業票コミット、固定入力5件のSHA-256、移行前公式結果記録のSHA-256は申告値と一致した。
- 【実測】移行前公式結果記録はPython 3.9.6、pytest 8.4.2、1,736件成功、失敗・error・skip 0、
  fallbackなし、終了コード0を示した。
- 【実測】正規構築処理は`.venv`が存在しない場合だけ新規作成する。したがって、現在の`.venv`を一意な
  `/private/tmp`へ先に退避し、不完全な新環境を別pathへ移して3.9 backupを戻す手順は実行仕様と整合する。
- 【実測】変更予定値をメモリ上で既存loaderへ渡すと、`environment_version: 1`と`runner_version: 2`のまま
  受理され、終了コード0だった。項目形式を変えない本作業で両版を維持しても形式上の拒否は起きない。
- 【判断】試験3件だけのRED commit、設定2件と依存固定だけのGREEN commit、公式結果記録、Evidence別commitの
  順序に循環はない。完了レビューでEvidenceだけを除外してGREEN状態を再構成すれば、結果記録の
  `source_state_digest`を照合できる。
- 【実測】移行手順は外部実装経路を起動せず、Git検査、`OUT-PC-006`、外部実装経路の再開を対象外とする。
  第1段の`使用停止`判断は維持される。

## 3. 試した反証と機械確認

【実測】「7 pathでは既存loaderが3.13設定を拒否する」という反証を、変更予定値をfileへ書かずメモリ上で
組み立てて試した。両loaderは既存の設定版のまま受理し、終了コード0だったため、反証は不成立だった。

【実測】一方、Homebrewの副作用抑止については、ローカルの`brew install --help`と`man brew`が既定の
追加処理を示し、`brew deps --tree python@3.13`が推移的依存2件を示したため、作業票の開始可判断は否定された。
最初のメモリ照合command一件は構文誤りで終了コード1となったため証拠から除外し、訂正版を単独実行した。

## 4. 維持したHuman判断境界

修正版の開始前レビューが`開始可`となった後も、次は利用者の明示承認後にだけ実施する。

1. Python 3.13と確認済み必須依存の外部取得。
2. `/opt/homebrew`への限定書込み。
3. 現行`.venv`の一意な`/private/tmp`への退避と、Python 3.13環境による正式`.venv`の置換。
4. 失敗時の不完全環境退避とPython 3.9環境の復元。

この承認に外部送信、外部実装経路の再開、Git検査の修正、第2段完了、履歴書換えを含めない。

## 5. 未実施と次の一作業

【未実施】作業票、試験、設定、依存固定、Evidence、Python、Homebrew package、`.venv`、外部実装経路は
変更していない。package導入、`.venv`移動、外部送信、履歴書換えは実施していない。

【次】操縦役は止める指摘1件だけをまとめ、Homebrewのdry-run、推移的依存の確認、副作用抑止を具体化した
作業票新版を作る。新版の独立開始前レビューが`開始可`となるまで移行作業を開始しない。
