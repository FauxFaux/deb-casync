#!/bin/sh
set -eu

T=$(mktemp -d --suffix=sync)
trap 'rm -rf '${T} EXIT

# --no-check here skips signature checking, for performance. This is expected to be run on a local, trusted mirror.
dpkg-source --extract --no-check --no-copy --skip-debianization $2 ${T}/src >/dev/null
cd ${T}/src
rm -rf debian

# normalise permissions, to simulate git, and to ensure we can read files
# this is, I believe, a common default umask.
chmod -R u=rwX,g=rX,o=rX .

# attempt to remove all metadata except permissions
# check with make --verbose
# see also https://github.com/systemd/casync/issues/81
casync make \
    --without=best \
    --without=2sec-time --without=sec-time --without=usec-time \
    --without=read-only \
    --without=16bit-uids \
    $1 >/dev/null
