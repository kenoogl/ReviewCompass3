# レビュー依頼 v2：group B — F-C1・F-C2修正後の再レビュー

- 作成日：2026-08-10
- Pilot：Claude／Reviewer：Codex／Closer：Codex
- collaboration mode：`role_neutral_pilot_review`、risk：`high`
- 先行依頼書：v1（完了Claimは完了レビューv1によりstale。変更せず保持）

## 1. 経緯とHuman承認

完了レビューv1（`records/session-handoffs/2026-08-10-codex-review-result-official-oracle-fix-v1.md`、
SHA-256 `fd9023716741502332e945d25df585bf97dd009a758b8c22ceff3431bde80195`、
判定`report_execution_mismatch`・blocking 2件）に対し、Humanが
2026-08-10「F-C1とF-C2の修正を承認する」と裁定した。scope v3（`6ce4d03`）で範囲を固定した。

## 2. commit列（review request v1以後）

| SHA | 役割 | 内容 |
| --- | --- | --- |
| `c5d7db3` | Pilot | review request v1（先行） |
| `9c9d9a7` | Reviewer | 完了レビューv1 result record |
| `6ce4d03` | Pilot | SCOPE v3：F-C2の是正（変更可能pathの追加）とF-C1の修正範囲 |
| `b44e1a6` | Pilot | 修正RED：一時repositoryでの隠蔽2態様＋nested rootの反証。実装前は隠蔽2態様が失敗 |
| `dddaf9b` | Pilot | 修正RED（契約更新）：期待call列へ`git ls-files -v`を追加。修正前実装で失敗を機械確認 |
| `33dfa38` | Pilot | 修正GREEN：`work_unit_transition.py`＋Evidence §8追記＋receipt v2 |

本依頼書のcommit SHAは自己参照のため記載せず、Reviewerがgitから特定する。

## 3. Claim（修正分）

- **F-C2**：scope v3 §2で契約recordを変更可能pathへ追記し、変更範囲を`sha256`値
  1箇所に限定して明記した。過去commitの書き換えはしていない。
- **F-C1**：`git ls-files -v`で隠蔽指定（`skip-worktree`・`assume-unchanged`）された
  追跡fileを列挙し、各fileについて`git rev-parse HEAD:<path>`と
  `git hash-object -- <path>`のblob idを**索引を経由せず**比較する。差があれば
  `blocked`。取得不能はfail-closedで差ありとみなす。
- **限界の明示**：W2型（別の正当なrepositoryをproject_rootへ渡す）は、利用者が対象を
  選ぶ自由と区別できないためtool単体では判定しない。要求rootとGitが答えるrootの
  食い違いは従来どおり拒否する（Evidence §8.2）。
- **反証の実行場所**：すべて使い捨ての一時repository。実repositoryの索引・作業treeには
  触れていない。
- **結果**：`pytest tests/test_work_unit_transition.py` 13 passed、
  公式全Test **1469 passed**・status `passed`、worktree clean。

## 4. 成果物SHA-256（修正後）

| file | SHA-256 |
| --- | --- |
| `tools/development/work_unit_transition.py` | `93e005fe299bd0e33d0ada6b92ad1732d05194ebe4d92e100e5111bd659b33b6` |
| `tests/test_work_unit_transition.py` | `f811eb9caa276f7b88e3ae237cec5c745cf2a85b93bf27eed12aacb33c01b40d` |
| Evidence（§8追記後） | `f38e9e59396954e75b73768e7328e355aa2ad93c38fcb841f36998fd200e1444` |
| 公式receipt（v2） | `49785d1bf32b458f9f673f91dee0c03344e0e95c26871f06e88847542e94f870` |

## 5. Reviewerへの確認観点

- **F-C1**：W1（`skip-worktree`）・追加反証（`assume-unchanged`）が
  **不成立**になること。あなた自身が一時repositoryで再現し、実repositoryを汚さないこと。
  W2型については§3の限界表明が妥当か（範囲外への拡張は求めない）。
- **F-C2**：scope v3が変更file境界を正しく閉じており、GREEN `33dfa38`と
  修正RED 2件が§4・§5の境界内であること。
- 修正RED（`dddaf9b`）の契約更新が、**修正前実装で失敗し修正後で合格**すること、
  検査性質を弱めていないこと。
- 正例：本repositoryの正常な公式runが`passed`のままで、件数が実行実績と一致すること。
- 完了レビューv1で確認済みの事項（P1〜D3の不成立、事故の痕跡なし、契約pinがv2の
  1箇所のみ）が維持されていること。
- non-blocking N-C1（receiptの`source_state_digest`がGREEN treeから再生成一致しない件）は
  本修正で扱っていない。判断はReviewerに委ねる。
