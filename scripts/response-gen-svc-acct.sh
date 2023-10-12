#!/bin/sh -e

_readlink(){ readlink "$1" || echo "$1"; }

# Don't shadow the 'realpath' executable which may be installed on
# some systems (e.g., via homebrew)
_realpath() { _path="$1"; cd "$(dirname "$_path")" && _readlink "$(pwd)"/"$(basename "$_path")"; }

_realscriptpath() {
    _realpath "$0"
}

real_path="$(_realscriptpath)"
SRC_ROOT="$(cd "$(dirname "$real_path")" && dirname "$(pwd)")"

export RESP_GEN_DOT_ENV_FILE="$SRC_ROOT"/dot_env_files/.env_pyonepassword_test_rw

response-generator "$@"
