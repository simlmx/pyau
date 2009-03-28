%module audiounit


%{
#include "AUChain.h"
#include "AudioUnitWrapper.h"
#include "FileMidi2AudioGenerator.h"
#include "CAComponentDescription.h"
#include "Parameter.h"
	
#include "FileSystemUtils.h"
	

	
%}

%typemap(in) OSType
{
	OSType a;
	FileSystemUtils::str2OSType(PyString_AsString($input) ,a);
	$1 = a;
}

%typemap(out) OSType {
	char temp[5];
	FileSystemUtils::OSType2str($1, temp);
	$result = PyString_FromStringAndSize(temp,4);
}


%typecheck(SWIG_TYPECHECK_STRING)
	OSType
{
	$1 = (PyString_Check($input) && PyString_Size($input)==4) ? 1 : 0;
}

%include "AUChain.h"
%include "AudioUnitWrapper.h"
%include "FileMidi2AudioGenerator.h"
%include "CAComponentDescription.h"
%include "Parameter.h"









