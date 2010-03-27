#
# Example of generating an auchain
#
# february 10th 2010
# Simon Lemieux
#
import numpy as N

import pygmy.audiounit.random_parameters.generators as generators
   
def generate_aupreset(host,
            effects_prob_on = None,
            synth_vol = .4,
            effects_vol = None,
            randomizer_synth = None,
            randomizer_effects = None,
            log_file = None,
            verbose=False):
    '''
        Generates random parameters for the synth and each effect in the (single) track of the host.

        Params
            host : A pygmy.audiounit.Host containing a single track with (and synth and ) a bunch of effects.

            effects_prob_on : List of probability of each effect to be on (that we are not forced to used every effect all the time).
                              default : 1. each
                              
            synth_vol : Volume (in [0., 1.]) of the synth (before effects).
            effects_vol : Volume of the output of each effects (in [0.,1.]).
                          default : synth_vol for each
            
            randomizer_synth : A randomizer, can be obtained with pygmy.audiounit.random_parameters.generators.get_randomizer(then_synth).
            randomizer_effects : A list of randomizers, obtained like the randomizer_synth.
            
            log_file : A file('some_path', 'a') where we are going to write when important stuff happens.
            
        Returns True if everything went fine, False if not. It should be fine most of the time, depending on how the random generators are coded.
        Note : Randomizers are passed only to speed up if we are calling this function many times. If they are not passed, they will be computed here.
    '''
    return_value = True
    
    # init
    
    effects = host.tracks[0].effects
    nb_effects = len(effects)
    synth = host.tracks[0].synth
        
    if effects_prob_on is None:
        effects_prob_on = [1.]*nb_effects
    
    if effects_vol is None:
        effects_vol = [synth_vol]*nb_effects
    
    if randomizer_synth is None:
        randomizer_synth = generators.get_randomizer(synth, host, synth_vol)
        
    if randomizer_effects is None:
        randomizer_effects = [ generators.get_randomizer(e, host, v) for e,v in zip(effects, effects_vol) ]
        
    # real thing
        
    for e in effects:
        e.bypass = True

    # we randomize the synth
    randomizer_synth.randomize_parameters()
    
    # we randomize effects one by one
    for e,r,p in zip(effects, randomizer_effects, effects_prob_on):
    
        e.bypass = False if N.random.uniform() < p else True
        
        if not e.bypass:
            print 'Using %s' % e.name
            nb = r.randomize_parameters()
            if nb == -1:
                return_value = False
                
    return return_value
    
def load_aupreset(aupresets_dir, host=None):
    """ Loads the .aupresets in 'aupresets_dir' back into the (single) track of the 'host'.
        If the host is not provided (None), we will make one. (TODO... if needed at some point)
    """
    synth = host.tracks[0].synth
    effects = host.tracks[0].effects
    dir = aupresets_dir
    
    synth.load_aupreset(os.path.join(dir, synth.name + '.aupreset'))
    for e in effects:
        file_path = os.path.join(dir, e.name + '.aupreset')
        if os.path.exists(file_path):
            e.load_aupreset(file_path)
            e.bypass = False
        else:
            e.bypass = True
    
def generate_data(host, randomizer_synth=None, randomizer_effects=None):
    """ Returns an array of data for the "synth+effects" instrument in the (single) track of 'host'
        host : The host containing a track with a synth and the effects
        randomizer_* : The randomizers : passed for speed up purposes, so we don't initialize them again. Must match the synth and effects in 'host'
        
    """
    
    synth = host.tracks[0].synth
    effects = host.tracks[0].effects
    
    if randomizer_synth is None:
        randomizer_synth = generators.get_randomizer(synth, host, None) # I don't think we need the volume so it should be OK
    if randomizer_effects is None:
        randomizer_effects = [ generators.get_randomizer(e, host, None) for e in effects ] # Same here
        
    data = randomizer_synth.get_parameters()
    
    for re in randomizer_effects:
        data = N.hstack((data, re.get_parameters()))
    
    return data
    
def load_data(data, host, randomizer_synth=None, randomizer_effects=None):
    """ The opposite of generate data. Starts from the numpy array of 'data'
        and sets the params of the audio units of the 'host' with it.
        See generate_data for the parameters, those are the same.
    """
    
    synth = host.tracks[0].synth
    effects = host.tracks[0].effects
    
    if randomizer_synth is None:
        randomizer_synth = generators.get_randomizer(synth, host, None) # I don't think we need the volume so it should be OK
    if randomizer_effects is None:
        randomizer_effects = [ generators.get_randomizer(e, host, None) for e in effects ] # Same here
        
    n = randomizer_synth.get_parameters().shape[0] # to know how much we need from 'data'
    randomizer_synth.set_parameters(data[:n])
    data = data[n:]
    
    for re in randomizer_effects:
        n = re.get_parameters().shape[0]
        re.set_parameters(data[:n])
        data = data[n:]
        
    print 'this should be empty :', data
    

    
    
        
        
        

        

    
    
