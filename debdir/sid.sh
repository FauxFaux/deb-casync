#!/bin/zsh
# might be zshisms; read _ sucks.

egrep '^Version: |^Directory: |^Package: ' /home/apt-mirror/mirror/debian.mirrors.ovh.net/debian/dists/sid/*/source/Sources | sed 'N; N; s/\n/ /g' | while read _ pkg _ vers _ dir; do echo $pkg $vers $dir/${pkg}_$vers.dsc; done

