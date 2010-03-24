/*
 *  AHHost.h
 *
 *  Created by simon on 20/04/09.
 *  Modified on march 16th 2010
 *
 * AudioUnit Host
 */
 
#ifndef __AHHOST__
#define __AHHOST__

#include <list>

#include "CAComponentDescription.h"
//#include "AUBuffer.h"
#include <CoreServices/../Frameworks/CarbonCore.framework/Headers/Files.h>
#include "AUOutputBL.h"
#include "CAStreamBasicDescription.h"
#include "CAAudioFileFormats.h"
#include "CAFilePathUtils.h"

#include "AHMidiPlayer.h"
#include "AHGraph.h"
#include "AHUtils.h"
#include "FileSystemUtils.h"



class AHHost
{
protected:
    Boolean listeningToMidi_;


    AHGraph graph_;
    AHMidiPlayer midiPlayer_;
    std::vector<AHTrack*> tracks_;

    int bufferSize_;
    int sampleRate_;
    
	MIDIClientRef client_;
	MIDIPortRef inputPort_;
    

    
public:
	AHHost();
	virtual ~AHHost();
    
    
    void LoadMidiFile(const std::string midiFile);
//	void LoadInstrument( const std::string& instrument, UInt32 busIndex = 0 );
	
	std::vector< std::list< std::vector<float> > > Bounce();
	void Play();
	void Stop();
	
    AHTrack* AddTrack(const string name, const string manu="");
    AHTrack* AddTrack(const CAComponentDescription instrumentDescription);
    void RemoveLastTrack();
    std::vector<AHTrack*>& GetTracks() { return tracks_; }
    
	//AUMidiPlayer& GetAUMidiPlayer() { return midiPlayer_; }
    void BounceToFile(const std::string& wavPath );
	
	//void ListenToMidi();
	//void StopListeningToMidi();
	
	static void MidiReadProc(const MIDIPacketList* pktlist, void* readProcRefCon, void* srcConnRefCon);
	
/*	static OSStatus RenderCallback(	void *							inRefCon,
							   AudioUnitRenderActionFlags *	ioActionFlags,
							   const AudioTimeStamp *			inTimeStamp,
							   UInt32							inBusNumber,
							   UInt32							inNumberFrames,
							   AudioBufferList *				ioData);*/
    

	
    
protected:

    ExtAudioFileRef CreateOutputFile( const std::string& outputFilePath);//, CAStreamBasicDescription& outputStreamDescription );
    //void RenderToFile(CAStreamBasicDescription& outputStreamDescription, ExtAudioFileRef wavFile);
	void RenderToFile(ExtAudioFileRef wavFile);
	std::vector< std::list< std::vector<float> > > RenderToBuffer();
	
    // TODO : mettre ca ailleurs?
	void GetOutputUnitStreamFormat(CAStreamBasicDescription &csbd);
    // TODO : verifier si on a besoin de ca
	void Reset();
};

#endif __AHHOST__