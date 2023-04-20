#!/bin/sh
./scripts/clean-notebooks.sh
find . -name "__pycache__" -type d | xargs rm -rf
find . -name ".DS_Store" -type f| xargs rm -rf
rm -rf \
    site \
    docs/api \
    .pytest_cache \
    .ipynb_checkpoints \
    build \
    dist \
    .coverage*
