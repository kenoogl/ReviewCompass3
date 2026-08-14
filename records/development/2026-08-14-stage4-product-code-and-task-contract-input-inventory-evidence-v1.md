# 立て直し計画v5 第4段 製品コード候補とTask Contract入力の目録 Evidence v1

- 作成日：2026-08-14
- 状態：`candidate_pending_independent_completion_review_and_human_decision`
- 観測commit：`66d608e5b5d605ddaf387bbd75a507ac934800c6`
- 作業票：`docs/development/2026-08-14-stage4-product-code-and-task-contract-input-bootstrap-work-ticket-v1.md`
- 作業票SHA-256：`26c0b1d117067112881a289fc871a33c374d6693e6c157b2c96c10bb4d5557c8`
- 開始前レビュー：`records/development/2026-08-14-stage4-product-code-and-task-contract-input-start-review-v1.md`
- 開始前レビューSHA-256：`d4eafd3048f5a4417228430ae4cdc8dfb88d3fd610674707fc8374b3e72d7206`

## 1. 目的と境界

【記録】利用者は、作業票§13の四点を承認した。本記録は、固定した152件のコード候補を意味群へ一度ずつ
割り当て、「何に使うか」と「今後どう扱うか」を別々に分類し、最初に詳しく確認する製品処理候補を一群だけ
示す。

【判断】本記録の`採用候補`は、利用者が正式採用を判断できる候補という意味であり、正式採用そのものではない。
コード内にある`provisional`（暫定）表示も変更しない。コード、試験、設定、上流文書、Issueは変更しない。

## 2. 固定した母集合

【実測】観測commitのGit treeから作業票と同じ規則で再生成した。

| 集合 | 件数 | path一覧SHA-256 | Git tree entry一覧SHA-256 |
| --- | ---: | --- | --- |
| コード候補 | 152 | `5d116414e108851af39710abc8483c0a5c48bd7b6a9a7db8377d014dc650e3ed` | `c8c1cf64d011ce15234a584b1604953907bd87051673eb74df8475ebcda4c29e` |
| 試験関連 | 192 | `f6db6ef2955bb4dcec171580e01660681b51704af47eaa823ad5f481242a856f` | `3426dbe2529af2f2971eb1d5c7c75678da39726d7d416081aae1131837d1d821` |

【実測】コード候補には`tools/**/*.py` 150件、拡張子なしの実行file
`tools/deployment/installed/trusted-review-send` 1件、rootの`setup.py` 1件が含まれる。試験関連192件は
`tests/**/*.py`と`conftest.py`であり、コード候補へ混ぜていない。

## 3. 機械処理と途中訂正

【実測】Git treeを正本にし、一時的なPython構文木解析で、各pathの内容識別値、公開処理、直接の読み込み先、
読み込み元、`__main__`入口を収集した。試験fileは、コードのモジュール名またはpathを直接含むかを別計算した。
分類の意味判断には、先頭説明、現在の案内・Decision、上流候補の機能区分も使った。

【実測】最初の一時解析では、絶対指定の読み込み先へ現在のモジュール名を誤って重ねたため、内部読み込み関係が
0件になった。この結果は分類へ使わなかった。

| 項目 | 内容 |
| --- | --- |
| 対象操作 | Pythonの直接読み込み関係の抽出 |
| 期待した実行者 | 一時的な構文木解析 |
| 実際の実行者 | 同じ一時解析。ただし絶対指定の基準位置を誤った |
| 事象 | 初回出力SHA-256 `01531d7d72cd54595b4acc04a184bd8a7fd78739cf30b434a79f96c2efef183c`、内部関係0件 |
| 機械訂正 | 絶対指定はそのまま、相対指定だけ現在位置から解決する式へ限定訂正 |
| 採用した結果 | 訂正後出力SHA-256 `7cbee7464b65fc99ea741236046e9d1579428255468344efc563a3c106d50447`、内部関係201件 |
| route | 初回出力を破棄し、訂正後出力だけを分類入力にした。恒久script・検査器・試験は追加しない |

【判断】これはrepository成果物の欠陥ではなく、作業中の一時解析の欠陥である。開始前に訂正し、訂正前の結果から
分類を進めなかったため、本Evidenceの報告不一致にはしない。

## 4. 分類結果の完全性

【実測】152件を30群へ割り当てた。正準化規則は
`group_id<TAB>用途<TAB>今後の扱い<TAB>path<LF>`を群順・群内path昇順に並べる方式である。

- 分類一覧SHA-256：`1863fefc7b6dfd19c88c7b13475464962a87d4594d2b487d40985a7c21017e6e`
- 割当件数：152
- 重複割当：0
- 未分類：0
- 母集合外混入：0
- 意味群：30

【実測】直接のモジュール名またはpath参照を持つ試験fileは、192件中170件だった。残る22件は共通fixture、設定、
repository全体検査等であり、「直接文字列が無い」ことを「試験が無い」とは解釈しない。

## 5. 二軸分類の集計

### 5.1 用途

| 用途 | path数 |
| --- | ---: |
| 製品 | 71 |
| 開発支援 | 71 |
| 共有 | 10 |
| 用途不明 | 0 |
| 合計 | 152 |

### 5.2 今後の扱い

| 今後の扱い | path数 |
| --- | ---: |
| 採用候補 | 34 |
| 保留 | 106 |
| 使用停止 | 12 |
| 履歴のみ | 0 |
| 合計 | 152 |

【判断】`用途不明`が0なのは、全pathに現在の先頭説明、実行入口、読み込み関係、関連試験、または固定Decisionの
いずれかがあり、製品、開発支援、共有の区別を付けられたためである。これは正式採用済みという意味ではない。

【判断】`履歴のみ`を0にしたのは、過去段階の処理にも現在の試験や参照が残り、「現在の実行には使わない」と
断定できなかったためである。過去段階用という理由だけで履歴専用にしない。

## 6. 30意味群

各`tree SHA-256`は、観測commitの`mode type object-id<TAB>path<LF>`を群内path昇順で連結した値である。

| 群 | 意味 | 用途 | 今後 | path数 | 関連試験file数 | tree SHA-256 | 主な根拠 |
| --- | --- | --- | --- | ---: | ---: | --- | --- |
| G01 | 配布用パッケージ入口 | 共有 | 保留 | 1 | 5 | `940ede49c6849d8bf408301c676d59f9de9ffa76dcd902d07b2668c67623e0c4` | 製品用Session入口と暫定レビュー入口の両方を配布するが、説明がscratch rebuildのまま |
| G02 | レビュー材料・実行・結果処理 | 製品 | 保留 | 14 | 18 | `2bb33f06b41ff5148a8cdbbc19a85a955c92bf2681c67e5e8b46d3bb2e85739d` | Review Context、実行、結果保存、triageに対応するが、全fileが暫定で外部runner境界を持つ |
| G03 | 第1段の材料列挙・移植候補・完了関門 | 開発支援 | 保留 | 3 | 3 | `17bd3a5553f178180a3750a73832f373b15b8063bb2c49b585fe93b564693f81` | 完了済み第1段に限定された処理。現在試験が残るため履歴のみとはしない |
| G04 | 不変結果保存の共有部品 | 共有 | 採用候補 | 1 | 3 | `1a4c30241eacff3540977125e3a74c3c9b6bed465aa342a3f65e52d2e02e15bb` | レビュー処理と開発支援の両方から読み込まれる |
| G05 | 内容識別値・例外・出力・パスの共有部品 | 共有 | 採用候補 | 5 | 5 | `7678443adb327937728e654417ac8de9c330de908f5f1ecdfdee4efd2b28afb5` | 製品候補と開発支援の双方から使われ、共有正本Decisionがある |
| G06 | リポジトリ結合と配置ルート | 共有 | 保留 | 2 | 2 | `cde7e282064aa03259169a77a84ca3c8f12923673d9f25b28914e3d4bce90675` | 製品配置と開発時のGit捕捉から使うが、耐久identity等が未完了 |
| G07 | 信頼済み外部実装送信経路 | 開発支援 | 使用停止 | 3 | 1 | `210ea380793f955aa56d2ef079ace2bd36f20adcf84b6474d1570a0e63a07add` | 第2段DecisionがClaude／Codex外部実装経路の使用停止を維持 |
| G08 | 設計と受入条件の適合検査 | 製品 | 保留 | 2 | 2 | `2eddc3eaca7b441759abc3bf9b99bff1bae8bcee6ec7d42d4cf4b116097b81a1` | 第5段候補の設計・受入検査で、現行製品入口へ未接続 |
| G09 | 開発方針とレビュー計画 | 開発支援 | 採用候補 | 4 | 7 | `076d85d695ffed396c5b46fd068142d7542edd0580b57f604e288161dc023cfe` | AGENTS.mdから到達する現行方針、参照検査、計画生成入口 |
| G10 | 開発環境と正規試験実行 | 開発支援 | 採用候補 | 4 | 7 | `ab82294cc6868fdd40b20944af6b576f7fd785c7878b4635031e528e40248db2` | 現在のPython環境と正規全試験受領記録を作る現役入口 |
| G11 | TODO引継ぎと作業単位遷移 | 開発支援 | 採用候補 | 7 | 14 | `5dbdaaddaaf365549492c324b851ac6b2855eb45794ea9e3a5ef71155eb5c9c6` | AGENTS.mdが現在の共通入口として要求し、本作業でも利用 |
| G12 | 開発時の静的検査と保証境界 | 開発支援 | 保留 | 4 | 4 | `9807ea2be87512ca959686c60b3a58c336aae88e650d4a21fb61a5994ded4073` | 検査対象が限定され、process目録には既知の見逃しがある |
| G13 | 既存処理の再利用・統合候補探索 | 開発支援 | 保留 | 4 | 6 | `88096545d4633753cafc1a2209afc99e545e44d14f6f7b32900268443b6cff55` | REQ-WORKFLOW-009候補に関係し、正式採用・実装は後続判断 |
| G14 | Claude・Codex外部実装連携 | 開発支援 | 使用停止 | 8 | 13 | `65f13f23ad2a8394d21aaa55c7f17ba527cc11ea2b7f97e6cdf16d2e0ec269c4` | 第2段Decisionが外部実装経路の使用停止を明示 |
| G15 | 改善候補とIssueの登録・検証 | 開発支援 | 採用候補 | 2 | 18 | `8e5567af52588a71d248193296a461c081b29f96da0b041cfac5ed09126dbdfd` | AGENTS.mdが改善候補登録とtriageの既存経路として指定 |
| G16 | 旧Issue解決Pilotの状態・事後確認 | 開発支援 | 保留 | 2 | 4 | `f3187f7b83e1969779e95fdfaa29228d48871fc578a1393e1307c708211137e3` | 旧Pilotの補助処理で、現在の正式な状態反映には使わない |
| G17 | Issue状態反映V4 | 開発支援 | 使用停止 | 1 | 1 | `8d282595d38caba36738b54712dc4ed76dcea740b8de08335537fc8e43bba9d7` | 利用者の中止Decisionにより暫定・使用停止のまま維持 |
| G18 | 操作分類と読み取り専用実行 | 開発支援 | 保留 | 2 | 4 | `4e8a4a856aae449ad25db8ec92eb4bb9bd56c6b035a5dedd14272d8431a55740` | 承認済みの狭い開発用sliceだが製品入口へ未接続 |
| G19 | 旧Session Log Bootstrap | 開発支援 | 保留 | 1 | 6 | `080c9e03a22de50f66f7c59747b3f71c7d160da0eb92786f94d526d362541864` | Work 1Bの自己開発用投影で、現在のSession製品入口とは別 |
| G20 | 外部送信の段階的安全境界 | 製品 | 保留 | 7 | 7 | `9d775f21971bdb5d4a5b5ca6bd8eb5e3ddf5a28350de749711f4cf9d6cd23743` | 製品の送信安全境界候補だが、senderは実送信不可で正式承認前 |
| G21 | 第2段の材料抽出・再判定・完了確認 | 開発支援 | 保留 | 23 | 23 | `3e5a8a6619c73718d86b4273bf0986d59444d6d43fc1520e7a083710198bdf49` | 完了済み第2段用。現在試験が残るため一括で履歴専用・削除にしない |
| G22 | 配置基準 | 共有 | 採用候補 | 1 | 8 | `9e05e3645ce803f1245235aad0648dd582f60a912acb121f4799291066d406a4` | Session移行、配置root、開発cacheの複数経路から利用 |
| G23 | 旧要求成果物の検証・移行 | 開発支援 | 保留 | 2 | 4 | `b929a97a3ab0dca2095ee6a037fa73f5bcfc0c68fbdfbae6a0f8574dd73d62ed` | 旧37要求の移行用で、現在の製品入口ではない |
| G24 | 要求の固定入力・機能分割・由来追跡 | 製品 | 保留 | 5 | 5 | `aee6cf4c48ca6b8c56ee8b2bdcc1d8824b8ec61e398befcb1fd346bbe198fe26` | Feature・Trace候補に対応するが、上流文書もコードも暫定で実行入口なし |
| G25 | Session記録の解析・伏字化・要約・来歴生成 | 製品 | 採用候補 | 10 | 14 | `f476cbf6df63bc2accfb188764b2b8216aefdb7c446572b40b56b2cbcab861e4` | 公開関数入口、閉じた読取り範囲、既存の入力・出力・停止試験がある |
| G26 | Session記録の設定・発見・保全・保存CLI | 製品 | 保留 | 9 | 15 | `a2768896f193ec469ec91ecc6bbb5846bded1cfb18dcab830e39856fa37c1197` | `repository_root`省略時に保存境界を強制しない反例が成立 |
| G27 | Session記録の配布・導入・定期実行 | 製品 | 保留 | 16 | 24 | `7c0deed0d476d1219dca44f5a77ec9c31f9bd55455c1699956032dff11800ba9` | 導入、解除、hook、scheduler等の環境変更を含むため最初の候補から外す |
| G28 | Session記録の継続回収・移行・私有領域検証 | 製品 | 保留 | 3 | 7 | `3b9639c8065f87aa073c2398577739d5d351cad330bf929912fcf67d6d3e85b8` | 継続回収と移行を含み、G25より副作用・依存が広い |
| G29 | 第0段Session記録完了関門 | 開発支援 | 保留 | 1 | 1 | `81e2ccf657d7e1ee9c1f1ec27602aab6a79c195ff050deabb2343486e71092a6` | 完了済み第0段の監査入口 |
| G30 | 最小Task Contract実行基盤 | 製品 | 保留 | 5 | 6 | `522530e034e95957699a6fae724b095290ae70310f96d93d71f521f0bdf66c83` | 中心機能候補だが、第4段で正式利用・実装を前倒ししない境界がある |

## 7. 最初の製品処理候補の比較

【判断】実行入口と利用者向け結果を持つ群から、次の三群を比較した。G30は作業票で未完成のTask Contract基盤を
最初の候補にしないと決めているため、比較対象から外した。

| 候補 | 利用者が得る結果 | 依存範囲 | 現在保証 | 副作用・戻しやすさ | 判断 |
| --- | --- | --- | --- | --- | --- |
| G25 Session記録の解析 | 一つのローカル記録から、伏字化転写、要約、来歴をメモリ上に得る | 10 path、群外依存0 | 直接参照14試験file。公開関数あり | raw fileの読取りだけ。file書込み、外部送信、外部processなし | **推奨** |
| G02 レビュー処理 | 固定材料から複数担当レビュー結果とtriageを得る | 14 path＋保存共有部品＋runner | 18試験fileだが全file暫定 | runner境界があり、外部実行経路の使用停止と切り分けが必要 | 保留 |
| G24 要求処理 | 固定入力から機能分割・由来記録を得る | 5 path | 5試験file | file書込みは閉じられるが、現在の実行入口がない | 保留 |

## 8. 推奨候補G25の詳しい確認

### 8.1 利用者向け処理

【判断】最初の候補は、次の一文で表す。

> 利用者が指定した一つのローカルのセッション記録を読み取り、機微情報を除いた転写、要約、来歴の候補を
> メモリ上に生成する。

【実測】現在の直接入口は公開関数`tools.session_logs.pipeline.prepare_artifact`である。公開関数は、他の製品処理から
明示的に呼び出せる処理入口を意味する。

```text
prepare_artifact(raw_log, raw_root=..., rules=..., tool_version=..., commits=(), changed_files=(), allow_patterns=())
```

【判断】当初はG25へ設定・発見・保全・保存CLIも含めていた。しかし、設定から`repository_root`を省略すると、
rawと転写の保存先がrepository内でも受理される反例が成立した。保存処理を同じ採用候補へ含めず、G26として
保留へ分けた。最初の候補は、書込みを持たない解析処理G25に限定する。

### 8.2 固定コード範囲

【実測】`prepare_artifact`から静的に到達するのは、付録AのG25にある10 pathだけで、群外の直接読み込み先は0件である。
10件のGit tree entry一覧SHA-256は
`f476cbf6df63bc2accfb188764b2b8216aefdb7c446572b40b56b2cbcab861e4`である。G26、G27、G28や
外部送信G20からG25を利用する逆向きの参照はあるが、G25からそれらを読み込まないため、最初の候補の前提に含めない。

### 8.3 入力、出力、停止

| 項目 | 現在コードで確認した内容 |
| --- | --- |
| 入力 | 一つのClaude／Codex JSONL path、raw root、伏字化規則、tool版、任意のcommit名・変更path |
| 読取り | source種別を識別し、raw fileを解析し、原文bytesの内容識別値を来歴へ記録 |
| 出力 | `PreparedArtifact`値。種別、共通event、伏字化転写、要約、来歴、解析上の注意、伏字化件数を持つ |
| 失敗 | 種別不明、raw読取不能、解析不能、機微情報残存、raw root外等を例外で停止 |
| 外部作用 | file書込みなし、network送信なし、外部processなし。入力raw fileだけを読む |
| 環境参照 | G25自身は環境値を解決しない。呼出し側から渡されたpattern規則を使い、環境依存規則の役割名だけを規則の内容識別値へ入れる |

【判断】G25は外部送信、権限付与、Issue状態更新、履歴書換え、file書込みを必要としない。入力を読んで値を返すだけで、
10 pathに閉じるため、他候補より境界を説明しやすく、戻しやすい。

### 8.4 最初のTask Contractへ渡す最小入力

【記録】既存構想`docs/concepts/2026-08-02-task-contract-centered-engineering.md`の内容識別値は
`80f388b9308450f1758f623346e25fa6623c8d5d59cb32979436ee3831af1d91`である。同文書§4.9の
最小核と、実行可能な契約に追加する項目から、G25に必要なものだけを次のように選ぶ。

| 最小項目 | G25から固定できる入力 | 第5段で確定すること |
| --- | --- | --- |
| Identity | 候補名G25、観測commit、10 pathのtree SHA-256、対応候補`REQ-SESSION-001`〜`003`・`REQ-PORTABLE-002`・`004` | 安定した契約ID、契約種別、版、内容識別値、source requirement IDの採否 |
| Responsibility | 一つのローカルSession記録から、伏字化転写、要約、来歴候補をメモリ上に生成する | この一文を正式責務として承認するか |
| Boundary | G25の10 pathと入力raw fileだけを範囲内とし、保存・発見・配布・外部送信・権限変更・Issue更新・Task Contract実行基盤を範囲外とする | downstreamの保存責務を別契約へ渡すか |
| Preconditions | 対応する三形式のJSONL、raw root、伏字化済みpattern規則、tool版を入力とし、G25の正式製品コード採用と契約承認を開始条件とする | 上流候補の採否、入力版とfreshness |
| Context Obligations | 固定した10 path、直接関連14試験file、55件成功記録、raw形状fixture、上流候補、既知の上流不一致3件を材料とする | 各材料のrequired／optional、freshness、競合時の扱い |
| Allowed Capabilities | 指定された一つのraw fileの読取りとメモリ上の計算だけを許す | 読取り対象root、資源上限。書込み、network、外部process、環境値解決は許可しない |
| Expected Outputs | `PreparedArtifact`のsource種別、共通event、伏字化転写、要約、来歴、解析上の注意、伏字化結果 | 正式な出力schemaと保持先。保持処理自体は本候補外 |
| Acceptance Criteria | 三形式を識別して決定的な値を返し、種別不明・読取不能・解析不能・機微情報残存・raw root外では停止する | 正式oracle、受入例、完了所有者 |
| Provenance Obligations | raw相対path・行範囲・raw／転写／要約／規則の内容識別値・tool版・任意のcommit名／変更pathと、固定コードtree SHA・試験受領記録を結ぶ | 保存期間、機密区分、実行記録の正本 |
| Escalation Policy | 入力種別不明、機微情報残存、root逸脱、固定入力のstale、上流競合、範囲外能力が必要な場合は停止してHumanへ戻す | retry可否と、意味的裁定・外部送信・不可逆操作の承認点 |
| 版付きdependency | G25の観測commitとtree SHA、既存構想の上記SHA、上流候補と55件の試験状態 | 契約確定時に採用する各版。未承認候補を暗黙に依存へ昇格しない |

【判断】この表で、最初の契約案を作るための責務、境界、前提、材料、能力、成果、受入、来歴、Humanへ戻す条件を
G25の現状へ対応付けられる。第5段では右列を定義挑戦とHuman判断で確定する。本記録はTask Contractそのもの、
契約ID、schema、生成器、状態機械、実行許可機構を作らず、G30を必須依存にしない。

### 8.5 G26を保留にした反例

【実測】`repository_root`を持たず、raw・転写・要約・来歴の各rootを現在のrepository内へ置く一時設定を作り、
`load_config`へ渡した。結果は次のとおりだった。

```json
{"accepted": true, "repository_root_is_none": true, "raw_inside_project": true, "transcript_inside_project": true}
```

【判断】G26の保存CLIは、`repository_root`がある場合には私有データとGit管理物の境界を検査するが、省略時には検査しない。
したがって、G26の9 pathは製品／保留とし、最初の正式製品コード集合へ含めない。修正案や追加試験は本作業の範囲外である。

### 8.6 上流候補との対応

【記録】統合計画候補の`FEAT-SESSION-RECORDS`と`REQ-SESSION-001`〜`003`、
`REQ-PORTABLE-002`・`004`が対応候補である。統合Intent候補の「必要な材料を明らかにする」、
「問題を隠さず戻れるようにする」、機密情報と生会話記録を分離する原則とも意味上は整合する。

【判断】これら上流文書はすべて暫定候補であり、本記録だけで正式要求・Featureへ昇格しない。G25の採用判断は、
現状コードを第5段で再利用できる資産として識別する判断に限り、将来の振る舞いや完成を承認しない。

### 8.7 試験と反証

【実測】G25のmodule名またはpathを直接参照する試験fileは14件だった。この14件を一回で実行し、
`55 passed in 0.20s`、終了コード0だった。分割前のSession関連26試験fileも`165 passed in 0.85s`、終了コード0である。

【実測】中心判断を崩す反例として次を個別実行した。

| 反例 | 試験 | 結果 |
| --- | --- | --- |
| 高い乱雑性を持つ未登録値が残っても成果候補を返す | `tests/test_session_log_pipeline.py::test_pipeline_fails_closed_when_high_entropy_remains` | 1 passed、終了0。値を返さず停止 |
| 種別不明のJSONLを既知形式として推測する | `tests/test_session_log_source_adapter.py::test_common_entry_rejects_unidentified_input` | 1 passed、終了0。未対応として拒否 |

【判断】反例は成立せず、G25を最初の候補として提示できる。ただし、試験成功は正式採用や製品完成の代わりではない。

## 9. 上流文書候補と既知不一致

【実測】統合Intent、統合計画、統合用語集の直接参照47件のうち44件は現在値と一致し、次の3件だけが不一致である。

1. 統合Intent候補が参照するsource catalog。
2. 統合計画候補が参照する開発方針。
3. 統合用語集候補が参照する統合Intent候補。

【実測】上流候補9件はすべて`provisional`である。独立した正式Feature PolicyとArchitecture Policyは存在せず、
統合計画候補および要求・設計候補内の節としてだけ存在する。

【判断】3件の不一致を本作業で修正せず、上流候補を自動採用もしない。第4段の採用判断では、上流候補の現在位置と
不一致を限界として引き継ぐ。

## 10. 正式製品コードとしての採用提案

【提案】利用者が第4段で正式製品コードとして識別する最初の集合は、G25の10 pathとする。群外の直接依存はない。
固定commitは`66d608e5b5d605ddaf387bbd75a507ac934800c6`、Git tree entry一覧SHA-256は
`f476cbf6df63bc2accfb188764b2b8216aefdb7c446572b40b56b2cbcab861e4`である。

【判断】ここでいう正式製品コードは、「第5段で製品作業へ再利用できる固定資産として識別する」意味に限る。
各moduleの`provisional`表示が示す実行時成熟度、最初のTask Contract、将来の変更、製品処理の完成を承認しない。

【提案】他の142 pathは次の扱いとし、削除・変更しない。

- 製品／保留61 path：後続の製品処理またはTask Contractごとに別判断する。G26の9 pathを含む。
- 開発支援71 path：製品コードへ含めない。うち17 pathは現在の開発支援採用候補、42 pathは保留、12 pathは使用停止。
- 共有10 path：現在の開発利用を変えず、製品側で必要になった時点に判断する。

## 11. 利用者が判断する点

1. G25の10 pathを、第5段で再利用できる正式製品コード集合として採用するか。
2. G26を含む製品／保留61 pathを未承認のまま維持し、最初のTask Contractの前提へ含めないか。
3. 開発支援71 path、共有10 path、使用停止12 pathを製品コードへ含めない分類を採用するか。
4. 最初にTask Contract化する候補を、G25の読取り専用Session記録解析とするか。
5. 上流候補9件の暫定状態と直接参照不一致3件を限界として残したまま、第4段完了候補へ進めるか。

## 12. 未実施

【未実施】正式製品コードの利用者採用、上流文書候補の正式化、参照不一致3件の修正、コード・試験・設定・schema・
Issue・既存Evidence・TODOの変更、コードの削除・統合、Task Contractの定義・承認・実装、REQ-WORKFLOW-009の
採用・実装、外部送信、権限変更、不可逆操作、第4段完了判断は行っていない。

【未実施】正規全試験は再実行していない。観測commit以後にコード・試験・設定の変更がなく、第3段の正規全試験
1,728件成功が現在のコード状態へ結び付いているためである。本作業ではG25直接関連55件と、分割前のSession関連
165件だけを追加実行した。

## 付録A：152 pathの一意割当

### G01 配布用パッケージ入口

- `setup.py`

### G02 レビュー材料・実行・結果処理

- `tools/bootstrap/bundle_verification.py`
- `tools/bootstrap/closed_payload.py`
- `tools/bootstrap/evidence_closure.py`
- `tools/bootstrap/material_bundle.py`
- `tools/bootstrap/raw_review_store.py`
- `tools/bootstrap/review_assurance.py`
- `tools/bootstrap/review_cli.py`
- `tools/bootstrap/review_contract.py`
- `tools/bootstrap/review_execution.py`
- `tools/bootstrap/review_materials.py`
- `tools/bootstrap/review_pipeline.py`
- `tools/bootstrap/review_response_parser.py`
- `tools/bootstrap/review_resume.py`
- `tools/bootstrap/review_triage.py`

### G03 第1段の材料列挙・移植候補・完了関門

- `tools/bootstrap/migration_candidates.py`
- `tools/bootstrap/source_universe.py`
- `tools/bootstrap/stage_one_gate.py`

### G04 不変結果保存の共有部品

- `tools/bootstrap/immutable_result_store.py`

### G05 内容識別値・例外・出力・パスの共有部品

- `tools/common/__init__.py`
- `tools/common/digests.py`
- `tools/common/errors.py`
- `tools/common/output.py`
- `tools/common/paths.py`

### G06 リポジトリ結合と配置ルート

- `tools/deployment/checkout_relocation.py`
- `tools/deployment/local_integrated_roots.py`

### G07 信頼済み外部実装送信経路

- `tools/deployment/installed/trusted-review-send`
- `tools/deployment/installed/trusted_review_send_dispatch.py`
- `tools/deployment/trusted_claude_transport.py`

### G08 設計と受入条件の適合検査

- `tools/design/bootstrap_conformance.py`
- `tools/design/design_contract.py`

### G09 開発方針とレビュー計画

- `tools/development/authority_reference_checker.py`
- `tools/development/policy.py`
- `tools/development/review_plan.py`
- `tools/development/review_plan_cli.py`

### G10 開発環境と正規試験実行

- `tools/development/bootstrap_environment.py`
- `tools/development/policy_test_runner.py`
- `tools/development/pytest_summary.py`
- `tools/development/task_python_cache.py`

### G11 TODO引継ぎと作業単位遷移

- `tools/development/todo_compaction.py`
- `tools/development/todo_handoff.py`
- `tools/development/todo_handoff_projection.py`
- `tools/development/todo_record_generation.py`
- `tools/development/todo_snapshot.py`
- `tools/development/todo_update_path.py`
- `tools/development/work_unit_transition.py`

### G12 開発時の静的検査と保証境界

- `tools/development/declaration_red_map_check.py`
- `tools/development/process_call_inventory.py`
- `tools/development/python_ast_boundary_check.py`
- `tools/development/verification_boundary.py`

### G13 既存処理の再利用・統合候補探索

- `tools/development/candidate_ranking.py`
- `tools/development/integration_exclusions.py`
- `tools/development/reuse_search_record.py`
- `tools/development/work4a_rebuild_v3.py`

### G14 Claude・Codex外部実装連携

- `tools/development/claude_bootstrap.py`
- `tools/development/claude_bootstrap_cli.py`
- `tools/development/claude_implementation_confirmation.py`
- `tools/development/claude_implementation_executor.py`
- `tools/development/claude_implementation_route.py`
- `tools/development/claude_implementation_route_cli.py`
- `tools/development/pilot_collaboration.py`
- `tools/development/pilot_collaboration_cli.py`

### G15 改善候補とIssueの登録・検証

- `tools/development/issue_intake_v4.py`
- `tools/development/issue_resolution_pilot.py`

### G16 旧Issue解決Pilotの状態・事後確認

- `tools/development/issue_resolution_post_write.py`
- `tools/development/issue_resolution_state.py`

### G17 Issue状態反映V4

- `tools/development/issue_resolution_v4.py`

### G18 操作分類と読み取り専用実行

- `tools/development/operation_routing.py`
- `tools/development/structured_argv_executor.py`

### G19 旧Session Log Bootstrap

- `tools/development/session_log_bootstrap.py`

### G20 外部送信の段階的安全境界

- `tools/egress/__init__.py`
- `tools/egress/approval.py`
- `tools/egress/dry_run.py`
- `tools/egress/gate.py`
- `tools/egress/payload.py`
- `tools/egress/prefilter.py`
- `tools/egress/sender.py`

### G21 第2段の材料抽出・再判定・完了確認

- `tools/extraction/batch_reassessment.py`
- `tools/extraction/candidate_integration.py`
- `tools/extraction/decision_review_material.py`
- `tools/extraction/dependencies.py`
- `tools/extraction/dependency_materials.py`
- `tools/extraction/design_decision_material.py`
- `tools/extraction/destination_classification.py`
- `tools/extraction/empirical_revalidation.py`
- `tools/extraction/essence_ledger.py`
- `tools/extraction/file_edges.py`
- `tools/extraction/followup_resolution.py`
- `tools/extraction/group_coverage.py`
- `tools/extraction/known_positives.py`
- `tools/extraction/population.py`
- `tools/extraction/priority_batches.py`
- `tools/extraction/reassessment.py`
- `tools/extraction/rule_recount_correction.py`
- `tools/extraction/seven_axes.py`
- `tools/extraction/stage_two_audit.py`
- `tools/extraction/stage_two_completion.py`
- `tools/extraction/stage_two_reaudit.py`
- `tools/extraction/structured_batch.py`
- `tools/extraction/structured_materials.py`

### G22 配置基準

- `tools/layout/baseline.py`

### G23 旧要求成果物の検証・移行

- `tools/requirements/artifact_layout.py`
- `tools/requirements/unified_migration.py`

### G24 要求の固定入力・機能分割・由来追跡

- `tools/requirements/boundary_relations.py`
- `tools/requirements/feature_partition.py`
- `tools/requirements/fixed_inputs.py`
- `tools/requirements/requirement_batch.py`
- `tools/requirements/source_trace.py`

### G25 Session記録の解析・伏字化・要約・来歴生成

- `tools/session_logs/parse_claude.py`
- `tools/session_logs/parse_codex.py`
- `tools/session_logs/parse_codex_rollout.py`
- `tools/session_logs/pipeline.py`
- `tools/session_logs/provenance.py`
- `tools/session_logs/redaction.py`
- `tools/session_logs/source_adapter.py`
- `tools/session_logs/source_kind.py`
- `tools/session_logs/summary.py`
- `tools/session_logs/transcript.py`

### G26 Session記録の設定・発見・保全・保存CLI

- `tools/session_logs/cli.py`
- `tools/session_logs/config.py`
- `tools/session_logs/discovery.py`
- `tools/session_logs/locking.py`
- `tools/session_logs/preservation.py`
- `tools/session_logs/regeneration.py`
- `tools/session_logs/repository_context.py`
- `tools/session_logs/storage.py`
- `tools/session_logs/updates.py`

### G27 Session記録の配布・導入・定期実行

- `tools/session_logs/deployment_lifecycle.py`
- `tools/session_logs/deployment_paths.py`
- `tools/session_logs/deployment_preflight.py`
- `tools/session_logs/distribution_validation.py`
- `tools/session_logs/entry.py`
- `tools/session_logs/hook_installation.py`
- `tools/session_logs/hooks.py`
- `tools/session_logs/limited_approval.py`
- `tools/session_logs/limited_deployment.py`
- `tools/session_logs/native_evidence.py`
- `tools/session_logs/native_validation.py`
- `tools/session_logs/portable_config.py`
- `tools/session_logs/schedule_backends.py`
- `tools/session_logs/scheduler.py`
- `tools/session_logs/systemd_scheduler.py`
- `tools/session_logs/windows_scheduler.py`

### G28 Session記録の継続回収・移行・私有領域検証

- `tools/session_logs/eventual_preservation.py`
- `tools/session_logs/preservation_migration.py`
- `tools/session_logs/private_validation.py`

### G29 第0段Session記録完了関門

- `tools/session_logs/stage_gate.py`

### G30 最小Task Contract実行基盤

- `tools/task_contract/__init__.py`
- `tools/task_contract/contract.py`
- `tools/task_contract/definition_challenge.py`
- `tools/task_contract/execution.py`
- `tools/task_contract/identity.py`
