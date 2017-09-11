#!/usr/bin/env python3
import multiprocessing
import sys

import os

import mirror
import ninja_syntax


def ninja(thing):
    n = ninja_syntax.Writer(open('.build.ninja~', 'w'))

    dest = os.path.join(mirror.dest_root, thing)

    n.variable('root', os.getcwd())
    n.variable('dest', dest)
    n.variable('thing', thing)
    n.variable('mirror', mirror.debian)
    if not os.path.isdir(dest):
        os.makedirs(dest)

    n.rule('gen', ['../casync.py', '$thing'])
    n.build('build.ninja', 'gen', '../casync.py', variables={'generator': 1})

    n.rule('idx', ['../add-to-sync.sh', '$out', '$in', '$dest/default.castr', '$thing'])

    # 8/8 + 1 = 2 on a quad-core with hyperthreading
    # 32/8 + 1 = 5 on a 32vCPU instance

    n.pool('huge', int(multiprocessing.cpu_count() / 8) + 1)
    n.pool('medium', int(multiprocessing.cpu_count() / 4) + 1)

    for dsc_path in mirror.all_dscs():
        dsc = mirror.read_dsc(dsc_path)
        src = dsc['Source']
        ver = dsc['Version']

        total_compressed = sum(int(file['size']) for file in dsc['Files'])

        # Rule of thumb: ~200mb packages expand to 2-3gb.
        # 64gb of ram for 32 cores -> 2gb of cache per core
        if total_compressed > 100 * 1024 * 1024:
            pool = 'huge'
        elif total_compressed > 10 * 1024 * 1024:
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
                implicit='../add-to-sync.sh',
                variables={
                    'description': '{} {} {}'.format(thing, src, ver),
                    'pool': pool
                })

    n.close()
    os.rename('.build.ninja~', 'build.ninja')


if __name__ == '__main__':
    ninja(sys.argv[1])
