from pygmy.audiounit import *
import pygmy.audiounit.random_parameters as rp



desc = CAComponentDescription('aumu', 'aut1', 'Alfa')


dir = rp.consts.automat1_aupreset_dir + '/test1'
functions = rp.consts.automat1_functions

chain_group = AUChainGroup()
chain_group.add_audiosource(desc)

au = chain_group.auchains[0].audiosource

for i in range(100):
	rp.randomize_parameters(au, functions)
	au.save_aupreset(dir + '/test_%i.aupreset' % i)
