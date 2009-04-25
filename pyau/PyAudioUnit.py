#
#  PyAudioUnit.py
#  
#
#  Created by simon on 24/03/09.
#  Copyright (c) 2009. All rights reserved.
#

import audiounit as au

from numpy.random import rand

class CAComponentDescription(object):
	"""
	wrap of c++ class CAComponentDescription
	"""
		
	def __init__(self, type='', subtype='', manufacturer=''):
		"""
		constructor
		type, subtype, manufacturer : 4 char long strings
		half-hack : if 'type' has type au.CAComponentDescription, we use it as our ca_component_description
		"""
		
		if isinstance(type, au.CAComponentDescription):
			self._ccd = type
		else:
			self._ccd = au.CAComponentDescription(type, subtype, manufacturer)
		
	def count(self):
		"""
		Gives the number of Components with this type/subtype/manufacturer
		(makes sens only when at least one is empty (''))
		"""
		return self._ccd.Count()
			
	type = property(lambda self : self._ccd.Type(), doc='Returns the Type of the Component.')
	subtype = property(lambda self : self._ccd.SubType(), doc='Returns the SubType of the Component.')
	manu = property(lambda self : self._ccd.Manu(), doc='Returns the Manufacturer of the Component.')
				
	def __str__(self):
		return "'" + (self.type if self.type != '\0\0\0\0' else r'\0\0\0\0') + "' '" \
				+ (self.subtype if self.subtype != '\0\0\0\0' else r'\0\0\0\0') + "' '" \
				+ (self.manu if self.manu != '\0\0\0\0' else r'\0\0\0\0') + "'"
	
			
class AudioUnit(object):
	""" Wrapper of an c++ AudiparpoUnitWrapper.
		Should not be created directly, but instead be taken from an AUChain.
	"""
	
	def __init__(self, real_audio_unit_wrapper):
		""" Constructor.
			Should not be called directly.
			Should be called from AUChain, when getting an audiosource, effect or output.
		"""
		self._auw = real_audio_unit_wrapper
		self._desc = None
		self._parameters = {}
		
	def _get_ccd(self):
		if self._desc is None:
			self._desc = CAComponentDescription(self._auw.Comp().Desc())
		return self._desc
					
	desc = property(_get_ccd, doc='Gets the CAComponentDescription associated with the AudioUnit')
	
	def get_parameters(self, scope = au.kAudioUnitScope_Global, element = 0):
		""" Returns the list of parameters of the audio unit for a scope and an element.
		"""
		# we keep somewhere the parameters so we don't do the next line each time
		if (scope, element) not in self._parameters:
			self._parameters[(scope, element)] = [Parameter(x) for x in self._auw.GetParameterList(scope, element)]
		return self._parameters[(scope, element)]

		
	def load_aupreset(self, aupreset_file):
		""" Sets the parameters of the Audio Unit according to those in the 'aupreset_file'.
		
			aupreset_file
				A path pointing the the .aupreset file.
		"""
		
		self._auw.LoadAUPresetFromFile(aupreset_file)
		
	def save_aupreset(self, aupreset_file):
		""" Saves the current setting of the parameters in a aupreset file.
		
			aupreset_file:
				Where to save the preset (usually a path pointing to a .aupreset file).
		"""
		self._auw.SaveAUPresetToFile(aupreset_file)
		
	def __str__(self):
		s = self.desc.__str__()
		return s
	
			
class AUChain(object):
	"""	Reprensents a chain of audio units : an audio source (e.g. instrument, generator, etc.) and a list of effects.
		Should not be created directly, but instead be taken from an AUChainGroup. 
	"""
	
	def __init__(self, real_auchain):
		""" Constructor.
			Should not be called directly.
		"""
		self._auchain = real_auchain	
		self._audiosource = None
		self._effects = None
		
	def _get_audiosource(self):
		if self._audiosource is None:
			self._audiosource = AudioUnit(self._auchain.GetAudioSource())
		return self._audiosource
		
	def _set_audiosource(self, desc):
		self._audiosource = None
		return AudioUnit(self._auchain.SetAudioSource(desc._ccd))
		
	audiosource = property( _get_audiosource,
						   _set_audiosource,
							doc='Get/Set the audiosource.\nSet takes a CAComponentDescription.')
	
	def _get_effects(self):
		if self._effects is None:
			self._effects = self._auchain.GetEffects()
			self._effects = [AudioUnit(e) for e in self._effects]
		return self._effects
		
	effects = property( _get_effects,
						doc='Get the list of effects.')
	
	def add_effect(self, desc):
		""" Adds an effect at the end of the chain. """
		self._effects = None
		return AudioUnit(self._auchain.AddEffect(desc._ccd))
		
	def remove_effect(self):
		""" Removes the last effect in the chain. """
		self._auchain.RemoveEffect()
		self._effects = None
		
	#TODO : verify if we need the next two methods
	def start():
		""" Starts the audio unit. """
		self._auchain.Start()
		
	def stop():
		""" Stops the audio unit. """
		self._auchain.Stop()
		
	def __str__(self):
		s = '( ' + self.audiosource.desc.__str__() + ' )'
		for e in self.effects:
			s += ' => '
			s += '( ' + e.desc.__str__() + ' )'
		return s
	
			
class AUChainGroup(object):
	""" Group of AUChains.
	"""
	
	def __init__(	self,
					#TODO : changer le CAComponentDescription de la ligne d'apres pour au.DEFAULT_OUTPUT_DESCRIPTION
					output_desc = CAComponentDescription('auou', 'def ', 'appl'),
					buffer_size = au.DEFAULT_BUFFER_SIZE,
					sample_rate = au.DEFAULT_SAMPLE_RATE):
		""" Constructor.
			
			output_desc
				CAComponentDescription representing the output
		"""
		self._acg = au.AUChainGroup(output_desc._ccd, buffer_size, sample_rate)
		self._au_chains = None
		self._output = None

	def add_audiosource(self, desc):
		""" Adds an AUChain (with audiosource described by 'desc') to the group. """
		self._au_chains = None
		return AudioUnit(self._acg.AddAudioSource(desc._ccd))
				
	def add_effect(self, desc, index_chain):
		""" Adds an effect at then end of the 'index_chain'-th AUChain. """
		return AudioUnit(self._acg.AddEffect(desc._ccd, index_chain))
		
	
	def get_audiosource(self, index):
		""" Gets the audiosource of the index-th AUGraph in the group. """
		return self.auchains[index]
		
	def _set_output(self, desc):
		self._acg.SetOutput(desc._ccd)
		self._output = None
		
	def _get_output(self):
		if self._output is None:
			self._output = AudioUnit( self._acg.GetOutput() )
		return self._output
	
	output = property(	_get_output,
						_set_output,
						doc='Gets/Sets the output unit.\nReturns an AudioUnit but takes a CAComponentDescription')
						
	def _get_auchains(self):
		if self._au_chains is None:
			self._au_chains = self._acg.GetAUChains()
			self._au_chains = [AUChain(x) for x in self._au_chains]
		return self._au_chains
		
	auchains = property(_get_auchains,
						doc='Gets the list of AUChains.')
						
	def start(self):
		""" Starts the group. """
		self._acg.Start()
		
	def stop(self):
		""" Stops the group. """
		self._acg.Stop()
		
	buffer_size = property( lambda self : self._acg.GetBufferSize,
							doc = 'Gets the buffer size of the AUChainGroup.')
	
	sample_rate = property( lambda self : self._acg.GetSampleRate,
							doc = 'Gets the sample rate of the AUChainGroup.')
							
	def __str__(self):
		s = 'AUChains :\n'
		for auc in self.auchains:
			s += ' ' + auc.__str__() + '\n'
		s += 'output :\n '
		s += self.output.__str__()		
		return s
		
		
class FileMidi2AudioGenerator(object):
	""" Takes a AUChainGroup and generates audio from midi files
		TODO : This class is currentlyt a work in progress.
	"""
	
	def __init__(self, auchain_group, midiDirectory, presetDirectory, outputDirectory):
		""" Constructor.
		
			auchain_group
				A AUChainGroup!
			midiDirectory
				A directory of midi files.
			presetDirectory
				A directory containing .aupreset files.
			outputDirectory
				Where to bounce the .wav files.
		"""
		
		#midiDirectory = au.FileSystemUtils_TrimTrailingSeparators(midiDirectory)
		#presetDirectory = au.FileSystemUtils_TrimTrailingSeparators(presetDirectory)
		#outputDirectory = au.FileSystemUtils_TrimTrailingSeparators(outputDirectory)

		instruments = au.FileSystemUtils_GetRelativeFilePaths(presetDirectory, ".aupreset")
				
		self._fm2ag = au.FileMidi2AudioGenerator(
			auchain_group._acg,
			midiDirectory,
			presetDirectory,
			instruments,
			outputDirectory,
			True, False, False)
			
	def generate_audio(self):
		""" Generates the .wav files. """
		self._fm2ag.GenerateAudio()
		

class Parameter(object):
	"""	Represents a parameter of an Audio Unit. """
	
	def __init__(self, real_parameter):
		""" Constructor.
			Should not be called directly but instead returned from an AudioUnit.
		"""
		self._param = real_parameter
		
	_info = property(lambda self : self._param.ParamInfo(), doc='Gets the AudioUnitParameterInfo of the parameter.')
	
	name = property(lambda self : self._param.GetName(), doc='Gets the name of the parameter.')
	
	value = property(
		lambda self : self._param.GetValue(),
		lambda self,x : self._param.SetValue(None, None, x),
		doc='Gets/Sets the value of the parameter.')
		
	unit = property(lambda self : self._param.GetParamTag(), doc = 'Gets a string representing the unit of the parameter.')
	
	def _get_range(self):
		return self._info.minValue, self._info.maxValue
	
	range = property(_get_range, doc='Gets the tuplet (minValue, maxValue) for the parameter.')
	
	default_value = property(lambda self : self._info.defaultValue, doc='Gets the default value for the parameter.')
	
	def _get_clumpID(self):
		has_clump, clumpID = self._param.GetClumpID()
		return clumpID if has_clump else None
	
	clumpID = property(_get_clumpID, doc="Gets the clump ID of the parameter (None if there isn't any)")
	
	def get_str_from_value(self, value=None):
		""" Returns a string representing the value.
			A value of 'None' says the use the current value of the parameter.
		"""
		if value is None:
			return self._param.GetStringFromValueCopy(None)
		else:
			temp = au.new_Float32p()
			au.Float32p_assign(temp, value)
			result = self._param.GetStringFromValueCopy(temp)
			au.delete_Float32p(temp)
			return result
		
	def get_value_from_str(self, string):
		""" Returns the value represented by a string. """
		return self._param.GetValueFromString(string)
		
	num_indexed_params = property(lambda self : self._param.GetNumIndexedParams(), doc='Gets the number of indexed parameters, 0 if the parameter is not indexed')
	
	def has_display_transformation(self):
		""" Tells if the parameter value needs to be transformed before displayed to the user.
		"""
		return self._param.HasDisplayTransformation()
		
	#TODO : deal with the differents diplay transformations
			
	def __str__(self):
		return '%s = %s %s' % (self.name, self.get_str_from_value(), self.unit)
		#return str(self.unit)
	
	def detailed_str(self):
		s = '%s | current value = %s | range = %s | default value = %s' % \
			(self.name, self.get_str_from_value(), self.range, self.get_str_from_value(self.default_value))
		if self.num_indexed_params > 0:
			s += ' | indexed parameter (%i)' % self.num_indexed_params
		return s
		
	
class Midi2AudioGenerator(object):
	""" Uses a AUChainGraph to transform a midi file to an audio file.
	"""
	
	def __init__(self, au_chain_group):
		""" Constructor. """
		self._m2ag = au.Midi2AudioGenerator(au_chain_group._acg)
		self._midifile = None
				
	def _set_midi(self, midifile):	
		self._midifile = midifile
		self._m2ag.LoadMidiFile(midifile)
		
	midifile = property(	lambda self : self._midifile,
							_set_midi,
							doc = 'Gets/sets the current midi file.\nUsually the number of tracks has to match the number of instruments (audiosources) in the AUChainGroup')
	
	def play(self):
		""" Plays the midi file using the AUChainGraph. """
		if self.midifile is None:
			print '\nYou have to set a midi file first'
		else:
			self._m2ag.PlayAudio()
		
	def bounce(wavfile_path):
		""" Renders the midi file using the AUChainGraph. """
		if self.midifile is None:
			print '\nYou have to set a midi file first'
		else:
			self._m2ag.BounceAudioToFile(wavefile_path)
			
	def reset(self):
		""" It isn't clear when it has to be called.
			At least when aupreset are changed in the audio units of the AUChainGroup...
			TODO : check that!!)
		"""
		self._m2ag.Reset()
		

		
	
def get_CAComponentDescriptions(desc):
	""" Gets all the CAComponentDescriptions that matches 'desc'.
		For example CAComponentDescription('aumu') would return all the components of type 'aumu'.
		
		desc
			The CAComponentDescription to be matched
	"""
	return [CAComponentDescription(x) for x in au.GetCAComponentDescriptions(desc._ccd)]

	
		
		

		
				
		
	
		

		
		
