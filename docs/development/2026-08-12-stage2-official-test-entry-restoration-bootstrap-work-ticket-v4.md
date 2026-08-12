# 第2段 公式試験入口の正常化 軽量作業票 v4

- 作業票ID：`BTW-STAGE2-OFFICIAL-TEST-ENTRY-RESTORATION-004`
- 状態：`approved_to_implement`
- 置換対象：`BTW-STAGE2-OFFICIAL-TEST-ENTRY-RESTORATION-003`
- v3 SHA-256：`7dc25beaf1af7bb22cbb9a0f1a4401babcda53cce66d6e5c7c19793b9ec4d6b1`
- v3修正後確認：`records/development/2026-08-12-stage2-official-test-entry-restoration-scope-correction-review-v1.md`
- v3修正後確認SHA-256：`bd09762fa42fede4254cc7f34d878f6c199c2fee1e453aed54ab3f3baac6668f`
- 基準コミット：`2fbab75ef9c41b85cd66c44af4c8fb1271fa00de`
- RED commit：`354c57e1d7dd28eaa6b2e271ea3dae60ce949720`
- 危険度：`high`

## 1. 目的

v3修正後確認の残存指摘`SR-SC-001`を解消する。v3の目的と責務分担は変えず、同じ新規恒久試験の中で、
`_run_git`の直接呼出しだけでなく、別名、大域名前表、無名関数を経由した間接呼出しも拒否する。

## 2. 入力と根拠

| 入力 | SHA-256 | 用途 |
| --- | --- | --- |
| v3作業票 | `7dc25beaf1af7bb22cbb9a0f1a4401babcda53cce66d6e5c7c19793b9ec4d6b1` | 新規試験とEvidenceの責務分担 |
| v3修正後確認 | `bd09762fa42fede4254cc7f34d878f6c199c2fee1e453aed54ab3f3baac6668f` | 間接呼出し3変種の偽陰性 |
| `tests/test_pilot_collaboration.py` | `8157394b5d40222196253dba5aaf2a645282864a4860fb2a5efc108c2b2dcb22` | 追加変更する唯一のfile |
| `tools/development/pilot_collaboration.py` | `86d7c6b3604e8a61976b9e793255dee44d8578d006672271a2e901b2d81b3eb6` | 読取り専用Git呼出しの実体 |

【記録】利用者は2026-08-12、v3修正後確認の`修正要`、残る迂回3変種、新たな承認対象と三択を提示された
後、推奨案「同一file・同一新規試験へ間接呼出しの反例を加える」を`1`で承認した。

## 3. 作業範囲と対象外

変更できるのは`tests/test_pilot_collaboration.py`一件だけである。変更内容は次に限る。

1. `TRACEABILITY`の`NG-PC-007`と`ST-PC-001`から削除済み試験名を除き、既存の変更範囲試験2件を残す。
2. `OUT-PC-006`を新規`test_pilot_git_processes_are_read_only`へ対応させる。
3. 同新規試験が、現在の`_run_git`定義一件と直接呼出し3件を構文木で確認し、`ls-tree`、`show`、
   `cat-file`だけを許す。
4. 同新規試験内の一時sourceで、`push`、`commit`、`reset`、`tag`の直接呼出しと、少なくとも次の間接呼出しを
   違反として検出する。
   - `git_writer = _run_git`による別名化
   - `globals()["_run_git"]`による大域名前表からの取得
   - `_run_git`を無名関数へ渡してからの呼出し
5. `subprocess.run`が`_run_git`定義外に追加されることと、`_run_git`名が直接の呼出し先以外で参照されることを
   拒否する。

製品コード、要求本文、他の試験file、v1のRED 3 file、保持中GREEN 2 fileは本補正で変更しない。
自動試験はGit書込み経路がないことだけを確認し、意味的に完結したcommit、停止、push・履歴書換え・
外部送信なしは完了Evidenceで別に確認する。

## 4. 期待する成果

- 対応表の未定義参照が0件になる。
- 現行製品コードは正常例として成功し、直接書込み4種と間接呼出し3変種が失敗側へ分類される。
- 補正は`tests/test_pilot_collaboration.py`一件だけのcommitへ固定される。
- その後、保持中GREENへ戻り、v1の関連試験と公式全試験を正常終了させる。

## 5. 機械確認

次を単独実行する。

```text
.venv/bin/python3 -m pytest -q \
  tests/test_pilot_collaboration.py::test_requirement_traceability_covers_all_26_ids
.venv/bin/python3 -m pytest -q \
  tests/test_pilot_collaboration.py::test_pilot_git_processes_are_read_only
.venv/bin/python3 -m pytest -q \
  tests/test_pilot_collaboration_entrypoints.py::test_change_scope_rejects_forbidden_commit_before_later_allowed_commit \
  tests/test_pilot_collaboration_entrypoints.py::test_change_scope_does_not_hide_code_inside_handoff_directory
```

構文木から対応表3 key、定義済み試験、製品コードの`_run_git`参照とprocess呼出しを再列挙する。
実Git書込みは行わない。補正commit後はv1第5.2節へ戻る。

## 6. レビューで判断する事項

v2とv3で一回の修正後確認を使い終えたため、新しい開始前レビューは追加しない。利用者がv3修正後確認の
事実を踏まえて本v4の限定範囲を承認したことを開始根拠とする。

完了レビューは、v1からv4、RED、補正、GREEN、Evidenceを一続きで一回だけ確認する。Git書込み禁止の
自動試験と、事後のGit・外部操作Evidenceを混同しない。

## 7. 停止条件と完了条件

製品コード、要求本文、他の試験fileを変更する必要がある場合、または上記7反例のいずれかを同じ一fileで
拒否できない場合は停止する。公式全試験で対応表未定義参照以外の新しい失敗が見つかった場合も停止する。

完了には、補正一file commit、指定試験合格、RED不変、関連試験合格、公式全試験合格、Evidence、
独立完了レビュー`verified`を要する。第2段完了とPython 3.13移行は別判断のままとする。
