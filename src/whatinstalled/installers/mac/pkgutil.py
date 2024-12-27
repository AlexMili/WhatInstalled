import logging

from whatinstalled.installers.base import BaseInstaller, execute_command


def _build_dict(x: str, include_latest: bool = False) -> dict[str, str | None]:
    data = {
        "name": x,
        "version": None,
        "source": "pkgutil",
    }

    if include_latest is True:
        data["latest"] = None

    return data


class PkgutilInstaller(BaseInstaller):
    name = "pkgutil"
    list_cmd = "pkgutil --pkgs"
    outdated_cmd = "echo '[]'"
    available_cmd = "pkgutil --pkgs"

    def list_packages(self, include_latest: bool = False) -> list[dict[str, str | None]]:
        pkgs_output = execute_command(self.list_cmd)

        if pkgs_output is not None:
            pkgs = []
            for pkg in pkgs_output.split("\n"):
                if len(pkg) > 0:
                    pkgs.append(_build_dict(pkg, include_latest=include_latest))

            if include_latest is True:
                logging.warning("Listing outdated packages is not possible with pkgutil")

            self.packages = pkgs

        return self.packages

    def list_outdated(self) -> list[dict[str, str | None]]:
        return self.outdated
