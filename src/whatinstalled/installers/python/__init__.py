from whatinstalled.installers.python.pip import PipInstaller
from whatinstalled.installers.python.pipx import PipxInstaller


INSTALLERS = [PipInstaller(), PipxInstaller()]


def list_packages(
    excluded: list[str] = [], include_latest: bool = False
) -> list[dict[str, str | None]]:
    all_pkgs = []

    for installer in INSTALLERS:
        if (len(excluded) > 0 and installer.name not in excluded) or len(excluded) == 0:
            all_pkgs += installer.list_packages(include_latest=include_latest)

    return all_pkgs


def list_installers() -> list[str]:
    installers = []

    for installer in INSTALLERS:
        if installer.is_available() is True:
            installers.append(installer.name)

    return installers
