#
# Stuff for generating aupresets for Tal's "Use".
#
# february 21th 2010
# Simon Lemieux
#

import numpy.random as NR

import pyau.random_parameters.randfunc as RF
from param_randomizer import param_randomizer

from pyau.random_parameters.volume import normalize_volume

class tal_dub3_param_randomizer(param_randomizer):
    
    def __init__(self, au, host, volume=.5, prob_on=1.):
        super(tal_dub3_param_randomizer, self).__init__(au, host, volume, prob_on)

    def reset_parameters(self):
        super(tal_dub3_param_randomizer, self).reset_parameters()
        self.params_dict['delaytimesync'].value = 1.
        self.params_dict['delaytwice_l'].value = 0.
        self.params_dict['delaytwice_r'].value = 0.
        self.params_dict['resonance'].value = 0.
        
    def randomize_parameters(self, nb_trials=10):
        """
        Returns the number of trials if it succeded, -1 if not.
        But -1 should very unusual.
        
        nb_trials : nb of time it will try before it stops and returns -1
        """
        self.au.bypass = False if NR.uniform() < self.prob_on else True
        if self.au.bypass == True:
            self.reset_parameters()        
            return 0
            
        for no_trial in range(nb_trials):
            self.reset_parameters()        
            
            RF.randomize_parameter(self.params_dict['inputdrive'], self.au, RF.uniform_custom(.45, 1.))
            RF.randomize_parameter(self.params_dict['delaytime'], self.au, RF.uniform_custom(0.017, .04))
            RF.randomize_parameter(self.params_dict['feedback'], self.au, RF.uniform_custom(0., .3))
            
            f = lambda x : -.15*x**2 + .42*x + .18
            hp = self.params_dict['highcut']
            cp = self.params_dict['cutoff']
            hp.value = 0.; cp.value = 0.
            while cp.value < f(hp.value):
                RF.randomize_parameter(hp, self.au, RF.uniform)
                RF.randomize_parameter(cp, self.au, RF.uniform)
                
            param_vol = self.params_dict['dry']
            normalize_volume(self.host, param_vol, target_peak=self.volume, verbose=False)
            vol = param_vol.value
            RF.randomize_parameter(self.params_dict['wet'], self.au, RF.uniform_custom(vol/3., vol))
            if vol < param_vol.range[1] and vol > param_vol.range[0]:
                return no_trial
        return -1
            
    def _used_parameters(self):
        return 'inputdrive delaytime feedback highcut cutoff dry wet'.split()

    
    
    

