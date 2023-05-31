#!/bin/sh

if [ -z "$PYONEPASSWORD_BASELINE" ];
then
    echo "PYONEPASSWORD_BASELINE environment variable must be set"
    exit 1
fi

if [ -z "$1" ];
then
    echo "api module argument required"
    exit 1
fi

api_module="$1"

diffogram(){
    git --no-pager diff --no-index --histogram "$1" "$2"
}

diffogram "${PYONEPASSWORD_BASELINE}/pyonepassword/api/$api_module.py" "$(pwd)/pyonepassword/pyonepassword/api/$api_module.py"
