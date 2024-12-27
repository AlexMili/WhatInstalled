import json
import logging
import os
import subprocess

from whatinstalled.installers.base import BaseInstaller, execute_command


def _build_dict(name: str, include_latest: bool = False) -> dict[str, str | None]:
    # Some packages start with an "@" but the "@" is also
    # the way to separate version number with package name on node.
    # Skipping the first character allow to only get the "@" to separate the
    # version number
    idx: int = name[1:].index("@")
    data: dict[str, str | None] = {
        "name": name[0 : idx + 1],
        "version": name[idx + 2 :],
        "source": "yarn",
    }

    if include_latest is True:
        data["latest"] = data["version"]

    return data


class YarnInstaller(BaseInstaller):
    name = "yarn"
    list_cmd = "yarn list --json --depth=0 --no-progress --cwd {path}"
    outdated_cmd = "yarn outdated --json --depth=0 --no-progress --cwd {path}"
    available_cmd = "yarn --version"

    def __init__(self, path: str):
        super().__init__()

        if path is None:
            logging.error(
                "Yarn is not intended to be used globally. "
                "Please provide a path where you installed packages."
            )

        if os.path.exists(path) is True:
            self.path = path
        else:
            logging.error(f"{path} doesn't exists (Yarn installer)")

    def list_packages(
        self, include_latest: bool = False
    ) -> list[dict[str, str | None]]:
        pkgs_output = execute_command(self.list_cmd.replace("{path}", f"'{self.path}'"))

        if pkgs_output is not None:
            pkgs_parsed = json.loads(pkgs_output)

            pkgs = []
            for elt in pkgs_parsed["data"]["trees"]:
                pkgs.append(_build_dict(elt["name"], include_latest=include_latest))

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
        # For some reason, yarn outdated always return exit code 1
        pkgs_outdated = execute_command(
            self.outdated_cmd.replace("{path}", f'"{self.path}"'),
            stderr=subprocess.STDOUT,
            return_stderr=True,
        )

        if pkgs_outdated is not None:
            if pkgs_outdated[-1:] == "\n":
                pkgs_outdated = pkgs_outdated[:-1]
            # Only the last line contains the data we are looking for
            outdated = json.loads(pkgs_outdated.split("\n")[-1])
            self.outdated = list(
                map(
                    lambda x: {"name": x[0], "latest_version": x[3]},
                    outdated["data"]["body"],
                )
            )

        return self.outdated
