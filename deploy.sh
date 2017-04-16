#!/bin/bash
DIR=$(dirname "$0")

chef --root="$DIR" purge
chef --root="$DIR" bake --output=blog --force
cp "$DIR/CNAME" "$DIR/blog/"
cp "$DIR/favicon.ico" "$DIR/blog/"

ghp-import -n -m "Publishing kinoshita.eti.br" -p -r origin -b gh-pages blog 
