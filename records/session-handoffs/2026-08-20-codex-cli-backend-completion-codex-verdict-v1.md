# Reviewer起動アダプタ 判定record（機械転記） contract-015-e2e-codex

- Reviewer：provider `openai`／model `gpt-5.6-sol`（アダプタ照合済み）
- 独立性：Tier 1（アダプタ判定。契約010 §5.1-4）
- 起動方式：headless機械起動（backend `codex-cli`）
- 依頼record：`records/session-handoffs/2026-08-20-codex-cli-backend-completion-codex-request-v1.md`（SHA-256 `f644057534d8c5e632c920aeb440d502c2a856f3eb8803d288db42e54386bb01`）
- 未加工出力：保存先種別 `private_root_immutable_store`、SHA-256 `7d7ca502b1f19305c0a1e1addf4234a1de4ed4f5c341277b5d893dee86f49dda`、参照権限：repo外私有領域（利用者とClaude）
- 実行識別子：`contract-015-e2e-codex`
- 判定：**rejected**
- 判定要旨：依頼recordと固定11 fileのSHA-256は全件一致し、実装の登録簿深化、訂正後のcodex固定引数、read-only sandbox、stdin遮断、rollout model照合、判定抽出は契約形と概ね整合した。しかし、GREEN合否が禁止されたセミコロン連結による終了コード射影で記録され、RED数値も機械生成fileから第三者照合できないため、RED→GREEN手続きと受入試験合格の証拠が成立していない。採用・受入は停止すべきである。
- 鮮度（Reviewer申告）：match（expected `f644057534d8c5e632c920aeb440d502c2a856f3eb8803d288db42e54386bb01`／observed `f644057534d8c5e632c920aeb440d502c2a856f3eb8803d288db42e54386bb01`）
- 未検査：sandboxと依頼の書込み禁止条件によりpytestを再実行しておらず、GREENは固定測定recordと試験コードの静的照合に限定した、repository外のCODEX_HOME rolloutおよびprivate raw保存領域は読取り禁止のため、今回の実E2Eにおける実観測model、command_execution全件、領域外読取りの有無を直接検査していない、networkアクセス禁止のためcodex-cliの追加実起動、外部接続、認証経路の動的再検査は実施していない

## findings

- C15-REVIEW-001（severity: high／blocking: true）：GREEN測定のtest合否はpytest単独commandの終了コードで固定されていない。4 suiteはいずれも「pytest ...; echo exit=$?」をsh経由で実行しており、測定entry自体のexitはechoの成功を示す0になる。これはrepository規律の「test・validatorの合否は単独で実行したcommandの終了コードで確認し、`;`連結の後段で判定しない」に反し、契約§9-9の単独終了コード0を受入証拠として確定できない。（根拠：`records/development/2026-08-20-contract-015-green-measurements-v1.md` §reviewer_launch試験の単独終了コード射影 22-34行、§request_builder試験の単独終了コード射影 50-62行、§G30契約操作試験の単独終了コード射影 78-90行、§RQ2装置試験の単独終了コード射影 106-118行。規律はAGENTS.md 71-72行）
- C15-REVIEW-002（severity: high／blocking: true）：RED先行の「21 failed, 70 passed」は機械生成fileに閉じておらず、実装Evidenceへの例外転記だけである。対象commit履歴でも試験と実装は同一commit bf3b69bに含まれ、指定Evidenceから第三者が実装前の失敗結果、内訳、終了コードを再照合できないため、依頼反証点3の追跡可能性を満たさない。（根拠：`records/development/2026-08-20-codex-cli-backend-implementation-evidence-v1.md` §1 12-20行および§6 60-63行。測定ブロックはGREENのみであり、RED rawまたは機械生成測定fileへの参照がない）
- C15-REVIEW-003（severity: medium／blocking: false）：openai系4種の遮断実装は共通ループにより存在するが、対象試験は4変数を列挙した後にOPENAI_API_KEYだけを設定しており、残るOPENAI_BASE_URL、OPENAI_ORGANIZATION、OPENAI_PROJECTの個別遮断を機械証明していない。実装構造上は同じ処理を通るため直ちに製品欠陥とは判定しないが、「4種が存在時に起動前停止」の試験証拠は不完全である。（根拠：`tests/test_reviewer_launch.py` test_codex_forbidden_auth_environment_stops 1678-1706行。実装側はtools/reviewer_launch/core.py 123-129行、436-444行、865-870行）

## 判定JSON（verbatim）

```json
{
  "findings": [
    {
      "blocking": true,
      "claim": "GREEN測定のtest合否はpytest単独commandの終了コードで固定されていない。4 suiteはいずれも「pytest ...; echo exit=$?」をsh経由で実行しており、測定entry自体のexitはechoの成功を示す0になる。これはrepository規律の「test・validatorの合否は単独で実行したcommandの終了コードで確認し、`;`連結の後段で判定しない」に反し、契約§9-9の単独終了コード0を受入証拠として確定できない。",
      "evidence_location": "§reviewer_launch試験の単独終了コード射影 22-34行、§request_builder試験の単独終了コード射影 50-62行、§G30契約操作試験の単独終了コード射影 78-90行、§RQ2装置試験の単独終了コード射影 106-118行。規律はAGENTS.md 71-72行",
      "evidence_path": "records/development/2026-08-20-contract-015-green-measurements-v1.md",
      "identifier": "C15-REVIEW-001",
      "severity": "high"
    },
    {
      "blocking": true,
      "claim": "RED先行の「21 failed, 70 passed」は機械生成fileに閉じておらず、実装Evidenceへの例外転記だけである。対象commit履歴でも試験と実装は同一commit bf3b69bに含まれ、指定Evidenceから第三者が実装前の失敗結果、内訳、終了コードを再照合できないため、依頼反証点3の追跡可能性を満たさない。",
      "evidence_location": "§1 12-20行および§6 60-63行。測定ブロックはGREENのみであり、RED rawまたは機械生成測定fileへの参照がない",
      "evidence_path": "records/development/2026-08-20-codex-cli-backend-implementation-evidence-v1.md",
      "identifier": "C15-REVIEW-002",
      "severity": "high"
    },
    {
      "blocking": false,
      "claim": "openai系4種の遮断実装は共通ループにより存在するが、対象試験は4変数を列挙した後にOPENAI_API_KEYだけを設定しており、残るOPENAI_BASE_URL、OPENAI_ORGANIZATION、OPENAI_PROJECTの個別遮断を機械証明していない。実装構造上は同じ処理を通るため直ちに製品欠陥とは判定しないが、「4種が存在時に起動前停止」の試験証拠は不完全である。",
      "evidence_location": "test_codex_forbidden_auth_environment_stops 1678-1706行。実装側はtools/reviewer_launch/core.py 123-129行、436-444行、865-870行",
      "evidence_path": "tests/test_reviewer_launch.py",
      "identifier": "C15-REVIEW-003",
      "severity": "medium"
    }
  ],
  "freshness": {
    "expected": "f644057534d8c5e632c920aeb440d502c2a856f3eb8803d288db42e54386bb01",
    "observed": "f644057534d8c5e632c920aeb440d502c2a856f3eb8803d288db42e54386bb01",
    "result": "match"
  },
  "reviewer": {
    "model": "gpt-5.6-sol",
    "provider": "openai"
  },
  "summary": "依頼recordと固定11 fileのSHA-256は全件一致し、実装の登録簿深化、訂正後のcodex固定引数、read-only sandbox、stdin遮断、rollout model照合、判定抽出は契約形と概ね整合した。しかし、GREEN合否が禁止されたセミコロン連結による終了コード射影で記録され、RED数値も機械生成fileから第三者照合できないため、RED→GREEN手続きと受入試験合格の証拠が成立していない。採用・受入は停止すべきである。",
  "target": {
    "commit": "ee41cddce4455cbe8654f8e19ebbe06d2c03a14c",
    "path": "records/session-handoffs/2026-08-20-codex-cli-backend-completion-codex-request-v1.md"
  },
  "unexamined": [
    "sandboxと依頼の書込み禁止条件によりpytestを再実行しておらず、GREENは固定測定recordと試験コードの静的照合に限定した",
    "repository外のCODEX_HOME rolloutおよびprivate raw保存領域は読取り禁止のため、今回の実E2Eにおける実観測model、command_execution全件、領域外読取りの有無を直接検査していない",
    "networkアクセス禁止のためcodex-cliの追加実起動、外部接続、認証経路の動的再検査は実施していない"
  ],
  "verdict": "rejected"
}
```
