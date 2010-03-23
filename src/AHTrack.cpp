/*
 *  AHTrack.cpp
 *
 *  Created by simon on 10/03/09.
 *  Modified by Simon on march 16th 2010
 *
 */


#include "AHTrack.h"

#include <iostream>

using namespace std;

AHTrack::AHTrack(CAComponentDescription synthDescription, AHGraph* graph, int trackIndex)
{
    graph_ = graph;
    synth_ = graph_->AddAHAudioUnitToGraph(synthDescription);
    trackIndex_ = trackIndex;
    armed_ = false;
    ConnectAllNodes();
}

AHTrack::~AHTrack()
{
    graph_->RemoveAHAudioUnitFromGraph(synth_);
    for (list<AHAudioUnit*>::iterator it = effects_.begin(); it != effects_.end(); it++)
        graph_->RemoveAHAudioUnitFromGraph(*it);
}

AHAudioUnit* AHTrack::SetSynth(const CAComponentDescription desc)
{
    graph_->DisconnectMixerInputs(trackIndex_);
	DisconnectAllNodes();

    graph_->RemoveAHAudioUnitFromGraph(synth_);
		
	synth_ = graph_->AddAHAudioUnitToGraph(desc);
	
	ConnectAllNodes();
    graph_->ConnectMixerInputs(trackIndex_);
	
	return synth_;
}

AHAudioUnit* AHTrack::SetSynth(const string name, const string manu)
{
    CAComponentDescription desc;
    if (FindAudioUnitFromName(name, manu, desc))
    {
        return SetSynth(desc);
    }
    else
    {
        cout << "\nThe audio unit '" << name;
        if (!manu.empty())
            cout << "' - '" << manu;
        cout << "' could not be found";
        return NULL;
    }
}

AHAudioUnit* AHTrack::AddEffect(const CAComponentDescription desc)
{
    graph_->DisconnectMixerInputs(trackIndex_);
	DisconnectAllNodes();
	
	effects_.push_back( graph_->AddAHAudioUnitToGraph(desc) );
	
	ConnectAllNodes();
    graph_->ConnectMixerInputs(trackIndex_);
	
	return effects_.back();
}

AHAudioUnit* AHTrack::AddEffect(const string name , const string manu)
{
    CAComponentDescription desc; 
    if (FindAudioUnitFromName(name, manu, desc))
    {
        return AddEffect(desc);
    }
    else
    {
        cout << "\nThe audio unit '" << name;
        if (!manu.empty())
            cout << "' - '" << manu;
        cout << "' could not be found";
        return NULL;
    }
}

void AHTrack::RemoveLastEffect()
{
    graph_->DisconnectMixerInputs(trackIndex_);
	DisconnectAllNodes();

    graph_->RemoveAHAudioUnitFromGraph(effects_.back());
    
    effects_.pop_back();
    
	ConnectAllNodes();
    graph_->ConnectMixerInputs(trackIndex_);
}

void AHTrack::ConnectAllNodes() const
{
    if(effects_.size())
	{
		list<AHAudioUnit*>::const_iterator prev_it = effects_.begin(), it = effects_.begin();
		it++;
		
		PrintIfErr( AUGraphConnectNodeInput(graph_->GetAUGraph(),
                                            synth_->GetAUNode(),
                                            0,
                                            (*prev_it)->GetAUNode(),
                                            0) );

        
        if (effects_.size() > 1 )
        {
            while(it != effects_.end())
            {
                PrintIfErr( AUGraphConnectNodeInput(graph_->GetAUGraph(), (*prev_it)->GetAUNode(), 0, (*it)->GetAUNode(), 0) );
                it++;
                prev_it++;
            }
        }
    }
    //PrintIfErr(AUGraphUpdate(graph_->GetAUGraph(), NULL));
}

void AHTrack::DisconnectAllNodes() const
{
    if(!effects_.size()) return;

    for ( list<AHAudioUnit*>::const_iterator it = effects_.begin(); it != effects_.end(); it++ )
    {
        PrintIfErr( AUGraphDisconnectNodeInput( graph_->GetAUGraph(), (*it)->GetAUNode(), 0 ) );
    }
}

/*AHAudioUnit* AHTrack::GetEffectAt(int index)
{
	list<AHAudioUnit*>::iterator it = effects_.begin();
	for(int i=0; i<index; i++)
		it++;
	return &(*it);
}*/