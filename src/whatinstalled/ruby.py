import subprocess
from typing import Optional


# Missing:
# - rvm


def gem():
    try:
        output = subprocess.check_output(
            "gem query --local",
            shell=True,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        return {}

    pkg_output = output.decode("utf-8")

    pkgs = []
    for pkg in pkg_output.split("\n"):
        if len(pkg) > 0 and "(" in pkg and ")" in pkg:
            info = pkg.split(" ")
            version = info[1].replace("default: ", "").replace("(", "").replace(")", "")
            pkgs.append({"name": info[0], "version": version, "source": "gem"})

    return pkgs


def all(excluded: Optional[list[str]] = []):
    all_pkgs = []

    all_pkgs += gem()

    return all_pkgs
