import os
import subprocess
from typing import Optional


def homebrew():
    try:
        output = subprocess.check_output(
            "brew list --versions",
            shell=True,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        return {}

    pkg_output = output.decode("utf-8")

    pkgs = []
    for pkg in pkg_output.split("\n"):
        if len(pkg) > 0:
            info = pkg.split(" ")
            pkgs.append({"name": info[0], "version": info[1], "source": "homebrew"})

    return pkgs


def macport():
    try:
        output = subprocess.check_output(
            "port installed",
            shell=True,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        return {}

    pkg_output = output.decode("utf-8")

    pkgs = []
    for pkg in pkg_output.split("\n"):
        if len(pkg) > 0 and "@" in pkg:
            info = pkg.strip().split(" ")
            pkgs.append(
                {
                    "name": info[0],
                    "version": info[1].replace("@", ""),
                    "source": "macport",
                }
            )

    return pkgs


def pkgutil():
    try:
        output = subprocess.check_output(
            "pkgutil --pkgs", shell=True, stderr=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError:
        return {}

    pkg_output = output.decode("utf-8")

    pkgs = []
    for pkg in pkg_output.split("\n"):
        if len(pkg) > 0:
            pkgs.append({"name": pkg, "version": None})

    return pkgs


def system():
    bins = []
    if os.path.exists("/usr/bin") is True:
        bins += os.listdir("/usr/bin")
    if os.path.exists("/usr/sbin") is True:
        bins += os.listdir("/usr/sbin")
    if os.path.exists("/usr/local/bin") is True:
        bins += os.listdir("/usr/local/bin")
    if os.path.exists("/usr/local/sbin") is True:
        bins += os.listdir("/usr/local/sbin")
    if os.path.exists("/usr/local/bin") is True:
        bins += os.listdir("/usr/local/bin")
    if os.path.exists("/usr/local/sbin") is True:
        bins += os.listdir("/usr/local/sbin")

    return list(map(lambda x: {"name": x, "version": None, "source": "system"}, bins))


def all(excluded: Optional[list[str]] = []):
    all_pkgs = []

    if (len(excluded) > 0 and "homebrew" not in excluded) or len(excluded) == 0:
        all_pkgs += homebrew()
    if (len(excluded) > 0 and "macport" not in excluded) or len(excluded) == 0:
        all_pkgs += macport()
    if (len(excluded) > 0 and "system" not in excluded) or len(excluded) == 0:
        all_pkgs += system()

    return all_pkgs
