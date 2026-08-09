"""front matter authority参照のDigest検査器（deferred #5）。

lifecycle: provisional
normative_status: non-normative
promotion_required: true

正本authority：`ISSUE-AUTHORITY-REFERENCE-DIGEST-CHECK-001`と改善候補
`IC-AUTHORITY-REFERENCE-DIGEST-CHECK-001`のscope／non_scope。検査対象は
Human承認済みallowlist（`tools/development/authority_reference_keys.json`）に
載ったfront matter keyの「現在有効な上位文書」参照だけであり、本文中の参照・
JSON record・`generated_from`等の時点固定pinは対象にしない
（`DEC-FIXED-SOURCE-KIND-001`の区別に従う）。

読み取り専用：参照Digestの自動書換え・fileの作成変更は行わない。
汎用YAML解析は使わず、許可keyの宣言された期待形（単一mapping／mappingのlist、
`path`＋`sha256`）だけを受け付ける専用解析とし、解釈不能な形はfail-closedに失敗させる。
"""

import argparse
import json
import re
from pathlib import Path

from tools.common.digests import file_sha256


_DEFAULT_ALLOWLIST = Path(__file__).with_name("authority_reference_keys.json")
_HEX64 = re.compile(r"^[0-9a-f]{64}$")
_TOP_KEY = re.compile(r"^([A-Za-z0-9_]+):\s*(.*)$")
_SHAPES = ("mapping", "mapping_list")


class CheckerError(Exception):
    """検査を安全に実行できない。文言は安定stop codeのみ。"""

    def __init__(self, stop_code):
        self.stop_code = stop_code
        super().__init__(stop_code)


def _load_allowlist(path):
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        data = None
    if (
        not isinstance(data, dict)
        or data.get("schema_version") != 1
        or not isinstance(data.get("keys"), dict)
        or not data["keys"]
        or any(
            not isinstance(key, str) or shape not in _SHAPES
            for key, shape in data["keys"].items()
        )
    ):
        raise CheckerError("allowlist_invalid")
    return data["keys"]


def _front_matter(lines):
    """front matter部分を(行番号, 行)のlistで返す。無ければ空list。"""

    if not lines or lines[0].strip() != "---":
        return []
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return [
                (number + 2, line)
                for number, line in enumerate(lines[1:index])
            ]
    return []


def _parse_pair_lines(pair_lines):
    """`path:`／`sha256:`のsub行群を(dict, 解釈可能か)へ写す。"""

    values = {}
    for _number, text in pair_lines:
        stripped = text.strip()
        name, separator, value = stripped.partition(":")
        if separator != ":" or name not in ("path", "sha256"):
            return None
        if name in values:
            return None
        values[name] = value.strip()
    return values


def _extract_references(matter_lines, allowlist):
    """許可keyの参照entryと、許可key配下の解釈不能entryを抽出する。"""

    references = []
    invalid = []
    index = 0
    while index < len(matter_lines):
        number, line = matter_lines[index]
        match = _TOP_KEY.match(line)
        index += 1
        if match is None:
            continue
        key = match.group(1)
        inline_value = match.group(2).strip()
        block = []
        while index < len(matter_lines):
            _sub_number, sub_line = matter_lines[index]
            if sub_line.strip() and not sub_line.startswith(" "):
                break
            block.append(matter_lines[index])
            index += 1
        if key not in allowlist:
            continue
        if inline_value:
            # 許可key行のコロン後の値は宣言形（mapping／mapping_list）に無い形であり、
            # 下位の参照対が正しくても黙って捨てずfail-closedにする（AR-P1-001）。
            invalid.append({"key": key, "path": "", "line": number})
            continue
        shape = allowlist[key]
        entries = []
        if shape == "mapping":
            entries.append((number, block))
        else:
            current = None
            for sub_number, sub_line in block:
                if sub_line.strip().startswith("- "):
                    current = (
                        sub_number,
                        [(sub_number, "  " + sub_line.strip()[2:])],
                    )
                    entries.append(current)
                elif current is not None and sub_line.strip():
                    current[1].append((sub_number, sub_line))
                elif sub_line.strip():
                    entries.append((sub_number, [(sub_number, sub_line)]))
        if not entries:
            invalid.append({"key": key, "path": "", "line": number})
            continue
        for entry_number, pair_lines in entries:
            values = _parse_pair_lines(
                [(n, t) for n, t in pair_lines if t.strip()]
            )
            if (
                values is None
                or set(values) != {"path", "sha256"}
                or not values["path"]
                or _HEX64.fullmatch(values["sha256"]) is None
            ):
                invalid.append({
                    "key": key,
                    "path": (values or {}).get("path", ""),
                    "line": entry_number,
                })
                continue
            references.append({
                "key": key,
                "path": values["path"],
                "sha256": values["sha256"],
                "line": entry_number,
            })
    return references, invalid


def _classify_reference(root, reference):
    relative = reference["path"]
    pure = Path(relative)
    if pure.is_absolute() or ".." in pure.parts or "\\" in relative:
        return "invalid"
    resolved = (root / relative).resolve()
    try:
        resolved.relative_to(root)
    except ValueError:
        return "invalid"
    if not resolved.is_file():
        return "missing"
    if file_sha256(resolved) != reference["sha256"]:
        return "mismatched"
    return "matched"


def _check_file(document_path, root, allowlist):
    try:
        text = Path(document_path).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        raise CheckerError("target_unreadable")
    matter = _front_matter(text.splitlines())
    references, invalid = _extract_references(matter, allowlist)
    report = {
        "checked": len(references),
        "matched": 0,
        "mismatched": [],
        "missing": [],
        "invalid": [
            {"key": item["key"], "path": item["path"], "line": item["line"]}
            for item in invalid
        ],
    }
    for reference in references:
        verdict = _classify_reference(root, reference)
        entry = {
            "key": reference["key"],
            "path": reference["path"],
            "line": reference["line"],
        }
        if verdict == "matched":
            report["matched"] += 1
        else:
            report[verdict].append(entry)
    return report


def run(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--allowlist", default=str(_DEFAULT_ALLOWLIST))
    parser.add_argument("--root", default=".")
    parser.add_argument("files", nargs="+")
    args = parser.parse_args(argv)
    try:
        allowlist = _load_allowlist(args.allowlist)
        root = Path(args.root).resolve()
        if not root.is_dir():
            raise CheckerError("root_invalid")
        files = {}
        acceptable = True
        totals = {
            "checked": 0,
            "matched": 0,
            "mismatched": 0,
            "missing": 0,
            "invalid": 0,
        }
        for document in args.files:
            report = _check_file(document, root, allowlist)
            files[document] = report
            totals["checked"] += report["checked"]
            totals["matched"] += report["matched"]
            totals["mismatched"] += len(report["mismatched"])
            totals["missing"] += len(report["missing"])
            totals["invalid"] += len(report["invalid"])
            if (
                report["checked"] == 0
                or report["mismatched"]
                or report["missing"]
                or report["invalid"]
            ):
                acceptable = False
    except CheckerError as error:
        print(json.dumps(
            {"status": "error", "reason": error.stop_code},
            ensure_ascii=False,
            sort_keys=True,
        ))
        return 5
    status = "ok" if acceptable and totals["checked"] > 0 else "failed"
    print(json.dumps(
        {"files": files, "status": status, "totals": totals},
        ensure_ascii=False,
        sort_keys=True,
    ))
    return 0 if status == "ok" else 5


def main():
    raise SystemExit(run())


if __name__ == "__main__":
    main()
