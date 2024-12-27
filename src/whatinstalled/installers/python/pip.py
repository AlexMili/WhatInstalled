import json
import logging

from whatinstalled.installers.base import BaseInstaller, execute_command


def _build_dict(
    x: dict[str, str], include_latest: bool = False
) -> dict[str, str | None]:
    data: dict[str, str | None] = {
        "name": x["name"],
        "version": x["version"],
        "source": "pip",
    }

    if include_latest is True:
        data["latest"] = x["version"]

    return data


class PipInstaller(BaseInstaller):
    name = "pip"
    list_cmd = "pip list --format json"
    outdated_cmd = "pip list --outdated --format json"
    available_cmd = "pip --version"

    def list_packages(self, include_latest: bool = False) -> list[dict[str, str | None]]:
        pkgs_output = execute_command(self.list_cmd)

        if pkgs_output is not None:
            pkgs = json.loads(pkgs_output)
            pkgs = list(map(lambda x: _build_dict(x, include_latest), pkgs))

            if include_latest is True:
                if len(self.outdated) == 0:
                    self.list_outdated()

                for item in self.outdated:
                    iter = list(filter(lambda x: x["name"] == item["name"], pkgs))
                    if len(iter) > 1:
                        logging.info(
                            f"Multiple packages found with the same name ({item['name']}). Taking the first."
                        )
                    iter[0]["latest"] = item["latest_version"]

            self.packages = pkgs

        return self.packages

    def list_outdated(self) -> list[dict[str, str | None]]:
        pkgs_outdated = execute_command(self.outdated_cmd)

        if pkgs_outdated is not None:
            outdated = json.loads(pkgs_outdated)
            self.outdated = outdated

        return self.outdated
