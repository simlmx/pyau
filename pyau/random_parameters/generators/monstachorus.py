#
# Stuff for generating aupresets for monstachorus.
#
# february 10th 2010
# Simon Lemieux
#

import numpy.random as NR
import pygmy.audiounit.random_parameters.randfunc as RF
from common import *

def monstachorus_random_params(m2ag, au, verbose=False):
    '''
    Generate random parameters for monstachorus 'au'.
    'au' must be in the graph of 'm2ag'.
        
    '''
    
    reset_parameters(au)
    for p in au.get_parameters():
        RF.randomize_parameter(p, au, RF.uniform)
