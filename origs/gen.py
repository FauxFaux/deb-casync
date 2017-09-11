#!/usr/bin/env python3

import os
import re

import ninja_syntax

CLEAN = re.compile('\.orig\.tar\.[a-z0-9]+$')

dest = '/home/deb-casync/data'
mirror = '/home/apt-mirror/mirror/debian.mirrors.ovh.net/debian'


def dscs():
    for root, _, files in os.walk(mirror):
        assert root[0:len(mirror)] == mirror
        root = root[len(mirror):]
        for file in files:
            if file.endswith('.dsc'):
                yield os.path.join(root, file)


def clean(name):
    return re.sub(CLEAN, '', os.path.basename(name))


# Why do I keep doing this? I hate you, Faux.
def read_format(dsc):
    with open(dsc) as d:
        fmt = None
        ver = None
        src = None

        for line in d.readlines():
            if 'Format: 3.0 (quilt)\n' == line:
                fmt = 'q'
            elif 'Format: 3.0 (native)\n' == line:
                fmt = 'n'
            elif 'Format: 1.0\n' == line:
                fmt = '1'
            elif line.startswith('Version: '):
                ver = line[len('Version: '):].strip()
            elif line.startswith('Source: '):
                src = line[len('Source: '):].strip()

            if fmt and ver and src:
                return fmt, src, ver
    raise Exception("Unrecognised source format")


def main():
    n = ninja_syntax.Writer(open('.build.ninja~', 'w'))

    n.variable('root', os.getcwd())
    n.variable('dest', dest)
    n.variable('mirror', mirror)
    if not os.path.isdir(dest):
        os.makedirs(dest)

    n.rule('gen', './gen.py')
    n.build('build.ninja', 'gen', 'gen.py', variables={'generator': 1})

    n.rule('idx', ['./add.sh', '$out', '$in', '$dest/default.castr'])

    for dsc in dscs():
        _, src, ver = read_format(mirror + dsc)

        if src.startswith('lib'):
            prefix=src[0:4]
        else:
            prefix=src[0]

        n.build('$dest/{}/{}/{}.caidx'.format(prefix, src, ver),
                'idx',
                '$mirror' + dsc,
                implicit='add.sh',
                variables={'description': 'IDX {} {}'.format(src, ver)})

    n.close()
    os.rename('.build.ninja~', 'build.ninja')


if '__main__' == __name__:
    main()
