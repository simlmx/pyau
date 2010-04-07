#
# created by simon lemieux
# june 2009
# edited april 2010
#
# Recursive cleaning of files ending with something
# Maybe there's some cleaner command line way to do this...

import sys
from os import remove#, walk
from random_walk import random_walk
from os.path import join


def die_with_usage():
    print 'usage : python clean_files.py suffix directory'
    print 'delete recursively all files ending by "suffix" in directory'
    print 'example : python clean_lock_files.py [-v] .pdf my_dir'
    print '          will delete all *.pdf files recursively in my_dir'
    sys.exit()

if __name__ == '__main__':
    nb_min_args = 3
    if len(sys.argv) < nb_min_args:
        die_with_usage()
    if sys.argv[1] == '-v':
        verbose = True
        sys.argv.pop(1)
    else:
        verbose = False
        
    suffix = sys.argv[1]
    dir = sys.argv[2]

    for root, dirs, files in random_walk(dir):
        for f in files:
            if f.endswith(suffix):
                path = join(root, f)
                remove(path)
                if verbose:
                    print 'removed %s' % path
           
