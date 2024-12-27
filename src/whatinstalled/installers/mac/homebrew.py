import json
import logging

from whatinstalled.installers.base import BaseInstaller, execute_command


def _build_dict(x: list[str], include_latest: bool = False) -> dict[str, str | None]:
    data: dict[str, str | None] = {
        "name": x[0],
        "version": x[1],
        "latest": None,
        "source": "homebrew",
    }

    if include_latest is True:
        data["latest"] = x[1]

    return data


class HomebrewInstaller(BaseInstaller):
    name = "homebrew"
    list_cmd = "brew list --versions"
    outdated_cmd = "brew outdated --json"
    available_cmd = "brew --version"

    def list_packages(
        self, include_latest: bool = False
    ) -> list[dict[str, str | None]]:
        pkgs_output = execute_command(self.list_cmd)

        if pkgs_output is not None:
            pkgs = []
            for pkg in pkgs_output.split("\n"):
                if len(pkg) > 0:
                    pkgs.append(_build_dict(pkg.split(" "), include_latest))

            if include_latest is True:
                if len(self.outdated) == 0:
                    self.list_outdated()

                for item in self.outdated:
                    item_name = item["name"]
                    # Listing outdated packages give the long name for instance "hashicorp/tap/terraform".
                    # But when listing packages, Homebrew only return "terraform" which is the short name
                    # version. So here we handle that part and use only the short name when encessary.
                    if item["name"] is not None and "/" in item["name"]:
                        item_name = item["name"].split("/")[-1]

                    iter = list(filter(lambda x: x["name"] == item_name, pkgs))
                    if len(iter) > 1:
                        logging.info(
                            f"Multiple packages found with the same name ({item_name}). "
                            "Taking the first."
                        )
                    iter[0]["latest"] = item["latest_version"]

            self.packages = pkgs

        return self.packages

    def list_outdated(self) -> list[dict[str, str | None]]:
        pkgs_outdated = execute_command(self.outdated_cmd)

        if pkgs_outdated is not None:
            outdated = json.loads(pkgs_outdated)
            outdated_formulae = list(
                map(
                    lambda x: {
                        "name": x["name"],
                        "latest_version": x["current_version"],
                    },
                    outdated["formulae"],
                )
            )
            outdated_casks = list(
                map(
                    lambda x: {
                        "name": x["name"],
                        "latest_version": x["current_version"],
                    },
                    outdated["casks"],
                )
            )

            self.outdated = outdated_formulae + outdated_casks

        return self.outdated
