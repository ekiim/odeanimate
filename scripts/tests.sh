#!/bin/sh
#echo "Running Automated testing"
REPORT_DIR=docs/tests
bash scripts/clean.sh
coverage run -m pytest \
    --tb=line \
    --doctest-modules \
    -v odeanimate \
    --html ${REPORT_DIR}/results/doctest.html \
    --self-contained-html

echo "Runing Examples"
while read f ; do 
    echo $f
    coverage run -m $(echo $f | sed -e 's/\//./g;s/\.py$//g') 012 > /dev/null & 
done < <(ls -1 examples/*.py )
wait

DOCTEST_EXIT_CODE=$?
# Reporting Phase
coverage report
mkdir -p ${REPORT_DIR}/coverage
coverage html -d ${REPORT_DIR}/coverage --title="Coverage Report"
# Resolving exit code
[[ ${DOCTEST_EXIT_CODE} -ne 0 ]] && exit 1
exit 0
