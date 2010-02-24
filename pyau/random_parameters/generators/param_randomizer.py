#
# General stuff for generating random parameters for audio units
#
# february 16th 2010
# Simon Lemieux
#

import pygmy.audiounit.random_parameters.randfunc as RF
from pygmy.audiounit.random_parameters.volume import normalize_volume
from numpy import array, hstack

class param_randomizer(object):
    ''' Utilities for generating random parameters for audio units.
        Typically this class should be subclassed for a specific audio unit.
        'volume' is the volume we want at the output of the audiounit. It is the max RMS in windows, as calculated by
        the function 'normalize_volume'. Not used by this class but should be used by class deriving this one.
    '''
    
    def __init__(self, au, m2ag, volume):
        self.m2ag = m2ag
        self.au = au
        self.volume = volume
        
        self.params = au.get_parameters()
        self.params_dict = dict([(p.name,p) for p in self.params])
        
    def reset_parameters(self):
        ''' Sets all parameters of an audiounit to their default value.
            This could be overrided for new default parameters.
            
            Note : this is called at the beginning of 'set_parameters' and should set the 
                   values that were not assigned at random.
        '''
        for p in self.params:
            p.value = p.default_value
    
    def randomize_parameters(self):
        ''' This method should be overrided to get some more interesting random generation of the parameters.
            Note : When overriding this one, you should also override _used_parameters.
        '''
        for p in self.params:
            RF.randomize_parameter(p, self.au, RF.uniform)
    
#    def _normalize_volume(self):
#        ''' This method should be overrided as well'''
#        print 'Error : "param_randomizer.set_parameters" not implemented yet'
        
    def _used_parameters(self):
        ''' The names of the params that are used.
            Must be overrided in most cases, if not will use all parameters.
            Has to be overriden when randomize_parameters is overriden, most of the time.
        '''
        return self.params_dict.keys()
    
    def get_parameters(self):
        ''' Returns the used parameters in the form of a numpy array.
            Typically for 'learning' purposes.
        '''
        x = array([0. if au.bypass else 1.])
        
        for name in self._used_parameters():
            num_indexed_params = self.params_dict[name].num_indexed_params
            if self.params_dict[name].num_indexed_params == 0:
                x = hstack((x, array([self.params_dict[name].value])))
                
            else:
                temp = zeros(num_indexed_params)
                temp[int(self.params_dict[name].value + .5)] = 1.
                x = hstack((x, temp))
                
        return x
        
    def set_parameters(self, x):
        ''' Opposite of get_parameters.
            Might need to be overriden in some cases
        '''
        print 'Error : "param_randomizer.set_parameters" not implemented yet'
        # TODO : be careful with the continuous params in [0., 1.] that are really discrete values, with e.g. 0. means A and >0. means B
        # we should use them as <.5 means A and >=.5 means B
