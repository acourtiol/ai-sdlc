#!/bin/sh
# Deterministic status router. Run from the product repository root.
# Usage: sh path/to/status.sh [product-repo-root]
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
root=${1:-.}
exec python3 "$script_dir/validator.py" route "$root"
