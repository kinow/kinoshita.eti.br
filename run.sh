#!/bin/bash
DIR=`dirname "$0"`

chef --root=$DIR serve --use-reloader

exit 0
