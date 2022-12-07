#!/bin/sh
uname -a
NUM_PROCS="$(nproc)"
export NUM_PROCS

python3 --version
echo "Number of processors: $NUM_PROCS"

cd "$TESTDIR" || exit

if [ -z "$PYVER_FACTOR" ];
then
    echo "PYVER_FACTOR not set"
    exit 1
fi
set -x
tox p -f "$PYVER_FACTOR" --workdir "$TOX_WORKDIR" -- "$@"
