#!/bin/sh
set -eu

T=$(mktemp -d --suffix=sync)
trap 'rm -rf '$T EXIT

if ! tar -C $T --strip-components=1 -xf $2; then
    rm -rf $T
    T=$(mktemp -d --suffix=sync)
    # there are things in the archive without a parent directory; so angry
    tar -C $T -xf $2
fi

cd $T

# why are there unreable files? combat-0.8.1
chmod -R u+rX .
casync make --without=2sec-time --without=usec-time --without=read-only --without=unix --without=best $1

