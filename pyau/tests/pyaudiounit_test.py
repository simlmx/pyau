#
#  pyaudiounit_test.py
#  
#
#  Created by simon on 30/03/09.
#  Copyright (c) 2009 . All rights reserved.
#

""" Test/Example of how works pygmy.audiounit
"""

from pygmy.audiounit import *

desc_ins = CAComponentDescription('aumu', 'aut1', 'Alfa')
desc_ins2 = CAComponentDescription('aumu', 'Nif8', '-NI-')
dist_desc = CAComponentDescription('aufx', 'dist', 'appl')
delay_desc = CAComponentDescription('aufx', 'dely', 'appl')

group = AUChainGroup()

ins1 = group.add_audiosource(desc_ins)
ins2 = group.add_audiosource(desc_ins2)

m2ag = Midi2AudioGenerator(group)
m2ag.midifile = '/Users/simon/tmp/awesome_midi.mid'

ins1.load_aupreset('/Users/simon/tmp/test_82.aupreset')
ins2.load_aupreset('/Users/simon/tmp/303.aupreset')

m2ag.play()

eff = group.add_effect(delay_desc, 0)
eff.load_aupreset('/Users/simon/tmp/delay.aupreset')

eff2 = group.add_effect(dist_desc, 1)
eff2.load_aupreset('/Users/simon/tmp/dist.aupreset')

m2ag.play()
