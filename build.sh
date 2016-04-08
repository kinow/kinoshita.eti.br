#!/bin/bash
DIR=`dirname "$0"`
./PieCrust/bin/chef --root=$DIR/site purge
./PieCrust/bin/chef --root=$DIR/site bake --config=production --output=blog --force

ghp-import -n -m "Publishing kinoshita.eti.br" -p -r origin -b gh-pages blog 
