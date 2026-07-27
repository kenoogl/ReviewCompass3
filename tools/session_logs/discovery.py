"""生セッションログの発見。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

from pathlib import Path


def discover_raw_logs(root) -> tuple:
  root_path = Path(root)
  if not root_path.exists():
    raise FileNotFoundError(root_path)
  if not root_path.is_dir():
    raise NotADirectoryError(root_path)

  return tuple(sorted(
    path.relative_to(root_path).as_posix()
    for path in root_path.rglob("*.jsonl")
    if path.is_file()
  ))
