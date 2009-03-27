#
#  PyAudioUnit.py
#  
#
#  Created by simon on 24/03/09.
#  Copyright (c) 2009. All rights reserved.
#

import audiounit as au

class CAComponentDescription:
	'''
	wrap of c++ class CAComponentDescription
	'''
	
	def __init__(self, type, subtype, manufacturer):
		self.ccd = au.CAComponentDescription()
		self.ccd.Type = type
		
	def __str__(self):
		return self.ccd.type() + ' ' + self.ccd.subtype() + ' ' + self.ccd.manufacturer()

class AUChain:
	'''
	reprensents a chain of audio units
	'''
	
	def __init__():
		pass