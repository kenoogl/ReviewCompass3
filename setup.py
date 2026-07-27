"""互換性のあるReviewCompass3パッケージ入口。"""

from setuptools import find_namespace_packages, setup


setup(
  name="reviewcompass3",
  version="0.0.1",
  description="ReviewCompass scratch rebuild",
  python_requires=">=3.9",
  packages=find_namespace_packages(
    include=("tools", "tools.*"),
  ),
  install_requires=("platformdirs>=4,<5",),
  entry_points={
    "console_scripts": (
      "reviewcompass3-session-logs="
      "tools.session_logs.entry:main",
      "reviewcompass3-bootstrap-review="
      "tools.bootstrap.review_cli:main",
    ),
  },
)
