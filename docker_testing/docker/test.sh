#!/bin/sh
uname -a
NUM_PROCS="$(nproc)"
export NUM_PROCS

python3 --version
echo "Number of processors: $NUM_PROCS"

cd "$TESTDIR" || exit

if [ -z "$PYTEST_ENV" ];
then
    echo "PYTEST_ENV not set"
    exit 1
fi

tox --parallel--safe-build -e "$PYTEST_ENV" --workdir "$TOX_WORKDIR" -- "$@"
