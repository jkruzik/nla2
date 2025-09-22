#!/bin/bash
set -e

if [ $# -lt 1 ]; then
  echo "Usage: $0 file.py"
  exit 1
fi

INPUT_FILE="$1"
NOTEBOOK_FILE="${INPUT_FILE%.*}.ipynb"

jupytext --to notebook "$INPUT_FILE" -o "$NOTEBOOK_FILE"
jupyter nbconvert --to notebook --execute "$NOTEBOOK_FILE" --inplace

