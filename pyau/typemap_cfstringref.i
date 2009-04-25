// CFStringRef
// note : code greatly inspired from Andrew Choi's
// http://members.shaw.ca/akochoi-old/blog/2005/09-25/index.html

%{
#include <CoreFoundation/CoreFoundation.h>
%}

%typemap(in) CFStringRef {
	printf("in");
	
   if (!PyString_Check($input)) {
       PyErr_SetString(PyExc_ValueError, "Expecting a string");
       return NULL;
   }
   $1 = CFStringCreateWithCString(NULL, PyString_AsString($input), kCFStringEncodingMacRoman);

}

%typemap(freearg) CFStringRef {

  CFRelease($1);
}

%typemap(arginit) CFStringRef {

  $1 = NULL;
}

%typemap(out) CFStringRef {
	
	if($1)
	{
		unsigned int len = CFStringGetLength($1);
		char *buffer = (char*)malloc(len + 1);
		if (CFStringGetCString($1, buffer, len + 1, kCFStringEncodingMacRoman)) {
			$result = PyString_FromStringAndSize(buffer, len);
			free(buffer);
			//CFRelease($1);
		}
		else {
			PyErr_SetString(PyExc_ValueError, "Can't convert string");
			//CFRelease($1);
			return NULL;
		}
	}
	else
		$result = PyString_FromStringAndSize(0,0);
}
