# Issue Resolution Pilot Plan revision RED Evidence v1

- recorded_at: `2026-08-04T09:18:16+09:00`
- subject: `PLAN-PILOT-TODO-GROWTH-001 version 2 / CHALLENGE-PILOT-TODO-GROWTH-001 version 2`
- test: `tests/test_issue_resolution_pilot_plan_revision.py`
- test_sha256: `1ecc2172e77d9dcaca12753dda3a7046dd8789080bc6749f14082ae96da6832b`

## RED

- command: `python3 -m pytest -q tests/test_issue_resolution_pilot_plan_revision.py`
- result: `5 failed in 0.06s`
- cause: validatorがPlan／Challengeのversionを1に固定し、Plan v2のderived state closure、12288／12289 bytes境界、link-only Claude入口を検査していなかった。

失敗した5件は次を固定した。

1. derived state closureを持つPlan v2を受理する。
2. derived state obligation、Work Item、Acceptance、oracleのいずれかが欠けるPlan v2を拒否する。
3. 12288 bytes合格と12289 bytes拒否が明記されないPlan v2を拒否する。
4. root `CLAUDE.md`を第二authorityにするPlan v2を拒否する。
5. Challenge v2を版付きpathで受理する。

## GREEN

- command: `python3 -m pytest -q tests/test_issue_resolution_pilot_plan_revision.py`
- result: `5 passed in 0.02s`
- implementation_sha256: `68d0a79a814633ee1ad6253491d6f855dd80e0433450a3d8ee35bb7302fed88d`
- plan_v2_sha256: `1aa63a008a9c396a211231185c965300b7f4caa45ef07424796d3b9f6d6482ac`
- challenge_v2_sha256: `ca5b12124d34dd039f73bd9638aabe23eaa47f0112fc3688d089a67f58936b24`

このEvidenceはPlan v2の最終Human承認ではない。Challenge v2の`ready_for_human_approval`を受け、別のHuman Decisionが必要である。
