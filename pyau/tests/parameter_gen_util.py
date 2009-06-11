# this is used to study with random generated presets
import sys
import numpy as N
import pylab as P

from pygmy.audiounit import *
import pygmy.audiounit.random_parameters as rp
P.ion()

desc = CAComponentDescription('aumu', 'aut1', 'Alfa')

midi = '/Users/simon/tmp/48.mid'

g = AUChainGroup()
au = g.add_audiosource(desc)

m2ag = Midi2AudioGenerator(g)

save_dir = '/Users/simon/Library/Audio/Presets/' + au.manu + '/' + au.name + '/test2'

m2ag.midifile = midi

def generate_preset():
	rp.randomize_parameters(au, rp.consts.automat1_functions)
	m2ag.play()
	data = m2ag.bounce()[0]
	P.figure(0)
	P.clf()
	P.subplot(211)
	P.plot(data[:5000])
	P.subplot(212)
	P.plot(N.abs(N.fft.rfft(data))[:5000])
	
#generate_preset()

#def play():
#	m2ag.play()
	
def save_preset(name):
	if not name.endswith('.aupreset'):
		name += '.aupreset'
	au.save_aupreset(save_dir + '/name')
	
compte = 0
def save_preset_compteur():
	global compte
	au.save_aupreset(save_dir + ('/%i.aupreset' % compte))
	compte+=1