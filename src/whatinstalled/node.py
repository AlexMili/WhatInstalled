import json
import subprocess
from typing import Optional


# Missing:
# - nvm


def _parse_name(name: str, source: str):
    # Some packages start with an "@" but the "@" is also
    # the way to separate version number with package name on node.
    # Skipping the first character allow to only get the "@" to separate the
    # version number
    idx = name[1:].index("@")
    return {"name": name[0 : idx + 1], "version": name[idx + 2 :], "source": source}


def yarn():
    try:
        output = subprocess.check_output(
            "yarn list --json --depth=0",
            shell=True,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        return {}

    pkg_output = output.decode("utf-8")
    pkgs = json.loads(pkg_output)

    pkgs_clean = []
    for elt in pkgs["data"]["trees"]:
        pkgs_clean.append(_parse_name(elt["name"], source="yarn"))

    return pkgs_clean


def npm():
    try:
        output = subprocess.check_output(
            "npm list -g --depth=0 --json",
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
                "version": pkgs["dependencies"][x]["version"],
                "source": "npm",
            },
            pkgs["dependencies"].keys(),
        )
    )


def all(excluded: Optional[list[str]] = []):
    all_pkgs = []

    all_pkgs += yarn()
    all_pkgs += npm()

    return all_pkgs
