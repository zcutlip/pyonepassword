#!/bin/sh
uname -a
NUM_PROCS="$(nproc)"
export NUM_PROCS

cd /usr/src/testdir || exit

echo "python: $(python3 --version)"
echo "tox: $(tox --version)"
echo "Number of processors: $NUM_PROCS"
echo "User: $(whoami)"
echo "Path: $PATH"


cd "$TESTDIR" || exit

if [ -z "$PYVER_FACTOR" ];
then
    echo "PYVER_FACTOR not set"
    exit 1
fi
set -x
tox p -f "$PYVER_FACTOR"-pytest --workdir "$TOX_WORKDIR" -- "$@"
