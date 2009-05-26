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