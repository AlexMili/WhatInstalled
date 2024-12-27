import logging

from whatinstalled.installers.base import BaseInstaller, execute_command


def _build_dict(x: list[str], include_latest: bool = False) -> dict[str, str | None]:
    data: dict[str, str | None] = {
        "name": x[0],
        "version": x[1],
        "source": "luarocks",
    }

    if include_latest is True:
        data["latest"] = x[1]

    return data


class LuarocksInstaller(BaseInstaller):
    name = "luarocks"
    list_cmd = "luarocks list --porcelain"
    outdated_cmd = "luarocks list --outdated --porcelain"
    available_cmd = "luarocks --version"

    def list_packages(self, include_latest: bool = False) -> list[dict[str, str | None]]:
        pkgs_output = execute_command(self.list_cmd)

        if pkgs_output is not None:
            pkgs: list[dict[str, str | None]] = []
            for pkg in pkgs_output.split("\n"):
                if len(pkg) > 0:
                    info = pkg.split("\t")
                    pkgs.append(_build_dict(info, include_latest))

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
            pkgs: list[dict[str, str | None]] = []
            for pkg in pkgs_outdated.split("\n"):
                if len(pkg) > 0:
                    info = pkg.split("\t")
                    pkgs.append({"name": info[0], "latest_version": info[2]})

            self.outdated = pkgs

        return self.outdated
