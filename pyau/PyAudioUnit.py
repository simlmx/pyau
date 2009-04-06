#
#  PyAudioUnit.py
#  
#
#  Created by simon on 24/03/09.
#  Copyright (c) 2009. All rights reserved.
#

import pygmy.audiounit as au

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
		return (self.type if self.type != '\0\0\0\0' else r'\0\0\0\0') + "' '" \
				+ (self.subtype if self.subtype != '\0\0\0\0' else r'\0\0\0\0') + "' '" \
				+ (self.manu if self.manu != '\0\0\0\0' else r'\0\0\0\0') + "'"
		
class AudioUnit(object):
	""" Wrapper of an c++ AudioUnitWrapper.
		Should not be created directly, but instead be taken from an AUChain.
	"""
	
	def __init__(self, real_audio_unit_wrapper):
		""" Constructor.
			Should not be called directly.
			Should be called from AUChain, when getting an audiosource, effect or output.
		"""
		self._auw = real_audio_unit_wrapper
		self._desc = None
		
	def _get_ccd(self):
		if self._desc is None:
			self._desc = CAComponentDescription(self._auw.Comp().Desc())
		return self._desc
					
	desc = property(_get_ccd, doc='Gets the CAComponentDescription associated with the AudioUnit')
	
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
		self._auchain.SetAudioSource(desc._ccd)
		self._audiosource = None
		
	audiosource = property( _get_audiosource,
						   _set_audiosource,
							doc='Get/Set the audiosource.\nSet takes a CAComponentDescription.')
	
	def _get_effects(self):
		if self._effects is None:
			self._effects = self._auchain.GetEffects()
			self._effects = map(lambda e : AudioUnit(e), self._effects)
		return self._effects
		
	effects = property( _get_effects,
						doc='Get the list of effects.')
	
	def add_effect(self, desc):
		""" Adds an effect at the end of the chain. """
		self._auchain.AddEffect(desc._ccd)
		self._effects = None
		
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
		self._acg.AddAudioSource(desc._ccd)
		self._au_chains = None
	
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
			self._au_chains = map( lambda x : AUChain(x), self._au_chains)
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
		
		
#TODO : changer les noms des params dans le constructeur, idem dans la version c++
class FileMidi2AudioGenerator:
	""" TODO
	"""
	
	def __init__(self, auchain_group, midiDirectory, presetDirectory, outputDirectory):
		""" TODO """
		
		midiDirectory = au.FileSystemUtils_TrimTrailingSeparators(midiDirectory)
		presetDirectory = au.FileSystemUtils_TrimTrailingSeparators(presetDirectory)
		outputDirectory = au.FileSystemUtils_TrimTrailingSeparators(outputDirectory)

		temp = au.StringList()
		au.FileSystemUtils_GetRelativeFilePaths(presetDirectory, ".aupreset", temp)
		instruments = temp
		
		print midiDirectory
		print presetDirectory
		print outputDirectory
				
		self._fm2ag = au.FileMidi2AudioGenerator(
			auchain_group._acg,
			midiDirectory,
			presetDirectory,
			instruments,
			outputDirectory,
			True, False, False)
			
	def generate_audio(self):
		""" TODO """
		self._fm2ag.GenerateAudio()
		
		
		
	
		
				
		
	
		

		
		
