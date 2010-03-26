#
# Stuff for generating aupresets for TAL Reverb.
#
# february 23th 2010
# Simon Lemieux
#

import pygmy.audiounit.random_parameters.randfunc as RF
from param_randomizer import param_randomizer
from pygmy.audiounit.random_parameters.volume import normalize_volume

import numpy.random as NR

class tal_reverb_param_randomizer(param_randomizer):
    
    def __init__(self, au, host, volume=.5):
        super(tal_reverb_param_randomizer, self).__init__(au, host, volume)
        self.volume = volume
    
    def reset_parameters(self):
        super(tal_reverb_param_randomizer, self).reset_parameters()
                
    def _used_parameters(self):
        return ['Pre Delay', 'Room Size', 'Damp', 'High Cut', 'Low Cut', 'Dry', 'Wet']
    
    def randomize_parameters(self):
        '''
        Returns the nb of times it was re-called.
        '''
        self.reset_parameters()
        RF.randomize_parameter(self.params_dict['Pre Delay'], self.au, RF.uniform_custom(0., .35))
        RF.randomize_parameter(self.params_dict['Room Size'], self.au, RF.uniform)
        RF.randomize_parameter(self.params_dict['Damp'], self.au, RF.uniform)

        
        # high and low cut
        a,b,c = 2.833, -1.5167, 0.4
        f = lambda x : a*x**2 + b*x + c
        hc = self.params_dict['High Cut']
        lc = self.params_dict['Low Cut']
        hc.value = 0.; lc.value = 0.
        while hc.value < f(lc.value):
            RF.randomize_parameter(hc, self.au, RF.uniform_custom(.2, 1.))
            RF.randomize_parameter(lc, self.au, RF.uniform_custom(0., .8))
            
        #for x in self._used_parameters():
         #   print self.params_dict[x]
        
        param_vol = self.params_dict['Dry']
        normalize_volume(self.host, param_vol, target_peak=self.volume, volumes = [.5, .7, .9], verbose=False)
                
        vol = param_vol.value
        if not (vol < 1. and vol > 0.):
            #print "volume was going to be %f" % vol
            return self.randomize_parameters() + 1
        else:
            RF.randomize_parameter(self.params_dict['Wet'], self.au, RF.uniform_custom(vol*3./4., vol))
            return 0

