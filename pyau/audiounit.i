%module audiounit



%{
#include "AUComponent.h"

#include "Defs.h"
#include "CAComponentDescription.h"
#include "CAAudioUnit.h"
#include "AudioUnitWrapper.h"
#include "AUChain.h"
#include "AUChainGroup.h"
#include "FileMidi2AudioGenerator.h"	
#include "FileSystemUtils.h"
#include "CAAUParameter.h"
#include "Parameter.h"

#undef check
%}


%include std_list.i
%include std_string.i

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

//
// %TEMPLATEs
//


%template(AudioUnitWrapperPtrList) std::list<AudioUnitWrapper*>;

%template(AUChainPtrList) std::list<AUChain*>;

%template(StringList) std::list<std::string>;


%template(ParameterList) std::list<Parameter>;



//
// %TYPEMAPs
//

// OSType

%typemap(in) OSType
{
	if (PyString_Size($input) == 0)
		$1 = 0;
	else
	{
		OSType a;
		FileSystemUtils::str2OSType(PyString_AsString($input) ,a);
		$1 = a;
	}
}

%typemap(out) OSType
{
	char temp[5];
	FileSystemUtils::OSType2str($1, temp);
	$result = PyString_FromStringAndSize(temp,4);
}

%typecheck(SWIG_TYPECHECK_STRING)
	OSType
{
	$1 = ( (PyString_Check($input) && PyString_Size($input)==4) || PyString_Size($input)==0 ) ? 1 : 0;
}

// CFStringRef

%include typemap_cfstringref.i

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
//	virtual void LoadAUPresetFromFile(std::string aupresetPath);
//	virtual void SaveAuPresetToFile(std::string aupresetPath);
	
	virtual std::list<Parameter> GetParameterList(AudioUnitScope scope, AudioUnitElement element);
	
//	virtual ~AudioUnitWrapper() {}
};

// AUChain.h

class AUChain
{
public:
	AUChain(CAComponentDescription audioSourceDescription, AUGraphWrapper& graph);
	void SetAudioSource(CAComponentDescription desc);
	AudioUnitWrapper& GetAudioSource() { return *audioSource_; }
	
	void AddEffect(CAComponentDescription desc);
	void RemoveEffect();	
	std::list<AudioUnitWrapper*> GetEffects() { reutrn effects_; }
};

// AUChainGroup.h

typedef std::list<AUChain*> AUChainList;

class AUChainGroup
{
public:
    AUChainGroup( CAComponentDescription outputDesc = GENERIC_OUTPUT_DESCRIPTION,
				 UInt32 bufferSize = DEFAULT_BUFFER_SIZE, Float64 sampleRate = DEFAULT_SAMPLE_RATE );
    
    void AddAudioSource( CAComponentDescription instrumentDescription );
//    AudioUnitWrapper& GetAudioSource( UInt32 chainIndex );
	
//  AudioUnitWrapper* GetMixer() { return mixer_; }
//  void UpdateMixerConnections();
    
    void SetOutput(CAComponentDescription desc);
	AudioUnitWrapper& GetOutput() { return *output_; }
    
    AUChainList& GetAUChains() { return auChains_; }
    AUChain& GetAUChain( UInt32 index = 0 );
    
    void Start() { graphWrapper_.Start(); }
	void Stop() { graphWrapper_.Stop(); }
    
    UInt32 GetBufferSize() { return graphWrapper_.GetBufferSize(); }
    Float64 GetSampleRate() { return graphWrapper_.GetSampleRate(); }
    AUGraph GetAUGraph() { return graphWrapper_.GetAUGraph(); }
};

// FileMidi2AudioGenerator.h

class FileMidi2AudioGenerator : public Midi2AudioGeneratorBase
{
public:
    FileMidi2AudioGenerator( AUChainGroup* auChainGroup, const std::string& midiParameter,
							const std::string& instrumentDirectory, const std::list<std::string>& instruments, const std::string& outputDirectory, 
							bool flattenMidiHierarchy = true, bool flattenSoundfontHierarchy = false, bool midiHierarchyBeforeSoundfont = false );

    void GenerateAudio();    
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