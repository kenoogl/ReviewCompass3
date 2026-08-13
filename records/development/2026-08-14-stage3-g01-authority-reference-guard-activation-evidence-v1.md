# 第3段 G01権威参照検査の現役接続 Evidence v1

- 記録日：2026-08-14
- 状態：`implemented_pending_independent_completion_review`
- 対象Issue：`ISSUE-TEST-GROWTH-STATE-PINNING-001`
- 関連Issue：`ISSUE-AUTHORITY-REFERENCE-DIGEST-CHECK-001`
- 基準commit：`8772630`
- 有効な作業票：v1とv2の組合せ
  - `docs/development/2026-08-14-stage3-g01-authority-reference-guard-activation-bootstrap-work-ticket-v1.md`
  - SHA-256：`2713e281b6a40ceff7f6e08ef4cee98ed687fbef2ebd5d0aebe70ba04150281a`
  - `docs/development/2026-08-14-stage3-g01-authority-reference-guard-activation-bootstrap-work-ticket-v2.md`
  - SHA-256：`28c78015c32926f0b7444b3ee9831dd667a6d26d79628774f7a0b0e0dcca3d64`
- 開始前レビュー：`records/development/2026-08-14-stage3-g01-authority-reference-guard-activation-start-review-v1.md`
  - SHA-256：`5b80782675f0db0e2fc3c84cfc6422d185d55e44903a975310ee95670ed9db53`
- 限定修正後確認：`records/development/2026-08-14-stage3-g01-authority-reference-guard-activation-scope-correction-review-v1.md`
  - SHA-256：`7d1cc9105058ac10db113260f33c8af3392feab743c22961d62ff364dd76aef5`
- 利用者承認：2026-08-14、再評価で推奨した案Cを「承認」

## 1. 実施と結果

【実測】試験fileだけを変更したRED commit `ef0aadc`で、対象試験は18件成功・1件失敗、終了コード1だった。
失敗はNUL文字を含む経路で`Path.resolve()`が`ValueError`を出した一件だけであり、実文書の正常照合、
既存異常例、空文書混在を含む他18件は成功した。

【実測】試験を変更せず、検査コードだけを変更したGREEN commit `e29c700`で、対象19件は全件成功、
終了コード0になった。`git diff --exit-code ef0aadc e29c700 -- tests/test_authority_reference_checker.py`は
終了コード0で、GREEN中に試験を弱めていない。

【実測】Human承認済みの次の実文書2件を検査コードの単独commandへ渡すと、初期開発チェックリスト8参照、
現行Plan 3参照、合計11参照がすべて一致し、終了コード0だった。

- `docs/development/2026-08-03-initial-development-checklist.md`
- `docs/current/reviewcompass3-plan-current.md`

【実測】正規全試験を単独実行し、1,728件成功、失敗・エラー・除外0、終了コード0だった。Pythonは
3.13.14、pytestは8.4.2、代替実行はなく、runner版は2だった。結果記録はリポジトリ外の
`/private/tmp/reviewcompass-g01-activation.6Flim2/full-receipt.json`へ保存した。

| 項目 | 値 |
| --- | --- |
| 結果記録SHA-256 | `358cfdff60d994073c43ce92395f021576f8f13e57cb9034a805a0e64ec38f9b` |
| 状態識別値 | `6ca1d8a4a92cbe9ef2e5b5a01c387b73cacd0ad5c8afbe07032206275106f36b` |
| 実行結果 | `1728 passed in 49.83s` |

【判断】結果記録は本Evidence追加前、GREEN commit `e29c700`の状態を識別する。本Evidenceと独立レビューを
追加した後の状態は、完了レビュー担当が正規全試験を独立再実行して結び付きを確認する。

## 2. 変更内容

### 2.1 試験

【実測】`tests/test_authority_reference_checker.py`は508行から460行へ減り、試験関数11件、引数展開後19件を
維持した。変更は次のとおりである。

- 7許可キーの合成文書を作る`_full_fixture`、複数参照を組み立てる`_list_block`、関連する合成データを削除した。
- 正常例を、実文書2件・7許可キー全種・11参照の直接照合へ置き換えた。
- 許可キー行の同居値4入力を、単一参照形式と複数参照形式の各1入力へ縮めた。
- 不正経路の既存入力表へNUL文字を1入力追加した。
- 空参照の既存入力表へ、正常文書と参照0件文書を同時に渡す1入力を追加した。

【判断】件数19の維持を目的にしていない。同じ拒否分岐の重複2入力を外し、別の分岐を守る不足2境界へ
入れ替えた結果である。大きな合成fixtureを除き、現行利用先を試験から直接読めるようにした。

### 2.2 検査コード

【実測】`tools/development/authority_reference_checker.py`では、`Path(relative)`と
`(root / relative).resolve()`の経路生成・解決だけを`try`で囲み、`ValueError`と`OSError`を既存の
`invalid`へ写した。内容識別値計算や対象文書の読込み例外は、この捕捉範囲へ含めていない。

【実測】冒頭の状態宣言を次へ変更した。

| 変更前 | 変更後 |
| --- | --- |
| `lifecycle: provisional` | `lifecycle: active` |
| `normative_status: non-normative` | `normative_status: operational-guard` |
| `promotion_required: true` | `promotion_required: false` |

【判断】REDでは暫定宣言を維持し、実文書照合とNUL境界が成功したGREENと同じ変更単位で現役宣言へ変えた。
現在の利用先は、正規全試験が通常収集する対象試験である。

## 3. 反証

反証はGREEN commitをリポジトリ外へ展開した4つの一時複製だけで行った。

1. 【実測】現行Planの`intent_ref`のSHA-256を一文字変更すると、実文書正常試験が失敗し、終了コード1になった。
2. 【実測】許可キー行の同居値拒否分岐を無効化すると、残した単一参照形式と複数参照形式の2件が失敗し、
   終了コード1になった。
3. 【実測】文書ごとの参照0件判定だけを無効化すると、正常文書と空文書を混ぜる新境界が失敗し、終了コード1になった。
4. 【実測】経路解決の`ValueError`捕捉だけを外すと、NUL文字の新境界が例外で失敗し、終了コード1になった。

【判断】4条件は互いに別の欠陥を検出する。実文書接続、同居値拒否、文書ごとの空合格禁止、安定した不正経路拒否を
一つの現在利用契約として守っている。

## 4. 変更範囲と並行commit

【実測】G01の実装commitは次の2件で、それぞれ宣言path一件だけを変更した。

| commit | 変更path |
| --- | --- |
| `ef0aadc` | `tests/test_authority_reference_checker.py` |
| `e29c700` | `tools/development/authority_reference_checker.py` |

【実測】REDとGREENの間に、別作業のcommit `6edf3a6`が入り、立て直し計画、TODO、新しい追補判断を変更した。
G01の2 commitにはこの3 pathの変更は含まれず、作業ツリーの競合もなかった。正規全試験は`6edf3a6`を含む
GREEN後の状態で成功した。

【記録】`6edf3a6`は、第3段中に追加・変更した成果物の現在利用先、守る性質、重複、再利用・共通化、四分類を
段完了前に確認する条件を追加した。今回の成果物については次節で先行して確認する。第3段全体の列挙と完了判断は
本作業へ広げない。

## 5. 今回作成・変更した成果物の役割

| 成果物 | 現在の利用先 | 守る性質 | 重複・再利用 | 四分類 | 役割終了時 |
| --- | --- | --- | --- | --- | --- |
| 検査コード | 対象試験を介した正規全試験 | 実文書の現在参照が実在し、現行bytesと一致し、不正経路を安定して拒否する | 既存`file_sha256`と既存全試験を再利用。新検査器なし | 現在の動作保証 | 対象2文書が現役でなくなった時に、試験・許可一覧と同じ意味単位で再評価する |
| 対象試験 | 正規全試験 | 実文書2件・11参照、同居値、空文書混在、NUL文字を含む19条件 | 重複2入力と合成fixtureを整理済み | 現在の動作保証 | 検査コードの利用終了時に同時整理する |
| 作業票v1/v2 | 独立レビューと将来の復旧 | 承認範囲、三案、TDD、停止・完了条件 | v2はv1の比較表だけを置換し、履歴を保持 | 履歴・監査資料 | Git履歴として保存する |
| 開始前レビューと限定修正後確認 | 実装開始根拠 | 比較規則と開始条件 | 一回の限定修正で閉じた | 履歴・監査資料 | Git履歴として保存する |
| 本Evidence | 独立完了レビューと将来の調査 | 実施、結果、反証、役割分類 | 既存Evidence形式を利用。新台帳なし | 履歴・監査資料 | Git履歴として保存する |

【判断】今回追加・変更した成果物に、役割不明または役割終了のものはない。コードと試験は一つの現役保証、
文書はその判断と実測を保存する監査資料である。共通化のための新しい補助コード、設定、台帳、関門は追加していない。

## 6. 内容識別値

| 対象 | SHA-256 |
| --- | --- |
| `tests/test_authority_reference_checker.py` | `70571cee5012d4a296ea5d3843829fcddf65b642216abe33d379906e5868dcde` |
| `tools/development/authority_reference_checker.py` | `d00cefbf806e3c3efc80755f04bc5f40a2a0a68f9f36eccc28c5f0da8f510ee2` |
| 許可一覧（不変） | `560a835103765149f7e02b52876b6d2cec2e4817e7ec94c8ab1cfea85cd744b2` |
| 初期開発チェックリスト（不変） | `16e8672cdf8d833f6deb879a1b3344702cbc45f068ded4aa928057d9db0abe76` |
| 現行Plan（不変） | `1a73597605eafb65a2259ccf19431e3aba041564d03fdb279150042a9bd0962f` |

## 7. 未実施

【未実施】許可一覧、実文書、設定、TODO、Issue、既存Evidence、中央の作業遷移処理、他の試験の変更、
全Markdown探索、新しい検査器・台帳・設定・関門、外部送信、Claude確認、Issue状態反映、別群、
第3段全成果物の列挙、第3段完了判断は行っていない。
