#!/usr/bin/env bash
jupyter nbconvert --clear-output --inplace $(find examples/ -name '*.ipynb')