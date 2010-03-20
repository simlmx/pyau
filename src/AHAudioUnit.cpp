/*
 *  AHAudioUnit.cpp
 *
 *  Created by simon on 19/03/09.
 *  Modified by Simon on march 16th 2010
 *
 */

#include "AHAudioUnit.h"
#include <iostream>

using namespace std;


void AHAudioUnit::LoadAUPresetFromFile(string aupresetPath)
{
	SInt32 errorCode;
    CFDataRef xmlData;
	
    CFURLRef presetURL = CFURLCreateFromFileSystemRepresentation( kCFAllocatorDefault, (const UInt8*) aupresetPath.c_str(), aupresetPath.size(), false );
    //Boolean status = 
    CFURLCreateDataAndPropertiesFromResource( kCFAllocatorDefault, presetURL, &xmlData, NULL, NULL, &errorCode );
    
    CFStringRef errorString;
    CFPropertyListRef propertyListRef = CFPropertyListCreateFromXMLData( kCFAllocatorDefault, (CFDataRef) xmlData, kCFPropertyListMutableContainers, &errorString );
	
	SetAUPreset(propertyListRef);
    
    CFRelease(xmlData);
    CFRelease(presetURL);
    CFRelease(propertyListRef);
    if (errorString)
        CFRelease(errorString);
	
// old:   UInt32 dataSize = sizeof(CFPropertyListRef);
 //old:   verify_noerr( AudioUnitSetProperty( audioUnit_, kAudioUnitProperty_ClassInfo, kAudioUnitScope_Global, 0, &propertyListRef, dataSize) );
	
}
void AHAudioUnit::SaveAUPresetToFile(std::string aupresetPath)
{	
	CFPropertyListRef classInfo = NULL;
	GetAUPreset(classInfo);
	
	CFStringRef path = CFStringCreateWithCString(kCFAllocatorDefault, aupresetPath.c_str(), kCFStringEncodingMacRoman);
	CFURLRef fileUrl = CFURLCreateWithFileSystemPath(kCFAllocatorDefault, path, kCFURLPOSIXPathStyle, false);
	CFDataRef xmlData = CFPropertyListCreateXMLData(kCFAllocatorDefault, classInfo);
	SInt32 errorCode;
	CFURLWriteDataAndPropertiesToResource(fileUrl, xmlData, NULL, &errorCode);
    
    CFRelease(path);
    CFRelease(fileUrl);
    CFRelease(xmlData);
    CFRelease(classInfo);
}

list<AHParameter> AHAudioUnit::GetParameterList(AudioUnitScope scope, AudioUnitElement element)
{
	
	UInt32 size;
	AudioUnitGetProperty(AU(), kAudioUnitProperty_ParameterList, scope, element, NULL, &size);
	UInt32 nb_params = size/sizeof(AudioUnitParameterID);		
	AudioUnitParameterID data[nb_params];
	AudioUnitGetProperty(AU(), kAudioUnitProperty_ParameterList, scope, element, &data, &size);
	
	list<AHParameter> params;
	for(UInt32 i=0; i<nb_params; i++)
	{
		AHParameter p(AU(), data[i], scope, element);
		params.push_back(p);
	}
					
	return params;
}

bool AHAudioUnit::GetView()
{
    UInt32 dataSize = 0;
	OSStatus result = GetPropertyInfo(kAudioUnitProperty_GetUIComponentList,
                                      kAudioUnitScope_Global, 0,
                                      &dataSize, NULL);
    if (!dataSize)
        cout << "Carbon view";
	if (result || !dataSize) {
		dataSize = 0;
		result = GetPropertyInfo(kAudioUnitProperty_CocoaUI,
                                 kAudioUnitScope_Global, 0,
                                 &dataSize, NULL);
        if(!dataSize)
            cout << "Cocoa view";
        else
            cout << "No view";
		if (result || !dataSize)
			return false;
	}
	return true;    
}
