#
# Stuff for generating aupresets for monstachorus.
#
# february 10th 2010
# Simon Lemieux
#

import random_parameters as RP

def monstachorus_random_params(m2ag, au, verbose=False):
    '''
    Generate random parameters for monstachorus 'au'.
    'au' must be in the graph of 'm2ag'.
        
    '''
    
    reset_parameters(au)
    for p in au.get_parameters()
        RP.randomize_parameter(p, au, RP.uniform)
