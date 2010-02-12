#
# Common stuff for generating aupresets.
#
# february 10th 2010
# Simon Lemieux
#

def parameter_dictionary(au):
    ''' Makes a dictionary with keys -> values = 'name of the parameter' -> pygmy.audiounit.Parameter.'''
    params = au.get_parameters()
    # dictionary with key = name of param, value = param
    params = dict([(p.name,p) for p in params])
    return params
    
def reset_parameters(au):
    ''' Sets all parameters of an audiounit to their default value. '''
    for p in au.get_parameters():
        p.value = p.default_value
