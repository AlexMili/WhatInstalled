**WhatInstalled** is a tool to list all packages ever installed on your machine.
Currently these package manager are handled:
- Homebrew
- Macport
- luarocks
- pip
- pipx
- gem
- npm
- yarn
- dpkg
- yum
- dnf

Comming soon:
- aptitude
- pacman
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


╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --profile                                  TEXT  Select a given profile among this list: mac,linux,python,lua,node,ruby [default: None]       │
│ --include-system    --no-include-system          Include system packages [default: no-include-system]                                         │
│ --exclude                                  TEXT  Exclude given installers separated by a comma [default: None]                                │
│ --json                                           Output to JSON                                                                               │
│ --csv                                            Output to CSV                                                                                │
│ --output                                   TEXT  Save the output in a file [default: None]                                                    │
│ --help                                           Show this message and exit.                                                                  │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯


```
