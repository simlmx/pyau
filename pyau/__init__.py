try :
    from audiounit import *
except :
    print "Audiounit not working on this machine.\nIf you received this while running setup.py test don't worry unless you need to use audiounit CoreAudio sound generation"
import random_parameters
