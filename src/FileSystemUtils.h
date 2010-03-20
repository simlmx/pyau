/*
 *  FileSystemUtils.h
 *  Midi2Audio
 *
 *  Created by sean on 16/02/09.
 *  Copyright 2009 __MyCompanyName__. All rights reserved.
 *
 */

#ifndef __FILE_SYSTEM_UTILS_HEADER_INCLUDED__
#define __FILE_SYSTEM_UTILS_HEADER_INCLUDED__

#include "CAFilePathUtils.h"

//temp
#include "CAComponentDescription.h"

class FileSystemUtils
{
public:
    static std::string GetFileName( const std::string& filePath, bool includeExtension = true );
	static std::string GetFileExtension( const std::string& filePath );
    static std::string GetParentDirectoryPath( const std::string& filePath );
    static void CreateDirectory( const std::string& directoryPath );
    
    static void GetFilePaths( const std::string& root, const std::string& extension, std::list<std::string>& filePaths );
    static void GetRelativeFilePaths( const std::string& root, const std::string& extension, std::list<std::string>& filePaths );
    static std::string TrimTrailingSeparators( const std::string& inputString );

    static std::string GetEscapedString( const std::string& inputString );

    static bool DeleteFile( const std::string& fileName );
	//static bool DeleteFile( const char* fname );
    
    static bool IsFileType( const std::string& filePath, const std::string& extension );
    static void str2OSType( const char* inString, OSType& outType );
	static void OSType2str( OSType inType, char * outString);
    
    //temp
    static void printDescName(CAComponentDescription desc);
};

#endif //__FILE_SYSTEM_UTILS_HEADER_INCLUDED__