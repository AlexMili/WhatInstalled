#!/usr/bin/env bash

set -e
set -x

# mypy src/whatinstalled
ruff check src/whatinstalled
