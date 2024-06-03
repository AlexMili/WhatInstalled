import subprocess
from typing import Optional


def luarocks():
    try:
        output = subprocess.check_output(
            "luarocks list --porcelain",
            shell=True,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        return {}

    pkg_output = output.decode("utf-8")

    pkgs = []
    for pkg in pkg_output.split("\n"):
        if len(pkg) > 0:
            info = pkg.split("\t")
            pkgs.append({"name": info[0], "version": info[1], "source": "luarocks"})

    return pkgs


def all(excluded: Optional[list[str]] = []):
    all_pkgs = []

    all_pkgs += luarocks()

    return all_pkgs
