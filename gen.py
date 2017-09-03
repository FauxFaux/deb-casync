#!/usr/bin/env python3

import os
import re
import ninja_syntax

CLEAN=re.compile('\.orig\.tar\.[a-z0-9]+$')

dest = '/mnt/data/deb-casync'
mirror = '/mnt/data/sources/mirror/deb.debian.org/debian'

def origs():
    for root, _, files in os.walk(mirror):
        assert root[0:len(mirror)] == mirror
        root = root[len(mirror):]
        for file in files:
            if '.orig.' in file and not file.endswith('.asc'):
                yield os.path.join(root, file)

def clean(name):
    return re.sub(CLEAN, '', os.path.basename(name))

def main():
    n = ninja_syntax.Writer(open('.build.ninja~', 'w'))

    n.variable('root', os.getcwd())
    n.variable('dest', dest)
    n.variable('mirror', mirror)
    if not os.path.isdir(dest):
        os.makedirs(dest)

    n.rule('gen', './gen.py')
    n.build('build.ninja', 'gen', 'gen.py', variables={'generator': 1})

    n.rule('idx', ['./add.sh', '$out', '$in'])
    for orig in origs():
        n.build('$dest/{}.caidx'.format(clean(orig)), 'idx', '$mirror' + orig, implicit='add.sh')

    n.close()
    os.rename('.build.ninja~', 'build.ninja')

if '__main__' == __name__:
    main()

