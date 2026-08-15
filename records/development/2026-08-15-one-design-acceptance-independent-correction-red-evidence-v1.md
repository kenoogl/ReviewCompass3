# One-design acceptance independent correction RED evidence v1

## Purpose

独立完了確認v1が示した形式検査1系統3変種を、設計側・受入条件側、直接核・正式入口へ固定し、修正前の誤受理と誤停止を再現する。

## Fixed inputs

- Independent review: `records/development/2026-08-15-one-design-acceptance-independent-completion-review-v1.md`
- Review SHA-256: `4af8107d8f617f26720cf34bc6ab12167e8f73c31439ecfc7aa4f14f6ca05888`
- Reviewed commit: `fb8c0b6443a0491ea635dbc9e8c3981e2df6fee8`
- Existing test baseline: commit `1a86295`
- Test target: `tests/test_one_design_acceptance.py`

## Execution

【実測】次を単独実行した。

```text
.venv/bin/python3 -m pytest -q --tb=short tests/test_one_design_acceptance.py -k 'non_integer_schema_versions or cannot_be_normalized or classifies_noncanonical'
```

- exit code: `1`
- result: `14 failed, 2 passed, 91 deselected in 0.15s`

## Failure classification

【実測】

1. `schema_version: true`と`1.0`は、設計・受入条件の4例すべてで停止せず、`DID NOT RAISE`となった。
2. 5,000桁整数は、設計・受入条件の直接核2例で生`ValueError`となった。
3. 単独surrogateの文字列・文字列配列は、設計・受入条件の直接核4例で生`UnicodeEncodeError`となった。
4. 巨大整数・単独surrogateの正式入口4例は、期待する終了コード2でなく4となった。
5. `schema_version: false`の設計・受入条件2例は既に`invalid_schema`で停止し、成功した。

## Fixed expectations

【記録】全追加例の期待は、直接核で`DesignAcceptanceStop(reason=invalid_schema, source=design|acceptance)`、正式入口で終了コード2と同じsourceの固定停止JSONである。既存91件の期待値、契約schema、停止語彙、変更pathは変更していない。

## Judgment

【判断】限定修正のREDは成立した。失敗14件は独立レビューの3変種に限られ、設計側・受入条件側、scalar・array、直接核・正式入口へ接続された。

## Next

試験を変更せず、形式版を厳密な整数型1だけにし、JSON復号の整数桁数超過と正準UTF-8化不能文字を対象sourceの`invalid_schema`へ変換する。
