%module audiounit



%{
#include "AUComponent.h"
#include "Defs.h"
#include "CAComponentDescription.h"
#include "CAAudioUnit.h"
//#include "Parameter.h"
#include "AudioUnitWrapper.h"
#include "AUChain.h"
#include "AUChainGroup.h"
#include "FileMidi2AudioGenerator.h"	
#include "FileSystemUtils.h"
#include "Midi2AudioGeneral.h"
#undef check
%}


%include std_list.i
%include std_string.i

// somes typedefs from MacTypes.h

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

//
// %TEMPLATEs
//


%template(AudioUnitWrapperPtrList) std::list<AudioUnitWrapper*>;

%template(AUChainPtrList) std::list<AUChain*>;

%template(StringList) std::list<std::string>;



//
// %TYPEMAPs
//

//OSType

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

//
// %INCLUDEs
//
class FileSystemUtils
{
public:
	static void GetRelativeFilePaths( const std::string& root, const std::string& extension, std::list<std::string>& OUTPUT);
	static std::string TrimTrailingSeparators( const std::string& inputString );
};

const UInt32 DEFAULT_BUFFER_SIZE = 512;
const Float64 DEFAULT_SAMPLE_RATE = 44100;

const std::string AUPRESET_EXTENSION = ".aupreset";
const std::string SOUNDFONT_EXTENSION = ".sf2";

class CAComponentDescription
{
public:
	CAComponentDescription (OSType inType, OSType inSubtype = 0, OSType inManu = 0);
	OSType	Type () const;
	OSType	SubType () const;
	OSType 	Manu () const;
	int		Count() const;
};

class CAComponent
{
public:
	const CAComponentDescription&	Desc () const;
};

class CAAudioUnit
{
public:
	const CAComponent&		Comp() const;
};

class AudioUnitWrapper : public CAAudioUnit
{
public:	
	AudioUnitWrapper(const AUNode &inNode, const AudioUnit& inUnit):CAAudioUnit(inNode, inUnit) {}

//	TODO : add some methods!
//	virtual void LoadAUPresetFromFile(std::string aupresetPath);
//	virtual void SaveAuPresetToFile(std::string aupresetPath);
	
//	virtual std::list<Parameter> GetParameterList(AudioUnitScope scope, AudioUnitElement element);
	
//	virtual ~AudioUnitWrapper() {}
};

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

class FileMidi2AudioGenerator : public Midi2AudioGeneratorBase
{
public:
    FileMidi2AudioGenerator( AUChainGroup* auChainGroup, const std::string& midiParameter,
							const std::string& instrumentDirectory, const std::list<std::string>& instruments, const std::string& outputDirectory, 
							bool flattenMidiHierarchy = true, bool flattenSoundfontHierarchy = false, bool midiHierarchyBeforeSoundfont = false );

    void GenerateAudio();    
};


%include "Midi2AudioGeneral.h"

//%include "Parameter.h"
//%include "FileMidi2AudioGenerator.h"
