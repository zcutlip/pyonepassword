# shellcheck shell=dash
# In shell, success is exit(0), error is anything else, e.g., exit(1)
SUCCESS=0
FAILURE=1

quit(){
    if [ $# -gt 1 ];
    then
        echo "$1"
        shift
    fi
    exit "$1"
}

branch_is_master(){
    _branch=$(git rev-parse --abbrev-ref HEAD)
    if [ "$_branch" = "master" ];
    then
        return $SUCCESS;
    else
        return $FAILURE;
    fi
}

branch_is_clean(){
    _modified=$(git ls-files -m) || quit "Unable to check for modified files." $?
    if [ -z "$_modified" ];
    then
        return $SUCCESS;
    else
        return $FAILURE;
    fi
}

current_version() {
    _version="$(python ./setup.py --version)" || quit "Unable to detect package version" $?
    printf "%s" "$_version"
}

version_is_tagged(){
    _version="$1"
    # e.g., verion = 0.1.0
    # check if git tag -l v0.1.0 exists
    tag_description=$(git tag -l v"$_version")
    if [ -n "$tag_description" ];
    then
        return $SUCCESS;
    else
        return $FAILURE;
    fi
}

prompt_yes_no(){
    prompt_string="$1"
    read -r -p "$prompt_string [Y/n] " response

    case $response in
    [yY][eE][sS]|[yY])
        return $SUCCESS
        ;;
        *)
        return $FAILURE
        ;;
    esac
}

_readlink(){ readlink "$1" || echo "$1"; }

# Don't shadow the 'realpath' executable which may be installed on
# some systems (e.g., via homebrew)
_realpath() { cd "$(dirname "$0")" && _readlink "$(pwd)"/"$(basename "$0")"; }

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
