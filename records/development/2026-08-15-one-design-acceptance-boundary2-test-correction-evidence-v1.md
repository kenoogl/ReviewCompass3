# One-design acceptance boundary 2 test correction evidence v1

## Purpose

境界2のRED commit後に発生した試験fixtureの手戻りと、明示契約に対する不足例の補充を、要求変更と区別して記録する。

## Socket fixture handback

- 対象操作：通常file以外としてUnix socketを実物作成し、安全読込が拒否することの確認。
- 期待executor：pytestの一時directory内で`AF_UNIX` socketを作る試験fixture。
- 実executor：最初はpytestの長い一時path、次に短い`/private/tmp` pathで実行した。
- 事象とEvidence：【実測】最初は製品呼出し前に`OSError: AF_UNIX path too long`、短縮後はsandboxがsocket作成を`PermissionError: [Errno 1] Operation not permitted`で停止した。
- 手作業理由：host制約とsandbox制約は製品の通常file判定とは無関係で、実socket作成を正規試験として安定実行できなかった。
- 訂正：実通常fileをopenした直後の`fstat`結果だけを`S_IFSOCK`へ差し替える決定的fixtureに変更した。期待する`unreadable_input / design`、製品分岐、通常file拒否の意味は変更していない。
- 機械処理候補：socket作成を許す隔離実行環境が正規化された場合だけ実物fixtureへ戻す。
- route：現行境界内の試験fixture訂正。契約、schema、製品能力の変更ではない。

## Missing explicit examples corrected

【記録】作業票v1 §4.2は「open後に同じ二fileを拒否」と「事前検査後のpath差替え」を明示していたが、RED commit `33db426`の24件には、異なる名前のhard linkと字句検査後のsymlink差替えが個別例としてなかった。

【実測】次の2例を追加した。

1. 異なる二pathが同じ機器番号・inodeなら`invalid_path / arguments`で停止する。
2. 字句検査後、file open直前にsymlinkへ差し替えると、非追跡openが`unreadable_input / design`で停止する。

【判断】これは契約拡張ではなく、作業票に既に固定された例の接続漏れ訂正である。

## Exception-detail correction

【実測】作業票v1 §3.3の「停止例外は固定reason/sourceだけを保持」に対し、初回実装はJSON復号例外を`__cause__`と`__context__`へ保持していた。追加した反証試験は、`JSONDecodeError`が残るため終了コード1で失敗した。

【実測】低位例外を保持しない位置で固定停止を生成するよう訂正後、JSON schema停止とfile open停止の双方で`__cause__`・`__context__`がnullとなり、対象70件が成功した。

【判断】秘密候補やpathを含み得る低位例外を停止objectへ保持しない契約適合修正であり、出力schemaや停止語彙の変更ではない。

