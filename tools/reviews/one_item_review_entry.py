"""一件レビュー材料作成・結果整理の製品入口。"""

import sys

from tools.common.digests import canonical_json_bytes
from tools.reviews.one_item_review import (
    ReviewStop,
    organize_results,
    prepare_material,
    read_input_files,
    validate_results,
)


def _arguments(argv):
    if not argv or argv[0] not in {"prepare", "organize"}:
        raise ReviewStop("invalid_arguments")
    operation = argv[0]
    remainder = argv[1:]
    if len(remainder) % 2:
        raise ReviewStop("invalid_arguments")
    values = {}
    for index in range(0, len(remainder), 2):
        name = remainder[index]
        if not name.startswith("--") or name in values:
            raise ReviewStop("invalid_arguments")
        values[name] = remainder[index + 1]
    expected = {"--input-root", "--material", "--review-spec"}
    if operation == "organize":
        expected.add("--results")
    if set(values) != expected:
        raise ReviewStop("invalid_arguments")
    return operation, values


def _stopped(reason):
    return {
        "external_send_approved": False,
        "reason": reason,
        "status": "stopped",
    }


def _write(value):
    sys.stdout.write(canonical_json_bytes(value).decode("utf-8") + "\n")


def main(argv=None):
    """二つの固定操作を実行し、安全なJSON一件だけを表示する。"""

    arguments = list(sys.argv[1:] if argv is None else argv)
    try:
        operation, values = _arguments(arguments)
        inputs = read_input_files(
            input_root=values["--input-root"],
            material=values["--material"],
            review_spec=values["--review-spec"],
            results=values.get("--results"),
        )
        material = prepare_material(inputs["material"], inputs["review_spec"])
        if operation == "prepare":
            result = material
        else:
            validated = validate_results(material, inputs["results"])
            result = organize_results(material, validated)
        _write(result)
        return 0
    except ReviewStop as error:
        _write(_stopped(error.reason))
        if error.reason in {
            "sensitive_data_remaining",
            "absolute_path_remaining",
        }:
            return 3
        return 2
    except Exception:
        _write(_stopped("internal_failure"))
        return 4


if __name__ == "__main__":
    raise SystemExit(main())
