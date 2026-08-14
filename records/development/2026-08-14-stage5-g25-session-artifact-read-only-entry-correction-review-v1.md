# 第5段 G25 Session記録 読取り専用入口 限定修正レビュー v1

- レビュー日：2026-08-14
- 対象commit：`44cc5ea7b19e890218d67d23064af4bd5c5ea3fe`
- 限定修正Evidence：
  `records/development/2026-08-14-stage5-g25-session-artifact-read-only-entry-correction-evidence-v1.md`
- Evidence SHA-256：`2d297c90834d6c33c40cadcc4bcf3c53a29c57a939dea539f526913ba34126b5`
- 先行独立レビューSHA-256：`798761ac4a77ff03c54327c0315f4687e8b149d287a0d6d78c6439f45609e5d7`
- 判定：`verified`

## 1. 判定

【判断】**verified**。先行独立レビューの止める指摘二件は、指定された最小範囲で解消した。

1. `:`直後と`file://`に含まれる絶対pathは、成功成果を返さず固定理由
   `absolute_path_remaining`、`status: stopped`、終了コード4となる。
2. 新入口の表示は、Human受入前の状態を示す
   `provisional / non-normative / promotion_required: true`へ戻った。

本判定は二指摘の限定修正だけを確認する。Human受入、正式・安定表示への昇格、第5段完了は代行しない。

## 2. 固定対象と修正範囲

【実測】対象commitと先行RED・GREEN commitは実在し、EvidenceのSHA-256は申告値と一致した。

先行レビューcommit`f6cf47b`から対象commitまでの成果物変更は、次の二fileだけだった。

- `tests/test_session_log_read_only_entry.py`
  - 既存のparameter付き停止試験へ二例を追加
- `tools/session_logs/read_only_entry.py`
  - 既存の絶対path検査を限定訂正
  - 先頭の状態表示三項目を訂正

【実測】このほかに追加されたのは限定修正Evidence一件だけである。`pyproject.toml`、G25既存10 path、
G26、G30、他142 path、契約、上流候補、設定、TODOは変更されていない。

【実測】限定GREEN時と現在の内容識別値はEvidence記載と一致した。

| path | SHA-256 |
| --- | --- |
| `tools/session_logs/read_only_entry.py` | `8d03610aaa677b9e4d6d4271fbb698ddd81928db95a72b14e7eb4e3588592c8a` |
| `tests/test_session_log_read_only_entry.py` | `8152c5bb82ca235d723aac69fb519b2b6284a3f92cf6e2972328b4f479e5e053` |

## 3. 絶対path二例の修正

【実測】限定RED commit`208276c`をリポジトリ外へ展開し、現在の作業ツリーを読み込まない条件で対象試験を
実行した。既存10件は成功し、次の追加二例だけが終了コード0となって失敗した。試験全体の終了コードは1だった。

- `absolute path:/Users/example/project`
- `file:///Users/example/project`

【実測】限定GREEN後の現在状態では、対象試験12件が成功し、終了コード0だった。追加二例はいずれも、
成功時の転写・要約を返さず、次の固定結果と終了コード4を確認する試験である。

```json
{"error":"absolute_path_remaining","external_send_approved":false,"status":"stopped"}
```

【実測】従来の`work=/Users/example/project`と、高い乱雑性の未登録値を含む既存例も同じ対象試験内で成功している。
したがって、追加二例を閉じる際に既存の停止境界は壊れていない。

【実測】限定RED、限定GREEN、対象commitの試験fileのGit物体識別値はすべて
`37a0a957968296afa7ab700d8174fe8b852bb004`で一致した。GREEN時に試験を変更していない。

## 4. 状態表示の修正

【実測】新入口先頭は次の表示になった。

- `lifecycle: provisional`
- `normative_status: non-normative`
- `promotion_required: true`

【判断】これは、実装開始は承認済みだが、Human受入と正式・安定表示への昇格は未実施という現在状態と一致する。
先行指摘の過大表示は解消した。

## 5. 試験と状態の結び付き

【実測】現在状態で限定範囲を独立再実行した。

| 確認 | 結果 | 終了コード |
| --- | --- | --- |
| 新入口の対象試験 | 12件成功 | 0 |
| 対象12件＋G25直接関連55件 | 67件成功 | 0 |

【実測】正規全試験の受領記録はリポジトリ外に現存し、SHA-256は
`706ea8c6e8a8330d0a724d42cf0b7129cc875dee50cdb2c1538a5f3e72b4f3b9`でEvidence記載と一致した。
受領記録は1,740件成功、失敗0、error 0、skip 0、終了コード0、Python 3.13.14、pytest 8.4.2、
runner版2、代替実行なしを記録していた。

【実測】受領記録と現在状態の間で増えた限定修正Evidence一件だけを状態計算から除き、runnerと同じ規則で
状態識別値を再計算した。結果は
`4251a9480253624dadf3d763254ae9096d56b54fe875e8923927bc793d7df6ff`で受領記録と一致した。
したがって、1,740件成功は限定GREEN状態へ結び付く。

## 6. 止める指摘と報告不一致

- 止める指摘：**0件**
- 報告不一致：**0件**

【判断】先行実装Evidenceの一般化と完了候補表示は、先行レビューの記録どおり履歴上staleのままである。
今回の限定修正Evidenceと本レビューが、その二指摘の解消を示す現在の根拠になる。

## 7. 試した反証

1. **追加二例だけを試験へ足し、実装は見逃したまま**：限定REDで二例だけが失敗し、現在状態では両方が
   固定停止結果になった。反証不成立。
2. **二例を閉じるため既存例を壊した**：対象12件が全件成功し、既存10件も維持された。反証不成立。
3. **GREEN時に試験を弱めた**：限定REDから対象commitまで試験fileのGit物体識別値が同一だった。
   反証不成立。
4. **状態表示が依然として正式・安定済み**：入口先頭三項目を直接確認し、慎重側の表示と一致した。
   反証不成立。
5. **修正範囲がG25または配布設定へ広がった**：全path差分を確認し、成果物変更は入口と既存試験の二fileだけ
   だった。反証不成立。
6. **全試験受領記録が別状態の結果**：Evidenceだけを除いた状態識別値を独立再計算し一致した。
   反証不成立。

## 8. 未実施

【未実施】既に確認済みの配布物、三形式、禁止副作用、G25到達境界は再審査していない。成果物コード、試験、
設定、`pyproject.toml`、TODO、Evidence、契約、G25既存10 path、G26、G30、他142 path、上流候補、Issueは
変更していない。新しい検査器、台帳、関門、試験fileは作っていない。Human受入、正式・安定表示への昇格、
第5段完了、外部送信、push、tag、amend、rebase、reset、履歴書換えは扱っていない。
