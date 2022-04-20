#!/bin/sh -e

. "$(dirname "$0")"/functions.sh
real_path="$(_realpath "$0")"
SRC_ROOT="$(cd "$(dirname "$real_path")" && dirname "$(pwd)")"
OP_BINARY_PATH="$SRC_ROOT/op-binaries"

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
    echo "Archive alredy present"
fi

echo "Checking hashes"
md5check /usr/local/bin/op "$OP_BINARY_PATH/$op_ver/op" || quit "Hashes don't match for /usr/local/bin/op vs $OP_BINARY_PATH/$op_ver/op" 1
echo "Hashes match"
