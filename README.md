**WhatInstalled** is a tool to list all packages you ever installed on your machine.
Currently these package manager are handled:
- Homebrew
- Macport
- luarocks
- pip
- pipx
- gem
- npm
- yarn

Comming soon:
- apt-get
- aptitude
- yum
- pacman
- dpkg
- dnf
- zypper
- easy_install
- rvm
- nvm

## Installation
You can install it with pip :
```bash
pip install whatinstalled
```
Or clone this repository and simply run :
```bash
cd whatinstalled/
pip install -e .
```

## Usage

```console
$ whatinstalled --help
Usage: main.py [OPTIONS]

╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --profile                                  TEXT  Select a given profile among this list: lua,mac,node,python,ruby [default: None]                                               │
│ --include-system    --no-include-system          Include system packages [default: no-include-system]                                                                           │
│ --exclude                                  TEXT  Exclude given installers separated by a comma [default: None]                                                                  │
│ --json              --no-json                    Output to JSON [default: no-json]                                                                                              │
│ --csv               --no-csv                     Output to CSV [default: no-csv]                                                                                                │
│ --help                                           Show this message and exit.                                                                                                    │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
