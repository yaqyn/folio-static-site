#!/bin/sh
set -eu
project_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
exec python3 -m unittest discover -s "$project_dir/src" "$@"
