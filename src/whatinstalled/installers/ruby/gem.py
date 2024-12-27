import logging

from whatinstalled.installers.base import BaseInstaller, execute_command


def _build_dict(x: list[str], include_latest: bool = False) -> dict[str, str | None]:
    version: str = x[1].replace("default: ", "").replace("(", "").replace(")", "")
    data: dict[str, str | None] = {"name": x[0], "version": version, "source": "gem"}

    if include_latest is True:
        data["latest"] = data["version"]

    return data


class GemInstaller(BaseInstaller):
    name = "gem"
    list_cmd = "gem query --local"
    outdated_cmd = "gem outdated --local"
    available_cmd = "gem --version"

    def list_packages(
        self, include_latest: bool = False
    ) -> list[dict[str, str | None]]:
        pkgs_output = execute_command(self.list_cmd)

        if pkgs_output is not None:
            pkgs = []
            for pkg in pkgs_output.split("\n"):
                if len(pkg) > 0 and "(" in pkg and ")" in pkg:
                    info = pkg.split(" ")
                    pkgs.append(_build_dict(info, include_latest=include_latest))

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
        outdated: list[dict[str, str | None]] = []

        if pkgs_outdated is not None:
            for line in pkgs_outdated.split("\n"):
                if len(line) > 0:
                    info = line.split(" (")
                    pkg = info[1].replace(")", "")
                    versions = pkg.split(" < ")
                    outdated.append({"name": info[0], "latest_version": versions[1]})

        self.outdated = outdated

        return self.outdated
