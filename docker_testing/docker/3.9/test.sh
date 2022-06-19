#!/bin/sh
uname -a
NUM_PROCS="$(nproc)"
export NUM_PROCS

echo "Number of processors: $NUM_PROCS"

cd "$TESTDIR" || exit
tox --parallel--safe-build -e py39 --workdir "$TOX_WORKDIR" -- "$@"
