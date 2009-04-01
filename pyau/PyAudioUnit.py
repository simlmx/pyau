#
#  PyAudioUnit.py
#  
#
#  Created by simon on 24/03/09.
#  Copyright (c) 2009. All rights reserved.
#

import audiounit as au

class CAComponentDescription(object):
	"""
	wrap of c++ class CAComponentDescription
	"""
		
	def __init__(self, type='', subtype='', manufacturer=''):
		"""
		constructor
		type, subtype, manufacturer : 4 char long strings
		"""
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
		
class AudioUnitWrapper(object):
	""" Wrapper of an Audio Unit.
		Should not be created directly, but instead be taken from an AUChain.
	"""
	
	def __init__(self, real_audio_unit_wrapper):
		""" Constructor.
			Should not be called directly.
			Should be called from AUChain, when getting an instrument, effect or output.
		"""
		self._auw = real_audio_unit_wrapper
		self._desc = None
		
	def _get_ccd(self):
		if self._desc is None:
			temp = CAComponentDescription()
			temp._ccd = self._auw.Comp().Desc()
			self._desc = temp
		return self._desc
					
	desc = property(_get_ccd, doc='Gets the CAComponentDescription associated with the AudioUnit')
		

class AUChain(object):
	"""
	Reprensents a chain of audio units.
	"""
	
	def __init__(self, desc_instrument, desc_output, max_frames_per_slice=512, sample_rate=44100.):
		""" Constructor.
		
		desc_instrument :
			CAComponentDescription representing the instrument of the chain.
		desc_output :
			CAComponentDescription representing the output of the chain.
		max_frames_per_slice :
			Maximum number of frames per slice in each audio unit.
		sample_rate :
			Sample rate of the audio units.
		
		"""
		self._chain = au.AUChain(desc_instrument._ccd, desc_output._ccd, max_frames_per_slice, sample_rate)
		self._instrument = None
		self._output = None
		self._effects = None
		
	def _get_instrument(self):
		if self._instrument is None:
			self._instrument = AudioUnitWrapper(self._chain.GetInstrument())
		return self._instrument
		
	def _set_instrument(self, desc):
		self._chain.SetInstrument(desc._ccd)
		self._instrument = None
		
	instrument = property( _get_instrument,
						   _set_instrument,
							doc='Get/Set the instrument.\nSet takes a CAComponentDescription.')
			
	def _get_output(self):
		if self._output is None:
			self._output = AudioUnitWrapper(self._chain.GetOutput())
		return self._output
		
	def _set_output(self, desc):	
		self._chain.SetOutput(desc._ccd)
		self._output = None
		
	output = property( _get_output,
					   _set_output,
						doc='Get/Set the output.\nSet takes a CAComponentDescription.')
	
	def _get_effects(self):
		if self._effects is None:
			self._effects = self._chain.GetEffects()
			self._effects = map(lambda e : AudioUnitWrapper(e), self._effects)
		return self._effects
		
	effects = property( _get_effects,
						doc='Get the list of effects.')
	
	def AddEffect(self, desc):
		""" Adds an effect at the end of the chain. """
		self._chain.AddEffect(desc._ccd)
		self._effects = None
		
	def RemoveEffect(self):
		""" Removes the last effect in the chain. """
		self._chain.RemoveEffect()
		self._effects = None
		
	def __str__(self):
		s = '( ' + self.instrument.desc.__str__() + ' )'
		for e in self.effects:
			s += ' => '
			s += '( ' + e.desc.__str__() + ' )'
		s += ' => '
		s += '( ' + self.output.desc.__str__() + ' )'
		return s
		
	
						
		
	
	
#	void SetOutput(CAComponentDescription desc);
#	AudioUnitWrapper* GetOutput() { return output_; };
	
#	void AddEffect(CAComponentDescription desc);
#	void RemoveEffect();
#	AudioUnitWrapper* GetEffectAt(int index=0);
	
#	void Start();
#	void Stop();