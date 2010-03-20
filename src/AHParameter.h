/*
 *  AHParameter.h
 *
 *  Created by simon on 20/03/09.
 *  Modified by Simon on march 16th 2010
 *
 * Represents an Audio Unit parameter.
 */

#ifndef __AHPARAMETER__
#define __AHPARAMETER__

#include "CAAUParameter.h"

class AHParameter : public CAAUParameter
{
public:
	AHParameter(AudioUnit au, AudioUnitParameterID param, AudioUnitScope scope, AudioUnitElement element)
	:CAAUParameter(au, param, scope, element) {}
	
	AHParameter(){}
    
    AudioUnitParameterID GetParameterID() { return mParameterID; }
};


#endif

