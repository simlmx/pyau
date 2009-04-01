%module audiounit



%{
#include "CAComponentDescription.h"
//#include "CAAudioUnit"
#include "Parameter.h"
#include "AudioUnitWrapper.h"
#include "AUChain.h"
#include "FileMidi2AudioGenerator.h"
	
#include "FileSystemUtils.h"
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


%include "CAComponentDescription.h"
%include "Parameter.h"
%include "CAAudioUnit.h"
%include "AudioUnitWrapper.h"
%include "AUChain.h"
%include "CAComponent.h"
%include "FileMidi2AudioGenerator.h"











