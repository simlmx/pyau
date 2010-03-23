#
# Stuff for generating aupresets for Kontakt 3
#
# march 10th 2010
# Simon Lemieux
#

import os

import pylab as P
import numpy as N

#import pygmy.audiounit as AU
import pygmy.audiounit.random_parameters.randfunc as RF
from pygmy.audiounit.random_parameters.generators.param_randomizer import param_randomizer
from pygmy.audiounit.random_parameters.volume import normalize_volume, check_volume
    
def kontakt3_aupreset_dir():
    ''' Returns the directory where to find kontakt3 aupresets.
        TODO : Do something more clean : we have to edit this sometimes...
    '''
    return '/Library/kontakt3_db/aupresets_usable'
    
class kontakt3_param_randomizer(param_randomizer):
    
    def __init__(self, au, host, volume=.5):
        super(kontakt3_param_randomizer, self).__init__(au, host, volume)
        self.aupresets = filter(lambda f : f.endswith('.aupreset'), os.listdir(kontakt3_aupreset_dir()))
        self.current_aupreset = None
    
    def _used_parameters(self):
        print 'Error : _used_parameters() has no sense for Kontakt3'
        
    def reset_parameters(self):
        print 'Error : reset_parameters() has no sense for Kontakt3'
        #super(automat1_param_randomizer, self).reset_parameters()
                
    def randomize_parameters(self):
        ''' Takes a random .aupreset '''
        self.current_aupreset = N.random.randint(len(self.aupresets))
        self.au.load_aupreset(self.aupresets[self.current_aupreset])
        
    def get_parameters(self):
        ''' One hot for the .aupresets. '''
        x = N.zeros(len(self.aupresets))
        x[self.current_aupreset] = 1.
        return x
        
    def set_parameters(self, x):
        self.current_aupreset = N.argmax(x)
        self.au.load_aupreset(self.aupresets[self.current_aupreset])
        
