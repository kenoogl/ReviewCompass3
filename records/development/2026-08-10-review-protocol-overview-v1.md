# レビュープロトコル全体像と実現状況

- 作成日：2026-08-10
- 作成者：Claude（Pilot）
- 位置づけ：**設計正本の要約と、現行codex CLI運用との差分の記録**。
  正本は`records/design/stage-five-design.json`（SHA-256
  `29ed55927061c9991ec7bbad3f03c929214527b653979d3453c9bbd7eb499c4f`）であり、
  本recordは正本を置き換えない。差分の把握を目的とする。
- 裁定済み部分：第3層のみ
  （`records/development/2026-08-10-review-material-mode-decision-v1.md`）。

## 第1層：役割の三分割（全9設計に共通）

正本の各設計は`machine_responsibilities`・`llm_responsibilities`・
`human_responsibilities`・`failure_strategy`を持つ。

| 担当 | 役割 |
| --- | --- |
| 機械 | 列挙、Digest、Schema、参照、被覆、状態遷移、保存を**検証する** |
| LLM | 文章読解、意味的関連性、所見、解釈、改善仮説を**提案する** |
| Human | 外部送信、意味競合、Finding、方針変更、段完了を**判断する** |
| 失敗時 | 不足を保持し**未確定のまま停止**（成功へ昇格しない） |

鉄則：**Human判断は機械関門を免除しない**。両方要るものは`hybrid`として両方検証する。

## 第2層：レビュー1回の8段階と実現状況

`DES-REVIEW-CONTEXT` → `DES-HARNESSED-EXECUTION` → `DES-REVIEW-TRIAGE`の順序。

| 段 | 内容 | 実装 | 運用への接続 |
| --- | --- | --- | --- |
| 1 | 材料の構成（対象・材料束・範囲・identityを版付き固定） | `material_bundle` | **接続済**（範囲固定文書として） |
| 2 | 閉包の判定（必要材料の充足。不足なら`blocked`） | `evidence_closure` | **未接続** |
| 3 | 封緘（承認済み材料だけを閉じ込めDigest付与） | `closed_payload` | **CLIでは不可**（第3層で代替） |
| 4 | 契約（固定promptと固定出力schema） | `review_contract` | **未接続**（promptのみ定型化） |
| 5 | 実行（複数担当へ送信。応答は解析前に不変保存） | `review_execution`・`raw_review_store` | **部分接続**（codex exec起動。起動記録は残る） |
| 6 | 厳格解析（schema準拠だけを受理） | `review_response_parser` | **未接続**（自由文Markdownを受理） |
| 7 | 統合（担当別・重複・競合を分離。競合は保持） | `review_triage` | **未使用**（単一担当のため） |
| 8 | 確定（来歴検査後にHumanが採用・拒否・保留） | — | **接続済**（Human承認文言） |

失敗戦略（`DES-REVIEW-TRIAGE`）：競合または来歴不一致なら**全候補を保持して確定を停止**する。
多数決または単一LLMによる自動採否は却下済みの代替案である。

### 実装の存在確認（機械出力）

```text
review_contract              実装:有 test:1件
review_response_parser       実装:有 test:1件
raw_review_store             実装:有 test:1件
evidence_closure             実装:有 test:1件
closed_payload               実装:有 test:1件
review_execution             実装:有 test:1件
review_triage                実装:有 test:1件
bootstrap/review系のtest総数: 22
```

`tools/bootstrap/review_pipeline.py`が段1〜8を統括する。**呼び出しているのは
自身のtestのみ**で、運用経路からの呼び出しは無い。

**すなわち、部品と統括は実装・test済みであり、欠けているのは運用への接続だけである。**

## 第3層：CLI運用での封緘の代替（裁定済み）

| 正本の要求 | CLI方式の代替 |
| --- | --- |
| 入力の封緘 | **発見力モード**（封緘せず、起動記録で事後照合） |
| 送信identityの固定 | 起動記録のsession IDと実行command全件 |
| 根拠の証明 | 抽出できたpath件数／抽出不能件数を判定recordへ記録 |
| 材料の出自 | 機械導出か判断選定かを範囲固定へ記録 |

## 第4層：材料の2区分

- **機械導出**（例：`find tools -name "*.py"` → 133件）：選び忘れが起きない。発見力は不要。
- **判断選定**（例：固定入力7件を手で選定）：漏れが原理的にありうる。発見力が必要。
- **混在型**（棚卸し：列挙は機械で漏れ0、分類は判断で9件漏れ）：判断部分に合わせる。

## 第5層：レビューの外側

| 設計 | 役割 |
| --- | --- |
| `DES-SEMANTIC-TRACE` | TaskからFindingまでの来歴を検証。**verdictだけ返し状態を変えない** |
| `DES-WORKFLOW-CONTROL` | 作業単位と段階の状態機械。**Run開始・完了とfile書込みが関門** |
| `DES-SELF-IMPROVEMENT` | 実測をledgerへ保存。改善は**固定比較とHuman承認後だけ**反映 |

`DES-SELF-IMPROVEMENT`は本日の教訓と直結する。方針の改善は「レビューで穴を潰す」のでは
なく「**実測をledgerへ貯め、固定比較し、Humanが承認する**」。2026-08-10にPilotが行った
「方針を書いてはレビューに掛ける」反復は、この設計に反していた。

## 本recordが決めていないこと

未接続段（2・4・6・7）の実現方法と着手順序。別途Humanが裁定する。
