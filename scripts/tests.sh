#!/bin/sh
echo "Running Automated testing"
REPORT_DIR=docs/tests
bash scripts/clean.sh
coverage run -m pytest \
    --tb=line \
    --doctest-modules \
    -v odeanimate \
    --html ${REPORT_DIR}/results/doctest.html \
    --self-contained-html

EXIT_CODE_DOCTEST=$?

# Reporting Phase
coverage report
mkdir -p ${REPORT_DIR}/coverage
coverage html -d ${REPORT_DIR}/coverage --title="Coverage Report"
# Resolving exit code
[[ ${EXIT_CODE_DOCTEST} -ne 0 ]] && exit 1
exit 0
