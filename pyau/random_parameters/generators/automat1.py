#
# Stuff for generating aupresets for automat1.
#
# january 18th 2010
# Simon Lemieux
#


import pylab as P
import numpy as N

#import pygmy.audiounit as AU
import pygmy.audiounit.random_parameters.randfunc as RF
from pygmy.audiounit.random_parameters.generators.param_randomizer import param_randomizer
from pygmy.audiounit.random_parameters.volume import normalize_volume, check_volume




def plot_sound(m2ag):
    data = m2ag.bounce()[0]
    P.figure(0)
    P.clf()
    P.subplot(211)
    P.plot(data[10000:10000+5000])
    P.subplot(212)
    P.plot(N.abs(N.fft.rfft(data))[:5000])
    
    
class automat1_param_randomizer(param_randomizer):
    
    def __init__(self, au, m2ag, volume=.5):
        super(automat1_param_randomizer, self).__init__(au, m2ag, volume)
    
    def _used_parameters(self):
        used = 'Mix1_Level MIX2_Level MIX3_Level'.split()
        for i in [1,2,3]:
            for suffix in 'Wave Width Stack StackOffset Detune SyncOffset'.split():
                used.append('OSC%i_%s' % (i, suffix))
            for suffix in 'FilterType CutOff Resonance ShapeType Bias Drive'.split():
                used.append('SHP%i_%s' % (i, suffix))
        for suffix in 'Attack Hold Decay Sustain Release'.split():
            used.append('AMP_%s' % suffix)
            
        return used
        
    def reset_parameters(self):
        super(automat1_param_randomizer, self).reset_parameters()
        self.params_dict['OSC2_Sync'].value = 2.
        self.params_dict['OSC3_Sync'].value = 2.
        self.params_dict['MIX1_Level'].value = 1.
        self.params_dict['AMP_Velocity'].value = .8
        
    
    def randomize_parameters(self):
        '''
        Generate random parameters in a clever way for audiounit 'au' (which must be automat1 by alphakanal)
        au must be in the graph of m2ag.
        '''
        verbose = False
        
        au = self.au
        m2ag = self.m2ag
        params = self.params_dict
        params["MIX1_Level"] = params["Mix1_Level"]
        

        self.reset_parameters()
            
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
            RF.randomize_parameter(params["OSC%i_Wave" % osc_no], au, RF.uniform_list(listes[osc_no-1]))
            
            if verbose:
                print 'Wave type : %s' % params["OSC%i_Wave" % osc_no].get_str_from_value()

            if params["OSC%i_Wave" % osc_no].value == 0: # if it's OFF we won't do nothing
                return
                
            # selecting other things
            while True : 
                RF.randomize_parameter(params['OSC%i_Width' % osc_no], au, RF.uniform)
                RF.randomize_parameter(params['OSC%i_Stack' % osc_no], au, RF.uniform)
                RF.randomize_parameter(params['OSC%i_StackOffset' % osc_no], au, RF.uniform_custom(0., .55))
                RF.randomize_parameter(params['SHP%i_FilterType' % osc_no], au, RF.uniform)
                RF.randomize_parameter(params['SHP%i_CutOff' % osc_no], au, RF.uniform)
                RF.randomize_parameter(params['SHP%i_Resonance' % osc_no], au, RF.uniform)
                RF.randomize_parameter(params['SHP%i_ShapeType' % osc_no], au, RF.uniform_list(range(4)+[5]))
                if verbose: 
                    print 'Shape type : %s (%i)' % (params['SHP%i_ShapeType' % osc_no].get_str_from_value(), params['SHP%i_ShapeType' % osc_no].value), 
                    
                if params['SHP%i_ShapeType' % osc_no].value == 3:
                    RF.randomize_parameter(params['SHP%i_Bias' % osc_no], au, RF.uniform_custom(0., .25))
                else:
                    RF.randomize_parameter(params['SHP%i_Bias' % osc_no], au, RF.uniform)
                RF.randomize_parameter(params['SHP%i_Drive' % osc_no], au, RF.uniform)
                if verbose:
                    print 'and bias is %s' % params['SHP%i_Bias' % osc_no].get_str_from_value()
                    
                
                # some "not osc1" specific parameters
                if osc_no != 1:
                    RF.randomize_parameter(params['OSC%i_Detune' % osc_no], au, RF.normal(.5, .05))
                    RF.randomize_parameter(params['OSC%i_SyncOffset' % osc_no], au, RF.uniform)
                    
                if verbose:
                    print 'listening to OSC %i' % osc_no
                    #m2ag.play()
                    
                params["MIX%i_Level" % osc_no].value = .2
                if check_volume(m2ag, verbose=verbose) > .004:
                    break
                if verbose:
                    print "Something doesn't sound good : let's do it again."
            
        for i in [1,2,3]:
            set_some_osc_params(i)
                        

        # OSC volumes
        params['MIX1_Level'].value = 1.
        for i in [2,3]:
            if params['OSC%i_Wave' % i].value == 0:
                params['MIX%i_Level' % i].value = params['MIX%i_Level' % i].default_value
            elif params['OSC%i_Wave' %i].value == 8: # if it's noise
                RF.randomize_parameter(params['MIX%i_Level' % i], au, RF.uniform_custom(0., .25)) 
            else:
                RF.randomize_parameter(params['MIX%i_Level' % i], au, RF.uniform) 
            
        
                     
        # envelop
        RF.randomize_parameter(params['AMP_Attack'], self.au, RF.normal(0., .3))
        params['AMP_Attack'].value = params['AMP_Attack'].value
        for suffix in 'Hold Decay Sustain Release'.split():
            RF.randomize_parameter(params['AMP_%s' % suffix], self.au, RF.uniform)

                     
        normalize_volume(m2ag, params["OUT_Master"], target_peak=self.volume, verbose=verbose)
        vol = params['OUT_Master']
        
        if not (vol.value < vol.range[1] and vol.value > vol.range[0]):
            # let's start over
            #raw_input('doing again random')
            print "It did't work with these settings, volume would have to be %f" % vol.value
            self.randomize_parameters()            
            #if verbose:
            
                       
#        for p in self._used_parameters():
#            print self.params_dict[p]
       