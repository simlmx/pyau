/*
 *  AHUtils.cp
 *
 *  Created by simon on 18/02/09.
 *  Modified by Simon on march 16th 2010
 *
 */

#include "AHUtils.h"
#include "AHDefs.h"

#include "CAComponentDescription.h"
#include "CAComponent.h"
#include "CAAutoDisposer.h"

#include <list>
#include <iostream>

using namespace std;

long CountAudioUnits(OSType AUType)
{
	CAComponentDescription temp(AUType);
	return AudioComponentCount(&temp);
}

list<CAComponent> GetCAComponentsForAUType(OSType inAUType)
{	
	CAComponentDescription temp(inAUType);
	AudioComponentDescription* desc = &temp;
	list<CAComponent> AUs;
	AudioComponent current = 0;
	while(true)
	{
		current = AudioComponentFindNext(current, desc);
		if (current)
			AUs.push_back(current);
		else
			break;		
	}
	return AUs;
}

list<CAComponent> GetMatchingCAComponents(CAComponentDescription desc)
{	
	list<CAComponent> descs;
	AudioComponent current = 0;
	while(true)
	{
		current = AudioComponentFindNext(current,&desc);
		if (current)
			descs.push_back(CAComponent(current));
		else
			break;		
	}
	return descs;
}

void PrintAllAudioUnits()
{
    // lame way of printing components, but in a interesting (at least for the guy writing this comment) order
    for (int i=0; i<(int)(sizeof(AUDIO_OSTYPES)/sizeof(OSType)); i++)
    {
        cout << "\n------- " << NAMES_AUDIO_OSTYPES[i] << " -------" << endl << endl;
        list<CAComponent> liste = GetMatchingCAComponents(CAComponentDescription(AUDIO_OSTYPES[i]));
        for( list<CAComponent>::iterator it = liste.begin(); it != liste.end(); it++)
        {
            CFStringRef manu = it->GetAUManu();
            CFStringRef name = it->GetAUName();
            if (manu && name)
            {
                PrintCFStringRef(name); printf(" - ");
                PrintCFStringRef(manu);// printf(" - ");
            }
            //it->Desc().Print();
            printf("\n");
        }
    }
}

//"Copy Pasted" from CAComponent.cpp :  _ShowCF(...)
void PrintCFStringRef(CFStringRef str)
{
    if (CFGetTypeID(str) != CFStringGetTypeID()) {
		CFShow(str);
		return;
	}
    
	UInt32 len = CFStringGetLength(str);
	char* chars = (char*)CA_malloc (len * 2); // give us plenty of room for unichar chars
	if (CFStringGetCString (str, chars, len * 2, kCFStringEncodingUTF8))
		printf ("%s", chars);
	else
		CFShow (str);
    
	free (chars);
}
                               
void PrintIfErr(OSStatus err)
{
    if (err)
    {
        cerr << "\nThere has been an error in the AU Host : " << err;
        //throw;
    }
}

// manu is optional, we will return the first match we find.
// returns true if we found something, false if not.
Boolean FindAudioUnitFromName(string name, string manu, CAComponentDescription &desc_out)
{
    CFStringRef ref_name = CFStringCreateWithCString(kCFAllocatorDefault, name.c_str(), kCFStringEncodingUTF8);
    CFStringRef ref_manu = CFStringCreateWithCString(kCFAllocatorDefault, manu.c_str(), kCFStringEncodingUTF8);
    
    Boolean found = false;
    
    for (int i=0; i<int(sizeof(AUDIO_OSTYPES)/sizeof(OSType)); i++)
    {
        list<CAComponent> liste = GetMatchingCAComponents(CAComponentDescription(AUDIO_OSTYPES[i]));
        for( list<CAComponent>::iterator it = liste.begin(); it != liste.end(); it++)
        {
            CFStringRef current_name = it->GetAUName();
            CFStringRef current_manu = it->GetAUManu();
            
            // name
            if (CFStringCompare(ref_name, current_name,  kCFCompareCaseInsensitive) == kCFCompareEqualTo)
            {
                // manu if one was specified
                if (manu!="")
                {
                    if (CFStringCompare(ref_manu, current_manu,  kCFCompareCaseInsensitive) == kCFCompareEqualTo)
                    {
                        found = true;
                        desc_out = it->Desc();
                        break;
                    }
                }
                else
                {
                    found = true;
                    desc_out = it->Desc();
                    break;
                }
            }
        }
        if (found)
            break;
    }
    return found ? true : false;        
}