#!/bin/bash
DIR=`dirname "$0"`

# Generate CV
#pushd cv
#make deploy
#popd

chef --root=$DIR serve --use-reloader

exit 0
