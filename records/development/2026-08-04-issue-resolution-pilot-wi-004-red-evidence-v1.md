# Issue Resolution Pilot WI-004 RED Evidence v1

- Test：`tests/test_todo_handoff_prompt_entrypoints.py`
- Test SHA-256：`cb2d557990bc01b4365b8ea8fdcd78f130a82eb65362f8b7a0ef5f393015d461`
- targeted：`1 passed, 2 failed in 0.06s`
- 全体：`632 passed, 2 failed in 2.61s`
- 失敗identity：共通promptとroot `CLAUDE.md`が存在しないための`FileNotFoundError` 2件。
- 合格した負例：`CLAUDE.md`へ独立したTODO意味規則を追加した構成を拒否した。
- 固定境界：共通prompt一件、4,096 bytes以下、AGENTS参照一件、Claude link-only参照一件、
  重複TODO意味規則0、第二authority拒否、LLM／機械executor分離。

RED確認後に同じTestを使用してWI-004実装へ進んだ。
