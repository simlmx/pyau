default: swig

audiounit_wrap.cpp :  
	swig -Wall -I../../../src/midi2audio -I/Developer/Examples/CoreAudio/PublicUtility -c++ -python -o audiounit_wrap.cpp audiounit.i && mv audiounit.py ..

swig : audiounit_wrap.cpp







