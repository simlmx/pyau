#
# Stuff for generating aupresets for Kontakt 3
#
# march 10th 2010
# Simon Lemieux
#

import os

import numpy as N

import pyau.random_parameters.randfunc as RF
from param_randomizer import param_randomizer
from pyau.random_parameters.volume import normalize_volume, check_volume
    
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
        self.aupresets_dict = dict([(preset,i) for i,preset in enumerate(self.aupresets)])
            
    def _used_parameters(self):
        print 'Error : _used_parameters() has no sense for Kontakt3'
        
    def reset_parameters(self):
        print 'Error : reset_parameters() has no sense for Kontakt3'
        #super(automat1_param_randomizer, self).reset_parameters()
                
    def randomize_parameters(self, nb_trials=10):
        """ Takes a random .aupreset 
            Returns the number of tries before getting a "good" sound, and -1 if it fails.
            But -1 be should very unusual.
            
            nb_trials : nb of time it will try before it stops and returns -1
        """
        for no_trial in range(nb_trials):
            current_aupreset = N.random.randint(len(self.aupresets))
            #print self.aupresets[self.current_aupreset]
            self.au.load_aupreset(self.aupresets[current_aupreset])
            vol = check_volume(self.host, verbose=False)
            if vol <= 0.:
                print "kontakt aupreset %s doesn't like midi file %s" % ( self.aupresets[current_aupreset], self.host.midifile )
            else:
                return no_trial
        return -1
        
    def get_parameters(self):
        ''' One hot for the .aupresets. '''
        current_aupreset = self.aupresets_dict[current_aupreset]
        x = N.zeros(len(self.aupresets))
        x[current_aupreset] = 1.
        return x
        
    def set_parameters(self, x):
        current_aupreset = N.argmax(x)
        self.au.load_aupreset(self.aupresets[current_aupreset])
        
