import os

import numpy as N
#import pylab as P
import networkx as NX
import pyglet
import pyglet.window.key as key

from setup_m2ag import *
from pygmy.audio import calc_feat as C
from pygmy.projects.timbre.fast_tsne import calc_tsne as tsne
from pygmy.projects.timbre.render.GraphWindow import GraphWindow
from pygmy.projects.timbre.normalization import normalize

import features as F
import parameter_gen_util as PA


preset_dir = '/Users/simon/Library/Audio/Presets/' + au.manu + '/' + au.name + '/test3_mix'

features = ['mfcc']

feature_values = []
labels = []

#compte =0
#ok = False
#min=99
for root, dirs, files in os.walk(preset_dir):   
    print 'now in dir %s' % root
    #if root.split('/')[-1] != 'test3_mix' and int(root.split('/')[-1]) == min:
    #    ok = True
    
    #if not ok:
    #    continue
    #compte +=1
    #if compte > 3:
    #    break
    for file in files:
        if not file.endswith('.h5'):
            continue        
        h5_path = os.path.join(root, file)
        
        # reads the features from the h5 file
        all_features_for_one_sound = []
        for f in features:
            try:
                all_features_for_one_sound.append(C.read_feature_file(h5_path, f)[0])
            except: 
                presets = map(int,h5_path[:-3].split('/')[-2:])
                print presets
                raw_input('press enter to continue')
                import parameter_gen_util as PA
                PA.mix_presets(*presets)
                au.save_aupreset(h5_path[:-3] + '.aupreset')
                os.remove(h5_path)
                os.remove(h5_path[:-3] + '.wav')
                
                
            while all_features_for_one_sound[-1].shape != (3,40):
                print 'redoing', file
                os.remove(h5_path)
                os.remove(h5_path[:-3] + '.wav')
                presets = map(int,h5_path[:-3].split('/')[-2:])
                PA.mix_presets(*presets)
                au.save_aupreset(h5_path[:-3] + '.aupreset')
                F.calculate_features(h5_path[:-3] + '.aupreset')
                all_features_for_one_sound[-1] = C.read_feature_file(h5_path, f)[0]
                
        feature_values.append(all_features_for_one_sound)
        labels.append('%s_%s' % tuple(h5_path[:-3].split('/')[-2:]))

dim0 = len(feature_values)
dim1 = feature_values[0][0].shape[0]
dim2 = sum( [ feature_values[0][i].shape[1] for i in range(len(features)) ] )
print dim0, dim1, dim2
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

print data.shape

#pour simplifier
#data = data[:,dim1//2,:]
data = data.mean(1)

N.savetxt('data.txt', data)

if 1:

    from pygmy.projects.timbre.knngrapher import buildKnnGraph
    
    #graph = NX.empty_graph(dim0)
    graph = buildKnnGraph(data,3)
    pos = tsne(data, PERPLEX=15)

    gw = GraphWindow(1000,900, graph, pos, labels)
    gw.colorizeAllGraph()

    @gw.event
    def on_click_node(node):
        print node, ':', labels[node]        
        au.load_aupreset( preset_dir + '/%s/%s.aupreset' % tuple(labels[node].split('_')) )
        #print 'node %i (%s) has been clicked' % (node, ig.labels[node])
        
    @gw.event
    def on_key_press(symbol, modifiers):
        if modifiers & key.MOD_CTRL and symbol == key.P:
            print 'PANIC'
            m2ag.panic()

    pyglet.app.run()

def find_neibhors(preset_no, n=12):
    preset = str(preset_no) + '.aupreset'
    idx = presets.index(preset)
    
    distances = [ [i, N.sum(N.abs(data_2d[idx] - data_2d[i]))] for i in range(data_2d.shape[0]) ]
    
    distances.sort(cmp= lambda x,y : -1 if x[1]<y[1] else 1)
    
    #print distances
    
    return [ presets[d[0]] for d in distances[1:11] ]
    