import json
import subprocess
from typing import Optional


# Missing:
# - easy_install


def pip():
    try:
        output = subprocess.check_output(
            "pip list --format json",
            shell=True,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        return {}

    pkg_output = output.decode("utf-8")

    pkgs = json.loads(pkg_output)

    return list(
        map(
            lambda x: {"name": x["name"], "version": x["version"], "source": "pip"},
            pkgs,
        )
    )


def pipx():
    try:
        output = subprocess.check_output(
            "pipx list --json",
            shell=True,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        return {}

    pkg_output = output.decode("utf-8")

    pkgs = json.loads(pkg_output)

    return list(
        map(
            lambda x: {
                "name": x,
                "version": pkgs["venvs"][x]["metadata"]["main_package"][
                    "package_version"
                ],
                "source": "pipx",
            },
            pkgs["venvs"].keys(),
        )
    )


def all(excluded: Optional[list[str]] = []):
    all_pkgs = []

    all_pkgs += pip()
    all_pkgs += pipx()

    return all_pkgs
