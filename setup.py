# 
# setup for the audiounit extention
# since not used by many people, we can compile it separatly if we want it
#
# Simon Lemieux
# 19 jan 2010
#

from setuptools import setup, Extension
import platform


if  platform.mac_ver()[0].rsplit('.',1)[0] == '10.6':
    publicutility_dir = '/Developer/Extras/CoreAudio/PublicUtility/'
else:
    publicutility_dir = '/Developer/Examples/CoreAudio/PublicUtility/'

src_dir = 'src/AudioUnitHost/'     

import numpy

ext = Extension('_pyau_swig',

       sources=['pygmy/audiounit/pyau.i',

                publicutility_dir + 'CACFDictionary.cpp',
                publicutility_dir + 'CACFArray.cpp',
                publicutility_dir + 'CAPersistence.cpp',
                publicutility_dir + 'CAAUParameter.cpp',
                publicutility_dir + 'CAAudioChannelLayoutObject.cpp',
                publicutility_dir + 'CAAudioChannelLayout.cpp',
                publicutility_dir + 'CAAudioUnit.cpp',
                publicutility_dir + 'CAAudioFileFormats.cpp',
                publicutility_dir + 'CAComponentDescription.cpp',
                publicutility_dir + 'CAFilePathUtils.cpp',
                publicutility_dir + 'CAStreamBasicDescription.cpp',
                publicutility_dir + 'AUOutputBL.cpp',
                publicutility_dir + 'CAComponent.cpp',
                
                src_dir + 'AHHost.cpp',
                src_dir + 'AHGraph.cpp',
                src_dir + 'AHMidiPlayer.cpp',
                src_dir + 'AHAudioUnit.cpp',
                src_dir + 'AHTrack.cpp',
                src_dir + 'AHParameter.cpp',								
                src_dir + 'AHUtils.cpp',
                src_dir + 'FileSystemUtils.cpp',

                
                 ],
       include_dirs=[	src_dir,
                        publicutility_dir,
                        numpy.get_include(),
                        ],
       swig_opts=[	'-c++',
                    '-I' + src_dir,
                    '-I' + publicutility_dir,
                    '-modern',
                    ],
       extra_link_args=[
            '-framework', 'CoreFoundation',
            '-framework', 'CoreServices',
            '-framework', 'AudioToolbox',
            '-framework', 'AudioUnit',
            '-framework', 'CoreMIDI',               
            ],
       )

setup(name="pyau",
      version="0.1",
      description="Python AudioUnit host",
      long_description="""Python AudioUnit host""",
      author="Simon Lemieux and Sean Wood",
      author_email="lemieux.simon@gmail.com",
      ext_modules = [ext]
)
