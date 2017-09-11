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
    n.pool('huge', 1)
    n.pool('medium', 4)

    for dsc_path in mirror.all_dscs():
        dsc = mirror.read_dsc(dsc_path)
        src = dsc['Source']
        ver = dsc['Version']

        total_compressed = sum(int(file['size']) for file in dsc['Files'])

        # Rule of thumb: ~200mb packages expand to 2-3gb.
        # 64gb of ram for 32 cores -> 2gb of cache per core
        if total_compressed > 100*1024*1024:
            pool = 'huge'
        elif total_compressed > 10*1024*1024:
            pool = 'medium'
        else:
            pool = None

        if src.startswith('lib'):
            prefix = src[0:4]
        else:
            prefix = src[0]

        n.build('$dest/{}/{}/{}.caidx'.format(prefix, src, ver),
                'idx',
                '$mirror' + dsc_path,
                implicit='add.sh',
                variables={
                    'description': 'IDX {} {}'.format(src, ver),
                    'pool': pool
                })

    n.close()
    os.rename('.build.ninja~', 'build.ninja')


if '__main__' == __name__:
    main()
