# group A 共通正本修正 範囲レビュー結果 v2

- レビュー日：2026-08-10
- Reviewer：Codex
- collaboration mode：`role_neutral_pilot_review`
- レビュー段階：scope（実装前の範囲レビュー）
- risk：`high`（Human確定済み）
- 判定：**verified**
- Finding：blocking 0件、non-blocking 0件、defer 0件
- model来歴：`~/.codex/config.toml`の実効値 `model = "gpt-5.6-sol"`、
  `model_reasoning_effort = "high"`

## 1. 固定対象と開始状態

- 対象：
  `records/session-handoffs/2026-08-10-claude-pilot-common-guard-fix-scope-v2.md`
- 対象SHA-256：`b10f34c38b09d623bfbd37af6b19fce024a2f36b2ffbac9503d96c5d82d8d2d7`
- 対象commit：`35d2fe6a251c1fbdd6b629791d9ab17ee0013ea4`
- 対象commitの親：`867d0b17130b76b10c9a336ff8576ba2236ac53f`
- 先行scope：`35941724c8e0cc99c6974c52ccb39218199d993b`
- 先行範囲レビュー：`867d0b17130b76b10c9a336ff8576ba2236ac53f`
- base：`17c2002491bf004b741077676845de56da845fbe`
- branch：`main`
- 許可範囲：本判定record 1件の新規作成と単独commit、読取り、決定的な照合
- 禁止範囲：対象scope、code、test、既存record、config、schema、上流設計、TODOの変更、
  RED、GREEN、外部送信、push、履歴書換え

【実測】対象commitは先行範囲レビューcommitを親とし、変更pathは対象scope v2の追加1件だけだった。
レビュー開始時のworktreeはcleanだった。先行scopeと先行範囲レビューは各commitから変更されていない。

【実測】対象scopeのSHA-256を内容から再計算した。v1 §3に固定された8入力も再計算し、8／8で
記載値と一致した。対象実装3 fileの値もv1記載値と一致しており、v1から引き継ぐ固定入力はstaleに
なっていない。

【記録】依頼文とscope v2は先行Findingを`SR-CG-SCOPE-001`と呼ぶ。一方、先行レビューrecord内の
見出しは`SR-A-SCOPE-001`である。本レビューでは、記載pathと欠落内容が同一であるため、同じ1件の
Findingとして照合した。

## 2. v1 Findingの解消可否

判定：**解消**

【実測】scope v2は`tests/test_common_module_pins.py`を変更可能pathへ追加し、GREEN（実装後の
合格段階）の意味単位commitへ置いた。変更可能部分は`_PINS`の値だけであり、同testのkey構成、
検査logic、他のtest fileはGREENで変更しないと明記している。

【実測】現行の指紋固定値（pin）は5／5で対象fileのSHA-256と一致し、単独testは`5 passed`、
終了コード0だった。`tools/common/digests.py`へ改行1 byteを加えた場合のSHA-256をメモリ内で
計算する反証では、現行pinと不一致になった。共通正本2 fileが実際にこのtestの検査対象であることも
抽出結果で確認した。

【判断】任意のpin値では受入条件5の「GREEN後の実装bytesと一致」を満たせない。keyの追加・削除や
検査logicの変更も、同条件の「修正前と同一」と、変更可能部分を`_PINS`の値だけに限る境界の両方に
反する。したがって、この例外を使って振る舞いの期待を削除または緩和する経路はscope上閉じている。

【記録】scope v1 §2はHumanの承認文言「組A修正 risk highを確定、着手を承認する」を保持する。
修正順序の裁定record（commit `4bb1c9b`）は、group Aを1つの`high`修正単位とし、共通正本の修正に
Human承認を要求している。scope v2 §1はこの承認文言とcommitをpin更新の根拠として明記し、Evidenceへ
転記することも要求している。pin test自身が要求するHuman承認記録との結線はある。

【判断】共通正本のbytes変更とpin更新を同じGREEN commitへ含める判断は妥当である。pinは実装bytesから
機械的に導く派生値であり、別の振る舞い期待ではない。これをGREENから外すと、許可範囲を守った実装commitで
公式全Testが失敗する。値だけの更新を同じ意味単位に含めることで、変更範囲と公式全Test合格を両立できる。

## 3. v1とv2の一体性

【実測】v1 §1〜§5・§8・§9の原文はcommit `3594172`から変更されていない。v2は、v1 §6のcommit境界と
§7の変更可能pathを差し替え、v1 §5の1〜4を維持したまま受入条件5を追加している。

【判断】差し替え後も、mode、役割、risk、Human承認、固定入力、F-A1・F-A2の範囲、受入条件1〜4、
停止条件、Humanへの確認事項はそのまま有効である。追加した受入条件5は、変更可能pathとGREEN commitの
例外を同じ制約へ結び、v1の既存test削除・緩和禁止とRED後のtest変更にHuman承認を要する規定を弱めない。
各節は矛盾なく一体として読める。

## 4. Finding（§11）

| §11区分 | scope段階の件数 | 判定 |
| --- | ---: | --- |
| 類型1：上流authorityとの矛盾 | 0 | なし |
| 類型2：Human境界・必要な承認の欠落 | 0 | なし |
| 類型3：誤った合格を許す受入条件・検証の欠陥 | 0 | なし |
| 類型4：禁止事項違反またはscope・schema境界の破り | 0 | なし |
| non-blocking | 0 | なし |
| defer | 0 | なし |

【判断】先行レビューで挙げたpin testの欠落だけを再確認し、同じ欠陥類型の境界を照合した。
v1で挙げなかった論点の追加や、command option、関数配置、fixture構成などの実装方式への評価は行っていない。

## 5. 判定と次

判定：**verified**

【判断】`SR-CG-SCOPE-001`（先行record内の`SR-A-SCOPE-001`）は解消した。pin更新の例外は
値だけに閉じ、実装bytesとの一致、key構成と検査logicの不変、Human承認根拠、更新前後の実測を要求する。
新たなscope境界の破れ、Human境界の欠落、誤った合格を許す受入条件はない。

Human境界：維持。裁定済み手順に従い、本レビュー後の再開はHuman判断とし、v1 §8の停止条件へ
到達した場合もHumanへ戻す。

未実施：code、test、対象scope、既存record、config、schema、上流設計、TODO、checklistの変更、
RED、GREEN、完了レビュー、Closer作業、push、履歴書換え。

次：Humanがgroup AのRED開始可否を判断する。

## 6. 実行時の手戻り

【実測】最初のpin test実行はsystemの`pytest`が存在せず終了コード127、最初のメモリ内反証式は
構文誤りで終了コード1だった。期待executorをrepositoryの`.venv`へ切り替え、式を単純化して再実行し、
それぞれ終了コード0を得た。手作業で結果を補完しておらず、今後もrepositoryの`.venv`を実行入口とする。
