/*
 *  AHMidiPlayer.h
 *
 *  Created by Sean on 28/03/09.
 *  Modified by Simon on march 16th 2010
 *
 * Things for playing midi.
 */

#ifndef __AHMIDIPLAYER__
#define __AHMIDIPLAYER__

#include <string>
#include <AudioToolbox/MusicPlayer.h>
#include "AHGraph.h"
#include "AHTrack.h"
#include "AHUtils.h"
#include "AHDefs.h"

class AHMidiPlayer
{
protected:
    AHGraph* graph_;
    std::vector<AHTrack*>* tracks_;
    
    MusicPlayer musicPlayer_;
    MusicSequence musicSequence_;
    MusicTimeStamp musicSequenceLength_;
    MusicSequenceLoadFlags musicSequenceLoadFlags_;
    
public:
    AHMidiPlayer(AHGraph* graph, std::vector<AHTrack*>* tracks);
    ~AHMidiPlayer();
        
    void LoadMidiFile( const std::string& midiFile );
    void CreateOneNote(int noteNumber, float duration, int velocity);

    void GetTime( MusicTimeStamp* currentTime );
    MusicTimeStamp GetSequenceLength() { return musicSequenceLength_; }
    MusicSequence GetMusicSequence() { return musicSequence_; }
	MusicPlayer GetMusicPlayer() { return musicPlayer_; }
    UInt32 GetTrackCount();

    
    void Start();
    void Stop();
    void Reset();
    
protected:
    void SetTrackInstrument( UInt32 trackIndex, UInt32 audiosourceIndex );
    void SetupMidiChannelMapping();
};

#endif