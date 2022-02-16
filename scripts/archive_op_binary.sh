#!/bin/sh -e

SRC_ROOT="$(cd "$(dirname $0)" && dirname "$(pwd)")"
OP_BINARY_PATH="$SRC_ROOT/op-binaries"


get_op_ver(){
    printf "$(/usr/local/bin/op --version)"
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
    echo "Nothing to archive"
fi
