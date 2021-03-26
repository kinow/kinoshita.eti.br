#!/bin/bash
# See: https://superuser.com/questions/275476/square-thumbnails-with-imagemagick-convert

SCRIPT=$(readlink -f "$0")
SCRIPTPATH=$(dirname "$SCRIPT")

### thumbnail generation

# source: https://stackoverflow.com/questions/11265607/how-should-i-batch-make-thumbnails-with-the-original-images-located-in-multiple
make_thumbnail() {
    pic=$1
    thumb=$(dirname "$1")/../thumbs/thumb-$(basename "$1")
    convert "$pic" -thumbnail 400x400 -gravity center -extent 400x400 "$thumb"
}

# Now we need a way to call make_thumbnail on each file.
# The easiest robust way is to restrict on files at level 2, and glob those
# with */*.jpg
# (we could also glob levels 2 and 3 with two globs: */*.jpg */*/*.jpg)

for pic in "${SCRIPTPATH}"/../assets/pages/art/images/*.*
do
    make_thumbnail "$pic"
done

### sprite generation
#
# if python -c 'import PIL; import glue'; then
# 	glue --png8 --scss "${SCRIPTPATH}/_sass/" --url "/assets/pages/art/" --img "${SCRIPTPATH}/assets/pages/art/" "${SCRIPTPATH}/assets/pages/art/thumbs/" "${SCRIPTPATH}/assets/pages/art/"
# 	# FIXME: seems to be a bug in glue!
# 	rm -rf "${SCRIPTPATH}/assets/pages/art/images.css"
# 	exit 0
# else
# 	echo "No pillow or no glue!"
# 	exit 1
# fi
