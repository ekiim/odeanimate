#! /usr/bin/env bash
which docker
[[ "$?" != "0" ]] && "Make sure docker is installed." && exit 1
docker build --no-cache -t odeanimate:dev -f scripts/Dockerfile .
[[ "$?" != "0" ]] && "For some reason the build fail." && exit 1
