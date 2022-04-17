#!/bin/sh
[[ "$1" == "CI" ]] && CI_CHECK="--check"
black ./odeanimate ./examples ${CI_CHECK} || exit 1
