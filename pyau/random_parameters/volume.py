#
#  normalize_volume.py
#  Midi2Audio
#
#  Created by simon on 11/06/09.
#  Copyright (c) 2009 University of Montreal. All rights reserved.
#


"""
Used to normalize the volume of one or several .aupreset.
"""

import os, sys
from os.path import isdir, join

import numpy as N

def check_volume(host, window_length=2001, verbose=False):
    """ We bounce from the *host* and return some measure of the sound loudness (max RMS**.3)
    """
    x = host.bounce()
    x = N.mean(x, axis=0)
    
    rms_ = 0.
    for i in range(3, int(x.shape[0]/window_length)): # we skip the 3 first, sometimes weird things appears there (particularly with CamelCrush)
        win = x[i*window_length : (i+1)*window_length]
        rms_ = max(rms_, rms(win))
        #if verbose:
            #print '%.2f' % rms(win),
        
    if verbose:
        import pylab as P
        P.ion()
        P.figure(1)
        P.clf()
        P.plot(x)
        #host.play() 
        print 'rms :', rms_   
        print 'loudness :', rms_**.3
        #raw_input('next')     

    return rms_**.3 # .3 = thumb rule

def normalize_volume(host, volume_parameter, target_peak=.4, window_length=2001, volumes=None, verbose=False):
    """ Juste like 'normalize_volume' but using the current set of parameters of the audiounit instead of a .aupreset. 
        If window_length is None, we take untile the end of the signal.
        
        volumes : Overrides the default values with which we set the volume parameter for finding the optimal volume.
                  Has to be three values, e.g. [.3, .6 ,.8].
                
    """

    host = host

    volume_backup = volume_parameter.value
    
    # we calculate the peaks for 3 values
    if volumes is None:
        min_, max_ = list(volume_parameter.range)
        lap = max_ - min_
        values = [ min_ + lap/4., min_ + lap/2., min_ + 3.*lap/4.] 
    else:
        values = volumes
        
    nb_points = len(values)
    
    if verbose:
        print
        print 'values'
        print values
    
    peaks = []
    
    for v in values:
        volume_parameter.value = v
        loudness = check_volume(host, window_length = window_length, verbose = verbose)
        
        peaks.append(loudness)
    
    if verbose:
        print 'peaks'
        print peaks

    # we find the parabola going threw these points
    
    A = N.array( [ [ x**n for n in range(nb_points) ] for x in values ], dtype=float )
    b = N.array(peaks, dtype = float)
    
    #c = N.linalg.solve(A,b) for more than 2nd degree
    c,b,a = N.linalg.solve(A,b)
    
    # if y = "max peak" and x = "volume parameter value", then we'll say that y = a*x^2 + b*x + c
    
    h = -b/2./a
    k = c - b*b/a/4.
    y = target_peak
    
    if (y-k)/a >= 0:
        root = N.sqrt( (y-k)/a )
        s = root + h
        if s < 0 or s > 1:
            s = -root+h
    else:
        s = volume_parameter.range[0]
    
    # verifying if everything is OK
    if verbose:
        import pylab as P
        P.ion()
        P.figure(2)
        P.clf()
        x_values = N.arange(0.,1.,.01)
        # y_values = sum([ c[i]*x_values**i for i in range(nb_points) ]) for more than 2nd degree
        y_values = a*x_values**2 + b*x_values + c
        P.plot(x_values, y_values)
        P.plot(x_values, a*(x_values-h)**2+k)
        P.plot(values, peaks, 'x', ms=10)
        P.plot(s, target_peak, '*', ms = 15)
    # all this to have s as our volume
    
    if s > volume_parameter.range[1]:
        s = volume_parameter.range[1]
        
    if verbose:
        print 'volume parameter value'
        print s
        
    # we finally set the new value!
    volume_parameter.value = s

def rms(audio):
    """ Returns sqrt(mean(audio**2)). `audio` must be an 1D array. """
    #print '%.2f' % N.sqrt(N.mean(audio**2)),
    return N.sqrt(N.mean(audio**2))
    


def normalize_volume_presets(aupreset_file_or_dir, host, audiounit, volume_parameter, save_dir=None, target_peak=.1, verbose=False):
    """ Adjust the volume parameter of an audiounit so that the audiounit will output a know quantity of energy.
        Typically used to homogenize a list of .aupreset.
        Basically we calculate the peak in the audio signal for 3 values of volume_parameter ( min, max and (min+max)/2 )
        and extrapolate to find the value of volume_parameter that will give us a peak of target_peak.
        
        aupreset_file_or_dir
            A path pointing to a .aupreset file or a directory containing one or more .aupreset.
            
        host
            A pygmy.audiounit.Midi2AudioGenerator.
            The midifile property of the host is assumed to be set.
            Typically containing a single audiounit (corresponding to the .aupreset(s)).
            
        audiounit
            The audiounit for which we are gonna adjust the volume_parameter.
            Should be in the AUChainGroup of the host.
                        
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
        
        normalize_volume(host, volume_parameter, target_peak, verbose)
                   
        # and save
        new_preset = join(save_dir, p)

        if verbose:
            print 'Saving preset at', new_preset
        au.save_aupreset(new_preset)
        
# nv(save_dir, host, au, au.get_parameters()[89], '/Users/simon/tmp/test2', verbose=True)
        