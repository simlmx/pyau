#
# Stuff for generating aupresets for Camel Crusher.
#
# february 19th 2010
# Simon Lemieux
#

import pygmy.audiounit.random_parameters.randfunc as RF
from param_randomizer import param_randomizer
from pygmy.audiounit.random_parameters.volume import normalize_volume

import numpy.random as NR

class camel_crusher_param_randomizer(param_randomizer):
    
    def __init__(self, au, m2ag, volume=.5):
        super(camel_crusher_param_randomizer, self).__init__(au, m2ag, volume)
        self.volume = volume
    
    def reset_parameters(self):
        super(camel_crusher_param_randomizer, self).reset_parameters()
        self.params_dict['MasterOn'].value = 1.
        self.params_dict['DistOn'].value = 1.
        self.params_dict['CompressOn'].value = 1.
        
    def _used_parameters(self):
        used = []
        for s in ['Mech', 'Tube']:
            used.append('Dist%s' % s)
        for s in 'On Cutoff Res'.split():
            used.append('MmFilter%s' % s)
        for s in 'Amount Mode':
            used.append('Compress%s' % s)
        for s in 'Mix Volume':
            used.append('Master%s' % s)
        return used
    
    def randomize_parameters(self):
        
        # dist
        # 0. 2/3 of the time, uniform between 0. 1. for the rest of the time
        RF.randomize_parameter(self.params_dict['DistTube'], self.au, RF.uniform_custom(-2., 1.))
        self.params_dict['DistMech'].value = max(self.params_dict['DistMech'].value, 0.)
        RF.randomize_parameter(self.params_dict['DistTube'], self.au, RF.uniform_custom(-2., 1.))
        self.params_dict['DistTube'].value = max(self.params_dict['DistTube'].value, 0.)
        
        # cut off
        RF.randomize_parameter(self.params_dict['MmFilterOn'], self.au, RF.weighted_list([0., 1.], [.33, .67]))
        if self.params_dict['MmFilterOn'].value == 1.:
            RF.randomize_parameter(self.params_dict['MmFilterCutoff'], self.au, RF.uniform)
            RF.randomize_parameter(self.params_dict['MmFilterRes'], self.au, RF.uniform)
            
        # Compress
        # off half the time
        temp = RF.weighted_list([False, True], [.33, .67])(None, None)
        if temp:
            RF.randomize_parameter(self.params_dict['CompressAmount'], self.au, RF.uniform)
        RF.randomize_parameter(self.params_dict['CompressMode'], self.au, RF.weighted_list([0., 1.], [.5, .5]))
        
        # Master
        RF.randomize_parameter(self.params_dict['MasterMix'], self.au, RF.uniform)
        normalize_volume(self.m2ag, self.params_dict['MasterVolume'], target_peak=self.volume, volumes = [.5, .7, .9], verbose=False)
        
        #for p in self.params:
        #    if not p.name.startswith('Unused'):
        #        print p
                

        vol = self.params_dict['MasterVolume'].value
        if not (vol < 1. and vol > 0.):
            #print "let's do it again"
            raw_input('press enter to do it again')
            self.randomize_parameters()
        
        
        
            
