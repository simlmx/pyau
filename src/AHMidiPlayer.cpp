/*
 *  AHMidiPlayer.cpp
 *
 *  Created by Sean on 28/03/09.
 *  Modified by Simon on march 16th 2010
 *
 */

#include "AHMidiPlayer.h"
#include <iostream>

using namespace std;

AHMidiPlayer::AHMidiPlayer(AHGraph* graph, std::vector<AHTrack*>* tracks) :
    graph_(graph),
    tracks_(tracks),
    musicSequenceLength_(0),
    musicSequenceLoadFlags_(0)
{
    PrintIfErr( NewMusicPlayer( &musicPlayer_ ) );
    PrintIfErr( NewMusicSequence( &musicSequence_ ) );
    PrintIfErr( MusicPlayerSetSequence( musicPlayer_, musicSequence_ ) );
    PrintIfErr( MusicSequenceSetAUGraph( musicSequence_, graph_->GetAUGraph() ) );
}

AHMidiPlayer::~AHMidiPlayer()
{
    UInt32 ntracks = GetTrackCount();
    MusicTrack track;
    //CAShow(musicSequence_);
    for( UInt32 trackIndex = 0; trackIndex < ntracks; ++trackIndex )
    {
        PrintIfErr( MusicSequenceGetIndTrack( musicSequence_, 0, &track ) );// 0 because we always delete the first one
        PrintIfErr( MusicSequenceDisposeTrack(musicSequence_, track) );
    }
    PrintIfErr( DisposeMusicPlayer( musicPlayer_ ) );
	PrintIfErr( DisposeMusicSequence( musicSequence_ ) );
}

void AHMidiPlayer::Reset()
{
    PrintIfErr( MusicPlayerSetTime( musicPlayer_, 0 ) );
    PrintIfErr( MusicPlayerPreroll( musicPlayer_ ) );
}

void AHMidiPlayer::Start()
{
    if( MusicPlayerStart( musicPlayer_ ) )
        printf("\nUnable to Play/Bounce. Have you set a midi file?");
}

void AHMidiPlayer::Stop()
{
    PrintIfErr( MusicPlayerStop( musicPlayer_ ) );
}

void AHMidiPlayer::CreateOneNote(int noteNumber, float duration, int velocity)
{
    // new music stuff
    MusicPlayer temp_musicPlayer;
    MusicSequence temp_musicSequence;
    PrintIfErr( NewMusicPlayer(&temp_musicPlayer));
    PrintIfErr( NewMusicSequence(&temp_musicSequence) );
    PrintIfErr( MusicPlayerSetSequence(temp_musicPlayer, temp_musicSequence) );
    

    // Disposing old music stuff
    MusicTrack track;
    UInt32 ntracks = GetTrackCount();
    for( UInt32 trackIndex = 0; trackIndex < ntracks; ++trackIndex )
    {
        PrintIfErr( MusicSequenceGetIndTrack( musicSequence_, 0, &track ) );// 0 because we always delete the first one
        PrintIfErr( MusicSequenceDisposeTrack(musicSequence_, track) );
    }
    PrintIfErr( DisposeMusicPlayer(musicPlayer_) );
    PrintIfErr( DisposeMusicSequence(musicSequence_) );
    
    // Create a MusicSequence with one track, one note called temp_musicSequence
    PrintIfErr(MusicSequenceNewTrack(temp_musicSequence, &track));
    MusicTimeStamp beat = 1.0;
    MIDINoteMessage mess;
    mess.channel = 0;
    mess.note = noteNumber;
    mess.velocity = velocity;
    mess.releaseVelocity = 0;
    mess.duration = duration;
    PrintIfErr(MusicTrackNewMIDINoteEvent(track, beat, &mess));

    musicPlayer_ = temp_musicPlayer;
    musicSequence_ = temp_musicSequence;
    
    PrintIfErr( MusicSequenceSetAUGraph(musicSequence_, graph_->GetAUGraph()) );
               

    // // figure out sequence length, and add 8 beats to the end of the file to take decay etc. into account
    MusicTimeStamp trackLength;
    UInt32 propsize = sizeof( MusicTimeStamp );
    
    ntracks = GetTrackCount();
    //CAShow(musicSequence_);
    musicSequenceLength_ = 0;
    for( UInt32 trackIndex = 0; trackIndex < ntracks; ++trackIndex )
    {        
        PrintIfErr( MusicSequenceGetIndTrack( musicSequence_, trackIndex, &track ) );
        PrintIfErr( MusicTrackGetProperty( track, kSequenceTrackProperty_TrackLength, &trackLength, &propsize ) );

        if ( trackLength > musicSequenceLength_ ) musicSequenceLength_ = trackLength;
    }
    musicSequenceLength_ += 8;
    
    SetupMidiChannelMapping();

}

void AHMidiPlayer::LoadMidiFile( const string& midiFilePath )
{
    // new music stuff
    MusicPlayer temp_musicPlayer;
    MusicSequence temp_musicSequence;
    PrintIfErr( NewMusicPlayer(&temp_musicPlayer));
	PrintIfErr( NewMusicSequence(&temp_musicSequence) );
    PrintIfErr( MusicPlayerSetSequence(temp_musicPlayer, temp_musicSequence) );

    CFURLRef url = CFURLCreateFromFileSystemRepresentation( kCFAllocatorDefault, (const UInt8*) midiFilePath.c_str(), midiFilePath.size(), false );
    if ( MusicSequenceFileLoad( temp_musicSequence, url, 0, kMusicSequenceLoadSMF_ChannelsToTracks ) )
    {
        printf("\nUnable to load midi file.");
        
        PrintIfErr( DisposeMusicPlayer(temp_musicPlayer) );
        PrintIfErr( DisposeMusicSequence(temp_musicSequence) );
        
        return;
    }
    
    // Disposing old music stuff
    MusicTrack track;
    UInt32 ntracks = GetTrackCount();
    for( UInt32 trackIndex = 0; trackIndex < ntracks; ++trackIndex )
    {
        PrintIfErr( MusicSequenceGetIndTrack( musicSequence_, 0, &track ) );// 0 because we always delete the first one
        PrintIfErr( MusicSequenceDisposeTrack(musicSequence_, track) );
    }
    PrintIfErr( DisposeMusicPlayer(musicPlayer_) );
    PrintIfErr( DisposeMusicSequence(musicSequence_) );
    
    musicPlayer_ = temp_musicPlayer;
    musicSequence_ = temp_musicSequence;
    
    PrintIfErr( MusicSequenceSetAUGraph(musicSequence_, graph_->GetAUGraph()) );
               

    // // figure out sequence length, and add 8 beats to the end of the file to take decay etc. into account
    MusicTimeStamp trackLength;
    UInt32 propsize = sizeof( MusicTimeStamp );
    
    ntracks = GetTrackCount();
    //CAShow(musicSequence_);
    musicSequenceLength_ = 0;
    for( UInt32 trackIndex = 0; trackIndex < ntracks; ++trackIndex )
    {        
        PrintIfErr( MusicSequenceGetIndTrack( musicSequence_, trackIndex, &track ) );
        PrintIfErr( MusicTrackGetProperty( track, kSequenceTrackProperty_TrackLength, &trackLength, &propsize ) );

        if ( trackLength > musicSequenceLength_ ) musicSequenceLength_ = trackLength;
    }
    musicSequenceLength_ += 8;
    
    SetupMidiChannelMapping();

}

void AHMidiPlayer::GetTime( MusicTimeStamp* currentTime )
{
    PrintIfErr( MusicPlayerGetTime(musicPlayer_, currentTime) );
}

UInt32 AHMidiPlayer::GetTrackCount()
{
    UInt32 numberOfTracks;
    PrintIfErr( MusicSequenceGetTrackCount( musicSequence_, &numberOfTracks ) );
    return numberOfTracks;
}


void AHMidiPlayer::SetTrackInstrument( UInt32 midiTrackIndex, UInt32 trackIndex )
{	
	AUNode node = tracks_->at(trackIndex)->GetSynth()->GetAUNode();
    MusicTrack track;
    PrintIfErr( MusicSequenceGetIndTrack( musicSequence_, trackIndex, &track ) );
    PrintIfErr( MusicTrackSetDestNode(track, node) );
	Reset();
}


void AHMidiPlayer::SetupMidiChannelMapping()
{
    size_t instrumentIndex = 0;
    size_t numberOfInstruments = tracks_->size();
    UInt32 numberOfTracks = GetTrackCount();
		
    for ( size_t trackIndex = 0; trackIndex < numberOfTracks; trackIndex++, instrumentIndex++ )
    {
        if ( instrumentIndex >= numberOfInstruments )        
            instrumentIndex = numberOfInstruments - 1;       
        
        SetTrackInstrument(trackIndex, instrumentIndex);
    }
}