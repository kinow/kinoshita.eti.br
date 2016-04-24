#!/bin/bash
DIR=`dirname "$0"`

chef --root=$DIR serve e-reloader

exit 0
