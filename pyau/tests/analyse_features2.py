import os, sys
import numpy as N

import tables as T
import networkx as NX
#import itertools as IT
import pygmy.projects.timbre.h5io as h5io
from pygmy.projects.timbre.fast_tsne import calc_tsne as tsne

dir = '/Users/simon/Desktop/timbre/test3_mix'
h5 = '/Users/simon/tmp/big.h5'
h5 = T.openFile(h5)

paths = h5.getNode('/', 'rel_path')
labels = paths.read()

nb_mfcc = 12
mfcc = h5.getNode('/', 'mfcc')
dmfcc = h5.getNode('/', 'dmfcc')
data_mfcc = mfcc.read()[:,0,:nb_mfcc]
data_dmfcc_temp = dmfcc.read()[:,0,:]
data_dmfcc = data_dmfcc_temp[:,:nb_mfcc]
data_ddmfcc = data_dmfcc_temp[:, 40:40+nb_mfcc]

data = N.hstack((data_mfcc, data_dmfcc, data_ddmfcc))

feat_mean = N.mean(data,axis=0)
feat_cov = N.cov(data, rowvar=0)
print data.shape
print feat_mean.shape
print feat_cov.shape

sys.exit()

pos_file = '/Users/simon/tmp/pos.txt'
lm_file = '/Users/simon/tmp/lm.txt'


def find_neighbors(idx):
    
    feats = data[idx]
    label = labels[idx]
    path = paths[idx]


if 0:

    from pygmy.projects.timbre.knngrapher import buildKnnGraph
    from pygmy.projects.timbre.render.GraphWindow import GraphWindow
    import pyglet
    import pyglet.window.key as key
    
    from setup_m2ag import *

    nb_lm=6000
    graph = NX.empty_graph(nb_lm)
    #graph = 
    if os.path.exists(pos_file):
        print 'loading data'
        pos = N.loadtxt(pos_file)
        if os.path.exists(lm_file):
            lm = N.loadtxt(lm_file)
    else:
        print 'doing tsne'
        pos,lm = tsne(data, PERPLEX=15, LANDMARKS=1.*nb_lm/len(labels))
        N.savetxt(pos_file, pos)
        N.savetxt(lm_file, lm)
        
    print pos.shape#, type(pos), pos.shape
    print type(lm)
    lm = map(int,lm)
    
    gw = GraphWindow(1000,800, graph, pos, labels[lm])
    #gw.colorizeAllGraph()
    gw.draw_labels = False
    gw.colorizeAllNodes()

    @gw.event
    def on_click_node(node):
        print node, ':', labels[lm[node]]
        aupreset = dir + '/' + labels[lm[node]][:-3] + '.aupreset'
        print aupreset
        au.load_aupreset(aupreset)
        #print 'node %i (%s) has been clicked' % (node, ig.labels[node])
        
    @gw.event
    def on_key_press(symbol, modifiers):
        if modifiers & key.MOD_CTRL and symbol == key.P:
            print 'PANIC'
            m2ag.panic()

    pyglet.app.run()

