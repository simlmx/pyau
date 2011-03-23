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

using namespace std;

class AHHost
{
protected:
    Boolean listeningToMidi_;
    //Boolean playing_;
    


    AHGraph graph_;
    AHMidiPlayer midiPlayer_;
    vector<AHTrack*> tracks_;

    int bufferSize_;
    int sampleRate_;
    
	MIDIClientRef client_;
	MIDIPortRef inputPort_;
    

    
public:
	AHHost();
	virtual ~AHHost();
    
    
    void LoadMidiFile(const string midiFile);
//	void LoadInstrument( const string& instrument, UInt32 busIndex = 0 );
	
	vector< list< vector<float> > > Bounce();
	void Play();
    void PlayAndBlock(); // same as Play() but without using a callback
	void Stop();
	
    AHTrack* AddTrack(const string name, const string manu="");
    AHTrack* AddTrack(const CAComponentDescription instrumentDescription);
    void RemoveLastTrack();
    vector<AHTrack*>& GetTracks() { return tracks_; }
    
	AHMidiPlayer* GetAHMidiPlayer() { return &midiPlayer_; }
    AHGraph* GetAHGraph() { return &graph_; }
    void BounceToFile(const string& wavPath );
	
	void ListenToMidi();
	void StopListeningToMidi();
    Boolean IsListeningToMidi() { return listeningToMidi_; }
    
    void ResetAudioUnits();
	
	static void MidiReadProc(const MIDIPacketList* pktlist, void* readProcRefCon, void* srcConnRefCon);
	
    static OSStatus PlayCallBack(	void *							inRefCon,
                                 AudioUnitRenderActionFlags *	ioActionFlags,
                                 const AudioTimeStamp *			inTimeStamp,
                                 UInt32							inBusNumber,
                                 UInt32							inNumberFrames,
                                 AudioBufferList *				ioData);
    
protected:

    ExtAudioFileRef CreateOutputFile( const string& outputFilePath);//, CAStreamBasicDescription& outputStreamDescription );
    //void RenderToFile(CAStreamBasicDescription& outputStreamDescription, ExtAudioFileRef wavFile);
	void RenderToFile(ExtAudioFileRef wavFile);
	vector< list< vector<float> > > RenderToBuffer();
	
    // TODO : mettre ca ailleurs?
	void GetOutputUnitStreamFormat(CAStreamBasicDescription &csbd);
    // TODO : verifier si on a besoin de ca
	void Reset();
};

#endif __AHHOST__