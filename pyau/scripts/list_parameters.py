#!/usr/bin/env python
#
#  list_parameters.py
#  
#
#  Created by simon on 17/04/09.
#  Copyright (c) 2009 . All rights reserved.
#

from pygmy.audiounit import *

import sys

def print_usage_and_exit():

    print
    print 'usage:'
    print 'python list_parameters.py <type> <subtype> <manufacturer>'
    print '  prints all the parameters of a certain audio unit'
    print
    print '  example :'
    print '  "python list_audio_units.py aufx "def " appl"'
    print '  WARNING (and TODO!) : only works with type "aumu" for now'

    sys.exit()

if __name__ == '__main__':

    if len(sys.argv) < 4:
        print_usage_and_exit()
        
    type = sys.argv[1]
    if type != 'aumu' and type != 'aufx':
        print 'Error : type has to be "aumu" or "aufx"'
    subtype = sys.argv[2]
    manu = sys.argv[3]

    desc = CAComponentDescription(type, subtype, manu)

    #for now, the way it works, we need to use all the auchaingroup mechanism to get the audiounit which knows the parameters
    acg = AUChainGroup()
    if type == "aumu":
        au = acg.add_audiosource(desc)
    elif type == "aufx":
        acg.add_audiosource(CAComponentDescription("aumu", "dls ", "appl"))
        au = acg.add_effect(desc)
#    print au
    for i,p in enumerate(au.get_parameters()):
        #print "lambda p : %f, # %s" % (p.value, p.name)
        #print ('rp.default, # %i- %s' % (i,p.name)) + ((' (indexed params : %i)' % p.num_indexed_params) if p.num_indexed_params > 0 else (' (%f, %f)' % p.range))
        print p.detailed_str()

        #print 'yes' if p.default_value == p.value else 'non',