#!/usr/bin/env bash
echo "Running Automated testing"
ln README.md docs/index.md
python ./scripts/auto-doc.py ./docs/api odeanimate
[[ "$1" == "serve" ]] \
    && mkdocs serve --watch odeanimate/ \
    || mkdocs build
rm -rf ./docs/api ./docs/index.md
EXIT_CODE=$?
exit ${EXIT_CODE}
