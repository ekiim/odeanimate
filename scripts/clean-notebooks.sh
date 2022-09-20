#!/usr/bin/env bash
jupyter nbconvert --clear-output --inplace $(find docs/ -name '*.ipynb')
