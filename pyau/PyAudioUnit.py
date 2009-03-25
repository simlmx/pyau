#
#  PyAudioUnit.py
#  
#
#  Created by simon on 24/03/09.
#  Copyright (c) 2009. All rights reserved.
#

import _audiounit as AU

class CAComponentDescription:
	'''
	wrap of c++ class CAComponentDescription
	'''
	
	def __init__(self, type, subtype, manufacturer):
		self.ccd = AU.CAComponentDescription(type, subtype, manufacturer)
		
	def __str__(self):
		return self.ccd.type() + ' ' + self.ccd.subtype() + ' ' + self.ccd.manufacturer()

class AUChain:
	'''
	reprensents a chain of audio units
	'''
	
	def __init__():
		pass