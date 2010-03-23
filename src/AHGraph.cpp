/*
 *  AHGraph.cpp
 *  Midi2Audio
 *
 *  Created by Sean on 28/03/09.
 *  Modified by Simon on march 16th 2010
 *
 */

#include "AHGraph.h"

#include <AudioToolbox/AudioToolbox.h>

using namespace std;
namespace
{
    const Float32 DEFAULT_MIXER_INPUT_VOLUME = 1;
    const Float32 DEFAULT_MIXER_OUTPUT_VOLUME = 1;
}

AHGraph::AHGraph(std::vector<AHTrack*>* tracks)//( CAComponentDescription outputDescription /*=DEFAULT_OUTPUT_DESCRIPTION*/,
                    //        UInt32 bufferSize /*=DEFAULT_BUFFER_SIZE*/, Float64 sampleRate /*=DEFAULT_SAMPLE_RATE*/ )
:tracks_(tracks)
{
    PrintIfErr( NewAUGraph(&augraph_) );
    PrintIfErr( AUGraphOpen(augraph_) );
	PrintIfErr( AUGraphInitialize(augraph_) );
    
    // let's add the mixer
    mixer_ = AddAHAudioUnitToGraph(CAComponentDescription( kAudioUnitType_Mixer, kAudioUnitSubType_MultiChannelMixer, kAudioUnitManufacturer_Apple ) );
    PrintIfErr( AudioUnitSetParameter( mixer_->AU(), kMultiChannelMixerParam_Volume, kAudioUnitScope_Output, 0, DEFAULT_MIXER_OUTPUT_VOLUME, 0 ) );
    //todo : probablement quelques properties à setter
    output_ = NULL;
    SetOutput(DEFAULT_OUTPUT_DESCRIPTION);
}

AHGraph::~AHGraph()
{
    
    PrintIfErr( AUGraphStop(augraph_) );
	PrintIfErr( AUGraphUninitialize(augraph_) );		
	PrintIfErr( AUGraphClose(augraph_) );

    RemoveAHAudioUnitFromGraph(mixer_);
    RemoveAHAudioUnitFromGraph(output_);
    
    PrintIfErr( DisposeAUGraph(augraph_) );
}


void AHGraph::SetOutput(CAComponentDescription desc)
{
	Boolean wasRunning;
    PrintIfErr( AUGraphIsRunning(augraph_, &wasRunning) );
	if (wasRunning)
		Stop();
	//printf(wasRunning ? "was running" : "was not running");
	
    if (output_)
    {
        //disconnect mixer output
        PrintIfErr( AUGraphDisconnectNodeInput( augraph_, output_->GetAUNode(), 0 ) );
        PrintIfErr( AUGraphRemoveNode(augraph_, output_->GetAUNode()));
    }
    output_ = AddAHAudioUnitToGraph(desc);
	
    //connect mixer output
	PrintIfErr( AUGraphConnectNodeInput( augraph_, mixer_->GetAUNode(), 0, output_->GetAUNode(), 0 ) );
	PrintIfErr( AUGraphUpdate(augraph_, NULL) );
	if (wasRunning)
		Start();
}

void AHGraph::DisconnectMixerInputs() const
{    
    for ( int i = 0; i < int(tracks_->size()); i++ )
    {
        PrintIfErr( AUGraphDisconnectNodeInput( augraph_, mixer_->GetAUNode(), i ) );
    }
}

void AHGraph::DisconnectMixerInputs(int indexTrack) const
{    
    PrintIfErr( AUGraphDisconnectNodeInput( augraph_, mixer_->GetAUNode(), indexTrack ) );
}

void AHGraph::ConnectMixerInputs() const
{
    AudioUnit mixerAU = mixer_->AU();
    AUNode mixerAUNode = mixer_->GetAUNode();
    UInt32 nbOfTracks = tracks_->size();
    
	PrintIfErr( AudioUnitSetProperty( mixerAU, kAudioUnitProperty_ElementCount, kAudioUnitScope_Input, 0, &nbOfTracks, sizeof(nbOfTracks) ) );
	
	for(UInt32 i = 0; i<nbOfTracks; i++)
	{
		PrintIfErr( AUGraphConnectNodeInput( augraph_, GetLastNode(i), 0, mixerAUNode, i ) );
        PrintIfErr( AudioUnitSetParameter( mixerAU, kMultiChannelMixerParam_Volume, kAudioUnitScope_Input, i, DEFAULT_MIXER_INPUT_VOLUME, 0 ) );
	}

    PrintIfErr( AUGraphUpdate(augraph_, NULL));
}

void AHGraph::ConnectMixerInputs(int indexTrack) const
{
    //CAShow(augraph_);
    AUNode mixerAUNode = mixer_->GetAUNode();
    	
    PrintIfErr( AUGraphConnectNodeInput( augraph_, GetLastNode(indexTrack), 0, mixerAUNode, indexTrack ) );
    
    //CAShow(augraph_);
    PrintIfErr( AUGraphUpdate(augraph_, NULL));
}

AUNode AHGraph::GetLastNode(int track_index) const
{
    AHTrack* track = tracks_->at(track_index);
    list<AHAudioUnit*>& effects = track->GetEffects();
    
    return effects.size() ? effects.back()->GetAUNode() : track->GetSynth()->GetAUNode();
}

AHAudioUnit* AHGraph::AddAHAudioUnitToGraph(CAComponentDescription desc) const
{
    
    AUNode node;
	AudioUnit au;
	PrintIfErr( AUGraphAddNode(augraph_, &desc, &node ) );
	PrintIfErr( AUGraphNodeInfo(augraph_, node, NULL, &au) );
    
	/*AudioUnitSetProperty( au, kAudioUnitProperty_SampleRate,
     kAudioUnitScope_Output, 0,
     &sampleRate_, sizeof(sampleRate_) );
     
     AudioUnitSetProperty( au, kAudioUnitProperty_MaximumFramesPerSlice,
     kAudioUnitScope_Global, 0,
     &bufferSize_, sizeof(bufferSize_) );
     */ 
    // todo : verifier que ces trucs commentés là sont mis ailleurs
	
    
    return new AHAudioUnit(node, au);
}

void AHGraph::RemoveAHAudioUnitFromGraph(AHAudioUnit* au) const
{
    PrintIfErr( AUGraphRemoveNode(augraph_, au->GetAUNode()) );
    delete au;
}