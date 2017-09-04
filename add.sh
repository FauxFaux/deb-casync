#!/bin/sh
set -eu

T=$(mktemp -d --suffix=sync)
trap 'rm -rf '$T EXIT

dpkg-source --extract --no-check --no-copy --skip-debianization $2 $T/src >/dev/null
cd $T/src
rm -rf debian

# why are there unreadable files? combat-0.8.1
chmod -R u+rX .
casync make --without=2sec-time --without=usec-time --without=read-only --without=unix --without=best $1 >/dev/null
