%module pyau_swig


%{
#define SWIG_FILE_WITH_INIT
	
#include "AudioUnit/AUComponent.h"

#include "AHUtils.h"
#include "AHDefs.h"
#include "CAComponentDescription.h"
#include "CAAudioUnit.h"
#include "AHAudioUnit.h"
#include "AHTrack.h"
//#include "AHGraph.h"
#include "AHHost.h"	
#include "FileSystemUtils.h"
#include "CAAUParameter.h"
#include "AHParameter.h"
	
#undef check
	
%}

%include "numpy.i"

%include cpointer.i


%include std_list.i
%include std_string.i
%include std_vector.i


%init %{
import_array();
%}



// some typedefs from MacTypes.h

typedef unsigned char                   UInt8;
typedef signed char                     SInt8;
typedef unsigned short                  UInt16;
typedef signed short                    SInt16;

#if __LP64__
typedef unsigned int                    UInt32;
typedef signed int                      SInt32;
#else
typedef unsigned long                   UInt32;
typedef signed long                     SInt32;
#endif

typedef float               Float32;
typedef double              Float64;

typedef SInt32                          OSStatus;

// some typedefs from AUComponent.h

typedef UInt32							AudioUnitPropertyID;
typedef UInt32							AudioUnitParameterID;
typedef UInt32							AudioUnitScope;
typedef UInt32							AudioUnitElement;
typedef	Float32							AudioUnitParameterValue;



typedef struct AUListenerBase *AUParameterListenerRef;

%pointer_functions(Float32, Float32p);
//%pointer_functions(AUChainGroup, AUChainGroupp);

//
// %TEMPLATEs
//


%template(AHAudioUnitPtrList) std::list<AHAudioUnit>;

%template(AHTrackPtrVector) std::vector<AHTrack*>;

//%template(StringList) std::list<std::string>;

%template(AHParameterList) std::list<AHParameter>;

//%template(CAComponentDescriptionList) std::list<CAComponentDescription>;

%template(CAComponentList) std::list<CAComponent>;

//%template(FloatVectorListVector) std::vector< std::list< std::vector<float> > >;

%template(FloatVector) std::vector<float>;
%template(FloatVectorList) std::list< std::vector< float > >;
%template(FloatVectorListVector) std::vector< std::list< std::vector< float > > >;
//%template(FloatVectorListVector) std::vector<std::list<std::vector<float> > >;

//
// %TYPEMAPs
//

// OSType

%include typemap_ostype.i

// CFStringRef

%include typemap_cfstringref.i

// FloatVectorListVector (this is used only for audio data in Midi2AudioGenerator)
%typemap(out) std::vector< std::list< std::vector< float > > >
{
	// vector< list< vector< float > > > 
	// (channels < list of buffers >)

	if ( $1.size() )
	{
		int nbChannels = $1.size();
		int bufferSize = $1[0].front().size();
		int nbBuffers = $1[0].size();

		int nd = 2;
		npy_intp dims [] = { nbChannels, bufferSize*nbBuffers };
		
		PyObject* array = PyArray_SimpleNew(nd, dims, PyArray_DOUBLE);

		for (int chan=0; chan<nbChannels; chan++)
		{
			int index = 0;
			for (std::list< std::vector< float > >::iterator it=$1[chan].begin(); it!=$1[chan].end(); it++)
			{
				for (int i=0; i<bufferSize; i++)
				{
					
                    void* itemptr = PyArray_GETPTR2(array, chan, index);
                    PyObject * newItem = PyFloat_FromDouble((*it)[i]);
					if ( PyArray_SETITEM(array, itemptr, newItem) )
					{
						printf("\nerror : failed setting array item");
						$result = PyArray_SimpleNew(0, NULL, 0);
                        return $result;
					}
                    else
                        Py_DECREF(newItem);
					index++;
				}
			}
		}
		$result = array;
	}
	else					
		$result = PyArray_SimpleNew(0, NULL, 0);//this case has not been tested yet	
	
}


//
// %INCLUDEs
//

// AudioUnitProperty.h

enum {
	kAudioUnitScope_Global	= 0,
	kAudioUnitScope_Input	= 1,
	kAudioUnitScope_Output	= 2,
	kAudioUnitScope_Group	= 3,
	kAudioUnitScope_Part	= 4,
	kAudioUnitScope_Note	= 5
};

typedef struct AudioUnitParameterInfo
{
	char						name[52];
	CFStringRef					unitName;
	UInt32						clumpID;
	CFStringRef					cfNameString;
	AudioUnitParameterUnit		unit;						
	AudioUnitParameterValue		minValue;			
	AudioUnitParameterValue		maxValue;			
	AudioUnitParameterValue		defaultValue;		
	UInt32						flags;				
} AudioUnitParameterInfo;

// FileSystemUtils.h
/*
class FileSystemUtils
{
public:
	static void GetRelativeFilePaths( const std::string& root, const std::string& extension, std::list<std::string>& OUTPUT);
	static std::string TrimTrailingSeparators( const std::string& inputString );
};*/

// Defs.h
//%include "AHDefs.h"
/*const UInt32 DEFAULT_BUFFER_SIZE = 512;
const Float64 DEFAULT_SAMPLE_RATE = 44100;

const std::string AUPRESET_EXTENSION = ".aupreset";
const std::string SOUNDFONT_EXTENSION = ".sf2";*/

// we should just write the functions we need... it might be faster at compiling
// but it was a pain when modifying the c++ code to update those...

//%include "CAComponentDescription.h"
%include "CAComponent.h"
%include "CAAudioUnit.h"
%include "AHAudioUnit.h"
%include "AHTrack.h"
//%include "AHGraph.h"
%include "AHHost.h"
%include "CAAUParameter.h"
%include "AHParameter.h"
%include "AHUtils.h"

//long CountAudioUnits(OSType AUType);
//std::list<CAComponent> GetMatchingCAComponents(CAComponentDescription desc);