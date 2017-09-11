#!/usr/bin/env python3

import os
import re

import mirror
import ninja_syntax

dest = os.path.join(mirror.dest_root, 'debdir')


def main():
    n = ninja_syntax.Writer(open('.build.ninja~', 'w'))

    n.variable('root', os.getcwd())
    n.variable('dest', dest)
    n.variable('mirror', mirror.debian)
    if not os.path.isdir(dest):
        os.makedirs(dest)

    n.rule('gen', './gen.py')
    n.build('build.ninja', 'gen', 'gen.py', variables={'generator': 1})

    n.rule('idx', ['./add.sh', '$out', '$in'])

    for line in open('sid.lst'):
        src, ver, dsc = line.strip().split(' ')
        dsc = re.sub('_.*?:', '_', dsc)

        n.build('$dest/{}/{}/debian'.format(src, ver),
                'idx',
                '$mirror/' + dsc,
                implicit='add.sh',
                variables={'description': 'DEB {} {}'.format(src, ver)})

    n.close()
    os.rename('.build.ninja~', 'build.ninja')


if '__main__' == __name__:
    main()
