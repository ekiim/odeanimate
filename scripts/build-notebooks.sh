#!/bin/sh
find docs/examples -type f -name '*.ipynb' | \
    xargs -I '{}' jupyter nbconvert --to notebook --inplace --execute {}
