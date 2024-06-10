import json
from typing import Optional

import typer
from tabulate import tabulate
from typing_extensions import Annotated

from whatinstalled import lua, mac, node, python, ruby, linux  # noqa: F401


app = typer.Typer(add_completion=False)


@app.command()
def main(
    profile: Annotated[
        Optional[str],
        typer.Option(
            help="Select a given profile among this list: mac,linux,python,lua,node,ruby"
        ),
    ] = None,
    include_system: Annotated[
        Optional[bool], typer.Option(help="Include system packages")
    ] = False,
    exclude: Annotated[
        Optional[str],
        typer.Option(help="Exclude given installers separated by a comma"),
    ] = None,
    to_json: Annotated[Optional[bool], typer.Option("--json", help="Output to JSON")] = False,
    to_csv: Annotated[Optional[bool], typer.Option("--csv", help="Output to CSV")] = False,
    output: Annotated[Optional[str], typer.Option(help="Save the output in a file")] = None,
):
    all_pkgs = []

    excluded = []
    if exclude is not None and len(exclude) > 0:
        excluded = exclude.split(",")

    if include_system is False and "system" not in excluded:
        excluded.append("system")

    installers = ["mac", "linux", "python", "lua", "node", "ruby"]

    for installer in installers:
        if (
            (profile is not None and profile.strip() == installer) or profile is None
        ) and ((len(excluded) > 0 and installer not in excluded) or len(excluded) == 0):
            all_pkgs += globals()[installer].all(excluded)

    output_str = ""
    if to_json is True:
        output_str = json.dumps(all_pkgs)
    elif to_csv is True:
        output_str = "name;version;source\n"
        for pkg in all_pkgs:
            output_str += f"{pkg['name']};{pkg['version']};{pkg['source']}\n"
    else:
        output_str = tabulate(all_pkgs)

    if output is not None:
        with open(output, "w") as fp:
            fp.write(output_str)
    else:
        print(output_str)

if __name__ == "__main__":
    typer.run(main)
