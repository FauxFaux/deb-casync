#!/bin/zsh

set -eu

vfiles() {
    for s in ? lib?; do (
        cd $s
        for p in *(on/); do (
            cd $p
            a=(*.caidx(on))
            echo $p ${a%%.caidx}
        ) done
    ) done
}
