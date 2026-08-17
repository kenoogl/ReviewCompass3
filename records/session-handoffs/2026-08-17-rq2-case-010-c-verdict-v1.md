# Reviewer起動アダプタ 判定record（機械転記） rq2b2-case-010-c

- Reviewer：provider `google`／model `gemini-3.1-pro-high`（アダプタ照合済み）
- 独立性：Tier 1（アダプタ判定。契約010 §5.1-4）
- 起動方式：headless機械起動（backend `antigravity-cli`）
- 依頼record：`records/session-handoffs/2026-08-17-rq2-case-010-c-request-v1.md`（SHA-256 `987e99d18e726a319d16e534752066d88c375d4b9bce7e99bf0ea7ba28f88d25`）
- 未加工出力：保存先種別 `private_root_immutable_store`、SHA-256 `d5d0e33b8e9eab1a05039393384ab39c5f47faae59ccc88fa88ac95ff4c357a7`、参照権限：repo外私有領域（利用者とClaude）
- 実行識別子：`rq2b2-case-010-c`
- 判定：**rejected**
- 判定要旨：対象materialの記述内容を検査した結果、2点の内部矛盾（blocking）を発見したためrejectedと判定しました。1点目は、本作業票を「軽量作業票」とし新契約を立てないと宣言しているにもかかわらず、手順の第1歩で重い「作業別計画（schema 2）」の作成を要求している点です。2点目は、受入条件4で「実機確認1回」を掲げつつ「試験で代替する」としており、実機確認が受入条件として必要なのか除外されるのか自己矛盾しています。
- 鮮度（Reviewer申告）：not_computable（expected `987e99d18e726a319d16e534752066d88c375d4b9bce7e99bf0ea7ba28f88d25`／observed ``）。理由：読み取り専用環境のため、sha256sum等のコマンドが実行できずdigestの機械計算が行えないため。
- 未検査：対象依頼recordおよび対象materialのSHA-256ダイジェストの再計算と照合（環境制約のため）、外部計画書（評価データ取得計画v1等）との整合性確認（対象material以外の参照が範囲外であるため）

## findings

- FINDING-01（severity: high／blocking: true）：対象materialが「軽量作業票」であり「新契約は立てない」と宣言しているにも関わらず、着手後の手順1で「作業別計画（schema 2）」の作成と承認を要求しており、宣言と手順が内部矛盾しています。（根拠：`docs/evaluation/rq2-cases/case-010/launch-metrics-work-ticket.md` 10行目、38行目 vs 53行目）
- FINDING-02（severity: medium／blocking: true）：受入条件4の表題が「実機確認1回」であるにも関わらず、内容は「本作業票では試験（模擬実行）で代替する」となっており、実機確認が必要なのかテストで代替するのか自己矛盾しています（代替する場合、受入条件2・3と重複）。（根拠：`docs/evaluation/rq2-cases/case-010/launch-metrics-work-ticket.md` 46行目〜47行目）

## 判定JSON（verbatim）

```json
{
  "findings": [
    {
      "blocking": true,
      "claim": "対象materialが「軽量作業票」であり「新契約は立てない」と宣言しているにも関わらず、着手後の手順1で「作業別計画（schema 2）」の作成と承認を要求しており、宣言と手順が内部矛盾しています。",
      "evidence_location": "10行目、38行目 vs 53行目",
      "evidence_path": "docs/evaluation/rq2-cases/case-010/launch-metrics-work-ticket.md",
      "identifier": "FINDING-01",
      "severity": "high"
    },
    {
      "blocking": true,
      "claim": "受入条件4の表題が「実機確認1回」であるにも関わらず、内容は「本作業票では試験（模擬実行）で代替する」となっており、実機確認が必要なのかテストで代替するのか自己矛盾しています（代替する場合、受入条件2・3と重複）。",
      "evidence_location": "46行目〜47行目",
      "evidence_path": "docs/evaluation/rq2-cases/case-010/launch-metrics-work-ticket.md",
      "identifier": "FINDING-02",
      "severity": "medium"
    }
  ],
  "freshness": {
    "expected": "987e99d18e726a319d16e534752066d88c375d4b9bce7e99bf0ea7ba28f88d25",
    "observed": "",
    "reason": "読み取り専用環境のため、sha256sum等のコマンドが実行できずdigestの機械計算が行えないため。",
    "result": "not_computable"
  },
  "reviewer": {
    "model": "Gemini 3.1 Pro (High)",
    "provider": "Google"
  },
  "summary": "対象materialの記述内容を検査した結果、2点の内部矛盾（blocking）を発見したためrejectedと判定しました。1点目は、本作業票を「軽量作業票」とし新契約を立てないと宣言しているにもかかわらず、手順の第1歩で重い「作業別計画（schema 2）」の作成を要求している点です。2点目は、受入条件4で「実機確認1回」を掲げつつ「試験で代替する」としており、実機確認が受入条件として必要なのか除外されるのか自己矛盾しています。",
  "target": {
    "commit": "HEAD",
    "path": "records/session-handoffs/2026-08-17-rq2-case-010-c-request-v1.md"
  },
  "unexamined": [
    "対象依頼recordおよび対象materialのSHA-256ダイジェストの再計算と照合（環境制約のため）",
    "外部計画書（評価データ取得計画v1等）との整合性確認（対象material以外の参照が範囲外であるため）"
  ],
  "verdict": "rejected"
}
```
