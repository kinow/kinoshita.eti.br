---
date: 2017-10-14 00:24:54 +1300
layout: post
tags:
- programming
- shell script
- security
- opensource
- apache software foundation
categories:
- blog
title: Quickly Verifying jar Signatures For ASF Releases
---

The release process within the Apache Software Foundation includes a series of steps. Amongst these
steps is the [voting process](https://www.apache.org/foundation/voting.html). In Apache Commons, the
[release instructions](https://commons.apache.org/releases/prepare.html) includes a note on artefact
signatures.

 >During the course of the VOTE, make sure that one or more of the reviewers have verified the signatures and hash files included with the release artifacts. If no one specifically mentions having done that during the VOTE, ask on the dev list and make sure someone does this before you proceed with the release. 

Tired of always having to manually check several artefacts, or having to come up with the correct
shell commands to iterate through a list of files, the other day I wrote a simple script to download
the KEYS file, import it, download all the artefacts, then iterate through them and verify the
signature.

Here's the script. Licensed under the GPL licence.

```shell
#!/usr/bin/env bash

url=""

# From: https://blog.mafr.de/2007/08/05/cmdline-options-in-shell-scripts/
USAGE="Usage: `basename $0` [-hv] https://repository.apache.org/.../commons/commons-configuration/2.2/"

# Parse command line options.
while getopts hv: OPT; do
    case "$OPT" in
        h)
            echo $USAGE
            exit 0
            ;;
        v)
            echo "`basename $0` version 0.0.1"
            exit 0
            ;;
        \?)
            # getopts issues an error message
            echo $USAGE >&2
            exit 1
            ;;
    esac
done

# Remove the switches we parsed above.
shift `expr $OPTIND - 1`

# We want at least one non-option argument. 
# Remove this block if you don't need it.
if [ $# -eq 0 ]; then
    echo $USAGE >&amp;2
    exit 1
fi

# Access additional arguments as usual through 
# variables $@, $*, $1, $2, etc. or using this loop:
URL=$1

echo "url: ${URL}"

# Use a local temporary directory
BUILD_DIR=$(mktemp -d)
pushd "$BUILD_DIR"

echo "build dir: ${BUILD_DIR}"

# Download KEYS file
KEYS_URL=https://www.apache.org/dist/commons/KEYS

echo "importing KEYS from: ${KEYS_URL}"

wget "$KEYS_URL"
gpg --import KEYS

# Download JARs and signature files
echo "downloading all jars and signature files..."

wget -r -nd -np -e robots=off --wait 1 -R "index.html*" "${URL}"

# Check the files
for x in *.jar; do gpg --verify "${x}".asc; done

# EOF
```

The script can be found at GitHub too: [https://github.com/kinow/dork-scripts/tree/3c519a74f28c08310ce2e65f8e860d61fd0c5c07/gpg/asf-sigs](https://github.com/kinow/dork-scripts/tree/3c519a74f28c08310ce2e65f8e860d61fd0c5c07/gpg/asf-sigs)
