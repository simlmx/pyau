#
# Choosing the right generator class for a given audiounit
#
# february 16th 2010
# Simon Lemieux
#

import pygmy
from pygmy.audiounit import CAComponentDescription as Desc

from param_randomizer import param_randomizer

from automat1 import automat1_param_randomizer
from monstachorus import monstachorus_param_randomizer
from tal_use import tal_use_param_randomizer
from camel_crusher import camel_crusher_param_randomizer
from tal_dub3 import tal_dub3_param_randomizer
from tal_reverb import tal_reverb_param_randomizer
from kontakt3 import kontakt3_param_randomizer

def get_randomizer(au, m2ag, volume):
    ''' Returns the good derived (from param_randomizer) class for an audiounit.
    '''

    desc = au.desc
       

    if desc == Desc('aumu', 'aut1', 'Alfa'):
        return automat1_param_randomizer(au, m2ag, volume)
    elif desc == Desc('aufx', 'bbMC', 'beBU'):
        return monstachorus_param_randomizer(au, m2ag, volume)
    elif desc == Desc('aufx', 'TILT', 'Togu'):
        return tal_use_param_randomizer(au, m2ag, volume)
    elif desc == Desc('aumf', 'CaCr', 'CamA'):
        return camel_crusher_param_randomizer(au, m2ag, volume)
    elif desc == Desc('aumf', 'xg70', 'TOGU'):
        return tal_dub3_param_randomizer(au, m2ag, volume)
    elif desc == Desc('aumf', '676v', 'TOGU'):
        return tal_reverb_param_randomizer(au, m2ag, volume)
    elif desc == Desc('aumu', 'NiK3', '-NI-'):
        return kontakt3_param_randomizer(au, m2ag, volume)
    # this is where to add a new audiounit
    else:
        print 'Warning : using default param_randomizer for audiounit "%s"' % au.name
        return param_randomizer(au, m2ag, volume)
    
    
    