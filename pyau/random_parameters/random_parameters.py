#!/usr/bin/env python
#
#  random_parameters.py
#  
#
#  Created by simon on 17/04/09.
#  Copyright (c) 2009 . All rights reserved.
#

from numpy.random import rand, randint


def randomize_parameters(audiounit, functions):
	""" Set Audio Unit parameters to some values (usually used to give random values to parameters).
	
		parameters
			A list of pygmy.audiounit.Parameter.
			
		functions
			A list of functions taking a Parameter (the one to be set) and returning a float, examples : uniform, default, lambda p : 3.
	"""
	for p,f in zip(audiounit.get_parameters(), functions):
		p.value = f(p,audiounit)


def _uniform_interval(a,b):
	""" Return a uniform value between 'a' and 'b'. """
	return rand() * (b-a) + a
	
def uniform(param, au):
	""" Sets the value of the param to a random value uniformly distributed between the min and max value of the param
		or in [0,1,2, ... ,p.num_indexed_params-1] if the param has indexed params.
	"""
	if param.num_indexed_params > 0:
		return randint(param.num_indexed_params)
	else:
		return _uniform_interval(*param.range)
	
def default(param, au):
	""" Sets the value of a parameter to its default value. """
	return param.default_value