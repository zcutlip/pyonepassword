#!/bin/sh
uname -a
cd "$TESTDIR" || exit
tox --parallel--safe-build -e py38 --workdir "$TOX_WORKDIR" -- "$@"
