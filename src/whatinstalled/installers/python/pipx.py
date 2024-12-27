import json
import logging
from typing import Any

from whatinstalled.installers.base import BaseInstaller, execute_command


def _build_dict(
    x: str, pkgs: dict[str, Any], include_latest: bool = False
) -> dict[str, str | None]:
    data: dict[str, str | None] = {
        "name": x,
        "version": pkgs["venvs"][x]["metadata"]["main_package"]["package_version"],
        "source": "pipx",
    }

    if include_latest is True:
        data["latest"] = None

    return data


class PipxInstaller(BaseInstaller):
    name = "pipx"
    list_cmd = "pipx list --json"
    outdated_cmd = "echo '[]'"
    available_cmd = "pipx --version"

    def list_packages(
        self, include_latest: bool = False
    ) -> list[dict[str, str | None]]:
        pkgs_output = execute_command(self.list_cmd)

        if pkgs_output is not None:
            pkgs = json.loads(pkgs_output)
            pkgs = list(
                map(
                    lambda x: _build_dict(x, pkgs, include_latest),
                    pkgs["venvs"].keys(),
                )
            )

            if include_latest is True:
                logging.warning("Listing outdated packages is not possible with pipx")

            self.packages = pkgs

        return self.packages

    def list_outdated(self) -> list[dict[str, str | None]]:
        return self.outdated
