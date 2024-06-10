import re
import subprocess
from typing import Optional


# Missing:
# - apt list --installed
# - aptitude install
# - yum install
# - pacman install
# - dnf install
# - zypper in
# - pkgutil --pkgs


def dpkg():
    try:
        output = subprocess.check_output(
            "dpkg -l",
            shell=True,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        return {}

    pkg_output = output.decode("utf-8")

    regex = r"ii\s+([^\s]+)\s+([^\s]*)\s+([^\s]*)\s+(.*)"
    matches = re.finditer(regex, pkg_output, re.MULTILINE)

    pkgs = []
    for _, match in enumerate(matches, start=1):
        groups = match.groups()
        pkgs.append({"name": groups[0], "version": groups[1], "source": "dpkg"})

    return pkgs


def all(excluded: Optional[list[str]] = []):
    all_pkgs = []

    if (len(excluded) > 0 and "dpkg" not in excluded) or len(excluded) == 0:
        all_pkgs += dpkg()

    return all_pkgs


if __name__ == "__main__":
    all()
