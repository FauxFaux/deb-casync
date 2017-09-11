#!/bin/sh
set -eu

if [ -d "${1}" ]; then
    exit 0
fi

T=$(mktemp -d --suffix=sync -p /home/deb-casync/debdir)
trap 'rm -rf '"${T}" EXIT

# --no-check here skips signature checking, for performance. This is expected to be run on a local, trusted mirror.
dpkg-source --extract --no-check --no-copy "${2}" "${T}/src" >/dev/null
cd "${T}/src"
chmod u+rX -R debian
mkdir -p "${1}"
if [ -d debian ]; then
    mv -T debian "${1}"
else
    touch "${1}.wtf"
fi

