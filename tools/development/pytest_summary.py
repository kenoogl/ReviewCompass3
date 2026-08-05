"""公式Test実行の構造化集計。

件数はpytestのmachine API（report object）から数える。実行結果の出力文字列を解析しない。

`test_summary`の各fieldの意味は次のとおりである。

- passed：呼出し段階（`call`）が成功したtestの数。xpassedは含まない。
- failed：呼出し段階が失敗したtestの数。xfailedは含まない。
- skipped：実行を飛ばしたtestの数。xfailedは含まない。
- xfailed：失敗を期待していて、実際に失敗したtestの数。
- xpassed：失敗を期待していたのに成功したtestの数。
- errors：呼出し以外の段階（`setup`／`teardown`）で失敗したtestの数。
- total：上記6つの合計。

集計器は、この7つ以外のfieldを持つ入力を受理しない。値は0以上の整数だけを受理し、
真偽値は整数として扱わない。`total`が内訳の合計と一致しない入力も受理しない。
"""

import json
from pathlib import Path


#: 集計の書出し先をsubprocessへ渡す環境変数名。
SUMMARY_ENVIRONMENT_VARIABLE = "RC3_TEST_SUMMARY_PATH"

#: 集計fieldの並び。`total`は内訳の合計である。
SUMMARY_FIELDS = (
    "passed",
    "failed",
    "skipped",
    "xfailed",
    "xpassed",
    "errors",
    "total",
)

_COUNT_FIELDS = SUMMARY_FIELDS[:-1]


class TestSummaryError(Exception):
    """構造化集計を安全に扱えない。"""


def new_counts():
    """内訳を0で初期化する。"""

    return {field: 0 for field in _COUNT_FIELDS}


def record_report(counts, report):
    """pytestのreport objectを一件数える。

    report objectは`when`（段階）と`outcome`（結果）を持つ。`wasxfail`が付いていれば
    失敗を期待したtestである。ここでは属性だけを読み、文字列の整形結果を見ない。
    """

    when = getattr(report, "when", None)
    outcome = getattr(report, "outcome", None)
    expected_failure = hasattr(report, "wasxfail")

    if when != "call":
        if outcome == "failed":
            counts["errors"] += 1
        elif outcome == "skipped" and when == "setup":
            counts["skipped"] += 1
        return counts

    if outcome == "failed":
        counts["failed"] += 1
    elif outcome == "skipped":
        counts["xfailed" if expected_failure else "skipped"] += 1
    elif outcome == "passed":
        counts["xpassed" if expected_failure else "passed"] += 1
    return counts


def finalize(counts):
    """内訳へ`total`を足した集計を返す。"""

    if not isinstance(counts, dict) or set(counts) != set(_COUNT_FIELDS):
        raise TestSummaryError("test_summary_invalid: counts")
    summary = {field: counts[field] for field in _COUNT_FIELDS}
    summary["total"] = sum(summary[field] for field in _COUNT_FIELDS)
    validate_summary(summary)
    return summary


def validate_summary(summary):
    """fieldの過不足、型、負数、合計不一致を拒否する。"""

    if not isinstance(summary, dict):
        raise TestSummaryError("test_summary_invalid: not a mapping")
    if set(summary) != set(SUMMARY_FIELDS):
        raise TestSummaryError("test_summary_invalid: fields")
    for field in SUMMARY_FIELDS:
        value = summary[field]
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise TestSummaryError(f"test_summary_invalid: {field}")
    if summary["total"] != sum(summary[field] for field in _COUNT_FIELDS):
        raise TestSummaryError("test_summary_invalid: total")
    return True


def write_summary(path, counts):
    """内訳を確定してJSONで書き出す。"""

    summary = finalize(counts)
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(summary, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return summary


def read_summary(path):
    """書き出した集計を読み、検証して返す。"""

    target = Path(path)
    if not target.is_file():
        raise TestSummaryError("test_summary_unavailable: file is missing")
    try:
        summary = json.loads(target.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise TestSummaryError("test_summary_unavailable: unreadable") from error
    validate_summary(summary)
    return summary
