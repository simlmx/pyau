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
    
import numpy
ext = Extension('_audiounit',

       sources=['pygmy/audiounit/audiounit.i',

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

                'src/midi2audio/AUChain.cpp',								
                'src/midi2audio/AUChainGroup.cpp',
                'src/midi2audio/AUGraphWrapper.cpp',
                'src/midi2audio/AUMidiPlayer.cpp',
                'src/midi2audio/AUUtils.cpp',
                'src/midi2audio/AudioUnitSFWrapper.cpp',
                'src/midi2audio/AudioUnitWrapper.cpp',
                'src/midi2audio/FileMidi2AudioGenerator.cpp',
                'src/midi2audio/FileSystemUtils.cpp',
                'src/midi2audio/LiveMidi2AudioGenerator.cpp',
                'src/midi2audio/Midi2AudioUtils.cpp',
                'src/midi2audio/Parameter.cpp',
                'src/midi2audio/Midi2AudioGenerator.cpp',
                
                'src/midi2audio/Midi2AudioGeneral.cpp',
                
                 ],
       include_dirs=[	'src/midi2audio',
                        #'/Developer/Examples/CoreAudio/PublicUtility',
                        '/Developer/Extras/CoreAudio/PublicUtility',#10.6?
                         numpy.get_include(),

                        ],
       swig_opts=[	'-c++',
                    '-Isrc/midi2audio',
                    #'-I/Developer/Examples/CoreAudio/PublicUtility',
                    '-I/Developer/Extras/CoreAudio/PublicUtility', # 10.6?
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

setup(name="audiounit",
      version="0.1",
      description="Python AudioUnit host",
      long_description="""Python AudioUnit host""",
      author="Simon Lemieux and Sean Wood",
      author_email="lemieux.simon@gmail.com",
      ext_modules = [ext]
)
