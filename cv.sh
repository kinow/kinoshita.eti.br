#!/bin/bash
DIR=`dirname "$0"`

# Generate CV
pushd cv
make deploy
popd

exit 0
