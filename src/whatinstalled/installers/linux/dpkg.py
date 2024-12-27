import logging
import re

from whatinstalled.installers.base import BaseInstaller, execute_command


def _build_dict(x: str, include_latest: bool = False) -> dict[str, str | None]:
    data = {"name": x[0], "version": x[1], "source": "dpkg"}

    if include_latest is True:
        data["latest"] = None

    return data


class DpkgInstaller(BaseInstaller):
    name = "dpkg"
    list_cmd = "dpkg -l"
    outdated_cmd = "echo '[]'"
    available_cmd = "dpkg --version"

    def list_packages(self, include_latest: bool = False) -> list[dict[str, str | None]]:
        pkgs_output = execute_command(self.list_cmd)

        if pkgs_output is not None:
            pkgs = []

            regex = r"ii\s+([^\s]+)\s+([^\s]*)\s+([^\s]*)\s+(.*)"
            matches = re.finditer(regex, pkgs_output, re.MULTILINE)

            pkgs = []
            for _, match in enumerate(matches, start=1):
                groups = match.groups()
                pkgs.append(_build_dict(groups, include_latest))

            if include_latest is True:
                logging.warning(
                    "Listing outdated packages is not possible with dpkg"
                )

            self.packages = pkgs

        return self.packages

    def list_outdated(self) -> list[dict[str, str | None]]:
        return self.outdated
