#!/bin/bash
DIR=`dirname "$0"`
./PieCrust/bin/chef --root=$DIR/site serve --config=live