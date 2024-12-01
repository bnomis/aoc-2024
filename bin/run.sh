#!/usr/bin/env bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# shellcheck disable=1091
source "$SCRIPT_DIR"/activate.sh

PARENT_DIR="$( dirname "$SCRIPT_DIR" )"

"$PARENT_DIR"/src/aoc/run.py
