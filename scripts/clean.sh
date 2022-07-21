#!/bin/sh
find . -name "__pycache__" | xargs rm -rf
rm -rf docs/tests/coverage docs/tests/results
