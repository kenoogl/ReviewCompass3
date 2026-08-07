"""伏字化規則：環境依存参照と初版パターン規則。

承認：DEC-REDACTION-RULES-DESIGN-001
設計：docs/design/2026-08-07-redaction-rules-design-proposal.md

核心は「環境依存値が伏字化の副産物として漏れないこと」であり、置換先・digest・診断の
いずれにも実値が出ないことを固定する。
"""

import json
from pathlib import Path

import pytest

from tools.session_logs import redaction


def _environment_rules():
    return redaction.environment_reference_rules()


def test_e1_environment_rules_declare_roles_without_values():
    """規則は役割名だけを持ち、実値を持たない。"""

    rules = _environment_rules()
    roles = {rule.environment_role for rule in rules}
    assert roles == {"home_directory", "user_name", "host_name"}
    for rule in rules:
        assert not hasattr(rule, "pattern") or rule.pattern is None
        assert rule.label == rule.environment_role


def test_e2_resolution_happens_at_run_time():
    """実値は実行時に環境から解決される。"""

    resolved = redaction.resolve_environment_rules(_environment_rules())
    home = str(Path.home())
    assert any(rule.pattern and home in rule.pattern for rule in resolved)


def test_e3_replacement_carries_the_role_not_the_value():
    """置換先には役割名だけが出る（反証：実値が置換先へ漏れる）。"""

    home = str(Path.home())
    text = "設定は %s/.reviewcompass3/config.json にある" % home
    result = redaction.redact_with_environment(text)
    assert home not in result.text
    assert "[REDACTED:home_directory]" in result.text


def test_e4_digest_excludes_resolved_values():
    """規則digestの入力は役割名であり、解決後の実値を含まない。

    反証：digestが環境情報の写しになる。
    """

    digest = redaction.redaction_rules_digest(
        _environment_rules(), allow_patterns=()
    )
    home = str(Path.home())
    payload = redaction.redaction_rules_digest_payload(
        _environment_rules(), allow_patterns=()
    )
    assert home not in payload
    assert Path.home().name not in payload
    assert "home_directory" in payload
    assert len(digest) == 64


def test_e5_diagnostics_do_not_leak_values(tmp_path):
    """診断・報告に実値が出ない性質を壊さない。"""

    home = str(Path.home())
    text = "%s/secret とtoken Xq7Lm2Rt9Wz4Yb1Nc6Vd3KpEf8Gh5Jk" % home
    with pytest.raises(redaction.SensitiveDataRemaining) as error:
        redaction.redact_with_environment(text, strict=True)
    report_path = tmp_path / "report.json"
    redaction.write_sensitive_report(
        report_path, error.value, source_path="fixture"
    )
    written = report_path.read_text(encoding="utf-8")
    assert home not in written
    assert Path.home().name not in written


def test_e6_pattern_rules_cover_the_approved_initial_set():
    """承認された初版5件が登録されている。"""

    labels = {rule.label for rule in redaction.default_pattern_rules()}
    assert labels == {
        "email",
        "bearer_token",
        "api_key_assignment",
        "private_key_block",
        "aws_access_key_id",
    }


def test_e7_pattern_rules_redact_their_targets():
    """初版規則が対象を伏字にする（合成した架空の値のみ）。"""

    samples = {
        "email": "連絡先は sample.person@example.invalid です",
        "bearer_token": "Authorization: Bearer abcdefghijklmnopqrstuvwx",
        "api_key_assignment": 'api_key="ZZZfakekeyvalue1234567890"',
        "aws_access_key_id": "AKIAZZZZFAKEEXAMPLE1",
    }
    rules = redaction.default_pattern_rules()
    for label, text in samples.items():
        result = redaction.redact_text(text, rules)
        assert "[REDACTED:%s]" % label in result.text, label


def test_e9_digesting_resolved_rules_does_not_leak_the_value():
    """反証レビューで成立した漏れ（解決済み規則をdigestへ渡す誤用）を塞ぐ。

    解決済み規則はpatternに実値を含むため、誤って渡された場合でもdigestの入力は
    役割名だけになる。
    """

    resolved = redaction.resolve_environment_rules(_environment_rules())
    payload = redaction.redaction_rules_digest_payload(resolved, allow_patterns=())
    home = str(Path.home())
    assert home not in payload
    assert Path.home().name not in payload
    assert "home_directory" in payload


def test_e8_application_order_is_deterministic():
    """同じ入力から同じ結果が出る（適用順序が決定的である）。"""

    home = str(Path.home())
    text = "%s/x api_key=\"ZZZfakekeyvalue1234567890\"" % home
    first = redaction.redact_with_environment(text)
    second = redaction.redact_with_environment(text)
    assert first.text == second.text
    assert [item.label for item in first.findings] == [
        item.label for item in second.findings
    ]
