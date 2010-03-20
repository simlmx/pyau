#
# Choosing the right generator class for a given audiounit
#
# february 16th 2010
# Simon Lemieux
#

import pygmy

from param_randomizer import param_randomizer

from automat1 import automat1_param_randomizer
from monstachorus import monstachorus_param_randomizer
from tal_use import tal_use_param_randomizer
from camel_crusher import camel_crusher_param_randomizer
from tal_dub3 import tal_dub3_param_randomizer
from tal_reverb import tal_reverb_param_randomizer
from kontakt3 import kontakt3_param_randomizer

def get_randomizer(au, host, volume):
    ''' Returns the good derived (from param_randomizer) class for an audiounit.
    '''

    name = au.name
       
    if name == 'Automat1':
        return automat1_param_randomizer(au, host, volume)
    elif name == 'MonstaChorus':
        return monstachorus_param_randomizer(au, host, volume)
    elif name == 'Tal-USE-AU-Effect':
        return tal_use_param_randomizer(au, host, volume)
    elif name == 'CamelCrusher':
        return camel_crusher_param_randomizer(au, host, volume)
    elif name == 'TAL Dub III Plugin':
        return tal_dub3_param_randomizer(au, host, volume)
    elif name == 'TAL Reverb Plugin':
        return tal_reverb_param_randomizer(au, host, volume)
    elif name == 'Kontakt3':
        return kontakt3_param_randomizer(au, host, volume)
    # this is where to add a new audiounit
    else:
        print 'Warning : using default param_randomizer for audiounit "%s"' % au.name
        return param_randomizer(au, host)
    
    
    