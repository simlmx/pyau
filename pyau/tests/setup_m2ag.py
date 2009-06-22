from pygmy.audiounit import *

desc = CAComponentDescription('aumu', 'aut1', 'Alfa')
midi = '/Users/simon/tmp/48.mid'

g = AUChainGroup()
au = g.add_audiosource(desc)
m2ag = Midi2AudioGenerator(g)

m2ag.midifile = midi