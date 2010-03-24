/*
 *  AHGraph.h
 *
 *  Created by Sean on 28/03/09.
 *  Modified by Simon on march 16th 2010
 *  Copyright 2009 __MyCompanyName__. All rights reserved.
 *
 *  Contains the AUGraph, the mixer unit and the output unit, and makes the link with the tracks.
 */

#ifndef __AHGRAPH__
#define __AHGRAPH__

#include "AHAudioUnit.h"
#include "AHUtils.h"
#include "AHTrack.h"

#include "AudioToolbox/AudioToolbox.h"

#include <map>
#include <vector>

using namespace std;
class AHTrack;

class AHGraph
{
protected:
    AUGraph augraph_;

    vector<AHTrack*>* tracks_;    
    AHAudioUnit* mixer_;
    AHAudioUnit* output_;
      
public:
    AHGraph(vector<AHTrack*>* tracks);// CAComponentDescription outputDesc = DEFAULT_OUTPUT_DESCRIPTION,// todo : checker les defaults values
              //    UInt32 bufferSize = DEFAULT_BUFFER_SIZE, Float64 sampleRate = DEFAULT_SAMPLE_RATE );
    ~AHGraph();
    
public:
    void SetOutput(CAComponentDescription desc);
	AHAudioUnit* GetOutput() { return output_; }
      
    
    //UInt32 GetBufferSize() { return graphWrapper_->GetBufferSize(); }
    //Float64 GetSampleRate() { return graphWrapper_->GetSampleRate(); }
    AUGraph GetAUGraph() const { return augraph_; }
	
	//UInt32 GetAUChainCount() { return auChains_.size(); }
	
public:
    
    void ConnectMixerInputs() const;
    void ConnectMixerInputs(int trackIndex) const;
    void DisconnectMixerInputs() const;
    void DisconnectMixerInputs(int trackIndex) const;
    void UpdateGraph() const;

    
    AUNode GetLastNode(int track_index) const;
    
public:
    void Start() { PrintIfErr( AUGraphStart(augraph_) ); }
    void Stop() { PrintIfErr( AUGraphStop(augraph_) ); }
    
    AHAudioUnit* AddAHAudioUnitToGraph(CAComponentDescription desc) const;
    void RemoveAHAudioUnitFromGraph(AHAudioUnit* au) const;
    
};

#endif