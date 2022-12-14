#!/bin/sh -e

_readlink(){ readlink "$1" || echo "$1"; }

# Don't shadow the 'realpath' executable which may be installed on
# some systems (e.g., via homebrew)
_realpath() { cd "$(dirname "$0")" && _readlink "$(pwd)"/"$(basename "$0")"; }
real_path="$(_realpath "$0")"
SRC_ROOT="$(cd "$(dirname "$real_path")" && dirname "$(pwd)")"
# shellcheck source=./functions.sh
. "$SRC_ROOT"/scripts/functions.sh
OP_BINARY_PATH="$SRC_ROOT/op-binaries"

md5check(){
    _file1="$1"
    _file2="$2"
    hash1="$(md5sum "$_file1" | awk '{ print $1 }')"
    hash2="$(md5sum "$_file2" | awk '{ print $1 }')"
    [ "$hash1" = "$hash2" ]
    ret=$?
    if [ $ret -ne 0 ];
    then
        echo "$hash1"
        echo "$hash2"
    fi
    return $ret
}

get_op_ver(){
    _version="$(/usr/local/bin/op --version)"
    printf "%s" "$_version"
    unset _version
}

op_ver="$(get_op_ver)"

if [ ! -d "$OP_BINARY_PATH/$op_ver" ];
then
    mkdir -p "$OP_BINARY_PATH/$op_ver";
fi

if [ ! -f "$OP_BINARY_PATH/$op_ver/op" ];
then
    echo "Archiving" "$(which op)" "to $OP_BINARY_PATH/$op_ver/"
    cp "$(which op)" "$OP_BINARY_PATH/$op_ver/op";
else
    echo "op $op_ver archive already present"
fi

echo "Checking hashes"
md5check /usr/local/bin/op "$OP_BINARY_PATH/$op_ver/op" || quit "Hashes don't match for /usr/local/bin/op vs $OP_BINARY_PATH/$op_ver/op" 1
echo "Hashes match"
