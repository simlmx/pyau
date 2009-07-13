import os
import numpy as N

import tables as T
import networkx as NX
#import itertools as IT
import pygmy.projects.timbre.h5io as h5io
from pygmy.projects.timbre.fast_tsne import calc_tsne as tsne

dir = '/Users/simon/Desktop/timbre/test3_mix'
h5 = '/Users/simon/tmp/big.h5'
h5 = T.openFile(h5)

mfcc = h5.getNode('/', 'mfcc')
paths = h5.getNode('/', 'rel_path')
labels = paths.read()
data = mfcc.read()[:,0,:]
print data.shape

pos_file = '/Users/simon/tmp/pos.txt'
lm_file = '/Users/simon/tmp/lm.txt'
if 1:

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

