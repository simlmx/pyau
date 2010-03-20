/*
 *  Defs.h
 *
 *  Created by Sean on 28/03/09.
 *  Modified by Simon on march 16th 2010
 *
 * Several definitions.
 */

#ifndef __AHDEFS__
#define __AHDEFS__

#include <string>
#include <vector>
#include "CAComponentDescription.h"
//#include "CustomAUTypes.h"


const UInt32 DEFAULT_BUFFER_SIZE = 512;
const Float64 DEFAULT_SAMPLE_RATE = 44100;

//const std::string AUPRESET_EXTENSION = ".aupreset";
//const std::string SOUNDFONT_EXTENSION = ".sf2";

const CAComponentDescription GENERIC_OUTPUT_DESCRIPTION( kAudioUnitType_Output, kAudioUnitSubType_GenericOutput, kAudioUnitManufacturer_Apple );
const CAComponentDescription DEFAULT_OUTPUT_DESCRIPTION( kAudioUnitType_Output, kAudioUnitSubType_DefaultOutput, kAudioUnitManufacturer_Apple );

//const CAComponentDescription DEFAULT_INSTRUMENT_DESCRIPTION( kAudioUnitType_MusicDevice, kAudioUnitSubType_DLSSynth, kAudioUnitManufacturer_Apple );
//const CAComponentDescription KONTAKT_INSTRUMENT_DESCRIPTION( kAudioUnitType_MusicDevice, kAudioUnitSubType_Kontakt, kAudioUnitManufacturer_NativeInstruments );

const OSType AUDIO_OSTYPES[] = {'aumu', 'aufx', 'aumf'};
const std::string NAMES_AUDIO_OSTYPES[] = {"SYNTHS", "EFFECTS", "MUSIC EFFECTS"};


#endif
