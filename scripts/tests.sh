#!/usr/bin/env bash
echo "Running Automated testing"
[[ "$1" == "verbose" ]] && VERBOSE=-v || VERBOSE=-q
coverage run --source odeanimate -m \
    pytest ${VERBOSE} \
    --doctest-modules \
    odeanimate tests
EXIT_CODE=$?
coverage report
exit ${EXIT_CODE}
