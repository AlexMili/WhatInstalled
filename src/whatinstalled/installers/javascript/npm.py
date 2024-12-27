import json
import logging
from typing import Any

from whatinstalled.installers.base import BaseInstaller, execute_command


def _build_dict(
    x: str, pkgs: dict[str, Any], include_latest: bool = False
) -> dict[str, str | None]:
    data: dict[str, str | None] = {
        "name": x,
        "version": pkgs["dependencies"][x]["version"],
        "source": "npm",
    }

    if include_latest is True:
        data["latest"] = None

    return data


class NpmInstaller(BaseInstaller):
    name = "npm"
    list_cmd = "npm list -g --depth=0 --json"
    outdated_cmd = "npm outdated -g --json"
    available_cmd = "npm version"

    def list_packages(
        self, include_latest: bool = False
    ) -> list[dict[str, str | None]]:
        pkgs_output = execute_command(self.list_cmd)

        if pkgs_output is not None:
            pkgs_parsed = json.loads(pkgs_output)
            pkgs = list(
                map(
                    lambda x: _build_dict(
                        x, pkgs_parsed, include_latest=include_latest
                    ),
                    pkgs_parsed["dependencies"].keys(),
                )
            )

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
            outdated = json.loads(pkgs_outdated)
            self.outdated = list(
                map(
                    lambda x: {"name": x, "latest_version": outdated[x]["latest"]},
                    outdated,
                )
            )

        return self.outdated
