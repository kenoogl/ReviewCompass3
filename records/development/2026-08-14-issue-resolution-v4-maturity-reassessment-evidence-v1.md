# Issue解決処理v4の成熟度精査 Evidence v1

## 1. 判定

【判断】`修正後に再判定`。

【判断】現行コードをそのまま正式利用可能とは判定しない。止める原因は一つである。Issue更新後、解決記録の
保存先フォルダ作成が失敗すると、例外で停止する一方、Issueは`resolved`へ変更されたまま残り、解決記録は作られない。
「失敗時は元へ戻し、片方だけを残さない」という正式利用の安全境界を満たさない。

【判断】対象Issue `ISSUE-AUTHORITY-REFERENCE-DIGEST-CHECK-001`の状態反映は開始しない。Issueは
version 1、`registered`のまま維持する。コード修正、試験追加、成熟度宣言変更、TODO更新も本作業では行わない。

## 2. 固定材料

- 作業票：`docs/development/2026-08-14-issue-resolution-v4-maturity-reassessment-work-ticket-v1.md`
- 作業票commit：`b244308`
- Human判断：2026-08-14、選択肢1「別の小さい作業単位で成熟度を精査する」を選択。

【実測】固定材料は次のとおり一致した。

| 対象 | SHA-256／状態 |
| --- | --- |
| `tools/development/issue_resolution_v4.py` | `770585427e6185730506ec6aa5da8004a79d77e2cee00e9b4210290d03a2bae8` |
| `tests/test_issue_resolution_v4.py` | `d1d09ab998ebed10a85a9f93613463ba756593052a214853d02b52aab749a4fb` |
| `config/development-issue-resolution-pilot-v4.json` | `ed274e487318d44baed701ffbc8a1130df3e9d81cadca96515848a2bea228a8e` |
| 2026-08-10独立完了再レビュー | `0f53e5527772f8d74fec7c71a420c07c2e2155951be070423ff87ac70e157bd5`、`verified` |
| 2026-08-14状態反映開始前レビュー | `b6bab9acd0cffa1013cd13c6f284098f253c089fce748fd5310ed6e7055c6a28`、`開始不可` |
| 対象Issue | SHA-256 `d260ed570598f56ada2cd6b4e54f15543bba0e792db65c14403a038f8100afbe`、`registered` |

【実測】対象コードはcommit `9cef9ac`、対象試験はcommit `4f39479`以後、現在まで差分0だった。

## 3. 役割と既存の安全境界

【判断】対象は製品コードではなく、開発支援コードである。ReviewCompass3の利用者向け機能ではなく、開発中の
Issue台帳をHuman判断に従って更新する。

【実測】コードを構造分解し、次の境界を確認した。

- 遷移元を`registered`だけに限定し、遷移先を設定内の終端状態だけに限定する。
- Human判断記録を6項目ちょうどのJSONとして読み、判断者、日時、Issue、遷移先、文言、SHA-256を一致確認する。
- Evidenceを1件以上要求し、相対path、リポジトリ内、実在、SHA-256一致を確認する。
- 対象Issueの既存変更は`state`と`content_digest`だけである。
- 解決記録は`records/development/`配下へ新規作成だけを許す。
- Issue単体と全Issue台帳を事後検証する。
- Issueまたは解決記録のファイル書込み失敗と、事後検証失敗について復元処理を持つ。
- 外部送信、Git履歴操作、他Issueの更新は行わない。

## 4. 現在環境での既存試験

次はすべて単独commandの終了コードで確認した。

| 区分 | 結果 | 終了コード |
| --- | --- | --- |
| `tests/test_issue_resolution_v4.py -q` | 24件成功 | `0` |
| `tests/test_issue_intake_v4.py`、`test_issue_intake_v4_single_candidate.py`、`test_issue_resolution_state.py` | 67件成功 | `0` |
| 既存の三つの復元試験だけ | 3件成功 | `0` |

【判断】既存試験が検査する範囲は現在も成立する。今回の欠陥は、既存の三つの復元試験が扱う故障地点とは異なる。

## 5. 使い捨て複製での予定操作

【実測】現在のHEADを`git archive`でリポジトリ外へ展開し、実リポジトリを変更せずに次を確認した。

### 正常例

- 対象Issue：`ISSUE-AUTHORITY-REFERENCE-DIGEST-CHECK-001`
- 遷移：`registered`から`resolved`
- Evidence：G01実施EvidenceとG01独立完了レビューの2件
- 結果：終了コード0
- 既存Issueで変わったkey：`state`と`content_digest`だけ
- 解決記録：対象Issue、遷移、Human判断記録、Evidence 2件を保持

### 既知の異常例

| 反証 | 結果 | Issue | 解決記録 |
| --- | --- | --- | --- |
| commandの判断者とHuman判断記録の判断者が不一致 | `human_ruling_invalid`、終了5 | bytes不変 | 作成なし |
| EvidenceのSHA-256が古い | `evidence_invalid`、終了5 | bytes不変 | 作成なし |

【判断】予定入力の正常経路と、既知の二つの拒否境界は成立する。

## 6. 新しく成立した反証

### IR-MAT-001：解決記録の親フォルダ作成失敗でIssueが復元されない

【実測】リポジトリ外の使い捨て複製で、許可範囲内の新しい解決記録pathを指定し、その親フォルダの
`mkdir`だけに`OSError`を注入した。

結果：

- 呼出しは`OSError`で停止した。
- 対象Issueは元のbytesへ戻らなかった。
- 対象Issueのstateは`resolved`のまま残った。
- 解決記録は作成されなかった。

【実測】`record_file.parent.mkdir(...)`は対象Issueの更新後、解決記録の書込みと復元を囲む`try`の内側で
実行される。ただし、この`try`が捕捉するのは`ResolutionError`だけであり、`mkdir`が直接出す生の`OSError`は
復元処理へ入らない。既存の`test_record_write_failure_restores_issue_without_partial_record`は、親フォルダが
既に存在する状態で`_atomic_write`を失敗させるため、`ResolutionError`へ変換されて復元される。この一段前の
`mkdir`失敗は検査しない。

【判断】これは正式利用を止める。Humanが承認したIssue状態だけが変わり、承認根拠を固定する解決記録が無い状態を
残し得るためである。処理時間や実行頻度の問題ではない。

## 7. 最小修正候補と三案

本作業では修正しない。次作業をHumanが承認する場合の候補だけを示す。

| 案 | 内容 | 単純さ | 処理時間 | メモリ使用量 | 頑健さ | 変更範囲 | 保守負担 | 戻しやすさ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | 解決記録の親フォルダを事前条件とし、存在しなければIssue更新前に拒否する | 単純 | 差は無視できる | 差は無視できる | 新しいフォルダを正規に作る現在の用途を狭める | コードと試験 | 小 | 一変更を戻せる |
| B | 親フォルダ作成をIssue更新前へ移し、作成失敗を安定した不合格へ変換する | Cより変更が多い | 差は無視できる | 差は無視できる | Issue更新前に失敗するため復元へ依存せず、新規pathも維持 | コードと試験 | 小 | 一変更を戻せる |
| C | 親フォルダ作成を現在の位置に残し、既存の捕捉対象を`OSError`へ広げて既存の復元処理へ入れる | 最も単純 | 差は無視できる | 差は無視できる | 観測した片残りを防ぐが、Issue更新後の復元へ依存する | コードと試験 | 最小 | 一変更を戻せる |

【判断】観測した欠陥だけを直す最小案は案Cである。案Bは失敗をIssue更新前へ移せるため復元依存を減らすが、
処理位置の移動と失敗変換が必要で、案Cより変更が大きい。案Cは現在の処理順と既存の復元構造を保ったまま、
捕捉する失敗を一種類増やす。案Bと案Cのどちらも観測した片残りを防げるため、単純さ、変更範囲、保守負担、
戻しやすさを合わせて案Cを選ぶ。ただし、これは現役化や状態反映とは別のコード修正作業であり、Human承認、
失敗を再現する試験、実装修正、独立完了レビューを要する。

## 8. 手戻り

【実測】最初の親フォルダ故障注入は、macOSの`/var`と`/private/var`という同一実体のpath表現差により、注入地点へ
一致せず通常成功した。両pathを`resolve()`して同じ実体表現へ揃えた一回の再実行で§6の反証が成立した。

- 対象操作：親フォルダ作成失敗の注入
- 期待executor／実executor：精査用の一時Python処理／同処理
- 手作業理由：なし
- 事象とEvidence：初回は注入されず正常遷移、訂正後は`OSError`と片残りを再現
- 機械処理候補・route：一時確認処理のpath比較訂正であり製品欠陥とは分離。本記録だけに残す

## 9. 未実施

【未実施】対象コードと試験の変更、成熟度宣言変更、対象Issueと他Issueの状態変更、Human判断記録と解決記録の作成、
TODOと第4段資料の更新、新しい機構・検査器・試験・関門、履歴書換え、外部送信、全試験、第3段または第4段の完了判断。

【実測】精査終了時の対象IssueはSHA-256
`d260ed570598f56ada2cd6b4e54f15543bba0e792db65c14403a038f8100afbe`、state `registered`のままである。
