/*
 *  AHTrack.h
 *
 *  Created by simon on 10/03/09.
 *  Modified by Simon on march 16th 2010
 *
 * The AHTrack contains an synth, and effects, which are linked together.
 */

#ifndef	__AHTRACK__
#define __AHTRACK__

#include <list>
#include <string>

#include "CAComponentDescription.h"

#include "AHAudioUnit.h"
#include "AHGraph.h"
#include "AHDefs.h"
#include "AHUtils.h"
#include "FileSystemUtils.h"

using namespace std;

class AHGraph;

class AHTrack
{
protected:
    AHGraph* graph_;

	
    AHAudioUnit* synth_;
	list<AHAudioUnit*> effects_;
    
    Boolean armed_; // if it listen to incoming midi
	
public:
    int trackIndex_;
	AHTrack(CAComponentDescription synthDescription, AHGraph* graph, int trackIndex);
	virtual ~AHTrack();
    
    AHAudioUnit* SetSynth(const string name, const string manu="");
	AHAudioUnit* SetSynth(const CAComponentDescription desc);
	AHAudioUnit* GetSynth() { return synth_; }
    
	
    AHAudioUnit* AddEffect(const string name, const string manu="");
	AHAudioUnit* AddEffect(const CAComponentDescription desc);
	void RemoveLastEffect();
//	AHAudioUnit* GetEffectAt(int index=0);
	list<AHAudioUnit*>& GetEffects() { return effects_; }
    
    void Arm() { armed_ = true; }
    void Unarm() { armed_ = false; }
    bool IsArmed() { return armed_; }
	
protected:
	void ConnectAllNodes() const;
    void DisconnectAllNodes() const;
};


#endif