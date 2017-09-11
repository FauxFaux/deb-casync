import os

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


# Why do I keep doing this? I hate you, Faux.
def read_dsc(dsc):
    if dsc[0] == '/':
        dsc = dsc[1:]
    with open(os.path.join(debian, dsc)) as d:
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
