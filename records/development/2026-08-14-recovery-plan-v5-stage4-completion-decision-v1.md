# 立て直し計画v5 第4段 完了判断 v1

- 記録ID：`DEC-RECOVERY-PLAN-V5-STAGE4-COMPLETION-2026-08-14-V1`
- 判断日：2026-08-14
- 状態：`completed`
- 判断者：利用者
- 判断材料commit：`83cf15fc15a1f0cf4edd57ee360a7454d45cef91`
- コード観測commit：`66d608e5b5d605ddaf387bbd75a507ac934800c6`
- 上位計画：`docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md`
- 上位計画SHA-256：`8c814067511797e445d66779ad144f42ea0b139501ff6002a7d6c46e6706055c`

## 1. 利用者承認

【記録】利用者は、第4段の分類結果、G25の詳しい確認、最小Task Contract入力、独立完了レビューと
限定訂正レビュー、152件のうち実際に使用停止とした件数の説明を受けた後、次のとおり明示した。

> 上記5点を承認

【判断】次の五点を一つの意味的判断として採用する。

1. G25の10 pathを、第5段で再利用できる正式製品コード集合として採用する。
2. 他の142 pathは今回の正式製品コード集合へ含めない。一括削除または一括使用停止にはしない。
3. G25の読取り専用Session記録解析を、最初のTask Contract候補とする。
4. 上流候補9件は暫定のまま、既知の直接参照不一致3件も未修正の入力として第5段へ渡す。
5. 立て直し計画v5の第4段を完了し、第5段へ移る。

## 2. 正式製品コードとして採用する集合

【判断】正式製品コードとして識別する最初の集合は、意味群G25「Session記録の解析・伏字化・要約・来歴生成」
の次の10 pathである。

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

【実測】コード観測commitにおける10 pathのGit tree entry一覧SHA-256は
`f476cbf6df63bc2accfb188764b2b8216aefdb7c446572b40b56b2cbcab861e4`である。判断材料commitまで、
`tools`、`tests`、`config`、`setup.py`、`conftest.py`の差分は0件であり、この内容識別値は同じだった。

【判断】この集合を利用する製品処理は、次の一文で固定する。

> 利用者が指定した一つのローカルのセッション記録を読み取り、機微情報を除いた転写、要約、来歴の候補を
> メモリ上に生成する。

【判断】守る性質は、一つのraw fileだけを読み、三形式を識別し、伏字化した転写・要約・来歴候補を値として返し、
種別不明、読取不能、解析不能、機微情報残存、raw root外では停止することである。file書込み、network送信、
外部process、権限変更、Issue状態変更を行わない。

【実測】現在の入口は`tools.session_logs.pipeline.prepare_artifact`である。入口から到達するコードは上記10 pathに
閉じ、群外の直接読み込み先は0件だった。直接関連する14試験fileの55件は成功、終了コード0だった。

【判断】正式製品コードへの採用は、現在のコードを第5段で再利用できる資産として識別する判断である。
各moduleの`provisional`表示、将来の振る舞い変更、実行時成熟度、製品処理の完成、最初のTask Contractの承認を
代行しない。

## 3. 今回の正式製品コード集合へ含めない142 path

【判断】152件からG25の10件を除く142件は、今回の最初の正式製品コード集合へ含めない。内訳は次のとおりである。

| 用途 | path数 | 扱い |
| --- | ---: | --- |
| 製品／保留 | 61 | 後続の製品処理またはTask Contractごとに判断する |
| 開発支援 | 71 | 製品専用集合へ混ぜず、採用候補・保留・使用停止の個別分類に従う |
| 共有 | 10 | 製品専用へ取り込まず、共有として維持する |
| 合計 | 142 | 一括削除・一括使用停止はしない |

【判断】「今回の集合へ含めない」と「使用停止」を混同しない。全152件の今後の扱いは、採用候補34、保留106、
使用停止12、履歴のみ0である。実際に使用停止として維持する12件はG07の3件、G14の8件、G17の1件である。
他の130件は、必要な用途で維持するか、後続作業ごとに判断する。

## 4. 最初のTask Contract候補と最小入力

【判断】第5段で最初にTask Contract案を作る対象は、G25の読取り専用Session記録解析とする。

【記録】既存のTask Contract構想から選んだ最小入力は、Identity、Responsibility、Boundary、Preconditions、
Context Obligations、Allowed Capabilities、Expected Outputs、Acceptance Criteria、Provenance Obligations、
Escalation Policy、版付きdependencyの11項目である。各項目のG25への対応と第5段で確定する値は、次のEvidence
§8.4に固定されている。

- `records/development/2026-08-14-stage4-product-code-and-task-contract-input-inventory-evidence-v1.md`
  - SHA-256：`c55367fc6b8f72f7041612cedc11d609b359909156f619fcb72e6d72bd33e72a`

【判断】11項目で最初の契約案を作成できる。未完成のG30、契約生成器、状態機械、実行許可機構を必須依存にしない。
第5段では契約案を作り、独立した定義挑戦を行い、利用者が契約の意味と実装開始を別に判断する。

## 5. 上流候補と既知不一致

【実測】製品上流候補9件はすべて`provisional`である。統合Intent、統合計画、統合用語集の直接参照47件のうち、
44件は現在値と一致し、3件は既知の不一致だった。独立した正式Feature PolicyとArchitecture Policyは存在しない。

【判断】上流候補9件を、第5段の契約案を作るための暫定入力として維持する。本Decisionだけで正式要求、Feature、
Architecture Policyへ昇格しない。3件の不一致も自動修正せず、契約の定義挑戦で関連する場合に競合入力として扱う。

## 6. 独立レビューと限定訂正

【記録】最初の独立完了レビューは、分類、G25の10件、55試験、G26反例、上流47参照を再現した。そのうえで、
最小Task Contract入力の対応表が無いことと、G25自身が環境値を解決するという誤記を一原因として検出し、
`report_execution_mismatch`とした。

【記録】Evidence一件へ最小入力対応表を追加し、環境参照の一文だけを訂正した。変更点限定レビューは`verified`、
止める指摘0件、報告不一致0件だった。G25自身は環境値を解決せず、呼出し側から渡された規則を使う。

根拠：

- `records/development/2026-08-14-stage4-product-code-and-task-contract-input-inventory-independent-completion-review-v1.md`
  - SHA-256：`7072027956c67534af613e7fa71aa661edb93d118cf1c01d052c742606ef03bd`
- `records/development/2026-08-14-stage4-product-code-and-task-contract-input-inventory-correction-review-v1.md`
  - SHA-256：`2c5abce8085642ff02d81fef3552e154917145f581b63b64f1df81a9f4f92137`

## 7. 第4段の完了条件との対応

| 第4段の現行完了条件 | 判断 |
| --- | --- |
| ブートストラップの四領域が利用可能 | 第1段から第3段の完了判断を引き継ぎ、利用不能を示す新事実なし |
| 既存上流文書から最初のTask Contractを作成可能 | G25と最小入力11項目で可能 |
| コード候補をGit実状態から列挙 | 152 path、試験関連192 pathで完了 |
| 用途と今後の扱いを別々に分類 | 30意味群、重複0、未分類0で完了 |
| 最初の製品処理の到達範囲を説明 | G25の10 path、群外直接依存0で完了 |
| 利用先、守る性質、試験、根拠文書、再利用可否を説明 | 本Decision§2とEvidenceで完了 |
| 用途不明または未承認コードを最初の実装前提へ含めない | G25以外142 pathを最初の集合から除外して完了 |
| 正式製品コードを他コードから識別 | G25、観測commit、tree SHA、処理、性質、55試験、利用者判断で完了 |
| 採用対象と非採用対象の利用者判断 | 本Decision§1から§3で完了 |
| 軽量整理をREQ-WORKFLOW-009の実装完了と数えない | 要求候補は未採用・未実装のまま維持 |
| 独立完了レビュー | 限定訂正後`verified`で完了 |
| 段完了のHuman判断 | 本Decisionで完了 |

【判断】以上により、第4段の現行完了条件を、上流候補と正式製品コード採用の限定を含めて満たす。

## 8. 第5段への引継ぎ

【判断】次の段は、立て直し計画v5の第5段「Task Contract中心で製品本線を再開する」である。
最初の一作業は、G25の固定入力11項目からTask Contract案を作り、実装前の独立した定義挑戦を行うことである。

【判断】第5段では次を守る。

- 最初のTask Contract自体と実装開始は、利用者が別に承認する。
- G25以外の142 path、G26、G30、上流候補の正式化を暗黙の前提へ加えない。
- 契約案の作成と定義挑戦の段階では、コード・試験・設定を変更しない。
- 上流不一致3件がG25の責務または受入条件へ影響する場合だけ、競合として利用者へ戻す。
- 最初のTask Contractで定めた小さい範囲だけを、承認後にTDDで実装または接続する。

## 9. 対象Issue

【判断】`ISSUE-TEST-GROWTH-STATE-PINNING-001`は`registered / 第3段完了・条件付き再開待ち`のまま維持する。
第4段完了やG25の採用を理由に状態を変えない。状態固定試験の変更・削除、または別途承認されたWork 8測定の前に
だけ対象限定で再開する。

## 10. 未実施

【未実施】最初のTask Contractの定義・承認・実装、G25のコード・試験・設定・lifecycle表示の変更、
他142 pathの削除・統合・正式採用、上流候補9件の正式化、不一致3件の修正、G26反例の修正、G30の利用、
REQ-WORKFLOW-009の採用・実装、Issue状態変更、外部送信、push、tag、amend、rebase、reset、履歴書換えは
行っていない。
