#!/usr/bin/env python

from pygmy.audiounit import *

import sys

def print_usage_and_exit():
	
	print
	print 'usage:'
	print 'python list_audio_units.py <type>'
	print '  prints all audio units of a certain type'
	print
	print '  example :'
	print '  "python list_audio_units.py aumu" will print all music devices'
	print '  "python list_audio_units.py aufx" will print all effects'
	print
	
	sys.exit()


if __name__ == '__main__':
	
	if len(sys.argv) < 2:
		print_usage_and_exit()
		
	type = sys.argv[1]
	
	desc = CAComponentDescription(type)
	
	print_matching_components(desc)
	