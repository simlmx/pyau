%module audiounit



%{
#define SWIG_FILE_WITH_INIT
	
#include "AudioUnit/AUComponent.h"

#include "AUUtils.h"
#include "Defs.h"
#include "CAComponentDescription.h"
#include "CAAudioUnit.h"
#include "AudioUnitWrapper.h"
#include "AUChain.h"
#include "AUChainGroup.h"
#include "Midi2AudioGenerator.h"	
#include "FileSystemUtils.h"
#include "CAAUParameter.h"
#include "Parameter.h"
	
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

// some typedefs from AUComponent.h

typedef UInt32							AudioUnitPropertyID;
typedef UInt32							AudioUnitParameterID;
typedef UInt32							AudioUnitScope;
typedef UInt32							AudioUnitElement;
typedef	Float32							AudioUnitParameterValue;



typedef struct AUListenerBase *AUParameterListenerRef;

%pointer_functions(Float32, Float32p);
%pointer_functions(AUChainGroup, AUChainGroupp);

//
// %TEMPLATEs
//


%template(AudioUnitWrapperPtrList) std::list<AudioUnitWrapper*>;

%template(AUChainPtrVector) std::vector<AUChain*>;

%template(StringList) std::list<std::string>;

%template(ParameterList) std::list<Parameter>;

%template(CAComponentDescriptionList) std::list<CAComponentDescription>;

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
					if ( PyArray_SETITEM(array, itemptr, PyFloat_FromDouble((*it)[i])) )
					{
						printf("\nerror : failed setting array item");
						$result = PyArray_SimpleNew(0, NULL, 0);
					}
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

class FileSystemUtils
{
public:
	static void GetRelativeFilePaths( const std::string& root, const std::string& extension, std::list<std::string>& OUTPUT);
	static std::string TrimTrailingSeparators( const std::string& inputString );
};

// Defs.h

const UInt32 DEFAULT_BUFFER_SIZE = 512;
const Float64 DEFAULT_SAMPLE_RATE = 44100;

const std::string AUPRESET_EXTENSION = ".aupreset";
const std::string SOUNDFONT_EXTENSION = ".sf2";

// CAComponentDescription.h

class CAComponentDescription
{
public:
	CAComponentDescription (OSType inType, OSType inSubtype = 0, OSType inManu = 0);
	OSType	Type () const;
	OSType	SubType () const;
	OSType 	Manu () const;
	int		Count() const;
};

// CAComponent.h

class CAComponent
{
public:
	const CAComponentDescription&	Desc () const;
	CFStringRef		GetAUName () const { SetCompNames (); return mAUName ? mAUName : mCompName; }
};

// CAAudioUnit.h

class CAAudioUnit
{
public:
	const CAComponent&		Comp() const;
};

// AudioUnitWrapper.h

class AudioUnitWrapper : public CAAudioUnit
{
public:	
	AudioUnitWrapper(const AUNode &inNode, const AudioUnit& inUnit):CAAudioUnit(inNode, inUnit) {}

//	TODO : add some methods!
	virtual void LoadAUPresetFromFile(std::string aupresetPath);
	virtual void SaveAUPresetToFile(std::string aupresetPath);
	
	virtual std::list<Parameter> GetParameterList(AudioUnitScope scope, AudioUnitElement element);
	
//	virtual ~AudioUnitWrapper() {}
};

// AUChain.h

class AUChain
{
public:
	AUChain(CAComponentDescription audioSourceDescription, AUGraphWrapper& graph);
	AudioUnitWrapper& SetAudioSource(CAComponentDescription desc);
	AudioUnitWrapper& GetAudioSource() { return *audioSource_; }
	
	AudioUnitWrapper& AddEffect(CAComponentDescription desc);
	void RemoveEffect();	
	std::list<AudioUnitWrapper*> GetEffects() { reutrn effects_; }
};

// AUChainGroup.h

typedef std::vector<AUChain*> AUChainVector;

class AUChainGroup
{
public:
    AUChainGroup( CAComponentDescription outputDesc = GENERIC_OUTPUT_DESCRIPTION,
				 UInt32 bufferSize = DEFAULT_BUFFER_SIZE, Float64 sampleRate = DEFAULT_SAMPLE_RATE );
    
    AudioUnitWrapper& AddAudioSource( CAComponentDescription instrumentDescription );
	void RemoveAudioSource();
//    AudioUnitWrapper& GetAudioSource( UInt32 chainIndex );
	
//  AudioUnitWrapper* GetMixer() { return mixer_; }
//  void UpdateMixerConnections();
	
	AudioUnitWrapper& AddEffect(CAComponentDescription effectDescription, UInt32 chainIndex);
	AudioUnitWrapper& GetEffect(UInt32 chainIndex, UInt32 effectIndex);	
	void RemoveEffect(UInt32 chainIndex);
    
    void SetOutput(CAComponentDescription desc);
	AudioUnitWrapper& GetOutput() { return *output_; }
    
    AUChainVector& GetAUChains() { return auChains_; }
    AUChain& GetAUChain( UInt32 index = 0 );
    
    void Start() { graphWrapper_.Start(); }
	void Stop() { graphWrapper_.Stop(); }
    
    UInt32 GetBufferSize() { return graphWrapper_.GetBufferSize(); }
    Float64 GetSampleRate() { return graphWrapper_.GetSampleRate(); }
    AUGraph GetAUGraph() { return graphWrapper_.GetAUGraph(); }
};

// Midi2AudioGenerator.h

class Midi2AudioGenerator : public Midi2AudioGeneratorBase
{
public:
	Midi2AudioGenerator( AUChainGroup* auChainGroup);
    
    void LoadMidiFile(const std::string midiFile);
	
	std::vector< std::list< std::vector<float> > > GenerateAudio();
	void PlayAudio();
	
	void SetTrackInstrument(UInt32 trackIndex, UInt32 instrumentIndex);
	
    void Bounce( const std::string& wavPath );
};

// CAAUParameter.h

class CAAUParameter : public AudioUnitParameter {
public:
	CAAUParameter(AudioUnit au, AudioUnitParameterID param, AudioUnitScope scope, AudioUnitElement element);
	
	CAAUParameter(AudioUnitParameter &inParam);
	
	Float32						GetValue() const;
	
	void						SetValue(	AUParameterListenerRef			inListener, 
										 void *							inObject,
										 Float32							inValue) const;
	
	CFStringRef					GetName() const;  
	
	CFStringRef					GetStringFromValueCopy(const Float32 *value = NULL) const;	
	bool						ValuesHaveStrings () const;
	
	Float32						GetValueFromString (CFStringRef str) const;					
	
	const AudioUnitParameterInfo & ParamInfo() const;
	
	CFStringRef					GetParamTag() const	{ return mParamTag; }
	// this may return null! - 
	// in which case there is no descriptive tag for the parameter
	
	/*! @method GetParamName */
	CFStringRef					GetParamName (int inIndex) const;
	// this can return null if there is no name for the parameter
	
	int							GetNumIndexedParams () const;	

	bool						IsIndexedParam () const;	

	bool						HasNamedParams () const;	

	bool						GetClumpID (UInt32 &OUTPUT) const;	

	bool						HasDisplayTransformation () const;	

	bool						IsExpert () const;
};

// Parameter.h

class Parameter : public CAAUParameter
{
public:
	Parameter(AudioUnit au, AudioUnitParameterID param, AudioUnitScope scope, AudioUnitElement element)
:CAAUParameter(au, param, scope, element) {}
	Parameter(){}
};

// AUUtils.h

long CountAudioUnits(OSType AUType);
std::list<CAComponent> GetMatchingCAComponents(CAComponentDescription desc);