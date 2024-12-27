#!/usr/bin/env bash

set -e
set -x

pytest --cov=whatinstalled --cov-report=xml test/