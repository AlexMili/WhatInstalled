import logging
import re

from whatinstalled.installers.base import BaseInstaller, execute_command


def _build_dict(x: str, include_latest: bool = False) -> dict[str, str | None]:
    data = {"name": x[0], "version": x[1], "source": "dnf"}

    if include_latest is True:
        data["latest"] = None

    return data


class DnfInstaller(BaseInstaller):
    name = "dnf"
    list_cmd = "dnf list installed"
    outdated_cmd = "dnf list updates"
    available_cmd = "dnf --version"

    def list_packages(self, include_latest: bool = False) -> list[dict[str, str | None]]:
        pkgs_output = execute_command(self.list_cmd)

        if pkgs_output is not None:
            pkgs = []

            regex = r"([^\s]+)\s+([^\s]+)\s+([^\s]*)\n"
            matches = re.finditer(regex, pkgs_output, re.MULTILINE)

            pkgs = []
            for _, match in enumerate(matches, start=1):
                groups = match.groups()
                pkgs.append(_build_dict(groups, include_latest))

            if include_latest is True:
                if len(self.outdated) == 0:
                    self.list_outdated()

                for item in self.outdated:
                    iter = list(filter(lambda x: x["name"] == item["name"], pkgs))
                    if len(iter) > 1:
                        logging.info(
                            f"Multiple packages found with the same name ({item['name']}). "
                            "Taking the first."
                        )
                    iter[0]["latest"] = item["latest_version"]

            self.packages = pkgs

        return self.packages

    def list_outdated(self) -> list[dict[str, str | None]]:
        pkgs_outdated = execute_command(self.outdated_cmd)

        if pkgs_outdated is not None:
            regex = r"([^\s]+)\s+([^\s]+)\s+(updates)\n"
            matches = re.finditer(regex, pkgs_outdated, re.MULTILINE)

            for _, match in enumerate(matches, start=1):
                groups = match.groups()
                self.outdated.append({"name": groups[0], "latest_version": groups[1]})

        return self.outdated
