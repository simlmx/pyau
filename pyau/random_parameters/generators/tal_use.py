#
# Stuff for generating aupresets for Tal's "Use".
#
# february 16th 2010
# Simon Lemieux
#
#

from numpy.random import randint, uniform
import pygmy.audiounit.random_parameters.randfunc as RF
from param_randomizer import param_randomizer

from pygmy.audiounit.random_parameters.volume import normalize_volume

class tal_use_param_randomizer(param_randomizer):
    
    def __init__(self, au, host, volume=.5, prob_on=1.):
        super(tal_use_param_randomizer, self).__init__(au, host, volume, prob_on)
    
    def reset_parameters(self):
        super(tal_use_param_randomizer, self).reset_parameters()
        self.params_dict['On / Off'].value = 1.
        self.params_dict['Shelf frquency'].value = .5
        
    def randomize_parameters(self, nb_trials=10):
        """
        Returns the number of trials if it succeded, -1 if not.
        But -1 should very unusual.
        
        nb_trials : nb of time it will try before it stops and returns -1
        """
        self.au.bypass = False if uniform() < self.prob_on else True
        if self.au.bypass == True:
            self.reset_parameters()        
            return 0
            
        for no_trial in range(nb_trials):
            self.reset_parameters()        

            # we do so Shelf is in [0, .4]u[.6, 1.], so there is at least some effect
            RF.randomize_parameter(self.params_dict['Shelf'], self.au, RF.uniform_custom(0., .4))
            self.params_dict['Shelf'].value += [0., .6][randint(2)]        
            RF.randomize_parameter(self.params_dict['Bass lift'], self.au, RF.uniform)
            RF.randomize_parameter(self.params_dict['Shelf q'], self.au, RF.uniform_custom(.5, 1.))

                
            normalize_volume(self.host, self.params_dict['Volume'], target_peak=self.volume, verbose=False)
            #self.params_dict['Volume'].value = .9
            vol = self.params_dict['Volume'].value
            
            #print 'TAL USE volume : ', vol.value
                
            if vol < 1. and vol > 0.:
                return no_trial
        return -1
            

            
    def _used_parameters(self):
        return ['Shelf', 'Shelf q', 'Bass lift', 'Volume']

    
    
    

