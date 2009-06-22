# this is used to study with random generated presets
import sys, os
import numpy as N
import pylab as P

#from pygmy.audiounit import *
import pygmy.audiounit.random_parameters as rp
from pygmy.audiounit.normalize_volume import normalize_volume
P.ion()

verbose = True

from setup_m2ag import *


load_dir = '/Users/simon/Library/Audio/Presets/' + au.manu + '/' + au.name + '/test3' # for when we mix parameters
save_dir = '/Users/simon/Library/Audio/Presets/' + au.manu + '/' + au.name + '/test3_mix'

if not os.path.exists(save_dir):
    os.mkdir(save_dir)



def generate_preset():
    rp.randomize_parameters(au, rp.consts.automat1_functions)
    normalize_volume(m2ag, au.get_parameters()[rp.consts.automat1_volume_parameter_idx], verbose=verbose)
#	m2ag.play()
    data = m2ag.bounce()[0]
    P.figure(0)
    P.clf()
    P.subplot(211)
    P.plot(data[:5000])
    P.subplot(212)
    P.plot(N.abs(N.fft.rfft(data))[:5000])

    choice = ''
    while choice != 'y' and choice != 'n':
        choice = raw_input('\nsave? (y/n)')

    if choice == 'y':
        save_preset_compteur()

    generate_preset()


#generate_preset()

#def play():
#	m2ag.play()
	
def save_preset(name):
    if not name.endswith('.aupreset'):
        name += '.aupreset'
    au.save_aupreset(save_dir + '/name')
	
#let's look what was the last preset and start there
try:
    compte = max([ int(p[:-9]) for p in os.listdir(save_dir) if p.endswith('.aupreset')])+1
except:
    compte = 0
if verbose:
    print 'we start with %i.aupreset' % compte
def save_preset_compteur():
    global compte
    au.save_aupreset(save_dir + ('/%i.aupreset' % compte))
    compte+=1
    
def mix_presets(preset_name1, preset_name2):
    if type(preset_name1) == int:
        preset_name1 = '%i.aupreset' % preset_name1
    if type(preset_name2) == int:
        preset_name2 = '%i.aupreset' % preset_name2
    
    rp.mix_parameters(au, os.path.join(load_dir, preset_name1), os.path.join(load_dir, preset_name2), rp.consts.automat1_mix_functions)
    normalize_volume(m2ag, au.get_parameters()[rp.consts.automat1_volume_parameter_idx], verbose=verbose)
    
    
def mix_all_presets():
    presets = filter( lambda p : p.endswith('.aupreset'), os.listdir(load_dir) )    
    for p1 in presets:
        for p2 in presets:
            if p1 != p2:
                path = os.path.join(save_dir, '%s' % p1[:-9])
                if not os.path.exists(path):
                    os.mkdir(path)
                path = os.path.join(path, '%s.aupreset' % p2[:-9])
                if not os.path.exists(path):
                    mix_presets(p1,p2)
                    au.save_aupreset(path)
#mix_all_presets()