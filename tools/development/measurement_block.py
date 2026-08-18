"""測定ブロックの機械生成tool。

宣言JSONに列挙されたコマンド列をshellを使わずargv配列で実行し、
「コマンド・終了コード・所要秒・stdout／stderrの無加工全文・時刻」を
1つの機械生成markdownへnew-onlyで固定する。recordはこの生成物を参照し、
LLMは意味の説明だけを書く（数値転記の構造的排除）。

- 出力中のfenceには、外側fenceを内容の最長backtick連より長くして耐える。
- streamの規模上限超過は、明示の切り詰め印を機械が記す（黙って欠けない）。
- コマンドの非0終了はデータとして記録し、tool自体の失敗にしない。
  spawn失敗・timeoutは測定不完全（終了コード1）。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import argparse
import json
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

from tools.common import digests


STREAM_LIMIT_BYTES = 100_000
_BACKTICK_RUN = re.compile(r"`+")


def _fenced(content):
    longest = max(
        (len(run) for run in _BACKTICK_RUN.findall(content)),
        default=0,
    )
    fence = "`" * max(3, longest + 1)
    return f"{fence}text\n{content}\n{fence}"


def _clipped(text):
    encoded = text.encode("utf-8")
    if len(encoded) <= STREAM_LIMIT_BYTES:
        return text, None
    clipped = encoded[:STREAM_LIMIT_BYTES].decode("utf-8", errors="ignore")
    return clipped, len(encoded)


def _load_declaration(path):
    document = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(document, dict):
        raise ValueError("declaration is not an object")
    title = document.get("title")
    entries = document.get("entries")
    if not isinstance(title, str) or not title.strip():
        raise ValueError("title is invalid")
    if not isinstance(entries, list) or not entries:
        raise ValueError("entries is invalid")
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("entry is not an object")
        if not isinstance(entry.get("label"), str) or not entry["label"].strip():
            raise ValueError("entry label is invalid")
        argv = entry.get("argv")
        if (
            not isinstance(argv, list)
            or not argv
            or not all(isinstance(item, str) and item for item in argv)
        ):
            raise ValueError("entry argv is invalid")
    return title, entries


def _run_entry(entry, timeout_seconds):
    started = time.monotonic()
    try:
        completed = subprocess.run(
            entry["argv"],
            capture_output=True,
            text=True,
            errors="replace",
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired:
        return {
            "state": "timeout",
            "elapsed": round(time.monotonic() - started, 3),
            "stdout": "",
            "stderr": "",
        }
    except OSError as error:
        return {
            "state": "spawn_error",
            "detail": str(error),
            "elapsed": round(time.monotonic() - started, 3),
            "stdout": "",
            "stderr": "",
        }
    return {
        "state": "ran",
        "exit_code": completed.returncode,
        "elapsed": round(time.monotonic() - started, 3),
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def _render_stream(name, content):
    clipped, total_bytes = _clipped(content)
    lines = []
    if total_bytes is not None:
        lines.append(
            f"- {name}【切り詰め：全{total_bytes} byte中先頭"
            f"{STREAM_LIMIT_BYTES} byteのみ】："
        )
    else:
        lines.append(f"- {name}：")
    lines.append("")
    lines.append(_fenced(clipped))
    return lines


def _render(title, declaration_path, captured_at, results):
    lines = [
        f"# 測定ブロック：{title}",
        "",
        f"- captured_at：{captured_at}",
        f"- 宣言file：`{declaration_path}`（SHA-256 "
        f"`{digests.file_sha256(declaration_path)}`）",
        "- 生成tool：`tools/development/measurement_block.py`"
        "（機械生成file。手編集禁止）",
        "",
    ]
    for label, entry, result in results:
        lines.append(f"## {label}")
        lines.append("")
        lines.append(
            "- argv：`" + json.dumps(entry["argv"], ensure_ascii=False) + "`"
        )
        if result["state"] == "ran":
            lines.append(
                f"- exit：{result['exit_code']}・elapsed：{result['elapsed']}s"
            )
        elif result["state"] == "timeout":
            lines.append(f"- 状態：timeout（elapsed：{result['elapsed']}s）")
        else:
            lines.append(f"- 状態：spawn_error（{result['detail']}）")
        lines.append("")
        if result["stdout"]:
            lines.extend(_render_stream("stdout", result["stdout"]))
            lines.append("")
        if result["stderr"]:
            lines.extend(_render_stream("stderr", result["stderr"]))
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def run(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--commands", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--timeout-seconds", type=float, default=120.0)
    arguments = parser.parse_args(
        list(sys.argv[1:] if argv is None else argv)
    )
    declaration_path = Path(arguments.commands)
    output_path = Path(arguments.output)
    try:
        title, entries = _load_declaration(declaration_path)
    except (OSError, ValueError):
        print(json.dumps(
            {"schema_version": 1, "status": "input_invalid"},
            ensure_ascii=False,
            sort_keys=True,
        ))
        return 2
    if (
        output_path.exists()
        or output_path.is_symlink()
        or not output_path.parent.is_dir()
    ):
        print(json.dumps(
            {"schema_version": 1, "status": "input_invalid"},
            ensure_ascii=False,
            sort_keys=True,
        ))
        return 2
    captured_at = datetime.now().astimezone().isoformat(timespec="seconds")
    results = []
    incomplete = 0
    failed_count = 0
    for entry in entries:
        result = _run_entry(entry, arguments.timeout_seconds)
        if result["state"] != "ran":
            incomplete += 1
        elif result["exit_code"] != 0:
            failed_count += 1
        results.append((entry["label"], entry, result))
    content = _render(title, declaration_path, captured_at, results)
    with open(output_path, "x", encoding="utf-8") as stream:
        stream.write(content)
    status = "ok" if incomplete == 0 else "incomplete"
    print(json.dumps(
        {
            "schema_version": 1,
            "status": status,
            "output_path": str(output_path),
            "entry_count": len(entries),
            "failed_count": failed_count,
            "incomplete_count": incomplete,
        },
        ensure_ascii=False,
        sort_keys=True,
    ))
    return 0 if incomplete == 0 else 1


def main():
    raise SystemExit(run())


if __name__ == "__main__":
    main()
