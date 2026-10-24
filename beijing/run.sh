#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
DATA="${1:?Usage: bash run.sh /path/to/beijing_official_inner.zip}"
HDTS_DATA="$DATA" python -m unittest discover -s tests -v
python src/benchmark.py --data "$DATA" --output results
python verify.py --results results
