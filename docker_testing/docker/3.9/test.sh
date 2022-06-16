#!/bin/sh
uname -a
cd "$TESTDIR" || exit
tox --parallel--safe-build -e py39 --workdir "$TOX_WORKDIR" -- "$@"
