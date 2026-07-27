"""ブートストラップreview固定CLI・配置境界の暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib
import json


def test_dry_run_is_cwd_independent_and_creates_nothing(
  tmp_path,
  monkeypatch,
  capsys,
):
  repository = tmp_path / "repository"
  repository.mkdir()
  private_root = tmp_path / "private"
  config = repository / "review.json"
  config.write_text(
    json.dumps({
      "repository_root": str(repository),
      "private_root": str(private_root),
      "triage_root": "records/reviews",
      "attempt_id": "attempt-001",
    }),
    encoding="utf-8",
  )
  outside = tmp_path / "outside"
  outside.mkdir()
  monkeypatch.chdir(outside)
  review_cli = importlib.import_module(
    "tools.bootstrap.review_cli"
  )

  assert review_cli.run((
    "--config",
    str(config),
    "--dry-run",
  )) == 0

  result = json.loads(capsys.readouterr().out)
  assert result == {
    "parsed_location": "private",
    "raw_location": "private",
    "status": "dry_run",
    "triage_location": "git",
    "writes": 0,
  }
  assert not private_root.exists()
  assert not (repository / "records" / "reviews").exists()


def test_rejects_private_artifacts_inside_repository(tmp_path):
  repository = tmp_path / "repository"
  repository.mkdir()
  config = repository / "review.json"
  config.write_text(
    json.dumps({
      "repository_root": str(repository),
      "private_root": str(repository / "private"),
      "triage_root": "records/reviews",
      "attempt_id": "attempt-001",
    }),
    encoding="utf-8",
  )
  review_cli = importlib.import_module(
    "tools.bootstrap.review_cli"
  )

  assert review_cli.run((
    "--config",
    str(config),
    "--dry-run",
  )) == 2


def test_project_exposes_fixed_bootstrap_review_command():
  project = (
    __import__("pathlib").Path(__file__).parents[1]
    / "pyproject.toml"
  ).read_text(encoding="utf-8")

  assert (
    'reviewcompass3-bootstrap-review = '
    '"tools.bootstrap.review_cli:main"'
  ) in project
