"""公式Test実行の構造化集計hook。

`RC3_TEST_SUMMARY_PATH`が設定されているときだけ、pytestのreport objectから数えた集計を
その場所へ書き出す。設定されていなければ何もしない。実行結果の出力文字列は解析しない。

集計の定義は`tools/development/pytest_summary.py`のdocstringを正本とする。
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from tools.development import pytest_summary  # noqa: E402


_COUNTS = pytest_summary.new_counts()


def pytest_runtest_logreport(report):
    """report objectを一件ずつ数える。machine APIだけを読む。"""

    pytest_summary.record_report(_COUNTS, report)


def pytest_collectreport(report):
    """収集段階の失敗を数える。test単位のreportが出ない経路を落とさない。"""

    pytest_summary.record_collect_report(_COUNTS, report)


def pytest_sessionfinish(session, exitstatus):
    """session終了時に、要求された場所へ集計を書き出す。"""

    target = os.environ.get(pytest_summary.SUMMARY_ENVIRONMENT_VARIABLE)
    if not target:
        return
    pytest_summary.write_summary(target, _COUNTS)
