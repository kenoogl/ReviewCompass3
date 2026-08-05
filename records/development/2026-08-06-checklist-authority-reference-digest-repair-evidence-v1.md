# 初期開発チェックリストのauthority参照Digest修復Evidence v1

- 対象file：`docs/development/2026-08-03-initial-development-checklist.md`のfront matter
- 指示：Humanの指示「5番は修復」（2026-08-06、開発継続引き継ぎ後の照合報告§5に対する回答）
- 開始基準commit：`e97060a21fd17defa7b258609ca60638e5389d3c`
- 変更種別：参照Digestの訂正のみ。意味変更、順序変更、scope変更、checkbox変更を含まない。

## 0. 何を直したのか（範囲の明示）

**直したのは、チェックリストが「現在有効な上位文書」として指し示すDigestの値だけである。**
チェックリスト本文、各節のcheckbox、Evidence、進行順序、完了判断は一切変更していない。
上位文書であるCurrent PlanとDevelopment Policyの内容も変更していない。

## 1. 事象

front matterの2箇所が、実fileのbytesから計算したSHA-256と食い違っていた。

| 欄 | path | 記載値（旧） | 実値 |
| --- | --- | --- | --- |
| `authority_order[2].sha256` | `docs/current/reviewcompass3-plan-current.md` | `0ab828f4…9bf2694` | `1a735976…d0962f` |
| `operational_policy.sha256` | `docs/development/2026-08-02-development-policy.md` | `9078276d…f739a0` | `0d348803…f8ac18` |

同じfront matter内の他6件（Intent、統合用語集、policy v5 record、design memo 3件）は一致していた。

## 2. 原因

この欄は「活性化時点の固定snapshot」ではなく「現在有効な上位文書」を指す欄であり、
2026-08-04のcommit `c475becb3ebf3f3cb9e362d64bab79606ed3719d`で一度更新されている。
その後、上位文書だけが改定され、この欄が追随しなかった。

- Current Planは`c475bec`以降に7 commitで改定され、最終変更は`32d33fc`である。
- Development Policyは`c475bec`以降に3 commitで改定され、最終変更は`2cc4b80`である。

すなわち、上位文書を改定した各作業単位が、参照側であるチェックリストのfront matterを
stale閉包の対象に含めていなかった。表示上の不整合であり、完了判断そのものの誤りではない。

## 3. 修復内容

上記2行を、実fileのbytesから機械計算した値へ置換した。追加・削除した行はない。

修復後のチェックリスト自身のSHA-256は
`54d3b9f4eee5889b3b4d85e94c665eba0c643996ddf74f45f6a514389af00d02`である。

## 4. 機械照合

front matterの全参照について、記載値と実fileのbytesから再計算した値を比較した。

| 項目 | 結果 |
| --- | --- |
| 参照件数 | 8件 |
| 一致 | 8件 |
| 不一致・欠落 | 0件 |

再現command（一時検査scriptによる決定的比較。front matterを解析し、全`path`と`sha256`の組を
実fileのbytesから再計算した値と突き合わせ、不一致が1件でもあればexit code 1を返す）：

```text
.venv/bin/python3 <一時検査script> .
→ {"reference_count": 8, "mismatch_count": 0}、exit code 0
```

## 5. 下流参照への影響

チェックリスト自身のDigestが変わるため、これを記録している参照を確認した。

| 参照元 | 扱い |
| --- | --- |
| `TODO_NEXT_SESSION.md`の最新authority／Evidence欄 | 同じcommit内で新しい値へ更新した |
| `records/session-handoffs/2026-08-06-codex-to-claude-development-continuation.md` | 引き継ぎ時点の不変recordのため変更しない。当該commit時点の値として正しい |

`tests/test_task_contract_source_pin.py`の`PINNED_PLAN_SHA`と
`tests/test_task_contract_source_resolution.py`の`ACCEPTED_POLICY_SHA`は、
特定commitへ固定したTask Contractの入力pinであり、「現在有効な上位文書」を指す欄ではない。
本修復の対象外であり、変更していない。

## 6. Test

| 対象 | 結果 |
| --- | --- |
| `python3 tools/development/todo_handoff.py TODO_NEXT_SESSION.md` | `{"findings": [], "status": "passed"}` |
| 公式venv runnerの全Test | `1007 passed`、exit 0、Python 3.9.6、pytest 8.4.2、fallback `false` |
| `git diff --check` | 合格 |

## 7. 変更していない範囲

- チェックリスト本文、checkbox、各節のEvidence、進行順序、Work境界。
- Current Plan、Development Policy、Intent、統合用語集、Requirements、Task Contract、Test、実装code。
- 引き継ぎメモを含む既存の不変record。上書き、削除、無効化、stale化はしていない。
- Work 6A、Current Work Projection正式写像、新schemaは開始していない。
- push、PR、CI、外部送信は行っていない。

## 8. 機械処理に関する報告

front matterの参照Digestを現行fileへ突き合わせる**恒久的な検査器は存在しない**。
今回は一時検査scriptで決定的に照合したが、同種のdriftは`c475bec`以降で再発している。
恒久検査器の追加は本修復の承認範囲外であるため実装せず、機械化候補としてHumanへ報告する。
