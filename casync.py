#!/usr/bin/env python3

# Dumb wrapper because Python is dumb
import sys

import debdir.gen as dd
import origs.gen as origs

if __name__ == '__main__':
    if 'debdir' == sys.argv[1]:
        dd.main()
    elif 'origs' == sys.argv[1]:
        origs.main()
    else:
        assert False
