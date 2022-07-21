#!/bin/sh
PYLINT_DISABLE="R0801,C,R0913,R0914"
pylint odeanimate examples tests --disable $${PYLINT_DISABLE}
exit 0
