#
# Stuff for generating aupresets for automat1.
#
# january 18th 2010
# Simon Lemieux
#


import pylab as P
import numpy as N

import random_parameters as RP
import pygmy.audiounit as AU
from normalize_volume import normalize_volume, check_volume
from generate_common import *



def plot_sound(m2ag):
    data = m2ag.bounce()[0]
    P.figure(0)
    P.clf()
    P.subplot(211)
    P.plot(data[10000:10000+5000])
    P.subplot(212)
    P.plot(N.abs(N.fft.rfft(data))[:5000])

    


def automat1_random_params(m2ag, au, verbose=False):
    '''
    Generate random parameters in a clever way for audiounit 'au' (which must be automat1 by alphakanal)
    au must be in the graph of m2ag.
    '''

    # dictionary with key = name of param, value = param
    params = parameter_dictionary(au)
    # hack because of some incosistancy in their param's naming
    params["MIX1_Level"] = params["Mix1_Level"]

    reset_parameters(au)
            
    def set_some_osc_params(osc_no):
        ''' Setting up oscillator 'osc_no'.
        '''
        
        if verbose:
            print '---------'
            print '- OSC %i -' % osc_no
            print '---------'

        # let's mute everything excep 'osc_no'
        for i in [1,2,3]:
            params['MIX%i_Level' % i].value = (1. if i == osc_no else 0.)
            
        # selecting which type of wave
        listes = [range(1,6), range(0,6), range(0,6)+[8]] # it can only be sin, tri, rect, saw, table / + off / + noise
        RP.randomize_parameter(params["OSC%i_Wave" % osc_no], au, RP.uniform_list(listes[osc_no-1]))
        
        if verbose:
            print 'Wave type : %s' % params["OSC%i_Wave" % osc_no].get_str_from_value()

        if params["OSC%i_Wave" % osc_no].value == 0: # if it's OFF we won't do nothing
            return
            
        # selecting other things
        while True : 
            RP.randomize_parameter(params["OSC%i_Width" % osc_no], au, RP.uniform)
            RP.randomize_parameter(params["OSC%i_Stack" % osc_no], au, RP.uniform)
            RP.randomize_parameter(params["OSC%i_StackOffset" % osc_no], au, RP.uniform_custom(0., .55))
            RP.randomize_parameter(params["SHP%i_FilterType" % osc_no], au, RP.uniform)
            RP.randomize_parameter(params["SHP%i_CutOff" % osc_no], au, RP.uniform)
            RP.randomize_parameter(params["SHP%i_Resonance" % osc_no], au, RP.uniform)
            RP.randomize_parameter(params['SHP%i_ShapeType' % osc_no], au, RP.uniform_list(range(4)+[5]))
            if verbose: 
                print 'Shape type : %s (%i)' % (params['SHP%i_ShapeType' % osc_no].get_str_from_value(), params['SHP%i_ShapeType' % osc_no].value), 
                
            if params['SHP%i_ShapeType' % osc_no].value == 3:
                RP.randomize_parameter(params['SHP%i_Bias' % osc_no], au, RP.uniform_custom(0., .25))
            else:
                RP.randomize_parameter(params['SHP%i_Bias' % osc_no], au, RP.uniform)
            RP.randomize_parameter(params['SHP%i_Drive' % osc_no], au, RP.uniform)
            if verbose:
                print 'and bias is %s' % params['SHP%i_Bias' % osc_no].get_str_from_value()
                
            
            # some "not osc1" specific parameters
            if osc_no != 1:
                RP.randomize_parameter(params['OSC%i_Detune' % osc_no], au, RP.normal(.5, .05))
                params['OSC%i_Sync' % osc_no].value = 2.
                RP.randomize_parameter(params['OSC%i_SyncOffset' % osc_no], au, RP.uniform)
                
            if verbose:
                print 'listening to OSC %i' % osc_no
                #m2ag.play()
                
            params["MIX%i_Level" % osc_no].value = .2
            if check_volume(m2ag, rms_min=.004, verbose=verbose):
                break
            if verbose:
                print "Something doesn't sound good : let's do it again."
        
        #second part
    
    for i in [1,2,3]:
        set_some_osc_params(i)
                    

    # OSC volumes
    params['MIX1_Level'].value = 1.
    for i in [2,3]:
        if params['OSC%i_Wave' % i].value == 0:
            params['MIX%i_Level' % i].value = params['MIX%i_Level' % i].default_value
        else:
            RP.randomize_parameter(params['MIX%i_Level' % i], au, RP.uniform) 
                 
    normalize_volume(m2ag, params["OUT_Master"], target_peak=.4, verbose=verbose)
    vol = params['OUT_Master']
    
    if vol.value >= vol.range[1] or vol.value <= vol.range[0]:
        # let's start over
        automat1_random_params(m2ag, au, verbose):
        if verbose:
            print "It did't work with these settings, volume would have to be %f" % vol.value
            raw_input()
                
    if verbose:
        print "listening to the sum of the 3 OSC"
        #m2ag.play()
       
    
    

# example
    
desc = AU.CAComponentDescription('aumu', 'aut1', 'Alfa')
midi = '/Users/simon/tmp/midis/69.mid'

g = AU.AUChainGroup()
au = g.add_audiosource(desc)
m2ag = AU.Midi2AudioGenerator(g)
m2ag.midifile = midi
#m2ag.play()
   
    

while True:
    automat1_random_params(m2ag=m2ag, au=au, verbose=False)
    raw_input('press Enter')

del m2ag
del g
del au
    
    








