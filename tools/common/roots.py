"""repository root解決の正本（配置同型性の原則、デプロイ方針record §3論点4b-1）。

親ディレクトリ遡り（root深度の知識）は本moduleにのみ置く。他のfileは本moduleへ
委譲し、遡りを複製しない（RC2 paths.py型の一元化）。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

from pathlib import Path


def repo_root():
  """repository rootの絶対pathを返す。"""
  return Path(__file__).resolve().parents[2]
