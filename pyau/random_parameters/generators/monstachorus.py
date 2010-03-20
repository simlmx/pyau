#
# Stuff for generating aupresets for monstachorus.
#
# february 10th 2010
# Simon Lemieux
#

import pygmy.audiounit.random_parameters.randfunc as RF
from param_randomizer import param_randomizer

import numpy.random as NR

class monstachorus_param_randomizer(param_randomizer):
    
    def __init__(self, au, host, volume=None):
        super(monstachorus_param_randomizer, self).__init__(au, host, None)
        
    def randomize_parameters(self):
        self.reset_parameters()
        p = self.params
        p[0].value = 1.
        p[1].value = 1.
        while p[0].value > .4 and p[1].value > .9 - p[0].value: # hand-picked rule
            for i in [0,1]:
                # greater than .2 to ensure some chorus
                RF.randomize_parameter(p[i], self.au, RF.uniform_custom(.2, 1.))
        # greater than .2 again to ensure some chorus 
        RF.randomize_parameter(p[2], self.au, RF.uniform_custom(.2, 1.))
