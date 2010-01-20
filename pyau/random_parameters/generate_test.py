#
# Stuff for generating aupresets.
#
# january 18th 2010
# Simon Lemieux
#

#
# Automat1
#
import pylab as P
import numpy as N

import random_parameters as RP
import pygmy.audiounit as AU
from normalize_volume import normalize_volume, check_volume


desc = AU.CAComponentDescription('aumu', 'aut1', 'Alfa')
midi = '/Users/simon/tmp/69.mid'

g = AU.AUChainGroup()
au = g.add_audiosource(desc)
m2ag = AU.Midi2AudioGenerator(g)
m2ag.midifile = midi

params = au.get_parameters()
# dictionary with key = name of param, value = param
params = dict([(p.name,p) for p in params])


def plot_sound():
    data = m2ag.bounce()[0]
    P.figure(0)
    P.clf()
    P.subplot(211)
    P.plot(data[10000:10000+5000])
    P.subplot(212)
    P.plot(N.abs(N.fft.rfft(data))[:5000])

    


def automat1_random_params(verbose=False):

    for p in au.get_parameters():
        p.value = p.default_value
        
    rms_min = .004
    
    # OSC 1
    if verbose:
        print '- OSC 1 -'
    #params["OUT_Master"].value = 1.
    print params["OUT_Master"].value
    while True:
        # max out level 1
        params["Mix1_Level"].value = 1.
        RP.randomize_parameter(params["OSC1_Wave"], au, RP.uniform_list(range(1,6))) # it can only be sin, tri, rect, saw, table
        RP.randomize_parameter(params["OSC1_Width"], au, RP.uniform)
        RP.randomize_parameter(params["OSC1_Stack"], au, RP.uniform)
        RP.randomize_parameter(params["OSC1_StackOffset"], au, RP.uniform_custom(0.,.55))
        RP.randomize_parameter(params["SHP1_FilterType"], au, RP.uniform)
        RP.randomize_parameter(params["SHP1_CutOff"], au, RP.uniform)
        RP.randomize_parameter(params["SHP1_Resonance"], au, RP.uniform)
        
        if verbose:
            print 'Wave type : %s' % params["OSC1_Wave"].get_str_from_value()
            
        params["Mix1_Level"].value = .2
        if check_volume(m2ag, rms_min=rms_min, verbose=True):
            break
        m2ag.play()
        if verbose:
            print "Something's wrong, let's do it again."
    
    m2ag.play()
    
    # OSC 2   
    print '- OSC 2 -' 
    params["Mix1_Level"].value = 0.    
    while True:
        # max out level 1
        params["MIX2_Level"].value = 1.
        RP.randomize_parameter(params["OSC2_Wave"], au, RP.uniform_list(range(0,6))) # it can be off as well
        RP.randomize_parameter(params["OSC2_Width"], au, RP.uniform)
        RP.randomize_parameter(params["OSC2_Stack"], au, RP.uniform)
        RP.randomize_parameter(params["OSC2_StackOffset"], au, RP.uniform_custom(0.,.55))
        RP.randomize_parameter(params["SHP2_FilterType"], au, RP.uniform)
        RP.randomize_parameter(params["SHP2_CutOff"], au, RP.uniform)
        RP.randomize_parameter(params["SHP2_Resonance"], au, RP.uniform)
        
        if verbose:
            print 'Wave type : %s' % params["OSC2_Wave"].get_str_from_value()
        
        if params["OSC2_Wave"].value == 0: # if OFF was chosen as wave type, let's skip this part
            break
        
        params["MIX2_Level"].value = .2
        if check_volume(m2ag, rms_min=rms_min, verbose=verbose):
            break
            
        if verbose:
            print "Something's wrong, let's do it again."
            
    m2ag.play()
    
    # OSC 3 
    print '- OSC 3 -'   
    params["MIX2_Level"].value = 0.
    while True:
        # max out level 1
        params["MIX3_Level"].value = 1.
        RP.randomize_parameter(params["OSC3_Wave"], au, RP.uniform_list(range(0,6)+[8])) # it can be off or noise as well
        RP.randomize_parameter(params["OSC3_Width"], au, RP.uniform)
        RP.randomize_parameter(params["OSC3_Stack"], au, RP.uniform)
        RP.randomize_parameter(params["OSC3_StackOffset"], au, RP.uniform_custom(0.,.55))
        RP.randomize_parameter(params["SHP3_FilterType"], au, RP.uniform)
        RP.randomize_parameter(params["SHP3_CutOff"], au, RP.uniform)
        RP.randomize_parameter(params["SHP3_Resonance"], au, RP.uniform)
        
        if verbose:
            print 'Wave type : %s' % params["OSC3_Wave"].get_str_from_value()
        
        params["MIX3_Level"].value = .2
        if params["OSC3_Wave"].value == 0: # if OFF was chosen as wave type, let's skip this part
            break
                    
        if check_volume(m2ag, rms_min=rms_min, verbose=verbose):
            break

    m2ag.play()
        

    # OSC volumes
    levels = [lev for type, lev in zip('OSC1_Wave OSC2_Wave OSC3_Wave'.split(), 'Mix1_Level MIX2_Level MIX3_Level'.split()) if params[type].value != 0]
    print levels
    
    
    #m2ag.play()
    #plot_sound()

    
    
    

        
    
    
    

while True:
    automat1_random_params(verbose=True)
    raw_input('press Enter')

#del m2ag
#del g
#del au
    
    








