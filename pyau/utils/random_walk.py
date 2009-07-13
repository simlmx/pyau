#
#  random_walk.py
#  
#
#  Created by simon lemieux on 30/06/09.
#  Copyright (c) 2009 . All rights reserved.
#
from os import listdir
from os.path import join, isdir, islink
from random import shuffle

def random_walk(top, topdown=True, onerror=None):
    """ Like os.walk but randomly.
        Inspired from os.walk.
    """
        
    # We may not have read permission for top, in which case we can't
    # get a list of the files the directory contains.  os.path.walk
    # always suppressed the exception then, rather than blow up for a
    # minor reason when (say) a thousand readable directories are still
    # left to visit.  That logic is copied here.
    try:
        # Note that listdir and error are globals in this module due
        # to earlier import-*.
        names = listdir(top)
    except OSError, err:
        if onerror is not None:
            onerror(err)
        return

    shuffle(names)
    dirs, nondirs = [], []
    for name in names:
        if isdir(join(top, name)):
            dirs.append(name)
        else:
            nondirs.append(name)

    if topdown:
        yield top, dirs, nondirs
    for name in dirs:
        path = join(top, name)
        if not islink(path):
            for x in random_walk(path, topdown, onerror):
                yield x
    if not topdown:
        yield top, dirs, nondirs
    
