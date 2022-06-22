#!/bin/sh

# File: deletebranch.sh
# Author: Zachary Cutlip <uid000@gmail.com>
# Purpose: (Relatively) safely delete specified branch from local and origin in one pass

quit(){
    if [ $# -gt 1 ];
    then
        echo "$1"
        shift
    fi
    exit "$1"
}

local_branch_exists() {
    _branch="$1"
    git branch | grep "[:space:]*$_branch$"
    return $?
}

remote_branch_exists() {
    _remote="$1"
    _branch="$2"
    _remote_string="remotes\/$_remote\/$_branch"
    git branch -a | grep "[:space:]*$_remote_string$"
    return $?
}

is_current_branch() {
    _to_delete="$1"
    _branch=$(git rev-parse --abbrev-ref HEAD)
    [ "$_to_delete" = "$_branch" ]
    return $?
}

merged() {
    _to_delete="$1"
    _commit=$(git log "$_to_delete" | head -1)
    git log | grep "$_commit";
    return $?
}

remote_merged() {
    _remote="$1"
    _to_delete="$2"
    _remote_string="remotes/$_remote/$_to_delete"
    _commit=$(git log "$_remote_string" | head -1)
    git log | grep "$_commit";
    return $?
}

to_delete=$1
remote="origin"
if [ $# -gt 1 ];
then
    remote="$2"
fi

if [ -z "$to_delete" ];
then
    quit "Specify a branch to delete" 1
fi

if is_current_branch "$to_delete";
then
    quit "Can't delete current branch: $to_delete" 1
fi

if [ "$to_delete" = "master" ] || [ "$to_delete" = "main" ];
then
    quit "Refusing to delete master or main branch." 1
fi

local_exists=0
remote_exists=0
if local_branch_exists "$to_delete";
then
    local_exists=1
fi
if remote_branch_exists "$remote" "$to_delete";
then
    remote_exists=1
fi

if [ $local_exists -eq 0 ] && [ $remote_exists -eq 0 ];
then
    quit "Neither local nor remote branch exists" 1
fi

if [ $local_exists -gt 0 ];
then
    if ! merged "$to_delete";
    then
        quit "Branch $to_delete appears not to be merged." 1
    fi
elif [ $remote_exists -gt 0 ];
then
    if ! remote_merged "$remote" "$to_delete";
    then
        quit "Remote branch $to_delete appears not to be merged." 1
    fi
fi

echo "Deleting branch $to_delete from local and $remote."

git push -d "$remote" "$to_delete"
ret1=$?
git branch -d "$to_delete"
ret2=$?

[ $ret1 -eq 0 ] && [ $ret2 -eq 0 ]
quit $?
