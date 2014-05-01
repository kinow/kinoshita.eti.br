#!/bin/bash
DIR=`dirname "$0"`
./PieCrust/bin/chef --root=$DIR/site bake --config=production --output=blog
