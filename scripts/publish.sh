#!/bin/sh
echo $PWD
./scripts/clean.sh || exit 1
./scripts/build.sh || exit 1
twine \
    upload \
    -u __token__ \
    -p ${PYPI_TOKEN} \
    --non-interactive \
    dist/*
echo "Published"
