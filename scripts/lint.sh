#!/bin/sh
[[ "$1" == "CI" ]] \
    && CI_CHECK_BLACK="--check"
echo "black"
black ./odeanimate ./examples ${CI_CHECK_BLACK}
EXIT_CODE_BLACK=$?

echo "pylint"
PYLINT_DISABLE="R0801,C,R0913,R0914"
pylint ./odeanimate ./examples --disable ${PYLINT_DISABLE}
# EXIT_CODE_PYLINT=$?
# For now this won't be a blocker for PRs.
EXIT_CODE_PYLINT=0

[[ "${EXIT_CODE_BLACK}" != "0" ]] \
    || [[ "${EXIT_CODE_PYLINT}" != "0" ]] \
    && exit 1
exit 0