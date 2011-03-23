#
#  pyau.py
#  
#
#  Created by simon on 24/03/09.
#  Copyright (c) 2009. All rights reserved.
#

__all__ = ['Host', 'print_audiounits']

from copy import deepcopy

from numpy.random import rand

import pyau_swig as au

# TODO : fix this : gui makes conflicts via ssh
#from au_gui import launch_gui

#try:
#    import IPython
#    IPython.Shell.hijack_tk()
#except:
#    pass

#import Tkinter
#Tkinter.Tk().withdraw() # hack
    

class Host(object):
    """ Host object which contains tracks. Can bounce, play etc.
    """

    def __init__(self):
        """ Constructor. """
        self._ah_host = au.AHHost()
        self._midifile = None
        self._tracks = None

    def _set_midi(self, midifile):	
        self._midifile = midifile
        self._ah_host.LoadMidiFile(midifile)
        
    midifile = property(    lambda self : self._midifile,
                            _set_midi,
                            doc = 'Gets/sets the current midi file path.\nUsually the number of tracks has to match the number of instruments (audiosources) in the AUChainGroup')
                            
    def play(self, block=False):
        """ Plays the midi file using the AUChainGraph. """
        if block:
            self._ah_host.PlayAndBlock()
        else:
            self._ah_host.Play()

    def stop(self):
        """ Stops the playing started with 'play'. """
        self._ah_host.Stop()

    def reset_audiounits(self):
        """ "Resets" audiounits... I'm not sure what it does exactly.
            It is supposed to clean internal buffers, e.g. for reverbs and delays.
            This function should not be used unless you know what you're doing!
        """
        self._ah_host.ResetAudioUnits()

    def bounce(self, wavfile_path=None):
        """ Renders the midi file.
        
            if 'wavfile_path' is specified, renders to that file
            if not (None) returns the audio in a numpy array
        """
        if wavfile_path is not None:
            self._ah_host.BounceToFile(wavfile_path)
        else:
            return self._ah_host.Bounce()
         
    def _get_tracks(self):
        """ Gets the tracks. """
        if self._tracks is None:
            self._tracks = map(Track, self._ah_host.GetTracks())
        return self._tracks
        
    tracks = property(_get_tracks, doc="Returns the host's tracks.")
    
    def add_track(self, name, manu=""):
        """ Add a new track with synth named "name" and manufacturere "manu" (optional). """
        self._tracks = None
        t = self._ah_host.AddTrack(name, manu)
        return Track(t) if t is not None else None
        
    def remove_last_track(self):
        """ Removes the last track from the host. """
        self._tracks = None
        self._ah_host.RemoveLastTrack()
        
    def __str__(self):
        s = ''
        if len(self.tracks) == 0:
            s += 'No Tracks\n'
        else:
            s += 'Tracks :\n'
            for i,t in enumerate(self.tracks):
                s += '%i: %s\n' % (i, t.__str__())
        return s
        
    #def __del__(self):
    #    super(Host, self).__del__()
    #    for t in self.tracks:
    #        del t.synth
    #        for e in t.effects:
    #            del e
    #        del t

class Track(object):
    """	Represents a chain of audio units : a synth and a list of effects.
        Should not be created directly, but instead be taken from a Host. 
    """

    def __init__(self, ah_track):
        """ Constructor.
            Should not be called directly.
        """
        self._ah_track = ah_track	
        self._synth = None
        self._effects = None

    def _get_synth(self):
        if self._synth is None:
            self._synth = AudioUnit(self._ah_track.GetSynth())
        return self._synth

    def _set_synth(self, name, manu=""):
        self._synth = None
        s = self._ah_track.SetSynth(name, manu)
        return AudioUnit(s) if s is not None else None

    synth = property( _get_synth,
                            _set_synth,
                            doc='Get/Set the synth.\nSet takes the name of the Audio Unit, and optionally his manufacturer.')

    def _get_effects(self):
        #todo cache this??? what doesn't it work?
        self._effects = self._ah_track.GetEffects()
        self._effects = map(AudioUnit, self._effects)
        return self._effects

    effects = property( _get_effects, doc='Get the list of effects.')
                        
    def add_effect(self, name, manu=""):
        """ Adds the effect named 'name' of manufacturer 'manu' (optional) at the end of the Track. """
        self._effects = None
        e = self._ah_track.AddEffect(name, manu)
        return AudioUnit(e) if e is not None else None
        
    def remove_last_effect(self):
        """ Removes the last effect of the track. """
        self._effects = None
        self._ah_track.RemoveLastEffect()
        
    def arm(self):
        """ Track will listen for incoming midi events. """
        self._ah_track.Arm()
    
    def unarm(self):
        """ Track won't listen for incoming midi events. """
        self._ah_track.Unarm()
        
    is_armed = property( lambda self : self._ah_track.IsArmed(), doc='Is the track armed (listening for incoming midi events)')

    def __str__(self):
        s = '[ ' + self.synth.name + ' ]'
        for e in self.effects:
            s += ' => '
            s += '[ ' + e.name + ' ]'
        if self.is_armed:
            s += ' -- ARMED'
        return s

class AudioUnit(object):
    """ Represents an AudioUnit.
        Should not be created directly, but instead be taken from an AHTrack.
    """

    def __init__(self, ah_audiounit):
        """ Constructor.
            Should not be called directly.
            Should be called from Track, when getting an synth or effect
        """
        self._ah_au = ah_audiounit
        self._desc = None
        self._ah_parameters = {}
        self._ah_parameters_dicts = {}
        self._last_aupreset = ''
        

    def get_parameters(self, scope = au.kAudioUnitScope_Global, element = 0):
        """ Returns the list of parameters of the audio unit for a scope and an element.
        """
        # we keep somewhere the parameters so we don't do the next line each time
        if (scope, element) not in self._ah_parameters:
            self._ah_parameters[(scope, element)] = [Parameter(x) for x in self._ah_au.GetParameterList(scope, element)]
        return self._ah_parameters[(scope, element)]
        
    def get_parameters_dict(self, scope = au.kAudioUnitScope_Global, element = 0):
        """ Returns the list of parameters of the audio unit for a scope and an element,
            but in a dictionary with keys = "name of the parameter" and values = "the parameter itself".
        """
        if (scope, element) not in self._ah_parameters_dicts:            
            params = self.get_parameters()
            names = [p.name for p in params]
            d = dict(zip(names, params))
            self._ah_parameters_dicts[(scope, element)] = d
        return self._ah_parameters_dicts[(scope, element)]

        
    def load_aupreset(self, aupreset_file):
        """ Sets the parameters of the Audio Unit according to those in the 'aupreset_file'.
        
            aupreset_file
                A path pointing the the .aupreset file.
        """
        
        self._ah_au.LoadAUPresetFromFile(aupreset_file)
        self._last_aupreset=aupreset_file
        
    def save_aupreset(self, aupreset_file):
        """ Saves the current setting of the parameters in a aupreset file.
        
            aupreset_file:
                Where to save the preset (usually a path pointing to a .aupreset file).
        """
        self._ah_au.SaveAUPresetToFile(aupreset_file)
        
    name = property(lambda self : self._ah_au.GetName(), doc = 'Returns the name of the audiounit')
    manu = property(lambda self : self._ah_au.GetManu(), doc = 'Returns the manufacturer of the audiounit')

    bypass = property(lambda self : self._ah_au.GetBypass(),
                      lambda self, x : self._ah_au.SetBypass(x),
                      doc = 'If True the audio unit passed its input unchanged through its output.')


    def gui(self):
        """ launches a basic gui for controlling the audiounit. """
        launch_gui(self)

    def __str__(self):
        s = '%s by %s' % (self.name, self.manu)
        return s
        
        
class Parameter(object):
    """	Represents a parameter of an Audio Unit. """

    def __init__(self, ah_parameter):
        """ Constructor.
            Should not be called directly but instead returned from an AudioUnit.
        """
        self._ah_parameter = ah_parameter

    _info = property(lambda self : self._ah_parameter.ParamInfo(), doc='Gets the AudioUnitParameterInfo of the parameter.')

    id = property(lambda self : self._ah_parameter.GetParameterID(), doc='Gets the ID of the parameter.')

    name = property(lambda self : self._ah_parameter.GetName(), doc='Gets the name of the parameter.')

    value = property(
        lambda self : self._ah_parameter.GetValue(),
        lambda self,x : self._ah_parameter.SetValue(None, None, x),
        doc='Gets/Sets the value of the parameter.')

    unit = property(lambda self : self._ah_parameter.GetParamTag(), doc = 'Gets a string representing the unit of the parameter.')

    def _get_range(self):
        return self._info.minValue, self._info.maxValue

    range = property(_get_range, doc='Gets the tuplet (minValue, maxValue) for the parameter.')

    default_value = property(lambda self : self._info.defaultValue, doc='Gets the default value for the parameter.')

    def _get_clumpID(self):
        has_clump, clumpID = self._ah_parameter.GetClumpID()
        return clumpID if has_clump else None

    clumpID = property(_get_clumpID, doc="Gets the clump ID of the parameter (None if there isn't any)")

    def get_str_from_value(self, value=None):
        """ Returns a string representing the value.
            A value of 'None' says the use the current value of the parameter.
        """
        if value is None:
            return self._ah_parameter.GetStringFromValueCopy(None)
        else:
            temp = au.new_Float32p()
            au.Float32p_assign(temp, value)
            result = self._ah_parameter.GetStringFromValueCopy(temp)
            au.delete_Float32p(temp)
            return result

    def get_value_from_str(self, string):
        """ Returns the value represented by a string. """
        return self._ah_parameter.GetValueFromString(string)

    num_indexed_params = property(lambda self : self._ah_parameter.GetNumIndexedParams(), doc='Gets the number of indexed parameters, 0 if the parameter is not indexed')

    def has_display_transformation(self):
        """ Tells if the parameter value needs to be transformed before displayed to the user.
        """
        return self._ah_parameter.HasDisplayTransformation()

    #TODO : deal with the differents diplay transformations

    def __str__(self):
        return '%s = %s %s' % (self.name, self.get_str_from_value(), self.unit)
        #return str(self.unit)

    #def __repr__(self):
    #    return '<Parameter %s>' % self.name

    def detailed_str(self):
        s = '%s | %s | current value = %s | range = %s | default value = %s' % \
            (self.id, self.name, self.get_str_from_value(), self.range, self.get_str_from_value(self.default_value))
        if self.num_indexed_params > 0:
            s += ' | indexed parameter (%i)' % self.num_indexed_params
        return s
		
	
                   
        
	
def print_audiounits():
    """ Prints all relevant audio units. """
    au.PrintAllAudioUnits()
