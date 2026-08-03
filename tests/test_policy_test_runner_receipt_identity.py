"""Test receiptを入力source identityへ自己参照させないTest。"""

from tools.development import policy_test_runner


def test_source_state_digest_excludes_designated_receipt_output(tmp_path):
    source = tmp_path / "source.py"
    source.write_text("value = 1\n")
    receipt = tmp_path / "verification-receipt.json"
    receipt.write_text('{"run": 1}\n')

    first = policy_test_runner._source_state_digest(
        tmp_path,
        excluded_paths=(receipt,),
    )
    receipt.write_text('{"run": 2}\n')
    second = policy_test_runner._source_state_digest(
        tmp_path,
        excluded_paths=(receipt,),
    )

    assert first == second
