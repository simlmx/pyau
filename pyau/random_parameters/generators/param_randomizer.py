#
# General stuff for generating random parameters for audio units
#
# february 16th 2010
# Simon Lemieux
#

import pygmy.audiounit.random_parameters.randfunc as RF
from pygmy.audiounit.random_parameters.volume import normalize_volume
from numpy import array, hstack, argmax, zeros
import numpy.random as NR
class param_randomizer(object):
    ''' Utilities for generating random parameters for audio units.
        Typically this class should be subclassed for a specific audio unit.
        'volume' is the volume we want at the output of the audiounit. It is the max RMS in windows, as calculated by
        the function 'normalize_volume'. Not used by this class but should be used by class deriving this one.
        prob_on : Probability of the effect to be on. Useful when we have a bunch of effects and do not want them to be necessary all on.
    '''
    
    def __init__(self, au, host, volume, prob_on=1.):
        self.host = host
        self.au = au
        self.volume = volume
        self.prob_on = prob_on
        
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
            
            In general, returns the number of times it had to try again new parameters before giving something that makes sense.
            This is for audio units where generating can give a bad sound and we need to start again.
        '''
        
        for p in self.params:
            RF.randomize_parameter(p, self.au, RF.uniform)
        return 0
    
#    def _normalize_volume(self):
#        ''' This method should be overrided as well'''
#        print 'Error : "param_randomizer.set_parameters" not implemented yet'
        
    def _used_parameters(self):
        ''' The names of the params that are used.
            Must be overrided in most cases ; if not, it will use all parameters.
            Has to be overriden when randomize_parameters is overriden, almost all of the time.
            This is typically in order for get_parameters() and set_parameters() to work properly.
        '''
        return self.params_dict.keys()
    
#    def _force_indexed_params(self):
#        """ Returns a list of the names of the params that are indexed parameters, but not
#            identified as such. We often see params in [0., 1.] where 0. means 'off' and anything else means
#            'on'. For learning purposes, it's better to treat them as discrete params
#        """
#        pass # not used yet, after all I (simon) did not need it... but it might be usefull at some point (with other audio units)
    
    def get_parameters(self):
        ''' Returns the used parameters in the form of a numpy array.
            This is for 'learning' purposes.
        '''
        x = array([0. if self.au.bypass else 1.])
        
        for name in self._used_parameters():
            param = self.params_dict[name]
            num_indexed_params = param.num_indexed_params
            if param.num_indexed_params in [0,2]:
                x = hstack((x, array([param.value])))
            else:
                temp = zeros(num_indexed_params)
                temp[int(param.value + .5)] = 1. # TODO : checker si ca cest OK
                x = hstack((x, temp))
                
        return x
        
    def set_parameters(self, data):
        ''' Opposite of get_parameters.
        '''
        self.reset_parameters()
        self.au.bypass = True if data[0] == 0 else False
        data = data[1:]
        
        for p_name in self._used_parameters():
            p = self.params_dict[p_name]
            if p.num_indexed_params == 0:
                p.value = data[0]
                data = data[1:]
            elif p.num_indexed_params == 2:
                center = (p.range[1] + p.range[0])/2.
                p.value = p.range[1] if data[0]>center else p.range[0]
                data = data[1:]
            else:
                n = p.num_indexed_params       
                p.value = float(argmax(data[:n]))
                data = data[n:]
