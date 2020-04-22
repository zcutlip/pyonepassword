#!/bin/sh

quit(){
    if [ $# -gt 1 ];
    then
        echo $1
        shift
    fi
    exit $1
}

branch=$(git rev-parse --abbrev-ref HEAD)
if [ ! $branch == "master" ];
then
    echo 
    quit "Attempting to tag from branch $branch. Check out 'master' first." 1
fi

modified=$(git ls-files -m) || quit "Unable to check for modified files." $?

if [ ! -z "$modified" ];
then
    echo "Tree contains uncommitted modifications:"
    git ls-files -m
    quit 1
fi

version="v$(python ./setup.py --version)" || quit "Unable to detect package version" $?

existing_version=$(git tag -l "$version")

if [ ! -z "$existing_version" ];
then
    echo "Version $version already tagged."
    git tag -l
    quit 1
fi

echo "Tagging version: $version"

git tag -a "$version" -m "version $version" || quit "Failed to tag $version" $?

echo "Tags:"
git tag -l

quit "Done." 0
