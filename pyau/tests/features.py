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
from pygmy.projects.timbre.normalization import normalize
from pygmy.projects.timbre.fast_tsne import calc_tsne as tsne
from pygmy.projects.timbre.render.GraphWindow import GraphWindow

verbose = True

##
## calc feat init
##

features = 'mfcc dmfcc'.split()

params = C.assert_defaults()
for f in features:
    params['do_%s' % f] = C.COMPUTE
params['fs_target'] = -1
params['seglen_sec'] = .333

##
## audiounit stuff
##

desc = AU.CAComponentDescription('aumu', 'aut1', 'Alfa')

midi = '/Users/simon/tmp/48.mid'

g = AU.AUChainGroup()
au = g.add_audiosource(desc)

m2ag = AU.Midi2AudioGenerator(g)
m2ag.midifile = midi

##
## some directories/files consts
##

preset_dir = '/Users/simon/Library/Audio/Presets/' + au.manu + '/' + au.name + '/test2'
#preset_dir = '/Users/simon/tmp/test2'
presets = os.listdir(preset_dir)
#trim
for i,p in enumerate(presets):
    if not p.endswith('.aupreset'):
        del presets[i]

h5_dir = '/Users/simon/tmp/h5'
wav_dir = '/Users/simon/tmp/wav'


##
## calc_feat
##

feature_values = []

for p in presets:#[:10]:

    if verbose:
        print 'Working on preset %s' % p
    
    aupreset_filename = p
    filename = p[:-9]#we trim the .aupreset
    h5_filename = filename + '.h5'
    wave_filename = filename + '.wav'
    
    aupreset_path = os.path.join(preset_dir,aupreset_filename)
    wav_path = os.path.join(wav_dir, wave_filename)
    h5_path = os.path.join(h5_dir, h5_filename)
    
    au.load_aupreset(aupreset_path)
    if not os.path.exists(wav_path):
        m2ag.bounce(wav_path)
    
    # calculates the features and stores them in a h5 file
    C.calc_feat(wav_path, os.path.join(h5_dir, filename), params = params)
    
    # reads the features from the h5 file
    all_features_for_one_sound = []
    for f in features:
        all_features_for_one_sound.append(C.read_feature_file(h5_path, f)[0])
        
    feature_values.append(all_features_for_one_sound)

dim0 = len(feature_values)
dim1 = feature_values[0][0].shape[0]
dim2 = sum( [ feature_values[0][i].shape[1] for i in range(len(features)) ] )
#print dim0, dim1, dim2
# dim0 = nb of aupresets = nb of sounds
# dim1 = nb of steps in time where the features are calculated
# dim2 = total nb of features for a sound

data = N.empty((0, dim1, dim2), dtype=float)

#dim0
for son in feature_values:    
    #dim1 and dim2
    concatenated_features = N.empty((dim1, 0), dtype=float)

    for values in son:
        concatenated_features = N.hstack((concatenated_features, values))
        
    concatenated_features = concatenated_features.reshape((1, dim1, dim2))
    
    data = N.vstack((data, concatenated_features))
    
data2 = data.copy()
means, stds = normalize(data.reshape(dim0*dim1,dim2))

print data

#pour simplifier
#data = data[:,dim1//2,:]
data = data.mean(1)

data_2d = tsne(data, PERPLEX=21)

graph = NX.empty_graph(dim0)

pos = data_2d

gw = GraphWindow(500,400, graph, pos, presets)



@gw.event
def on_click_node(node):
    print node, ':', presets[node]
    au.load_aupreset(os.path.join(preset_dir, presets[node]))
    #print 'node %i (%s) has been clicked' % (node, ig.labels[node])
    
@gw.event
def on_key_press(symbol, modifiers):
    if modifiers & key.MOD_CTRL and symbol == key.P:
        print 'PANIC'
        m2ag.panic()

pyglet.app.run()

            

