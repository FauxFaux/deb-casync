import os
import debian.deb822 as deb822

#export MIRROR=/mnt/data/sources/mirror/deb.debian.org/debian
debian = os.getenv('MIRROR')
dest_root = os.getenv('DEST')

assert debian
assert dest_root


def all_dscs():
    for root, _, files in os.walk(debian):
        assert root[0:len(debian)] == debian
        root = root[len(debian):]
        for file in files:
            if file.endswith('.dsc'):
                yield os.path.join(root, file)


def read_dsc(dsc):
    if dsc[0] == '/':
        dsc = dsc[1:]
    with open(os.path.join(debian, dsc)) as d:
        return deb822.Dsc(d)
