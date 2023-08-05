from __future__ import annotations

from pathlib import Path

from setuptools import find_packages, setup

_version = (
    "0.0.8"  # Version will be replaced by the CD pipeline
)
VERSION = "0.0.0" if _version.startswith("{{") else _version


def get_readme() -> str:
    readme = Path("README.md")
    return readme.read_text(encoding="utf-8")


def get_requirements() -> list[str]:
    requirements = Path("requirements.txt")
    return requirements.read_text(encoding="utf-8").splitlines()


setup(
    name="better-fsm",
    description="",
    long_description=get_readme(),
    long_description_content_type="text/markdown",
    version=VERSION,
    packages=find_packages(include=["better_fsm", "better_fsm.*"]),
    install_requires=get_requirements(),
    keywords=[],
    package_data={"better_fsm": ["py.typed"]},
)
