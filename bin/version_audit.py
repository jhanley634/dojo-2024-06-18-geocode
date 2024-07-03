#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
"""
A version_audit() compares `pip freeze` against requirements.txt.
"""
import re
import subprocess
from collections.abc import Generator
from dataclasses import dataclass
from pathlib import Path


def _get_requirements(reqs_in_file: Path) -> Generator[tuple[str, str], None, None]:

    line_re = re.compile(r"^(?P<name>[\w-]+)\s*>=\s*(?P<version>[\d.]+)")

    for line in reqs_in_file.read_text().splitlines():
        if m := line_re.search(line):
            yield m[1], m[2]


@dataclass
class Package:
    name: str
    version: str


def _get_frozen_versions() -> Generator[Package, None, None]:

    line_re = re.compile(r"^(?P<name>[\w-]+)\s*==\s*(?P<version>[\d.]+)")

    pkgs = subprocess.check_output(["pip", "freeze"]).decode().splitlines()
    for pkg in pkgs:
        if m := line_re.search(pkg):
            yield Package(m[1], m[2])


def version_audit(reqs_in_file: Path = Path("requirements.txt")) -> None:
    """
    Compare `pip freeze` against requirements.txt, reporting any discrepancies.
    """
    reqs = dict(_get_requirements(reqs_in_file))

    for pkg in _get_frozen_versions():
        if pkg.name in reqs and pkg.version != reqs[pkg.name]:
            print(f"{pkg.name} >= {pkg.version} \t(was {reqs[pkg.name]})")


if __name__ == "__main__":
    version_audit()
