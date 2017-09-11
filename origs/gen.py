#!/usr/bin/env python3

import os

import mirror
import ninja_syntax

dest = os.path.join(mirror.dest_root, 'data')


def main():
    n = ninja_syntax.Writer(open('.build.ninja~', 'w'))

    n.variable('root', os.getcwd())
    n.variable('dest', dest)
    n.variable('mirror', mirror.debian)
    if not os.path.isdir(dest):
        os.makedirs(dest)

    n.rule('gen', './gen.py')
    n.build('build.ninja', 'gen', ['../casync.py', 'origs'], variables={'generator': 1})

    n.rule('idx', ['./add.sh', '$out', '$in', '$dest/default.castr'])

    for dsc in mirror.all_dscs():
        _, src, ver = mirror.read_dsc(dsc)

        if src.startswith('lib'):
            prefix = src[0:4]
        else:
            prefix = src[0]

        n.build('$dest/{}/{}/{}.caidx'.format(prefix, src, ver),
                'idx',
                '$mirror' + dsc,
                implicit='add.sh',
                variables={'description': 'IDX {} {}'.format(src, ver)})

    n.close()
    os.rename('.build.ninja~', 'build.ninja')


if '__main__' == __name__:
    main()
