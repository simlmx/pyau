/*
 *  FileSystemUtils.cpp
 *  Midi2Audio
 *
 *  Created by sean on 16/02/09.
 *  Copyright 2009 __MyCompanyName__. All rights reserved.
 *
 */

#include <CoreFoundation/CoreFoundation.h>
#include <CoreServices/CoreServices.h>
#include <AudioToolbox/AudioToolbox.h>
#include <CoreMIDI/CoreMIDI.h>
#include <pthread.h>
#include <unistd.h>

#include <AUOutputBL.h>
#include "CAStreamBasicDescription.h"
#include "CAAudioFileFormats.h"
#include "CAFilePathUtils.h"

#include <iostream>
#include <list>
#include <string>
#include <sstream>
#include <sys/types.h>
#include <dirent.h>
#include <algorithm>
#include <cctype>

#include "FileSystemUtils.h"

using namespace std;

namespace
{
    const string CREATE_DIRECTORY_COMMAND_PREFIX( "mkdir -p " );
    const string DELETE_FILE_COMMAND_PREFIX( "rm -f " );
}

std::string FileSystemUtils::GetFileName( const std::string& filePath, bool includeExtension /*= true*/ )
{
    std::string fileName( filePath );

    size_t lastDirectorySeparatorLocation = fileName.rfind( "/" );
    if ( lastDirectorySeparatorLocation != std::string::npos )
    {
        fileName.erase( 0, lastDirectorySeparatorLocation + 1 );
    }

    if ( !includeExtension )
    {
        size_t extensionStartIndex = fileName.rfind( "." );
        if ( extensionStartIndex != std::string::npos )
        {
            fileName.erase( extensionStartIndex );
        }
    }
    
    return fileName;
}

std::string FileSystemUtils::GetFileExtension( const std::string& filePath )
{
    std::string extension( filePath );
    
    size_t lastPeriodLocation = extension.rfind( "." );
    if ( lastPeriodLocation != std::string::npos )
    {
        extension.erase( 0, lastPeriodLocation + 1 );
    }
    
    return extension;
}

string FileSystemUtils::GetParentDirectoryPath( const std::string& filePath )
{
    string parentDirectoryPath( filePath );
    size_t lastDirectorySeparatorLocation = parentDirectoryPath.rfind( "/" );
    if ( lastDirectorySeparatorLocation == std::string::npos )
    {
        return "";
    }
    
    parentDirectoryPath.erase( lastDirectorySeparatorLocation );
    return parentDirectoryPath;
}

void FileSystemUtils::CreateDirectory( const string& directoryPath )
{
    string escapedDirectoryPath = GetEscapedString(directoryPath);
    try
    {
        if ( access( directoryPath.c_str(), 0 ) )
        {
            system( ( CREATE_DIRECTORY_COMMAND_PREFIX + escapedDirectoryPath ).c_str() );
            /*if ( system( ( CREATE_DIRECTORY_COMMAND_PREFIX + directoryPath ).c_str() ) != 0 )
            {
                CreateDirectory( GetParentDirectoryPath( directoryPath ) );
                system( ( CREATE_DIRECTORY_COMMAND_PREFIX + directoryPath ).c_str() );
            }*/
        }
    }
    catch( ... )
    {
        cout << "midi2Audio ERROR: unable to create " << directoryPath << endl;
    }
}

void FileSystemUtils::GetFilePaths( const string& parameter, const string& extension, list<string>& filePaths )
{
    if ( IsFileType(parameter, extension) )
    {
        filePaths.push_back(parameter);
        return;
    }

    DIR* directory = opendir( parameter.c_str() );
    if ( directory == NULL )
    {
        return;
    }
    
    dirent* directoryEntry;
    while ( ( directoryEntry = readdir( directory ) ) != NULL )
    {
        if ( strcmp( directoryEntry->d_name, "." ) == 0 ||
             strcmp( directoryEntry->d_name, ".." ) == 0 ) continue;
    
        GetFilePaths( parameter + "/" + directoryEntry->d_name, extension, filePaths );
    }
    
    closedir( directory );
}

void FileSystemUtils::GetRelativeFilePaths( const std::string& root, const std::string& extension, list<string>& filePaths )
{
    if ( IsFileType(root, extension) )
    {
        string fileName = root;
        filePaths.push_back(fileName.replace( 0, GetParentDirectoryPath(fileName).size() + 1, "" ) );
        return;
    }

    // call function with absolute paths, then trim the paths
    string element;
    list<string> absoluteFilePaths;
    GetFilePaths( root, extension, absoluteFilePaths );
    for ( list<string>::iterator iter = absoluteFilePaths.begin(); iter != absoluteFilePaths.end(); ++iter )
    {
        if ( (*iter).find(root) == 0 )
        {
            string element = *iter;
            filePaths.push_back( element.replace( 0, root.size() + 1, "" ) );
        }
        else
        {
            cout << *iter << "isn't a child of " << root << "!!" << endl;
            continue;
        }
    }
    return;
}

bool FileSystemUtils::IsFileType( const std::string& filePath, const std::string& extension )
{
    string lowerCaseFilePath(filePath);
    string lowerCaseExtension(extension);
    std::transform( lowerCaseFilePath.begin(), lowerCaseFilePath.end(), lowerCaseFilePath.begin(), ::tolower );
    std::transform( lowerCaseExtension.begin(), lowerCaseExtension.end(), lowerCaseExtension.begin(), ::tolower );
    
    return lowerCaseFilePath.rfind( lowerCaseExtension, lowerCaseFilePath.size() - lowerCaseExtension.size() ) != std::string::npos;
}

std::string FileSystemUtils::TrimTrailingSeparators( const std::string& inputString )
{
    size_t index = inputString.size();
    while ( index > 0 )
    {
        if ( inputString.at( index - 1 ) != '/' )
        {
            break;
        }
        
        --index;
    }
    
    return inputString.substr( 0, index );
}


std::string FileSystemUtils::GetEscapedString( const std::string& inputString )
{
    stringstream escapedString;
    char currentCharacter;
    for ( int characterIndex = 0; characterIndex < inputString.size(); characterIndex++ )
    {
        currentCharacter = inputString.at(characterIndex);
        if ( currentCharacter == ' ' ||
             currentCharacter == '(' ||
             currentCharacter == ')'  ||
             currentCharacter == '\'' )
        {
            escapedString << "\\";
        }
        
        escapedString << currentCharacter;
    }
    
    return escapedString.str();
}

bool FileSystemUtils::DeleteFile( const string& fileName )
{
    try
    {
        // use this to determine if a file exists first
        FILE *f = fopen (fileName.c_str(), "r");
        if (f)
        {
            fclose (f);
            // wipe out the output file
            //char str[1024];
            //sprintf (str, "rm -f %s", fname);
            //system(str);
            system( ( DELETE_FILE_COMMAND_PREFIX + GetEscapedString(fileName) ).c_str() );
            return true;
        }
        return false;
        /*if ( access( fileName.c_str(), 0 ))
        {
            system( ( DELETE_FILE_COMMAND_PREFIX + fileName ).c_str() );
            return true;
        }*/
    }
    catch( ... )
    {
        return false;
    }
    return false;
}

void FileSystemUtils::str2OSType( const char* inString, OSType& outType )
{
	if( inString == NULL )
	{
		outType = 0;
		return;
	}
	
	size_t len = strlen(inString);
	if (len <= 4)
	{
		char workingString[5];
		
		workingString[4] = 0;
		workingString[0] = workingString[1] = workingString[2] = workingString[3] = ' ';
		memcpy (workingString, inString, strlen(inString));
		outType = 	*(workingString + 0) <<	24	|
					*(workingString + 1) <<	16	|
					*(workingString + 2) <<	8	|
					*(workingString + 3);
		return;
	}

	if (len <= 8) {
		if (sscanf (inString, "%lx", &outType) == 0) {
			printf ("* * Bad conversion for OSType\n"); 
			exit(1);
		}
		return;
	}
	printf ("* * Bad conversion for OSType\n"); 
	exit(1);
}

void FileSystemUtils::OSType2str( OSType inType, char * outString)
{
	char  b1,b2,b3,b4;
	b1 = (inType >> 24) & 255;
	b2 = (inType >> 16) & 255;
	b3 = (inType >> 8)  & 255;
	b4 = inType & 255;
	outString[0] = b1;
	outString[1] = b2;
	outString[2] = b3;
	outString[3] = b4;
	outString[4] = 0;
}

//temp for debug
void FileSystemUtils::printDescName(CAComponentDescription desc)
{
    char type[5];
    char subtype[5];
    char manu[5];
    OSType2str(desc.Type(), type);
    OSType2str(desc.SubType(), subtype);
    OSType2str(desc.Manu(), manu);
    
    printf("%s-%s-%s", type, subtype, manu);
}