#
#  normalize_volume.py
#  Midi2Audio
#
#  Created by simon on 11/06/09.
#  Copyright (c) 2009 University of Montreal. All rights reserved.
#

# TODO : don't use the max ('peak') of the signal, but some function of the 'mean' over the signal to normalize

"""
Used to normalize the volume of one or several .aupreset.
Not particularly clean but works!
"""

import os, sys
from os.path import isdir, join

import numpy as N

import pygmy.audiounit as AU

def normalize_volume(midi2audio_generator, volume_parameter, save_dir=None, target_peak=.1, verbose=False):
    """ Juste like 'normalize_volume' but using the current set of parameters of the audiounit instead of a .aupreset. """

    m2ag = midi2audio_generator

    volume_backup = volume_parameter.value
    
    # we calculate the peaks for 3 values
    values = list(volume_parameter.range)
    values.insert(1, N.mean(values))
    
    if verbose:
        print 'values'
        print values
    
    peaks = []
    for v in values:
        volume_parameter.value = v
        x = m2ag.bounce()
        #x = N.random.rand(2,10^6)
        peaks.append(N.max(N.abs(x)))
    
    if verbose:
        print 'peaks'
        print peaks
        
        print 'ratio :'
        print peaks[2]/peaks[1]
        print "(if the ratio is always the same, then it's not worth doing the parabola stuff!"
            
    # we find the parabola going threw these points
    
    A = N.array( [ [ x**n for n in [2,1,0] ] for x in values ], dtype=float )
    b = N.array(peaks, dtype = float)
    
    a,b,c = N.linalg.solve(A,b)
    
    # if y = "max peak" and x = "volume parameter value", then we'll say that y = a*x^2 + b*x + c
    
    h = -b/2/a
    k = c - b*b/a
    y = target_peak
    
    root = N.sqrt( (y-k)/a )
    s = root + h
    
    # all this to have s as our volume
    
    if s > volume_parameter.range[1]:
        s = volume_parameter.range[1]
        
    if verbose:
        print 'volume parameter value'
        print s
        
    # we finally set the new value!
    volume_parameter.value = s

    


def normalize_volume_presets(aupreset_file_or_dir, midi2audio_generator, audiounit, volume_parameter, save_dir=None, target_peak=.1, verbose=False):
    """ Adjust the volume parameter of an audiounit so that the audiounit will output a know quantity of energy.
        Typically used to homogenize a list of .aupreset.
        Basically we calculate the peak in the audio signal for 3 values of volume_parameter ( min, max and (min+max)/2 )
        and extrapolate to find the value of volume_parameter that will give us a peak of target_peak.
        
        aupreset_file_or_dir
            A path pointing to a .aupreset file or a directory containing one or more .aupreset.
            
        midi2audio_generator
            A pygmy.audiounit.Midi2AudioGenerator.
            The midifile property of the midi2audio_generator is assumed to be set.
            Typically containing a single audiounit (corresponding to the .aupreset(s)).
            
        audiounit
            The audiounit for which we are gonna adjust the volume_parameter.
            Should be in the AUChainGroup of the midi2audio_generator.
                        
        volume_parameter
            The pygmy.audiounit.Parameter of the audiounit to be adjusted.
            
        target_peak
            The highest (absolute) value we want in our sound (assuming the signal is between -1 and 1).
        suffix
            Some suffix to be added to the name of the .aupreset when saving the new .aupreset.
            The old .aupreset will be replaced if no suffix is specified.
    """
    
    if save_dir is None:
        print 'Error : you have to specify a save_dir'
    
    m2ag = midi2audio_generator
    au = audiounit
    
    if isdir(aupreset_file_or_dir): 
        presets = [ join(aupreset_file_or_dir, p) for p in os.listdir(aupreset_file_or_dir) if p.endswith('.aupreset') ]
    else:
        presets = [ aupreset_file_or_dir ]
    
    for p in presets:  
        
        if verbose:
            print
            print 'Normalizing preset', p
    
        au.load_aupreset(p)
        
        normalize_volume(m2ag, volume_parameter, target_peak, verbose)
                   
        # and save
        new_preset = join(save_dir, p)

        if verbose:
            print 'Saving preset at', new_preset
        au.save_aupreset(new_preset)
        
# nv(save_dir, m2ag, au, au.get_parameters()[89], '/Users/simon/tmp/test2', verbose=True)
        