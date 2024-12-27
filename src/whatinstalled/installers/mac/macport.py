import logging
import re

from whatinstalled.installers.base import BaseInstaller, execute_command


def _build_dict(x: list[str], include_latest: bool = False) -> dict[str, str | None]:
    data: dict[str, str | None] = {
        "name": x[0],
        "version": x[1].replace("@", ""),
        "source": "macport",
    }

    if include_latest is True:
        data["latest"] = x[1].replace("@", "")

    return data


class MacportInstaller(BaseInstaller):
    name = "macport"
    list_cmd = "port installed"
    outdated_cmd = "port outdated"
    available_cmd = "port version"

    def list_packages(
        self, include_latest: bool = False
    ) -> list[dict[str, str | None]]:
        pkgs_output = execute_command(self.list_cmd)

        if pkgs_output is not None:
            pkgs = []
            for pkg in pkgs_output.split("\n"):
                if len(pkg) > 0 and "@" in pkg:
                    info = pkg.strip().split(" ")
                    pkgs.append(_build_dict(info, include_latest=include_latest))

            if include_latest is True:
                if len(self.outdated) == 0:
                    self.list_outdated()

                for item in self.outdated:
                    iter = list(filter(lambda x: x["name"] == item["name"], pkgs))
                    if len(iter) > 1:
                        logging.info(
                            f"Multiple packages found with the same name ({item['name']})."
                            " Taking the first."
                        )
                    iter[0]["latest"] = item["latest_version"]

            self.packages = pkgs

        return self.packages

    def list_outdated(self) -> list[dict[str, str | None]]:
        pkgs_outdated = execute_command(self.outdated_cmd)
        outdated = []

        if pkgs_outdated is not None:
            regex = r"([^\s]*)\s+([^\s]*) < ([^\s]*)"
            matches = re.finditer(regex, pkgs_outdated, re.MULTILINE)

            for _, match in enumerate(matches, start=1):
                groups = match.groups()
                outdated.append({"name": groups[0], "latest_version": groups[2]})

            self.outdated = outdated

        return self.outdated
