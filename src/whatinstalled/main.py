from typing import Optional

import typer
from tabulate import tabulate
from typing_extensions import Annotated

from whatinstalled import lua, mac, node, python, ruby  # noqa: F401


app = typer.Typer(add_completion=False)


@app.command()
def main(
    profile: Annotated[
        Optional[str],
        typer.Option(
            help="Select a given profile among this list: lua,mac,node,python,ruby"
        ),
    ] = None,
    include_system: Annotated[
        Optional[bool], typer.Option(help="Include system packages")
    ] = False,
    exclude: Annotated[
        Optional[str],
        typer.Option(help="Exclude given installers separated by a comma"),
    ] = None,
    json: Annotated[Optional[bool], typer.Option(help="Output to JSON")] = False,
    csv: Annotated[Optional[bool], typer.Option(help="Output to CSV")] = False,
):
    all_pkgs = []

    excluded = []
    if exclude is not None and len(exclude) > 0:
        excluded = exclude.split(",")

    if include_system is False and "system" not in excluded:
        excluded.append("system")

    installers = ["python", "mac", "node", "lua", "ruby"]

    for installer in installers:
        if (
            (profile is not None and profile.strip() == installer) or profile is None
        ) and ((len(excluded) > 0 and installer not in excluded) or len(excluded) == 0):
            all_pkgs += globals()[installer].all(excluded)

    if json is True:
        print(all_pkgs)
    elif csv is True:
        print("name;version;source")
        for pkg in all_pkgs:
            print(f"{pkg['name']};{pkg['version']};{pkg['source']}")
    else:
        print(tabulate(all_pkgs))


if __name__ == "__main__":
    typer.run(main)
