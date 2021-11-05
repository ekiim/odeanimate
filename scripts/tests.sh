#!/bin/sh
echo "Running Automated testing"
python -m doctest \
    $(find odeanimate -type f -name '*.py') \
    && printf "\tDoctest\tPASS\n"

echo "Building Examples"
find examples -type f -name '*.py' \
    | sed -E 's/\//./g' | sed -E 's/.py//g'  \
    | xargs -I {} python -m {}
