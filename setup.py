# 
# setup for the audiounit extention
# since not used by many people, we can compile it separatly if we want it
#
# Simon Lemieux
# 19 jan 2010
#

from os.path import join
from setuptools import setup, Extension
import platform


if  platform.mac_ver()[0].rsplit('.',1)[0] == '10.6':
    publicutility_dir = '/Developer/Extras/CoreAudio/PublicUtility'
else:
    publicutility_dir = '/Developer/Examples/CoreAudio/PublicUtility'

src_dir = 'src'     

import numpy

ext = Extension('_pyau_swig',

       sources=['pyau/pyau.i',

                join( publicutility_dir, 'CACFDictionary.cpp' ),
                join( publicutility_dir, 'CACFArray.cpp' ),
                join( publicutility_dir, 'CAPersistence.cpp' ),
                join( publicutility_dir, 'CAAUParameter.cpp' ),
                join( publicutility_dir, 'CAAudioChannelLayoutObject.cpp' ),
                join( publicutility_dir, 'CAAudioChannelLayout.cpp' ),
                join( publicutility_dir, 'CAAudioUnit.cpp' ),
                join( publicutility_dir, 'CAAudioFileFormats.cpp' ),
                join( publicutility_dir, 'CAComponentDescription.cpp' ),
                join( publicutility_dir, 'CAFilePathUtils.cpp' ),
                join( publicutility_dir, 'CAStreamBasicDescription.cpp' ),
                join( publicutility_dir, 'AUOutputBL.cpp' ),
                join( publicutility_dir, 'CAComponent.cpp' ),
                
                join( src_dir, 'AHHost.cpp' ),
                join( src_dir, 'AHGraph.cpp' ),
                join( src_dir, 'AHMidiPlayer.cpp' ),
                join( src_dir, 'AHAudioUnit.cpp' ),
                join( src_dir, 'AHTrack.cpp' ),
                join( src_dir, 'AHParameter.cpp' ),								
                join( src_dir, 'AHUtils.cpp' ),
                join( src_dir, 'FileSystemUtils.cpp' ),

                
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
      ext_modules = [ext],
)
