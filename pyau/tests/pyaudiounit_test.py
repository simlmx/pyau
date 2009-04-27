#
#  pyaudiounit_test.py
#  
#
#  Created by simon on 30/03/09.
#  Copyright (c) 2009 . All rights reserved.
#

""" Test/Example of how works pygmy.audiounit
"""
import sys
from pygmy.audiounit import *


g = AUChainGroup()

print g

aut1 = g.add_audiosource(CAComponentDescription('aumu', 'aut1', 'Alfa'))
fm8 = g.add_audiosource(CAComponentDescription('aumu', 'Nif8', '-NI-'))
fm82 = g.add_audiosource(CAComponentDescription('aumu', 'Nif8', '-NI-'))

print g

m2ag = Midi2AudioGenerator(g)
m2ag.midifile = '/Users/simon/tmp/link.mid'

#m2ag.play()

aut1.load_aupreset('/Users/simon/tmp/test_52.aupreset')
fm8.load_aupreset('/Users/simon/tmp/808.aupreset')
fm82.load_aupreset('/Users/simon/tmp/303.aupreset')

m2ag.play()

g.add_effect(CAComponentDescription('aufx', 'dist', 'appl'), 2)
g.add_effect(CAComponentDescription('aufx', 'dely', 'appl'), 2)

print g

m2ag.play()