#
#  random_parameters.py
#  
#
#  Created by simon on 17/04/09.
#  Copyright (c) 2009 . All rights reserved.
#

import numpy as N
import numpy.random as NR

def randomize_parameters(audiounit, functions):
    """ Set AudioUnit parameters to some values (usually used to give random values to parameters).

        parameters
            A list of pygmy.audiounit.Parameter.
            
        functions
            A list of functions taking a Parameter (the one to be set) and a AudioUnit (corresponding to the parameter) and returning a float, examples : uniform, default, lambda p,au : 3.
            The number of functions has to be the same as the number of parameters of the audiounit.
    """
    for p,f in zip(audiounit.get_parameters(), functions):
        p.value = f(p,audiounit)
        
def randomize_parameter(parameter, audiounit, function):
    """ Same as *randomize_parameters* but for a single parameter. """
    parameter.value = function(parameter,audiounit)
        
def mix_parameters(audiounit, aupreset1, aupreset2, functions):
    """ Sets some audiounit's parameters using two exising aupresets. 
        
        audiounit
            The Audiounit.
            
        aupreset1,aupreset2
            The aupreset files.
            
        functions
            A list of functions taking as input two parameters and a (corresponding) audiounit and returning a new (mixed) value for the parameters.
            The number of functions has to be the same as the number of parameters of the audiounit.
            An example of function could be mix_mean, mix_weighted_mean(.4) or lambda p1,p2,au : 2.
    """
    au = audiounit
    params = au.get_parameters()
    au.load_aupreset(aupreset1)
    values1 = N.array([ p.value for p in params ])
    au.load_aupreset(aupreset2)
    values2 = N.array([ p.value for p in params ])
    
    for v1,v2,p,f in zip(values1, values2, params, functions):
        p.value = f(v1,v2,p,au)

        
###
### functions for generating random parameter values
### (Parameter, Audiounit) --> float/int
###
        
def _uniform_interval(a,b):
    """ Return a uniform value between 'a' and 'b'. """
    return NR.rand() * (b-a) + a

def uniform(param, au):
	""" Sets the value of the param to a random value uniformly distributed between the min and max value of the param
		or in [0,1,2, ... ,p.num_indexed_params-1] if the param has indexed params.
	"""
	if param.num_indexed_params > 0:
		return NR.randint(param.num_indexed_params)
	else:
		return _uniform_interval(*param.range)
        
def uniform_custom(a,b):
    """ Returns a function taking a Parameter and an Audiounit and returning a random number between *a* and *b*. """
    return lambda param,au : _uniform_interval(a,b)
	
def default(param, au):
	""" Sets the value of a parameter to its default value. """
	return param.default_value
    
def normal(mean,std):
    """ Returns a fonction taking a param and a audiounit and returning a normal distributed number of mean 'mean' and standard deviation 'std'. """
    return lambda param,au : NR.normal(mean,std)
    
def uniform_list(values):
    """ Returns a fonction taking a param and a audiounit and returning a value in *values* with uniformly distributed probability. """
    def f(p,a):
        index = NR.randint(len(values))
        return values[index]
    return f
    


###
### fonctions for mixing two parameter's values
### (float, float, Parameter, Audiounit) --> float/int
###
    
    
def mix_mean(v1,v2,param,audiounit):
    """ Returns the mean of v1 and v2
    
        v1,v2
            some values of parameter param
    """
    return mix_weighted_mean()
    
def mix_random_weighted_mean():
    """ Same as mix_weighted_mean but the weight is choosed uniformly between 0. and 1. """
    return mix_weighted_mean(NR.rand())
    
def mix_weighted_mean(weight=.5):
    """ Returns a function taking two floats (some values for the parameter), a pygmy.audiounit.Parameter and a pygmy.audiounit.Audiounit and returning a weighted mean of the two floats.
    
        weight
            The weight for the 'weighted' mean.
    
        Typically used with some audiounit_mix_functions in random_parameters_const.py.
    """
    
    w = weight
    return lambda v1,v2,param,audiounit : (w * v1 + (1.-w) * v2)
    
def mix_random(v1,v2,param, audiounit):
    """ Returns p1.value with probability .5 and p2.value with the same probability
    
        v1,v2
            Two values for the parameter param.
        param
            A pygmy.audiounit.Parameter.
        audiounit
            A pygmy.audiounit.Audiounit.
            
        Typically used with some audiounit_mix_functions in random_parameters_const.py.
    """
    return [v1,v2][NR.randint(2)]

def mix_default(v1,v2,param, audiounit):
    """ Default function used to mix parameters.
        Uses mix_random if the parameter is indexed ;
        uses mix_random_weighted_mean() if it is not.
    """
    
    if param.num_indexed_params > 0.:
        return mix_random(v1,v2,param,audiounit)
    else:
        return mix_random_weighted_mean()(v1,v2,param,audiounit)
    
