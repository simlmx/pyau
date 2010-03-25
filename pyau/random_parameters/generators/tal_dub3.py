#
# Stuff for generating aupresets for Tal's "Use".
#
# february 21th 2010
# Simon Lemieux
#

from numpy.random import randint
import pygmy.audiounit.random_parameters.randfunc as RF
from param_randomizer import param_randomizer

from pygmy.audiounit.random_parameters.volume import normalize_volume

class tal_dub3_param_randomizer(param_randomizer):
    
    def __init__(self, au, host, volume=.5):
        super(tal_dub3_param_randomizer, self).__init__(au, host, volume)

    def reset_parameters(self):
        super(tal_dub3_param_randomizer, self).reset_parameters()
        self.params_dict['delaytimesync'].value = 1.
        self.params_dict['delaytwice_l'].value = 0.
        self.params_dict['delaytwice_r'].value = 0.
        self.params_dict['resonance'].value = 0.
        
    def randomize_parameters(self):
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
        if not ( vol < param_vol.range[1] and vol > param_vol.range[0] ):
            # let's start over
            print 'starting over TAL DUB 3'
            self.randomize_parameters()
            
    def _used_parameters(self):
        return 'inputdrive delaytime feedback highcut cutoff dry wet'.split()

    
    
    

