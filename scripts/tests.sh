#!/usr/bin/env bash
echo "Running Automated testing"
pytest 
EXIT_CODE=$?
exit ${EXIT_CODE}
