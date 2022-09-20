#!/usr/bin/env bash
echo "Running Automated testing"
[[ "$1" == "verbose" ]] && VERBOSE=-v || VERBOSE=-q
coverage run --source odeanimate -m \
    pytest ${VERBOSE} \
    --doctest-modules \
    odeanimate tests
EXIT_CODE=$?
[[ "${EXIT_CODE}" == "0" ]] && coverage report
coverage json -o .coverage.json
exit ${EXIT_CODE}
