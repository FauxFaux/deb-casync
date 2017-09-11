#!/bin/sh
set -eu

T=$(mktemp -d --suffix=sync)
trap 'rm -rf '${T} EXIT

if [ "$4" = "origs" ]; then
    skip=yes
elif [ "$4" = "debdir" ]; then
    # skip=no
    if [ -d "${1}" ]; then
        exit 0
    fi
else
    exit 1
fi

# --no-check here skips signature checking, for performance. This is expected to be run on a local, trusted mirror.
dpkg-source --extract --no-check --no-copy ${skip+--skip-debianization} "${2}" "${T}/src" >/dev/null
cd ${T}/src

if [ "$4" = "origs" ]; then
    rm -rf debian
elif [ "$4" = "debdir" ]; then
    cd debian
else
    exit 1
fi

# normalise permissions, to simulate git, and to ensure we can read files
# this is, I believe, a common default umask.
chmod -R u+rwX,g=u,o=rX .

mkdir -p "$(dirname "$1")"

# attempt to remove all metadata except permissions
# check with make --verbose
# see also https://github.com/systemd/casync/issues/81
casync make \
    --store=$3 \
    --without=best \
    --without=2sec-time --without=sec-time --without=usec-time \
    --without=read-only \
    --without=16bit-uids \
    $1 >/dev/null
