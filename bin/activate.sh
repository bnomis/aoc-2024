#!/usr/bin/env bash
ROOT_BIN_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
ROOT_DIR="$( dirname "$ROOT_BIN_DIR" )"

if [ -z ${PYTHONPATH+x} ]; then
    export PYTHONPATH=$ROOT_DIR/src
else
    export PYTHONPATH=$ROOT_DIR/src:$PYTHONPATH
fi
