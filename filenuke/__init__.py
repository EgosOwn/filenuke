#!/usr/bin/env python3

import sys
import os

import nuke

if __name__ == "__main__":
    try:
        path_to_del = sys.argv[1]
    except IndexError:
        sys.exit(1)
    if os.path.isfile(path_to_del):
        nuke.clean(path_to_del)
    else:
        nuke.clean_tree(path_to_del)
    print(f'Overwrote and deleted {path_to_del}')

