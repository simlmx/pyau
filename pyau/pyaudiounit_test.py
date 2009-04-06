#
#  pyaudiounit_test.py
#  
#
#  Created by simon on 30/03/09.
#  Copyright (c) 2009 . All rights reserved.
#

""" Test/Example of how works pyaudiounit
"""

from pyaudiounit import *

audiosource_desc = CAComponentDescription('aumu', 'Nif8', '-NI-')
effect_desc = CAComponentDescription('aufx', 'dist', 'appl')

print audiosource_desc
print

chain_group = AUChainGroup()
print chain_group
print

chain_group.add_audiosource(audiosource_desc)
#chain_group.add_audiosource(audiosource_desc)

#chain = chain_group.auchains[0]
#chain.add_effect(effect_desc)

#print chain
#print


fm2ag = FileMidi2AudioGenerator(chain_group, 'mid', 'aupreset', 'wav')
fm2ag.generate_audio()
