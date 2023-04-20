#!/bin/sh
./scripts/tests.sh || exit 1
python -m build
