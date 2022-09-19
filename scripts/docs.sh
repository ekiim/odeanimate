#!/usr/bin/env bash
echo "Running Automated testing"
python ./scripts/auto-doc.py ./docs/api odeanimate
[[ "$1" == "serve" ]] && mkdocs serve || mkdocs build
rm -rf ./docs/api
EXIT_CODE=$?
exit ${EXIT_CODE}
