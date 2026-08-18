"""機械的レビュー計画を一行JSONで返すCLI。"""

import json
from pathlib import Path
import sys

from tools.development.review_plan import ReviewPlanStop, build_review_plan


_REQUIRED_FLAGS = ("base-commit", "risk", "stage", "classification")
_OPTIONAL_FLAGS = ("target-commit",)


def _parse(arguments):
    if len(arguments) % 2 != 0:
        raise ReviewPlanStop("input_invalid")
    values = {}
    known = set(_REQUIRED_FLAGS) | set(_OPTIONAL_FLAGS)
    for index in range(0, len(arguments), 2):
        flag = arguments[index]
        if not flag.startswith("--"):
            raise ReviewPlanStop("input_invalid")
        name = flag[2:]
        if name not in known or name in values:
            raise ReviewPlanStop("input_invalid")
        values[name] = arguments[index + 1]
    if any(name not in values for name in _REQUIRED_FLAGS):
        raise ReviewPlanStop("input_invalid")
    return values


def _write(value):
    sys.stdout.write(
        json.dumps(
            value,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )
        + "\n"
    )


def run(argv=None):
    arguments = tuple(sys.argv[1:] if argv is None else argv)
    try:
        values = _parse(arguments)
        result = build_review_plan(
            Path.cwd(),
            base_commit=values["base-commit"],
            target_commit=values.get("target-commit", "HEAD"),
            risk=values["risk"],
            stage=values["stage"],
            classification_path=values["classification"],
        )
        exit_code = 0
    except ReviewPlanStop as error:
        result = {
            "record_kind": "mechanical_review_plan_stop",
            "result": "stopped",
            "schema_version": 1,
            "stop_code": error.code,
        }
        exit_code = 2
    except Exception:
        result = {
            "record_kind": "mechanical_review_plan_stop",
            "result": "failed",
            "schema_version": 1,
            "stop_code": "internal_error",
        }
        exit_code = 1
    _write(result)
    return exit_code


def main():
    return run()


if __name__ == "__main__":
    raise SystemExit(main())
