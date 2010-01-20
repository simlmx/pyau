#
# Some random functions for parameters
# They will probably look like those in random_parameters.py but this is for a different context
#
# Simon Lemieux
# january 18th 2010
#

import numpy.random as NR

def uniform_interval(a,b):
	""" Return a uniform value between 'a' and 'b'. """
	return NR.rand() * (b-a) + a
    
