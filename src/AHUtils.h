/*
 *  AHUtils.h
 *
 *  Created by simon on 18/02/09.
 *  Modified by Simon on march 16th 2010
 *
 * Utils.
 */

#ifndef __AHUTILS__
#define __AHUTILS__

#include "CAComponent.h"
#include <list>

long CountAudioUnits(OSType AUType);
std::list<CAComponent> GetCAComponentsForAUType(OSType inAUType);

// returns a list of CAComponentDescriptions that match the CAComponentDescription passed to the function
std::list<CAComponent> GetMatchingCAComponents(CAComponentDescription desc);

void PrintAllAudioUnits();

void PrintCFStringRef(CFStringRef str);

void PrintIfErr(OSStatus);

// manu is facultative, pass "" if you don't want to use it
Boolean FindAudioUnitFromName(std::string name, std::string manu, CAComponentDescription &desc_out);

#endif