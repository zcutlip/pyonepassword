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
# shellcheck source=./functions.sh
. "$SRC_ROOT"/scripts/functions.sh
OP_BINARY_PATH="$SRC_ROOT/op-binaries"


# not all 'op' packages install to the same place
# so get the actual location where 'op' is installed
get_real_op_path(){
    _realpath "$(which op)"

}

op_path="$(get_real_op_path)"

# some 'macos' op packages install a universal binary,
# some install an architecture specific binary
op_is_universal_binary(){
    _op="$1"
    file "$_op" | grep 'Mach-O universal' >/dev/null
    return $?
}

get_op_arch(){
    _op="$1"
    _arch=""
    if ! op_is_universal_binary "$_op";
    then
        # TODO: This probably only works on macOS
        _arch="$(file "$_op" | awk '{print $NF }')"
    else
        _arch="universal"
    fi
    echo "$_arch"
}

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
    _version="$("$op_path" --version)"
    printf "%s" "$_version"
    unset _version
}

op_ver="$(get_op_ver)"

# make "universal" copy separate from arch-specific copy
op_arch="$(get_op_arch "$op_path")"
op_archive_dir="$OP_BINARY_PATH/$op_ver/$op_arch"

# destination should end up being like
# op-binaries/2.21.0/universal/op, or
# op-binaries/2.21.0/arm64/op, etc.
op_archive_dest="$op_archive_dir/op"


if [ ! -d "$op_archive_dir" ];
then
    mkdir -p "$op_archive_dir";
fi

if [ ! -f "$op_archive_dest" ];
then
    echo "Archiving" "$op_path" "to $op_archive_dir"
    cp "$op_path" "$op_archive_dest";
else
    echo "op $op_ver archive already present"
fi

echo "Checking hashes"
md5check "$op_path" "$op_archive_dest" || quit "Hashes don't match for $op_path vs $op_archive_dest" 1
echo "Hashes match"
