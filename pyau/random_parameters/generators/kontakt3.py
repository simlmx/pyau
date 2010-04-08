#
# Stuff for generating aupresets for Kontakt 3
#
# march 10th 2010
# Simon Lemieux
#

import os

import numpy as N

#import pygmy.audiounit as AU
import pygmy.audiounit.random_parameters.randfunc as RF
from pygmy.audiounit.random_parameters.generators.param_randomizer import param_randomizer
from pygmy.audiounit.random_parameters.volume import normalize_volume, check_volume
    
def kontakt3_aupreset_dir():
    ''' Returns the directory where to find kontakt3 aupresets.
        TODO : Do something more clean : we have to edit this sometimes...
    '''
    return '/Library/kontakt3_db/aupresets_usable_shortnames'
    
class kontakt3_param_randomizer(param_randomizer):
    
    def __init__(self, au, host, volume=.5):
        super(kontakt3_param_randomizer, self).__init__(au, host, volume)
        self.aupresets = [os.path.join(kontakt3_aupreset_dir(), f) for f in os.listdir(kontakt3_aupreset_dir()) if f.endswith('.aupreset')]
        self.aupresets.sort() # that way they are in the some order everytime
        self.current_aupreset = None
    
    def _used_parameters(self):
        print 'Error : _used_parameters() has no sense for Kontakt3'
        
    def reset_parameters(self):
        print 'Error : reset_parameters() has no sense for Kontakt3'
        #super(automat1_param_randomizer, self).reset_parameters()
                
    def randomize_parameters(self, nb_trials=10):
        """ Takes a random .aupreset 
            Returns True if it succeded, False if not.
            But false should very unusual.
            
            nb_trials : nb of time it will try before it stops and returns False
        """
        for no_trial in range(nb_trials):
            self.current_aupreset = N.random.randint(len(self.aupresets))
            #print self.aupresets[self.current_aupreset]
            self.au.load_aupreset(self.aupresets[self.current_aupreset])
            vol = check_volume(self.host, verbose=False)
            if vol <= 0.:
                print "kontakt aupreset %s doesn't like midi file %s" % ( self.aupresets[self.current_aupreset], self.host.midifile )
            else:
                return no_trial
        return -1
        
    def get_parameters(self):
        ''' One hot for the .aupresets. '''
        x = N.zeros(len(self.aupresets))
        x[self.current_aupreset] = 1.
        return x
        
    def set_parameters(self, x):
        self.current_aupreset = N.argmax(x)
        self.au.load_aupreset(self.aupresets[self.current_aupreset])
        
