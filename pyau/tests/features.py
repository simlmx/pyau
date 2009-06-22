#
#  features.py
#  Midi2Audio
#
#  Created by simon on 05/06/09.
#  Copyright (c) 2009 . All rights reserved.
#
import os

import numpy as N
import pylab as P
import networkx as NX
import pyglet
import pyglet.window.key as key

from pygmy.audio import calc_feat as C
import pygmy.audiounit as AU

verbose = True

#features = 'mfcc dmfcc'.split()
features = ['mfcc']

params = C.assert_defaults()
for f in features:
    params['do_%s' % f] = C.COMPUTE
params['fs_target'] = -1
params['seglen_sec'] = .333

from setup_m2ag import *

preset_dir = '/Users/simon/Library/Audio/Presets/' + au.manu + '/' + au.name + '/test3_mix'

def calculate_features(aupreset_path):
    """ Computes a .wav file and a .h5 files with features for an aupreset file. """    
    
    h5_path = aupreset_path[:-9] + '.h5'
    wav_path = aupreset_path[:-9] + '.wav'
            
    au.load_aupreset(aupreset_path)
    if not os.path.exists(wav_path):
        print 'bouncing'
        m2ag.bounce(wav_path)
    m2ag.bounce(wav_path)
    
    # calculates the features and stores them in a h5 file
    C.calc_feat(wav_path, h5_path[:-3], params = params)

def calculate_features_rec(preset_root_dirt):
    """ Computes the features using calculate_features for a whole directory recursively. """
    for root, dirs, files in os.walk(preset_root_dir): 
        for f in files:
            if not f.endswith('.aupreset'):
                continue

            aupreset_path = os.path.join(root, f)
            if verbose:
                print 'Working on preset %s' % aupreset_path
            
            calculate_features(aupreset_path)
